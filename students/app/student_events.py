from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

#1. student_events.py: Схемы событий
#Это чертежи твоих данных.
#Здесь определено, как выглядит «сообщение» в Kafka.
#Data Classes гарантируют, что если ты отправляешь событие «студент создан», у него обязательно будут имя, фамилия и ID.
#_now(): Автоматически ставит метку времени, чтобы знать, когда событие произошло (важно для порядка в ES).

def _now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class StudentCreated:
    event_type: str = "student_created"
    student_id: str = ""
    user_id: int = 0
    last_name: str = ""
    first_name: str = ""
    middle_name: str = ""
    gender: bool = False
    age: int = 0
    timestamp: str = field(default_factory=_now)


@dataclass
class StudentUpdated:
    event_type: str = "student_updated"
    student_id: str = ""
    user_id: int = 0
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    gender: Optional[bool] = None
    age: Optional[int] = None
    timestamp: str = field(default_factory=_now)


@dataclass
class StudentDeleted:
    event_type: str = "student_deleted"
    student_id: str = ""
    user_id: int = 0
    timestamp: str = field(default_factory=_now)
