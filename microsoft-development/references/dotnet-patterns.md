# .NET Common Patterns Reference

Essential patterns for modern .NET development with C# code examples.

---

## Dependency Injection

.NET's built-in DI container in `Microsoft.Extensions.DependencyInjection`.

### Service Registration

```csharp
var builder = WebApplication.CreateBuilder(args);

// Transient — new instance per request
builder.Services.AddTransient<IEmailService, SmtpEmailService>();

// Scoped — one per HTTP request
builder.Services.AddScoped<IRecipeRepository, RecipeRepository>();

// Singleton — shared across all requests
builder.Services.AddSingleton<ICacheService, MemoryCacheService>();

// Factory registration
builder.Services.AddScoped<INotificationService>(sp =>
{
    var config = sp.GetRequiredService<IOptions<NotificationOptions>>();
    return new NotificationService(config.Value.Provider);
});
```

### Constructor Injection

```csharp
public class RecipeService
{
    private readonly IRecipeRepository _repository;
    private readonly ILogger<RecipeService> _logger;

    public RecipeService(IRecipeRepository repository, ILogger<RecipeService> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public async Task<Recipe?> GetByIdAsync(int id)
    {
        _logger.LogInformation("Fetching recipe {RecipeId}", id);
        return await _repository.GetByIdAsync(id);
    }
}
```

---

## Options Pattern (IOptions)

Strongly typed configuration binding.

### Configuration Classes

```csharp
public class DatabaseOptions
{
    public const string SectionName = "Database";

    public string ConnectionString { get; set; } = string.Empty;
    public int MaxRetryCount { get; set; } = 3;
    public int CommandTimeoutSeconds { get; set; } = 30;
}

public class JwtOptions
{
    public const string SectionName = "Jwt";

    public string Secret { get; set; } = string.Empty;
    public string Issuer { get; set; } = string.Empty;
    public string Audience { get; set; } = string.Empty;
    public int ExpirationMinutes { get; set; } = 60;
}
```

### Registration and Usage

```csharp
// In Program.cs
builder.Services.Configure<DatabaseOptions>(
    builder.Configuration.GetSection(DatabaseOptions.SectionName));
builder.Services.Configure<JwtOptions>(
    builder.Configuration.GetSection(JwtOptions.SectionName));

// In a service — use IOptions<T> for singleton, IOptionsSnapshot<T>
// for scoped (reloads on change), IOptionsMonitor<T> for real-time
public class RecipeRepository
{
    private readonly DatabaseOptions _dbOptions;

    public RecipeRepository(IOptions<DatabaseOptions> options)
    {
        _dbOptions = options.Value;
    }
}
```

### appsettings.json

```json
{
  "Database": {
    "ConnectionString": "Server=localhost;Database=RecipeDb;Trusted_Connection=true;",
    "MaxRetryCount": 3,
    "CommandTimeoutSeconds": 30
  },
  "Jwt": {
    "Secret": "your-secret-key-at-least-32-characters-long",
    "Issuer": "KitchenOdyssey",
    "Audience": "KitchenOdysseyUsers",
    "ExpirationMinutes": 60
  }
}
```

---

## Middleware Pipeline

Request/response processing pipeline.

### Custom Middleware

```csharp
public class RequestTimingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestTimingMiddleware> _logger;

    public RequestTimingMiddleware(RequestDelegate next, ILogger<RequestTimingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var stopwatch = Stopwatch.StartNew();

        context.Response.OnStarting(() =>
        {
            stopwatch.Stop();
            context.Response.Headers["X-Response-Time"] = $"{stopwatch.ElapsedMilliseconds}ms";
            return Task.CompletedTask;
        });

        await _next(context);

        _logger.LogInformation(
            "{Method} {Path} responded {StatusCode} in {Elapsed}ms",
            context.Request.Method,
            context.Request.Path,
            context.Response.StatusCode,
            stopwatch.ElapsedMilliseconds);
    }
}

// Extension method for clean registration
public static class MiddlewareExtensions
{
    public static IApplicationBuilder UseRequestTiming(this IApplicationBuilder app)
        => app.UseMiddleware<RequestTimingMiddleware>();
}
```

### Pipeline Order

```csharp
var app = builder.Build();

// Order matters — each middleware wraps the next
app.UseExceptionHandler("/error");
app.UseHsts();
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseCors("AllowFrontend");
app.UseRequestTiming();       // Custom
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

---

## Minimal APIs

Concise endpoint definitions without controllers.

### Basic CRUD

```csharp
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddScoped<IRecipeRepository, RecipeRepository>();

var app = builder.Build();

var recipes = app.MapGroup("/api/recipes").WithTags("Recipes");

recipes.MapGet("/", async (IRecipeRepository repo) =>
    Results.Ok(await repo.GetAllAsync()));

recipes.MapGet("/{id:int}", async (int id, IRecipeRepository repo) =>
    await repo.GetByIdAsync(id) is { } recipe
        ? Results.Ok(recipe)
        : Results.NotFound());

recipes.MapPost("/", async (CreateRecipeRequest request, IRecipeRepository repo) =>
{
    var recipe = await repo.CreateAsync(request);
    return Results.Created($"/api/recipes/{recipe.Id}", recipe);
});

recipes.MapPut("/{id:int}", async (int id, UpdateRecipeRequest request, IRecipeRepository repo) =>
    await repo.UpdateAsync(id, request)
        ? Results.NoContent()
        : Results.NotFound());

recipes.MapDelete("/{id:int}", async (int id, IRecipeRepository repo) =>
    await repo.DeleteAsync(id)
        ? Results.NoContent()
        : Results.NotFound());

app.Run();
```

### Request Validation with Filters

```csharp
recipes.MapPost("/", async (CreateRecipeRequest request, IRecipeRepository repo) =>
{
    var recipe = await repo.CreateAsync(request);
    return Results.Created($"/api/recipes/{recipe.Id}", recipe);
})
.AddEndpointFilter(async (context, next) =>
{
    var request = context.GetArgument<CreateRecipeRequest>(0);
    if (string.IsNullOrWhiteSpace(request.Title))
        return Results.ValidationProblem(
            new Dictionary<string, string[]> { ["Title"] = ["Title is required"] });
    return await next(context);
});
```

---

## Entity Framework Core

### DbContext

```csharp
public class RecipeDbContext : DbContext
{
    public RecipeDbContext(DbContextOptions<RecipeDbContext> options) : base(options) { }

    public DbSet<Recipe> Recipes => Set<Recipe>();
    public DbSet<Ingredient> Ingredients => Set<Ingredient>();
    public DbSet<User> Users => Set<User>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Recipe>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.Property(e => e.Title).HasMaxLength(200).IsRequired();
            entity.Property(e => e.Description).HasMaxLength(2000);
            entity.HasMany(e => e.Ingredients).WithOne(i => i.Recipe);
            entity.HasOne(e => e.Author).WithMany(u => u.Recipes);
            entity.HasIndex(e => e.Title);
        });
    }
}
```

### Registration

```csharp
builder.Services.AddDbContext<RecipeDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("Default"),
        sqlOptions => sqlOptions.EnableRetryOnFailure(3)));
```

### Migrations

```bash
# Create migration
dotnet ef migrations add InitialCreate

# Apply migration
dotnet ef database update

# Generate SQL script
dotnet ef migrations script --idempotent -o migration.sql
```

### LINQ Queries

```csharp
public class RecipeRepository : IRecipeRepository
{
    private readonly RecipeDbContext _context;

    public RecipeRepository(RecipeDbContext context) => _context = context;

    public async Task<List<Recipe>> SearchAsync(string query, int page = 1, int pageSize = 20)
    {
        return await _context.Recipes
            .Include(r => r.Ingredients)
            .Include(r => r.Author)
            .Where(r => r.Title.Contains(query) || r.Description.Contains(query))
            .OrderByDescending(r => r.CreatedAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .AsNoTracking()
            .ToListAsync();
    }

    public async Task<Recipe?> GetByIdAsync(int id)
    {
        return await _context.Recipes
            .Include(r => r.Ingredients)
            .Include(r => r.Author)
            .FirstOrDefaultAsync(r => r.Id == id);
    }
}
```

---

## Configuration

### Sources (loaded in order, last wins)

```csharp
var builder = WebApplication.CreateBuilder(args);

// Default sources (auto-configured):
// 1. appsettings.json
// 2. appsettings.{Environment}.json
// 3. User secrets (Development only)
// 4. Environment variables
// 5. Command-line arguments

// Custom sources
builder.Configuration.AddJsonFile("custom-config.json", optional: true, reloadOnChange: true);
builder.Configuration.AddAzureKeyVault(new Uri("https://myvault.vault.azure.net/"), new DefaultAzureCredential());
```

### User Secrets (Development)

```bash
# Initialize user secrets
dotnet user-secrets init

# Set values
dotnet user-secrets set "Jwt:Secret" "my-dev-secret-key-12345678901234567890"
dotnet user-secrets set "Database:ConnectionString" "Server=localhost;Database=DevDb;"
```

### Environment Variables

```bash
# Convention: use __ (double underscore) for nested keys
Database__ConnectionString="Server=prod;Database=ProdDb;"
Jwt__Secret="production-secret"
```

---

## Logging (ILogger)

```csharp
public class RecipeService
{
    private readonly ILogger<RecipeService> _logger;

    public RecipeService(ILogger<RecipeService> logger) => _logger = logger;

    public async Task<Recipe?> GetByIdAsync(int id)
    {
        _logger.LogDebug("Fetching recipe {RecipeId}", id);

        try
        {
            var recipe = await _repository.GetByIdAsync(id);

            if (recipe is null)
            {
                _logger.LogWarning("Recipe {RecipeId} not found", id);
                return null;
            }

            _logger.LogInformation("Retrieved recipe {RecipeId}: {Title}", id, recipe.Title);
            return recipe;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to fetch recipe {RecipeId}", id);
            throw;
        }
    }
}
```

### Configuration in appsettings.json

```json
{
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning",
      "Microsoft.EntityFrameworkCore.Database.Command": "Information"
    }
  }
}
```

---

## Health Checks

```csharp
builder.Services.AddHealthChecks()
    .AddSqlServer(builder.Configuration.GetConnectionString("Default")!, name: "database")
    .AddRedis(builder.Configuration["Redis:ConnectionString"]!, name: "redis")
    .AddUrlGroup(new Uri("https://api.external.com/health"), name: "external-api");

var app = builder.Build();

app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = async (context, report) =>
    {
        context.Response.ContentType = "application/json";
        var result = new
        {
            status = report.Status.ToString(),
            checks = report.Entries.Select(e => new
            {
                name = e.Key,
                status = e.Value.Status.ToString(),
                duration = e.Value.Duration.TotalMilliseconds
            })
        };
        await context.Response.WriteAsJsonAsync(result);
    }
});
```

---

## Background Services (IHostedService)

```csharp
public class RecipeCleanupService : BackgroundService
{
    private readonly IServiceScopeFactory _scopeFactory;
    private readonly ILogger<RecipeCleanupService> _logger;
    private readonly TimeSpan _interval = TimeSpan.FromHours(6);

    public RecipeCleanupService(
        IServiceScopeFactory scopeFactory,
        ILogger<RecipeCleanupService> logger)
    {
        _scopeFactory = scopeFactory;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        _logger.LogInformation("Recipe cleanup service started");

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                using var scope = _scopeFactory.CreateScope();
                var context = scope.ServiceProvider.GetRequiredService<RecipeDbContext>();

                var cutoff = DateTime.UtcNow.AddDays(-30);
                var drafts = await context.Recipes
                    .Where(r => r.IsDraft && r.UpdatedAt < cutoff)
                    .ToListAsync(stoppingToken);

                if (drafts.Count > 0)
                {
                    context.Recipes.RemoveRange(drafts);
                    await context.SaveChangesAsync(stoppingToken);
                    _logger.LogInformation("Cleaned up {Count} stale drafts", drafts.Count);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error during recipe cleanup");
            }

            await Task.Delay(_interval, stoppingToken);
        }
    }
}

// Registration
builder.Services.AddHostedService<RecipeCleanupService>();
```

---

## Authentication & Authorization

### JWT Bearer Authentication

```csharp
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        var jwtOptions = builder.Configuration.GetSection("Jwt").Get<JwtOptions>()!;
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = jwtOptions.Issuer,
            ValidateAudience = true,
            ValidAudience = jwtOptions.Audience,
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(jwtOptions.Secret)),
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        };
    });

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("AdminOnly", policy => policy.RequireRole("Admin"));
    options.AddPolicy("RecipeOwner", policy =>
        policy.Requirements.Add(new RecipeOwnerRequirement()));
});
```

### Endpoint Authorization

```csharp
// Minimal API
recipes.MapPost("/", CreateRecipe).RequireAuthorization();
recipes.MapDelete("/{id}", DeleteRecipe).RequireAuthorization("AdminOnly");

// Controller
[Authorize]
[ApiController]
[Route("api/[controller]")]
public class RecipesController : ControllerBase
{
    [HttpGet]
    [AllowAnonymous]
    public async Task<IActionResult> GetAll() { /* ... */ }

    [HttpPost]
    public async Task<IActionResult> Create(CreateRecipeRequest request) { /* ... */ }

    [HttpDelete("{id}")]
    [Authorize(Policy = "AdminOnly")]
    public async Task<IActionResult> Delete(int id) { /* ... */ }
}
```
