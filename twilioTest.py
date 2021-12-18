# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['AC37804c695edc1fb632643fbfff0c3245']
# auth_token = os.environ['2a47bca83b62c8db87c9f801b6b7a4e8']
account_sid = 'AC37804c695edc1fb632643fbfff0c3245'
auth_token = '2a47bca83b62c8db87c9f801b6b7a4e8'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",
                     from_='+18324971734',
                     to='+12083500006'
                 )

print(message.sid)
