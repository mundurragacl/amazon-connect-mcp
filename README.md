# Amazon Connect MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.x-green.svg)](https://gofastmcp.com)

An MCP (Model Context Protocol) server that enables AI assistants to interact with Amazon Connect contact centers. Built with FastMCP and boto3.

## Features

- **86 Tools** covering all major Amazon Connect services
- **Multi-Region Support** - List instances across all AWS regions
- **Configuration Templates** - Pre-built templates for cases, views, routing, and more
- **Setup Wizard** - Guided setup for new Connect instances
- **Infrastructure as Code** - Generate CloudFormation templates

### Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| **Core** | 9 | Instance management, metrics, contacts, cases |
| **Cases** | 16 | Case templates, fields, layouts, domains |
| **Contacts** | 8 | Voice, chat, tasks, transfers, recording |
| **Config** | 17 | Flows, queues, routing profiles, users |
| **Analytics** | 5 | Metrics, evaluations, performance |
| **Profiles** | 8 | Customer profile management |
| **Campaigns** | 10 | Outbound campaign management |
| **AI** | 8 | Amazon Q in Connect integration |
| **Templates** | 3 | Template management |
| **Wizard** | 2 | Setup wizard and IaC generation |

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/amazon-connect-mcp.git
cd amazon-connect-mcp

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install
pip install -e .
```

### Configuration

Set AWS credentials via environment or AWS profile:

```bash
export AWS_REGION=us-east-1
export AWS_PROFILE=your-profile  # optional
```

### Running the Server

```bash
# Local (stdio) - for Claude Desktop, Cursor, etc.
fastmcp run src/amazon_connect_mcp/server.py

# Or as a module
python -m amazon_connect_mcp.server
```

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "amazon-connect": {
      "command": "python",
      "args": ["-m", "amazon_connect_mcp.server"],
      "cwd": "/path/to/amazon-connect-mcp",
      "env": {
        "AWS_PROFILE": "your-profile"
      }
    }
  }
}
```

## Usage Examples

### List All Connect Instances

```python
# Lists instances across all AWS regions
list_instances()

# Filter by region
list_instances(region="us-west-2")
```

### Get Real-Time Metrics

```python
get_current_metrics(instance_id="your-instance-id")
```

### Create a Case

```python
create_case(
    domain_id="your-domain-id",
    template_id="your-template-id",
    fields={"title": "Customer Issue", "priority": "High"}
)
```

### Use Configuration Templates

```python
# List available templates
template_list()

# Get a specific template
template_get(category="cases", name="general_support")

# Customize a template
template_customize(
    category="cases",
    name="billing_inquiry",
    overrides={"name": "Custom Billing Template"}
)
```

### Setup Wizard

```python
# Start guided setup
wizard_start_setup(
    use_case="ai_enhanced",  # basic, cases_enabled, ai_enhanced, full_enterprise
    instance_name="my-contact-center",
    region="us-east-1"
)

# Generate CloudFormation template
wizard_get_iac_template(
    use_case="basic",
    instance_name="my-cc",
    region="us-east-1"
)
```

## Available Templates

### Cases
- `general_support` - Standard support case template
- `billing_inquiry` - Billing-specific with conditional fields
- `technical_support` - Technical support with severity levels

### Agent Views
- `screen_pop` - Incoming contact screen pop
- `case_creation_form` - Case creation form
- `topic_selection` - Contact reason selection cards
- `call_disposition` - After-call work form

### Data Tables
- `holiday_schedule` - Holiday closures with custom messages
- `emergency_routing` - Emergency routing overrides

### Routing
- `business_hours` - M-F 8am-5pm
- `24x7` - 24/7 operation
- `general_support` - Standard queue config
- `support_agent` - Agent routing profile

### Infrastructure as Code
- `basic_instance.yaml` - CloudFormation template for basic setup

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│           amazon-connect-mcp (86 Tools)                 │
│                                                         │
│  TIER 1 - Core (Always Available):                     │
│  ├── list_instances (multi-region)                     │
│  ├── describe_instance, list_queues                    │
│  ├── get_current_metrics, search_contacts              │
│  └── create_case, get_case, search_cases              │
│                                                         │
│  TIER 2 - Domain Tools:                                │
│  ├── cases_*      (16 tools)                           │
│  ├── contacts_*   (8 tools)                            │
│  ├── config_*     (17 tools)                           │
│  ├── analytics_*  (5 tools)                            │
│  ├── profiles_*   (8 tools)                            │
│  ├── campaigns_*  (10 tools)                           │
│  └── ai_*         (8 tools)                            │
│                                                         │
│  WIZARD & TEMPLATES:                                   │
│  ├── template_list, template_get, template_customize   │
│  └── wizard_start_setup, wizard_get_iac_template       │
└─────────────────────────────────────────────────────────┘
```

## Documentation

- [Amazon Connect API Features](docs/AMAZON_CONNECT_API_FEATURES.md)
- [MCP Architecture Best Practices](docs/MCP_ARCHITECTURE_BEST_PRACTICES.md)
- [Templates & Views Research](docs/TEMPLATES_AND_VIEWS_RESEARCH.md)
- [TODO: Templates Implementation](docs/TODO_TEMPLATES.md)

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy src/
```

## Requirements

- Python 3.12+
- AWS credentials with Amazon Connect permissions
- FastMCP 2.x
- boto3

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions welcome! Please read the contributing guidelines before submitting PRs.
