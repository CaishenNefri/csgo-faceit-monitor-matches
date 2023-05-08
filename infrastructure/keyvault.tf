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

resource "azurerm_key_vault_secret" "storage_endpoint_queue" {
  name         = "STORAGE-ENDPOINT-QUEUE"
  value        = azurerm_storage_account.storage.primary_queue_endpoint
  key_vault_id = azurerm_key_vault.kv.id
}