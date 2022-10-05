import requests
import json

payload = {
    "value": "my_message345"
}


response = requests.post(url="http://0.0.0.0:8000/add-message/", data=json.dumps(payload))

print(response.status_code)
print(response.text)
