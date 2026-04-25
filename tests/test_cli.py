from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from report_cli.cli import REPORT_GENERATORS, CliHandler, main
from report_cli.readers import DataReader


@pytest.fixture
def mock_reader() -> MagicMock:
    """Фикстура для mock-ридера."""
    reader = MagicMock(spec=DataReader)
    reader.read.return_value = [
        {
            "title": "Кликбейт",
            "ctr": "20.0",
            "retention_rate": "30.0",
            "views": "1000",
            "likes": "500",
            "avg_watch_time": "2.0",
        },
        {
            "title": "Норм",
            "ctr": "8.0",
            "retention_rate": "75.0",
            "views": "2000",
            "likes": "1000",
            "avg_watch_time": "3.0",
        },
    ]
    return reader


@pytest.fixture
def cli_handler(mock_reader):
    """Фикстура для CliHandler с mock-зависимостями."""
    return CliHandler(REPORT_GENERATORS, mock_reader)


def test_cli_clickbait_report(cli_handler: CliHandler, tmp_path: Path):
    """Тестируем генерацию отчета clickbait с mock-данными."""
    csv_file = tmp_path / "data.csv"
    csv_file.touch()

    result = cli_handler.run([csv_file], "clickbait")

    output = "\n".join(result)
    assert "Кликбейт" in output
    assert "Норм" not in output


def test_cli_calls_reader_with_correct_file(
    cli_handler: CliHandler,
    tmp_path: Path,
):
    csv_file = tmp_path / "data.csv"
    csv_file.touch()

    cli_handler.run([csv_file], "clickbait")

    cli_handler.reader.read.assert_called_once_with(csv_file)


def test_cli_calls_reader_for_each_file(
    cli_handler: CliHandler,
    tmp_path: Path,
):
    file1 = tmp_path / "a.csv"
    file2 = tmp_path / "b.csv"
    file1.touch()
    file2.touch()

    cli_handler.run([file1, file2], "clickbait")

    assert cli_handler.reader.read.call_count == 2


def test_cli_unknown_report_type(cli_handler: CliHandler):
    with pytest.raises(ValueError, match="Unknown report type: unknown"):
        cli_handler.run([Path("data.csv")], "unknown")


def test_cli_file_not_exists(cli_handler):
    with pytest.raises(
        ValueError,
        match=r"File does not exist: nonexistent.csv",
    ):
        cli_handler.run([Path("nonexistent.csv")], "clickbait")


def test_cli_empty_report(cli_handler: CliHandler, tmp_path: Path):
    cli_handler.reader.read.return_value = []
    csv_file = tmp_path / "empty.csv"
    csv_file.touch()

    result = cli_handler.run([csv_file], "clickbait")
    assert result == []


def test_main_with_valid_arguments():
    mock_args = MagicMock()
    mock_args.files = [Path("data.csv")]
    mock_args.report = "clickbait"
    with (
        patch("argparse.ArgumentParser.parse_args", return_value=mock_args),
        patch("report_cli.cli.CliHandler") as mock_handler_class,
    ):
        mock_handler = MagicMock()
        mock_handler.run.return_value = ["line1", "line2"]
        mock_handler_class.return_value = mock_handler
        main()
        mock_handler.run.assert_called_once_with(
            [Path("data.csv")],
            "clickbait",
        )
