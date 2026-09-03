from pathlib import Path
import os

from dotenv import dotenv_values

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"

ENVIRONMENTS = ["qa", "uat", "prod"]
BROWSERS = ["chromium", "firefox", "webkit"]


class ConfigManager:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, env="qa", browser=None):

        if getattr(self, "_initialized", False):
            return

        self.environment = env

        self._browser_override = browser

        self._load()

        self._initialized = True

    def configure(self, env=None, browser=None):
        # Called from pytest_configure so --environment / --browser actually take effect.
        # Everything imports the singleton at module load, so we reload in place rather
        # than building a second instance.
        if env:
            if env not in ENVIRONMENTS:
                raise ValueError(f"Unsupported environment: {env}. Expected one of {ENVIRONMENTS}.")
            self.environment = env

        if browser:
            self._browser_override = browser

        self._load()

    def _load(self):

        self._read_environment_files()

        self._read_configuration()

        self._validate_configuration()

    def _read_environment_files(self):
        # default.env holds everything common; the per-environment file only lists what
        # differs. Real environment variables still win over both so CI can override.
        env_file = CONFIG_DIR / f"{self.environment}.env"

        if not env_file.exists():
            raise FileNotFoundError(
                f"Environment configuration file not found: {env_file}"
            )

        self._settings = dict(dotenv_values(CONFIG_DIR / "default.env"))

        self._settings.update(dotenv_values(env_file))

    def _setting(self, name):
        return os.getenv(name) or self._settings.get(name)

    def _read_configuration(self):

        self.base_url = self._setting("BASE_URL")

        self.api_base_url = self._setting("API_BASE_URL")

        self.browser = self._browser_override or self._setting("BROWSER")

        self.headless = self._setting("HEADLESS")

        self.timeout = self._setting("DEFAULT_TIMEOUT")

        self.expect_timeout = self._setting("EXPECT_TIMEOUT")

        self.dummyjson_api_base_url = self._setting("DUMMYJSON_API_BASE_URL")

    def _validate_configuration(self):

        if not self.base_url:
            raise ValueError(
                "BASE_URL is missing."
            )

        if not self.api_base_url:
            raise ValueError(
                "API_BASE_URL is missing."
            )

        self.timeout = self._positive_int("DEFAULT_TIMEOUT", self.timeout)

        self.expect_timeout = self._positive_int("EXPECT_TIMEOUT", self.expect_timeout)

        if not self.headless:
            raise ValueError(
                "HEADLESS is missing."
            )

        if str(self.headless).lower() not in ["true", "false"]:
            raise ValueError(
                "HEADLESS must be true or false."
            )

        self.headless = str(self.headless).lower() == "true"

        if self.browser not in BROWSERS:
            raise ValueError(
                f"Unsupported browser: {self.browser}. Expected one of {BROWSERS}."
            )

        if not self.dummyjson_api_base_url:
            raise ValueError(
                "DUMMYJSON_API_BASE_URL is missing."
            )

    @staticmethod
    def _positive_int(name, value):

        if not value:
            raise ValueError(f"{name} is missing.")

        try:
            value = int(value)
        except ValueError:
            raise ValueError(f"{name} must be an integer.")

        if value <= 0:
            raise ValueError(f"{name} must be greater than zero.")

        return value


config = ConfigManager()
