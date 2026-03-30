# Course Summary: Designing and Deploying Agentic AI Systems with Amazon Bedrock
## A Postgraduate Course for Practicing Data Scientists

**Target Audience:** Healthcare data scientists transitioning from traditional ML to agentic AI systems
**Focus Domain:** Healthcare financial analytics and revenue cycle management
**Platform:** Amazon Bedrock with focus on production deployment

---

## Module 1: Foundations of Agentic AI (Weeks 1-2)

### Key Concepts

**What is Agentic AI?**
- An agentic AI system uses an LLM as a reasoning engine that dynamically selects, sequences, and invokes external tools while maintaining state across multi-step interactions
- The LLM is a component of the system, not the product itself

**The Spectrum of Intelligence:**
- **Level 1:** Single LLM Call - simple summarization, classification
- **Level 2:** Chained Prompts - predefined sequence of LLM calls
- **Level 3:** Tool-Using Agents (ReAct) - LLM decides which tools to call
- **Level 4:** Multi-Agent Systems - specialized agents coordinating on complex goals

**Six Fundamental Components of Agents:**
1. **Reasoning Engine (LLM)** - orchestrates agent behavior (Claude 3 Sonnet recommended)
2. **Tools** - functions with name, description, input schema, and execution environment
3. **Memory** - in-context, session, long-term, and semantic knowledge
4. **Knowledge** - pre-trained, RAG-retrieved, structured, and injected context
5. **Planning** - ReAct (reason + act), plan-then-execute, or hierarchical
6. **State** - current task context, tool history, entities, constraints, errors

### Healthcare Financial Analytics Applications

**Case Studies:**
- Revenue Cycle Analytics Briefing Agent (data gathering automation)
- Contract Rate Benchmarking Agent (CMS MRF analysis)
- Contribution Margin and GL Analytics Agent (multi-system integration)
- Healthcare Financial Forecasting Agent (predictive analytics)

### Why Data Scientists Struggle

The transition requires shifting from model-centric to system-centric thinking:
- The model is one component among many that can fail
- Tool descriptions are as critical as code
- Evaluation is fundamentally harder (non-deterministic, multi-step)
- Latency multiplies with each reasoning loop
- State management is complex and error-prone

**Key Takeaway:** Building production agents requires distributed systems engineering mindset, not just data science expertise.

---

## Module 2: Defining Agent Goals and Success Metrics (Week 3)

### The Metrics Challenge

Unlike supervised ML with clear metrics (accuracy, F1, AUC), agent success has multiple dimensions that must be measured holistically.

### Core Performance Metrics

1. **Task Completion Rate (TCR)** - % of sessions producing complete, correct output
   - Development: >80%, Production: >95%, Mature: >98%

2. **Tool Correctness Rate (TCR-T)** - % of tool calls that are correct
   - Dimensions: tool selection, parameter accuracy, timing

3. **Hallucination Rate** - % of outputs with unsupported factual claims
   - Healthcare target: <0.1% for financial figures, <1% for narrative

4. **Latency Metrics** - Time-based performance (p50, p95, p99)
   - Real-time clinical: <3s, Interactive analytics: <60s, Batch: N/A

5. **Cost Per Interaction** - Total AWS cost per session
   - Track: LLM tokens, Lambda execution, KB queries, data transfer

6. **Safety Metrics** - PHI exposure, financial accuracy, escalation appropriateness

### Goal Decomposition Framework

**Step 1:** Define proximal goal (what the agent accomplishes in one session)
**Step 2:** Define necessary preconditions (what must be true to succeed)
**Step 3:** Define success criteria at each step
**Step 4:** Define failure modes and severity (minor → catastrophic)

### Multi-Objective Tradeoffs

Must balance conflicting objectives:
- **Accuracy vs. Speed** - careful verification vs. fast response
- **Completeness vs. Cost** - gathering all data vs. token budgets
- **Autonomy vs. Safety** - fewer touchpoints vs. error prevention
- **Personalization vs. Consistency** - user adaptation vs. standardization

### Evaluation Frameworks

**Synthetic Evaluation Sets:** Build test scenarios with expected tool sequences and outputs

**Human Review Pipelines:**
- Development: 100% reviewed
- Beta: 30% reviewed
- Production (90 days): 10% reviewed
- Mature: 2-5% reviewed + 100% flagged outputs

**LLM-as-Judge:** Use separate LLM to evaluate outputs at scale (with calibration)

**Adversarial Prompting:** Test prompt injection, scope violations, hallucination inducement

**Key Takeaway:** Agent evaluation requires a portfolio of metrics, not a single number. Design metrics before building the agent.

---

## Module 3: Agent System Architecture (Weeks 4-5)

### The Agent Loop: Mechanics

**Step-by-Step Execution:**
1. **Context Assembly** - system prompt + tools + history + memory + user input
2. **LLM Invocation** - returns final answer, tool call, or clarification request
3. **Tool Execution** - validate, invoke, capture response (Lambda in Bedrock)
4. **Observation Injection** - append tool result to context
5. **Stopping Conditions** - natural completion, max iterations, timeout, error threshold

**Critical Understanding:** System prompt token cost is paid on every LLM call in every iteration. Optimize ruthlessly.

### Tool Registry Design

**Principles:**
1. Each tool does one thing well (don't create "super tools")
2. Tools should be idempotent where possible
3. Consistent error structures
4. Descriptions include negative information (when NOT to use)
5. Group related tools into action groups

**Tool Description Quality = Agent Performance**
- Poor descriptions cause more production failures than any other factor
- Include format, examples, and explicit constraints

### Memory Architecture

**Decision Tree:**
- Same session only? → In-context memory
- Across sessions? → External storage
- Structured data? → DynamoDB
- Semantic/unstructured? → Vector store (OpenSearch)
- Both? → Hybrid architecture

**Session Attributes in Bedrock:** Key-value pairs persist across turns within session

### State Management

Explicit state machines prevent production failures:
- Define states (INITIATED → DATA_RETRIEVED → ANALYSIS_COMPLETE)
- Validate transitions
- Enable resume after interruption
- Support audit trail
- Implement rollback

### Observability Layers

1. **Bedrock Agent Traces** - full reasoning loop with rationale and actions
2. **CloudWatch Logs** - Lambda execution logs (structured logging)
3. **CloudWatch Metrics** - custom agent-specific metrics
4. **AWS X-Ray** - distributed tracing across components

### Guardrails

**Bedrock Guardrails categories:**
- **Content Filters** - hate, violence, sexual content, misconduct
- **Topic Denial** - deny specific topics (legal advice, fraudulent billing)
- **Sensitive Information Redaction** - auto-detect and redact PII
- **Grounding Check** - require responses grounded in retrieved context

**Key Takeaway:** Understanding the agent loop at the mechanical level enables you to predict failure modes, design observability, control costs, and govern behavior.

---

## Module 4: Amazon Bedrock Deep Dive (Weeks 6-7)

### What is Amazon Bedrock?

Fully managed foundational model service with enterprise-grade features:
- Model access: Claude, Llama, Mistral, Titan, Cohere
- Bedrock Agents: Managed agentic orchestration
- Knowledge Bases: Managed RAG infrastructure
- Guardrails: Content filtering and control
- HIPAA-eligible, VPC integration, IAM-native, CloudTrail logging

**Recommended Stack for Healthcare:**
- Agent backbone: Claude 3 Sonnet (quality/cost balance)
- Simple tasks: Claude 3 Haiku
- Embeddings: Titan Embeddings V2
- High-stakes: Claude 3 Opus

### Creating a Bedrock Agent: Console Walkthrough

**Step-by-Step Process:**

1. **Navigate to Amazon Bedrock → Builder tools → Agents → Create Agent**

2. **Basic Configuration:**
   - Agent name (permanent identifier)
   - IAM role (use pre-created least-privilege role for production)
   - Foundation model selection (Claude 3 Sonnet)
   - Instructions (system prompt) - most critical field

3. **Action Groups Configuration:**
   - Name action groups descriptively
   - Choose: "Define with API schemas" (multi-function, recommended)
   - Connect to Lambda function with resource-based policy
   - Define tool schemas (OpenAPI format)

4. **Knowledge Base Attachment:**
   - Select previously created Knowledge Base
   - Write instructions for when to use KB

5. **Advanced Settings:**
   - Guardrails (attach content filters)
   - Orchestration strategy (Default = ReAct)
   - Multi-agent collaboration (if needed)

6. **Prepare Agent:**
   - Click "Prepare" to compile configuration (10-60s)
   - Status: NOT_PREPARED → PREPARING → PREPARED

### Lambda Function Requirements

**Handler format for Bedrock Agents:**
```python
def lambda_handler(event, context):
    # Parse Bedrock event structure
    action_group = event['actionGroup']
    api_path = event['apiPath']
    parameters = event.get('parameters', [])

    # Execute tool logic
    result = execute_tool(api_path, parameters)

    # Return Bedrock-formatted response
    return {
        'actionGroup': action_group,
        'apiPath': api_path,
        'httpStatusCode': 200,
        'responseBody': {'application/json': {'body': json.dumps(result)}}
    }
```

**Resource-based policy required:**
```bash
aws lambda add-permission \
  --function-name your-function \
  --principal bedrock.amazonaws.com \
  --source-arn "arn:aws:bedrock:region:account:agent/*"
```

### Testing and Debugging

**Console Test Interface:**
- Test pane on right side of Agent Builder
- Enter test queries, click "Run"
- Enable "Show trace" to see reasoning steps

**Trace Interpretation:**
Each orchestration step shows:
- Rationale (agent's reasoning)
- Action invocation (tool name, parameters)
- Observation (tool result)

**Common Failure Signatures:**
1. "I don't have a tool for that" → Improve tool description
2. Parameter format errors → Add format examples to schema
3. Repeated tool calls → System prompt or context management issue
4. Lambda invocation error → Check function ARN and permissions
5. Permission denied → Check both IAM policy and resource-based policy

### Versions and Aliases

**Production Deployment Flow:**
1. Edit agent configuration (DRAFT)
2. Test DRAFT thoroughly
3. Create Version (immutable snapshot → v1, v2, etc.)
4. Update Alias to point to new version ("production" → v2)
5. Application code always calls alias (not version directly)
6. Rollback = update alias back to previous version

**Key Takeaway:** Never deploy DRAFT to production. Always use versions and aliases for stability and rollback capability.

---

## Module 5: Knowledge Bases in Amazon Bedrock (Week 8)

### What Knowledge Bases Solve

LLMs have static training data and may hallucinate. Knowledge Bases enable:
- **Accuracy** - retrieval from authoritative sources
- **Currency** - update without retraining
- **Auditability** - cite specific sources
- **Scope control** - constrain to curated corpus

### RAG Architecture

**Ingestion Pipeline (run once, then on updates):**
1. Documents in S3 (PDF, DOCX, HTML, TXT, CSV, MD)
2. Document Loader extracts text
3. Text Chunker splits into overlapping chunks (300 tokens default, 20% overlap)
4. Titan Embeddings V2 converts to 1,536-dimensional vectors
5. OpenSearch Serverless stores vectors + original text + metadata

**Query Pipeline (at inference time):**
1. User/agent query converted to vector
2. k-NN search finds most similar chunks
3. Optional re-ranking and metadata filtering
4. Chunks injected into agent context
5. LLM generates grounded response with citations

### Creating a Knowledge Base: Key Decisions

**Chunking Strategy:**
| Document Type | Strategy | Chunk Size | Rationale |
|--------------|----------|------------|-----------|
| IPPS final rules | Fixed size | 512 tokens | Balance completeness/precision |
| MS-DRG manual | Hierarchical | 256/1024 | Clear section structure |
| Contract summaries | Semantic | Auto | Semantic structure |
| Rate tables | Fixed size | 256 tokens | Precise table retrieval |

**Embedding Model:**
- **Titan Embeddings V2** (recommended) - 1024 dimensions, HIPAA-eligible, no data egress
- **Cohere Multilingual** - If non-English content

**Vector Store:**
- **OpenSearch Serverless** (recommended) - Fully managed, HIPAA-eligible, native AWS integration
- **Cost:** ~$175/month baseline (2 OCUs × 24/7 × $0.24/OCU-hour)

### Advanced Patterns

**Metadata Filtering:**
```python
retrieval_filter = {
    "andAll": [
        {"equals": {"key": "payer_id", "value": "BCBS-001"}},
        {"greaterThanOrEquals": {"key": "effective_year", "value": "2026"}}
    ]
}
```

**Hybrid Retrieval:**
Combine semantic similarity with keyword matching (BM25):
```python
'overrideSearchType': 'HYBRID'  # vs. 'SEMANTIC' (default)
```

### Compliance Considerations

1. **Proprietary contract terms** - access-control with S3 policies
2. **Document currency** - sync schedule aligned with CMS updates, metadata flags
3. **Source attribution** - always cite sources in agent responses
4. **Separation of concerns** - KB for methodology, tools for live rate data

**Key Takeaway:** Chunking strategy is the most impactful configuration decision. Test retrieval quality before connecting to agent.

---

## Module 6: MCP (Model Context Protocol) Servers (Week 9)

### What is MCP?

**Problem:** Every AI framework has its own way of defining tools (LangChain, Bedrock, CrewAI, etc.)

**Solution:** MCP is an open standard protocol for how AI applications (clients) communicate with tool providers (servers). The "HTTP of AI tool integration."

**Promise:** Write a tool once (as MCP server), use in any MCP-compatible client.

### MCP Protocol

**Defines:**
- **Transport:** stdio (local) or HTTP+SSE/WebSocket (remote)
- **Message format:** JSON-RPC 2.0
- **Capabilities:** Tools, Resources, Prompts, Sampling
- **Lifecycle:** Initialize → List tools → Call tool → Handle response

### Building an MCP Server

**Minimal Python MCP Server:**
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("financial-analytics-tools")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name="get_negotiated_rates", description="...", inputSchema={...})]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    result = await handle_tool(name, arguments)
    return [TextContent(type="text", text=json.dumps(result))]
```

**HTTP Service (Enterprise):**
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("financial-analytics-tools")

@mcp.tool()
def get_negotiated_rates(payer_id: str, procedure_code: str) -> dict:
    """Tool implementation"""
    return {"status": "success", "rates": {...}}
```

### When to Use MCP vs. Direct Lambda

**Use MCP when:**
- Multiple AI clients (Claude Desktop, custom apps, Bedrock agents)
- Tool standardization across framework is valuable
- External developer ecosystem
- Separation of tool/agent developers

**Use Direct Lambda when:**
- Exclusively on Bedrock
- Lower latency critical (no network hop)
- Simpler architecture
- Security simplicity (keep in AWS IAM)

### Security Architecture for MCP

**Authentication:** OAuth2 with Cognito for enterprise deployments

**Authorization:** Scope-based access control per client

**PHI Access Controls:**
- Patient-level access checks in every tool
- Audit every PHI access

**Network Security:**
```
External Clients → API Gateway (WAF) → Auth (Cognito)
                         ↓
                    VPC Boundary
                         ↓
                  MCP Server (ECS Fargate)
                         ↓
                   Backend APIs (EHR)
```

**Key Takeaway:** MCP standardizes tool access across frameworks, but adds architectural complexity. Evaluate whether multi-client support justifies the overhead.

---

## Module 7: Productionizing Agent Systems (Weeks 10-11)

### The Demo Gap

**Why demos fail in production:**
- Non-determinism amplifies at scale
- Integration failures multiply
- Load reveals hidden assumptions
- Cost scales unexpectedly
- User behavior diverges from tests

### CI/CD Pipeline for Agents

**6-Stage Pipeline:**

1. **Static Validation** - Unit tests, schema validation, IAM checks, PHI scanning
2. **Integration Tests** - Tool-level tests against mocks, error paths, latency, permissions
3. **Agent Evaluation** - 100+ synthetic scenarios, task completion rate, tool correctness, adversarial tests
4. **Human Review Gate** - Clinical expert review, 0 critical failures required
5. **Staging Deployment** - Real services with test data, smoke tests, canary sessions
6. **Production Deployment** - Alias update, traffic shifting, monitoring, auto-rollback

### Infrastructure as Code

**AWS CDK for Bedrock Agents:**
- Lambda functions with execution roles
- Bedrock Agent with IAM role
- CloudWatch alarms and dashboards
- Budget alerts
- Reproducible across environments

### Observability Stack

**5 Layers:**

1. **Business Metrics** - Analyses initiated/completed, underpayments identified, acceptance rate
2. **Technical Performance** - Latency (p50/p95/p99), success rate, token consumption
3. **Cost Monitoring** - Daily LLM cost, cost per session, monthly spend
4. **Quality Metrics** - Completion rate, escalation rate, human review scores
5. **Security & Compliance** - Guardrail triggers, failed auth, unusual access

### Cost Controls

**Multi-Layer Rate Limiting:**
1. **Bedrock Service Quotas** - Request limit increases proactively
2. **Application-Level** - DynamoDB token bucket (per user, per org)
3. **Session Token Limits** - Cap tokens per session to prevent runaway

**AWS Budgets:** Alert at 80% of budget, forecasted overrun

### Error Taxonomy

**6 Categories:**
1. **Transient Infrastructure** - Retry with backoff
2. **Tool Input Errors** - Return to agent for correction
3. **Data Not Found** - Structured "not found" response
4. **Business Logic Violations** - Explain constraint, suggest alternatives
5. **Permissions/Authorization** - Escalate, do NOT retry
6. **Unhandled/Unknown** - Log all context, escalate, capture reference ID

### Human Override Patterns

1. **Review and Approve** - Agent prepares, human approves, then execute
2. **Exception-Based** - Agent proceeds, humans can override if error detected
3. **Audit and Retrospective** - Agent completes, sample audited afterward (low-consequence only)

### Healthcare Governance

**Required Framework:**
- **AI Ethics Committee** - Review use cases, establish policies, investigate incidents
- **Risk Assessment** - Clinical accuracy, compliance, operational, reputational, financial
- **Model Cards** - Document capabilities, limitations, evaluation, accountability
- **Incident Response** - Define escalation, rollback, breach notification process

**HIPAA Requirements:**
- Business Associate Agreement with AWS
- Minimum Necessary access
- Access Controls (IAM)
- Audit Controls (CloudTrail)
- Transmission Security (TLS/HTTPS)
- Breach Notification (within 60 days)

**FDA SaMD Considerations:**
If agent informs clinical decisions, may require:
- Pre-market review
- Predetermined change control plans
- Real-world performance monitoring

### Production Architecture

**Complete Stack:**
- Application Tier: ALB → ECS Fargate → API Gateway → Bedrock
- Agent Tier: Bedrock Agent + Action Groups + Knowledge Base
- Data Tier: DynamoDB (state/limits), S3 (docs/audit), External systems
- Security: IAM, Secrets Manager, KMS, Cognito, WAF
- Observability: CloudWatch, CloudTrail, X-Ray
- CI/CD: GitHub/CodeCommit → CodeBuild → Evaluation → CodeDeploy

**Availability Targets:**
- 99.9% uptime (43.8 min downtime/month)
- RTO: 30 minutes
- RPO: 1 hour

**Key Takeaway:** Production deployment requires CI/CD, comprehensive monitoring, cost controls, error handling, human oversight, and governance infrastructure. It is not a "set and forget" system.

---

## Cross-Module Themes

### 1. Healthcare-Specific Considerations

Throughout all modules, the course emphasizes:
- **HIPAA compliance** - BAA, audit trails, access controls, breach notification
- **Financial accuracy** - Rate calculations, underpayment detection, forecasting
- **Regulatory constraints** - CMS rules, payer contracts, FDA SaMD guidance
- **Audit requirements** - SOX compliance, source attribution, decision traceability
- **Patient safety** - Human override, escalation paths, guardrails

### 2. From Model-Centric to System-Centric

**Data scientists must learn:**
- The LLM is one component in a larger system
- Tool descriptions are as critical as code
- Non-determinism requires portfolio metrics, not single numbers
- State management is complex and requires explicit design
- Cost is a design constraint, not an afterthought
- Observability must be designed in, not added later

### 3. Production-Ready Checklist

Before deploying to production:
- [ ] Synthetic evaluation set (100+ scenarios, >95% pass rate)
- [ ] Human review pipeline (calibrated reviewers, documented rubrics)
- [ ] Adversarial testing (50+ scenarios, prompt injection, scope violations)
- [ ] Cost model and budget alerts
- [ ] Rate limiting (service, application, session levels)
- [ ] CloudWatch dashboards (business, technical, cost, quality, security)
- [ ] Incident response playbook
- [ ] Rollback procedure tested
- [ ] HIPAA compliance verified (BAA, audit controls, access controls)
- [ ] Governance review and sign-off

### 4. Key Technical Decisions

**Agent Type:**
- Simple queries → Single LLM call
- Fixed workflows → Prompt chains
- Unknown pathways → ReAct agent
- Complex delegation → Multi-agent system

**Model Selection:**
- Reasoning quality required → Claude 3 Sonnet or Opus
- High volume, simple tasks → Claude 3 Haiku
- Cost-sensitive → Haiku or Titan Express

**Tool Pattern:**
- Bedrock-only → Direct Lambda (Action Groups)
- Multi-client ecosystem → MCP servers
- External partners → API Gateway + OpenAPI

**Knowledge Base:**
- Methodology/reference docs → Bedrock Knowledge Base (RAG)
- Live data lookups → Tools (Lambda to database/API)
- Both needed → Hybrid (KB + tools)

---

## Course Capstone Project

Students design, implement, and defend a complete agentic AI system for a healthcare use case.

**Required Components:**
1. Architecture document with diagram
2. Working Bedrock agent with ≥2 action groups
3. Knowledge base with real or synthetic corpus
4. Evaluation report against defined metrics
5. Governance and risk assessment memo
6. 20-minute defended presentation

**Acceptable Domains:**
- Revenue cycle management
- Clinical decision support
- Care coordination
- Utilization management and prior authorization
- Quality reporting and HEDIS tracking
- Patient communication and chronic disease management
- Pharmacy benefits management

---

## Final Takeaways

### For Data Scientists Entering This Field:

1. **Agentic AI is system design, not model optimization** - Success requires distributed systems thinking, not just ML expertise

2. **Non-determinism is the norm** - Design for it with portfolio metrics, human review, and comprehensive logging

3. **Healthcare requires governance** - Technical excellence is necessary but not sufficient. Compliance, audit trails, and incident response are mandatory

4. **Cost is a first-class concern** - At scale, agent costs can be substantial. Design with cost awareness from day one

5. **Evaluation never ends** - Build evaluation infrastructure as a first-class artifact. Systems without ongoing evaluation cannot be safely improved

6. **Build for the long term** - Version everything, test relentlessly, own failures, center on healthcare impact

### The Opportunity

Healthcare financial analytics is an ideal domain for agentic AI:
- Multi-step, multi-source workflows (claims, rates, GL, forecasting)
- Heterogeneous data (structured + unstructured, internal + external)
- Clear success metrics (underpayment identification, forecast accuracy)
- High-value outcomes (revenue optimization, contract negotiations)
- Human-in-the-loop appropriate (recommend, don't act autonomously)

The systems you build today will shape how healthcare organizations make financial decisions for years to come. Build them well.

---

**Course Version:** 0.1.0
**Last Updated:** 2026-02-04
**Platform:** Amazon Bedrock with AWS foundational services
**Prerequisites:** Python 3.9+, AWS fundamentals, ML pipelines, basic prompt engineering
