from fastapi import FastAPI
from http import HTTPStatus
from livraria.schemas import Message
from livraria.schemas import UserSchema, UserPublic, UserDB, UserList

app = FastAPI()

database=[]

@app.get('/', status_code=HTTPStatus.OK, response_model = Message)
def read_root():
    return { 'message':'ola mundo'}

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model= UserPublic)
def create_user(user:UserSchema):
    user_with_id = UserDB(
        id=len(database) +1, 
        **user.model_dump()
    )
    database.append(user_with_id)
    return user_with_id

@app.get('/users/', response_model = UserList)
def read_users():
    return {'users': database}