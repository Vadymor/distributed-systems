import uvicorn
import logging as lg
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from collections import OrderedDict
from time import sleep
from random import randrange
import requests

lg.basicConfig(level=lg.INFO)

app = FastAPI()

messages = OrderedDict()


class Message(BaseModel):
    value: str
    number: int


def filter_consecutive_messages():
    consecutive_messages = []
    index = 0

    for key, value in messages.items():
        if key - index == 1:
            consecutive_messages.append(value)
            index += 1
        else:
            lg.info("Inconsistent order")
            break

    return consecutive_messages


@app.get("/get-messages-secondary/")
def get_messages():
    """
    This Function stands for returning of all messages in GET request
    :return: returns the list with all messages, already sorted
    """
    consecutive_messages = filter_consecutive_messages()
    return {"messages": consecutive_messages}


@app.post("/add-message-secondary/")
def add_messages(message: Message, response: Response):
    """
    This Function stands for adding of new messages to the Secondaries from the Master
    :param message: message from the Master
    :param response: POST response
    :return: returns the text about results of request
    """
    global messages

    # delay emulation
    sleep(randrange(4))

    messages[message.number] = message.value

    messages = OrderedDict(sorted(messages.items()))

    response.status_code = status.HTTP_200_OK
    lg.info("Message was added successfully")


@app.on_event("startup")
async def startup_event():
    """
    This Function stands for adding of all messages to the Secondary from the Master.
    This Function runs once at node startup
    """
    global messages

    master_port = 8000
    response = requests.get(url=f"http://master:{master_port}/get-messages/",
                            timeout=60)

    master_messages = response.json()['messages']

    for index, msg in enumerate(master_messages):
        messages[index + 1] = msg

    messages = OrderedDict(sorted(messages.items()))


if __name__ == '__main__':
    lg.info("The Secondary`s launch is starting")
    uvicorn.run(app, host="0.0.0.0", port=8001)
