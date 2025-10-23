"""Zendesk API client."""

import mindsdb_sdk
from typing import List
from models.zendesk_ticket import ZendeskTicket


class ZendeskClient:
    """Client for interacting with Zendesk API."""

    def __init__(self, database="zendesk_datasource"):
        self.server = mindsdb_sdk.connect()
        self.kb = self.server.knowledge_bases.get("zendesk_kb")

    def search_tickets(self, content: str = None, filters: dict = None):
        query = "SELECT * FROM zendesk_kb"
        conditions = []

        if content:
            conditions.append(f"content = '{content}'")

        if filters:
            for key, value in filters.items():
                conditions.append(f"{key} = '{value}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return self.server.query(query).fetch()

    
    def query_tickets(self, query: dict = None) -> List[ZendeskTicket]:
        table = self.server.databases.zendesk_datasource.tables.issues

        df = table.filter(**query).fetch() if query else table.fetch()
    
        records = df.to_dict(orient="records")

        return [ZendeskTicket(**record) for record in records]
