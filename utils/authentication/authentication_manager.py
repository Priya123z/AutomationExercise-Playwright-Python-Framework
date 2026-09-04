from __future__ import annotations
import os
from pathlib import Path
from utils.artifact_manager import artifact
from utils.config_manager import config
from utils.credentials_manager import credential_manager
from flows.UI_Flow.login_flow import LoginFlow

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

    def _storage_state_path(self, role: str) -> Path:
        return self.auth_directory / f"{role}.json"

    def _storage_state_exists(self, role: str) -> bool:
        """
        Checks whether the storage state already exists.
        """
        return self._storage_state_path(role).exists()

    def _create_storage_state(self, browser, role: str) -> Path:

        context = browser.new_context()
        try:
            page = context.new_page()
            page.goto(config.base_url)
            login_page = LoginFlow(page)

            credentials = credential_manager.get_credentials(role)
            login_page.login(credentials.username, credentials.password)

            storage_state = self._storage_state_path(role)

            # Under xdist two workers can land here together. Write to a process-unique
            # file and rename, so nobody ever reads a half-written state.
            partial = storage_state.with_name(f"{role}.{os.getpid()}.partial")
            context.storage_state(path=partial)
            partial.replace(storage_state)

            return storage_state
        finally:
            context.close()

    def clear_all_storage_states(self):
        """
        Deletes every storage state for the current environment.
        """
        for file in self.auth_directory.glob("*.json"):
            file.unlink()

    def get_storage_state(self, browser, role: str)->Path:
        """
        Returns the storage state for a role, logging in once per execution.
        """

        storage_state = self._storage_state_path(role)

        if storage_state.exists():
            return storage_state

        return self._create_storage_state(browser, role)

auth = AuthManager()
