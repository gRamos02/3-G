from typing import Union

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/consulta")
def read_item(item_id: int, q: Union[str, None] = None):
    """
    """
    return {"item_id": item_id, "q": q}
