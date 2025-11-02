# LLM Guidance Best Practices

## Overview

Templates include embedded guidance to help LLMs use Amazon Connect APIs correctly without trial-and-error. This reduces "ping-pong" iterations and gets things done faster.

## Guidance Hierarchy

```
templates/
├── _global_guidance.json          # Read FIRST - applies to ALL tools
├── cases/
│   ├── _llm_guidance.json         # Category-specific guidance
│   ├── general_support.json       # Template with _llm_guidance field
│   └── layouts/
├── routing/
│   ├── _llm_guidance.json
│   └── hours_of_operation/
```

**Loading order:** Global → Category → Template-specific

## Key Principles

### 1. CRITICAL_FIRST_STEP

Always document prerequisites that cause silent failures:

```json
{
  "CRITICAL_FIRST_STEP": {
    "action": "ALWAYS call set_session FIRST",
    "tool": "set_session",
    "params": {"instance_id": "<id>", "region": "<region>"},
    "why": "ALL tools fail with ResourceNotFoundException if region doesn't match"
  }
}
```

### 2. Step-by-Step Workflows

Number steps with dependencies and exact tool names:

```json
{
  "caseCreationWorkflow": {
    "step0_setRegion": {
      "tool": "set_session",
      "CRITICAL": "Do this FIRST"
    },
    "step1_checkDomain": {
      "tool": "list_domains_for_instance",
      "fallback": "cases_create_domain"
    },
    "step2_createProfile": {
      "tool": "profiles_create_profile",
      "returns": "ProfileId"
    }
  }
}
```

### 3. Show Correct vs Wrong

When APIs have gotchas, show both:

```json
{
  "layoutCreationGuidance": {
    "CRITICAL_ERRORS": [
      "❌ System fields (title, status) CANNOT be in layouts",
      "❌ Using 'basicLayout' instead of 'basic' fails",
      "✅ Only custom fields (UUID-based) can be in layouts"
    ],
    "correctStructure": {
      "content": {"basic": {"topPanel": {...}}}
    },
    "wrongStructure": {
      "content": {"basicLayout": "WRONG - use 'basic'"}
    }
  }
}
```

### 4. ARN Formats with Real Examples

Don't just show format - show real example:

```json
{
  "arnFormat": "arn:aws:profile:{region}:{account}:domains/{domain}/profiles/{id}",
  "example": "arn:aws:profile:us-east-1:512144631813:domains/MyDomain/profiles/abc123",
  "CRITICAL": "customer_id MUST be this ARN format, NOT a plain string"
}
```

### 5. Common Errors with Solutions

Map error messages to fixes:

```json
{
  "commonErrors": {
    "ResourceNotFoundException": {
      "cause": "Region mismatch",
      "solution": "Call set_session(instance_id, region) FIRST"
    },
    "ValidationException": {
      "cause": "Invalid parameter format",
      "solution": "Check parameter types, required fields"
    }
  }
}
```

### 6. Dependency Order

Document what must exist before creating:

```json
{
  "dependencyOrder": [
    "1. set_session (CRITICAL - do first)",
    "2. Hours of Operation (no dependencies)",
    "3. Queues (requires hours_of_operation_id)",
    "4. Routing Profiles (requires queue_id)",
    "5. Contact Flows (requires queue_ids)"
  ]
}
```

### 7. Minimal vs Full Examples

Show minimal working example first:

```json
{
  "exampleUsage": {
    "minimalCase": {
      "fields": {"title": "Issue", "customer_id": "arn:aws:profile:..."}
    },
    "fullCase": {
      "fields": {"title": "...", "customer_id": "...", "Priority": "High", ...}
    }
  }
}
```

## Template Structure

Each template should have:

```json
{
  "name": "Template Name",
  "description": "What this template is for",
  
  "_llm_guidance": {
    "workflow": ["Step 1...", "Step 2..."],
    "critical_notes": ["Must do X before Y"],
    "common_errors": {}
  },
  
  "requiredFields": {
    "forCreation": ["field1", "field2"],
    "systemManaged": ["id", "created_at"]
  },
  
  "dependencies": {
    "resourceName": {
      "required": true,
      "tool": "tool_to_create_it"
    }
  },
  
  "exampleUsage": {
    "minimal": {},
    "full": {}
  }
}
```

## Testing Checklist

Before releasing a template:

1. [ ] Can LLM create resource on first try?
2. [ ] Are all prerequisites documented?
3. [ ] Are common errors mapped to solutions?
4. [ ] Is dependency order clear?
5. [ ] Are ARN formats shown with real examples?
6. [ ] Is minimal working example provided?

## Lessons Learned

From testing, these caused the most iterations:

| Issue | Root Cause | Template Fix |
|-------|-----------|--------------|
| ResourceNotFoundException | Region mismatch | CRITICAL_FIRST_STEP |
| Invalid customer_id | Plain string vs ARN | ARN format + example |
| Layout validation errors | System fields in layout | CANNOT_USE list |
| API parameter errors | Wrong key names | correctStructure vs wrongStructure |
| Missing dependencies | Unknown order | dependencyOrder array |
| Wrong domain_id | Used ID from different region | CRITICAL_RESOURCE_REGIONS warning |
| Profiles not found | Domain doesn't exist in current region | List domains first pattern |
| Empty filters error | API requires non-empty arrays | Auto-fetch fallback in code |
| User creation failed | Password required but not passed | userCreation guidance with requiredParams |
| Related item wrong format | Content structure incorrect | Show nested structure: `{comment: {body, contentType}}` |
| Tool works in Python but fails in MCP | Server caches session/code | Restart MCP server after code changes |
| Time range invalid | Future dates or dates too far back | analyticsGuidance with timeRangeRules |
| Large response breaks client | Template content too big | Return path reference instead of content |
| ARN format wrong | Wildcard `*` instead of account ID | Use describe_instance to get real ARN |
| AI search wrong format | API requires specific query structure | Tool handles format internally, user passes simple string |
| AI list_knowledge_bases wrong param | assistantId doesn't exist in API | Removed param - API lists all KBs |
| AI search wrong format | API requires specific query structure | Tool handles format internally, user passes simple string |
| AI list_knowledge_bases wrong param | assistantId doesn't exist in API | Removed param - API lists all KBs |

## Cross-Region Gotchas

Resources are region-specific. Common mistake:

```
❌ Wrong:
1. set_session(region="us-west-2")
2. cases_list_domains() → domain_id = "abc123"
3. set_session(region="us-east-1")  # Changed region!
4. get_case(domain_id="abc123")     # FAILS - domain doesn't exist here

✅ Correct:
1. set_session(region="us-east-1")
2. cases_list_domains() → domain_id = "xyz789"  # Fresh lookup
3. get_case(domain_id="xyz789")     # Works
```

Add this to templates:

```json
{
  "CRITICAL_RESOURCE_REGIONS": {
    "warning": "Resource IDs are region-specific",
    "pattern": "Always list resources AFTER set_session, don't reuse IDs across regions"
  }
}
```

## Adding New Guidance

1. Test the workflow manually
2. Document every error encountered
3. Add to appropriate `_llm_guidance.json`
4. Include in template's `_llm_guidance` field
5. Test that LLM can succeed on first try

## Analytics-Specific Guidance

Time-based APIs are tricky. Always include:

```json
{
  "analyticsGuidance": {
    "timeRangeRules": {
      "CRITICAL": "Times MUST be in the PAST",
      "format": "ISO 8601: 2025-01-03T00:00:00Z",
      "maxRange": "35 days for historical",
      "commonMistake": "Using future dates"
    },
    "safePattern": {
      "description": "Use current time minus offset",
      "end_time": "now - 1 minute",
      "start_time": "now - 24 hours"
    }
  }
}
```

## Large Response Handling

When tools return large content (templates, YAML, etc.):

```json
{
  "largeResponsePattern": {
    "problem": "Large responses break JSON serialization or client parsing",
    "solution": "Return path reference + fetch instruction",
    "example": {
      "template_path": "templates/iac/cloudformation/basic_instance.yaml",
      "note": "Use template_get() to fetch full content"
    }
  }
}
```
