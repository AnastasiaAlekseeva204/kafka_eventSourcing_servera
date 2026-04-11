from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass

class Student(Base):
    __tablename__ = 'students'
    id : Mapped[int] = mapped_column(primary_key=True)
    last_name : Mapped[str] = mapped_column()
    first_name : Mapped[str] = mapped_column()
    middle_name : Mapped[str] = mapped_column()
    gender: Mapped[bool] = mapped_column()
    age : Mapped[int] = mapped_column()
    owner_id : Mapped[int] = mapped_column()
