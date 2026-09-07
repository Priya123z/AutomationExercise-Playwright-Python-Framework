import os
import re

from flows.UI_Flow.login_flow import LoginFlow
from utils.artifact_manager import artifact
from utils.config_manager import config

class AuthManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.environment = config.environment
        # Storage state lives with the run's artifacts, not in the repo. It is rebuilt
        # once per execution and shared by every test in that run.
        self.auth_directory = (artifact.execution_dir / "auth" / self.environment)

        self._create_auth_directory()
        self._initialized = True


    def _create_auth_directory(self):
        self.auth_directory.mkdir(
            parents=True,
            exist_ok=True)

    def _storage_state_path(self, email):
        slug = re.sub(r"[^A-Za-z0-9]+", "_", email).strip("_")
        return self.auth_directory / f"{slug}.json"

    def _create_storage_state(self, browser, user):

        context = browser.new_context()
        try:
            page = context.new_page()
            page.goto(config.base_url)
            LoginFlow(page).login(user.email, user.password)

            storage_state = self._storage_state_path(user.email)

            # Under xdist two workers can land here together. Write to a process-unique
            # file and rename, so nobody ever reads a half-written state.
            partial = storage_state.with_name(f"{storage_state.stem}.{os.getpid()}.partial")
            context.storage_state(path=partial)
            partial.replace(storage_state)

            return storage_state
        finally:
            context.close()

    def get_storage_state(self, browser, user):
        """Storage state for an account, logging in once per execution.

        The account is created over the API by the fixture that asks for this, so
        there is no password in the repository and nothing to configure before a
        first run. There used to be a config/credentials.json holding a real
        password for a shared practice site.
        """

        storage_state = self._storage_state_path(user.email)

        if storage_state.exists():
            return storage_state

        return self._create_storage_state(browser, user)

auth = AuthManager()
