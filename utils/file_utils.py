import re
class FileUtils:
    @staticmethod
    def sanitize_filename(name):
        name= re.sub("[^A-Za-z0-9_-]+","_",name)
        return name.strip("_")


