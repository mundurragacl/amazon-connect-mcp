# Amazon Connect MCP - Default Templates TODO

## Overview
This TODO list tracks the implementation of default templates and wizard functionality for the Amazon Connect MCP server. The goal is to enable users to quickly configure Amazon Connect instances with best-practice defaults.

---

## Phase 1: Core Template Definitions

### 1.1 Cases Templates
- [ ] **Create `templates/cases/general_support.json`**
  - Standard support case template
  - Fields: Title, Description, Priority, Status, Category
  - Layout with Top panel and More info sections

- [ ] **Create `templates/cases/billing_inquiry.json`**
  - Billing-specific case template
  - Fields: Account Number, Invoice ID, Amount, Issue Type
  - Conditional fields for refund requests

- [ ] **Create `templates/cases/technical_support.json`**
  - Technical support case template
  - Fields: Product, Version, Error Code, Steps to Reproduce
  - Priority escalation rules

- [ ] **Create `templates/cases/fields/standard_fields.json`**
  - Reusable field definitions
  - Priority (High/Medium/Low)
  - Category (Billing/Technical/General/Sales)
  - Resolution Status

### 1.2 Agent Views Templates
- [ ] **Create `templates/views/screen_pop.json`**
  - Detail view for incoming contact screen pop
  - Customer info, recent cases, account status

- [ ] **Create `templates/views/case_creation_form.json`**
  - Form view for creating new cases
  - Multi-section with validation

- [ ] **Create `templates/views/topic_selection.json`**
  - Cards view for agent topic selection
  - Common contact reasons

- [ ] **Create `templates/views/call_disposition.json`**
  - Form view for after-call work
  - Disposition codes, notes, follow-up

- [ ] **Create `templates/views/customer_lookup.json`**
  - Form + List view for customer search
  - Search by phone, email, account

### 1.3 Data Tables Templates
- [ ] **Create `templates/data_tables/holiday_schedule.json`**
  - Holiday closures with custom messages
  - Date, name, is_closed, message

- [ ] **Create `templates/data_tables/emergency_routing.json`**
  - Emergency flags for routing overrides
  - Queue, is_emergency, redirect_queue, message

- [ ] **Create `templates/data_tables/business_hours_override.json`**
  - Temporary hours changes
  - Date range, new hours, reason

- [ ] **Create `templates/data_tables/agent_extensions.json`**
  - Direct dial extensions
  - Extension, agent_id, department

### 1.4 Routing Templates
- [ ] **Create `templates/routing/hours_of_operation/business_hours.json`**
  - M-F 8am-5pm standard hours

- [ ] **Create `templates/routing/hours_of_operation/24x7.json`**
  - 24/7 operation hours

- [ ] **Create `templates/routing/hours_of_operation/extended_hours.json`**
  - M-F 7am-9pm, Sat 9am-5pm

- [ ] **Create `templates/routing/queues/general_support.json`**
  - Standard support queue config

- [ ] **Create `templates/routing/queues/sales.json`**
  - Sales queue with priority routing

- [ ] **Create `templates/routing/queues/technical.json`**
  - Technical support queue

- [ ] **Create `templates/routing/profiles/support_agent.json`**
  - Voice + Chat + Task concurrency

- [ ] **Create `templates/routing/profiles/sales_agent.json`**
  - Voice-focused with outbound

### 1.5 Customer Profiles Templates
- [ ] **Create `templates/profiles/standard_customer.json`**
  - Basic customer profile mapping
  - Name, contact info, account

- [ ] **Create `templates/profiles/order_history.json`**
  - Order object type mapping
  - Order ID, date, amount, status

### 1.6 AI Configuration Templates
- [ ] **Create `templates/ai/prompts/answer_generation.yaml`**
  - Custom answer generation prompt
  - Tone, format, guardrails

- [ ] **Create `templates/ai/prompts/intent_detection.yaml`**
  - Intent labeling prompt
  - Categories, confidence thresholds

- [ ] **Create `templates/ai/guardrails/standard.json`**
  - PII redaction rules
  - Content filters
  - Hallucination limits

- [ ] **Create `templates/ai/agents/support_assistant.json`**
  - AI agent for support use case
  - Linked prompts and guardrails

### 1.7 Outbound Campaign Templates
- [ ] **Create `templates/campaigns/appointment_reminder.json`**
  - Agentless appointment reminders
  - IVR flow, timing, retry logic

- [ ] **Create `templates/campaigns/survey_outreach.json`**
  - Post-contact survey campaign
  - Progressive dialer config

- [ ] **Create `templates/campaigns/collections.json`**
  - Collections campaign
  - Predictive dialer, AMD config

---

## Phase 2: MCP Wizard Tools

### 2.1 Setup Wizard Tools
- [ ] **Add `wizard_start_setup` tool**
  - Initialize wizard session
  - Collect instance requirements
  - Return setup options

- [ ] **Add `wizard_configure_basics` tool**
  - Set instance alias, region
  - Enable channels (voice/chat/task/email)
  - Configure basic settings

- [ ] **Add `wizard_configure_cases` tool**
  - Enable Cases domain
  - Select/customize case templates
  - Create fields and layouts

- [ ] **Add `wizard_configure_routing` tool**
  - Set hours of operation
  - Create queues
  - Configure routing profiles

- [ ] **Add `wizard_configure_ai` tool**
  - Enable Amazon Q in Connect
  - Configure knowledge base
  - Set up AI prompts/guardrails

- [ ] **Add `wizard_configure_views` tool**
  - Select agent workspace views
  - Configure step-by-step guides
  - Set up data tables

- [ ] **Add `wizard_deploy` tool**
  - Generate CloudFormation/SAM template
  - Validate configuration
  - Deploy to AWS

### 2.2 Template Management Tools
- [ ] **Add `template_list` tool**
  - List available templates by category
  - Show template metadata

- [ ] **Add `template_get` tool**
  - Retrieve template content
  - Support customization parameters

- [ ] **Add `template_customize` tool**
  - Modify template values
  - Validate against schema

- [ ] **Add `template_apply` tool**
  - Apply template to Connect instance
  - Handle dependencies

### 2.3 IaC Generation Tools
- [ ] **Add `iac_generate_cloudformation` tool**
  - Generate CFN template from config
  - Include all resources

- [ ] **Add `iac_generate_sam` tool**
  - Generate SAM template
  - Include Lambda functions

- [ ] **Add `iac_validate` tool**
  - Validate generated templates
  - Check resource dependencies

- [ ] **Add `iac_deploy` tool**
  - Deploy via CloudFormation/SAM
  - Track deployment status

---

## Phase 3: Template Directory Structure

```
src/amazon_connect_mcp/
├── templates/
│   ├── __init__.py
│   ├── loader.py              # Template loading utilities
│   ├── validator.py           # Schema validation
│   ├── cases/
│   │   ├── general_support.json
│   │   ├── billing_inquiry.json
│   │   ├── technical_support.json
│   │   └── fields/
│   │       └── standard_fields.json
│   ├── views/
│   │   ├── screen_pop.json
│   │   ├── case_creation_form.json
│   │   ├── topic_selection.json
│   │   ├── call_disposition.json
│   │   └── customer_lookup.json
│   ├── data_tables/
│   │   ├── holiday_schedule.json
│   │   ├── emergency_routing.json
│   │   ├── business_hours_override.json
│   │   └── agent_extensions.json
│   ├── routing/
│   │   ├── hours_of_operation/
│   │   │   ├── business_hours.json
│   │   │   ├── 24x7.json
│   │   │   └── extended_hours.json
│   │   ├── queues/
│   │   │   ├── general_support.json
│   │   │   ├── sales.json
│   │   │   └── technical.json
│   │   └── profiles/
│   │       ├── support_agent.json
│   │       └── sales_agent.json
│   ├── profiles/
│   │   ├── standard_customer.json
│   │   └── order_history.json
│   ├── ai/
│   │   ├── prompts/
│   │   │   ├── answer_generation.yaml
│   │   │   └── intent_detection.yaml
│   │   ├── guardrails/
│   │   │   └── standard.json
│   │   └── agents/
│   │       └── support_assistant.json
│   ├── campaigns/
│   │   ├── appointment_reminder.json
│   │   ├── survey_outreach.json
│   │   └── collections.json
│   └── iac/
│       ├── cloudformation/
│       │   ├── basic_instance.yaml
│       │   ├── cases_enabled.yaml
│       │   ├── ai_enhanced.yaml
│       │   └── full_enterprise.yaml
│       └── sam/
│           └── connect_with_lambda.yaml
└── tools/
    ├── wizard.py              # Wizard tools
    └── templates.py           # Template management tools
```

---

## Phase 4: Implementation Priority

### High Priority (Week 1-2)
1. [ ] Create template directory structure
2. [ ] Implement template loader
3. [ ] Create 3 core case templates
4. [ ] Create 3 core view templates
5. [ ] Add `template_list` and `template_get` tools

### Medium Priority (Week 3-4)
6. [ ] Create routing templates
7. [ ] Create data table templates
8. [ ] Add wizard start/configure tools
9. [ ] Implement template customization

### Lower Priority (Week 5-6)
10. [ ] Create AI configuration templates
11. [ ] Create campaign templates
12. [ ] Add IaC generation tools
13. [ ] Create CloudFormation templates

---

## Phase 5: Wizard Flow Design

### Setup Wizard Flow
```
1. wizard_start_setup
   ├── Collect: instance_name, region, use_case
   └── Return: recommended_template_set

2. wizard_configure_basics
   ├── Input: channels, identity_type
   └── Create: instance configuration

3. wizard_configure_routing (optional)
   ├── Input: hours_template, queue_count
   └── Create: hours, queues, profiles

4. wizard_configure_cases (optional)
   ├── Input: case_templates[], custom_fields[]
   └── Create: domain, templates, fields

5. wizard_configure_ai (optional)
   ├── Input: knowledge_base_source, prompt_customizations
   └── Create: Q in Connect config

6. wizard_configure_views (optional)
   ├── Input: view_templates[], data_tables[]
   └── Create: views, guides, tables

7. wizard_deploy
   ├── Input: deployment_method (api/cloudformation/sam)
   └── Execute: deploy and return status
```

---

## Notes

### Template Design Principles
1. **Minimal but Complete**: Include only necessary fields with sensible defaults
2. **Customizable**: Allow parameter overrides without modifying base template
3. **Documented**: Include descriptions for all fields
4. **Validated**: Schema validation before deployment
5. **Versioned**: Track template versions for updates

### API Considerations
- Use batch operations where possible
- Handle rate limiting gracefully
- Implement idempotent operations
- Support dry-run mode for validation

### Testing Strategy
- Unit tests for template loading/validation
- Integration tests with mock AWS responses
- End-to-end tests with real Connect instance (optional)
