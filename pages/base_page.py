import re
import datetime
from playwright.sync_api import Page, expect, Locator
from loguru import logger

from utils.config_manager import config


class BasePage:

    def __init__(self, page: Page):
        self.page = page

    def _execute_action(self, action, operation: str,locator:Locator | None = None , description: str|None = None):
        logger.info(f"{operation}: {description}")
        try:
            result = action()
            logger.info(f"Successfully completed {operation} on {description}")
            return result
        except Exception as e:
            logger.exception(f"Failed {operation} on {description}")
            self.screenshot(f"Failed {operation}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
            raise

    def click(self, locator:Locator,description:str):
        self.wait_for_visibility(locator,description)
        return self._execute_action(
            action=lambda: locator.click(),
            operation="Click",
            locator=locator,
            description= description
        )

    def fill(self, locator:Locator, value: str,description:str):
        self.wait_for_visibility(locator,description)
        return self._execute_action(
            action=lambda:locator.fill(value),
            operation="Fill",
            locator=locator,
            description= description
        )

    def get_text(self, locator:Locator,description:str):
        self.wait_for_visibility(locator,description)

        return self._execute_action(
            action=lambda: locator.text_content(),
            operation="Get Text",
            locator=locator,
            description= description
        )
    def get_all_text(self,locator:Locator,description:str):
        self.wait_for_visibility(locator,description)
        return  self._execute_action(
            action = lambda :locator.all_inner_texts(),
            operation="Get All Text",
            locator=locator,
            description= description
        )


    def is_visible(self, locator:Locator,description:str):
        return self._execute_action(
            action=lambda: locator.is_visible(),
            operation="Is Visible",
            locator=locator,
            description= description
        )

    def wait_for_visibility(self, locator:Locator,description:str):

        return self._execute_action(
            action=lambda:expect(locator).to_be_visible(),
            operation="Wait for Visible",
            locator=locator,
            description= description
        )

    def get_current_url(self):
        return self._execute_action(
            action=lambda: self.page.url,
            operation="Get Current URL",

            description="Current Browser URL"
        )

    def screenshot(self, name: str):
        logger.info(f"Saving screenshot {name}")
        self.page.screenshot(path=f"screenshots/{name}.png")

    def wait_for_url_pattern(self,pattern:str,description:str):

        return self._execute_action(
            action=lambda: expect(self.page).to_have_url(re.compile(pattern),timeout=config.expect_timeout),
            operation="Wait for URL pattern",
            description= description
        )

    def wait_for_exact_url(self,url:str,description:str):
            return self._execute_action(
                action=lambda: expect(self.page).to_have_url(url),
                operation="Wait for Exact URL",
                description=description
            )