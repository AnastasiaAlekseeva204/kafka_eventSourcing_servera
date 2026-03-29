import uuid
import json
import os

from confluent_kafka import Consumer, Producer
#2. student_es.py: Инструменты для Event Sourcing

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


class StudentEventConsumer:

    @classmethod
    def _make_consumer(cls):
        return Consumer({
            "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"),
            "group.id": f"fastapi-reader-{uuid.uuid4()}",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": False
        })

    @classmethod
    def _read_all(cls):
        c = cls._make_consumer()
        events = []
        c.subscribe(["student-events"])
        while not c.assignment():
            c.poll(0.1)
        while True:
            msg = c.poll(2.0)
            if msg is None:
                break
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                break
            try:
                events.append(json.loads(msg.value().decode("utf-8")))
            except Exception as e:
                print(e)
        c.close()
        return events

    @classmethod
    def load_all_events(cls):
        return cls._read_all()

    @classmethod
    def load_events(cls, student_id):
        events = []
        for event in cls._read_all():
            if event["op"] in ["c", "u"] and event["student"]["student_id"] == student_id:
                events.append(event)
            elif event["op"] == "d" and event["student_id"] == student_id:
                events.append(event)
        return events


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
        self.__version__ = -1
        self.__deleted__ = False
        self.__ids_event__ = set()

    def load(self):
        events = StudentEventConsumer.load_events(self.__student_id__)
        for event in events:
            event_id = event.get("id_event")
            if event_id is None or event_id not in self.__ids_event__:
                if event["op"] == "c":
                    student = event["student"]
                    self.__last_name__ = student["last_name"]
                    self.__first_name__ = student["first_name"]
                    self.__middle_name__ = student["middle_name"]
                    self.__gender__ = student["gender"]
                    self.__age__ = student["age"]
                    self.__owner__ = student.get("owner_id")
                    self.__version__ = 0
                elif event["op"] == "u":
                    student = event["student"]
                    self.__last_name__ = student["last_name"]
                    self.__first_name__ = student["first_name"]
                    self.__middle_name__ = student["middle_name"]
                    self.__gender__ = student["gender"]
                    self.__age__ = student["age"]
                    self.__version__ += 1
                elif event["op"] == "d":
                    self.__deleted__ = True
            if event_id:
                self.__ids_event__.add(event_id)

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

    def update(self, old_version, last_name=None, first_name=None, middle_name=None, gender=None, age=None):
        if self.__deleted__:
            raise RuntimeError("Cannot update deleted student")
        if self.__version__ != old_version:
            raise RuntimeError(f"Not correct version: {old_version}")
        if last_name: self.__last_name__ = last_name
        if first_name: self.__first_name__ = first_name
        if middle_name: self.__middle_name__ = middle_name
        if gender is not None: self.__gender__ = gender
        if age: self.__age__ = age
        student = {
            "student_id": self.__student_id__,
            "last_name": self.__last_name__,
            "first_name": self.__first_name__,
            "middle_name": self.__middle_name__,
            "gender": self.__gender__,
            "age": self.__age__,
            "owner_id": self.__owner__,
        }
        send_event_to_kafka({"op": "u", "student": student})
        self.__version__ += 1

    def delete(self, old_version):
        if self.__deleted__:
            raise RuntimeError("Cannot delete deleted student")
        if self.__version__ != old_version:
            raise RuntimeError(f"Not correct version: {old_version}")
        self.__deleted__ = True
        send_event_to_kafka({"op": "d", "student_id": self.__student_id__})

    def is_deleted(self):
        return self.__deleted__

    def get_id(self):
        return self.__student_id__

    def get_last_name(self):
        return self.__last_name__

    def get_first_name(self):
        return self.__first_name__

    def get_middle_name(self):
        return self.__middle_name__

    def get_gender(self):
        return self.__gender__

    def get_age(self):
        return self.__age__

    def get_version(self):
        return self.__version__

    def get_ids_event(self):
        return list(self.__ids_event__)


class StudentsEventSourcing:
    @staticmethod
    def load():
        events = StudentEventConsumer.load_all_events()

        ids = set()
        for event in events:
            if event["op"] == "c":
                ids.add(event["student"]["student_id"])

        students = [StudentEventSourcing(student_id=sid) for sid in ids]

        for student in students:
            student.load()

        return [s for s in students if not s.is_deleted()]
