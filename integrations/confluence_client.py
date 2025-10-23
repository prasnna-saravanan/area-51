"""Confluence integration via MindsDB."""

from typing import Dict, List, Union

import mindsdb_sdk

from tools.search import SemanticSearchTool
from models.confluence_page import ConfluencePage


class ConfluenceClient:
    """Client for interacting with Confluence via MindsDB."""

    def __init__(self):
        """Initialize MindsDB connection."""
        self.server = mindsdb_sdk.connect()
        self.search_tool = SemanticSearchTool(kb_name="confluence_kb")

    def get_pages(
        self, space_key: str = "SOP", limit: int = 100, as_models: bool = False
    ) -> List[Union[Dict, ConfluencePage]]:
        """
        Get pages from Confluence via MindsDB.

        Args:
            space_key: Space key (default: SOP)
            limit: Maximum number of pages
            as_models: If True, return ConfluencePage objects instead of dicts

        Returns:
            List of pages
        """
        query = f"""
        SELECT * FROM confluence_datasource.pages
        WHERE spaceKey = '{space_key}'
        LIMIT {limit}
        """
        results = self.server.query(query).fetch()

        if as_models:
            return [ConfluencePage(**row) for row in results]
        return results

    def get_page(
        self, page_id: str, as_model: bool = False
    ) -> Union[Dict, ConfluencePage]:
        """Get a specific page by ID."""
        query = f"""
        SELECT * FROM confluence_datasource.pages
        WHERE id = '{page_id}'
        """
        results = self.server.query(query).fetch()

        if results:
            result = results[0]
            return ConfluencePage(**result) if as_model else result
        return {} if not as_model else None

    def search_kb(self, query: str, filters: Dict = None) -> List[Dict]:
        """Search knowledge base semantically."""
        return self.search_tool.search(content=query, filters=filters)

    def search_pages(self, content: str = None, filters: Dict = None) -> List[Dict]:
        """
        Search Confluence pages in the knowledge base.

        Args:
            content: Search content query
            filters: Metadata filters (e.g., {'status': 'current'})

        Returns:
            List of matching pages
        """
        return self.search_tool.search(content=content, filters=filters)

    def query_pages(
        self, filters: Dict = None, as_models: bool = False
    ) -> List[Union[Dict, ConfluencePage]]:
        """
        Query Confluence pages from the datasource with filters.

        Args:
            filters: Filters to apply (e.g., {'spaceKey': 'SOP', 'status': 'current'})
            as_models: If True, return ConfluencePage objects instead of dicts

        Returns:
            List of matching pages
        """
        results = self.search_tool.query_raw_data(
            datasource="confluence_datasource", table="pages", filters=filters
        )

        if as_models:
            return [ConfluencePage(**row) for row in results]
        return results

    def refresh_data(self) -> None:
        """Refresh Confluence data from source."""
        query = "REFRESH confluence_datasource"
        self.server.query(query)
        print("✓ Refreshed Confluence datasource")

    def get_recent_pages(
        self, days: int = 7, as_models: bool = False
    ) -> List[Union[Dict, ConfluencePage]]:
        """Get recently updated pages."""
        query = f"""
        SELECT * FROM confluence_datasource.pages
        WHERE version_createdAt >= NOW() - INTERVAL '{days}' DAY
        ORDER BY version_createdAt DESC
        """
        results = self.server.query(query).fetch()

        if as_models:
            return [ConfluencePage(**row) for row in results]
        return results

    def insert_data(self) -> None:
        """Insert Confluence data into knowledge base."""
        try:
            confluence_kb = self.server.knowledge_bases.get("confluence_kb")
            confluence_kb.insert_query(
                self.server.databases.confluence_datasource.tables.pages
            )
            print("✓ Inserted data into confluence_kb")
        except Exception as e:
            print(f"Error inserting data: {e}")
