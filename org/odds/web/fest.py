from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_home():
    return {"payload": "Hello, World"}


@app.get("/items/{item_id}")
def get_item(item_id: int, q: Union[str, None] = None):
    return {"payload": {"item_id": item_id, "q": q}}
