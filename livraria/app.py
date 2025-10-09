from fastapi import FastAPI, HTTPException, Depends
from http import HTTPStatus
from sqlalchemy import select
from livraria.schemas import Message
from livraria.schemas import UserSchema, UserPublic, UserList

from livraria.database import get_session
from livraria.models import User

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model = Message)
def read_root():
    return { 'message':'ola mundo'}

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model= UserPublic)
def create_user(user:UserSchema, session=Depends(get_session) ):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) |  (User.email == user.email)
            )
    )
    if db_user:
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists'
            )
        elif db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists'
            )

    db_user=User(username=user.username, email=user.email, password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

@app.get('/users/', response_model = UserList)
def read_users(
    limit: int = 10,
    offset:int = 0,
    session=Depends(get_session)
   ):
    user = session.scalars(
        select(User).limit(limit).offset(offset)
        )
    return {"users":user}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id:int, user:UserSchema, session = Depends(get_session)):
    db_user= session.scalar(
        select(User).where(User.id==user_id)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    db_user.email =user.email
    db_user.username = user.username
    db_user.password = user.password

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id:int, session = Depends(get_session)):
    db_user= session.scalar(
        select(User).where(User.id==user_id)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    session.delete(db_user)
    session.commit()
    
    return {'message': 'User deleted'}

@app.get('/users/{user_id}', response_model=UserPublic)
def get_user(user_id:int, session = Depends(get_session)):
    db_user= session.scalar(
        select(User).where(User.id == user_id)
    )
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )
    return db_user
