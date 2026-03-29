import json
import os
from kafka import KafkaProducer
from kafka.errors import KafkaError

class KafkaService:
    _producer = None

    @classmethod
    def get_producer(cls):
        if cls._producer is None:
            cls._producer = KafkaProducer(
                bootstrap_servers=os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
        return cls._producer

    @classmethod
    def send_message(cls, topic, message):
        try:
            producer = cls.get_producer()
            producer.send(topic, value=message)
            producer.flush()
            print(f"Message sent to topic '{topic}': {message}")
        except Exception as e:
            print(f"Kafka unavailable, skipping event: {e}")
