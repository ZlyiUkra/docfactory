# Azure Functions Example
# джерело: https://github.com/upstash/redis-js/blob/v1.36.4/examples/azure-functions/README.md
# отримано: 2026-10-16
# версія: redis-1.36.4, redis-1.36.3, redis-1.36.2, redis-1.36.1, redis-1.36.0, redis-1.35.8, redis-1.35.7, redis-1.35.6, redis-1.35.5, redis-1.35.4, redis-1.35.3, redis-1.35.2, redis-1.35.1, redis-1.35.0, redis-1.34.9, redis-1.34.8, redis-1.34.7, redis-1.34.6, redis-1.34.5, redis-1.34.4, redis-1.34.3, redis-1.34.2, redis-1.34.1

### Prerequisites

1. Create an Azure account.
2. Set up Azure CLI
3. Install the Azure Functions Core Tools

### Project Setup

Clone the example and install dependencies

```shell
git clone https://github.com/upstash/redis-js.git
cd redis-js/examples/azure-functions
npm install
```

### Create Azure Resources

You can use the command below to find the `name` of a region near you.

```shell
az account list-locations
```

Create a resource group.

```shell
az group create --name AzureFunctionsQuickstart-rg --location <REGION>
```

Create a storage account.

```shell
az storage account create --name <STORAGE_NAME> --location <REGION> --resource-group AzureFunctionsQuickstart-rg --sku Standard_LRS --allow-blob-public-access false
```

Create your Function App.

```shell
az functionapp create --resource-group AzureFunctionsQuickstart-rg --consumption-plan-location <REGION> --runtime node --runtime-version 18 --functions-version 4 --name <APP_NAME> --storage-account <STORAGE_NAME>
```

### Database Setup

Create a Redis database using Upstash Console or Upstash CLI and set `UPSTASH_REDIS_REST_URL` and `UPSTASH_REDIS_REST_TOKEN` in your Function App's settings.

```shell
az functionapp config appsettings set --name <APP_NAME> --resource-group AzureFunctionsQuickstart-rg --settings UPSTASH_REDIS_REST_URL=<YOUR_URL> UPSTASH_REDIS_REST_TOKEN=<YOUR_TOKEN>
```

### Deploy

Take a build of your application.

```shell
npm run build
```

Publish your application.

```shell
func azure functionapp publish <APP_NAME>
```

Visit the given Invoke URL.
