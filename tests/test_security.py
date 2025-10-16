from jwt import decode

from livraria.security import create_access_token

from livraria.settings import Settings

from http import HTTPStatus

settings = Settings()
def test_jwt():
    data ={'sub': 'test@test.com'}
    token = create_access_token(data)

    result = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={ 'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

    assert response.json() == { 'detail': 'Could not validate credentials'}