import argparse
import logging

from pathlib import Path

from tabulate import tabulate

from report_cli.readers import CsvDataReader, DataReader
from report_cli.report_generator import (
    ClickbaitReportGenerator,
    ReportGenerator,
)

logger = logging.getLogger(__name__)

REPORT_GENERATORS: dict[str, type[ReportGenerator]] = {
    "clickbait": ClickbaitReportGenerator,
}


class CliHandler:
    def __init__(
        self,
        report_generators: dict[str, type[ReportGenerator]],
        reader: DataReader,
    ):
        self.report_generators = report_generators
        self.reader = reader

    def get_report_generator(self, report_type: str) -> ReportGenerator:
        report_class = self.report_generators.get(report_type)
        if report_class is None:
            raise ValueError(f"Unknown report type: {report_type}")
        return report_class()

    def run(self, files: list[Path], report_type: str) -> list[str]:
        report_generator = self.get_report_generator(report_type)
        for file in files:
            if not file.exists():
                raise ValueError(f"File does not exist: {file}")
        all_rows = (row for file in files for row in self.reader.read(file))
        report = report_generator.generate(all_rows)
        if not report:
            return []
        table = tabulate(report, headers="keys", tablefmt="grid")
        return table.splitlines()


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser(
        prog="Youtube Reports CLI",
    )
    parser.add_argument("-f", "--files", type=Path, nargs="+", required=True)
    parser.add_argument("-r", "--report", type=str, required=True)
    args = parser.parse_args()
    logger.info(f"Data files: {','.join((str(f)) for f in args.files)}")
    reader = CsvDataReader()
    cli_handler = CliHandler(REPORT_GENERATORS, reader)
    try:
        report = cli_handler.run(args.files, args.report)
        logger.info("\n".join(report))
    except ValueError as e:
        logger.info(str(e))


if __name__ == "__main__":
    main()
