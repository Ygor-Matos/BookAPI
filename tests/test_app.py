from http import HTTPStatus

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

def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() =={ 'users': [
        {
            'id': 1,
            'username': 'teste',
            'email': 'teste@teste.com'            
        }
    ]
    }

def test_update_user(client):
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


def test_update_user_error(client):
    response_max = client.put(
        '/users/1000',
        json={
        'password': "mudei",
        'username': 'dunossingo',
        'email': 'teste@teste.com'
        }
    )

    response_min = client.put(
        '/users/0',
        json={
        'password': "mudei",
        'username': 'dunossingo',
        'email': 'teste@teste.com'
        }
    )

    assert response_max.json() =={'detail':'user not found'} 
    assert response_min.json() =={'detail':'user not found'} 

def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == { 'message': 'user deleted'}

def test_delete_user_error(client):
    
    response_max = client.delete('users/1000')
    response_min = client.delete('users/0')

    assert response_max.json() == {'detail':'user not found'}
    assert response_min.json() == {'detail':'user not found'}