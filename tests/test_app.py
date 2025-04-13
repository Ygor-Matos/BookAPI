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
    ...