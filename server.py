from typing import Union
from main import ChatbotHandler
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
bot = ChatbotHandler()

origins = [
    "localhost",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"intellitrip": "API up"}


@app.get("/consulta/")
def read_item(input: str):
    response = bot.request_bot(input=input)
    return json.loads(response) 
