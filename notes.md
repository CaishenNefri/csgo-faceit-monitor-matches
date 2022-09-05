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
  - Python webpage with list of mejz matches

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

# Set env variable
$env:AZDO_PERSONAL_ACCESS_TOKEN="***REMOVED***"
$env:AZDO_ORG_SERVICE_URL="https://dev.azure.com/Caishen"


# Know problems
Azure DevOps Pipeline do not see existing resource right after manually creation. Resolution: try implement terraform into pipeline | do not destry infra
  - https://github.com/microsoft/azure-pipelines-tasks/issues/15532

## Python APP
Run Python Flask server:  
`flask --app hello.py run`