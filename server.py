from typing import Union
from main import ChatbotHandler
from fastapi import FastAPI

app = FastAPI()
bot = ChatbotHandler()

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/consulta/")
def read_item(input: str):
    response = bot.request_bot(input=input)
    return  response 
