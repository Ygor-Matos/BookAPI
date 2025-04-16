from sqlalchemy import select

from livraria.models import User


def test_create_user(session):

    user = User(
        username='usuario teste',
        email='teste@teste.com', 
        password='senha',
        
       )
    session.add(user)
    session.commit()
        
    result = session.scalar(
        select(User).where(User.email == 'teste@teste.com')
    )
        
    assert result.username == 'usuario teste'
    assert result.email == 'teste@teste.com'
    assert result.password == 'senha'