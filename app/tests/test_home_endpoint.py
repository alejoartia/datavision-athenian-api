import pytest
from fastapi.testclient import TestClient
from app.routes.app import dashboard


@pytest.fixture
def client():
    client = TestClient(dashboard)
    return client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Data-vision"}
