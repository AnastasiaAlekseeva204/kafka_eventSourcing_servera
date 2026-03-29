from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

#создание таблицы пользователя
class User(Base):
    __tablename__ = 'users'
    id : Mapped[int] = mapped_column(primary_key=True)
    login_name : Mapped[str] = mapped_column(unique=True)
    hashed_password : Mapped[str] = mapped_column()

