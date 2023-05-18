import logging
import os

import json

from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient

def main():
    logging.basicConfig(filename="logs.log", level=logging.INFO)
    logging.info('SMS App triggered')

    logging.info("Get Subscriber's Numbers")
    subscribers = getRecipients()

    # Acquire a credential object to be able to insert to Storage Account
    logging.info("Authenticate to queue")
    credential = DefaultAzureCredential()
    queue_service_client = QueueClient(
        account_url = os.environ["STORAGE_ENDPOINT_QUEUE"],
        credential  = credential,
        queue_name  = os.environ["QUEUE_NAME"]
        )
    
    logging.info("Start loop trought messages in queue.")
    while(True):
        logging.info("Get message from queue")
        msg = queue_service_client.receive_message()
        logging.info(f"Message received: {msg}")
        if (msg == None): 
            logging.info("Message queue is empty. Stopping script")
            break
        else:
            queue_service_client.delete_message(msg, msg.pop_receipt)
            nick = getPlayerNick(msg.content)
            if (nick):
                for sub in subscribers["Contacts"]:
                    sms = f'{nick}\ znów\ przegrał\ faceita\ Miłego\ dnia\ {sub["Nick"]}'
                    sendSMS(sub["Number"], sms)
            
        
        
    

# Sending sms via Android Debug Bridge (ADB)
# Mobile phone is connected via usb cable to PC/Raspberry and it has enabled usb debugging 
def sendSMS(recipient, message):
    # +48790998250 - is a Short Message service center (SMSC) for Play operator
    cmd = f'adb shell service call isms 6 s16 "com.android.mms" s16 "{recipient}" s16 "+48790998250" s16 "{message}" i32 0 i32 0'
    os.system(cmd)

def getPlayerNick(playerId):
    dictionary = {
        "4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb" : "mejz", 
        "993fa04b-8e3b-4964-b9f0-32ca1584e699" : "kapa" 
    }
    try:
        nick = dictionary[playerId]
        logging.info(f"Parse message to player name: {nick}")
        return nick
    except:
        logging.info("Player not on the list.")
        return False
    
def getRecipients():
    # Opening JSON file
    f = open(os.environ["FILE_SUB_NUMBERS"])
    
    # returns JSON object as a dictionary
    data = json.load(f)
    return data


# Run main function
if __name__ == '__main__':
    main()
    