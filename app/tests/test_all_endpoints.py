from fastapi.testclient import TestClient
from app.routes.app import dashboard

client = TestClient(dashboard)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Data-vision"}


def test_upload_file():
    response = client.post("/upload/1")
    assert response.status_code == 200 or response.status_code == 404


def test_get_data():
    response = client.post("/analysis_file/1")
    print(response.status_code)
    print(response.json())
    assert response.status_code == 200 or response.status_code == 404


def test_review_stats():
    response = client.get("/review_stats")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user_stats():
    response = client.get("/file_list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_save_stats():
    response = client.get("/save_analysis")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_saved_analysis_list():
    response = client.get("/saved_analysis_list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_saved_analysis_object():
    response = client.get("/analysis/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
