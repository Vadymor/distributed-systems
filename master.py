import json
import requests
from datetime import datetime
import uvicorn
import logging as lg
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

lg.basicConfig(level=lg.INFO)

app = FastAPI()

# list of received messages
messages = []

# global message counter
counter = 1


class Message(BaseModel):
    value: str


@app.get("/get-messages")
def get_messages():
    """
    This Function stands for returning of all messages in GET request
    :return: returns the list with all messages
    """
    return messages


@app.post("/add-message/")
def add_messages(message: Message, response: Response):
    """
    This Function stands for adding of new messages in the list and replicating it in the secondaries
    :param message: received message
    :param response: POST response
    :return: returns the text about results of request
    """
    global counter
    messages.append(message.value)

    replication_status = replicate_on_secondaries(message.value, counter)

    counter += 1

    if replication_status:
        response.status_code = status.HTTP_200_OK
        lg.info("Replication was successful")
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        lg.warning("Replication wasn't successful")


def replicate_on_secondaries(replicated_message: str, message_number: int) -> bool:
    """
    Function for replicating the message on the secondaries
    :param replicated_message: message for replication
    :param message_number: message number
    :return: replication status
    """
    payload = {
        "value": replicated_message,
        "number": message_number
    }

    response1 = make_request(payload, 8001)
    response2 = make_request(payload, 8002)

    if response1 and response2:
        return True
    else:
        return False


def make_request(payload, port) -> bool:
    try:
        response = requests.post(url=f"http://127.0.0.1:{port}/add-message-secondary/", data=json.dumps(payload))
        lg.info(f"Response status code from the Sec{port} is: {response.status_code} at {datetime.now()}")
        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as err:
        print(err)
        return False


if __name__ == '__main__':
    lg.info("The Master`s launch is starting")
    uvicorn.run(app, host="127.0.0.1", port=8000)
