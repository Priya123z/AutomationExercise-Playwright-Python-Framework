import re
class FileUtils:
    @staticmethod
    def sanitize_filename(name:str)->str:
        name= re.sub("[^A-Za-z0-9_-]+","_",name)
        return name.strip("_")


