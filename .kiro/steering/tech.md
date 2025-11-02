# Technology Stack

## Core Technologies

- **Python 3.12+**: Primary language
- **FastMCP 2.x**: MCP server framework
- **boto3**: AWS SDK for Python
- **Pydantic**: Data validation and settings management
- **Pydantic Settings**: Configuration management

## Build System

- **Build Backend**: Hatchling
- **Package Manager**: pip
- **Virtual Environment**: Python venv

## Development Dependencies

- **pytest**: Testing framework
- **ruff**: Linting and formatting
- **mypy**: Type checking (mentioned in README)

## Common Commands

### Setup
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install package in development mode
pip install -e .

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running
```bash
# Run as FastMCP server (stdio mode)
fastmcp run src/amazon_connect_mcp/server.py

# Run as Python module
python -m amazon_connect_mcp.server
```

### Development
```bash
# Run tests
pytest

# Type checking
mypy src/

# Linting (implied from dev dependencies)
ruff check src/
```

## AWS Configuration

Requires AWS CLI configuration with appropriate profiles and IAM permissions for Amazon Connect services. Uses environment variables with `CONNECT_MCP_` prefix for configuration.