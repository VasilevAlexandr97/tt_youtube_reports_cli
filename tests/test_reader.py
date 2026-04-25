from pathlib import Path

import pytest

from report_cli.readers import CsvDataReader


@pytest.fixture
def reader() -> CsvDataReader:
    return CsvDataReader()


@pytest.fixture
def csv_file(tmp_path: Path) -> Path:
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(
        "title,ctr,retention_rate,views,likes,avg_watch_time\n"
        "Как я неделю не мыл кружку и выгорел,23.0,25,213400,6700,2.8\n"
        "Собеседование в FAANG: я пришёл в пижаме,8.0,88,18900,560,9.5\n"
        "Я попросил повышения и мне дали чай,15.5,45,61200,1650,5.1\n",
    )
    return csv_file

def test_reads_all_row(csv_file: Path, reader: CsvDataReader):
    rows = list(reader.read(csv_file))
    assert len(rows) == 3


def test_returns_dicts_with_correct_keys(
    csv_file: Path,
    reader: CsvDataReader,
):
    rows = list(reader.read(csv_file))
    assert rows[0] == {
        "title": "Как я неделю не мыл кружку и выгорел",
        "ctr": "23.0",
        "retention_rate": "25",
        "views": "213400",
        "likes": "6700",
        "avg_watch_time": "2.8",
    }
