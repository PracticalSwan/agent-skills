---
name: microsoft-development
description: Microsoft technology development hub combining documentation lookup, code reference, and sample retrieval for Azure, .NET, Microsoft 365, Windows, Power Platform, and all Microsoft technologies. Use when working with Azure SDKs, .NET libraries, building Microsoft APIs, looking up API references, or needing official Microsoft documentation samples.
compatibility: Requires Microsoft Learn MCP Server (https://learn.microsoft.com/api/mcp)
license: Complete terms in LICENSE.txt
---



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`


Comprehensive skill for Microsoft technology development including Azure, .NET, Microsoft 365, Windows, and Power Platform.

## When to Use This Skill

- Querying official Microsoft documentation for Azure, .NET, Microsoft 365, or Windows
- Verifying Microsoft API methods, packages, and signatures before implementation
- Finding official code samples for Azure SDKs, Graph, or Power Platform workflows
- Building or troubleshooting applications on Microsoft cloud/platform services
- Validating Microsoft-specific limits, configuration, and best practices

## Part 1: Microsoft Documentation

### When to Use Docs

- **Understanding concepts** — "How does Cosmos DB partitioning work?"
- **Learning a service** — "Azure Functions overview", "Container Apps architecture"
- **Finding tutorials** — "quickstart", "getting started", "step-by-step"
- **Configuration options** — "App Service configuration settings"
- **Limits & quotas** — "Azure OpenAI rate limits", "Service Bus quotas"
- **Best practices** — "Azure security best practices"

### Tools

| Tool | Use For |
|------|---------|
| `microsoft_docs_search` | Find documentation—concepts, guides, tutorials, configuration |
| `microsoft_docs_fetch` | Get full page content (when search excerpts aren't enough) |

### Query Effective Tips

Good queries are specific:

```


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

"Azure Functions"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

"Azure Functions Python v2 programming model"
"Cosmos DB partition key design best practices"
"Container Apps scaling rules KEDA"
```

### Include Context in Queries

- **Version** when relevant (`@.NET 8`, `@EF Core 8`)
- **Task intent** (`quickstart`, `tutorial`, `overview`, `limits`)
- **Platform** for multi-platform docs (`Linux`, `Windows`)

### When to Fetch Full Page

Fetch after search when:
- **Tutorials** — need complete step-by-step instructions
- **Configuration guides** — need all options listed
- **Deep dives** — user wants comprehensive coverage
- **API references** — need complete method signatures and overloads

### Query Examples

```python


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

microsoft_docs_search("Azure Static Web Apps deployment patterns")
microsoft_docs_search(".NET Core dependency injection best practices")
microsoft_docs_search("Power BI row-level security implementation")



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

microsoft_docs_search("App Service app settings reference")
microsoft_docs_search("Functions host.json configuration options")



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

microsoft_docs_search("Azure OpenAI rate limits pricing tiers")
microsoft_docs_search("Azure Storage account limits and quotas")
```

---

## Part 2: Microsoft Code Reference

### Tools

| Need | Tool | Example |
|------|------|---------|
| API method/class lookup | `microsoft_docs_search` | `"BlobClient UploadAsync Azure.Storage.Blobs"` |
| Working code sample | `microsoft_code_sample_search` | `query: "upload blob managed identity", language: "python"` |
| Full API reference | `microsoft_docs_fetch` | Fetch URL from search (for overloads, full signatures) |

### Finding Code Samples

Use `microsoft_code_sample_search` to get official, working examples:

```python
microsoft_code_sample_search(query="upload file to blob storage", language="csharp")
microsoft_code_sample_search(query="authenticate with managed identity", language="python")
microsoft_code_sample_search(query="send message service bus", language="javascript")
microsoft_code_sample_search(query="Power BI embed report", language="csharp")
```

**When to use code samples:**
- **Before writing code** — find a working pattern to follow
- **After errors** — compare your code against a known-good sample
- **Unsure of initialization/setup** — samples show complete context
- **New API usage** — see recommended patterns from Microsoft

### API Lookups

Use `microsoft_docs_search` to verify methods exist and find correct usage:



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

"BlobClient UploadAsync Azure.Storage.Blobs"
"GraphServiceClient Users Microsoft.Graph"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

"DefaultAzureCredential class Azure.Identity"
"IOptions<T> interface Microsoft.Extensions"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

"Azure Blob Storage NuGet package"
"azure-storage-blob pip package"
"Microsoft.Graph SDK npm"


### Error Troubleshooting Workflow

When encountering errors with Microsoft APIs:

1. **Search the error**: `"Service Bus timeout error Azure"`
2. **Find code samples** with similar scenarios
3. **Verify method signatures**: Check parameter types and order
4. **Review best practices**: Official docs often show anti-patterns



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

microsoft_docs_search("request body too large Service Bus")



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

microsoft_code_sample_search(query="configure Service Bus message size limit", language="python")



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

microsoft_docs_search("ServiceBusClient configuration options")


---

## Part 3: Azure Development Workflows

### Azure Storage (Blobs)

#### Common Tasks

**Upload file to blob storage:**
```csharp
// Using Azure.Storage.Blobs
var blobServiceClient = new BlobServiceClient(connectionString);
var blobContainerClient = blobServiceClient.GetBlobContainerClient("mycontainer");
var blobClient = blobContainerClient.GetBlobClient("myfile.txt");

await blobClient.UploadAsync(filePath);
```

```python
// Using azure-storage-blob
from azure.storage.blob import BlobServiceClient

blob_service_client = BlobServiceClient.from_connection_string(connection_string)
blob_client = blob_service_client.get_blob_client(container="mycontainer", blob="myfile.txt")

with open("myfile.txt", "rb") as data:
    blob_client.upload_blob(data)
```

**Download file:**
```javascript
const { BlobServiceClient } = require("@azure/storage-blob");

const blobServiceClient = BlobServiceClient.fromConnectionString(connectionString);
const containerClient = blobServiceClient.getContainerClient("mycontainer");
const blobClient = containerClient.getBlobClient("myfile.txt");

await blobClient.downloadToFile("downloaded.txt");
```

**List blobs with filtering:**
```csharp
await foreach (var blob in blobContainerClient.GetBlobsAsync())
{
    if (blob.Name.EndsWith(".txt"))
    {
        Console.WriteLine($"{blob.Name} (Size: {blob.Properties.ContentLength})");
    }
}
```

### Azure Functions

#### HTTP Trigger Function

```csharp
// .NET 8 Isolated Worker
using Microsoft.Azure.Functions.Worker;

[Function("HttpExample")]
public HttpResponseData Run(
    [HttpTrigger(AuthorizationLevel.Function, "get", "post")] HttpRequestData req,
    FunctionContext executionContext)
{
    var logger = executionContext.GetLogger("HttpExample");
    logger.LogInformation("C# HTTP trigger function processed a request.");

    var response = new HttpResponseData(HttpStatusCode.OK);
    response.Headers.Add("Content-Type", "text/plain; charset=utf-8");
    response.Body = $"Welcome to Azure Functions, {req.Query["name"]}!";

    return response;
}
```

```javascript
// Node.js v4 model
const { app } = require('@azure/functions');

app.http('httpExample', {
    route: 'hello/{name:alpha}',
    methods: ['GET'],
    authLevel: 'function',
    handler: async (request, context) => {
        const name = request.params.name || 'world';
        return { body: `Hello, ${name}!` };
    }
});
```

### Cosmos DB

#### Basic Document Operations


from azure.cosmos import CosmosClient
import azure.cosmos.cosmos_client as cosmos_client



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

client = CosmosClient(url, credential)
database = client.get_database_client("mydatabase")
container = database.get_container_client("mycontainer")



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

item = {
    "id": "1",
    "name": "John Doe",
    "age": 30
}
container.create_item(item)



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

for item in container.query_items(
    query="SELECT * FROM c WHERE c.age > @age",
    parameters=[{"name": "@age", "value": 25}]
):
    print(item)


### Azure App Service / Static Web Apps

#### Configuration

```yaml


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

config:
  appLocation: "/"
  outputLocation: "dist"
  apiLocation: "api"

platform:
  apiRuntime: "node:18"

production:
  branch: "main"
  pullRequestPreviewSettings:
    branch: "main"
```

#### GitHub Actions

```yaml


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

name: Deploy to Azure

on:
  push:
    branches: [ main ]

env:
  AZURE_WEBAPP_NAME: "myapp"
  AZURE_WEBAPP_PACKAGE_PATH: "./dist"

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "18"

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy to Azure Static Web Apps
        uses: azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "src"
          api_location: "api"
          output_location: "dist"
```

---

## Part 4: .NET Development

### Common Patterns

#### Dependency Injection

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);

// Register services
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(connectionString));

builder.Services.AddScoped<IRepository, EFRepository>();
builder.Services.AddHttpClient();

var app = builder.Build();

// Inject in controllers
app.MapControllers();

app.Run();
```

#### Async/Await Best Practices

```csharp
// ✅ Correct - ConfigureAwait(true)
public async Task<IEnumerable<User>> GetUsersAsync()
{
    var users = await _repository.GetAllAsync().ConfigureAwait(false);
    return users;
}

// ✅ Correct - Use async all the way
public async Task<User> CreateUserAsync(User user)
{
    _dbContext.Users.Add(user);
    await _dbContext.SaveChangesAsync().ConfigureAwait(false);
    return user;
}
```

#### Logging

```csharp
// Constructor injection
public class ProductService
{
    private readonly ILogger<ProductService> _logger;

    public ProductService(ILogger<ProductService> logger)
    {
        _logger = logger;
    }

    public void ProcessProducts()
    {
        _logger.LogInformation("Starting product processing");
        // ... code
        _logger.LogWarning("Product count exceeds threshold: {Count}", count);
    }
}
```

---

## Part 5: Microsoft Graph

#### Microsoft Graph Authentication

```csharp
// Using Azure.Identity and Microsoft.Graph
using Azure.Identity;
using Microsoft.Graph;

var credential = new ClientSecretCredential(
    tenantId,
    clientId,
    clientSecret);

var graphClient = new GraphServiceClient(credential, new[] { "https://graph.microsoft.com/.default" });
```

```javascript
// Using @azure/identity and @microsoft/microsoft-graph-client
const { ClientSecretCredential } = require("@azure/identity");
const { Client } = require("@microsoft/microsoft-graph-client");

const credential = new ClientSecretCredential(tenantId, clientId, clientSecret);
const client = Client.initWithMiddleware({
    authenticationProvider: credential,
});
```

#### Common Operations

**Get user:**
```csharp
var user = await graphClient.Users["user@example.com"].GetAsync();
Console.WriteLine($"User: {user.DisplayName} ({user.Mail})");
```

**Send email:**
```csharp
var message = new Message
{
    Subject = "Meeting Tomorrow",
    Body = new ItemBody
    {
        ContentType = BodyType.Text,
        Content = "Don't forget about our meeting at 2 PM."
    },
    ToRecipients = new[] { new Recipient { EmailAddress = new EmailAddress { Address = "recipient@example.com" } } }
};

await graphClient.Me.SendMailAsync(message);
```

---

## Part 6: Development Best Practices

### Azure Best Practices

- **Use Managed Identities** instead of hardcoded credentials
- **Configure diagnostics and logging** from the start
- **Follow resource naming conventions** for organization
- **Use resource tags** for cost tracking and organization
- **Set up RBAC** with principle of least privilege
- **Implement retry policies** for transient failures
- **Monitor application health** with Application Insights

### .NET Best Practices

- **Use async/await properly** - ConfigureAwait for non-UI code
- **Validate inputs early** - fail fast with meaningful errors
- **Use dependency injection** - don't create service instances manually
- **Implement proper logging** - structured logging with correlation IDs
- **Follow SOLID principles** - design for testability
- **Use configuration patterns** - IOptions<T> for configuration
- **Implement proper exception handling** - don't catch base Exception

### Microsoft Graph Best Practices

- **Use batch requests** - combine multiple operations
- **Select specific properties** - avoid $select=* when possible
- **Use delta queries** - for syncing changes
- **Implement proper error handling** - handle throttling (429 responses)
- **Cache frequently accessed data** - reduce API calls

---

## Part 7: Troubleshooting Guide

### Common Error Patterns

#### Authentication Errors
```
Error: "The remote server returned an error: (401) Unauthorized"

Solutions:
1. Verify credentials are correct
2. Check token hasn't expired
3. Verify right permissions/scopes are granted
4. For Azure: check Managed Identity is properly configured
```

#### Configuration Errors
```
Error: "Configuration value not found" or "Invalid connection string"

Solutions:
1. Verify key names in appsettings.json / environment variables
2. Check connection string format (semicolon-separated key=value pairs)
3. For Azure: Use GetConnectionString() or proper secret reference
```

#### API Limiting
```
Error: "Request rate limit exceeded" or HTTP 429

Solutions:
1. Implement retry with exponential backoff
2. Use batching for multiple operations
3. Increase service tier if needed
4. Implement caching to reduce unnecessary calls
```

### Debugging Steps

1. **Enable verbose logging** - increase log level to DEBUG
2. **Use Application Insights** - monitor live metrics and dependencies
3. **Check official documentation** - search error message or scenario
4. **Review code samples** - compare working example to your code
5. **Verify configuration** - all connection strings, credentials, URLs correct

---

## Quick Reference: Microsoft Development

### Azure Services Common Packages

| Service | NuGet Package | pip Package | npm Package |
|---------|--------------|------------|-----------|
| Blob Storage | Azure.Storage.Blobs | azure-storage-blob | @azure/storage-blob |
| Cosmos DB | Microsoft.Azure.Cosmos | azure-cosmos | @azure/cosmos |
| Functions | Microsoft.Azure.Functions.Worker | azure-functions | @azure/functions |
| App Service | none (built-in) | none (built-in) | none (built-in) |
| Key Vault | Azure.Security.KeyVault.Secrets | azure-keyvault-secrets | @azure/keyvault-secrets |

### .NET Common Namespaces

```csharp
// Core
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Configuration;

// Azure
using Azure.Identity;
using Azure.Storage.Blobs;
using Microsoft.Azure.Cosmos;

// General
using System.Net;
using System.Text.Json;
```

### Common Search Queries


## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

"Azure Storage best practices"
"Azure Functions performance optimization"
"Cosmos DB partitioning design"
"Azure App Service deployment"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

".NET Core dependency injection patterns"
"Entity Framework Core async best practices"
".NET 8 performance improvements"
"C# async await ConfigureAwait"



## Skill Paths

- Workspace skills: `.github/skills/`
- Global skills: `C:/Users/LOQ/.agents/skills/`

"Microsoft Graph API authentication"
"Microsoft Graph batch requests"
"Graph Explorer usage"


## References & Resources

### Documentation
- [Azure Services Quick Reference](./references/azure-services-quickref.md) — 25 Azure services with CLI, SDK packages, and use cases
- [.NET Patterns](./references/dotnet-patterns.md) — 9 .NET design patterns with C# examples

### Scripts
- [Azure Health Check](./scripts/azure-health-check.ps1) — PowerShell script to check Azure resource health and status

### Examples
- [Azure Function API Example](./examples/azure-function-api-example.md) — Azure Functions v4 isolated API with Cosmos DB and GitHub Actions
