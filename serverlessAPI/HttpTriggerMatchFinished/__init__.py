import logging
import uuid
import json

import azure.functions as func

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage], outputTable: func.Out[str]) -> str:
    logging.info('Python HTTP trigger function processed a request.')

    # Acquire a credential object
    credential = DefaultAzureCredential()
    blob_service_client = BlobServiceClient(
        account_url="https://storage69415.blob.core.windows.net",
        credential=credential)

    containers = blob_service_client.list_containers()
    for container in containers:
            print(container['name'])

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        msg.set(name)

        rowKey = str(uuid.uuid4())
        data = {
            "Name": "Output bindin message",
            "PartitionKey": "message",
            "RowKey": rowKey
        }
        outputTable.set(json.dumps(data))
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. RowKey: {rowKey}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
