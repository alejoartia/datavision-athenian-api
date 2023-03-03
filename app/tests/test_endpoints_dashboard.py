from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.index import app

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
