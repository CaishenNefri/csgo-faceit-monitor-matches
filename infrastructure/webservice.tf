resource "azurerm_service_plan" "serviceplan" {
  name                = "service-plan-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  os_type             = "Linux"
  sku_name            = "B1"

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
    STORAGE_TABLE_PLAYERS  = "players"
  }

  key_vault_reference_identity_id = azurerm_user_assigned_identity.function_identity.id

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.function_identity.id]
  }
}

# Add custom domain to web service

resource "azurerm_dns_cname_record" "cname" {
  name                = "faceit"
  zone_name           = data.terraform_remote_state.common.outputs.dns_zone_name
  resource_group_name = data.terraform_remote_state.common.outputs.rg_name
  ttl                 = 3600
  record              = azurerm_linux_web_app.webapp.default_hostname
}

resource "azurerm_dns_txt_record" "txt" {
  name                = "asuid.${azurerm_dns_cname_record.cname.name}"
  zone_name           = data.terraform_remote_state.common.outputs.dns_zone_name
  resource_group_name = data.terraform_remote_state.common.outputs.rg_name
  ttl                 = 3600

  record {
    value = azurerm_linux_web_app.webapp.custom_domain_verification_id
  }
}

resource "azurerm_app_service_custom_hostname_binding" "faceit" {
  hostname            = "${azurerm_dns_cname_record.cname.name}.${data.terraform_remote_state.common.outputs.dns_zone_name}"
  app_service_name    = azurerm_linux_web_app.webapp.name
  resource_group_name = azurerm_resource_group.rg.name

  depends_on = [
    azurerm_dns_cname_record.cname,
    azurerm_dns_txt_record.txt
  ]
}

resource "azurerm_app_service_managed_certificate" "managed" {
  custom_hostname_binding_id = azurerm_app_service_custom_hostname_binding.faceit.id
}

resource "azurerm_app_service_certificate_binding" "binding" {
  hostname_binding_id = azurerm_app_service_custom_hostname_binding.faceit.id
  certificate_id      = azurerm_app_service_managed_certificate.managed.id
  ssl_state           = "SniEnabled"
}