from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseReader(ABC):
    """
    Defines the contract that every data reader must implement.
    """

    @abstractmethod
    def validate(
        self,
        filepath: Path,
        **kwargs: Any
    ) -> None:
        """Validate the data source."""
        ...

    @abstractmethod
    def read(
        self,
        filepath: Path,
        **kwargs: Any
    ) -> list[dict]:
        """Read the data source and return standardized data."""
        ...