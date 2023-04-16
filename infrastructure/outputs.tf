output "appserviceName" {
  value       = azurerm_linux_web_app.webapp.name
  description = "Name of the appservice"
}

output "appserviceHostname" {
  value       = azurerm_linux_web_app.webapp.default_hostname
  description = "Hostname of the appservice"
}