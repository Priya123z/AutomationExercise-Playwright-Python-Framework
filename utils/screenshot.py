from playwright.sync_api import Page
from utils.artifact_manager import artifact
from utils.file_utils import FileUtils


class Screenshot:

    @staticmethod
    def capture(page:Page, name:str):

        safe_name = FileUtils.sanitize_filename(name)

        path=artifact.screenshots_dir/f"{safe_name}.png"

        page.screenshot(path=path)



