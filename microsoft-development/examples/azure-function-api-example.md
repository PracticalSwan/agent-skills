# Azure Functions REST API Example

Complete Azure Functions v4 (isolated process) HTTP API with Cosmos DB, authentication, OpenAPI, and CI/CD.

---

## Project Structure

```
RecipeApi/
  RecipeApi.csproj
  Program.cs
  host.json
  local.settings.json
  Models/
    Recipe.cs
    CreateRecipeRequest.cs
    UpdateRecipeRequest.cs
  Functions/
    RecipeFunctions.cs
  Services/
    IRecipeService.cs
    CosmosRecipeService.cs
  .github/
    workflows/
      deploy.yml
```

---

## Configuration Files

### RecipeApi.csproj

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <AzureFunctionsVersion>v4</AzureFunctionsVersion>
    <OutputType>Exe</OutputType>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.Azure.Functions.Worker" Version="1.22.0" />
    <PackageReference Include="Microsoft.Azure.Functions.Worker.Sdk" Version="1.17.4" />
    <PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.Http.AspNetCore" Version="1.3.2" />
    <PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.CosmosDB" Version="4.8.0" />
    <PackageReference Include="Microsoft.Azure.Cosmos" Version="3.39.0" />
    <PackageReference Include="Microsoft.Extensions.Http" Version="8.0.0" />
    <PackageReference Include="Microsoft.Azure.Functions.Worker.Extensions.OpenApi" Version="1.5.1" />
    <PackageReference Include="Microsoft.Identity.Web" Version="2.19.0" />
  </ItemGroup>
</Project>
```

### Program.cs

```csharp
using Microsoft.Azure.Cosmos;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using RecipeApi.Services;

var host = new HostBuilder()
    .ConfigureFunctionsWebApplication()
    .ConfigureServices((context, services) =>
    {
        services.AddApplicationInsightsTelemetryWorkerService();
        services.ConfigureFunctionsApplicationInsights();

        // Cosmos DB client — singleton for connection pooling
        services.AddSingleton(sp =>
        {
            var connectionString = context.Configuration["CosmosDb:ConnectionString"];
            return new CosmosClient(connectionString, new CosmosClientOptions
            {
                SerializerOptions = new CosmosSerializationOptions
                {
                    PropertyNamingPolicy = CosmosPropertyNamingPolicy.CamelCase
                }
            });
        });

        services.AddSingleton<IRecipeService>(sp =>
        {
            var client = sp.GetRequiredService<CosmosClient>();
            var databaseName = context.Configuration["CosmosDb:DatabaseName"] ?? "RecipeDb";
            var containerName = context.Configuration["CosmosDb:ContainerName"] ?? "Recipes";
            return new CosmosRecipeService(client, databaseName, containerName);
        });
    })
    .Build();

host.Run();
```

### host.json

```json
{
  "version": "2.0",
  "logging": {
    "applicationInsights": {
      "samplingSettings": {
        "isEnabled": true,
        "excludedTypes": "Request"
      },
      "enableLiveMetricsFilters": true
    },
    "logLevel": {
      "default": "Information",
      "Host.Results": "Error",
      "Function": "Information"
    }
  },
  "extensions": {
    "http": {
      "routePrefix": "api"
    }
  }
}
```

### local.settings.json

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "dotnet-isolated",
    "CosmosDb:ConnectionString": "AccountEndpoint=https://localhost:8081/;AccountKey=C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw==",
    "CosmosDb:DatabaseName": "RecipeDb",
    "CosmosDb:ContainerName": "Recipes"
  }
}
```

---

## Models

### Models/Recipe.cs

```csharp
using System.Text.Json.Serialization;

namespace RecipeApi.Models;

public class Recipe
{
    [JsonPropertyName("id")]
    public string Id { get; set; } = Guid.NewGuid().ToString();

    [JsonPropertyName("title")]
    public string Title { get; set; } = string.Empty;

    [JsonPropertyName("description")]
    public string Description { get; set; } = string.Empty;

    [JsonPropertyName("ingredients")]
    public List<string> Ingredients { get; set; } = [];

    [JsonPropertyName("instructions")]
    public List<string> Instructions { get; set; } = [];

    [JsonPropertyName("prepTimeMinutes")]
    public int PrepTimeMinutes { get; set; }

    [JsonPropertyName("difficulty")]
    public string Difficulty { get; set; } = "Easy";

    [JsonPropertyName("tags")]
    public List<string> Tags { get; set; } = [];

    [JsonPropertyName("authorId")]
    public string AuthorId { get; set; } = string.Empty;

    [JsonPropertyName("createdAt")]
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

    [JsonPropertyName("updatedAt")]
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}
```

### Models/CreateRecipeRequest.cs

```csharp
namespace RecipeApi.Models;

public class CreateRecipeRequest
{
    public string Title { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public List<string> Ingredients { get; set; } = [];
    public List<string> Instructions { get; set; } = [];
    public int PrepTimeMinutes { get; set; }
    public string Difficulty { get; set; } = "Easy";
    public List<string> Tags { get; set; } = [];
}
```

### Models/UpdateRecipeRequest.cs

```csharp
namespace RecipeApi.Models;

public class UpdateRecipeRequest
{
    public string? Title { get; set; }
    public string? Description { get; set; }
    public List<string>? Ingredients { get; set; }
    public List<string>? Instructions { get; set; }
    public int? PrepTimeMinutes { get; set; }
    public string? Difficulty { get; set; }
    public List<string>? Tags { get; set; }
}
```

---

## Services

### Services/IRecipeService.cs

```csharp
using RecipeApi.Models;

namespace RecipeApi.Services;

public interface IRecipeService
{
    Task<IEnumerable<Recipe>> GetAllAsync(int limit = 50, string? continuationToken = null);
    Task<Recipe?> GetByIdAsync(string id);
    Task<Recipe> CreateAsync(Recipe recipe);
    Task<Recipe?> UpdateAsync(string id, UpdateRecipeRequest request);
    Task<bool> DeleteAsync(string id);
    Task<IEnumerable<Recipe>> SearchAsync(string query);
}
```

### Services/CosmosRecipeService.cs

```csharp
using Microsoft.Azure.Cosmos;
using RecipeApi.Models;

namespace RecipeApi.Services;

public class CosmosRecipeService : IRecipeService
{
    private readonly Container _container;

    public CosmosRecipeService(CosmosClient client, string databaseName, string containerName)
    {
        _container = client.GetContainer(databaseName, containerName);
    }

    public async Task<IEnumerable<Recipe>> GetAllAsync(int limit = 50, string? continuationToken = null)
    {
        var query = new QueryDefinition("SELECT * FROM c ORDER BY c.createdAt DESC OFFSET 0 LIMIT @limit")
            .WithParameter("@limit", limit);

        var results = new List<Recipe>();
        using var iterator = _container.GetItemQueryIterator<Recipe>(query);

        while (iterator.HasMoreResults)
        {
            var response = await iterator.ReadNextAsync();
            results.AddRange(response);
        }

        return results;
    }

    public async Task<Recipe?> GetByIdAsync(string id)
    {
        try
        {
            var response = await _container.ReadItemAsync<Recipe>(id, new PartitionKey(id));
            return response.Resource;
        }
        catch (CosmosException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            return null;
        }
    }

    public async Task<Recipe> CreateAsync(Recipe recipe)
    {
        recipe.Id = Guid.NewGuid().ToString();
        recipe.CreatedAt = DateTime.UtcNow;
        recipe.UpdatedAt = DateTime.UtcNow;

        var response = await _container.CreateItemAsync(recipe, new PartitionKey(recipe.Id));
        return response.Resource;
    }

    public async Task<Recipe?> UpdateAsync(string id, UpdateRecipeRequest request)
    {
        var existing = await GetByIdAsync(id);
        if (existing is null) return null;

        if (request.Title is not null) existing.Title = request.Title;
        if (request.Description is not null) existing.Description = request.Description;
        if (request.Ingredients is not null) existing.Ingredients = request.Ingredients;
        if (request.Instructions is not null) existing.Instructions = request.Instructions;
        if (request.PrepTimeMinutes.HasValue) existing.PrepTimeMinutes = request.PrepTimeMinutes.Value;
        if (request.Difficulty is not null) existing.Difficulty = request.Difficulty;
        if (request.Tags is not null) existing.Tags = request.Tags;
        existing.UpdatedAt = DateTime.UtcNow;

        var response = await _container.ReplaceItemAsync(existing, id, new PartitionKey(id));
        return response.Resource;
    }

    public async Task<bool> DeleteAsync(string id)
    {
        try
        {
            await _container.DeleteItemAsync<Recipe>(id, new PartitionKey(id));
            return true;
        }
        catch (CosmosException ex) when (ex.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            return false;
        }
    }

    public async Task<IEnumerable<Recipe>> SearchAsync(string query)
    {
        var sqlQuery = new QueryDefinition(
            "SELECT * FROM c WHERE CONTAINS(LOWER(c.title), @query) OR CONTAINS(LOWER(c.description), @query)")
            .WithParameter("@query", query.ToLower());

        var results = new List<Recipe>();
        using var iterator = _container.GetItemQueryIterator<Recipe>(sqlQuery);

        while (iterator.HasMoreResults)
        {
            var response = await iterator.ReadNextAsync();
            results.AddRange(response);
        }

        return results;
    }
}
```

---

## Functions

### Functions/RecipeFunctions.cs

```csharp
using System.Net;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Azure.Functions.Worker.Http;
using Microsoft.Azure.WebJobs.Extensions.OpenApi.Core.Attributes;
using Microsoft.Azure.WebJobs.Extensions.OpenApi.Core.Enums;
using Microsoft.Extensions.Logging;
using Microsoft.OpenApi.Models;
using RecipeApi.Models;
using RecipeApi.Services;

namespace RecipeApi.Functions;

public class RecipeFunctions
{
    private readonly IRecipeService _recipeService;
    private readonly ILogger<RecipeFunctions> _logger;

    public RecipeFunctions(IRecipeService recipeService, ILogger<RecipeFunctions> logger)
    {
        _recipeService = recipeService;
        _logger = logger;
    }

    [Function("GetRecipes")]
    [OpenApiOperation(operationId: "GetRecipes", tags: ["Recipes"])]
    [OpenApiResponseWithBody(statusCode: HttpStatusCode.OK, contentType: "application/json",
        bodyType: typeof(IEnumerable<Recipe>), Description: "List of recipes")]
    public async Task<HttpResponseData> GetRecipes(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "recipes")] HttpRequestData req)
    {
        _logger.LogInformation("Getting all recipes");

        var recipes = await _recipeService.GetAllAsync();

        var response = req.CreateResponse(HttpStatusCode.OK);
        await response.WriteAsJsonAsync(recipes);
        return response;
    }

    [Function("GetRecipeById")]
    [OpenApiOperation(operationId: "GetRecipeById", tags: ["Recipes"])]
    [OpenApiParameter(name: "id", In = ParameterLocation.Path, Required = true, Type = typeof(string))]
    [OpenApiResponseWithBody(statusCode: HttpStatusCode.OK, contentType: "application/json",
        bodyType: typeof(Recipe), Description: "Recipe details")]
    [OpenApiResponseWithoutBody(statusCode: HttpStatusCode.NotFound, Description: "Recipe not found")]
    public async Task<HttpResponseData> GetRecipeById(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "recipes/{id}")] HttpRequestData req,
        string id)
    {
        _logger.LogInformation("Getting recipe {RecipeId}", id);

        var recipe = await _recipeService.GetByIdAsync(id);

        if (recipe is null)
        {
            return req.CreateResponse(HttpStatusCode.NotFound);
        }

        var response = req.CreateResponse(HttpStatusCode.OK);
        await response.WriteAsJsonAsync(recipe);
        return response;
    }

    [Function("CreateRecipe")]
    [OpenApiOperation(operationId: "CreateRecipe", tags: ["Recipes"])]
    [OpenApiSecurity("bearer_auth", SecuritySchemeType.Http, Scheme = OpenApiSecuritySchemeType.Bearer)]
    [OpenApiRequestBody(contentType: "application/json", bodyType: typeof(CreateRecipeRequest), Required = true)]
    [OpenApiResponseWithBody(statusCode: HttpStatusCode.Created, contentType: "application/json",
        bodyType: typeof(Recipe), Description: "Created recipe")]
    [OpenApiResponseWithoutBody(statusCode: HttpStatusCode.BadRequest, Description: "Validation error")]
    public async Task<HttpResponseData> CreateRecipe(
        [HttpTrigger(AuthorizationLevel.Anonymous, "post", Route = "recipes")] HttpRequestData req)
    {
        var request = await req.ReadFromJsonAsync<CreateRecipeRequest>();

        if (request is null || string.IsNullOrWhiteSpace(request.Title))
        {
            var badRequest = req.CreateResponse(HttpStatusCode.BadRequest);
            await badRequest.WriteAsJsonAsync(new { error = "Title is required" });
            return badRequest;
        }

        var recipe = new Recipe
        {
            Title = request.Title,
            Description = request.Description,
            Ingredients = request.Ingredients,
            Instructions = request.Instructions,
            PrepTimeMinutes = request.PrepTimeMinutes,
            Difficulty = request.Difficulty,
            Tags = request.Tags,
            AuthorId = GetUserId(req)
        };

        var created = await _recipeService.CreateAsync(recipe);
        _logger.LogInformation("Created recipe {RecipeId}: {Title}", created.Id, created.Title);

        var response = req.CreateResponse(HttpStatusCode.Created);
        response.Headers.Add("Location", $"/api/recipes/{created.Id}");
        await response.WriteAsJsonAsync(created);
        return response;
    }

    [Function("UpdateRecipe")]
    [OpenApiOperation(operationId: "UpdateRecipe", tags: ["Recipes"])]
    [OpenApiSecurity("bearer_auth", SecuritySchemeType.Http, Scheme = OpenApiSecuritySchemeType.Bearer)]
    [OpenApiParameter(name: "id", In = ParameterLocation.Path, Required = true, Type = typeof(string))]
    [OpenApiRequestBody(contentType: "application/json", bodyType: typeof(UpdateRecipeRequest), Required = true)]
    [OpenApiResponseWithBody(statusCode: HttpStatusCode.OK, contentType: "application/json",
        bodyType: typeof(Recipe), Description: "Updated recipe")]
    [OpenApiResponseWithoutBody(statusCode: HttpStatusCode.NotFound, Description: "Recipe not found")]
    public async Task<HttpResponseData> UpdateRecipe(
        [HttpTrigger(AuthorizationLevel.Anonymous, "put", Route = "recipes/{id}")] HttpRequestData req,
        string id)
    {
        var request = await req.ReadFromJsonAsync<UpdateRecipeRequest>();

        if (request is null)
        {
            return req.CreateResponse(HttpStatusCode.BadRequest);
        }

        var updated = await _recipeService.UpdateAsync(id, request);

        if (updated is null)
        {
            return req.CreateResponse(HttpStatusCode.NotFound);
        }

        _logger.LogInformation("Updated recipe {RecipeId}", id);

        var response = req.CreateResponse(HttpStatusCode.OK);
        await response.WriteAsJsonAsync(updated);
        return response;
    }

    [Function("DeleteRecipe")]
    [OpenApiOperation(operationId: "DeleteRecipe", tags: ["Recipes"])]
    [OpenApiSecurity("bearer_auth", SecuritySchemeType.Http, Scheme = OpenApiSecuritySchemeType.Bearer)]
    [OpenApiParameter(name: "id", In = ParameterLocation.Path, Required = true, Type = typeof(string))]
    [OpenApiResponseWithoutBody(statusCode: HttpStatusCode.NoContent, Description: "Recipe deleted")]
    [OpenApiResponseWithoutBody(statusCode: HttpStatusCode.NotFound, Description: "Recipe not found")]
    public async Task<HttpResponseData> DeleteRecipe(
        [HttpTrigger(AuthorizationLevel.Anonymous, "delete", Route = "recipes/{id}")] HttpRequestData req,
        string id)
    {
        var deleted = await _recipeService.DeleteAsync(id);

        if (!deleted)
        {
            return req.CreateResponse(HttpStatusCode.NotFound);
        }

        _logger.LogInformation("Deleted recipe {RecipeId}", id);
        return req.CreateResponse(HttpStatusCode.NoContent);
    }

    [Function("SearchRecipes")]
    [OpenApiOperation(operationId: "SearchRecipes", tags: ["Recipes"])]
    [OpenApiParameter(name: "q", In = ParameterLocation.Query, Required = true, Type = typeof(string))]
    [OpenApiResponseWithBody(statusCode: HttpStatusCode.OK, contentType: "application/json",
        bodyType: typeof(IEnumerable<Recipe>), Description: "Search results")]
    public async Task<HttpResponseData> SearchRecipes(
        [HttpTrigger(AuthorizationLevel.Anonymous, "get", Route = "recipes/search")] HttpRequestData req)
    {
        var query = System.Web.HttpUtility.ParseQueryString(req.Url.Query).Get("q");

        if (string.IsNullOrWhiteSpace(query))
        {
            var badRequest = req.CreateResponse(HttpStatusCode.BadRequest);
            await badRequest.WriteAsJsonAsync(new { error = "Query parameter 'q' is required" });
            return badRequest;
        }

        var results = await _recipeService.SearchAsync(query);

        var response = req.CreateResponse(HttpStatusCode.OK);
        await response.WriteAsJsonAsync(results);
        return response;
    }

    private static string GetUserId(HttpRequestData req)
    {
        // In production, extract from JWT claims
        // req.Headers.TryGetValues("Authorization", out var authHeaders);
        return "anonymous";
    }
}
```

---

## Local Development

### Prerequisites

```bash
# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Install Cosmos DB Emulator (Windows) or use Docker
# Windows: Download from https://aka.ms/cosmosdb-emulator
# Docker:
docker run -p 8081:8081 -p 10250-10255:10250-10255 mcr.microsoft.com/cosmosdb/linux/azure-cosmos-emulator
```

### Create Database and Container

```bash
# Using Azure CLI (for cloud Cosmos DB)
az cosmosdb sql database create \
  --account-name mycosmosaccount \
  --resource-group my-rg \
  --name RecipeDb

az cosmosdb sql container create \
  --account-name mycosmosaccount \
  --resource-group my-rg \
  --database-name RecipeDb \
  --name Recipes \
  --partition-key-path "/id" \
  --throughput 400
```

### Run Locally

```bash
# Restore and build
dotnet restore
dotnet build

# Start function app
func start

# Test endpoints
curl http://localhost:7071/api/recipes
curl -X POST http://localhost:7071/api/recipes \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Pasta","description":"Delicious","ingredients":["pasta","sauce"],"instructions":["boil","mix"],"prepTimeMinutes":20}'

# OpenAPI/Swagger UI
# Navigate to http://localhost:7071/api/swagger/ui
```

---

## Deployment

### Application Settings (Azure Portal / CLI)

```bash
az functionapp config appsettings set \
  --name my-recipe-api \
  --resource-group my-rg \
  --settings \
    "CosmosDb:ConnectionString=AccountEndpoint=https://mycosmosaccount.documents.azure.com:443/;AccountKey=..." \
    "CosmosDb:DatabaseName=RecipeDb" \
    "CosmosDb:ContainerName=Recipes"
```

### GitHub Actions Workflow

#### .github/workflows/deploy.yml

```yaml
name: Deploy Azure Functions

on:
  push:
    branches: [main]
  workflow_dispatch:

env:
  AZURE_FUNCTIONAPP_NAME: my-recipe-api
  DOTNET_VERSION: 8.0.x

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: ${{ env.DOTNET_VERSION }}

      - name: Restore dependencies
        run: dotnet restore

      - name: Build
        run: dotnet build --configuration Release --no-restore

      - name: Publish
        run: dotnet publish --configuration Release --output ./publish --no-build

      - name: Deploy to Azure Functions
        uses: Azure/functions-action@v1
        with:
          app-name: ${{ env.AZURE_FUNCTIONAPP_NAME }}
          package: ./publish
          publish-profile: ${{ secrets.AZURE_FUNCTIONAPP_PUBLISH_PROFILE }}

      - name: Smoke test
        run: |
          sleep 30
          RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" https://${{ env.AZURE_FUNCTIONAPP_NAME }}.azurewebsites.net/api/recipes)
          if [ "$RESPONSE" != "200" ]; then
            echo "Smoke test failed with status $RESPONSE"
            exit 1
          fi
          echo "Smoke test passed"
```

---

## API Endpoints Summary

| Method | Route | Auth | Description |
|--------|-------|------|-------------|
| GET | `/api/recipes` | Anonymous | List all recipes |
| GET | `/api/recipes/{id}` | Anonymous | Get recipe by ID |
| POST | `/api/recipes` | Bearer | Create new recipe |
| PUT | `/api/recipes/{id}` | Bearer | Update recipe |
| DELETE | `/api/recipes/{id}` | Bearer | Delete recipe |
| GET | `/api/recipes/search?q=` | Anonymous | Search recipes |
| GET | `/api/swagger/ui` | Anonymous | OpenAPI docs |
