# MCP Architecture Best Practices for Large Tool Sets

This document outlines architecture patterns and best practices for building MCP servers with many tools, based on 2025 industry research and production implementations.

---

## The Problem: Context Window Bloat & Tool Selection Degradation

When building MCP servers with many tools (like Amazon Connect's 200+ APIs), two critical issues emerge:

1. **Context Window Bloat**: Tool definitions consume massive context (50 tools ≈ 10-20K tokens)
2. **Tool Selection Degradation**: LLM accuracy drops significantly beyond 30-50 tools
3. **Static Front-Loading**: All tools loaded upfront waste context on unused capabilities

---

## Architecture Patterns

### Pattern 1: Tool Grouping (Namespacing)

**Best for: 20-50 tools**

Group tools into logical namespaces to simplify LLM decision-making.

```
// Instead of flat list:
create_case, get_case, update_case, create_contact, get_contact...

// Use namespaced tools:
cases/create, cases/get, cases/update
contacts/create, contacts/get
metrics/realtime, metrics/historical
```

**Benefits:**
- LLM first selects category, then specific tool
- Reduces cognitive load
- Scales to ~50 tools effectively

---

### Pattern 2: Dynamic Toolsets (Lazy Loading)

**Best for: 50-200 tools**

Only load tools relevant to the current context. This is the officially recommended MCP approach.

```python
# Expose toolset management tools
ListAvailableToolsets()    # Returns: ["cases", "contacts", "metrics", "campaigns"]
GetToolsetTools("cases")   # Returns tools in that category
EnableToolset("cases")     # Dynamically adds case tools to active set

# LLM only sees enabled toolsets
```

**Implementation (GitHub MCP Server pattern):**
```typescript
class DynamicToolsetServer {
  private toolsets = {
    cases: { enabled: false, tools: ["create_case", "get_case", "update_case"] },
    contacts: { enabled: false, tools: ["start_chat", "start_call", "transfer"] },
    metrics: { enabled: false, tools: ["get_realtime_metrics", "get_historical"] }
  };

  // Meta-tools for toolset management
  listToolsets() { return Object.keys(this.toolsets); }
  enableToolset(name: string) { this.toolsets[name].enabled = true; }
  
  // Only return enabled tools
  getActiveTools() {
    return Object.entries(this.toolsets)
      .filter(([_, v]) => v.enabled)
      .flatMap(([_, v]) => v.tools);
  }
}
```

---

### Pattern 3: Defer Loading (Anthropic's 2025 Solution)

**Best for: 100+ tools**

Tools are registered with `defer_loading: true`. LLM uses a search tool to discover and load tools on-demand.

```json
{
  "tools": [
    {
      "type": "tool_search_tool_regex_20251119",
      "name": "tool_search"
    },
    {
      "type": "mcp_toolset",
      "mcp_server_name": "amazon-connect",
      "default_config": { "defer_loading": true },
      "configs": {
        "describe_instance": { "defer_loading": false }
      }
    }
  ]
}
```

**How it works:**
1. LLM sees only the tool search tool initially
2. When LLM needs capabilities, it searches for relevant tools
3. Matching tools (3-5) get expanded into full definitions on-demand
4. LLM selects and invokes the appropriate tool

**Benefits:**
- 80-90% reduction in context usage
- Scales to 10,000+ tools
- Maintains high selection accuracy

---

### Pattern 4: Multiple MCP Servers

**Best for: Enterprise scale (AWS approach with 30+ servers)**

Split functionality into separate, specialized MCP servers.

```
amazon-connect-mcp/
├── connect-core-server/        # Instance, queues, routing
├── connect-contacts-server/    # Contact operations
├── connect-cases-server/       # Case management
├── connect-analytics-server/   # Metrics & reporting
├── connect-profiles-server/    # Customer profiles
└── connect-ai-server/          # Amazon Q, knowledge bases
```

**Organization strategies:**
- **By domain**: Cases, Contacts, Analytics, Configuration
- **By permission level**: Read-only vs. Write operations
- **By performance**: Fast lookups vs. batch operations

---

### Pattern 5: MCP Gateway (AWS AgentCore Pattern)

**Best for: Enterprise with multiple MCP servers**

A centralized gateway that unifies multiple MCP servers behind a single interface.

```
┌─────────────────────────────────────────────────────┐
│                    MCP Gateway                       │
│  - Unified authentication                           │
│  - Tool discovery across all servers                │
│  - Semantic search across tools                     │
│  - Request routing                                  │
└─────────────────────────────────────────────────────┘
         │              │              │
    ┌────┴────┐   ┌────┴────┐   ┌────┴────┐
    │ Cases   │   │Contacts │   │Analytics│
    │ Server  │   │ Server  │   │ Server  │
    └─────────┘   └─────────┘   └─────────┘
```

**Benefits:**
- Single connection point for AI agents
- Centralized auth and access control
- Semantic tool search across all servers
- Teams can maintain separate servers

---

### Pattern 6: Single Endpoint (Universal Translator)

**Best for: Large/legacy REST APIs**

One powerful tool that accepts natural language and translates to API calls.

```python
@mcp.tool()
def amazon_connect_api(natural_language_query: str) -> dict:
    """
    Execute Amazon Connect operations using natural language.
    Examples:
    - "Find all cases for customer john@example.com"
    - "Create a new case for order #12345 with high priority"
    - "Get real-time metrics for the support queue"
    """
    # Backend translates to appropriate API calls
    return api_translator.execute(natural_language_query)
```

**Benefits:**
- Minimal context usage (1 tool definition)
- LLM doesn't need to know API structure
- Backend handles complexity

**Trade-offs:**
- Requires sophisticated NL→API translation
- Less transparent/debuggable

---

## Recommended Architecture for Amazon Connect MCP

Given Amazon Connect's 200+ APIs across 9 services, use **Defer Loading (Pattern 3)** with a single server:

```
┌─────────────────────────────────────────────────────────┐
│           amazon-connect-mcp (Single Server)            │
│                                                         │
│  TIER 1 - Always Loaded (~10-15 core tools):           │
│  ├── describe_instance                                  │
│  ├── list_queues                                        │
│  ├── get_current_metrics                                │
│  ├── search_contacts                                    │
│  ├── create_case                                        │
│  └── get_case                                           │
│                                                         │
│  TIER 2 - Defer Loaded (on-demand via tool search):    │
│  ├── cases/* (50+ tools) ────────► defer_loading: true │
│  ├── contacts/* (30+ tools) ─────► defer_loading: true │
│  ├── config/* (80+ tools) ───────► defer_loading: true │
│  ├── analytics/* (20+ tools) ────► defer_loading: true │
│  ├── profiles/* (40+ tools) ─────► defer_loading: true │
│  ├── campaigns/* (25+ tools) ────► defer_loading: true │
│  └── ai/* (50+ tools) ───────────► defer_loading: true │
└─────────────────────────────────────────────────────────┘
```

### How It Works

1. **LLM sees**: Tier 1 tools + tool search capability (~15 tools in context)
2. **User asks**: "Create a case template with custom fields"
3. **LLM searches**: Finds `cases/create_template`, `cases/create_field`
4. **Tools expand**: Full definitions loaded into context on-demand
5. **LLM executes**: With only the relevant tools visible

### Benefits
- **Single MCP server** - Simpler deployment and maintenance
- **Minimal context usage** - ~10-15 tools normally visible
- **200+ tools available** - All accessible via search when needed
- **High accuracy** - LLM only sees relevant tools for the task

### Implementation

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({ name: "amazon-connect-mcp" });

// ============================================
// TIER 1: Core Tools (Always Loaded)
// ============================================
server.tool(
  "describe_instance",
  { instance_id: z.string() },
  async ({ instance_id }) => { /* ... */ },
  { defer_loading: false }  // Always available
);

server.tool(
  "get_current_metrics",
  { instance_id: z.string(), queue_ids: z.array(z.string()).optional() },
  async (params) => { /* ... */ },
  { defer_loading: false }
);

server.tool(
  "create_case",
  { domain_id: z.string(), template_id: z.string(), fields: z.record(z.any()) },
  async (params) => { /* ... */ },
  { defer_loading: false }
);

// ============================================
// TIER 2: Domain Tools (Defer Loaded)
// ============================================

// Cases domain
server.tool(
  "cases/create_template",
  { domain_id: z.string(), name: z.string(), fields: z.array(z.string()) },
  async (params) => { /* ... */ },
  { defer_loading: true }  // Loaded on-demand
);

server.tool(
  "cases/create_field",
  { domain_id: z.string(), name: z.string(), type: z.enum(["text", "number", "boolean", "date"]) },
  async (params) => { /* ... */ },
  { defer_loading: true }
);

// Contacts domain
server.tool(
  "contacts/start_outbound_voice",
  { instance_id: z.string(), destination: z.string(), contact_flow_id: z.string() },
  async (params) => { /* ... */ },
  { defer_loading: true }
);

// Config domain
server.tool(
  "config/create_workspace",
  { instance_id: z.string(), name: z.string() },
  async (params) => { /* ... */ },
  { defer_loading: true }
);

// ... 200+ more tools with defer_loading: true
```

### Client Configuration (Anthropic)

```json
{
  "tools": [
    {
      "type": "tool_search_tool_regex_20251119",
      "name": "tool_search"
    },
    {
      "type": "mcp_toolset",
      "mcp_server_name": "amazon-connect-mcp",
      "default_config": { "defer_loading": true },
      "configs": {
        "describe_instance": { "defer_loading": false },
        "get_current_metrics": { "defer_loading": false },
        "search_contacts": { "defer_loading": false },
        "create_case": { "defer_loading": false },
        "get_case": { "defer_loading": false }
      }
    }
  ]
}
```

### Tool Naming Convention

Use namespaced names for deferred tools to improve search accuracy:

```
cases/create_case
cases/get_case
cases/update_case
cases/create_template
cases/create_field

contacts/start_voice
contacts/start_chat
contacts/transfer
contacts/stop

config/create_workspace
config/create_view
config/create_flow
config/create_data_table

analytics/get_realtime_metrics
analytics/get_historical_metrics
analytics/search_contacts

profiles/create_profile
profiles/search_profiles
profiles/merge_profiles

campaigns/create_campaign
campaigns/start_campaign
campaigns/put_outbound_batch

ai/query_assistant
ai/search_content
ai/get_recommendations
```

---

## Best Practices Summary

### Tool Design
1. **Design for use cases, not API calls** - Combine related operations into single tools
2. **Use descriptive names** - `create_support_case` not `cases_post_endpoint`
3. **Return actionable responses** - Minimize tokens, maximize usefulness

### Organization
4. **Namespace tools** - Use `domain/action` format
5. **Start with dynamic toolsets** - Don't load everything upfront
6. **Split at ~30-50 tools per server** - Beyond this, use multiple servers

### Performance
7. **Keep core tools non-deferred** - Frequently used tools should always be available
8. **Use permissions to scope** - Only request tools the user needs
9. **Implement semantic search** - Help LLMs find the right tool

### Scaling
10. **Consider MCP Gateway** - For enterprise with multiple servers
11. **Use defer_loading** - For 100+ tools
12. **Monitor token usage** - Track context consumption

---

## Pattern Comparison

| Pattern | Tool Count | Complexity | Best For |
|---------|-----------|------------|----------|
| Namespacing | 20-50 | Low | Simple categorization |
| Dynamic Toolsets | 50-200 | Medium | Domain-based loading |
| Defer Loading | 100-10,000 | Medium | Large tool catalogs |
| Multiple Servers | 100+ | High | Enterprise/team separation |
| MCP Gateway | 200+ | High | Multi-server unification |
| Single Endpoint | Any | High | Legacy API abstraction |

---

## References

- [MCP Server Best Practices (MCPcat)](https://mcpcat.io/blog/mcp-server-best-practices/)
- [MCP Patterns Guide (Elastic Path)](https://www.elasticpath.com/blog/mcp-magic-moments-guide-to-llm-patterns)
- [AWS MCP Servers (GitHub)](https://github.com/awslabs/mcp)
- [AWS AgentCore Gateway](https://aws.amazon.com/blogs/machine-learning/transform-your-mcp-architecture-unite-mcp-servers-through-agentcore-gateway/)
- [Anthropic Defer Loading](https://unified.to/blog/scaling_mcp_tools_with_anthropic_defer_loading)
- [MCP Specification](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [GitHub MCP Server Dynamic Tools](https://github.com/github/github-mcp-server)


---

## Framework & Language Recommendation

Based on 2025 research, here's a comprehensive analysis of MCP server frameworks for building the Amazon Connect MCP server.

### Framework Comparison Matrix

| Framework | Language | Performance | Ease of Use | Production Ready | Caching | Defer Loading |
|-----------|----------|-------------|-------------|------------------|---------|---------------|
| **FastMCP** | Python | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ Built-in | ✅ |
| **MCP-Framework** | TypeScript | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Manual | ✅ |
| **FastMCP (TS)** | TypeScript | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Manual | ✅ |
| **Foxy Contexts** | Go | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | Manual | ✅ |
| **UltraFast MCP** | Rust | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | Manual | ✅ |
| **Quarkus MCP** | Java | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Manual | ✅ |

### 🏆 Recommended: FastMCP (Python)

**Why FastMCP Python is the best choice for Amazon Connect MCP:**

1. **Built-in Middleware System**
   - Response caching (TTL-based, LRU eviction)
   - Rate limiting
   - Error handling
   - Logging & timing
   - Tool injection

2. **Production Features Out-of-Box**
   - Authentication hooks
   - Session management
   - SSE streaming
   - Streamable HTTP transport
   - Progress notifications

3. **AWS SDK Integration**
   - boto3 is the most mature AWS SDK
   - Native async support with aioboto3
   - Extensive AWS documentation and examples

4. **Developer Experience**
   - Decorator-based API (`@mcp.tool()`)
   - Pydantic validation (automatic schema generation)
   - Hot reload in development
   - CLI tools for testing

5. **Community & Adoption**
   - ~20,000+ developers using FastMCP
   - Incorporated into official MCP Python SDK
   - Active maintenance and updates

### Performance Benchmarks (2025)

```
Language Performance (relative to Python baseline):
├── Rust:   ~60x faster (CPU-bound tasks)
├── Go:     ~2x faster (CPU-bound), excellent concurrency
├── Java:   ~1.5x faster (with Quarkus native)
├── Node:   ~1.2x faster (async I/O)
└── Python: baseline (but sufficient for I/O-bound MCP)
```

**Key insight**: MCP servers are I/O-bound (waiting on AWS API calls), not CPU-bound. Python's async performance is sufficient, and developer productivity gains outweigh raw speed differences.

### FastMCP Implementation Example

```python
from fastmcp import FastMCP
from fastmcp.server.middleware import (
    ResponseCachingMiddleware,
    RateLimitingMiddleware,
    TimingMiddleware
)
import boto3

# Initialize with middleware
mcp = FastMCP(
    "amazon-connect-mcp",
    middleware=[
        ResponseCachingMiddleware(
            call_tool={"enabled": True, "ttl": 300},  # 5 min cache
            list_tools={"enabled": True, "ttl": 3600}  # 1 hour cache
        ),
        RateLimitingMiddleware(requests_per_minute=100),
        TimingMiddleware()
    ]
)

# AWS clients (cached)
connect_client = boto3.client('connect')
cases_client = boto3.client('connectcases')

# ============================================
# TIER 1: Core Tools (Always Loaded)
# ============================================

@mcp.tool()
async def describe_instance(instance_id: str) -> dict:
    """Get Amazon Connect instance details."""
    return connect_client.describe_instance(InstanceId=instance_id)

@mcp.tool()
async def get_current_metrics(
    instance_id: str,
    queue_ids: list[str] | None = None
) -> dict:
    """Get real-time metrics for queues and agents."""
    filters = {"Queues": queue_ids} if queue_ids else {}
    return connect_client.get_current_metric_data(
        InstanceId=instance_id,
        Filters=filters,
        CurrentMetrics=[
            {"Name": "AGENTS_AVAILABLE", "Unit": "COUNT"},
            {"Name": "CONTACTS_IN_QUEUE", "Unit": "COUNT"}
        ]
    )

@mcp.tool()
async def create_case(
    domain_id: str,
    template_id: str,
    fields: dict
) -> dict:
    """Create a new case in Amazon Connect Cases."""
    return cases_client.create_case(
        domainId=domain_id,
        templateId=template_id,
        fields=[{"id": k, "value": v} for k, v in fields.items()]
    )

# ============================================
# TIER 2: Domain Tools (Defer Loaded)
# ============================================

@mcp.tool(defer_loading=True)
async def cases_create_template(
    domain_id: str,
    name: str,
    description: str = ""
) -> dict:
    """Create a case template."""
    return cases_client.create_template(
        domainId=domain_id,
        name=name,
        description=description
    )

@mcp.tool(defer_loading=True)
async def cases_create_field(
    domain_id: str,
    name: str,
    field_type: str  # "Text", "Number", "Boolean", "DateTime", "SingleSelect"
) -> dict:
    """Create a custom field for cases."""
    return cases_client.create_field(
        domainId=domain_id,
        name=name,
        type=field_type
    )

@mcp.tool(defer_loading=True)
async def contacts_start_outbound_voice(
    instance_id: str,
    destination_phone: str,
    contact_flow_id: str,
    source_phone: str,
    attributes: dict | None = None
) -> dict:
    """Initiate an outbound voice call."""
    return connect_client.start_outbound_voice_contact(
        InstanceId=instance_id,
        DestinationPhoneNumber=destination_phone,
        ContactFlowId=contact_flow_id,
        SourcePhoneNumber=source_phone,
        Attributes=attributes or {}
    )

@mcp.tool(defer_loading=True)
async def config_create_workspace(
    instance_id: str,
    name: str,
    description: str = ""
) -> dict:
    """Create an agent workspace."""
    return connect_client.create_workspace(
        InstanceId=instance_id,
        Name=name,
        Description=description
    )

# Run server
if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
```

### Project Structure

```
amazon-connect-mcp/
├── pyproject.toml
├── src/
│   └── amazon_connect_mcp/
│       ├── __init__.py
│       ├── server.py              # Main FastMCP server
│       ├── config.py              # Settings & AWS config
│       ├── middleware/
│       │   ├── __init__.py
│       │   └── aws_caching.py     # Custom AWS response caching
│       └── tools/
│           ├── __init__.py
│           ├── core.py            # Tier 1: Always loaded
│           ├── cases.py           # Tier 2: Defer loaded
│           ├── contacts.py
│           ├── config.py
│           ├── analytics.py
│           ├── profiles.py
│           ├── campaigns.py
│           └── ai.py
├── tests/
│   └── ...
└── README.md
```

### Alternative: TypeScript (MCP-Framework)

If your team prefers TypeScript:

```typescript
import { MCPServer } from "mcp-framework";
import { ConnectClient } from "@aws-sdk/client-connect";

const server = new MCPServer({ name: "amazon-connect-mcp" });
const connect = new ConnectClient({});

// Tier 1: Core tools
server.tool("describe_instance", {
  description: "Get Amazon Connect instance details",
  parameters: { instance_id: { type: "string", required: true } },
  handler: async ({ instance_id }) => {
    return connect.describeInstance({ InstanceId: instance_id });
  },
  deferLoading: false
});

// Tier 2: Deferred tools
server.tool("cases/create_template", {
  description: "Create a case template",
  parameters: {
    domain_id: { type: "string", required: true },
    name: { type: "string", required: true }
  },
  handler: async ({ domain_id, name }) => { /* ... */ },
  deferLoading: true
});

server.start({ transport: "streamable-http", port: 8000 });
```

### When to Choose Each Language

| Choose Python (FastMCP) | Choose TypeScript | Choose Go/Rust |
|------------------------|-------------------|----------------|
| AWS-heavy integrations | VS Code extensions | Extreme performance needs |
| Data/ML pipelines | Web-adjacent services | High concurrency (10K+ req/s) |
| Rapid prototyping | Existing Node stack | Memory-constrained environments |
| Built-in middleware needed | Frontend team familiarity | Systems programming |

### Caching Strategy

FastMCP's built-in caching handles:

```python
ResponseCachingMiddleware(
    # Cache tool listings for 1 hour (rarely change)
    list_tools={"enabled": True, "ttl": 3600},
    
    # Cache resource listings for 1 hour
    list_resources={"enabled": True, "ttl": 3600},
    
    # Cache tool results for 5 minutes (balance freshness vs. API calls)
    call_tool={"enabled": True, "ttl": 300},
    
    # Cache resource reads for 5 minutes
    read_resource={"enabled": True, "ttl": 300}
)
```

For AWS-specific caching, add a custom layer:

```python
from functools import lru_cache
from datetime import datetime, timedelta

class AWSCache:
    def __init__(self, ttl_seconds: int = 300):
        self._cache = {}
        self._ttl = ttl_seconds
    
    def get(self, key: str):
        if key in self._cache:
            value, expiry = self._cache[key]
            if datetime.now() < expiry:
                return value
            del self._cache[key]
        return None
    
    def set(self, key: str, value):
        self._cache[key] = (value, datetime.now() + timedelta(seconds=self._ttl))

# Usage in tools
aws_cache = AWSCache(ttl_seconds=300)

@mcp.tool()
async def list_queues(instance_id: str) -> dict:
    cache_key = f"queues:{instance_id}"
    cached = aws_cache.get(cache_key)
    if cached:
        return cached
    
    result = connect_client.list_queues(InstanceId=instance_id)
    aws_cache.set(cache_key, result)
    return result
```

### Deployment Options

1. **Local (stdio)**: For Claude Desktop, Cursor, etc.
   ```bash
   fastmcp run server.py
   ```

2. **Remote (Streamable HTTP)**: For cloud deployment
   ```bash
   fastmcp run server.py --transport streamable-http --port 8000
   ```

3. **Docker**:
   ```dockerfile
   FROM python:3.12-slim
   WORKDIR /app
   COPY pyproject.toml .
   RUN pip install .
   COPY src/ src/
   CMD ["fastmcp", "run", "src/amazon_connect_mcp/server.py", "--transport", "streamable-http"]
   ```

4. **AWS Lambda** (via AWS AgentCore Runtime):
   - Deploy as container to AgentCore
   - Gateway handles auth, rate limiting, tool discovery

---

## Summary: Recommended Stack

| Component | Choice | Reason |
|-----------|--------|--------|
| **Language** | Python 3.12+ | Best AWS SDK, async support, productivity |
| **Framework** | FastMCP 2.x | Built-in caching, middleware, production-ready |
| **Transport** | Streamable HTTP | Modern, supports streaming, remote deployment |
| **Validation** | Pydantic | Automatic schema generation, type safety |
| **AWS SDK** | boto3 + aioboto3 | Mature, well-documented, async support |
| **Caching** | FastMCP middleware + custom | TTL-based, LRU eviction |
| **Deployment** | Docker / AWS AgentCore | Scalable, managed infrastructure |

---

## Additional References

- [FastMCP Documentation](https://gofastmcp.com)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [MCP-Framework (TypeScript)](https://github.com/QuantGeekDev/mcp-framework)
- [Foxy Contexts (Go)](https://github.com/strowk/foxy-contexts)
- [UltraFast MCP (Rust)](https://lib.rs/crates/ultrafast-mcp-server)
- [Quarkus MCP (Java)](https://github.com/quarkiverse/quarkus-mcp-server)
