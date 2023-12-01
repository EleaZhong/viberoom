from flask import Flask
from dotenv import load_dotenv
import os
import urllib.parse

app = Flask(__name__)

def get_access():
    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    redirect_uri = 'http://localhost:5000/'
    scope = 'user-modify-playback-state'

    url = 'https://accounts.spotify.com/authorize'
    url += '?response_type=token'
    url += '&client_id=' + urllib.parse.quote(client_id, safe="!~*'()")
    url += '&scope=' + urllib.parse.quote(scope, safe="!~*'()")
    url += '&redirect_uri=' + redirect_uri

    return url

if __name__ == '__main__':
    print(get_access())