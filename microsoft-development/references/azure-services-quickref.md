# Azure Services Quick Reference

Organized by category with descriptions, use cases, pricing hints, and SDK package names.

---

## Compute

### App Service
Web app hosting with managed platform, auto-scale, deployment slots, and custom domains.

- **Use cases:** Web APIs, SPAs, full-stack apps, containerized web apps
- **Pricing hint:** Free (F1), Basic (B1 ~$13/mo), Standard (S1 ~$73/mo), Premium (P1v3 ~$138/mo)
- **SDK packages:**
  - JS: `@azure/arm-appservice`
  - Python: `azure-mgmt-web`
  - .NET: `Azure.ResourceManager.AppService`

### Azure Functions
Serverless event-driven compute — pay only for execution time.

- **Use cases:** HTTP APIs, scheduled jobs, event processing, webhooks, background tasks
- **Pricing hint:** Consumption plan: 1M executions free/month, ~$0.20 per additional million
- **SDK packages:**
  - JS: `@azure/functions` (v4 programming model)
  - Python: `azure-functions`
  - .NET: `Microsoft.Azure.Functions.Worker`

### Container Apps
Serverless containers with built-in scaling, Dapr integration, and revision management.

- **Use cases:** Microservices, API gateways, background workers, event-driven apps
- **Pricing hint:** Consumption: ~$0.000012/vCPU-second, 180K vCPU-seconds free/month
- **SDK packages:**
  - JS: `@azure/arm-appcontainers`
  - Python: `azure-mgmt-appcontainers`
  - .NET: `Azure.ResourceManager.AppContainers`

### Azure Kubernetes Service (AKS)
Managed Kubernetes with integrated CI/CD, monitoring, and governance.

- **Use cases:** Complex microservice architectures, multi-container apps, ML workloads
- **Pricing hint:** Control plane free; pay for VMs (e.g., Standard_D2s_v5 ~$70/mo)
- **SDK packages:**
  - JS: `@azure/arm-containerservice`
  - Python: `azure-mgmt-containerservice`
  - .NET: `Azure.ResourceManager.ContainerService`

### Virtual Machines
Full IaaS with Linux/Windows VMs, SSH/RDP, and custom images.

- **Use cases:** Legacy apps, custom OS needs, GPU workloads, development/test
- **Pricing hint:** B1s (1 vCPU, 1GB) ~$7.50/mo; D2s_v5 (2 vCPU, 8GB) ~$70/mo
- **SDK packages:**
  - JS: `@azure/arm-compute`
  - Python: `azure-mgmt-compute`
  - .NET: `Azure.ResourceManager.Compute`

---

## Storage

### Blob Storage
Object storage for unstructured data — files, images, videos, backups.

- **Use cases:** Static file hosting, media storage, data lake, backup/archive
- **Pricing hint:** Hot: ~$0.018/GB/mo, Cool: ~$0.01/GB/mo, Archive: ~$0.002/GB/mo
- **SDK packages:**
  - JS: `@azure/storage-blob`
  - Python: `azure-storage-blob`
  - .NET: `Azure.Storage.Blobs`

### Table Storage
NoSQL key-value store for semi-structured data at massive scale.

- **Use cases:** User profiles, device metadata, IoT data, config storage
- **Pricing hint:** ~$0.045/GB/mo storage, ~$0.00036/10K transactions
- **SDK packages:**
  - JS: `@azure/data-tables`
  - Python: `azure-data-tables`
  - .NET: `Azure.Data.Tables`

### Queue Storage
Simple message queueing between application components.

- **Use cases:** Task queues, decoupled processing, load leveling
- **Pricing hint:** ~$0.004/10K operations
- **SDK packages:**
  - JS: `@azure/storage-queue`
  - Python: `azure-storage-queue`
  - .NET: `Azure.Storage.Queues`

### Azure Files
SMB/NFS file shares in the cloud, mountable on Windows/Linux/macOS.

- **Use cases:** Shared app storage, file migration, hybrid file serving
- **Pricing hint:** Hot: ~$0.06/GB/mo (premium SSD ~$0.16/GB/mo)
- **SDK packages:**
  - JS: `@azure/storage-file-share`
  - Python: `azure-storage-file-share`
  - .NET: `Azure.Storage.Files.Shares`

### Data Lake Storage Gen2
Hierarchical namespace on top of Blob Storage — optimized for analytics.

- **Use cases:** Big data analytics, Hadoop/Spark workloads, data lakehouse
- **Pricing hint:** Similar to Blob (Hot: ~$0.018/GB/mo) with hierarchical namespace surcharge
- **SDK packages:**
  - JS: `@azure/storage-file-datalake`
  - Python: `azure-storage-file-datalake`
  - .NET: `Azure.Storage.Files.DataLake`

---

## Database

### Cosmos DB
Globally distributed, multi-model (SQL, MongoDB, Cassandra, Gremlin, Table) database.

- **Use cases:** Global apps, real-time personalization, IoT, gaming leaderboards
- **Pricing hint:** Serverless from ~$0.25/1M RUs; Provisioned 400 RU/s ~$24/mo
- **SDK packages:**
  - JS: `@azure/cosmos`
  - Python: `azure-cosmos`
  - .NET: `Microsoft.Azure.Cosmos`

### Azure SQL Database
Managed SQL Server with built-in intelligence, scaling, and high availability.

- **Use cases:** Relational apps, SaaS, reporting, ERP backends
- **Pricing hint:** Basic (5 DTU) ~$5/mo; S0 (10 DTU) ~$15/mo; serverless from ~$0.514/vCore-hour
- **SDK packages:**
  - JS: `mssql` or `tedious`
  - Python: `pyodbc`, `azure-mgmt-sql`
  - .NET: `Microsoft.Data.SqlClient`

### Azure Database for PostgreSQL
Managed PostgreSQL with Flexible Server and Citus (distributed).

- **Use cases:** Web apps, geospatial, JSON workloads, multi-tenant SaaS
- **Pricing hint:** Burstable B1ms ~$12/mo; General Purpose D2s ~$125/mo
- **SDK packages:**
  - JS: `pg`
  - Python: `psycopg2`, `azure-mgmt-rdbms`
  - .NET: `Npgsql`

### Azure Cache for Redis
In-memory data store for caching, session management, and real-time analytics.

- **Use cases:** Session cache, output cache, rate limiting, pub/sub messaging
- **Pricing hint:** Basic C0 (250MB) ~$16/mo; Standard C1 (1GB) ~$80/mo
- **SDK packages:**
  - JS: `ioredis` or `redis`
  - Python: `redis`, `azure-mgmt-redis`
  - .NET: `StackExchange.Redis`

---

## Networking

### Azure Front Door
Global load balancer with WAF, CDN, and intelligent routing.

- **Use cases:** Global web apps, multi-region HA, DDoS protection, SSL offloading
- **Pricing hint:** Standard ~$35/mo base + per-request pricing
- **SDK packages:**
  - JS: `@azure/arm-frontdoor`
  - Python: `azure-mgmt-frontdoor`
  - .NET: `Azure.ResourceManager.FrontDoor`

### Azure CDN
Content delivery network for static assets and media streaming.

- **Use cases:** Static site hosting, media delivery, API acceleration
- **Pricing hint:** Standard Microsoft: ~$0.081/GB (first 10TB)
- **SDK packages:**
  - JS: `@azure/arm-cdn`
  - Python: `azure-mgmt-cdn`
  - .NET: `Azure.ResourceManager.Cdn`

### Application Gateway
Regional L7 load balancer with WAF, URL routing, and SSL termination.

- **Use cases:** Internal web apps, API routing, SSL offloading, WAF protection
- **Pricing hint:** Standard_v2 ~$175/mo + capacity unit charges
- **SDK packages:**
  - JS: `@azure/arm-network`
  - Python: `azure-mgmt-network`
  - .NET: `Azure.ResourceManager.Network`

---

## Identity

### Microsoft Entra ID (formerly Azure AD)
Cloud identity and access management — SSO, MFA, conditional access.

- **Use cases:** User authentication, SSO, B2B collaboration, app registration
- **Pricing hint:** Free tier includes basic AAD; P1 ~$6/user/mo, P2 ~$9/user/mo
- **SDK packages:**
  - JS: `@azure/identity`, `@azure/msal-browser`, `@azure/msal-node`
  - Python: `azure-identity`, `msal`
  - .NET: `Azure.Identity`, `Microsoft.Identity.Web`

### MSAL (Microsoft Authentication Library)
Client libraries for authenticating users and acquiring tokens.

- **Use cases:** SPA login, Node.js API auth, desktop app auth, daemon apps
- **Pricing hint:** Free (part of Entra ID)
- **SDK packages:**
  - JS: `@azure/msal-browser` (SPA), `@azure/msal-node` (server)
  - Python: `msal`
  - .NET: `Microsoft.Identity.Client`

---

## Messaging

### Service Bus
Enterprise message broker with queues, topics, and subscriptions.

- **Use cases:** Microservice communication, ordered messaging, transaction processing
- **Pricing hint:** Basic ~$0.05/1M operations; Standard ~$10/mo + per-message
- **SDK packages:**
  - JS: `@azure/service-bus`
  - Python: `azure-servicebus`
  - .NET: `Azure.Messaging.ServiceBus`

### Event Grid
Reactive event routing with per-event push delivery model.

- **Use cases:** Resource change notifications, serverless triggers, event-driven architectures
- **Pricing hint:** ~$0.60/1M operations (first 100K free/month)
- **SDK packages:**
  - JS: `@azure/eventgrid`
  - Python: `azure-eventgrid`
  - .NET: `Azure.Messaging.EventGrid`

### Event Hubs
Big data streaming platform — millions of events per second.

- **Use cases:** Telemetry ingestion, log streaming, real-time analytics, Kafka replacement
- **Pricing hint:** Basic ~$11/TU/mo; Standard ~$22/TU/mo
- **SDK packages:**
  - JS: `@azure/event-hubs`
  - Python: `azure-eventhub`
  - .NET: `Azure.Messaging.EventHubs`

---

## AI & Machine Learning

### Azure OpenAI Service
GPT-4, GPT-4o, DALL-E, Whisper — enterprise-grade with content filtering.

- **Use cases:** Chatbots, content generation, document analysis, code assistance
- **Pricing hint:** GPT-4o ~$2.50/1M input tokens, $10/1M output tokens (varies by model)
- **SDK packages:**
  - JS: `openai` (with Azure config) or `@azure/openai`
  - Python: `openai` (with Azure config) or `azure-ai-openai`
  - .NET: `Azure.AI.OpenAI`

### Azure AI Services (formerly Cognitive Services)
Pre-built AI models — vision, speech, language, decision.

- **Use cases:** OCR, image classification, speech-to-text, sentiment analysis, translation
- **Pricing hint:** Free tiers available; pay-per-transaction (e.g., Vision: ~$1/1K transactions)
- **SDK packages:**
  - JS: `@azure/ai-text-analytics`, `@azure/ai-vision-image-analysis`, `@azure/ai-form-recognizer`
  - Python: `azure-ai-textanalytics`, `azure-ai-vision`, `azure-ai-formrecognizer`
  - .NET: `Azure.AI.TextAnalytics`, `Azure.AI.Vision.ImageAnalysis`, `Azure.AI.FormRecognizer`

### Azure Machine Learning
MLOps platform — model training, deployment, monitoring, and pipelines.

- **Use cases:** Custom model training, AutoML, model registry, batch inference
- **Pricing hint:** Free workspace; pay for compute (e.g., NC6s_v3 GPU ~$3.06/hr)
- **SDK packages:**
  - JS: `@azure/arm-machinelearning`
  - Python: `azure-ai-ml`, `azureml-core`
  - .NET: `Azure.ResourceManager.MachineLearning`
