# TODO
  - Done: Create infrastructure with terraform: https://docs.microsoft.com/en-us/azure/app-service/provision-resource-terraform
  - Done: Getting started with Python in Azure: https://docs.microsoft.com/en-us/azure/developer/python/cloud-development-overview
  - Done: Create simple HelloWorld Pyton app: 
    - https://docs.microsoft.com/en-us/azure/developer/python/tutorial-deploy-app-service-on-linux-01
    - https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-portal%2Cterminal-bash%2Clocal-git-deploy%2Cdeploy-instructions-azportal%2Cdeploy-instructions-zip-azcli
  - Done: Learn how to edite Python Code in Visual Studio https://code.visualstudio.com/docs/python/editing
  - Nope: Deploy on Azure HelloWorld Python app by terraform
  - Done: Read about Key concepts: https://docs.microsoft.com/en-us/azure/devops/pipelines/get-started/key-pipelines-concepts?view=azure-devops
  - Done: Deploy CI/CD:
    - https://docs.microsoft.com/en-us/azure/devops/pipelines/ecosystems/python-webapp?view=azure-devops
    - https://docs.microsoft.com/en-us/azure/devops/pipelines/targets/webapp?view=azure-devops&tabs=linux%2Cyaml
  - Done: Check if Pipeline will work with new terraform infra
    - create ServicePrincipal with owner permissions
    - update main.tf
  - Done: Update terraform file: use new app service new as a variable in Azure DevOps pipeline
  - Done: Use in pipeline dynamic app-service name
  - Done: Add keyvault to pipeline
  - Done: Run Terraform from yaml pipeline
    - do plan
    - do apply using generated plan
    - authenticate: https://julie.io/writing/terraform-on-azure-pipelines-best-practices/#:~:text=difficult%20to%20understand.-,Why%20does%20az%20login%20not%20work%20in%20CI/CD%3F,-In%20short%2C%20it
    - https://julie.io/writing/terraform-on-azure-pipelines-best-practices/ 
  - Intergrate keyvault
    - Azure DevOps personal access token
    - service principal for terraform
  - Done: Python webpage with list of mejz matches
    - Done: Load test json not from API
    - Done: create function to call API
    - Done: List match (team, score) for one player
    - Done: List last 10 matches
    - Done: Add time when match finished: https://realpython.com/python-datetime/
  - Done: Create Python Function to catch webhook
    - Done: Create terraform Infra with Azure Function
    - Done: Prepare helloworld code to grap data from Postman
      - https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-configuration
      - https://learn.microsoft.com/en-us/azure/azure-functions/scripts/functions-cli-create-serverless-python
      - https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-decorators
    - Done: Deploy App to Azure Function
    - Done: Save grabbed code to Storage Account Table
      - Example for adding msg to queue: https://learn.microsoft.com/en-us/azure/azure-functions/functions-add-output-binding-storage-queue-vs-code?tabs=in-process&pivots=programming-language-python
      - Example for using tables: https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-table-output?tabs=in-process%2Cstorage-extension&pivots=programming-language-python
      - Can not use dynamic table name (why? no fuckinf idea). have to use Pyhon SDK
        - https://pypi.org/project/azure-data-tables/
        - https://pypi.org/project/azure-storage-blob/
        - https://learn.microsoft.com/en-us/azure/developer/python/sdk/authentication-overview
      - Done: Create table from request: Table Contributor must be granted!!!
    - Done: Use different tables
    - Done: Create managed identity -> user user assigned idenitity instead
      - Done: managed identity can not be created and used in one terraform apply run -->> https://github.com/hashicorp/terraform/issues/29923
      - Done: assign permission to terraform service prencipal to be able to assign permissions
      - Done: create user managed identity
      - Done: Tweak code to use user assigned identity: 
        - https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python#:~:text=their%20home%20tenants.-,managed_identity_client_id,-str
        - https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.managedidentitycredential?view=azure-python
        - Use Env variable: https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level&pivots=python-mode-decorators#environment-variables
    - collect Faceit raw request from postman
    - Done: grap storage account url from Terraform/Variable/etc -> Done via App Settings 
  - Done: Add some kind of monitoring or diagnostic settings
    - use App Insights to enable log streaming: https://learn.microsoft.com/en-us/azure/azure-functions/functions-monitoring
    - problem with app_settings | set_config updated from nowhere
  - Done: Azure Function to update table when match finishend
  - Done: Azure Function get INFO who is playing - for whome we get webhook
  - Done: Save to table info about ELO points
  - Display/Plot graph on main page
    - Not needed as Mejz is gamer: Push dump data to table (10 matches - elo changes)
    - Done: Read from storage table
    - Plot graph for one player: https://www.chartjs.org/docs/latest/general/data-structures.html
    - Plot for each player
    - Switch to real data
  - Done: Create LOCK to not delete Storage Account / terraform disable destroying
  - Azure Function Webhook Subsription provide security header and query string
  - Move token from _init_.py outside code
  - Disaply last 10 matches
  - Set triggers
    - https://pumpingco.de/blog/run-an-azure-pipelines-job-only-if-source-code-has-changed/
    - https://learn.microsoft.com/en-us/azure/devops/pipelines/process/pipeline-triggers?view=azure-devops
    - https://learn.microsoft.com/en-us/azure/devops/pipelines/process/resources?view=azure-devops&tabs=schema
    - Use templates
    - condition for terraform
    - condition for Azure Function
    - condition for Azure WebSite
  - Move Python code to container
  - Tweak deploying to use artifacts


# Links
  - Faceit App: https://developers.faceit.com/apps/5f1ce3c7-a4f1-4bba-89e2-7851728477d3
  - Faceit Developer portal: https://developers.faceit.com/


# DATA
- API Key:
    - >***REMOVED***
<!-- - 1-5c99a93b-8caa-44fd-9def-d407f8737676
- a0b4a0e5-f633-47f1-ae4b-a9b6cd0a8399 -->
- Mejz id - player_id:
    - >4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb

## Players IDs
mejz    : '4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb',
lewy    : '78491fee-bcdb-46d2-b9df-cae69862e01c',
neo     : '00c0c7ae-3e57-45d3-82c2-c167fd45fdaf',
kapa    : '993fa04b-8e3b-4964-b9f0-32ca1584e699',
hajsen  : '14cadb67-6c68-4896-99d3-e3f8a5d509b1',
caishen : '5ba2c07d-072c-4db9-a08d-be94f905899c',
fanatyk : 'dde67c08-df21-4f65-a7b6-46e4ad550f25',
kobze   : '3e2857f6-3a7e-443f-99b7-0bcd1a5114a6'


# Set env variable
$env:AZDO_PERSONAL_ACCESS_TOKEN="***REMOVED***"
$env:AZDO_ORG_SERVICE_URL="https://dev.azure.com/Caishen"


# Know problems
1. Azure DevOps Pipeline do not see existing resource right after manually creation. Resolution: try implement terraform into pipeline | do not destry infra
  - https://github.com/microsoft/azure-pipelines-tasks/issues/15532
  - `https://www.garyjackson.dev/posts/azure-function-app-conflicting-plans/`
  - Not Mitigated: need to way untill is accesible 
2. Web Service Plan must be created after Function App Serivce Plan:
  - https://www.garyjackson.dev/posts/azure-function-app-conflicting-plans/
  - https://github.com/hashicorp/terraform-provider-azurerm/issues/10020
  - Mitigated: by removing all infra and recreate them with depends_on 

# Python APP - website
Install reqiriments:
`pip install -r requirements.txt`
Run Python Flask server (debug to restart server on each code change):  
`flask --app hello.py run --debug`+

# Setup
## Manual steps
- Grant Terraform Service Principal permission to grant privileges 

# Azure Function - grap webhooks from Faceit
Faceit Dev can send webhook data when it's subscribed: https://developers.faceit.com/apps/5f1ce3c7-a4f1-4bba-89e2-7851728477d3/webhooks
We have to put IDs of players to get infromaiton about status.  


## Implementation:  
Azure Function is used as serverless API to receiving Faceit's webhooks
https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python
https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-powershell%2Cpowershell%2Cbrowser