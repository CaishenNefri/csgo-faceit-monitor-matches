import requests
from flask import Flask
import json
myapp = Flask(__name__)

@myapp.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux - 04 September 2022 check"

@myapp.route("/mejz", methods=['GET', 'POST'])
def parse_request():
    response = requests.get(
            "https://open.faceit.com/data/v4/players/4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb/history?game=csgo&offset=0&limit=5",
            headers={"Authorization":"Bearer ***REMOVED***"}
        )
    print(response)
    print(response.json())
    return response.json()["items"][0]

# def get_player_team(match, player):  