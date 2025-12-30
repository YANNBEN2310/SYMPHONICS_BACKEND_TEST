import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """
    client de test FastAPI partagé entre tous les tests.
    """
    return TestClient(app)
