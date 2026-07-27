from pathlib import Path
import os

from dotenv import load_dotenv


class ConfigManager:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, env="qa"):

        if getattr(self, "_initialized", False):
            return

        self.environment = env

        self._load_environment_file()

        self._read_configuration()

        self._validate_configuration()

        self._initialized = True

    def _load_environment_file(self):

        project_root = Path(__file__).resolve().parent.parent

        env_file = project_root / "config" / f"{self.environment}.env"

        if not env_file.exists():
            raise FileNotFoundError(
                f"Environment configuration file not found: {env_file}"
            )

        load_dotenv(env_file,override=True)

    def _read_configuration(self):

        self.base_url = os.getenv("BASE_URL")

        self.browser = os.getenv("BROWSER")

        self.headless = os.getenv("HEADLESS")

        self.timeout = os.getenv("DEFAULT_TIMEOUT")

        self.expect_timeout = os.getenv("EXPECT_TIMEOUT")

    def _validate_configuration(self):

        if not self.base_url:
            raise ValueError(
                "BASE_URL is missing."
            )

        if not self.timeout:
            raise ValueError(
                "TIMEOUT is missing."
            )

        try:
            self.timeout = int(self.timeout)
        except ValueError:
            raise ValueError(
                "TIMEOUT must be an integer."
            )

        if self.timeout <= 0:
            raise ValueError(
                "TIMEOUT must be greater than zero."
            )

        if not self.headless:
            raise ValueError(
                "HEADLESS is missing."
            )

        allowed = ["true", "false"]

        if self.headless.lower() not in allowed:
            raise ValueError(
                "HEADLESS must be true or false."
            )

        self.headless = self.headless.lower() == "true"

        browsers = ["chromium", "firefox", "webkit"]

        if self.browser not in browsers:
            raise ValueError(
                f"Unsupported browser: {self.browser}"
            )
        if not self.expect_timeout:
            raise ValueError(
                "EXPECT_TIMEOUT is missing."
            )

        try:
            self.expect_timeout = int(self.expect_timeout)
        except ValueError:
            raise ValueError(
                "EXPECT_TIMEOUT must be an integer."
            )

        if self.expect_timeout <= 0:
            raise ValueError(
                "EXPECT_TIMEOUT must be greater than zero."
            )




config = ConfigManager()
