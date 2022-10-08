import uvicorn
import logging as lg
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from time import sleep

lg.basicConfig(level=lg.INFO)

app = FastAPI()

messages = {}


class Message(BaseModel):
    value: str
    number: int


@app.get("/get-messages-secondary/")
def get_messages():
    sorted_messages = sorted(messages.items())

    return [i[1] for i in sorted_messages]


@app.post("/add-message-secondary/")
def add_messages(message: Message, response: Response):
    messages[message.number] = message.value

    # delay emulation
    sleep(1)

    response.status_code = status.HTTP_200_OK
    lg.info("Message was added successfully")


if __name__ == '__main__':
    lg.info("The Secondary`s launch is starting")
    uvicorn.run(app, host="127.0.0.1", port=8002)
    # uvicorn secondary:app --host 127.0.0.1 --port 8001
