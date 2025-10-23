import mindsdb_sdk
import sys

def create_db():
    server = mindsdb_sdk.connect()
    
    print("Connecting to local PostgreSQL with PGVector on port 5432...")

    try:
        server.databases.create(
            engine='pgvector',  
            name='zendesk',
            connection_args={
                'host': '127.0.0.1',
                'port': 5432,
                'database': 'mindsdb',  
                'user': 'mindsdb',      
                'password': 'mindsdb'
            }
        )
        print("✓ Successfully connected to PostgreSQL with PGVector!")
        print("✓ Database connection 'my_pgvector' is ready to use")
        print("\nNext: Run Cell 11 to create jira_kb_hybrid knowledge base")
                
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")


def create_kb(api_key = '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'):
    server = mindsdb_sdk.connect()
    server.knowledge_bases.drop("zendesk_kb")
    print("✓ Deleted existing zendesk_kb")

    # Create new knowledge base with PGVector storage
    zendesk_kb = server.knowledge_bases.create(
        name="zendesk_kb",
        embedding_model={
            "provider": "openai",
            "model_name": "text-embedding-3-small",
            "api_key": api_key,
        },
        reranking_model={
            "provider": "openai",
            "model_name": "gpt-4",
            "api_key": api_key,
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
    
