from http import HTTPStatus
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from crypt import CryptService
from validation_models import TokenOut, UserRegister
from database import SessionLocal
from database_models import User
from producer import KafkaService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/health", status_code=HTTPStatus.OK)
def health():
    return {"status": "ok"}


@app.post("/api/auth/register", response_model=TokenOut)
def register_user(user_register: UserRegister, session: Session = Depends(get_session)):
    try:
        login = getattr(user_register, "login_name", getattr(user_register, "username", None))
        pwd = getattr(user_register, "password", None)

        if not login or not pwd:
            raise HTTPException(status_code=400, detail="Missing login or password in request body")

        existing = session.query(User).filter(User.login_name == login).first()
        if existing:
            raise HTTPException(status_code=409, detail="User already exists")

        hashed_password = CryptService.get_hash_password(pwd)
        database_user = User(
            login_name=login,
            hashed_password=hashed_password,
        )
        session.add(database_user)
        session.commit()
        session.refresh(database_user)

        KafkaService.send_message("user-events", {
            "event_type": "user_registered",
            "login": login,
            "user_id": database_user.id
        })

        token = CryptService.create_token(id_user=database_user.id)
        return TokenOut(access_token=token)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.post("/api/auth/login", response_model=TokenOut)
def login_user(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.query(User).filter(User.login_name == form.username).first()

    if not user or not CryptService.verify_password(form.password, str(user.hashed_password)):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid credentials")

    KafkaService.send_message("user-events", {
        "event_type": "user_logged_in",
        "login": form.username,
        "user_id": user.id
    })

    token = CryptService.create_token(id_user=user.id)
    return TokenOut(access_token=token)
