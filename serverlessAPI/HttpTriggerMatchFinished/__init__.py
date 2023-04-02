import logging
import os
import time

import json

import requests

import azure.functions as func

from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient

faceitTokenHeader = {"Authorization":f"Bearer {os.environ['FACEIT_TOKEN']}"} #Token to authorize to Faceit API
playersTable = os.environ["STORAGE_TABLE_PLAYERS"]

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    playersWatched = getDictionaryOfWatchedPlayers()

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
    tableName = playersTable #table 
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

def getDictionaryOfWatchedPlayers():
    # Get to storage account
    credential = DefaultAzureCredential()
    table_service_client = TableServiceClient(
        endpoint=os.environ["STORAGE_ENDPOINT_TABLE"],
        credential=credential)

    # Get Storage Account table    
    table_client = table_service_client.get_table_client(table_name="playersWatched")
    entities     = table_client.list_entities() #List all entities from table

    playersList = [] #Prepare list to save players
    for entity in entities:
        playersList.append(entity["PartitionKey"]) #Save in proper format to list
 
    return playersList