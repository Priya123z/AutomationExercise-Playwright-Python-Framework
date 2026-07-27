import json

from dataclasses import dataclass
from pathlib import Path

from loguru import logger


@dataclass(frozen=True)
class Credentials:
    username: str
    password: str

class CredentialManager:


    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self,"_initialized", False):
            return
        self.project_root =  Path(__file__).parent.parent.resolve()
        self.credentials_file = self.project_root /"config"/ "credentials.json"
        self.credentials = self._load_credentials()
        self._initialized = True


    def _load_credentials(self) -> dict:
        if not self.credentials_file.exists():
            raise FileNotFoundError(f"{self.credentials_file} does not exist")
        with open(self.credentials_file) as json_file:
            return json.load(json_file)

    def get_credentials(self, role:str) -> Credentials:
        role = role.lower()
        if role not in self.credentials:
            raise ValueError(f"Invalid role {role}")
        user = self.credentials[role]
        logger.info(
            f"Loading credentials for role '{role}'")
        return Credentials(user["username"], user["password"])

credential_manager = CredentialManager()
