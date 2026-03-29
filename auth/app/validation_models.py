from typing import Annotated
from pydantic import BaseModel, Field

LoginType = Annotated[str, Field(min_length=3)]
PasswordType = Annotated[str, Field(min_length=8, max_length=36)]

class StudentBase(BaseModel):
    login_name: LoginType
    password: PasswordType

class UserRegister(StudentBase):
    pass

class UserLogin(StudentBase):
    pass

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"