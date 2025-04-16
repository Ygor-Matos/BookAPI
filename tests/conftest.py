import pytest

from fastapi.testclient import TestClient
from livraria.models import table_registry

from sqlalchemy.orm import Session

from livraria.app import app
from sqlalchemy import create_engine

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def session():
    #setup
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    #teardown
    table_registry.metadata.drop_all(engine)