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

#Queue for pushing notification to be send as SMS
resource "azurerm_storage_queue" "smsNotification" {
  name                 = "smsnotification"
  storage_account_name = azurerm_storage_account.storage.name
}