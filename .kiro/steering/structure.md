# Project Structure

## Root Directory Layout

```
├── src/amazon_connect_mcp/          # Main package
├── docs/                            # Documentation
├── .kiro/                          # Kiro IDE configuration
├── .github/                        # GitHub workflows
├── pyproject.toml                  # Project configuration
└── README.md                       # Main documentation
```

## Package Structure

```
src/amazon_connect_mcp/
├── __init__.py                     # Package initialization
├── server.py                       # Main MCP server entry point
├── config.py                       # Settings and configuration
├── aws_clients.py                  # AWS client management
├── tools/                          # MCP tool implementations
│   ├── __init__.py
│   ├── core.py                     # Tier 1 core tools
│   ├── cases.py                    # Case management tools
│   ├── contacts.py                 # Contact handling tools
│   ├── config.py                   # Configuration tools
│   ├── analytics.py                # Analytics and metrics
│   ├── profiles.py                 # Customer profiles
│   ├── campaigns.py                # Outbound campaigns
│   ├── ai.py                       # Amazon Q integration
│   └── wizard.py                   # Setup wizard tools
└── templates/                      # Configuration templates
    ├── __init__.py
    ├── loader.py                   # Template loading utilities
    ├── cases/                      # Case templates
    ├── views/                      # Agent view templates
    ├── data_tables/                # Data table templates
    ├── routing/                    # Routing templates
    └── iac/                        # Infrastructure as Code
        └── cloudformation/         # CloudFormation templates
```

## Architecture Patterns

### Tool Organization
- **Tier 1 (core.py)**: Essential tools always loaded first
- **Tier 2 (domain modules)**: Specialized tools loaded by domain
- **Wizard & Templates**: Setup and configuration utilities

### Client Management
- Centralized AWS client creation in `aws_clients.py`
- LRU caching for client instances
- Region-aware client management

### Configuration
- Pydantic-based settings with environment variable support
- `CONNECT_MCP_` prefix for environment variables
- Default values for common settings

### Template System
- JSON/YAML template files organized by category
- Dynamic template loading and customization
- Support for CloudFormation intrinsic functions

## Naming Conventions

- **Tool Functions**: `{domain}_{action}` (e.g., `cases_create_template`)
- **Files**: Snake case (e.g., `aws_clients.py`)
- **Classes**: PascalCase (e.g., `Settings`)
- **Constants**: UPPER_SNAKE_CASE