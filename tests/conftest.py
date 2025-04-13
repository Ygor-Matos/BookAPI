import pytest

from fastapi.testclient import TestClient

from livraria.app import app

@pytest.fixture()
def client():
    return TestClient(app)