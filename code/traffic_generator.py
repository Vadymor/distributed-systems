## Import extensions
from time import sleep, perf_counter
from random import sample, randint
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import string

## Input parameters setup
letters = string.ascii_letters
acceptance_levels = [1,2,3]
messages = []

## Messages generation
for i in range(0,100):
    messages.append(
        {
        "value": "".join(sample(letters,5)),
        "write_concern": sample(acceptance_levels,1)[0]
    }
    )

## Definition of request function to Master
def make_request_to_master(payload: dict[str, int]):
    sleep(randint(1,5))
    try:
        response =requests.post(url="http://localhost:8000/add-message/",
                                 data=json.dumps(payload),
                                 timeout=4)

        if response.status_code == 200:
            return True
        else:
            return False    
    except Exception as err:
        return False

## Definition of function with ThreadPoolExecutor to invoke "make_request_to_master" function     
def pooled_requests(messages):
    # create the thread pool
    n_threads = len(messages)
    with ThreadPoolExecutor(n_threads) as executor:
        # download each url and save as a local file
        _ = [executor.submit(make_request_to_master, message) for message in messages]

## Timer start
start = perf_counter()

## Invoke ThreadPoolExecutor to send requests
pooled_requests(messages)

## Timer end
finish = perf_counter()    

print(f'It took {finish-start} second(s) to finish.')