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
    """
    This Function stands for returning of all messages in GET request
    :return: returns the list with all messages, already sorted
    """
    sorted_messages = sorted(messages.items())

    return {"messages": [i[1] for i in sorted_messages]}


@app.post("/add-message-secondary/")
def add_messages(message: Message, response: Response):
    """
    This Function stands for adding of new messages to the Secondaries from the Master
    :param message: message from the Master
    :param response: POST response
    :return: returns the text about results of request
    """

    messages[message.number] = message.value

    # delay emulation
    sleep(1)

    response.status_code = status.HTTP_200_OK
    lg.info("Message was added successfully")


if __name__ == '__main__':
    lg.info("The Secondary`s launch is starting")
    uvicorn.run(app, host="0.0.0.0", port=8001)
