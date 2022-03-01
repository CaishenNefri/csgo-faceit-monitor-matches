terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.97"
    }
  }

  required_version = ">=1.1.0"
}

provider "azurerm" {
  features {}
}

resource "random_integer" "ri" {
  min = 10000
  max = 99999
}


resource "azurerm_resource_group" "rg" {
  name     = "rg-csgo-faceit-monitor-matches"
  location = var.location
}

resource "azurerm_app_service_plan" "appserviceplan" {
  name                = "app-service-plan-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind = "Linux"
  reserved = true
  sku {
    tier = "Free"
    size = "F1"
  }
}

resource "azurerm_app_service" "appservice" {
  name                = "app-service-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  app_service_plan_id = azurerm_app_service_plan.appserviceplan.id
  
  site_config {
    app_command_line = "gunicorn --bind=0.0.0.0 --timeout 600 hello:myapp"
    use_32_bit_worker_process = true
    linux_fx_version = "PYTHON|3.9"
    # python_version = 3.4 # Can not use higher version because of terraform provider ....
  }
#   source_control {
#     repo_url           = "https://github.com/Azure-Samples/nodejs-docs-hello-world"
#     branch             = "master"
#     manual_integration = true
#     use_mercurial      = false
#   }
}