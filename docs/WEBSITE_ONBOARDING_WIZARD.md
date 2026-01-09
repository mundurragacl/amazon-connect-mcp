# Website Onboarding Wizard

Automated contact center setup from website discovery.

## Overview

A wizard that scrapes a company website to extract business information and automatically configures a complete Amazon Connect contact center with Amazon Q in Connect for FAQ handling.

## Tools

### 1. `wizard_discover_website(url)`

Fetches website and extracts:
- **Brand name** → instance alias
- **Industry** → template selection
- **Hours of operation** → hours config
- **FAQ content** → knowledge base articles
- **Products/Services** → case fields, routing

**Industry Detection Keywords:**
```python
INDUSTRY_KEYWORDS = {
    "healthcare": ["patient", "appointment", "medical", "doctor", "health", "clinic"],
    "ecommerce": ["cart", "shipping", "order", "return", "product", "shop"],
    "telecom": ["plan", "data", "minutes", "coverage", "mobile", "phone"],
    "financial": ["account", "transaction", "loan", "credit", "banking"],
    "insurance": ["policy", "claim", "coverage", "premium"],
    "travel": ["booking", "reservation", "flight", "hotel"],
    "utilities": ["meter", "outage", "service", "bill"],
    "technology": ["software", "subscription", "license", "support"]
}
```

**Returns:**
```json
{
  "brand": "Acme Corp",
  "industry": "ecommerce",
  "hours": {
    "timezone": "America/New_York",
    "schedule": [
      {"day": "MONDAY", "start": "09:00", "end": "17:00"},
      {"day": "TUESDAY", "start": "09:00", "end": "17:00"}
    ]
  },
  "faqs": [
    {
      "title": "How do I return an item?",
      "summary": "Our return policy allows 30-day returns for most items.",
      "content": "1. Log into your account\n2. Go to Order History\n3. Click Return Item..."
    }
  ],
  "products": ["Electronics", "Clothing", "Home & Garden"],
  "support_email": "support@acme.com",
  "support_phone": "+1-800-555-0123"
}
```

### 2. `wizard_generate_faq_files(brand, faqs)`

Creates FAQ text files for Q in Connect ingestion.

**Output Structure:**
```
./{brand}/
├── faq/
│   ├── 01-how-do-i-return-an-item.txt
│   ├── 02-what-are-your-hours.txt
│   └── 03-how-do-i-track-my-order.txt
└── {brand}_onboarding_state.json
```

**FAQ File Format:**
```
Title: How do I return an item?

Summary: Our return policy allows 30-day returns for most items.

Process:
1. Log into your account at acme.com
2. Navigate to Order History
3. Find the order containing the item
4. Click "Return Item" button
5. Select reason for return
6. Print shipping label
7. Drop off at any carrier location

Returns are processed within 5-7 business days after receipt.
```

**Requirements:**
- One question per file
- Max 1 MB per file (Q in Connect limit)
- .txt format (supported by Q in Connect)

### 3. `wizard_execute_onboarding(config, resume_from=None)`

Executes the full onboarding workflow with resume support.

**Config Input:**
```json
{
  "brand": "Acme Corp",
  "industry": "ecommerce",
  "region": "us-east-1",
  "hours": {...},
  "faq_directory": "./acme-corp/faq"
}
```

## Workflow Phases

### Phase 1: Discovery
```
User provides URL
    ↓
wizard_discover_website(url)
    ↓
Present extracted data to user
    ↓
User confirms or provides feedback
    ↓
Loop until approved
```

### Phase 2: FAQ Generation
```
wizard_generate_faq_files(brand, faqs)
    ↓
Creates ./{brand}/faq/*.txt
    ↓
User reviews FAQ files
    ↓
User can edit files manually
    ↓
User approves
```

### Phase 3: Instance Creation
```
Step 1: create_instance(alias=brand, identity_management_type="CONNECT_MANAGED")
Step 2: sleep(60)
Step 3: describe_instance() → check status
Step 4: If not ACTIVE: sleep(30), retry (max 5 attempts)
Step 5: set_session(instance_id, region)
```

### Phase 4: Routing Setup
```
Step 6: config_create_hours_of_operation(...)
Step 7: config_create_queue(name="{brand} Support", hours_id)
Step 8: config_create_routing_profile(name="{brand} Agent", queue_id)
```

### Phase 5: Customer Profiles (MUST be before Cases)
```
Step 9:  profiles_create_domain(brand)
Step 10: profiles_associate_domain(instance_id, domain_name)
```

### Phase 6: Cases Setup
```
Step 11: cases_create_domain(brand)
Step 12: cases_create_field(...) × N (industry-specific fields)
Step 13: cases_create_template(from industry template)
Step 14: cases_create_layout(from industry layout)
Step 15: cases_associate_domain(instance_id, domain_id)
```

### Phase 7: Amazon Q in Connect
```
Step 16: Enable Amazon Q in Connect
Step 17: Create knowledge base
Step 18: For each FAQ file in ./{brand}/faq/:
         - start_content_upload() → presigned URL
         - Upload .txt file to presigned URL
         - create_content(knowledge_base_id, upload_id, name)
Step 19: Associate knowledge base with queue
```

## State Management

**State File:** `./{brand}/{brand}_onboarding_state.json`

```json
{
  "brand": "acme-corp",
  "started_at": "2026-01-09T20:00:00Z",
  "updated_at": "2026-01-09T20:15:00Z",
  "region": "us-east-1",
  "current_phase": 4,
  "current_step": 7,
  "completed_steps": [1, 2, 3, 4, 5, 6],
  "resources": {
    "instance_id": "abc-123",
    "hours_of_operation_id": "def-456",
    "queue_id": "ghi-789",
    "routing_profile_id": "jkl-012",
    "profiles_domain_name": "acme-corp",
    "cases_domain_id": "mno-345",
    "knowledge_base_id": "pqr-678"
  },
  "error": null
}
```

**Resume Logic:**
```python
def execute_step(step_num, state):
    if step_num in state["completed_steps"]:
        return  # Skip completed
    
    try:
        result = run_step(step_num, state)
        state["completed_steps"].append(step_num)
        state["resources"].update(result)
        save_state(state)
    except Exception as e:
        state["error"] = {"step": step_num, "message": str(e)}
        save_state(state)
        raise
```

## Industry Template Mapping

| Industry | Case Template | Layout | Fields |
|----------|--------------|--------|--------|
| ecommerce | `ecommerce_support` | `retail_ecommerce_layout` | order_id, product, shipping |
| healthcare | `healthcare_support` | `healthcare_layout` | patient_id, appointment, provider |
| financial | `financial_services` | `financial_services_layout` | account, transaction, amount |
| telecom | `telecom_support` | `telecom_layout` | service_id, plan, device |
| insurance | `insurance_claims` | `insurance_claims_layout` | policy, claim, adjuster |
| travel | `travel_hospitality` | `travel_hospitality_layout` | reservation, loyalty, dates |
| utilities | `utilities_support` | `utilities_layout` | service_address, meter, outage |
| technology | `technology_support` | `technology_layout` | product, license, version |

## Q in Connect Content Upload

**Supported Formats:** HTML, Word, PDF, .txt (up to 1 MB)

**Upload Flow:**
```python
# 1. Get presigned URL
response = qconnect.start_content_upload(
    knowledgeBaseId=kb_id,
    contentType="text/plain"
)
upload_id = response["uploadId"]
presigned_url = response["url"]

# 2. Upload file
with open(faq_file, "rb") as f:
    requests.put(presigned_url, data=f.read())

# 3. Create content record
qconnect.create_content(
    knowledgeBaseId=kb_id,
    uploadId=upload_id,
    name=faq_title
)
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Instance not ACTIVE after 5 retries | Slow provisioning | Manual check in console |
| profiles_associate_domain fails | Instance not ready | Retry after 30s |
| cases_associate_domain fails | Profiles not associated | Check Phase 5 completed |
| Content upload fails | File > 1MB | Split into smaller files |
| ResourceNotFoundException | Region mismatch | Verify set_session called |

## Usage Example

```
User: Set up a contact center for https://acme-store.com


LLM: I'll help you set up a contact center. Let me analyze your website first.

[Calls wizard_discover_website("https://acme-store.com")]

LLM: Here's what I found:
- Brand: Acme Store
- Industry: E-commerce
- Hours: Mon-Fri 9am-6pm EST
- FAQs found: 12 questions
- Products: Electronics, Home Goods, Apparel

Does this look correct? Should I generate the FAQ files for review?

User: Yes, looks good

[Calls wizard_generate_faq_files("acme-store", faqs)]

LLM: I've created 12 FAQ files in ./acme-store/faq/
Please review them and let me know when ready to proceed.

User: Reviewed, all good. Proceed with setup.

[Calls wizard_execute_onboarding(config)]

LLM: Starting onboarding...
✓ Phase 3: Instance created (acme-store)
✓ Phase 4: Routing configured
✓ Phase 5: Customer Profiles enabled
✓ Phase 6: Cases configured with e-commerce template
✓ Phase 7: Amazon Q in Connect enabled with 12 FAQ articles

Your contact center is ready!
Instance: acme-store
Region: us-east-1
```

## Future Enhancements

1. **Multi-language FAQ**: Detect website language, generate FAQs in multiple languages
2. **Logo extraction**: Use brand logo for agent workspace customization
3. **Social media integration**: Extract social links for omnichannel setup
4. **Competitor analysis**: Suggest differentiating features based on industry
5. **Cost estimation**: Estimate monthly costs based on expected volume
