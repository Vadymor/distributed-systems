import requests
import json
import numpy as np


payload_m = {
    "value": str(np.random.randn(1)[0])
}


post_m = requests.post(url="http://127.0.0.1:8000/add-message/", data=json.dumps(payload_m))

print(f'The status code of post request to Master is {post_m.status_code} and the text is:\n{post_m.text}')

get_m = requests.get(url="http://127.0.0.1:8000/get-messages/")

print(f'The status code of post request to Master is {get_m.status_code} and the text is:\n{get_m.text}')

payload_s = {
    "value": get_m.text
}

post_s1 = requests.post(url="http://127.0.0.1:8001/add-message/", data=json.dumps(payload_s))
post_s2 = requests.post(url="http://127.0.0.1:8002/add-message/", data=json.dumps(payload_s))


print(f'The status code of post request to Secondary 1 is {post_s1.status_code} and the text is:\n{post_s1.text}')

print(f'The status code of post request to Secondary 2 is {post_s2.status_code} and the text is:\n{post_s2.text}')