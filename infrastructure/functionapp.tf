
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
    STORAGE_TABLE_PLAYERS           = "players"
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