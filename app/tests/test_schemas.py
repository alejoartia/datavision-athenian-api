from datetime import date
from app.schemas.dashboard import Dashboard, FileCsv, QueriesAnalyzed, TeamStats, StatsId


def test_dashboard_model():
    data = {
        "review_time": 120,
        "team_name": "Team A",
        "review_date": date(2022, 3, 1),
        "merge_time": 180,
    }
    dashboard = Dashboard(**data)
    assert dashboard.review_time == 120
    assert dashboard.team_name == "Team A"
    assert dashboard.review_date == date(2022, 3, 1)
    assert dashboard.merge_time == 180


def test_file_csv_model():
    data = {"name": "file.csv"}
    file_csv = FileCsv(**data)
    assert file_csv.name == "file.csv"


def test_queries_analyzed_model():
    data = {"query_number": 10}
    queries_analyzed = QueriesAnalyzed(**data)
    assert queries_analyzed.query_number == 10


def test_team_stats_model():
    data = {
        "team_id": 1,
        "team_name": "Team A",
        "mean_review_time": 120.0,
        "median_review_time": 100.0,
        "mode_review_time": 90.0,
        "mean_merge_time": 180.0,
        "median_merge_time": 200.0,
        "mode_merge_time": 210.0,
        "created_date": date(2022, 3, 1),
    }
    team_stats = TeamStats(**data)
    assert team_stats.team_id == 1
    assert team_stats.team_name == "Team A"
    assert team_stats.mean_review_time == 120.0
    assert team_stats.median_review_time == 100.0
    assert team_stats.mode_review_time == 90.0
    assert team_stats.mean_merge_time == 180.0
    assert team_stats.median_merge_time == 200.0
    assert team_stats.mode_merge_time == 210.0
    assert team_stats.created_date == date(2022, 3, 1)


def test_stats_id_model():
    data = {"query_number": 10}
    stats_id = StatsId(**data)
    assert stats_id.query_number == 10
