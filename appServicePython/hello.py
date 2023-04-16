import requests
import os
from flask import Flask, render_template
import json
from datetime import datetime #To convert TimeStamp
from dateutil import tz #To use CET instead UTC


# Access to Azure Storage Account Table
from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient

faceitTokenHeader = {"Authorization":f"Bearer {os.environ['FACEIT_TOKEN']}"} #Token to authorize to Faceit API


myapp = Flask(__name__)

player_mejz_id = "4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb"

@myapp.route("/dateUpdate")
def hello():
    return "Hello Flask, on Azure App Service for Linux - 04 September 2022 check"

@myapp.route("/mejz", methods=['GET', 'POST'])
def parse_request():
    f           = open('mejz_matches.json')
    response    = json.load(f)
    match       = response["items"][0]
    timeMatch   = getMatchTimeFinish(match)
    print(timeMatch)
    return "OK"

@myapp.route("/mejzMatches", methods=['GET', 'POST'])
def list_maches():
    response = getPlayerMatches(player_mejz_id, limit = 10) # function to get player matches from API
    summary = ""
    for match in response["items"]:
        team                = getPlayerTeam(match, player_mejz_id)
        matchStats          = getMatchStats(match)
        matchMap            = getMatchMap(matchStats)
        matchScore          = getMatchScore(matchStats)
        ifWon               = ifTeamWon(match, team)    
        timeMatchFinished   = getMatchTimeFinish(match)
        match_summary       = f"Map: {matchMap} | Score: {matchScore} | Win: {ifWon} | Finished at: {timeMatchFinished}"
        print(match_summary)
        summary             = summary + "<br/>" + match_summary
    return summary

@myapp.route("/", methods=['GET', 'POST'])
@myapp.route("/graph", methods=['GET', 'POST'])
def plot_graph():
    players = getDictionaryOfWatchedPlayers() #Get list of watched players from Azure Storage Account Table

    credential = DefaultAzureCredential()
    table_service_client = TableServiceClient(
        endpoint=os.environ["STORAGE_ENDPOINT_TABLE"],
        credential=credential)

    table_client = table_service_client.get_table_client(table_name="players")

    plot_data = {}
    for name, id in players.items():
        print(name)
        print(id)
        parameters = {
            "pk": id,
        }    
        query_filter = "PartitionKey eq @pk"
        entities     = table_client.query_entities(query_filter, parameters=parameters)

        # Fulfill python dictionary
        plot_data[name] =  {}
        plot_data[name]["data"] = []
        plot_data[name]["labels"] = []
        plot_data[name]["kdRatio"] = []
        plot_data[name]["matchMap"] = []
        plot_data[name]["matchScore"] = []
        plot_data[name]["ifWin"] = []

        for entity in entities:
            date_time = entity.get("RowKey")
            date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%SZ') # Convert string TimeStamp to Date Time
            date_time = date_time.replace(tzinfo=tz.UTC) # Assign UTC to Date Time
            date_time = date_time.astimezone(tz.gettz("Europe/Warsaw")) # Convert from UTC to "Europe/Warsaw"
            date_time = date_time.strftime("%Y/%m/%d %H:%M") # Convert Date Time to string as Chart.js is going back to UTC

            plot_data[name]["data"].append(entity.get("Elo")) #Append Elo to data set
            plot_data[name]["labels"].append(date_time) # Append date_time to X axis for graph
            plot_data[name]["kdRatio"].append(entity.get("kdRatio", "-")) ##Append KD to plot_data
            plot_data[name]["matchMap"].append(entity.get("matchMap", "-")) ##Append Map of Match to plot_data
            plot_data[name]["matchScore"].append(entity.get("matchScore", "-")) ##Append Final Score of match to plot_data
            plot_data[name]["ifWin"].append(entity.get("ifWin", "")) ##Append if match Won to plot_data
   
 
    # Return the components to the HTML template
    return render_template(
        template_name_or_list='graph.html',
        plot_data=plot_data,
    )


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
            headers=faceitTokenHeader
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
            headers=faceitTokenHeader
    )
    return response.json()

def getPlayerElo(player):
    response = requests.get(
            f"https://open.faceit.com/data/v4/players/{player}",
            headers=faceitTokenHeader
        )
    toJson = response.json()
    return toJson["games"]["csgo"]["faceit_elo"]

def getMatchTimeFinish(match):
    timeStamp = match["finished_at"] # get timestamp from json match details
    date_time = datetime.fromtimestamp(timeStamp, tz=tz.gettz("Europe/Warsaw")) # convert timestamp to to datetime object and switch to "Europe/Warsaw" timezone
    date_time = date_time.strftime("%m/%d/%Y, %H:%M:%S") # convert datiem to human read string
    return date_time

def getDictionaryOfWatchedPlayers():
    # Get to storage account
    credential = DefaultAzureCredential()
    table_service_client = TableServiceClient(
        endpoint=os.environ["STORAGE_ENDPOINT_TABLE"],
        credential=credential)

    # Get Storage Account table    
    table_client = table_service_client.get_table_client(table_name="playersWatched")
    entities     = table_client.list_entities() #List all entities from table

    playersList = {} #Prepare dictionary to save players
    for entity in entities:
        playersList[entity["RowKey"]] = entity["PartitionKey"] #Save in proper format to dictionary
 
    return playersList