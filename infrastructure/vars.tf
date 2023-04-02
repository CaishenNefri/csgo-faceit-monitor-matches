variable "location" {
  default = "WestEurope"
}

variable "devops_token" {
  sensitive = true
  type      = string
  nullable  = false
}