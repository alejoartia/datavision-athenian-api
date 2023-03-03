from fastapi.testclient import TestClient

from app.tests.index_test import app

client = TestClient(app)


def test_read_main():
    response = client.get("/app/v1/")
    assert response.status_code == 200


def test_upload_file():
    response = client.post('/app/v1/upload')
    assert response.status_code == 422


def test_get_data():
    response = client.post('/app/v1/analysis_file/1')
    assert response.status_code == 200


def test_analysis():
    response = client.get('/app/v1/analysis/1')
    assert response.status_code == 200


def test_saved_analysis_list():
    response = client.get('/app/v1/saved_analysis_list')
    assert response.status_code == 200


def test_save_analysis():
    response = client.get('/app/v1/save_analysis')
    assert response.status_code == 200


def test_file_list():
    response = client.get('/app/v1/file_list')
    assert response.status_code == 200


def test_review_stats():
    response = client.get('/app/v1/review_stats')
    assert response.status_code == 200
