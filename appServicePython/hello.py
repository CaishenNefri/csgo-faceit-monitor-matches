from asyncio.windows_events import NULL
from dataclasses import dataclass
from operator import truediv
import re
from urllib import response
import requests
from flask import Flask
import json
from datetime import datetime #To convert TimeStamp
from dateutil import tz #To use CET instead UTC

myapp = Flask(__name__)

player_mejz_id = "4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb"

@myapp.route("/")
def hello():
    return "Hello Flask, on Azure App Service for Linux - 04 September 2022 check"

@myapp.route("/mejz", methods=['GET', 'POST'])
def parse_request():
    f = open('mejz_matches.json')
    response = json.load(f)
    # response = getPlayerMatches(player_mejz_id) # function to get player matches from API
    match = response["items"][0]
    timeMatch =  getMatchTimeFinish(match)
    print(timeMatch)
    return "OK"

@myapp.route("/mejzMatches", methods=['GET', 'POST'])
def list_maches():
    response = getPlayerMatches(player_mejz_id, limit = 10) # function to get player matches from API
    summary = ""
    for match in response["items"]:
        team = getPlayerTeam(match, player_mejz_id)
        matchStats = getMatchStats(match)
        matchMap = getMatchMap(matchStats)
        matchScore = getMatchScore(matchStats)
        ifWon = ifTeamWon(match, team)    
        timeMatchFinished = getMatchTimeFinish(match)
        match_summary = f"Map: {matchMap} | Score: {matchScore} | Win: {ifWon} | Finished at: {timeMatchFinished}"
        print(match_summary)
        summary = summary + "<br/>" + match_summary
    return summary


def getPlayerTeam(match, player):
    for team in match["teams"]:
        print(team)
        print(match["teams"][team]["team_id"])
        for gamer in match["teams"][team]["players"]:
            print(gamer["nickname"])
            if(player == gamer["player_id"]):
                print(f"Player {player} playing for {team}")
                return team

def ifTeamWon(match, team):
    if(match["results"]["winner"] == team):
        print(f"{team} won")
        return True
    else:
        print(f"{team} loose")
        return False

def getPlayerMatches(player, offset = 0, limit = 10):
    response = requests.get(
            f"https://open.faceit.com/data/v4/players/{player}/history?game=csgo&offset={offset}&limit={limit}",
            headers={"Authorization":"Bearer ***REMOVED***"}
        )
    print("test")
    print(response.json())
    return response.json()

def getMatchScore(matchStats):
    return matchStats["rounds"][0]["round_stats"]["Score"]

def getMatchMap(matchStats):
    return matchStats["rounds"][0]["round_stats"]["Map"]

def getMatchStats(match):
    match_id = match["match_id"]
    response = requests.get(
        f"https://open.faceit.com/data/v4/matches/{match_id}/stats",
            headers={"Authorization":"Bearer ***REMOVED***"}
    )
    return response.json()

def getPlayerElo(player):
    response = requests.get(
            f"https://open.faceit.com/data/v4/players/{player}",
            headers={"Authorization":"Bearer ***REMOVED***"}
        )
    toJson = response.json()
    return toJson["games"]["csgo"]["faceit_elo"]

def getMatchTimeFinish(match):
    timeStamp = match["finished_at"] # get timestamp from json match details
    date_time = datetime.fromtimestamp(timeStamp, tz=tz.gettz("Europe/Warsaw")) # convert timestamp to to datetime object and switch to "Europe/Warsaw" timezone
    date_time = date_time.strftime("%m/%d/%Y, %H:%M:%S") # convert datiem to human read string
    return date_time