from abc import ABC, abstractmethod
from pathlib import Path


class BaseWriter(ABC):

    @abstractmethod
    def write(self, file_path: Path, data) -> None:
        pass

    @abstractmethod
    def append(self, file_path: Path, data) -> None:
        pass