from pydantic import BaseModel, EmailStr, Field


class UserLoginModel(BaseModel):
    username: str
    password: str


class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    email: EmailStr
    national_id: str = Field(regex='^[0-9]{10}$')


class User(UserBase):
    id: str = Field(alias='_id')


class UserCreate(UserBase):
    password: str = Field(regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')
