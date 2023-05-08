import logging
import os
import time

import json

import requests

from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient

def main():
    logging.info('SMS App triggered')

    # Acquire a credential object to be able to insert to Storage Account
    credential = DefaultAzureCredential()

    queue_service_client = QueueClient(
        account_url = os.environ["STORAGE_ENDPOINT_QUEUE"],
        credential  = credential,
        queue_name  = os.environ["QUEUE_NAME"]
        )
    
    while(True):
        msg = queue_service_client.receive_message()
        if (msg == None): 
            logging.info("Message queue is empty. Stopping script")
            print("Message queue is empty. Stopping script")
            break
        
        print(f"Message body: {msg}")

        
        nick = getPlayerNick(msg.content)        
        sendSMS(nick)


        queue_service_client.delete_message(msg)
    

def sendSMS(nickname="unknown"):
    print(f"SMS Send for {nickname}")

def getPlayerNick(playerId):
    dictionary = {
        "4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb" : "mejz", 
        "993fa04b-8e3b-4964-b9f0-32ca1584e699" : "kapa" 
    }
    try:
        return dictionary[playerId]
    except:
        return "Unknown"

if __name__ == '__main__':
    main()
    