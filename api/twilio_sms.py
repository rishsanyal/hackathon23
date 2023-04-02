import os
from twilio.rest import Client

account_sid = "ACf6c06a8ac5a7db8fd1072e68cac96150"
auth_token = os.environ["10cbe160498be5958654970eebbbbf7e"]
client = Client(account_sid, auth_token)
message = client.messages.create(
  body="Helloooooooo",
  from_="+18555791042",
  to="+14155681694"
)
print(message.sid)