import os

import mindsdb_sdk
import requests
from dotenv import load_dotenv

root_env = os.path.join(os.path.dirname(__file__), "..", ".env")

if os.path.exists(root_env):
    load_dotenv(root_env)


def create_db():
    server = mindsdb_sdk.connect()

    print("Connecting to local PostgreSQL with PGVector on port 5432...")

    try:
        server.databases.create(
            engine="pgvector",
            name="zendesk",
            connection_args={
                "host": "host.docker.internal",
                "port": 5432,
                "database": "mindsdb",
                "user": "mindsdb",
                "password": "mindsdb",
            },
        )
        print("✓ Successfully connected to PostgreSQL with PGVector!")
        print("✓ Database connection 'my_pgvector' is ready to use")
        print("\nNext: Run Cell 11 to create jira_kb_hybrid knowledge base")

    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")


def create_kb(
    api_key="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",
):
    server = mindsdb_sdk.connect()
    try:
        server.knowledge_bases.drop("zendesk_kb")
    except requests.HTTPError:
        pass
    print("✓ Deleted existing zendesk_kb")

    # Create new knowledge base with PGVector storage
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    if azure_key:
        azure_config = {
            "api_key": azure_key,
            "endpoint": os.getenv("AZURE_ENDPOINT", "https://tx-dev.openai.azure.com/"),
            "api_version": os.getenv("AZURE_API_VERSION", "2024-02-01"),
            "deployment": os.getenv("AZURE_DEPLOYMENT", "text-embedding-3-large"),
            "inference_deployment": os.getenv("AZURE_INFERENCE_DEPLOYMENT", "gpt-4.1"),
        }
    zendesk_kb = server.knowledge_bases.create(
        name="zendesk_kb",
        embedding_model={
            "provider": "azure_openai",
            "model_name": azure_config.get("deployment", "text-embedding-3-large"),
            "api_key": azure_config.get("api_key"),
            "base_url": azure_config.get("endpoint"),
            "api_version": azure_config.get("api_version", "2024-02-01"),
            "deployment": azure_config.get("deployment", "text-embedding-3-large"),
        },
        reranking_model={
            "provider": "azure_openai",
            "model_name": azure_config.get("inference_deployment", "gpt-4.1"),
            "api_key": azure_config.get("api_key"),
            "base_url": azure_config.get("endpoint"),
            "api_version": azure_config.get("api_version", "2024-02-01"),
            "deployment": azure_config.get("inference_deployment", "gpt-4.1"),
        },
        storage=server.databases.zendesk.tables.zendesk_tickets,
        metadata_columns=[
            "id",
            "status",
            "priority",
            "type",
            "assignee_id",
            "requester_id",
            "tags",
            "url",
            "created_at",
            "updated_at",
        ],
        content_columns=[
            "subject",
            "description",
        ],
        id_column="id",
    )

    print("Created Knowledge base")

    zendesk_data = server.databases.zendesk_datasource.tables.tickets.filter()
    zendesk_kb.insert(zendesk_data)
    print("Data inserted into knowledge base")


if __name__ == "__main__":
    create_db()
    create_kb()
