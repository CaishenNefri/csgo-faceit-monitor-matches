terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.17.0"
    }
    azuredevops = {
      source  = "microsoft/azuredevops"
      version = "~>0.2.2"
    }
  }

  backend "azurerm" {
    resource_group_name  = "rg-constant"
    storage_account_name = "constantstorage"
    container_name       = "terraformstatecontainer"
    key                  = "prod.terraform.tfstate"
  }

  required_version = ">=1.1.0"
}

provider "azurerm" {
  features {}
}

provider "azuredevops" {
  org_service_url       = "https://dev.azure.com/Caishen"
  personal_access_token = "***REMOVED***"
}

data "azuredevops_project" "p" {
  name = "csgo-faceit-monitor-matches"
}

resource "random_integer" "ri" {
  min = 10000
  max = 99999
}

resource "azuredevops_variable_group" "vg" {
  project_id   = data.azuredevops_project.p.id
  name         = "Variable Group"
  description  = "Variable Group Description"
  allow_access = true

  variable {
    name  = "webAppName"
    value = azurerm_linux_web_app.webapp.name
  }
}


resource "azurerm_resource_group" "rg" {
  name     = "rg-csgo-faceit-monitor-matches"
  location = var.location
}

resource "azurerm_service_plan" "serviceplan" {
  name                = "service-plan-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "F1"

  depends_on = [
    azurerm_service_plan.functionplan
    /* The reason why Service Plan depends on Function Service Plan:
      https://www.garyjackson.dev/posts/azure-function-app-conflicting-plans/
      Shortcut: can not be created before due some internal Azure Error
    */
  ]
}

resource "azurerm_linux_web_app" "webapp" {
  name                = "webapp-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  service_plan_id     = azurerm_service_plan.serviceplan.id

  site_config {
    always_on        = false
    app_command_line = "gunicorn --bind=0.0.0.0 --timeout 600 hello:myapp"
    application_stack {
      python_version = "3.8"
    }
  }
}

### START Function APP
resource "azurerm_storage_account" "storage" {
  name                     = "storage${random_integer.ri.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "functionplan" {
  name                = "service-plan-app-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_linux_function_app" "functionapp" {
  name                = "function-app-${random_integer.ri.result}"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.secondary_access_key
  service_plan_id            = azurerm_service_plan.functionplan.id

  site_config {}
}
### END Function APP


output "appserviceName" {
  value       = azurerm_linux_web_app.webapp.name
  description = "Name of the appservice"
}

output "appserviceHostname" {
  value       = azurerm_linux_web_app.webapp.default_hostname
  description = "Hostname of the appservice"
}