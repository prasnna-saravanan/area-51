# Contributing to Area51

Welcome to Area51. We're excited you're interested in contributing to our unified enterprise knowledge search platform. This guide will help you get started, whether you're a first-time contributor or an experienced open-source developer.

## Hacktoberfest Contributors

Welcome, Hacktoberfest participants. Area51 is proud to participate in Hacktoberfest. Here's what you need to know:

- **Quality over quantity**: We value thoughtful, well-tested contributions over quick fixes
- **Valid contributions**: Bug fixes, features, documentation improvements, tests, and performance optimizations are all welcome
- **Communication**: Comment on issues before starting work to avoid duplicate efforts
- **PR labels**: Maintainers will add `hacktoberfest-accepted` labels to approved PRs

**Looking for Hacktoberfest issues?** Check out issues labeled with:
- `good-first-issue` - Perfect for first-time contributors
- `hacktoberfest` - Specifically marked for Hacktoberfest
- `help-wanted` - We'd especially appreciate help here
- `documentation` - Improve our docs and help others

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Types of Contributions](#types-of-contributions)
- [Pull Request Process](#pull-request-process)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. All contributors are expected to:

- Be respectful and considerate in all interactions
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what's best for the community and project
- Show empathy towards other contributors

Unacceptable behavior includes harassment, trolling, insulting comments, personal attacks, or any form of discrimination. Violations may result in removal from the project.

## Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed
- **Docker and Docker Compose** for running MindsDB and PostgreSQL
- **Git** for version control
- **uv** package manager (recommended) or pip
- **API Credentials** for testing (optional for documentation-only contributions):
  - Azure OpenAI API key
  - Zendesk API credentials
  - Jira API credentials
  - Confluence API credentials

### Setting Up Your Development Environment

1. **Fork the repository**
   
   Click the "Fork" button at the top right of the repository page on GitHub.

2. **Clone your fork**

   ```bash
   git clone https://github.com/YOUR-USERNAME/area51.git
   cd area51
   ```

3. **Add upstream remote**

   ```bash
   git remote add upstream https://github.com/ORIGINAL-OWNER/area51.git
   ```

4. **Install dependencies**

   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -e .
   ```

5. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your API credentials
   ```

6. **Start the infrastructure**

   ```bash
   docker-compose up -d
   ```

7. **Run the setup script**

   ```bash
   uv run python setup.py --mode setup
   ```

8. **Verify installation**

   ```bash
   # Open MindsDB Studio
   open http://localhost:47334
   
   # Run tests
   uv run python -m pytest tests/
   ```

### Understanding the Codebase

```
area51/
├── agent.py                 # LangGraph conversational agent
├── server.py                # MCP server for AI assistants
├── server_langgraph.py      # LangGraph server implementation
├── setup.py                 # Automated setup and configuration
├── integrations/            # Platform API clients
│   ├── zendesk_client.py   # Zendesk API integration
│   ├── jira_client.py      # Jira API integration
│   └── confluence_client.py # Confluence API integration
├── models/                  # Data models and schemas
├── tools/                   # Search and analysis tools
├── utils/                   # Setup and utility scripts
└── tests/                   # Test suite
```

**Key files to understand:**
- `agent.py` - Main LangGraph agent with routing logic
- `tools/search.py` - Core search functionality across knowledge bases
- `integrations/` - API clients for external platforms
- `utils/setup_*.py` - Setup scripts for datasources, knowledge bases, and jobs

## Development Workflow

### Creating a Branch

Always create a new branch for your changes:

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create a feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions or improvements
- `perf/` - Performance improvements

### Making Changes

1. **Write clean, readable code** following our [code standards](#code-standards)
2. **Add tests** for new functionality
3. **Update documentation** if you change APIs or behavior
4. **Test your changes** locally before committing
5. **Keep commits focused** - one logical change per commit

### Commit Message Guidelines

We follow conventional commit messages for clarity and automated changelog generation:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(search): add hybrid search support for Confluence KB

Implemented hybrid search combining semantic and keyword-based 
search with configurable alpha parameter.

Closes #123
```

```
fix(jira): handle pagination for large issue lists

Fixed bug where only first 50 issues were indexed. Now properly
handles pagination through all results.

Fixes #456
```

```
docs(readme): update MCP server configuration examples

Added examples for both Cursor and Claude Desktop, clarified
environment variable requirements.
```

### Syncing Your Fork

Keep your fork up to date with upstream changes:

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## Types of Contributions

We welcome many types of contributions:

### Bug Reports

Found a bug? Please create an issue with:

- **Clear title** - Summarize the bug in one line
- **Steps to reproduce** - Detailed steps to recreate the issue
- **Expected behavior** - What should happen
- **Actual behavior** - What actually happens
- **Environment** - OS, Python version, relevant package versions
- **Logs/screenshots** - Any relevant error messages or images

**Use the bug report template** when creating issues.

### Feature Requests

Have an idea for a new feature?

- **Check existing issues** to avoid duplicates
- **Explain the use case** - Why is this feature needed?
- **Describe the solution** - How do you envision it working?
- **Consider alternatives** - What other approaches could work?

**Use the feature request template** when creating issues.

### Code Contributions

Areas where we especially welcome contributions:

1. **New integrations** - Add support for more platforms (GitHub Issues, Linear, etc.)
2. **Search improvements** - Better ranking, filtering, or query understanding
3. **Agent enhancements** - Improve routing logic or add new capabilities
4. **Performance optimizations** - Make searches faster or reduce resource usage
5. **Error handling** - Better error messages and recovery
6. **Testing** - Increase test coverage or add integration tests
7. **Developer experience** - Better logging, debugging tools, or setup scripts

### Documentation

Documentation is crucial! We welcome:

- **Tutorial improvements** - Make getting started easier
- **API documentation** - Document functions, classes, and modules
- **Architecture guides** - Explain how components work together
- **Use case examples** - Real-world usage scenarios
- **Troubleshooting guides** - Common issues and solutions
- **Translations** - Help non-English speakers (future)

### Testing

Help improve our test coverage:

- **Unit tests** - Test individual functions and classes
- **Integration tests** - Test component interactions
- **End-to-end tests** - Test complete workflows
- **Performance tests** - Benchmark search performance
- **Test data** - Provide realistic test datasets

## Pull Request Process

### Before Submitting

- [ ] Code follows our [style guidelines](#code-standards)
- [ ] Tests pass locally (`uv run python -m pytest`)
- [ ] New tests cover your changes
- [ ] Documentation updated (if needed)
- [ ] Commit messages follow conventions
- [ ] Branch is up to date with main
- [ ] No merge conflicts

### Submitting Your PR

1. **Push your branch** to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a pull request** on GitHub
   - Use a clear, descriptive title
   - Fill out the PR template completely
   - Link related issues using "Closes #123" or "Fixes #456"
   - Add screenshots/videos for UI changes
   - Explain why the change is needed
   - Describe how you tested it

3. **Respond to feedback**
   - Address reviewer comments promptly
   - Push additional commits if needed
   - Update the PR description if scope changes
   - Be open to suggestions and alternative approaches

4. **PR Review Process**
   - At least one maintainer approval required
   - All CI checks must pass
   - No merge conflicts
   - Conversations resolved
   - Maintainers may request changes or suggest improvements

### After Your PR is Merged

- Delete your feature branch (optional but recommended)
- Sync your fork with upstream
- You've successfully contributed to Area51

## Code Standards

### Python Style Guide

We follow **PEP 8** with some modifications. Use the provided linting tools:

```bash
# Format code with black
uv run black .

# Check with ruff
uv run ruff check .
```

### Code Quality Guidelines

1. **Write readable code**
   - Use descriptive variable and function names
   - Add comments for complex logic
   - Keep functions focused and small (< 50 lines when possible)
   - Avoid deep nesting (max 3-4 levels)

2. **Type hints**
   - Use type hints for function signatures
   - Use Pydantic models for data structures
   - Example:
     ```python
     from typing import List, Optional
     from pydantic import BaseModel
     
     def search_knowledge_base(
         query: str, 
         kb_name: str, 
         limit: int = 10
     ) -> List[dict]:
         """Search a knowledge base with semantic search."""
         pass
     ```

3. **Error handling**
   - Use specific exceptions, not bare `except:`
   - Provide helpful error messages
   - Log errors appropriately
   - Example:
     ```python
     from tenacity import retry, stop_after_attempt
     
     @retry(stop=stop_after_attempt(3))
     def api_call_with_retry():
         try:
             response = make_api_call()
             response.raise_for_status()
             return response.json()
         except requests.HTTPError as e:
             logger.error(f"API call failed: {e}")
             raise
     ```

4. **Documentation**
   - Write docstrings for all public functions/classes
   - Use Google-style docstrings
   - Example:
     ```python
     def search_jira(query: str, limit: int = 10) -> List[dict]:
         """Search Jira issues using semantic search.
         
         Args:
             query: Natural language search query
             limit: Maximum number of results to return
             
         Returns:
             List of matching Jira issues with metadata
             
         Raises:
             MindsDBError: If the knowledge base is not available
             ValueError: If query is empty or limit is invalid
         """
         pass
     ```

5. **Constants and configuration**
   - Use ALL_CAPS for constants
   - Store configuration in environment variables
   - Use `.env` for local development
   - Example:
     ```python
     import os
     from dotenv import load_dotenv
     
     load_dotenv()
     
     MINDSDB_URL = os.getenv("MINDSDB_URL", "http://localhost:47334")
     MAX_SEARCH_RESULTS = 50
     ```

### Code Review Checklist

When reviewing code (or preparing your PR), check for:

- [ ] Code is readable and well-organized
- [ ] Functions have clear purposes
- [ ] Type hints are present
- [ ] Error handling is appropriate
- [ ] No hardcoded credentials or secrets
- [ ] Logging is appropriate (not too verbose, not too quiet)
- [ ] Tests cover the changes
- [ ] Documentation is updated
- [ ] No unnecessary dependencies added

## Testing Guidelines

### Running Tests

```bash
# Run all tests
uv run python -m pytest

# Run specific test file
uv run python -m pytest tests/test_hybrid_search.py

# Run with coverage
uv run python -m pytest --cov=integrations --cov=tools --cov=models

# Run with verbose output
uv run python -m pytest -v
```

### Writing Tests

1. **Location**: Place tests in the `tests/` directory
2. **Naming**: Test files should be named `test_*.py`
3. **Structure**: Use clear test function names

```python
import pytest
from tools.search import search_confluence

def test_search_confluence_returns_results():
    """Test that Confluence search returns results for valid query."""
    results = search_confluence("docker deployment", limit=5)
    
    assert isinstance(results, list)
    assert len(results) <= 5
    assert all("title" in r for r in results)

def test_search_confluence_handles_empty_query():
    """Test that empty query raises appropriate error."""
    with pytest.raises(ValueError, match="Query cannot be empty"):
        search_confluence("", limit=5)

def test_search_confluence_respects_limit():
    """Test that limit parameter is respected."""
    results = search_confluence("authentication", limit=3)
    assert len(results) <= 3
```

### Test Coverage Goals

- **Minimum**: 70% coverage for new code
- **Target**: 80%+ coverage overall
- Focus on:
  - Core search functionality
  - API integrations
  - Error handling paths
  - Edge cases

### Integration Tests

For integration tests that require MindsDB:

```python
import pytest
import mindsdb_sdk

@pytest.fixture
def mindsdb_client():
    """Provide MindsDB client for tests."""
    server = mindsdb_sdk.connect("http://localhost:47334")
    yield server

def test_knowledge_base_search(mindsdb_client):
    """Test real knowledge base search."""
    query = "SELECT * FROM confluence_kb WHERE content='docker' LIMIT 5"
    result = mindsdb_client.query(query)
    
    assert result is not None
    assert len(result) <= 5
```

## Documentation

### Documentation Standards

1. **README.md**: Keep up to date with setup instructions and examples
2. **Code comments**: Explain "why" not "what"
3. **Docstrings**: Document all public APIs
4. **Architecture docs**: Explain major components and design decisions
5. **CHANGELOG.md**: Document user-facing changes (maintainers handle this)

### Documentation Style

- Use clear, simple language
- Provide code examples
- Include screenshots for visual features
- Test all code examples before committing
- Link to related documentation

### What to Document

When adding features, update:
- README.md (if user-facing)
- Function/class docstrings
- Architecture docs (for major changes)
- QUICKSTART.md (if setup changes)
- API documentation (if applicable)

## Community

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Pull Request Comments**: For code review discussions

### Communication Guidelines

- **Be respectful**: Treat everyone with respect and kindness
- **Be patient**: Maintainers are volunteers with other commitments
- **Be clear**: Provide enough context in your questions
- **Search first**: Check existing issues and docs before asking
- **Give back**: Help answer questions from other contributors

### Recognition

We value all contributors! Contributors will be:
- Listed in CONTRIBUTORS.md (future)
- Mentioned in release notes for significant contributions
- Acknowledged in the repository

## Issue Labels

Understanding our labels helps you find issues to work on:

- `good-first-issue` - Great for newcomers
- `help-wanted` - We'd especially appreciate help
- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Documentation improvements
- `performance` - Performance optimization
- `testing` - Test-related
- `hacktoberfest` - Suitable for Hacktoberfest
- `priority:high` - High priority issue
- `priority:medium` - Medium priority
- `priority:low` - Low priority
- `wontfix` - This won't be addressed
- `duplicate` - Duplicate of another issue

## Maintainer Notes

For maintainers reviewing PRs:

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass and coverage is adequate
- [ ] Documentation is updated
- [ ] No security issues (secrets, injection risks)
- [ ] Performance impact is acceptable
- [ ] Breaking changes are documented
- [ ] Commit messages follow conventions

### Merging PRs

1. Ensure all checks pass
2. Resolve any conflicts
3. Squash commits if needed
4. Add appropriate labels
5. Update CHANGELOG.md if needed
6. Merge using "Squash and merge" for most PRs

### Hacktoberfest PRs

For Hacktoberfest PRs:
- Review within 48 hours if possible
- Add `hacktoberfest-accepted` label for quality contributions
- Add `invalid` label for spam/low-quality PRs
- Be extra welcoming to first-time contributors

## Thank You

Thank you for contributing to Area51. Every contribution, no matter how small, helps make this project better for everyone.

---

**Questions?** Feel free to open a discussion or comment on an issue. We're here to help!

**Ready to contribute?** Check out our [good first issues](https://github.com/OWNER/area51/labels/good-first-issue) to get started!

