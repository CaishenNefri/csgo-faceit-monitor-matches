from operator import truediv
from urllib import response
import requests
from flask import Flask
import json
myapp = Flask(__name__)

@myapp.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux - 04 September 2022 check"

@myapp.route("/mejz", methods=['GET', 'POST'])
def parse_request():
    f = open('mejz_matches.json')
    response = json.load(f)
    # for match in response["items"][0]:
    # match = response["items"][0]
    response = requests.get(
            "https://open.faceit.com/data/v4/players/4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb/history?game=csgo&offset=0&limit=5",
            headers={"Authorization":"Bearer ***REMOVED***"}
        )
    match = response.json()
    match = match["items"][0]
    team = getPlayerTeam(match, "4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb")
    print(ifTeamWon(match, team))
    return "OK"

def getPlayerTeam(match, player):
    for team in match["teams"]:
        print(team)
        print(match["teams"][team]["team_id"])
        for gamer in match["teams"][team]["players"]:
            print(gamer["nickname"])
            if(player == gamer["player_id"]):
                return team

def ifTeamWon(match, team):
    if(match["results"]["winner"] == team):
        return True
    else:
        return False

def getPlayerMatches(player):
    response = requests.get(
            "https://open.faceit.com/data/v4/players/{player}/history?game=csgo&offset=0&limit=5",
            headers={"Authorization":"Bearer ***REMOVED***"}
        )
    print("test")
    print(response.json())
    return response.json()