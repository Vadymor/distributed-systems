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
    messages.append(message.value)

    replication_status = replicate_on_secondaries(message.value)

    if replication_status:
        response.status_code = status.HTTP_200_OK
        lg.info("Replication was successful")
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        lg.warning("Replication wasn't successful")


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
    lg.info(f"Response status code from the Sec1 is: {response1.status_code} at {datetime.now()}")

    response2 = requests.post(url="http://127.0.0.1:8002/add-message-secondary/", data=json.dumps(payload))
    lg.info(f"Response status code from the Sec2 is: {response2.status_code} at {datetime.now()}")

    if response1.status_code == 200 and response2.status_code == 200:
        return True
    else:
        return False

if __name__ == '__main__':
    lg.info("The Master`s launch is starting")
    uvicorn.run(app, host="127.0.0.1", port=8000)
  




