# Azure Database Service Choice

## My Choice
**Azure Cosmos DB (NoSQL API - Serverless Tier)**

## Justification
Azure Cosmos DB is a good choice for the Text Analyzer application because it can easily store and manage JSON data without needing a fixed database structure. Using the azure-cosmos library, the Python function can save the analysis results directly to the database with minimal code. Its SQL query features also make it easy to retrieve analysis history, sort results by date, and limit the number of records returned.

## Alternatives Considered
* **Azure SQL Database:** Not chosen because it requires predefined tables and schemas, which makes storing flexible JSON data more complicated.
* **Azure Table Storage:** Not chosen because its query capabilities are limited, making it difficult and less efficient to sort and retrieve historical data by timestamp.
* **Azure Blob Storage:** Not chosen because, although it can store JSON files at a low cost, it does not support database-style queries.

## Cost Considerations
This solution uses the Azure Cosmos DB Serverless Tier, which charges only when the database is used. Unlike fixed-cost options, there are no ongoing charges when the system is idle. If the Azure Function isn’t running, there are no database operation costs, making it a cost-efficient option for development and testing. 
