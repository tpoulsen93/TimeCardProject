# Download the helper library from https://www.twilio.com/docs/python/install
import json
import os
from twilio.rest import Client
from dotenv import load_dotenv
from datetime import date

from fastapi import FastAPI, Request, Form
from pydantic import BaseModel

load_dotenv()
account = os.environ.get('account_sid')
token = os.environ.get('auth_token')

app = FastAPI()



# client = Client(account_sid, auth_token)

# message = client.messages \
#                 .create(
#                      body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#                      from_='+18324971734',
#                      to='+12083500006'
#                  )

# print(message.sid)

users = {
    "+12083500006": "Taylor Poulsen",
    "+14322761331": "Daniel Bogden"
}


class SMS(BaseModel):
    From: str
    Body: str


@app.get("/")
def read_root():
    today = date.today()
    return {"msg": f"Hello, Taylor.  Today is {today}"}


@app.post("/sms")
async def response(From: str = Form(...), Body: str = Form(...)) -> str:
    print(f"Mesage from: {From}")
    print(f"Body: {Body}")
    pass
    


