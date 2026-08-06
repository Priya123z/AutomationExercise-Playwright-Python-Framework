import json
from pathlib import Path
from dataclasses import asdict

from models.AutomationExercise_UI_API_Models.user import User


class JsonUtils:

    @staticmethod
    def save_latest(user: User, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w") as file:
            json.dump(asdict(user), file, indent=4)

    def append_history(user:User):
        pass


    @staticmethod
    def load_user(path: Path) -> User:
        with open(path) as file:
            data = json.load(file)

        return User(**data)

