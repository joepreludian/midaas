import pytest
from fastapi.testclient import TestClient
from midaas.main import app


@pytest.fixture(scope="session")
def http_client():
    return TestClient(app)
