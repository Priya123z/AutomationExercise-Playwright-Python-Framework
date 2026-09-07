from utils.artifact_manager import artifact
from utils.file_utils import FileUtils


class Screenshot:

    @staticmethod
    def capture(page, name):

        safe_name = FileUtils.sanitize_filename(name)

        path=artifact.screenshots_dir/f"{safe_name}.png"

        page.screenshot(path=path)
