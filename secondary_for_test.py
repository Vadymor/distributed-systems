import uvicorn
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from time import sleep

app = FastAPI()

messages = []


class Message(BaseModel):
    value: str


@app.get("/get-messages-secondary/")
def get_messages():
    return messages


@app.post("/add-message-secondary/")
def add_messages(message: Message, response: Response):
    messages.append(message.value)

    # delay emulation
    sleep(5)

    response.status_code = status.HTTP_200_OK
    return "Message was added successfully"


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8002)
    # uvicorn secondary:app --host 0.0.0.0 --port 8002
