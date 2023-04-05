from typing import Optional
from ninja import Schema, Field
from password_validator import PasswordValidator
from pydantic import validator, EmailStr
from passlib.hash import pbkdf2_sha256 as sha256
from django.contrib.auth.hashers import make_password

from .models import User

class UserRegisterSchema(Schema):
    email: EmailStr
    firstname: str = Field(strip_whitespace=True, min_length=3, max_length=20)
    lastname: str = Field(strip_whitespace=True, min_length=3, max_length=20)
    password: str

    @validator('password', allow_reuse=True)
    def validate_password(cls, v):
        ''' Checks and verifies that password is secure
            Password must have minimum of 6 characters, have an uppercase, a lowercase, a number, and a symbol
        '''
        schema = PasswordValidator()
        schema.min(6).uppercase().lowercase().digits().symbols()

        if not schema.validate(v):
            raise ValueError(
                'Password not secure! Must contain minimum of 6 characters, an uppercase, a lowercase, a number, and a symbol')
        
        hashed_password = make_password(v)
        return hashed_password
        

    @validator('email', allow_reuse=True)
    def check_credentials_taken(cls, v, field):
        data = User.objects.filter(email=v).exists()

        if data:
            raise ValueError(f'{field.name} already exists!')

        return v

class UserIDSchema(Schema):
    id: str

class UserLoginSchema(Schema):
    email: EmailStr
    password: str

class UserDataSchema(Schema):
    id: str
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    verified: bool
    token: Optional[str]

class ForgotPasswordSchema(Schema):
    email: EmailStr

    @validator('email', allow_reuse=True)
    def check_credentials_taken(cls, v, field):
        data = User.objects.filter(email=v).exists()

        if data == False:
            raise ValueError(f'{field.name} does not exist!')

        return v

class ResetPasswordSchema(Schema):
    password: str
    token: str

    @validator('password', allow_reuse=True)
    def validate_password(cls, v):
        ''' Checks and verifies that password is secure
            Password must have minimum of 6 characters, have an uppercase, a lowercase, a number, and a symbol
        '''
        schema = PasswordValidator()
        schema.min(6).uppercase().lowercase().digits().symbols()

        if not schema.validate(v):
            raise ValueError(
                'Password not secure! Must contain minimum of 6 characters, an uppercase, a lowercase, a number, and a symbol')
        
        hashed_password = make_password(v)
        return hashed_password

class VerifyOTPSchema(Schema):
    id: str
    otp: int = Field(min=10000, max=99999)