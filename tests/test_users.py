from http import HTTPStatus
from livraria.schemas import UserPublic

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



def test_update_user(client,user, token):
    #FAZER ISSO COM OS OUTROS 
    #TESTES QUE ESTÃO DANDO ERRO, colocar dependencia de token e preencher o response
    #com o header
    response = client.put(
        f'/users/{user.id}',
        headers={'authorization': f'Bearer {token}'},
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



def test_delete_user(client,user,token):
    
    response = client.delete('/users/1', headers={'authorization': f'Bearer {token}'},)

    assert response.json() == { 'message': 'User deleted'}




def test_delete_user_without_permission(client,user,token):

    response = client.delete('users/3',headers={'authorization': f'Bearer {token}'})
    
    
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail':'Not enough permissions'}



def test_update_user_error(client,user, token):
    response = client.put(
        '/users/1000',
        headers={'authorization': f'Bearer {token}'},
        json={
        'password': "mudei",
        'username': 'dunossingo',
        'email': 'teste@teste.com'
        }
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() =={'detail':'Not enough permission'} 


def test_get_user_error(client):
    response= client.get('users/1')
    
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail':'User not found'}

