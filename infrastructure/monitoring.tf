### Monitoring
resource "azurerm_application_insights" "appinsights" {
  name                = "app-insights"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  application_type    = "other"
  retention_in_days   = "30"
}
### Monitoring END