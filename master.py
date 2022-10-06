import json
import requests
from datetime import datetime
import uvicorn
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()

# list of received messages
messages = []


class Message(BaseModel):
    value: str


@app.get("/get-messages")
def get_messages():
    """
    Function for returning all messages in GET request
    :return: list with all messages
    """
    return messages


@app.post("/add-message/")
def add_messages(message: Message, response: Response):
    """
    Function for adding new messages in the list and replicating it in the secondaries
    :param message: received message
    :param response: POST response
    :return: text about results of request
    """
    messages.append(message.value)

    replication_status = replicate_on_secondaries(message.value)

    if replication_status:
        response.status_code = status.HTTP_200_OK
        return "Replication was successful"
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return "Replication wasn't successful"


def replicate_on_secondaries(replicated_message: str) -> bool:
    """
    Function for replicating the message on the secondaries
    :param replicated_message: message for replication
    :return: replication status
    """
    payload = {
        "value": replicated_message
    }

    response1 = requests.post(url="http://127.0.0.1:8001/add-message-secondary/", data=json.dumps(payload))
    print(f"Response status code from 1: {response1.status_code} at {datetime.now()}")

    response2 = requests.post(url="http://127.0.0.1:8002/add-message-secondary/", data=json.dumps(payload))
    print(f"Response status code from 2: {response2.status_code} at {datetime.now()}")

    if response1.status_code == 200 and response2.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
