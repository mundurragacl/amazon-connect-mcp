# Amazon Connect MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.x-green.svg)](https://gofastmcp.com)

An MCP (Model Context Protocol) server that enables AI assistants to interact with Amazon Connect contact centers. Built with FastMCP and boto3.

## Features

- **88 Tools** covering all major Amazon Connect services
- **91 Configuration Templates** - Industry-specific templates for cases, views, routing, and more
- **Multi-Region Support** - List instances across all AWS regions
- **Setup Wizard** - Guided setup for new Connect instances
- **Infrastructure as Code** - Generate CloudFormation templates

### Tool Categories

| Category | Tools | Description |
|----------|-------|-------------|
| **Core** | 9 | Instance management, metrics, contacts, cases |
| **Cases** | 17 | Case templates, fields, layouts, domains |
| **Contacts** | 8 | Voice, chat, tasks, transfers, recording |
| **Config** | 17 | Flows, queues, routing profiles, users |
| **Analytics** | 5 | Metrics, evaluations, performance |
| **Profiles** | 9 | Customer profile management |
| **Campaigns** | 10 | Outbound campaign management |
| **AI** | 8 | Amazon Q in Connect integration |
| **Templates** | 3 | Template management |
| **Wizard** | 2 | Setup wizard and IaC generation |

### Template Categories

| Category | Count | Description |
|----------|-------|-------------|
| **Cases** | 20 | Industry-specific case templates and layouts |
| **Views** | 15 | Agent workspace screen pops and disposition forms |
| **Data Tables** | 8 | Routing rules, SLAs, outage status, schedules |
| **Routing** | 15 | Hours of operation, queues, agent profiles |
| **Evaluation Forms** | 6 | Quality management scoring templates |
| **Contact Flows** | 15 | Industry-specific IVR and routing flows |
| **Step-by-Step Guides** | 6 | Agent workflow templates |
| **Customer Profiles** | 5 | Unified customer view layouts |
| **IaC** | 1 | CloudFormation templates |

## Prerequisites

### AWS CLI & Credentials

1. Install the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

2. Configure your credentials:
```bash
# If you don't have a profile yet, create one
aws configure --profile my-connect-profile

# You'll be prompted for:
# - AWS Access Key ID
# - AWS Secret Access Key  
# - Default region (e.g., us-east-1)
# - Output format (json)
```

3. Verify your setup:
```bash
# List available profiles
aws configure list-profiles

# Test connectivity
aws sts get-caller-identity --profile my-connect-profile
```

Your profile needs IAM permissions for Amazon Connect. See [Amazon Connect required permissions](https://docs.aws.amazon.com/connect/latest/adminguide/security-iam.html).

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/mundurragacl/amazon-connect-mcp.git
cd amazon-connect-mcp

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install
pip install -e .
```

### Running the Server

```bash
# Local (stdio) - for Claude Desktop, Cursor, etc.
fastmcp run src/amazon_connect_mcp/server.py

# Or as a module
python -m amazon_connect_mcp.server
```

### Cursor

[![Install MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](cursor://anysphere.cursor-deeplink/mcp/install?name=amazon-connect&config=eyJjb21tYW5kIjoicHl0aG9uIiwiYXJncyI6WyItbSIsImFtYXpvbl9jb25uZWN0X21jcC5zZXJ2ZXIiXSwiZW52Ijp7IkFXU19QUk9GSUxFIjoieW91ci1wcm9maWxlIn19)

Or manually add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "amazon-connect": {
      "command": "python",
      "args": ["-m", "amazon_connect_mcp.server"],
      "env": {
        "AWS_PROFILE": "your-profile"
      }
    }
  }
}
```

### Kiro CLI

Add to `.kiro/settings/mcp.json` (workspace) or `~/.kiro/settings/mcp.json` (global):

```json
{
  "mcpServers": {
    "amazon-connect": {
      "command": "python",
      "args": ["-m", "amazon_connect_mcp.server"],
      "env": {
        "AWS_PROFILE": "your-profile"
      }
    }
  }
}
```

**For macOS with virtual environment**, use the full path approach:

```json
{
  "mcpServers": {
    "amazon-connect": {
      "command": "sh",
      "args": ["-c", "cd /path/to/amazon-connect-mcp && source .venv/bin/activate && python -m amazon_connect_mcp.server"],
      "env": {
        "AWS_PROFILE": "your-profile"
      }
    }
  }
}
```

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

**Recommended (macOS/Linux):**
```json
{
  "mcpServers": {
    "amazon-connect": {
      "command": "/path/to/amazon-connect-mcp/.venv/bin/amazon-connect-mcp",
      "env": {
        "AWS_PROFILE": "your-profile"
      }
    }
  }
}
```

**Alternative (if above doesn't work):**
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

### Cases Templates (Industry-Specific)
| Industry | Template | Key Fields |
|----------|----------|------------|
| General | `general_support` | Standard support case |
| General | `billing_inquiry` | Billing-specific with conditional fields |
| General | `technical_support` | Technical support with severity levels |
| Healthcare | `healthcare_support` | Patient ID, insurance, appointments |
| Financial Services | `financial_services` | Account, transactions, disputes |
| Insurance | `insurance_claims` | Policy, claims, adjusters |
| E-Commerce/Retail | `ecommerce_support` | Orders, returns, shipping |
| Telecommunications | `telecom_support` | Service, devices, outages |
| Travel/Hospitality | `travel_hospitality` | Reservations, loyalty, refunds |
| Technology/SaaS | `technology_support` | Products, bugs, integrations |
| Utilities | `utilities_support` | Service address, meters, outages |

### Cases Layouts
- `general_support_layout` - Standard Z-formation layout
- `healthcare_layout` - Patient-focused layout
- `financial_services_layout` - Account and transaction layout
- `retail_ecommerce_layout` - Order and shipping layout
- `insurance_claims_layout` - Policy and claims layout
- `telecom_layout` - Service and device layout
- `travel_hospitality_layout` - Reservation and booking layout
- `technology_layout` - Product and issue layout
- `utilities_layout` - Service address and meter layout

### Agent Views (Industry-Specific)
| Type | Template | Description |
|------|----------|-------------|
| Screen Pop | `screen_pop` | Generic customer info display |
| Screen Pop | `healthcare_screen_pop` | Patient info with HIPAA compliance |
| Screen Pop | `financial_screen_pop` | Account overview with fraud alerts |
| Screen Pop | `ecommerce_screen_pop` | Order and shipping details |
| Screen Pop | `telecom_screen_pop` | Service and device info |
| Screen Pop | `insurance_screen_pop` | Policy and claims overview |
| Screen Pop | `travel_screen_pop` | Reservation details |
| Screen Pop | `technology_screen_pop` | Product and subscription info |
| Screen Pop | `utilities_screen_pop` | Service account with outage alerts |
| Disposition | `call_disposition` | Generic after-call work form |
| Disposition | `healthcare_disposition` | Healthcare-specific disposition |
| Disposition | `ecommerce_disposition` | E-commerce disposition with refunds |
| Disposition | `financial_disposition` | Financial services disposition |
| Form | `case_creation_form` | Case creation form |
| Selection | `topic_selection` | Contact reason selection cards |

### Data Tables
| Template | Description |
|----------|-------------|
| `holiday_schedule` | Holiday closures with custom messages |
| `emergency_routing` | Emergency routing overrides |
| `sla_configuration` | SLA rules by customer tier |
| `skill_routing_rules` | Skill-based routing configuration |
| `geographic_routing` | Location-based routing rules |
| `outage_status` | Real-time outage and incident tracking |
| `healthcare_provider_directory` | Healthcare department routing |
| `product_support_matrix` | Product-specific support routing |

### Routing Templates
**Hours of Operation:**
- `business_hours` - M-F 8am-5pm
- `24x7` - 24/7 operation
- `healthcare_hours` - Healthcare with on-call support
- `financial_services_hours` - Extended hours with 24/7 fraud line
- `ecommerce_hours` - Extended hours with peak season config
- `utilities_24x7` - 24/7 with emergency prioritization

**Queue Configurations:**
- `general_support` - Standard queue config
- `healthcare_queues` - Healthcare department queues
- `financial_queues` - Banking queues with fraud priority
- `ecommerce_queues` - Retail queues with VIP support
- `telecom_queues` - Telecom service queues

**Agent Routing Profiles:**
- `support_agent` - General support agent profile
- `healthcare_profiles` - Healthcare agent profiles
- `financial_profiles` - Financial services profiles
- `ecommerce_profiles` - E-commerce agent profiles

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
