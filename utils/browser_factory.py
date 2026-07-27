from utils.logger import logger


class BrowserFactory:

    @staticmethod
    def create_browser(playwright, config):

        if config.browser == "chromium":
            return BrowserFactory._create_chromium(playwright, config)

        elif config.browser == "firefox":
            return BrowserFactory._create_firefox(playwright, config)

        elif config.browser == "webkit":
            return BrowserFactory._create_webkit(playwright, config)

        raise ValueError(
            f"Unsupported browser: {config.browser}"
        )

    @staticmethod
    def _create_chromium(playwright, config):

        logger.info("Launching Chromium Browser")

        return playwright.chromium.launch(
            headless=config.headless
        )

    @staticmethod
    def _create_firefox(playwright, config):

        logger.info("Launching Firefox Browser")

        return playwright.firefox.launch(
            headless=config.headless
        )

    @staticmethod
    def _create_webkit(playwright, config):

        logger.info("Launching WebKit Browser")

        return playwright.webkit.launch(
            headless=config.headless
        )