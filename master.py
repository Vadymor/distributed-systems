import uvicorn
from fastapi import FastAPI

app = FastAPI()

messages = [
    "fddsdsf",
    "fdsfdsfdsf433c43c"
]


@app.get("/get-messages")
def get_messages():
    return messages


@app.post("/add-message")
def add_messages(message: str):
    messages.append(message)
    return messages


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
