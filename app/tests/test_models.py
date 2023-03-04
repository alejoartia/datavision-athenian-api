import pytest
from app.models.dashboard import Base, Dashboard, FileCsv, QueriesAnalyzed, StatsId, TeamStats
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)


@pytest.fixture(scope='module')
def session():
    Base.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


def test_create_dashboard(session):
    file = FileCsv()
    session.add(file)
    session.commit()

    dashboard = Dashboard(review_time=30, team='Team A', date=date.fromisoformat('2022-01-01'), merge_time=15,
                          file=file)
    session.add(dashboard)
    session.commit()

    assert dashboard.id is not None
    assert dashboard.team == 'Team A'
    assert dashboard.date == date.fromisoformat('2022-01-01')
    assert dashboard.file.id == file.id


def test_create_queries_analyzed(session):
    query = QueriesAnalyzed(query_number=42)
    session.add(query)
    session.commit()

    assert query.id is not None
    assert query.query_number == 42


def test_create_stats_id(session):
    stats_id = StatsId(query_number=42)
    session.add(stats_id)
    session.commit()

    assert stats_id.id is not None
    assert stats_id.query_number == 42


def test_create_team_stats(session):
    stats_id = StatsId(query_number=42)
    session.add(stats_id)
    session.commit()

    team_stats = TeamStats(name='Team A', mean_review_time=20.0, median_review_time=15.0, mode_review_time=10.0,
                           mean_merge_time=25.0, median_merge_time=20.0, mode_merge_time=15.0, stat=stats_id)
    session.add(team_stats)
    session.commit()

    assert team_stats.id is not None
    assert team_stats.name == 'Team A'
    assert team_stats.mean_review_time == 20.0
    assert team_stats.stat.id == stats_id.id


def test_query_team_stats(session):
    stats_id = StatsId(query_number=42)
    session.add(stats_id)
    session.commit()

    team_stats = TeamStats(name='Team A', mean_review_time=20.0, median_review_time=15.0, mode_review_time=10.0,
                           mean_merge_time=25.0, median_merge_time=20.0, mode_merge_time=15.0, stat=stats_id)
    session.add(team_stats)
    session.commit()

    result = session.query(TeamStats).filter(TeamStats.name == 'Team A').first()

    assert result is not None
    assert result.name == 'Team A'
    assert result.mean_review_time == 20.0
