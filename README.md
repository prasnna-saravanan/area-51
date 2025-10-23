# Area51 - Zendesk + JIRA + Confluence Integration

Semantic search and recommendation system for support tickets, JIRA issues, and documentation.

## Use Cases

- **Reply Recommendation**: Recommend macros/snippets based on semantic similarity
- **Bug Detection**: Check if Zendesk tickets correlate to recent JIRA releases
- **Doc Recommendations**: Suggest documentation updates based on ticket patterns
- **SLA Monitoring**: Rank tickets likely to breach SLA
- **Escalation Tracking**: Identify merchants at risk of churn
- **Doc Updates**: Get suggestions for technical documentation improvements

## Structure

```
├── tools/              # Search and analysis tools
├── integrations/       # Client integrations
│   ├── notion_client.py
│   ├── zendesk_client.py
│   └── jira_client.py
├── agent.py           # Main agent logic
├── mcp.py             # MCP server
└── pyproject.toml     # Dependencies
```

## Setup

```bash
uv sync
```

## Usage

```bash
uv run python agent.py
```

