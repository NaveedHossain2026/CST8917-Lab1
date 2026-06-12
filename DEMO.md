# Serverless Text Analyzer App (Azure Functions + Cosmos DB)

A serverless Python application built with **Azure Functions** and **Azure Cosmos DB**.  
It analyzes text (word count, characters, sentences, reading time) and stores results in a NoSQL database for historical tracking and retrieval.

---

## 🎥 Demo Video
[YouTube Demo](PASTE_YOUR_UNLISTED_YOUTUBE_URL_HERE)

---

## ⚙️ Prerequisites

Make sure you have the following installed:

- Python 3.12+
- Azure Functions Core Tools v4
- Visual Studio Code
- Azurite (local storage emulator)

---

## 🔐 Configuration

### Local Setup (`local.settings.json`)

Create a `local.settings.json` file in the project root:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "CosmosDBConnectionString": "<your-cosmos-db-connection-string>"
  }
}
```

### Azure Deployment Settings

In Azure Function App settings, add:

- **Name:** CosmosDBConnectionString  
- **Value:** Your Azure Cosmos DB connection string

---

## ▶️ Running Locally

### 1. Create virtual environment

python -m venv .venv

Activate it:

Windows:
.venv\Scripts\activate

macOS/Linux:
source .venv/bin/activate

---

### 2. Install dependencies

pip install -r requirements.txt

---

### 3. Start Azurite

In VS Code:
- Press F1
- Run: Azurite: Start

---

### 4. Run Azure Functions

func start

---

## 🧪 API Testing

### Analyze Text (POST)

curl -X POST http://localhost:7071/api/textanalyzer \
-H "Content-Type: application/json" \
-d "{\"text\": \"Hello serverless world!\"}"

---

### Get History (GET)

curl "http://localhost:7071/api/getanalysishistory?limit=5"

---

