"""Tools for semantic search and analysis."""

from typing import Dict, List, Optional

import mindsdb_sdk


class SemanticSearchTool:
    """Generic search tool for MindsDB knowledge bases."""

    def __init__(self, kb_name: str = "confluence_kb"):
        """
        Initialize the search tool.

        Args:
            kb_name: Name of the knowledge base to search
        """
        self.server = mindsdb_sdk.connect()
        self.kb_name = kb_name

    def search(
        self, content: str = None, filters: Dict = None, top_k: int = 5
    ) -> List[Dict]:
        """
        Search knowledge base semantically.

        Args:
            content: Search content query
            filters: Metadata filters (e.g., {'status': 'current'})
            top_k: Maximum number of results to return

        Returns:
            List of matching documents
        """
        query = f"SELECT * FROM {self.kb_name}"
        conditions = []

        if content:
            conditions.append(f"content = '{content}'")

        if filters:
            for key, value in filters.items():
                conditions.append(f"{key} = '{value}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        results = self.server.query(query).fetch()

        # Return top_k results
        return results[:top_k] if results else []

    def search_by_meta(self, filters: Dict, top_k: int = 5) -> List[Dict]:
        """
        Search by metadata filters only.

        Args:
            filters: Dictionary of metadata filters
            top_k: Maximum number of results to return

        Returns:
            List of matching documents
        """
        return self.search(content=None, filters=filters, top_k=top_k)

    def query_raw_data(
        self, datasource: str, table: str, filters: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Query raw data from a datasource (not from KB).

        Args:
            datasource: Datasource name (e.g., 'confluence_datasource')
            table: Table name (e.g., 'pages')
            filters: Filters to apply

        Returns:
            List of matching records
        """
        table_obj = self.server.databases[datasource].tables[table]

        if filters:
            df = table_obj.filter(**filters).fetch()
        else:
            df = table_obj.fetch()

        return df.to_dict(orient="records") if hasattr(df, "to_dict") else df

    def refresh_kb(self, datasource: str, table: str) -> None:
        """
        Refresh datasource and update knowledge base.

        Args:
            datasource: Datasource name to refresh
            table: Table name to insert into KB
        """
        # Refresh the datasource
        query = f"REFRESH {datasource}"
        self.server.query(query)
        print(f"✓ Refreshed {datasource}")

        # Update KB
        try:
            kb = self.server.knowledge_bases.get(self.kb_name)
            kb.insert_query(self.server.databases[datasource].tables[table])
            print(f"✓ Updated {self.kb_name}")
        except Exception as e:
            print(f"Error updating KB: {e}")
