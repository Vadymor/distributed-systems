import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from time import sleep

app = FastAPI()

messages = []


class Message(BaseModel):
    value: str


@app.get("/get-messages")
def get_messages():
    return messages


@app.post("/add-message/")
def add_messages(message: Message):
    messages.append(message.value)

    # emulate working with secondaries
    sleep(1)

    return messages


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8001)
