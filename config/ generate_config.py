import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_data_factory_config():
    config = {
        "name": "StockMarketAnalyzerDF",
        "location": "eastus",
        "identity": {
            "type": "SystemAssigned",
            "principalId": os.getenv('AZURE_PRINCIPAL_ID'),
            "tenantId": os.getenv('AZURE_TENANT_ID')
        }
    }
    
    with open('factory/StockMarketAnalyzerDF.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("Data Factory configuration file created successfully.")

def create_linked_service_configs():
    # Azure Data Lake Storage
    adls_config = {
        "name": "AzureDataLakeStorage",
        "properties": {
            "type": "AzureBlobFS",
            "typeProperties": {
                "url": f"https://{os.getenv('AZURE_STORAGE_ACCOUNT_NAME')}.dfs.core.windows.net",
                "accountKey": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "AzureKeyVault",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": "AZURE-STORAGE-ACCOUNT-KEY"
                }
            }
        }
    }
    
    with open('linkedService/AzureDataLakeStorage.json', 'w') as f:
        json.dump(adls_config, f, indent=2)
    print("Azure Data Lake Storage linked service configuration created.")

    # Azure Databricks
    databricks_config = {
        "name": "AzureDatabricks",
        "properties": {
            "type": "AzureDatabricks",
            "typeProperties": {
                "domain": os.getenv('DATABRICKS_WORKSPACE_URL'),
                "accessToken": {
                    "type": "AzureKeyVaultSecret",
                    "store": {
                        "referenceName": "AzureKeyVault",
                        "type": "LinkedServiceReference"
                    },
                    "secretName": "DATABRICKS-ACCESS-TOKEN"
                },
                "existingClusterId": os.getenv('DATABRICKS_CLUSTER_ID')
            }
        }
    }
    
    with open('linkedService/AzureDatabricks.json', 'w') as f:
        json.dump(databricks_config, f, indent=2)
    print("Azure Databricks linked service configuration created.")

    # Alpha Vantage API
    alpha_vantage_config = {
        "name": "AlphaVantageAPI",
        "properties": {
            "type": "RestService",
            "typeProperties": {
                "url": "https://www.alphavantage.co/",
                "enableServerCertificateValidation": true,
                "authenticationType": "Anonymous"
            }
        }
    }
    
    with open('linkedService/AlphaVantageAPI.json', 'w') as f:
        json.dump(alpha_vantage_config, f, indent=2)
    print("Alpha Vantage API linked service configuration created.")

    # Azure Key Vault
    key_vault_config = {
        "name": "AzureKeyVault",
        "properties": {
            "type": "AzureKeyVault",
            "typeProperties": {
                "baseUrl": f"https://{os.getenv('KEY_VAULT_NAME')}.vault.azure.net/"
            }
        }
    }
    
    with open('linkedService/AzureKeyVault.json', 'w') as f:
        json.dump(key_vault_config, f, indent=2)
    print("Azure Key Vault linked service configuration created.")

def main():
    create_data_factory_config()
    create_linked_service_configs()
    print("All configuration files generated successfully.")

if __name__ == "__main__":
    main()