import time

import requests_mock
import requests

def payment_webhook(data):
    if data["type"] == "payment_intent.succeeded":
        return f"Payment succeeded for ID: {data['data']['object']['id']}"
    elif data["type"] == "payment_intent.payment_failed":
        return f"Payment failed for ID: {data['data']['object']['id']}"

with requests_mock.Mocker() as mock:
    mock.post(
        url="https://myapp.com/webhook",
        json={
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_12345"}}
        }
    )

    webhook_response = requests.post(
        url="https://myapp.com/webhook",
        json={
            "type": "payment_intent.succeeded",
            "data": {"object": {"id": "pi_12345"}}
        }
    )

    print(payment_webhook(webhook_response.json()))