from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
import uuid
from datetime import datetime
from sqlalchemy import JSON, DateTime, String
from sqlalchemy.dialects.postgresql import UUID # Для корректной работы с Postgres

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


class OutboxStudent(Base):
    __tablename__ = "outbox_student"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    aggregate_type: Mapped[str] = mapped_column(String(255))
    aggregate_id: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    #53^14