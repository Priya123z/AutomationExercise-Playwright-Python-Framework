from __future__ import annotations
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright
from api.product_api import ProductAPI
from models.create_product_request import CreateProductRequest
from models.login_request import LoginRequest
from models.update_product_request import UpdateProductRequest
from utils.artifact_manager import artifact
from utils.authentication.authentication_manager import auth
from utils.factories.browser_factory import BrowserFactory
from utils.file_utils import FileUtils
from utils.logger import logger
from utils.screenshot import Screenshot
from utils.config_manager import config
from api.api_client import APIClient
from api.auth_api import AuthAPI
from utils.test_data import TestData
from flows.API_Flow.product_flow import ProductFlow




# -------------------------
# Browser Fixtures
# -------------------------

@pytest.fixture(scope="session")
def playwright():
    logger.info("Starting Playwright engine")
    with sync_playwright() as p:
        yield p
    logger.info("Stopping Playwright engine")


@pytest.fixture(scope="session")
def browser(playwright):
    # auth.clear_all_storage_states()
    browser = BrowserFactory.create_browser(playwright=playwright, config=config)
    yield browser
    logger.info("Closing Browser")
    browser.close()


@pytest.fixture(scope="function")
def context(browser,request):
    logger.info("Creating Browser Context with tracing and video recording enabled")
    browser_context = browser.new_context(record_video_dir = artifact.videos_dir)

    browser_context.route("**/*",block_ads)

    browser_context.tracing.start(screenshots=True, snapshots=True)
    yield browser_context
    logger.info("Closing Browser Context")
    test_name = FileUtils.sanitize_filename(request.node.name)
    trace_path = artifact.traces_dir/f"{test_name}.zip"
    browser_context.tracing.stop(path=artifact.traces_dir/f"{test_name}.zip")
    logger.info(trace_path.exists())
    logger.info(trace_path)
    browser_context.close()


def _create_page(context):
    page = context.new_page()
    page.goto(config.base_url)
    return page


@pytest.fixture
def page(context):

        logger.info("Opening New Page")

        page = _create_page(context)

        yield page

        logger.info("Closing Page")

        page.close()


# -------------------------
# Authentication Fixtures
# -------------------------

@pytest.fixture(scope="function")
def authenticated_context(browser, request):

    logger.info("Creating Authenticated Browser Context")

    storage_state = auth.get_storage_state(browser=browser,role="user1")

    context = browser.new_context(storage_state=storage_state,record_video_dir=artifact.videos_dir)

    context.route("**/*",block_ads)

    context.tracing.start(screenshots=True,snapshots=True)

    yield context

    logger.info("Closing Authenticated Browser Context")

    test_name = FileUtils.sanitize_filename(request.node.name)

    context.tracing.stop(path=artifact.traces_dir / f"{test_name}.zip")

    context.close()




@pytest.fixture
def authenticated_page(authenticated_context):

    logger.info("Opening Authenticated Page")

    page = create_page(authenticated_context)

    yield page

    logger.info("Closing Authenticated Page")

    page.close()


# -------------------------
# Pytest Hooks
# -------------------------


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = item.funcargs.get("page")

        if page:

            Screenshot.capture(page, item.name)

def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chromium",
        help="Browser to execute tests"
    )


# -------------------------
# API Fixtures
# -------------------------


@pytest.fixture(scope="session")
def api_client(playwright):
    logger.info("Creating API request context")
    request_context = playwright.request.new_context(
        base_url=config.api_base_url,
        extra_http_headers={
            "Content-Type": "application/json",
            "Accept":"application/json"
        })
    client = APIClient(request_context)
    yield client
    logger.info("Closing API request context")
    request_context.dispose()


@pytest.fixture(scope="session")
def auth_api(api_client):
    return AuthAPI(api_client)



@pytest.fixture(scope="session")
def product_api(api_client):
    return ProductAPI(api_client)

@pytest.fixture
def product_flow():
    return ProductFlow()

# -------------------------
# Test Data Fixtures
# -------------------------


TEST_DATA_DIR = Path(__file__).parent / "test_data"/ "api"


@pytest.fixture(scope="session")
def login_request():
    return TestData.load(filepath = TEST_DATA_DIR/"login.json",model = LoginRequest)


@pytest.fixture(scope="session")
def create_product_request():
    return TestData.load(filepath = TEST_DATA_DIR/"create_product.json",model = CreateProductRequest)

@pytest.fixture(scope="session")
def update_product_request():
    return TestData.load(filepath = TEST_DATA_DIR/"update_product.json",model = UpdateProductRequest)[0]


#------------------------------
# AD - Block
#------------------------------


AD_DOMAINS = [
    "doubleclick.net",
    "googlesyndication.com",
    "googleadservices.com",
    "googleads.g.doubleclick.net",
    "adservice.google.com",
    "pagead2.googlesyndication.com",
]

def block_ads(route):
    url = route.request.url.lower()

    if any(domain in url for domain in AD_DOMAINS):
        logger.info(f"BLOCKED AD REQUEST: {url}")
        route.abort()
    else:
        route.continue_()

