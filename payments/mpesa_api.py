import requests
from requests.auth import HTTPBasicAuth

consumer_key = "gFpApA8usNRPpNNLhDTw5tYYG7qZ1V8LAUsxpeEhGgMof1dG"
consumer_secret = "75ZiItGbGVrzrW5pnvGWFciAiUx7v6aDotHieX3JMHwj1GG0bmkqJvP2WFHlR7vM"


def get_access_token():
    consumer_key = "gFpApA8usNRPpNNLhDTw5tYYG7qZ1V8LAUsxpeEhGgMof1dG"
    consumer_secret = "75ZiItGbGVrzrW5pnvGWFciAiUx7v6aDotHieX3JMHwj1GG0bmkqJvP2WFHlR7vM"
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        raise Exception("Failed to get access token")