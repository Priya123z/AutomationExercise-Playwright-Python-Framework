import os
from pathlib import Path
from datetime import datetime
class ArtifactManager:
    _instance = None

    _ARTIFACT_TYPES = ["logs","screenshots","reports","videos","traces","allure-results"]
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
        # xdist workers are separate processes. Without a shared id each one stamps its
        # own timestamp and the run gets split across two artifact folders, one of which
        # ends up empty.
        execution_id = os.environ.get("TEST_EXECUTION_ID")
        if not execution_id:
            execution_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            os.environ["TEST_EXECUTION_ID"] = execution_id
        return execution_id

    def _create_execution_directories(self):

        project_root = Path(__file__).resolve().parent.parent
        self.execution_dir = project_root / "artifacts" / self.execution_id
        self.execution_dir.mkdir(parents=True, exist_ok=True)

    def _create_sub_directories(self):
        for folder in self._ARTIFACT_TYPES:
            path = self.execution_dir / folder
            path.mkdir(parents=True, exist_ok=True)
            attribute_name = folder.replace("-", "_") + "_dir"
            setattr(self, attribute_name, path)

    @property
    def html_report(self):
        return self.reports_dir / "report.html"

    @property
    def allure_report_dir(self):
        return self.execution_dir / "allure-report"
artifact = ArtifactManager()