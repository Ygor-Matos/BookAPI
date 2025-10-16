from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from livraria.security import verify_password, create_access_token
from livraria.database import get_session
from livraria.schemas import Token
from livraria.models import User

from sqlalchemy.orm import Session
from sqlalchemy import select

from typing import Annotated

router = APIRouter(prefix='/auth', tags=['auth'])
T_session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post('/token', response_model=Token)
def login_for_access_token(
    session: T_session,
    form_data: T_OAuth2Form,
):
    user = session.scalar(
        select(User).where(User.email == form_data.username)
    )

    if not user or not verify_password(form_data.password,user.password):
        raise HTTPException(
            status_code=400, detail='Incorrect email or password'
        )
    
    access_token = create_access_token(data={'sub':user.email})
    
    return {'access_token' : access_token, 'token_type':'Bearer'}
