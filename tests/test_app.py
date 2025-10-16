from http import HTTPStatus
from livraria.schemas import UserPublic

def test_read_root_deve_retornar_ok(client):
    response = client.get('/') #ACt (ação)

    assert response.status_code == HTTPStatus.OK #  assert 
    assert response.json() == { 'message':'ola mundo'} #assert





