import json
import io
import pytest
from fastapi.testclient import TestClient
from app.index import app, get_db
from app.models.dashboard import FileCsv, Dashboard, QueriesAnalyzed, StatsId, TeamStats
from sqlalchemy.orm import Session
from datetime import datetime

client = TestClient(app)


@pytest.fixture
def db():
    db = get_db()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def file_csv(db):
    file_csv = FileCsv(time_created=datetime.now())
    db.add(file_csv)
    db.commit()
    yield file_csv
    db.delete(file_csv)
    db.commit()


@pytest.fixture
def dashboard_data(db, file_csv):
    data = [
        Dashboard(review_time=1, team='team1', date='2022-03-01', merge_time=2, file_id=file_csv.id),
        Dashboard(review_time=2, team='team2', date='2022-03-02', merge_time=3, file_id=file_csv.id),
        Dashboard(review_time=3, team='team1', date='2022-03-03', merge_time=4, file_id=file_csv.id)
    ]
    db.add_all(data)
    db.commit()
    yield data
    db.delete_all(data)
    db.commit()


@pytest.fixture
def stats_id(db):
    stats_id = StatsId(time_created=datetime.now())
    db.add(stats_id)
    db.commit()
    yield stats_id
    db.delete(stats_id)
    db.commit()


@pytest.fixture
def team_stats(db, stats_id):
    data = [
        TeamStats(name='team1', mean_review_time=2.0, median_review_time=2.0, mode_review_time=[2.0],
                  mean_merge_time=3.0, median_merge_time=3.0, mode_merge_time=[3.0], stats_id=stats_id.query_number),
        TeamStats(name='team2', mean_review_time=2.0, median_review_time=2.0, mode_review_time=[2.0],
                  mean_merge_time=3.0, median_merge_time=3.0, mode_merge_time=[3.0], stats_id=stats_id.query_number)
    ]
    db.add_all(data)
    db.commit()
    yield data
    db.delete_all(data)
    db.commit()


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Data-vision"}


def test_upload_file(db):
    csv_file = io.StringIO("review_time,team,date,merge_time\n1,team1,2022-03-01,2\n2,team2,2022-03-02,3\n")
    response = client.post("/upload", files={"file": ("test.csv", csv_file)})
    assert response.status_code == 200
    assert "review_time" in response.json()

    file_csv = db.query(FileCsv).first()
    assert file_csv is not None
    assert file_csv.time_created is not None

    dashboard_data = db.query(Dashboard).filter_by(file_id=file_csv.id).all()
    assert len(dashboard_data) == 2


def test_review_stats(db, dashboard_data):
    response = client.get("/review_stats")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2
    assert response.json()[0]['name'] == 'team1'
