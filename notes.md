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
  - Done: Display/Plot graph on main page
    - Not needed as Mejz is gamer: Push dump data to table (10 matches - elo changes)
    - Done: Read from storage table
    - Done: Plot graph for one player: https://www.chartjs.org/docs/latest/general/data-structures.html
    - Done: Plot for each player
  - Done: Create LOCK to not delete Storage Account / terraform disable destroying
  - Done: Save K/D and other match stats to Storage Account
  - Done: Display match stats on graph
  - Done: Add Dais to watcher
  - Done: Remove Faceit Token from code
  - Done:  Use env env for storage account table endpoint
  - Done: Move Watched Plaers list outside of code
  - Done: Move token from _init_.py outside code
  - Azure Function Webhook Subsription provide security header and query string
  - Done: Rotate secrets
    - DevOps token
    - Service Principal Terraform: Caishen-csgo-faceit-monitor-matches-1564f82f-9f08-47e0-9939-5e3dcc739b5e 
    - FaceitToken
    - Remove sensitive data form GitHub repository
      - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository
    - Rotated faceit, devops and sp tokens
  - Done: Publish GitHub Repository
  - Prepare ReadMe
    - Diagram
    - How it works
    - Screenshots
  - Done: Analyze how to use custom domain in Web Service
  - Done: Use Custom Domain
    - buy domain
    - create subdomain
    - create certificate
  - SMS Notification
    - Done: Read Azure Communication Services => only available for paied subscriptions
    - Done: Create Queune for pushing notifications
    - Done: Push notification to queue via Powershell/Curl/Python | Works with storage key but not with DefaultAzureCredential because identity didn't have storage account queue contributor
    - Done: Read queue Python
    - Done: Loop through every message in queue
    - Done: Compare id to player name
    - Understand logging inside Python script
    - Activate Sim Card
    - Use USB Modem/Bring other modem
    - Send simple sms via modem
    - Send SMS via Python
    - Table with numbers
    - Table to check who should be "szkalowany"
    - Update Function to send to queue 
    - Create Python App and Docker Container
    - Install Rasperry 
    - Ansible script to download and use docker image with our app
    - Put Raspberry to the wardrobe
    - How to keep secret in environmet variables as encrypted
    - Create GitHub release for application
  - Impemented Azure Open AI for SMS Notifications
    - Read docs about OpenAI on Azure
    - Greetings base on day, time ("Miłego dnia", miłego wieczoru etc")
  - Set triggers in DevOps pipeline
    - https://pumpingco.de/blog/run-an-azure-pipelines-job-only-if-source-code-has-changed/
    - https://learn.microsoft.com/en-us/azure/devops/pipelines/process/pipeline-triggers?view=azure-devops
    - https://learn.microsoft.com/en-us/azure/devops/pipelines/process/resources?view=azure-devops&tabs=schema
    - Use templates
    - condition for terraform
    - condition for Azure Function
    - condition for Azure WebSite
  - Move Python code to container
  - Create schedulled Azure function to calculate average ELO per year, month, week, day
  - Tweak deploying to use artifacts
  - Use containers to run terraform inside Azure DevOps - in ADO there is not the newest version of terraform
  - Done: Use refresh=false at terraform apply stage -> will increase speed but could be harmfull (not yuet tested)


# Links
  - Faceit App: https://developers.faceit.com/apps/5f1ce3c7-a4f1-4bba-89e2-7851728477d3
  - Faceit Developer portal: https://developers.faceit.com/


# DATA
## Players IDs
mejz    : '4ea9d337-ad40-4b55-aab1-0ecf7d5e7dcb',
lewy    : '78491fee-bcdb-46d2-b9df-cae69862e01c',
neo     : '00c0c7ae-3e57-45d3-82c2-c167fd45fdaf',
kapa    : '993fa04b-8e3b-4964-b9f0-32ca1584e699',
hajsen  : '14cadb67-6c68-4896-99d3-e3f8a5d509b1',
caishen : '5ba2c07d-072c-4db9-a08d-be94f905899c',
fanatyk : 'dde67c08-df21-4f65-a7b6-46e4ad550f25',
kobze   : '3e2857f6-3a7e-443f-99b7-0bcd1a5114a6',
hrd     : '30536f2c-ae65-4403-9d3e-64c01724a6ff',
Daiss   : 'cbd5f9a1-6e80-4122-a222-2ec0c8f06261'

List of watched players is now stored in storage account in playersWatched table to be easily managed from one place



# Set env variable
$env:AZDO_PERSONAL_ACCESS_TOKEN="xxx" # from key vaults
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

# Local Develop/Debug
## Python APP - website
To be able to run locally App Service we need to run following commands in sequence
Install reqiriments:
`pip install -r requirements.txt`
Use local env app settings = get values from KeyVault to not have them saved in code repository
```Powershell
Connect-AzAccount
$Env:STORAGE_ENDPOINT_TABLE = Get-AzKeyVaultSecret -VaultName 'kv69415' -Name 'STORAGE-ENDPOINT-TABLE' -AsPlainText
$Env:FACEIT_TOKEN           = Get-AzKeyVaultSecret -VaultName 'kv69415' -Name 'faceitToken' -AsPlainText
$Env:STORAGE_TABLE_PLAYERS = "playersTest"
```
Run Python Flask server (debug to restart server on each code change):  
`flask --app hello.py run --debug`

## Terraform Setup
```Powershell
$Env:TF_VAR_devops_token = Get-AzKeyVaultSecret -VaultName 'kv69415' -Name 'devops-token' -AsPlainText
terraform apply -auto-approve
```

## SMS Notify App
```Powershell
Connect-AzAccount
$Env:STORAGE_ENDPOINT_QUEUE = Get-AzKeyVaultSecret -VaultName 'kv69415' -Name 'STORAGE-ENDPOINT-QUEUE' -AsPlainText
$Env:AZURE_TENANT_ID        = Get-AzKeyVaultSecret -VaultName 'kv69415' -Name 'sp-sms-notify-tenant-id' -AsPlainText
$Env:AZURE_CLIENT_ID        = Get-AzKeyVaultSecret -VaultName 'kv69415' -Name 'sp-sms-notify-app-id' -AsPlainText
$Env:AZURE_CLIENT_SECRET    = Get-AzKeyVaultSecret -VaultName 'kv69415' -Name 'sp-sms-notify-pw' -AsPlainText
$Env:QUEUE_NAME             = "smsnotificationtest"
```

# Setup
## Manual steps
- Grant Terraform Service Principal permission to grant privileges 
- Push to KeyVailt devops-token | faceitToken
- Grant Storage Table Data Contributor and Storage Queue Data Contributor for Operator/Owner/Developer to develop from local
- Terraform Service Principal needs Application Administrator role to be able to create another service principal for smsNotify App

# Azure Function - grap webhooks from Faceit
Faceit Dev can send webhook data when it's subscribed: https://developers.faceit.com/apps/5f1ce3c7-a4f1-4bba-89e2-7851728477d3/webhooks
We have to put IDs of players to get infromaiton about status.  


## Implementation:  
Azure Function is used as serverless API to receiving Faceit's webhooks
https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python
https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-powershell%2Cpowershell%2Cbrowser