import mindsdb_sdk
import sys


def create_kb(api_key):
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
    create_kb(sys.argv[0])
