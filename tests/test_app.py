from fastapi.testclient import TestClient
from http import HTTPStatus
from livraria.app import app


def test_read_root_deve_retornar_ok():
    client = TestClient(app) # arrange (organização)
    
    response = client.get('/') #ACt (ação)

    assert response.status_code == HTTPStatus.OK #  assert 
    assert response.json() == { 'message':'ola mundo'} #assert
