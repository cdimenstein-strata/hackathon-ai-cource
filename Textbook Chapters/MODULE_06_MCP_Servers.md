# MODULE 6: MCP (Model Context Protocol) Servers
## Week 9 | Textbook Content

---

## Chapter 6.1 — What Is MCP?

### The Standardization Problem MCP Solves

By 2024, every major AI framework — LangChain, LlamaIndex, Bedrock Agents, AutoGen, CrewAI — had its own way of defining and invoking tools. This created a fragmented ecosystem where:

- A tool written for LangChain couldn't be used in CrewAI without rewriting it
- A Bedrock Action Group Lambda function couldn't be called by a LlamaIndex agent
- An enterprise building multiple AI systems needed to maintain separate tool implementations for each framework
- Tool authors couldn't share tools across the ecosystem without framework-specific wrappers

**Model Context Protocol (MCP)** is an open standard, introduced by Anthropic in late 2024, that defines a universal protocol for how AI applications (clients) communicate with tool providers (servers). It is, in essence, the HTTP of AI tool integration — a standard protocol that any client can use to discover and call any server's tools.

**The core promise:** Write a tool once (as an MCP server), and it can be used by any MCP-compatible AI client — Claude Desktop, Cursor, custom agents, Bedrock agents with MCP integration, or any other client that implements the protocol.

---

### The Protocol Specification

MCP defines:

1. **Transport:** How messages are sent between client and server (stdio for local, HTTP+SSE or WebSocket for remote)

2. **Message format:** JSON-RPC 2.0 messages for all communication

3. **Capabilities:**
   - **Tools:** Functions the server exposes for the AI to call
   - **Resources:** Data sources the AI can read
   - **Prompts:** Pre-written prompts the AI can use
   - **Sampling:** The ability for the server to request AI-generated text

4. **Lifecycle:**
   - Initialize: Client and server exchange capabilities
   - List tools: Client discovers what tools the server offers
   - Call tool: Client invokes a specific tool
   - Handle response: Client processes the result

**MCP message structure (tool call):**

```json
// Client → Server: Call a tool
{
  "jsonrpc": "2.0",
  "id": "call-1",
  "method": "tools/call",
  "params": {
    "name": "get_negotiated_rates",
    "arguments": {
      "payer_id": "BCBS-PPO-001",
      "procedure_code": "27447"
    }
  }
}

// Server → Client: Tool result
{
  "jsonrpc": "2.0",
  "id": "call-1",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"status\": \"success\", \"payer\": \"BlueCross\", \"plan\": \"PPO\"}"
      }
    ],
    "isError": false
  }
}
```

---

## Chapter 6.2 — Building an MCP Server

### MCP Server Structure

An MCP server is a program that:
1. Listens for connections from MCP clients
2. Reports its capabilities (available tools, resources, prompts)
3. Executes tool calls and returns results

**Minimal MCP server in Python (using the official MCP SDK):**

```python
# Install: pip install mcp
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
import asyncio
import json
import boto3

# Create the MCP server
app = Server("financial-analytics-tools")

# Define the available tools
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="get_negotiated_rates",
            description="""Retrieves CMS MRF negotiated rates for a specific payer and procedure code.
            Returns contracted rate, rate type (per diem/DRG/fee schedule), effective date,
            and market percentile. Use when you need to compare actual allowed amounts against
            contracted rates.
            Do NOT use for historical rate queries outside the current contract period.""",
            inputSchema={
                "type": "object",
                "required": ["payer_id", "procedure_code"],
                "properties": {
                    "payer_id": {
                        "type": "string",
                        "description": "The payer's identifier. Format: alphanumeric payer code (e.g., BCBS-PPO-001)."
                    },
                    "procedure_code": {
                        "type": "string",
                        "description": "CPT or HCPCS code for the procedure, or MS-DRG for inpatient services."
                    }
                }
            }
        ),
        Tool(
            name="query_claims_summary",
            description="""Returns aggregated claims data for a service line and payer over a date range.
            Returns: total encounters, total billed amount, total allowed amount, denial count,
            denial rate. Use when you need volume and financial performance data for a
            service line/payer combination.""",
            inputSchema={
                "type": "object",
                "required": ["service_line", "payer_id", "date_range"],
                "properties": {
                    "service_line": {
                        "type": "string",
                        "description": "The clinical service line (e.g., Orthopedics, Cardiology, Obstetrics)."
                    },
                    "payer_id": {
                        "type": "string",
                        "description": "The payer's identifier from the contract management system."
                    },
                    "date_range": {
                        "type": "object",
                        "description": "Date range for claims aggregation. Object with 'start' and 'end' keys in YYYY-MM-DD format."
                    }
                }
            }
        )
    ]

# Handle tool calls
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:

    if name == "get_negotiated_rates":
        result = await handle_get_negotiated_rates(arguments)

    elif name == "query_claims_summary":
        result = await handle_query_claims_summary(arguments)

    else:
        result = {"error": f"Unknown tool: {name}"}

    return [TextContent(type="text", text=json.dumps(result))]


async def handle_get_negotiated_rates(arguments: dict) -> dict:
    payer_id = arguments["payer_id"]
    procedure_code = arguments["procedure_code"]

    # In production: query CMS MRF API or contract management system
    # For demo: mock response
    if not payer_id:
        return {
            "status": "error",
            "error_code": "INVALID_PAYER_ID",
            "error_message": f"Invalid payer ID: {payer_id}. Expected a valid payer identifier."
        }

    # Simulate CMS MRF lookup
    rates_data = {
        "status": "success",
        "rates": {
            "payer_id": payer_id,
            "procedure_code": procedure_code,
            "contracted_rate": 12450.00,
            "rate_type": "DRG",
            "effective_date": "2026-01-01",
            "expiration_date": "2026-12-31",
            "market_percentile": 52,
            "rate_basis": "MS-DRG base rate multiplier"
        }
    }

    return rates_data


# Run the server (stdio mode for local use)
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

**Running the server:**
```bash
python financial_analytics_mcp_server.py
```

The server starts and waits for client connections over stdin/stdout.

---

### MCP Server as an HTTP Service (Remote MCP)

For enterprise deployment, MCP servers typically run as HTTP services rather than local stdio processes:

```python
from mcp.server.fastmcp import FastMCP
import uvicorn

# FastMCP provides HTTP transport
mcp = FastMCP("financial-analytics-tools")

@mcp.tool()
def get_negotiated_rates(payer_id: str, procedure_code: str) -> dict:
    """
    Retrieve CMS MRF negotiated rates for a specific payer and procedure code.

    Args:
        payer_id: Payer identifier from the contract management system (e.g., BCBS-PPO-001)
        procedure_code: CPT, HCPCS, or MS-DRG code for the procedure or service.

    Returns:
        Contracted rate, rate type, effective date, and market percentile
    """
    # Implementation here
    return {"status": "success", "rates": {...}}


@mcp.tool()
def get_contribution_margin(service_line: str, period: str) -> dict:
    """
    Retrieve contribution margin data for a service line over a specified period.

    Args:
        service_line: Clinical service line name (e.g., Orthopedics, Cardiology)
        period: Reporting period in YYYY-MM or YYYY-QN format (e.g., 2026-Q1)

    Returns:
        Contribution margin details including gross revenue, direct costs, and margin percentage
    """
    # Implementation here
    return {"service_line": service_line, "period": period, "contribution_margin": {...}}


# Run as HTTP server
if __name__ == "__main__":
    uvicorn.run(mcp.get_app(), host="0.0.0.0", port=8080)
```

**Deploying as a containerized service on AWS:**

```yaml
# docker-compose.yml for local development
version: '3.8'
services:
  financial-analytics-mcp:
    build: .
    ports:
      - "8080:8080"
    environment:
      - AWS_DEFAULT_REGION=us-east-1
      - EHR_API_BASE_URL=${EHR_API_BASE_URL}
    volumes:
      - ~/.aws:/root/.aws:ro  # AWS credentials (for development only)
```

For production: Deploy as an ECS Fargate service or Lambda Function URL.

---

## Chapter 6.3 — Agent Communication Patterns

### Diagram: MCP Architecture

```
Diagram Title: MCP Server in Enterprise Healthcare Financial Analytics Architecture

Components:

[AI Applications (MCP Clients)]
  ├── Claude Desktop (developer workstation)
  ├── Custom Python Agent (Bedrock-based)
  ├── Revenue Cycle Analytics Dashboard
  └── Managed Care Contracting Tool

[MCP Gateway Layer]
  ├── Authentication (API Gateway + Cognito)
  ├── Rate limiting
  ├── Audit logging (CloudTrail)
  └── Request routing

[MCP Servers (Tool Providers)]
  ├── Claims Analytics MCP Server
  │     └── Tools: query_claims_data, get_denial_patterns, get_allowed_amounts, get_payer_mix
  │     └── Runtime: ECS Fargate
  │     └── Backend: Claims Data Warehouse
  │
  ├── Rate Transparency MCP Server
  │     └── Tools: get_negotiated_rates, compare_market_rates, get_chargemaster_rates
  │     └── Runtime: ECS Fargate
  │     └── Backend: CMS MRF API + Contract Management System
  │
  ├── Financial Forecasting MCP Server
  │     └── Tools: predict_encounter_volume, predict_price_escalation, predict_utilization_rate
  │     └── Runtime: Lambda
  │     └── Backend: SageMaker Forecasting Endpoints
  │
  └── GL/Payroll Analytics MCP Server
        └── Tools: get_contribution_margin, get_labor_costs, get_payer_mix
        └── Runtime: Lambda
        └── Backend: GL System + Payroll System

[Security & Governance Layer]
  ├── IAM: Per-server roles with least-privilege
  ├── Secrets Manager: Data warehouse and API credentials
  ├── CloudWatch: Metrics and logs for all server calls
  └── AWS WAF: Protection on API Gateway

Data Flow (Request):
  AI Client → API Gateway (authenticated) → MCP Server → Backend System → Return data
  Every step logged to CloudWatch + CloudTrail

Cross-Client Consistency:
  All clients call the same MCP servers
  Tool implementations are maintained once, used everywhere
  Updates to tool behavior automatically apply to all clients
```

### Sequence Diagram: MCP Tool Call Flow

```
Diagram Title: MCP Tool Invocation Sequence

Participants:
  AI Application (Client)
  API Gateway
  MCP Server
  Backend System (EHR API)
  CloudWatch

Sequence:

1. Initialization (happens once per session):
   Client → API Gateway: Connect, authenticate (bearer token)
   API Gateway → MCP Server: Forward authenticated connection
   MCP Server → Client: Initialize response + capabilities
   MCP Server → Client: tools/list response (available tools with schemas)

2. Tool Discovery:
   Client → MCP Server: tools/list request
   MCP Server → Client: Array of Tool objects (name, description, inputSchema)
   Client caches tool list for the session

3. Tool Invocation:
   Client → API Gateway: POST tools/call {name, arguments}
   API Gateway → MCP Server: Forward request (with auth context)
   MCP Server → CloudWatch: Log tool invocation start (tool_name, session_id)
   MCP Server: Validate arguments against inputSchema
   MCP Server → Backend System: Call EHR API with validated params
   Backend System → MCP Server: Raw data response
   MCP Server: Transform response to MCP format
   MCP Server → CloudWatch: Log tool completion (duration, status)
   MCP Server → API Gateway: tool result response
   API Gateway → Client: Tool result

4. Error Handling:
   If backend system unavailable:
   MCP Server → Client: isError: true, error message
   Client: Handles error in agent reasoning loop

Security Notes:
  - Authentication at API Gateway: OAuth2 token from Cognito
  - MCP Server's backend calls: IAM role (not user credentials)
  - All calls logged: session_id, tool_name, args (sanitized), duration, status
  - PHI never logged: only metadata and identifiers
```

---

## Chapter 6.4 — Enterprise Architecture Implications

### When MCP is the Right Pattern

MCP is the right choice when:

**You have multiple AI clients:** If you have a Claude Desktop instance for developers, a custom web application for clinical staff, and a Bedrock agent for automation — all using the same tools — MCP allows you to implement the tools once and serve all clients.

**Tool standardization is valuable:** When you want a single, authoritative implementation of "how to query patient data" or "how to check prior auth," MCP creates that single implementation.

**External developer ecosystem:** If you want to allow authorized third parties to build AI applications that use your healthcare data, MCP provides a clean API boundary.

**Separation of concerns:** Tool developers (who understand EHR APIs and payer systems) and AI application developers (who build agent workflows) can work independently.

---

### When Direct Lambda is Better

Direct Lambda integration (Bedrock Action Groups) is the right choice when:

**You're exclusively on Bedrock:** If all your AI clients are Bedrock Agents, there's no need for the additional indirection of MCP.

**Lower latency is critical:** MCP adds a network hop. For ultra-low-latency requirements, direct Lambda invocation within AWS VPC is faster.

**Simpler architecture:** MCP servers require their own deployment, authentication, and monitoring infrastructure. For simple use cases, this overhead is not justified.

**Security simplicity:** Direct Lambda to Bedrock keeps everything within AWS IAM. MCP introduces external token management.

---

### Comparison Table: Integration Patterns

| Dimension | Direct Lambda (Bedrock Action Groups) | MCP Server | API Gateway Pattern |
|-----------|--------------------------------------|------------|---------------------|
| Client compatibility | Bedrock only | Any MCP client | Any HTTP client |
| Latency | Lowest (in-VPC) | Medium (network hop) | Medium (API call) |
| Standardization | Bedrock-specific | Cross-framework | Standard HTTP |
| Authentication | AWS IAM (native) | OAuth2 / API key | API Gateway auth |
| Tool discovery | Bedrock schema | MCP tools/list | OpenAPI spec |
| Deployment complexity | Low | Medium | Low-Medium |
| Monitoring | CloudWatch (native) | Custom + CloudWatch | API Gateway + Lambda |
| Healthcare compliance | HIPAA via Bedrock BAA | Depends on deployment | Standard HIPAA controls |
| Best for | Bedrock-centric teams | Multi-client ecosystems | External integrations |
| Schema format | OpenAPI (for Bedrock) | JSON Schema (MCP native) | OpenAPI |

---

## Chapter 6.5 — Security Architecture for MCP

### Authentication and Authorization

MCP servers handling healthcare data must implement robust authentication and authorization. Key requirements:

**Authentication:** Every MCP client must prove its identity before accessing tools. Use OAuth2 with Cognito for enterprise deployments.

**Authorization:** Different clients should have access to different tools. A clinical decision support tool may need read-only EHR access; a care management system may need write access. Implement scope-based authorization.

**PHI Access Controls:**
- Patient data tools must verify the client has appropriate authorization to access the specific patient's data
- Implement patient-level access checks in every tool that returns PHI
- Audit every PHI access (who, what patient, what data, when)

**MCP Server Authentication Implementation:**

```python
from mcp.server.fastmcp import FastMCP
from functools import wraps
import boto3
import jwt
from typing import Optional

mcp = FastMCP("financial-analytics-tools")

def get_cognito_public_keys():
    """Fetch Cognito JWK for token verification."""
    import urllib.request
    COGNITO_USER_POOL_ID = "us-east-1_XXXXXXXXX"
    region = "us-east-1"
    jwks_url = f"https://cognito-idp.{region}.amazonaws.com/{COGNITO_USER_POOL_ID}/.well-known/jwks.json"
    with urllib.request.urlopen(jwks_url) as response:
        return json.loads(response.read())

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return claims."""
    try:
        # Decode header to get kid
        header = jwt.get_unverified_header(token)
        # Get matching public key
        jwks = get_cognito_public_keys()
        public_key = next(
            (k for k in jwks['keys'] if k['kid'] == header['kid']),
            None
        )
        if not public_key:
            return None
        # Verify and decode token
        claims = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience="your-app-client-id"
        )
        return claims
    except Exception:
        return None

def requires_scope(scope: str):
    """Decorator to require specific OAuth scope."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # In practice, token comes from request context
            # This is a simplified example
            token = get_current_request_token()
            claims = verify_token(token)
            if not claims:
                raise PermissionError("Invalid authentication token")
            if scope not in claims.get('scope', '').split():
                raise PermissionError(f"Required scope '{scope}' not granted")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

@mcp.tool()
@requires_scope("financial:read")
async def get_contribution_margin(service_line: str, period: str) -> dict:
    """Get contribution margin data for a service line and reporting period."""
    # Tool implementation
    ...
```

---

### Network Security for MCP Servers

For enterprise healthcare MCP deployments:

```
Network Architecture:

External MCP Clients ──► API Gateway (public endpoint, WAF)
                              │
                         [Auth: Cognito]
                              │
                    ┌─────────▼─────────┐
                    │   VPC Boundary    │
                    │                   │
                    │  MCP Server       │
                    │  (ECS Fargate     │
                    │   private subnet) │
                    │        │          │
                    │   Backend APIs    │
                    │   (EHR, Payer)    │
                    └───────────────────┘

Security controls:
- API Gateway: WAF, throttling, request validation
- VPC: MCP server in private subnet, no public IP
- Security groups: Only HTTPS inbound from API Gateway
- TLS: All traffic encrypted in transit
- Secrets Manager: Backend API credentials (never in env vars)
- CloudTrail: All API Gateway calls logged
- VPC Flow Logs: Network traffic monitoring
```

---

## Chapter 6.6 — Reflection Prompts

1. Your organization currently has Bedrock Agents using direct Lambda action groups to power a claims analytics system. The architecture team proposes migrating all tools to MCP servers to "standardize" tool access across the revenue cycle analytics platform. Make the case for and against this migration. What questions would you need answered — such as which downstream clients need to consume claims data, what latency is acceptable for denial pattern queries, and whether external auditors will need access — before recommending a decision?

2. A developer on your team argues that an MCP server exposing rate transparency data is just "API Gateway with a different JSON format." Is this correct? What does MCP provide beyond what a standard REST API Gateway provides for a rate transparency use case — particularly around tool discovery, schema enforcement, and multi-client compatibility? When would a standard REST API be a superior choice for exposing CMS MRF negotiated rates?

3. A Rate Transparency MCP server will be used by both an internal finance team querying contracted rates for managed care contract negotiations and by external auditors performing underpayment analysis. Design the authentication and authorization architecture. What scopes or roles would you define to separate internal finance access from external auditor access? How do you revoke access for a specific auditor engagement after it concludes?

4. Consider the latency implications of the MCP pattern vs. direct Lambda for a financial analytics use case: A Bedrock Agent running a contribution margin query invokes a tool. In the Lambda pattern, the call goes: Bedrock → Lambda (in AWS). In the MCP pattern: Bedrock → API Gateway → ECS → GL/Payroll data warehouse. Estimate the latency difference. At what point does this become a user-experience problem for an analyst running an interactive financial dashboard vs. a nightly batch forecasting job?

5. You are building an MCP server for coding crosswalk lookup tools (CPT to MS-DRG mapping, ICD-10 lookup, HCPCS code validation). Should this server be authenticated or unauthenticated? What are the business and compliance implications of unauthenticated access to coding crosswalk tools — consider whether these lookups could reveal proprietary charge capture logic or enable gaming of DRG optimization?

---

*End of Module 6 Textbook Content*
