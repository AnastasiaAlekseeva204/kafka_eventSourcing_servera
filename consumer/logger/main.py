import asyncio
import json
import datetime
from aiokafka import AIOKafkaConsumer


async def consume():
    while True:
        consumer = AIOKafkaConsumer(
            'student_events',
            bootstrap_servers='kafka:9092',
            group_id="logging_group",
            auto_offset_reset='earliest'
        )
        try:
            await consumer.start()
            print("CONSUMER STARTED: Waiting for messages...", flush=True)
            log_file = "/app/students_history.log"
            async for msg in consumer:
                data = json.loads(msg.value.decode('utf-8'))
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"[{timestamp}] RECEIVED EVENT: {data}"
                print(log_entry, flush=True)
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(log_entry + "\n")
        except Exception as e:
            print(f"Kafka not ready, retrying in 5s: {e}", flush=True)
            await asyncio.sleep(5)
        finally:
            await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
