data "azuread_client_config" "current" {}

resource "azuread_application" "sp_sms_app" {
  display_name = "sms_notify"
  owners       = [data.azuread_client_config.current.object_id]
}

resource "azuread_service_principal" "sp_sms_app" {
  application_id               = azuread_application.sp_sms_app.application_id
  app_role_assignment_required = false
  owners                       = [data.azuread_client_config.current.object_id]
}

resource "azuread_service_principal_password" "sp_sms_app" {
  service_principal_id = azuread_service_principal.sp_sms_app.object_id
}

# SMS Notify application Service Principal save to Key Vault
resource "azurerm_key_vault_secret" "sp-sms-notify-object-id" {
  name         = "sp-sms-notify-object-id"
  value        = azuread_application.sp_sms_app.object_id
  key_vault_id = azurerm_key_vault.kv.id
}

resource "azurerm_key_vault_secret" "sp-sms-notify-pw" {
  name         = "sp-sms-notify-pw"
  value        = azuread_service_principal_password.sp_sms_app.value
  key_vault_id = azurerm_key_vault.kv.id
}