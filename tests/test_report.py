from typing import Any

import pytest

from report_cli.report_generator import ClickbaitReportGenerator


@pytest.fixture
def generator() -> ClickbaitReportGenerator:
    return ClickbaitReportGenerator()


@pytest.fixture
def sample_rows() -> list[dict[str, Any]]:
    return [
        # 1. Полное соответствие (CTR > 15 И Retention < 40)
        {
            "title": "Как я неделю не мыл кружку и выгорел",
            "ctr": "23.0",
            "retention_rate": "25",
            "views": "213400",
            "likes": "6700",
            "avg_watch_time": "2.8",
        },
        # 2. Не проходит по CTR (CTR <= 15)
        {
            "title": "Собеседование в FAANG: я пришёл в пижаме",
            "ctr": "8.0",
            "retention_rate": "88",
            "views": "18900",
            "likes": "560",
            "avg_watch_time": "9.5",
        },
        # 3. Не проходит по Retention (Retention >= 40)
        {
            "title": "Я попросил повышения и мне дали чай",
            "ctr": "15.5",
            "retention_rate": "45",
            "views": "61200",
            "likes": "1650",
            "avg_watch_time": "5.1",
        },
        # 4. Пограничный случай: CTR ровно 15.0 (не должен пройти, так как условие > 15)
        {
            "title": "Кейс: Граница CTR",
            "ctr": "15.0",
            "retention_rate": "30",
            "views": "1000",
            "likes": "50",
            "avg_watch_time": "3.0",
        },
        # 5. Пограничный случай: Retention ровно 40 (не должен пройти, так как условие < 40)
        {
            "title": "Кейс: Граница Retention",
            "ctr": "20.0",
            "retention_rate": "40",
            "views": "1000",
            "likes": "50",
            "avg_watch_time": "3.0",
        },
    ]


@pytest.fixture
def empty_rows() -> list:
    return []


@pytest.fixture
def valid_rows() -> list[dict[str, Any]]:
    return [
        {
            "title": "Как я случайно удалил базу данных на проде",
            "ctr": "28.5",
            "retention_rate": "18",
            "views": "320000",
            "likes": "12500",
            "avg_watch_time": 2.1,
        },
        {
            "title": "Почему PHP всё ещё жив в 2026 году",
            "ctr": "19.2",
            "retention_rate": "34",
            "views": "45000",
            "likes": "1200",
            "avg_watch_time": "3.8",
        },
        {
            "title": "5 признаков, что твой код — спагетти",
            "ctr": "22.0",
            "retention_rate": "31",
            "views": "89000",
            "likes": "4300",
            "avg_watch_time": "3.5",
        },
    ]


def test_filters_by_ctr_and_retention(
    generator: ClickbaitReportGenerator,
    sample_rows: list,
):
    result = generator.generate(sample_rows)
    titles = [row["title"] for row in result]
    assert titles == ["Как я неделю не мыл кружку и выгорел"]


def test_returns_only_required_columns(
    generator: ClickbaitReportGenerator,
    sample_rows: list,
):
    result = generator.generate(sample_rows)
    assert result
    for row in result:
        assert set(row.keys()) == {"title", "ctr", "retention_rate"}


def test_sorted_by_ctr_descending(
    generator: ClickbaitReportGenerator,
    valid_rows: list,
):
    result = generator.generate(valid_rows)
    ctrs = [float(row["ctr"]) for row in result]
    assert ctrs == sorted(ctrs, reverse=True)


def test_ctr_boundary_exactly_15_excluded(generator: ClickbaitReportGenerator):
    rows = [{"title": "Граница", "ctr": "15.0", "retention_rate": "30.0"}]
    assert generator.generate(rows) == []


def test_retention_boundary_exactly_40_excluded(
    generator: ClickbaitReportGenerator,
):
    rows = [{"title": "Граница", "ctr": "20.0", "retention_rate": "40.0"}]
    assert generator.generate(rows) == []


def test_empty_input(generator: ClickbaitReportGenerator, empty_rows: list):
    assert generator.generate(empty_rows) == []
