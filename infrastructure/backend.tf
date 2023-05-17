terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.50.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = ">=2.38.0"
    }
    azuredevops = {
      source  = "microsoft/azuredevops"
      version = "~>0.4.0"
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
