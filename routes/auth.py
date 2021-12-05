from fastapi import HTTPException, Depends, APIRouter
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from starlette import status

from models.user import UserLoginModel
from mongodb import db
from passlib.context import CryptContext
from serializer import serialize_dict

auth = APIRouter(prefix='/auth')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = True


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate(user_data: UserLoginModel):
    user = await db.user.find_one({'username': user_data.username})
    if not user:
        return False
    if not verify_password(user_data.password, user['password']):
        return False
    return user


@AuthJWT.load_config
def get_config():
    return Settings()


@auth.post('/token/')
async def token(user_data: UserLoginModel, authorize: AuthJWT = Depends()):
    user = await authenticate(user_data)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='username or password is incorrect')
    access_token = authorize.create_access_token(subject=user['username'])
    refresh_token = authorize.create_refresh_token(subject=user['username'])
    authorize.set_access_cookies(access_token)
    authorize.set_refresh_cookies(refresh_token)
    return {"user": serialize_dict(user), "access_token": access_token, "refresh_token": refresh_token}


@auth.post('/refresh/')
def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    current_username = authorize.get_jwt_subject()
    new_access_token = authorize.create_access_token(subject=current_username)
    authorize.set_access_cookies(new_access_token)
    return {"access_token": new_access_token}

@auth.delete('/logout/')
def logout(authorize: AuthJWT = Depends()):
    authorize.jwt_required()

    authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}