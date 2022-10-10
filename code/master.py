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
    return {"messages": messages}


@app.post("/add-message/")
def add_messages(message: Message, response: Response):
    """
    This Function stands for adding of new messages in the list and replicating it in the secondaries
    :param message: received message
    :param response: POST response
    :return: returns the text about results of request
    """
    global counter

    message_number = counter

    counter += 1

    messages.append(message.value)

    replication_status = replicate_on_secondaries(message.value, message_number)

    if replication_status:
        response.status_code = status.HTTP_200_OK
        lg.info("Replication was successful")
        return {"response_message": "Replication was successful"}
    else:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        lg.warning("Replication wasn't successful")
        return {"response_message": "Replication wasn't successful"}


def replicate_on_secondaries(replicated_message: str, message_number: int) -> bool:
    """
    This Function stands for replicating of the message on the secondaries
    :param replicated_message: message for replication
    :param message_number: message number
    :return: replication status
    """
    payload = {
        "value": replicated_message,
        "number": message_number
    }

    response1 = make_request(payload, 1, 8001)
    response2 = make_request(payload, 2, 8002)

    if response1 and response2:
        return True
    else:
        return False


def make_request(payload: dict[str, str], secondary_number: int, port: int) -> bool:
    """
    This Function stands for the post request of the message from the Master to the Secondaries
    :param payload: message that consists of value (message content) and number (message ID)
    :param secondary_number: secondary service number
    :param port: the port of secondary as param, to operate over several Secondaries
    :return: boolean value, to confirm successfull post request to both of Secondaries
    """

    try:
        lg.info(f"Send request to the Sec{secondary_number} at {datetime.now()}")

        response = requests.post(url=f"http://secondary{secondary_number}:{port}/add-message-secondary/",
                                 data=json.dumps(payload))

        lg.info(f"Response status code from the Sec{secondary_number} is: {response.status_code} at {datetime.now()}")

        if response.status_code == 200:
            return True
        else:
            return False
    except Exception as err:
        lg.error(err)
        return False


if __name__ == '__main__':
    lg.info("The Master`s launch is starting")
    uvicorn.run(app, host="0.0.0.0", port=8000)
