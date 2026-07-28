
import pytest
from playwright.sync_api import sync_playwright

from utils.artifact_manager import artifact
from utils.authentication.authentication_manager import auth
from utils.factories.browser_factory import BrowserFactory
from utils.file_utils import FileUtils
from utils.logger import logger
from utils.screenshot import Screenshot
from utils.config_manager import config



@pytest.fixture(scope="session")
def browser(playwright):
    # auth.clear_all_storage_states()
    browser = BrowserFactory.create_browser(playwright=playwright, config=config)
    yield browser
    logger.info("Closing Browser")
    browser.close()


@pytest.fixture(scope="session")
def playwright():
    logger.info("Starting Playwright engine")
    with sync_playwright() as p:
        yield p
    logger.info("Stopping Playwright engine")

@pytest.fixture(scope="function")
def context(browser,request):
    logger.info("Creating Browser Context with tracing and video recording enabled")
    browser_context = browser.new_context(record_video_dir = artifact.videos_dir)
    browser_context.tracing.start(screenshots=True, snapshots=True)
    yield browser_context
    logger.info("Closing Browser Context")
    test_name = FileUtils.sanitize_filename(request.node.name)
    trace_path = artifact.traces_dir/f"{test_name}.zip"
    browser_context.tracing.stop(path=artifact.traces_dir/f"{test_name}.zip")
    print(trace_path.exists())
    print(trace_path)
    browser_context.close()


@pytest.fixture(scope="function")
def authenticated_context(browser, request):

    logger.info("Creating Authenticated Browser Context")

    storage_state = auth.get_storage_state(browser=browser,role="user1")

    context = browser.new_context(storage_state=storage_state,record_video_dir=artifact.videos_dir)

    #context = browser.new_context(record_video_dir = artifact.videos_dir)

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


def create_page(context):
    page = context.new_page()
    page.goto(config.base_url)
    return page

@pytest.fixture
def page(context):

        logger.info("Opening New Page")

        page = create_page(context)

        yield page

        logger.info("Closing Page")

        page.close()



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