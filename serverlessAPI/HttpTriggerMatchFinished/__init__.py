import logging
import os

import azure.functions as func

from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Acquire a credential object
    credential = DefaultAzureCredential()
    table_service_client = TableServiceClient(
        endpoint=os.environ["STORAGE_ENDPOINT_TABLE"],
        credential=credential)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        logging.info(f"Try to create table {name}")
        table_service_client.create_table_if_not_exists(name)

        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
