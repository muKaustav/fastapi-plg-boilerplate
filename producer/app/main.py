import os
from faker import Faker
from fastapi import FastAPI
from aiokafka import AIOKafkaProducer

app = FastAPI()

fake = Faker()

producer = AIOKafkaProducer(
    bootstrap_servers=f"{os.getenv('KAFKA_HOST')}:{os.getenv('KAFKA_PORT')}",
    client_id="my-producer",
)


@app.post("/")
async def produce_message():
    try:
        message = fake.sentence()

        await producer.send_and_wait(os.getenv("KAFKA_TOPIC"), message.encode())

        return {"message": message}

    except Exception as e:
        print("error occurred: ", e)

        return {"message": "Message not sent"}


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")
    await producer.stop()
