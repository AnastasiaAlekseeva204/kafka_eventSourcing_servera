import datetime
import os
from http.client import HTTPException

from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

SECRET_KEY = os.getenv("SECRET_KEY")
TOKEN_EXPIRATION_SECONDS = 60


class CryptService:
    Context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    @classmethod
    def get_hash_password(cls,password: str) -> str:
        return cls.Context.hash(password)

    @classmethod
    def verify_password(cls, password: str, hashed_password: str) -> bool:
        return cls.Context.verify(password,hashed_password)

    @staticmethod
    def create_token(id_user: int) -> str:
        claims = {
            "sub": str(id_user),
            "exp": datetime.datetime.now() + datetime.timedelta(minutes=TOKEN_EXPIRATION_SECONDS)
        }
        return jwt.encode(claims=claims, key = SECRET_KEY, algorithm='HS256')