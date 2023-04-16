provider "azurerm" {
  features {}
}

provider "azuredevops" {
  org_service_url       = "https://dev.azure.com/Caishen"
  personal_access_token = var.devops_token
}
