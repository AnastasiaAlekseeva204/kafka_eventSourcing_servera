import jwt
import os

# Берем из системы, убираем возможные пробелы/кавычки
SECRET_KEY = os.getenv("SECRET_KEY", "cpflsdDLCMSd;msdvnsvdmkdkm,").strip()

class CryptService:
    @staticmethod
    def decode_token(token: str) -> str | None:
        try:
            claims = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
            sub = claims.get("sub")
            return str(sub) if sub else None
        except Exception as e:
            print(f"JWT Error: {e}")
            return None