import azure.functions as func
import json
import re
import uuid
import os
from datetime import datetime
from azure.cosmos import CosmosClient, exceptions

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Initialize Cosmos Client from Environment Variable safely
CONNECTION_STRING = os.environ.get("CosmosDBConnectionString")
DATABASE_NAME = "LabDatabase"
CONTAINER_NAME = "AnalysisHistory"

def get_container():
    # Helper to resolve Cosmos connection targets
    client = CosmosClient.from_connection_string(CONNECTION_STRING)
    database = client.get_database_client(DATABASE_NAME)
    return database.get_container_client(CONTAINER_NAME)

@app.route(route="textanalyzer", methods=["POST"])
def TextAnalyzer(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        original_text = req_body.get('text', '')
    except ValueError:
        return func.HttpResponse("Invalid JSON input.", status_code=400)

    if not original_text:
        return func.HttpResponse("Please pass 'text' in the request body.", status_code=400)

    # Core Analysis Logic
    words = re.findall(r'\b\w+\b', original_text)
    word_count = len(words)
    char_count = len(original_text)
    char_no_spaces = len(original_text.replace(" ", ""))
    sentences = [s for s in re.split(r'[.!?]+', original_text) if s.strip()]
    sentence_count = len(sentences) if sentences else 1
    
    analysis = {
        "wordCount": word_count,
        "characterCount": char_count,
        "characterCountNoSpaces": char_no_spaces,
        "sentenceCount": sentence_count,
        "readingTimeMinutes": round(word_count / 200, 2)
    }
    
    metadata = {
        "analyzedAt": datetime.utcnow().isoformat(),
        "textPreview": original_text[:50] + "..." if len(original_text) > 50 else original_text
    }

    # Generate a record document matching Part 13 specifications
    record_id = str(uuid.uuid4())
    document = {
        "id": record_id,
        "analysis": analysis,
        "metadata": metadata,
        "originalText": original_text
    }

    # Save Document to Azure Cosmos DB
    try:
        container = get_container()
        container.create_item(body=document)
    except exceptions.CosmosHttpResponseError as e:
        return func.HttpResponse(f"Database write failure: {str(e)}", status_code=500)

    return func.HttpResponse(json.dumps(document), mimetype="application/json")


@app.route(route="GetAnalysisHistory", methods=["GET"])
def GetAnalysisHistory(req: func.HttpRequest) -> func.HttpResponse:
    # Read query parameter 'limit', default to 10
    limit_param = req.params.get('limit', '10')
    try:
        limit = int(limit_param)
    except ValueError:
        limit = 10

    try:
        container = get_container()
        # Query items sorted by analysis timestamp descending
        query = f"SELECT * FROM c ORDER BY c.metadata.analyzedAt DESC OFFSET 0 LIMIT {limit}"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        
        response_payload = {
            "count": len(items),
            "results": items
        }
        return func.HttpResponse(json.dumps(response_payload), mimetype="application/json")
    except exceptions.CosmosHttpResponseError as e:
        return func.HttpResponse(f"Database read failure: {str(e)}", status_code=500)