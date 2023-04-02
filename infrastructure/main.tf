terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.50.0"
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

provider "azurerm" {
  features {}
}

provider "azuredevops" {
  org_service_url       = "https://dev.azure.com/Caishen"
  personal_access_token = var.devops_token
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

  variable {
    name  = "funAppName"
    value = azurerm_linux_function_app.functionapp.name
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

  app_settings = {
    AZURE_CLIENT_ID        = azurerm_user_assigned_identity.function_identity.client_id
    STORAGE_ENDPOINT_TABLE = azurerm_storage_account.storage.primary_table_endpoint
    FACEIT_TOKEN           = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault.kv.vault_uri}secrets/faceitToken/)"
    STORAGE_TABLE_PLAYERS  = "players" #Place where to saved elo
  }

  key_vault_reference_identity_id = azurerm_user_assigned_identity.function_identity.id

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.function_identity.id]
  }
}

### START Function APP
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

  key_vault_reference_identity_id = azurerm_user_assigned_identity.function_identity.id

  site_config {
    application_stack {
      python_version = "3.9"
    }
    application_insights_key = azurerm_application_insights.appinsights.instrumentation_key
  }

  app_settings = {
    AZURE_CLIENT_ID                 = azurerm_user_assigned_identity.function_identity.client_id
    STORAGE_ENDPOINT_TABLE          = azurerm_storage_account.storage.primary_table_endpoint
    WEBSITE_ENABLE_SYNC_UPDATE_SITE = false
    FACEIT_TOKEN                    = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault.kv.vault_uri}secrets/faceitToken/)"
    STORAGE_TABLE_PLAYERS           = "players" #Place where to saved elo
  }

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.function_identity.id]
  }

  lifecycle {
    ignore_changes = [tags]
  }
}

resource "azurerm_user_assigned_identity" "function_identity" {
  name                = "identity-function-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
}

# Grant Storage Table Data Contributor permission for user assigned idenitty of Function to storage account
resource "azurerm_role_assignment" "function_identity" {
  scope                = azurerm_storage_account.storage.id
  role_definition_name = "Storage Table Data Contributor"
  principal_id         = azurerm_user_assigned_identity.function_identity.principal_id
}
### END Function APP

### Monitoring
resource "azurerm_application_insights" "appinsights" {
  name                = "app-insights"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  application_type    = "other"
  retention_in_days   = "30"
}
### Monitoring END

### Create Storage Account with table "players"
# table "players" contains match_finished info
resource "azurerm_storage_account" "storage" {
  name                     = "storage${random_integer.ri.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_management_lock" "storage" {
  name       = "storage-lock"
  scope      = azurerm_storage_account.storage.id
  lock_level = "CanNotDelete"
  notes      = "Locked because it contains every ELO changefor player"
}

resource "azurerm_storage_table" "players" {
  name                 = "players"
  storage_account_name = azurerm_storage_account.storage.name

  lifecycle {
    prevent_destroy = true
  }
}

# To get current tenand_id
data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "kv" {
  name                        = "kv${random_integer.ri.result}"
  location                    = azurerm_resource_group.rg.location
  resource_group_name         = azurerm_resource_group.rg.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  purge_protection_enabled    = false

  sku_name = "standard"
}

resource "azurerm_key_vault_access_policy" "tf-runner" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = "1fa3933e-555b-4c1d-b5cb-7a1035e833d3" #Service Principal object id

  certificate_permissions = ["Backup", "Create", "Delete", "DeleteIssuers", "Get", "GetIssuers", "Import", "List", "ListIssuers", "ManageContacts", "ManageIssuers", "Purge", "Recover", "Restore", "SetIssuers", "Update"]
  key_permissions         = ["Backup", "Create", "Decrypt", "Delete", "Encrypt", "Get", "Import", "List", "Purge", "Recover", "Restore", "Sign", "UnwrapKey", "Update", "Verify", "WrapKey", "Release", "Rotate", "GetRotationPolicy", "SetRotationPolicy"]
  secret_permissions      = ["Backup", "Delete", "Get", "List", "Purge", "Recover", "Restore", "Set"]
  storage_permissions     = ["Backup", "Delete", "DeleteSAS", "Get", "GetSAS", "List", "ListSAS", "Purge", "Recover", "RegenerateKey", "Restore", "Set", "SetSAS", "Update"]
}

resource "azurerm_key_vault_access_policy" "uai" {
  key_vault_id = azurerm_key_vault.kv.id
  tenant_id    = azurerm_user_assigned_identity.function_identity.tenant_id
  object_id    = azurerm_user_assigned_identity.function_identity.principal_id

  secret_permissions = [
    "Get",
  ]
}

resource "azurerm_key_vault_secret" "storage_endpoint_table" {
  name         = "STORAGE-ENDPOINT-TABLE"
  value        = azurerm_storage_account.storage.primary_table_endpoint
  key_vault_id = azurerm_key_vault.kv.id
}


output "appserviceName" {
  value       = azurerm_linux_web_app.webapp.name
  description = "Name of the appservice"
}

output "appserviceHostname" {
  value       = azurerm_linux_web_app.webapp.default_hostname
  description = "Hostname of the appservice"
}