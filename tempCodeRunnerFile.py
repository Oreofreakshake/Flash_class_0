import requests
import sys

API_URL = "https://rest.messagebird.com/messages"
API_KEY = "vCDUBHy51glPCXeJANB3VuGaq"

RECIPIENT = int(input("Number: "))
ORIGINATOR = str(input("Name: "))
TEXT = str(input("SMS: "))

payload = {
    "recipients": RECIPIENT,
    "originator": ORIGINATOR,
    "body": TEXT,
    "type": "flash",
}

for i in range(10):
    requests.post(
        API_URL, headers={"Authorization": f"AccessKey {API_KEY}"}, data=payload
    )