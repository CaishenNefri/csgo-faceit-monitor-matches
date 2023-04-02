import logging
import os
import time

import json

import requests

import azure.functions as func

from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient

## Players IDs to see who played match
playersWatched = [
'4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb', #mejz   
'78491fee-bcdb-46d2-b9df-cae69862e01c', #lewy   
'00c0c7ae-3e57-45d3-82c2-c167fd45fdaf', #neo    
'993fa04b-8e3b-4964-b9f0-32ca1584e699', #kapa   
'14cadb67-6c68-4896-99d3-e3f8a5d509b1', #hajsen 
'5ba2c07d-072c-4db9-a08d-be94f905899c', #caishen
'dde67c08-df21-4f65-a7b6-46e4ad550f25', #fanatyk
'3e2857f6-3a7e-443f-99b7-0bcd1a5114a6', #kobze
'30536f2c-ae65-4403-9d3e-64c01724a6ff', #'hrd
'cbd5f9a1-6e80-4122-a222-2ec0c8f06261' #DaiSS
]
# Test players list
# playersWatched = [
#     'b45dcc4e-f205-4d50-adc3-f25bf3050632',
#     'f9f6be9c-a8cf-45e9-800a-ffd1e89f33aa'
# ]

faceitTokenHeader = {"Authorization":f"Bearer {os.environ['FACEIT_TOKEN']}"} #Token to authorize to Faceit API

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Acquire a credential object to be able to insert to Storage Account
    credential = DefaultAzureCredential()
    table_service_client = TableServiceClient(
        endpoint=os.environ["STORAGE_ENDPOINT_TABLE"],
        credential=credential)


    # Log whole webhook payload
    payload = req.get_json()
    dump    = json.dumps(payload, indent=2)
    # logging.info(f"Login payload body of webhook \n{dump}") 

    ####################################
    #Part for further autorization of webhook request
    # name = req.params.get('name')
    # if not name:
    #     try:
    #         req_body = req.get_json()
    #     except ValueError:
    #         pass
    #     else:
    #         name = req_body.get('name')
    #####################################

    logging.info(f"Get details from match: timestamp and match id")
    timestamp = payload.get('timestamp')
    matchId   = payload.get('payload').get('id')
    
    #List all players from match
    playersPlayed = []
    logging.info(f"List all players from match")
    for team in payload.get('payload').get('teams'):
        for player in team.get('roster'):
            playerId = player.get('id') 
            logging.info(f"PlayerID {playerId}")
            playersPlayed.append(playerId)

    playersPlayedWatched = []
    #Compare who is playing match from payload
    for pPlayed in playersPlayed:
        for pWatched in playersWatched:
            if (pPlayed == pWatched):
                logging.info(f"Following player played and we watch him: {pPlayed}")
                playersPlayedWatched.append(pPlayed)

    logging.info(f"Players Played and Watched: {playersPlayedWatched}")    
    playersStats = getPlayerStatsFromMatch(matchId, playersPlayedWatched)

    for pWatched in playersPlayedWatched:
        elo = getPlayerElo(pWatched)
        pushToTable(table_service_client, pWatched, timestamp, elo, matchId, playersStats[pWatched])

    return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
    )


def pushToTable(table_service_client, playerId, timestamp, elo, matchId, stats):
    # tableName = "players" #prod table 
    tableName = "playersTest" #test table
    entity = {
        'PartitionKey': playerId,
        'RowKey'      : timestamp,
        'Elo'         : elo,
        'MatchId'     : matchId
    }
    for key in stats.keys():
        entity[key] = stats[key]


    logging.info(f"Create table {tableName} if not exist")
    table_service_client.create_table_if_not_exists(tableName)
    logging.info(f"Get table client")
    table_client = table_service_client.get_table_client(table_name=tableName)
    logging.info(f"Push following entity to table: {entity}")
    try:
        response = table_client.create_entity(entity=entity)
        logging.info(f"Print response {response}")
    except:
        logging.info(f"Something goes wrong. Propably entity already exist")
        #TODO use ErrorName

def getPlayerElo(playerId):
    response = requests.get(
            f"https://open.faceit.com/data/v4/players/{playerId}",
            #TODO Remove token from code
            headers=faceitTokenHeader
        )
    toJson = response.json()
    return toJson["games"]["csgo"]["faceit_elo"]

def getPlayerStatsFromMatch(matchId: str, playersId : list):
    # Request match details for specific player
    response = requests.get(
        f"https://open.faceit.com/data/v4/matches/{matchId}/stats",
        #TODO Remove token from code
        headers=faceitTokenHeader
        )

    
    matchStats = response.json() # conver reposne from Faceit to json
    matchStats = matchStats["rounds"][0]
    logging.info(f"Dump match stats from faceit response:\n{json.dumps(matchStats, indent=2)}")
    
    playersStats = {}
    matchRounds = int(matchStats["round_stats"]["Rounds"])
    
    for playerId in playersId:
        playerStats  = {} # Python dictinary
        playerStats["matchMap"] = matchStats["round_stats"]["Map"]
        # Find specific player details and save to dictionary
        for team in matchStats["teams"]:
            playerFound = False
            for player in team["players"]:
                if (playerId == player["player_id"]):
                    playerFound = True
                    playerS = player["player_stats"]
                    playerStats["kills"]   = int(playerS["Kills"])
                    playerStats["deaths"]  = int(playerS["Deaths"])
                    playerStats["kdRatio"] = playerS["K/D Ratio"]
                    playerStats["kpr"]     = playerStats["kills"]/matchRounds
                else:
                    continue

            # If player founded then save last details and return from function
            if (playerFound):
                playerStats["ifWin"]       = team["team_stats"]["Team Win"]
                finalScore                 = int(team["team_stats"]["Final Score"])
                playerStats["matchScore"]  = f"{finalScore} / {matchRounds-finalScore}"
                logging.info(f"Saved details to dictionary \n{playerStats}")
                playersStats[playerId] = playerStats
                break
    
    return playersStats