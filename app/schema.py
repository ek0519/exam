import re
from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, EmailStr, validator


class User(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    is_verify: bool


class ChangeUserName(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)


class CreateUser(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50,
                          title='contains at least one lower character, one upper '
                                'character, one digit and one special character '
                          )
    password_confirmation: str = Field(..., min_length=8, max_length=50)

    @validator('password')
    def password_check(cls, v):
        regex = r'^.*(?=.{8,})(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?=.*[@#$%^&+=]).*$'
        if len(re.findall(regex, v)) == 0:
            raise ValueError('Password must be matched with the rules')
        return v

    @validator('password_confirmation')
    def password_confirmation_check(cls, v, values):
        if values['password'] != v:
            raise ValueError('Password confirmation must be matched with the password')
        return v


class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=50,
                          title='contains at least one lower character,'
                                ' one upper character, one digit and one '
                                'special character '
                          )

    @validator('password')
    def password_check(cls, v):
        regex = r'^.*(?=.{8,})(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?=.*[@#$%^&+=]).*$'
        if len(re.findall(regex, v)) == 0:
            raise ValueError('Password must be matched with the rules')
        return v


class UserOut(User):
    login_time: int = Field(default=0)
    last_login_ip: str
    remember_me: str = None


class EmailSchema(BaseModel):
    email: List[EmailStr]


class UserList(User):
    login_time: int = Field(default=0)
    last_login_ip: str
    last_login_at: datetime = Field(default=None)


class FacebookAuth(BaseModel):
    access_token: str


class UserResetPassword(BaseModel):
    old_password: str = Field(..., min_length=8, max_length=50,
                              title='contains at least one lower character, '
                                    'one upper character, one digit and one '
                                    'special character '
                              )
    new_password: str = Field(..., min_length=8, max_length=50)

    new_password_confirmation: str = Field(..., min_length=8, max_length=50)

    @validator('old_password')
    def old_password_check(cls, v):
        regex = r'^.*(?=.{8,})(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?=.*[@#$%^&+=]).*$'
        if len(re.findall(regex, v)) == 0:
            raise ValueError('Password must be matched with the rules')
        return v

    @validator('new_password')
    def new_password_check(cls, v):
        regex = r'^.*(?=.{8,})(?=.*[a-z])(?=.*\d)(?=.*[A-Z])(?=.*[@#$%^&+=]).*$'
        if len(re.findall(regex, v)) == 0:
            raise ValueError('Password must be matched with the rules')
        return v

    @validator('new_password_confirmation')
    def new_password_confirmation_check(cls, v, values):
        if values['new_password'] != v:
            raise ValueError('Password confirmation must be matched with the password')
        return v
