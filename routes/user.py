from fastapi import APIRouter, HTTPException
from starlette import status

from routes.auth import get_password_hash
from mongodb import db
from models.user import User, UserCreate
from serializer import serialize_dict

user = APIRouter(prefix='/users')


@user.post('/', response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    user_dict = dict(user)
    #  async validation for unique username, email, national_id
    if await db.user.find_one({'username': user_dict['username']}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='username is already taken')
    if await db.user.find_one({'email': user_dict['email']}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='email is already taken')
    if await db.user.find_one({'national_id': user_dict['national_id']}):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='This national ID has already been registered')

    user_dict['password'] = get_password_hash(user_dict['password'])
    created_user = await db.user.insert_one(user_dict)
    created_user = await db.user.find_one({'_id': created_user.inserted_id})
    return serialize_dict(created_user)
