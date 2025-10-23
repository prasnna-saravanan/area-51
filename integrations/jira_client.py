from typing import Dict, List
import mindsdb_sdk

from models.jira_issue import JiraIssue


class JiraClient:
    """Client for interacting with JIRA API."""

    def __init__(self):
        self.server = mindsdb_sdk.connect()
        self.jira_kb = self.server.knowledge_bases.get('jira_kb')

    def search_tickets(self, content: str = None, filters: dict = None):
        query = "SELECT * FROM jira_kb"
        conditions = []

        if content:
            conditions.append(f"content = '{content}'")

        if filters:
            for key, value in filters.items():
                conditions.append(f"{key} = '{value}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return self.server.query(query).fetch().to_dict(orient="records")

    
    def query_tickets(self, query: dict = None) -> List[JiraIssue]:
        table = self.server.databases.jira_datasource.tables.issues

        df = table.filter(**query).fetch() if query else table.fetch()
    
        records = df.to_dict(orient="records")

        return [JiraIssue(**record) for record in records]
        