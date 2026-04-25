from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import ClassVar


class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, rows: Iterable[dict]) -> list[dict]:
        pass


class ClickbaitReportGenerator(ReportGenerator):
    COLUMNS: ClassVar[list[str]] = ["title", "ctr", "retention_rate"]

    def _is_valid(self, row: dict) -> bool:
        try:
            min_ctr = 15
            max_retention_rate = 40
            return (
                float(row["ctr"]) > min_ctr
                and float(row["retention_rate"]) < max_retention_rate
            )
        except (ValueError, KeyError, TypeError):
            return False

    def generate(self, rows: Iterable[dict]) -> list[dict]:
        filtered_rows = (row for row in rows if self._is_valid(row))
        sorted_rows = sorted(
            filtered_rows,
            key=lambda x: float(x["ctr"]),
            reverse=True,
        )
        return [{k: row[k] for k in self.COLUMNS} for row in sorted_rows]
