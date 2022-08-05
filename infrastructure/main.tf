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
    value = azurerm_app_service.appservice.name
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
}

resource "azurerm_app_service" "appservice" {
  name                = "app-service-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_service_plan.serviceplan.id

  site_config {
    app_command_line          = "gunicorn --bind=0.0.0.0 --timeout 600 hello:myapp"
    use_32_bit_worker_process = true
    linux_fx_version          = "PYTHON|3.9"
    # python_version = 3.4 # Can not use higher version because of terraform provider ....
  }
  #   source_control {
  #     repo_url           = "https://github.com/Azure-Samples/nodejs-docs-hello-world"
  #     branch             = "master"
  #     manual_integration = true
  #     use_mercurial      = false
  #   }
}

output "appserviceName" {
  value       = azurerm_app_service.appservice.name
  description = "Name of the appservice"
}

output "appserviceHostname" {
  value       = azurerm_app_service.appservice.default_site_hostname
  description = "Hostname of the appservice"
}