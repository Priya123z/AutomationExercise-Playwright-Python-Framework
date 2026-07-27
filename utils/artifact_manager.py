from pathlib import Path
from datetime import datetime
class ArtifactManager:
    _instance = None

    _ARTIFACT_TYPES = ["logs","screenshots","reports","videos","traces"]
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self.execution_id = self._generate_execution_Id()
        self._create_execution_directories()
        self._create_sub_directories()
        self._initialized = True


    def _generate_execution_Id(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _create_execution_directories(self):

        project_root = Path(__file__).resolve().parent.parent
        self.execution_dir = project_root / "artifacts" / self.execution_id
        self.execution_dir.mkdir(parents=True, exist_ok=True)

    def _create_sub_directories(self):
        for folder in self._ARTIFACT_TYPES:
            path = self.execution_dir/folder
            path.mkdir(parents=True, exist_ok=True)
            setattr(self, f"{folder}_dir", path)

artifact = ArtifactManager()