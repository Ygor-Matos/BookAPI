from http import HTTPStatus
from livraria.schemas import UserPublic

def test_read_root_deve_retornar_ok(client):
    response = client.get('/') #ACt (ação)

    assert response.status_code == HTTPStatus.OK #  assert 
    assert response.json() == { 'message':'ola mundo'} #assert

def test_create_user(client):
    
    response = client.post( # user Schema
        '/users/',
        json={
        'username':"teste",
        'email':"teste@teste.com",
        'password':'senhateste'
        }
    )

    assert response.status_code == HTTPStatus.CREATED

    #validar userPublic
    assert response.json() == {
        'id': 1,
        'username': 'teste',
        'email': 'teste@teste.com'
    }

def test_create_user_username_already_registered(client, user):
    
    response = client.post( # user Schema
        '/users/',
        json={
        'username':"teste",
        'email':"teste@testando.com",
        'password':'senhateste'
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()=={
        "detail": 'Username already exists'
    }


def test_create_user_email_already_registered(client, user):
    
    response = client.post( # user Schema
        '/users/',
        json={
        'username':"testando",
        'email':"teste@teste.com",
        'password':'senhateste'
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()=={
        "detail": 'Email already exists'
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() =={ 'users': []}

def test_read_users_with_user(client,user):
    user_schema= UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() =={ 'users': [user_schema]}



def test_update_user(client,user):
    response = client.put(
        '/users/1',
        json={
        'password': "mudei",
        'username': 'dunossingo',
        'email': 'teste@teste.com'
        }
    )

    assert response.json() =={
        'id': 1,
        'username': 'dunossingo',
        'email': 'teste@teste.com'
    }



def test_delete_user(client,user):
    response = client.delete('/users/1')

    assert response.json() == { 'message': 'User deleted'}

def test_delete_user_error(client):

    response = client.delete('users/0')
    
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail':'User not found'}



def test_update_user_error(client,user):
    response = client.put(
        '/users/1000',
        json={
        'password': "mudei",
        'username': 'dunossingo',
        'email': 'teste@teste.com'
        }
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() =={'detail':'User not found'} 


def test_get_user_error(client):
    response= client.get('users/1')
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail':'User not found'}
