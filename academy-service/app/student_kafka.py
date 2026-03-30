import uuid
import json
import os

from confluent_kafka import Consumer, Producer


class StudentEventProducer:
    __p__ = Producer({
        "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
    })

    @classmethod
    def produce(cls, data: dict):
        if data["op"] in ["c", "u"]:
            key = data["student"]["student_id"]
        else:
            key = data["student_id"]

        cls.__p__.produce(
            topic="student-events",
            value=json.dumps(data).encode("utf-8"),
            key=str(key).encode("utf-8")
        )
        cls.__p__.flush()


def send_event_to_kafka(event):
    event["id_event"] = str(uuid.uuid4())
    StudentEventProducer.produce(event)


class StudentEventSourcing:
    def __init__(self, student_id, last_name=None, first_name=None, middle_name=None, gender=None, age=None, owner_id=None):
        self.__student_id__ = student_id
        self.__last_name__ = last_name
        self.__first_name__ = first_name
        self.__middle_name__ = middle_name
        self.__gender__ = gender
        self.__age__ = age
        self.__owner__ = owner_id


    def create(self):
        student = {
            "student_id": self.__student_id__,
            "last_name": self.__last_name__,
            "first_name": self.__first_name__,
            "middle_name": self.__middle_name__,
            "gender": self.__gender__,
            "age": self.__age__,
            "owner_id": self.__owner__,
        }
        self.__version__ = 0
        send_event_to_kafka({"op": "c", "student": student})
