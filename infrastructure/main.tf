data "terraform_remote_state" "common" {
  backend = "azurerm"

  config = {
    resource_group_name  = "rg-constant"
    storage_account_name = "constantstorage"
    container_name       = "terraformstatecontainer"
    key                  = "infra-common.prod.terraform.tfstate"
  }
}

# To get current tenand_id
data "azurerm_client_config" "current" {}

resource "random_integer" "ri" {
  min = 10000
  max = 99999
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-csgo-faceit-monitor-matches"
  location = var.location
}