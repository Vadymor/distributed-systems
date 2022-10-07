import requests
import json
import logging as lg
from datetime import datetime

lg.basicConfig(level=lg.DEBUG)
lg.debug("The debug of the Master scripting logic has begun")

payload = {
    "value": "message_4"
}


response = requests.post(url="http://127.0.0.1:8000/add-message/", data=json.dumps(payload))
# response = requests.get(url="http://0.0.0.0:8000/get-messages/")
# response = requests.get(url="http://0.0.0.0:8002/get-messages-secondary/")

lg.debug(f"Response status code from the Master is: {response.status_code} at {datetime.now()}")
