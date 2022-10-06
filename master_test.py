import requests
import json

payload = {
    "value": "message_4"
}


response = requests.post(url="http://0.0.0.0:8000/add-message/", data=json.dumps(payload))
# response = requests.get(url="http://0.0.0.0:8000/get-messages/")
# response = requests.get(url="http://0.0.0.0:8002/get-messages-secondary/")


print(response.status_code)
print(response.text)
