import pytest

from fastapi.testclient import TestClient
from livraria.models import table_registry, User

from livraria.security import get_password_hash

from sqlalchemy.orm import Session

from livraria.app import app
from livraria.database import get_session
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

@pytest.fixture()
def client(session):

    def get_session_override():
        return session
    #substituindo o banco de dados de produção pelo banco de dados em memória.
    with  TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture()
def session():
    #setup
    engine = create_engine('sqlite:///:memory:',
                           connect_args={'check_same_thread':False},
                           poolclass=StaticPool,

    )
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

    #teardown
    table_registry.metadata.drop_all(engine)

@pytest.fixture()
def user(session):
    pwd = 'testtest'
    user= User(
        username='teste', 
        email='teste@teste.com', 
        password=get_password_hash(pwd)
    )
    session.add(user)
    session.commit()
    session.refresh(user)


    user.clean_password = pwd # Monkey Patch
    return user

@pytest.fixture()
def token(client,user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']