# Lab 1 Extensions
import json
import requests
from datetime import datetime
import uvicorn
import logging as lg
from fastapi import FastAPI, Response, status
from pydantic import BaseModel

# Lab 2 extensions
from time import sleep
from random import random
from threading import Thread, Condition


# simple countdown latch, starts closed then opens once count is reached
class CountDownLatch:
    # constructor
    def __init__(self, count, acceptance_count):
        # store the count
        self.count = count
        # control access to the count and notify when latch is open
        self.condition = Condition()

        self.acceptance_count = count - acceptance_count
 
    # count down the latch by one increment
    def count_down(self):
        # acquire the lock on the condition
        with self.condition:
            # check if the latch is already open
            if self.count == self.acceptance_count:
                return
            # decrement the counter
            self.count -= 1
            # check if the latch is now open
            if self.count == self.acceptance_count:
                # notify all waiting threads that the latch is open
                self.condition.notify_all()
 
    # wait for the latch to open
    def wait(self):
        # acquire the lock on the condition
        with self.condition:
            # check if the latch is already open
            if self.count == self.acceptance_count:
                return
            # wait to be notified when the latch is open
            self.condition.wait()


# To return value from "make_request" func
class ThreadWithReturnValue(Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


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

    acceptance_level = 2
    responses = 0

    # create the countdown latch
    latch = CountDownLatch(2, 1)

    threads = []
    for i in range(1, 3):
        thread = ThreadWithReturnValue(target=make_request, args=(latch, payload, i, int(f'800{i}')))
        threads.append(thread)

        lg.info(f'Thread for port 800{i}, Sec{i} is starting at {datetime.now()}')

        thread.start()

    for index, thread in enumerate(threads):
        responses += thread.join()

    lg.info('Waiting on latch to replicate on secondaries')
    latch.wait()

    if responses == acceptance_level:
        return True
    else:
        return False


def make_request(latch: CountDownLatch, payload: dict[str, str], secondary_number: int, port: int) -> bool:
    """
    This Function stands for the post request of the message from the Master to the Secondaries
    :param latch: -------
    :param payload: message that consists of value (message content) and number (message ID)
    :param secondary_number: secondary service number
    :param port: the port of secondary as param, to operate over several Secondaries
    :return: boolean value, to confirm successfull post request to both of Secondaries
    """

    try:
        lg.info(f"Send request to the Sec{secondary_number} at {datetime.now()}")

        response = requests.post(url=f"http://secondary{secondary_number}:{port}/add-message-secondary/",
                                 data=json.dumps(payload),
                                 timeout=300)

        latch.count_down()

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
