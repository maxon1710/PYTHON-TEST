import requests

def get_rate():
    response = requests.get("https://api.exchangerate.com")
    print (response)
    return response.json()["rate"]
