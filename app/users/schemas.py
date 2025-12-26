from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ValidationInfo, field_validator
from app.exceptions import (
    PasswordsDoNotMatchException,
    PasswordTooShortException,
)

class SUserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    password_confirm: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None

    @field_validator('password_confirm')
    @classmethod
    def passwords_match(cls, v: str, info: ValidationInfo) -> str:
        if 'password' in info.data and v != info.data['password']:
            raise PasswordsDoNotMatchException()
        return v

    @field_validator('password')
    @classmethod
    def password_strength(cls, v):
        if len(v) < 6:
            raise PasswordTooShortException
        return v
    
class SUserAuth(BaseModel):
    email: EmailStr
    password: str

from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class SUserUpdate(BaseModel):
    email: Optional[EmailStr]
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]