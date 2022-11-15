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
  - Add keyvault to pipeline
  - Run Terraform from yaml pipeline
    - do plan
    - do apply using generated plan
    - authenticate: https://julie.io/writing/terraform-on-azure-pipelines-best-practices/#:~:text=difficult%20to%20understand.-,Why%20does%20az%20login%20not%20work%20in%20CI/CD%3F,-In%20short%2C%20it
    - https://julie.io/writing/terraform-on-azure-pipelines-best-practices/ 
  - Intergrate keyvault
    - Azure DevOps personal access token
    - service principal for terraform
  - 
  - Done: Python webpage with list of mejz matches
    - Done: Load test json not from API
    - Done: create function to call API
    - Done: List match (team, score) for one player
    - Done: List last 10 matches
    - Done: Add time when match finished: https://realpython.com/python-datetime/
  - Create Python Function to catch webhook
    - Done: Create terraform Infra with Azure Function
    - Done: Prepare helloworld code to grap data from Postman
      - https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-configuration
      - https://learn.microsoft.com/en-us/azure/azure-functions/scripts/functions-cli-create-serverless-python
      - https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python?pivots=python-mode-decorators
    - Done: Deploy App to Azure Function
    - Save grabbed code to Storage Account Table
    - Tweak code: collect Faceit raw request from postman
    - Tweak deploying to use artifacts
  - Add some kind of monitoring or diagnostic settings
  - Move Python code to container
  - Add step to terraform infa: produce artifact with terraform plan out
    - create terraform plan artifact
    - use artifact in apply
    - create approve step for prod
  - Divide Install requriments job from deploying job by doing stages


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
caishen : '5ba2c07d-072c-4db9-a08d-be94f905899c'

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
Run Python Flask server:  
`flask --app hello.py run`+

# Azure Function - grap webhooks from Faceit
Faceit Dev can send webhook data when it's subscribed: https://developers.faceit.com/apps/5f1ce3c7-a4f1-4bba-89e2-7851728477d3/webhooks
We have to put IDs of players to get infromaiton about status.  

## Implementation:  
Azure Function is used as serverless API to receiving Faceit's webhooks
https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-python
https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=azure-powershell%2Cpowershell%2Cbrowser