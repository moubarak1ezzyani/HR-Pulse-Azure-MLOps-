terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  # --- CONFIGURATION DU REMOTE BACKEND ---
  # Demande ces infos à ton formateur si tu ne les as pas
  backend "azurerm" {
    resource_group_name  = "RG-HR-PULSE-MGMT-YENNAYA"
    storage_account_name = "<NOM_DU_STORAGE_ACCOUNT_CENTRAL>"
    container_name       = "tfstate"
    key                  = "moubarak.terraform.tfstate" # Ton prénom pour ne pas écraser les autres
  }
}

provider "azurerm" {
  features {}
}

# 1. On pointe vers le serveur SQL du formateur
data "azurerm_mssql_server" "formateur_server" {
  name                = "sql-server-hr-pulse-2026"
  resource_group_name = "RG-HR-PULSE-MGMT-YENNAYA"
}

# 2. Ta base de données (Déjà créée, Terraform ne fera rien de plus)
resource "azurerm_mssql_database" "db_student" {
  name      = "db-moubarak"
  server_id = data.azurerm_mssql_server.formateur_server.id

  # Configuration Serverless
  sku_name     = "GP_S_Gen5_1"
  min_capacity = 0.5
  max_size_gb  = 2

  auto_pause_delay_in_minutes = 15
}

# 3. NOUVEAU : Création du service Azure AI Language (NER)
resource "azurerm_cognitive_account" "ai_language_student" {
  name                = "cog-hr-pulse-moubarak"
  location            = "westeurope" # Doit correspondre à la région du RG
  resource_group_name = "RG-HR-PULSE-MGMT-YENNAYA"
  kind                = "TextAnalytics"
  sku_name            = "F0" # F0 est le Free Tier (Gratuit)
}

# 4. On expose les variables nécessaires pour le script Python (.env)
output "ai_endpoint" {
  value = azurerm_cognitive_account.ai_language_student.endpoint
}

output "ai_key" {
  value     = azurerm_cognitive_account.ai_language_student.primary_access_key
  sensitive = true
}