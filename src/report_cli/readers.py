import csv

from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any


class DataReader(ABC):
    @abstractmethod
    def read(self, file_path: Path) -> Iterator[dict[str, Any]]:
        pass


class CsvDataReader(DataReader):
    def read(self, file_path: Path) -> Iterator[dict[str, Any]]:
        with file_path.open("r") as csv_file:
            reader = csv.DictReader(csv_file)
            yield from reader
