from __future__ import annotations
import platform
import shutil
import urllib.request
from pathlib import Path
import pytest
from playwright.sync_api import expect, sync_playwright
from api.product_api import ProductAPI
from flows.API_Flow.auth_flow import AuthFlow
from flows.API_Flow.auth_negative_flow import AuthNegativeFlow
from models.DummyJsonAPIModels.create_product_request import CreateProductRequest
from models.DummyJsonAPIModels.login_request import LoginRequest
from models.DummyJsonAPIModels.update_product_request import UpdateProductRequest
from utils.artifact_manager import artifact
from utils.authentication.authentication_manager import auth
from utils.factories.browser_factory import BrowserFactory
from utils.factories.user_factory import UserFactory
from utils.file_utils import FileUtils
from utils.logger import logger
from utils.screenshot import Screenshot
from utils.config_manager import config as framework_config
from utils.config_manager import CONFIG_DIR
from api.api_client import APIClient
from api.auth_api import AuthAPI
from api.dummyjson_auth_api import DummyJsonAuthAPI
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
    browser = BrowserFactory.create_browser(playwright=playwright, config=framework_config)
    yield browser
    logger.info("Closing Browser")
    browser.close()


@pytest.fixture(scope="function")
def context(browser,request):
    logger.info("Creating Browser Context with tracing and video recording enabled")
    browser_context = browser.new_context(record_video_dir = artifact.videos_dir)
    route_ads(browser_context)
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
    page.goto(framework_config.base_url)
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

    route_ads(context)

    context.tracing.start(screenshots=True,snapshots=True)

    yield context

    logger.info("Closing Authenticated Browser Context")

    test_name = FileUtils.sanitize_filename(request.node.name)

    context.tracing.stop(path=artifact.traces_dir / f"{test_name}.zip")

    context.close()




@pytest.fixture
def authenticated_page(authenticated_context):

    logger.info("Opening Authenticated Page")

    page = _create_page(authenticated_context)

    yield page

    logger.info("Closing Authenticated Page")

    page.close()


# -------------------------
# Pytest Hooks
# -------------------------


def pytest_configure(config):
    try:
        framework_config.configure(
            env=config.getoption("--environment"),
            browser=config.getoption("--browser"),
        )
    except (ValueError, FileNotFoundError) as exc:
        raise pytest.UsageError(str(exc))

    # Four expect() calls did not pass a timeout, so they used Playwright's 5s
    # default while the rest of the framework waited the configured 20s. Against a
    # slow public site that is the difference between a pass and a flake. Setting
    # it once means a new call site cannot get this wrong.
    expect.set_options(timeout=framework_config.expect_timeout)

    config.option.htmlpath = str(artifact.html_report)
    config.option.allure_report_dir = str(artifact.allure_results_dir)

    _write_allure_environment()
    _write_allure_categories()


def _write_allure_categories():
    """Copy the failure taxonomy into the results so Allure can classify.

    Without this the report's Categories panel is empty and every failure looks
    alike. Most of what has actually gone wrong here was not a product defect —
    the practice site challenges datacenter addresses and the DummyJSON API rate
    limits a busy runner — and those two deserve to be named rather than sitting
    in the same bucket as a real regression.
    """
    source = CONFIG_DIR / "allure_categories.json"
    if source.exists():
        shutil.copyfile(source, artifact.allure_results_dir / "categories.json")


def _write_allure_environment():
    # Without this the report's Environment panel is empty, so you cannot tell which
    # browser or which URL a published run actually used.
    values = {
        "Environment": framework_config.environment,
        "Browser": framework_config.browser,
        "Headless": framework_config.headless,
        "Base.URL": framework_config.base_url,
        "API.URL": framework_config.api_base_url,
        "DummyJSON.URL": framework_config.dummyjson_api_base_url,
        "Default.Timeout.ms": framework_config.timeout,
        "Expect.Timeout.ms": framework_config.expect_timeout,
        "Python": platform.python_version(),
        "Execution.ID": artifact.execution_id,
    }

    lines = "\n".join(f"{key}={value}" for key, value in values.items())
    (artifact.allure_results_dir / "environment.properties").write_text(lines + "\n")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    detail = config.stash.get(_SITE_UNREACHABLE, None)
    if detail:
        terminalreporter.write_sep(
            "=", "automationexercise.com skipped", yellow=True, bold=True,
        )
        terminalreporter.write_line(
            f"The site did not answer this host with JSON ({detail}). It sits behind "
            "Cloudflare, which challenges datacenter addresses, so these tests were "
            "skipped rather than failed. The DummyJSON API tests still ran."
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        page = (
            item.funcargs.get("page")
            or item.funcargs.get("authenticated_page")
        )

        if page:
            Screenshot.capture(page, item.name)

            logger.error(
                f"Test failed: {item.nodeid}. "
                f"Screenshot captured: {item.name}"
            )


_SITE_UNREACHABLE = pytest.StashKey[str]()


def _site_serves_us(url, timeout=20):
    """Is the practice site answering this machine normally?

    It is behind Cloudflare, which serves an HTML challenge to datacenter
    addresses. From a GitHub runner that means every test touching the site fails,
    and the failures look like defects: element not found, JSON decode error at
    char 0. They are not. Better to check once and skip with the reason than to
    publish a report full of failures nobody can act on.
    """
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "python-urllib (framework preflight)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(400).decode("utf-8", "replace").lstrip()
            return body[:1] in ("{", "["), f"HTTP {response.status}, body starts {body[:80]!r}"
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


def pytest_collection_modifyitems(config, items):
    # The UI tests drive a public practice site. Under parallel load it sometimes
    # answers a checkout click with neither the address page nor the register
    # prompt, and no wait fixes that because nothing is coming. Those get two
    # retries. API tests get none, and a real regression still fails every
    # attempt, so this hides flakiness in the target rather than in this code.
    for item in items:
        if "ui" in item.keywords:
            item.add_marker(pytest.mark.flaky(reruns=2, reruns_delay=3))

    # Everything except the DummyJSON tests needs automationexercise.com. Probe it
    # once; if it is not answering us with JSON, skip those with the reason rather
    # than letting them fail as though the framework were broken.
    needs_site = [
        i for i in items
        if "DummyJsonAPI" not in str(i.fspath) and ("ui" in i.keywords or "api" in i.keywords)
    ]

    if not needs_site:
        return

    reachable, detail = _site_serves_us(framework_config.api_base_url + "/productsList")

    if reachable:
        return

    config.stash[_SITE_UNREACHABLE] = detail
    skip = pytest.mark.skip(
        reason=f"automationexercise.com is not serving this host: {detail}"
    )
    for item in needs_site:
        item.add_marker(skip)


def pytest_addoption(parser):
    parser.addoption("--browser",action="store",default=None,help="Browser to execute tests: chromium, firefox, webkit")
    parser.addoption("--environment",action="store",default="qa",help="Environment to execute tests: qa, uat, prod")


# -------------------------
# API Fixtures
# -------------------------


#---------------------------
# Automation Exercise API fixture
#---------------------------


@pytest.fixture(scope="session")
def automation_exercise_api_client(playwright):
    logger.info("Creating Automation Exercise API request context")

    request_context = playwright.request.new_context(
        base_url=framework_config.api_base_url,
    )

    client = APIClient(
        request_context,
        framework_config.api_base_url,
    )

    yield client

    logger.info("Closing Automation Exercise API request context")
    request_context.dispose()



#---------------------------
# Dummy JSON API fixture
#---------------------------

@pytest.fixture(scope="session")
def dummyjson_api_client(playwright):
    logger.info("Creating DummyJSON API request context")

    request_context = playwright.request.new_context(
        base_url=framework_config.dummyjson_api_base_url,
    )

    client = APIClient(
        request_context,
        framework_config.dummyjson_api_base_url,
    )

    yield client

    logger.info("Closing DummyJSON API request context")
    request_context.dispose()


@pytest.fixture(scope="session")
def auth_api(automation_exercise_api_client):
    return AuthAPI(automation_exercise_api_client)

@pytest.fixture(scope="session")
def dummyjson_auth_api(dummyjson_api_client):
    return DummyJsonAuthAPI(dummyjson_api_client)

@pytest.fixture(scope="session")
def dummyjson_product_api(dummyjson_api_client):
    return ProductAPI(dummyjson_api_client)

@pytest.fixture
def product_flow(dummyjson_product_api):
    return ProductFlow(dummyjson_product_api)

@pytest.fixture(scope="session")
def auth_flow(auth_api):
    return AuthFlow(auth_api)

@pytest.fixture
def auth_negative_flow(auth_api,auth_flow):
    return AuthNegativeFlow(auth_api,auth_flow)


@pytest.fixture
def registered_user(auth_api):
    """A real account, created over the API and removed afterwards.

    The UI login tests used to read six accounts out of test_data/users/users.json
    and expect them to exist on the site. They are accounts on a shared public
    practice app, so they get deleted or reset by other people and the tests fail
    for reasons that have nothing to do with this code. Creating the account the
    test needs takes one API call and always works.
    """
    user = UserFactory.create()

    response, body = auth_api.register(user)
    assert response.status == 200, f"could not create the test account: {response.text()}"
    assert body.responseCode == 201, body.message

    yield user

    # Leave the practice site as we found it.
    try:
        auth_api.delete_user(user)
    except Exception as exc:
        logger.warning(f"could not delete {user.email}: {exc}")


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
    "adservice.google.com",
]


def block_ads(route):
    route.abort()


def route_ads(browser_context):
    # One glob per ad domain instead of routing "**/*" through Python. Matching stays in
    # the browser, so only requests we actually intend to block cross the boundary.
    for domain in AD_DOMAINS:
        browser_context.route(f"**/*{domain}/**", block_ads)

