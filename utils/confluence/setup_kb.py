"""Setup and refresh Confluence KB with pgvector storage."""

import argparse
import os
from typing import Dict, List

import mindsdb_sdk
from dotenv import load_dotenv

# Load environment variables from .env files
# Try root .env first, then fall back to utils/confluence/.env
root_env = os.path.join(os.path.dirname(__file__), "..", "..", ".env")

if os.path.exists(root_env):
    load_dotenv(root_env)


def setup_pgvector_datasource() -> None:
    """Create pgvector datasource in MindsDB."""
    server = mindsdb_sdk.connect()

    # Get credentials from environment
    host = os.getenv("PGVECTOR_HOST", "host.docker.internal")
    port = os.getenv("PGVECTOR_PORT", "5432")
    database = os.getenv("PGVECTOR_DATABASE", "postgres")
    user = os.getenv("PGVECTOR_USER", "postgres")
    password = os.getenv("PGVECTOR_PASSWORD", "admin")

    # Drop existing datasource if needed
    try:
        server.databases.drop("pgvector_datasource")
        print("✓ Dropped existing pgvector_datasource")
    except Exception:
        pass

    # Create pgvector datasource using SDK
    server.databases.create(
        name="pgvector_datasource",
        engine="pgvector",
        connection_args={
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
        },
    )
    print("✓ Created pgvector_datasource")


def setup_confluence_datasource() -> None:
    """Create Confluence datasource in MindsDB."""
    server = mindsdb_sdk.connect()

    # Get credentials from environment
    api_base = os.getenv("CONFLUENCE_API_BASE")
    username = os.getenv("CONFLUENCE_USERNAME")
    password = os.getenv("CONFLUENCE_PASSWORD")

    if not all([api_base, username, password]):
        raise ValueError(
            "Missing Confluence credentials. Set CONFLUENCE_API_BASE, "
            "CONFLUENCE_USERNAME, and CONFLUENCE_PASSWORD environment variables"
        )

    # Drop existing datasource if needed
    try:
        server.databases.drop("confluence_datasource")
        print("✓ Dropped existing confluence_datasource")
    except Exception:
        pass

    # Create Confluence datasource
    server.databases.create(
        name="confluence_datasource",
        engine="confluence",
        connection_args={
            "api_base": api_base,
            "username": username,
            "password": password,
        },
    )
    print("✓ Created confluence_datasource")


def create_confluence_kb(
    api_key: str, azure_config: dict = None, use_pgvector: bool = True
) -> None:
    """Create Confluence knowledge base with pgvector storage."""
    server = mindsdb_sdk.connect()

    # Drop existing KB if it exists
    try:
        server.knowledge_bases.drop("confluence_kb")
        print("✓ Dropped existing confluence_kb")
    except Exception:
        pass

    # Configure embedding model
    if azure_config:
        embedding_model = {
            "provider": "azure_openai",
            "model_name": azure_config.get("deployment", "text-embedding-3-large"),
            "api_key": azure_config.get("api_key"),
            "base_url": azure_config.get("endpoint"),
            "api_version": azure_config.get("api_version", "2024-02-01"),
            "deployment": azure_config.get("deployment", "text-embedding-3-large"),
        }
        reranking_model = {
            "provider": "azure_openai",
            "model_name": azure_config.get("inference_deployment", "gpt-4.1"),
            "api_key": azure_config.get("api_key"),
            "base_url": azure_config.get("endpoint"),
            "api_version": azure_config.get("api_version", "2024-02-01"),
            "deployment": azure_config.get("inference_deployment", "gpt-4.1"),
        }
    else:
        embedding_model = {
            "provider": "openai",
            "model_name": "text-embedding-3-small",
            "api_key": api_key,
        }
        reranking_model = {
            "provider": "openai",
            "model_name": "gpt-4o",
            "api_key": api_key,
        }

    # Create knowledge base with pgvector storage
    kb_params = {
        "name": "confluence_kb",
        "embedding_model": embedding_model,
        "reranking_model": reranking_model,
        "metadata_columns": [
            "id",
            "status",
            "title",
            "spaceId",
            "authorId",
            "createdAt",
        ],
        "content_columns": ["body_storage_value"],
        "id_column": "id",
    }

    if use_pgvector:
        # Use pgvector storage
        kb_params["storage"] = server.databases.pgvector_datasource.tables.pages
        print("Creating KB with pgvector storage...")
    else:
        print("Creating KB without storage...")

    server.knowledge_bases.create(**kb_params)
    print("✓ Created confluence_kb")


def insert_confluence_data() -> None:
    """Insert Confluence data into knowledge base using SDK."""
    server = mindsdb_sdk.connect()

    # Get the KB
    confluence_kb = server.knowledge_bases.get("confluence_kb")

    # Use insert_query method with SDK
    confluence_kb.insert_query(server.databases.confluence_datasource.tables.pages)
    print("✓ Inserted data into confluence_kb")


def refresh_and_update() -> None:
    """Refresh datasource and update knowledge base."""
    server = mindsdb_sdk.connect()

    # Refresh the datasource
    server.query("REFRESH confluence_datasource")
    print("✓ Refreshed confluence_datasource")

    # Update the KB
    insert_confluence_data()
    print("✓ Updated confluence_kb")


def search_confluence_kb(query: str, filters: Dict = None) -> List[Dict]:
    """Search Confluence knowledge base."""
    server = mindsdb_sdk.connect()

    # Build query following MindsDB docs pattern
    sql = f"SELECT * FROM confluence_kb WHERE content='{query}'"

    if filters:
        for key, value in filters.items():
            sql += f" AND {key}='{value}'"

    return server.query(sql).fetch()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Setup or refresh Confluence KB")
    parser.add_argument(
        "--mode",
        choices=["setup", "refresh"],
        default="setup",
        help="Operation mode: setup (full setup) or refresh (update existing KB)",
    )
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Please set OPENAI_API_KEY environment variable")
        return

    # Azure OpenAI config (optional)
    azure_config = None
    azure_key = os.getenv("AZURE_OPENAI_API_KEY")
    if azure_key:
        azure_config = {
            "api_key": azure_key,
            "endpoint": os.getenv("AZURE_ENDPOINT", "https://tx-dev.openai.azure.com/"),
            "api_version": os.getenv("AZURE_API_VERSION", "2024-02-01"),
            "deployment": os.getenv("AZURE_DEPLOYMENT", "text-embedding-3-large"),
            "inference_deployment": os.getenv("AZURE_INFERENCE_DEPLOYMENT", "gpt-4.1"),
        }
        print("Using Azure OpenAI for embeddings")

    if args.mode == "setup":
        print("=" * 60)
        print("Setting up Confluence KB...")
        print("=" * 60)

        # Setup pgvector datasource
        setup_pgvector_datasource()

        # Setup Confluence datasource
        setup_confluence_datasource()

        # Create KB with pgvector storage
        create_confluence_kb(api_key, azure_config, use_pgvector=True)

        # Insert data
        insert_confluence_data()

        # Example search
        results = search_confluence_kb("authentication")
        print(f"✓ Found {len(results)} results")

    elif args.mode == "refresh":
        print("=" * 60)
        print("Refreshing Confluence KB...")
        print("=" * 60)

        # Refresh datasource and update KB
        refresh_and_update()


if __name__ == "__main__":
    main()
