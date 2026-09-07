import datetime

from loguru import logger
from playwright.sync_api import expect

from utils.screenshot import Screenshot


class BasePage:

    def __init__(self, page):
        self.page = page

    def _execute_action(self, action, operation, locator=None, description=None):
        logger.info(f"{operation}: {description}")
        try:
            result = action()
            logger.info(f"Successfully completed {operation} on {description}")
            return result
        except Exception as e:
            logger.exception(f"Failed {operation} on {description} [{locator}]")
            # Actions nest, so the same exception passes through here more than once.
            # Capture the first (innermost) failure only.
            if not getattr(e, "_screenshot_taken", False):
                self.screenshot(f"Failed {operation}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
                e._screenshot_taken = True
            raise

    def click(self, locator, description):
        self.wait_for_visibility(locator,description)
        return self._execute_action(
            action=lambda: locator.click(),
            operation="Click",
            locator=locator,
            description= description
        )

    def fill(self, locator, value, description):
        self.wait_for_visibility(locator,description)
        return self._execute_action(
            action=lambda:locator.fill(value),
            operation="Fill",
            locator=locator,
            description= description
        )

    def select_option(self, locator, value, description):
        self.wait_for_visibility(locator,description)
        return self._execute_action(
            action=lambda:locator.select_option(value=value),
            operation="Select Option",
            locator=locator,
            description= description

        )
    def get_text(self, locator, description):
        self.wait_for_visibility(locator,description)

        return self._execute_action(
            action=lambda: locator.text_content(),
            operation="Get Text",
            locator=locator,
            description= description
        )

    def is_visible(self, locator, description):
        return self._execute_action(
            action=lambda: locator.is_visible(),
            operation="Is Visible",
            locator=locator,
            description= description
        )

    def wait_for_visibility(self, locator, description):

        return self._execute_action(
            action=lambda:expect(locator).to_be_visible(),
            operation="Wait for Visible",
            locator=locator,
            description= description
        )

    def screenshot(self, name):
        logger.info(f"Saving screenshot {name}")
        Screenshot.capture(self.page, name)
