data "azuredevops_project" "p" {
  name = "csgo-faceit-monitor-matches"
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