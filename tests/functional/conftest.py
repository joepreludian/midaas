import pytest
from fastapi.testclient import TestClient
from models.account import BankAccount


@pytest.fixture(scope="session")
def ensure_db():
    from midaas.config import base_config

    if (
        not base_config.dev_environment
        or not base_config.midaas_dynamodb_table_name.endswith("__test")
    ):
        raise Exception("Cannot run tests outside dev environment")

    BankAccount.create_table(write_capacity_units=2, read_capacity_units=2)
    yield
    BankAccount.delete_table()


@pytest.fixture(scope="session")
def http_client(ensure_db, ensure_mocked_http_client):
    from midaas.main import app

    return TestClient(app)
