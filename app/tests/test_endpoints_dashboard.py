import json
import io
import pytest
from fastapi.testclient import TestClient
from app.index import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Data-vision"}


def test_upload_file():
    csv_file = io.StringIO("review_time,team,date,merge_time\n1,team1,2022-03-01,2\n2,team2,2022-03-02,3\n")
    response = client.post("/upload", files={"file": ("test.csv", csv_file)})
    assert response.status_code == 200
    assert "review_time" in response.json()


def test_review_stats():
    response = client.get("/review_stats")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "name" in response.json()[0]


def test_file_list():
    response = client.get("/file_list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "id" in response.json()[0]


def test_save_analysis():
    response = client.get("/save_analysis")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "name" in response.json()[0]


def test_saved_analysis_list():
    response = client.get("/saved_analysis_list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "query_number" in response.json()[0]


def test_saved_analysis_object():
    response = client.get("/analysis/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "name" in response.json()[0]
