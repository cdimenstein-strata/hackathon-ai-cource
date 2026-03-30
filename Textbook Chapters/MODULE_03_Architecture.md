# MODULE 3: Agent System Architecture
## Weeks 4–5 | Textbook Content

---

## Chapter 3.1 — The Agent Loop: Mechanics and Internals

### What Actually Happens When You "Run an Agent"

When a student first encounters an agent framework — whether LangChain, CrewAI, Bedrock Agents, or a custom implementation — there is a tendency to treat the agent as a black box: input goes in, output comes out, magic in the middle. This is the most dangerous mental model you can bring to production agent design.

You must understand, at the mechanical level, exactly what happens during agent execution. This understanding is what allows you to predict failure modes, design observability, control costs, and govern behavior.

**The agent loop in detail:**

#### Step 1: Context Assembly

Before the LLM sees anything, the agent system assembles the full context. This includes:

- **System prompt:** The role definition, behavioral guidelines, constraints, and capability description
- **Tool definitions:** The complete list of available tools with names, descriptions, and input schemas (in JSON Schema format)
- **Conversation history:** All prior messages in the current session
- **Memory injections:** Any relevant content retrieved from external memory at session start
- **Current user input:** The latest message from the user

All of this becomes the input to the first LLM call. The total token count of this input determines the base cost and base latency of every agent step.

**Practical implication:** A system prompt that is 8,000 tokens long costs 8,000 tokens × input token price on every single LLM call in every agent loop iteration. If your agent runs 6 loop iterations, your system prompt alone costs 48,000 input tokens per session. Optimize your system prompt ruthlessly.

---

#### Step 2: LLM Invocation and Structured Output

The assembled context is sent to the LLM. The LLM returns one of three response types:

**Final Answer:** The LLM determines it has enough information to respond to the user. It generates the final response and the loop ends.

**Tool Call:** The LLM determines it needs to take an action. It returns a structured tool call specification:

```json
{
  "type": "tool_use",
  "name": "query_claims_data",
  "input": {
    "date_range": "2025-01-01/2025-12-31",
    "service_line": "orthopedics",
    "payer_id": "BCBS-IL-001",
    "procedure_codes": ["27447", "27446"]
  }
}
```

**Clarification Request:** The LLM determines it cannot proceed without more information from the user.

**Critical technical point:** Modern frontier LLMs (Claude 3, GPT-4, Gemini) are explicitly trained to produce structured tool calls. This is not prompt engineering — it is a capability built into the model through fine-tuning on tool-use examples. Smaller or older models may not reliably produce well-structured tool calls, which is why model selection matters for agentic systems.

---

#### Step 3: Tool Execution

When the LLM returns a tool call, the agent framework:

1. Parses the tool call to extract tool name and parameters
2. Validates that the tool exists in the registry
3. Validates that the parameters match the tool's input schema
4. Invokes the tool (in Bedrock Agents, this means calling the Lambda function behind the action group)
5. Waits for the tool to return (or times out)
6. Captures the tool's response

**What can go wrong at this step:**
- The LLM generates a tool call with incorrect parameter names (the schema doesn't match)
- The LLM generates a tool call with parameters of the wrong type (sends a number where a string is expected)
- The tool throws an exception
- The tool times out (Lambda has a maximum execution time of 15 minutes, but Bedrock Agents has an internal timeout)
- The tool returns more data than can fit in the remaining context window
- The tool returns an error that the agent must handle gracefully

**Error handling design principle:** Every tool should return a structured response that includes a status field. Never return a raw exception to the agent. Return:

```json
{
  "status": "error",
  "error_code": "CLAIM_NOT_FOUND",
  "error_message": "No claims found for claim_id CLM-98432. Please verify the claim identifier.",
  "data": null
}
```

This gives the agent actionable information it can reason about, rather than a stack trace it cannot interpret.

---

#### Step 4: Observation Injection

The tool's response (the "observation") is appended to the agent's context as an "observation" message. The full context now includes:

- [Everything from before] + [The tool call the LLM made] + [The tool's response]

The LLM reads this complete context and makes its next decision.

**The context window management problem:** Each loop iteration adds the tool call and observation to the context. After several iterations, especially if tools return large responses, the context window may fill. When context fills:
- The agent may start dropping early context
- Reasoning quality degrades
- The agent may forget what it was originally trying to do

**Mitigation strategies:**
- Limit tool response sizes (truncate large responses to essential information)
- Summarize long tool results before injecting them
- Design tools to return only what the agent needs (don't return entire claims data dumps when you only need the denial reason summary)
- Use context window monitoring to detect when you're approaching limits

---

#### Step 5: Stopping Conditions

The agent loop must have well-defined stopping conditions:

**Natural completion:** The LLM produces a final answer.

**Maximum iterations:** The system enforces a maximum number of loop iterations. In Bedrock Agents, this is configurable. Without a maximum, a looping agent can run indefinitely, spending money and degrading user experience.

**Timeout:** The system enforces a maximum total execution time.

**Error threshold:** After N consecutive tool failures, the agent stops and escalates to human review.

**Human escalation trigger:** The agent itself determines that the task requires human judgment beyond its capabilities.

**In Bedrock Agents:** The maximum number of orchestration steps is configurable per agent (default and maximum vary by model). Plan your expected workflow depth and set the limit with headroom (e.g., if a normal workflow is 6 steps, set the maximum to 12 to allow for error recovery while preventing infinite loops).

---

### Sequence Diagram: ReAct Agent Execution

```
Diagram Title: ReAct Agent Full Execution Sequence

Participants:
  User
  Agent API (Bedrock Agents API)
  Orchestrator (internal to Bedrock)
  Foundation Model (Claude 3 Sonnet)
  Tool Registry
  Lambda (action group backend)
  Knowledge Base
  CloudWatch

Sequence:

1. User → Agent API: InvokeAgent(query, session_id)

2. Agent API → Orchestrator: Begin orchestration

3. Orchestrator → CloudWatch: Log session start

4. Orchestrator → Foundation Model:
   LLM Call 1
   Input: {system_prompt, tool_definitions, conversation_history, user_query}
   Output: {thought: "I need to retrieve claims data for this service line", action: query_claims_data, params: {service_line: "orthopedics", date_range: "2025-01-01/2025-12-31", payer_id: "BCBS-IL-001"}}

5. Orchestrator → CloudWatch: Log LLM call (input tokens, output tokens, latency)

6. Orchestrator → Tool Registry: Lookup action group for "query_claims_data"

7. Orchestrator → Lambda: Invoke(function_arn, input_payload)

8. Lambda → External API: Claims data warehouse query

9. External API → Lambda: Claims encounter JSON

10. Lambda → Orchestrator: Tool result (claims summary JSON)

11. Orchestrator → CloudWatch: Log tool invocation (tool name, params, result summary, latency)

12. Orchestrator → Foundation Model:
    LLM Call 2
    Input: {full_prior_context + tool_result_observation}
    Output: {thought: "I have claims volume. Now I need negotiated rates to identify underpayments.", action: get_negotiated_rates, params: {payer_id: "BCBS-IL-001", procedure_code: "27447"}}

13. [Repeat steps 7-12 for each tool call]

14. On final LLM call:
    Orchestrator → Foundation Model:
    Input: {full_context_with_all_observations}
    Output: {final_answer: "Underpayment analysis for CPT 27447 total knee arthroplasty complete. BCBS-IL is paying 12% below contracted rate across 47 claims..."}

15. Orchestrator → CloudWatch: Log session completion (total tokens, total cost, step count, duration)

16. Orchestrator → Agent API: Return final answer + trace

17. Agent API → User: Response + optional trace

Note: All steps run within Bedrock's managed infrastructure.
The caller sees only the final response unless they request the trace.
```

---

## Chapter 3.2 — Planning Cycles

### Single-Shot vs. Iterative Planning

**Single-shot planning (Plan-then-Execute):**
The agent creates a complete plan first, then executes each step without re-planning. Faster if the plan is correct; brittle if early steps fail or reveal new information that invalidates the plan.

```python
# Conceptual Plan-then-Execute implementation
def plan_then_execute_agent(goal: str, tools: list) -> str:
    # Phase 1: Planning
    plan = llm.generate(f"""
        Goal: {goal}
        Available tools: {tools}
        Create a step-by-step execution plan.
    """)

    # Phase 2: Execution
    results = []
    for step in plan.steps:
        result = execute_tool(step.tool, step.params)
        results.append(result)
        # Note: We don't re-plan based on results

    # Phase 3: Synthesis
    return llm.generate(f"Given these results: {results}, answer: {goal}")
```

**When single-shot planning fails:** If step 3's result reveals that step 4 was wrong, a plan-then-execute agent will run step 4 anyway. The rigid plan cannot adapt.

**Iterative planning (ReAct):**
After each tool call, the agent re-evaluates: is the plan still correct? Do I need to adjust my next step? This is more robust but more expensive (more LLM calls per session).

**Bedrock Agents use iterative planning (ReAct) by default.** This is the right choice for healthcare financial analytics use cases where unexpected findings — such as discovering a payer is systematically underpaying on a procedure code — require re-routing the analysis mid-session.

---

### Multi-Turn Planning (Human-in-the-Loop)

Some healthcare financial workflows are too complex or too high-stakes for fully autonomous planning. Multi-turn planning builds human checkpoints into the agent's workflow:

```
Agent completes Phase 1 → Presents findings to human → Human approves/redirects
→ Agent completes Phase 2 → Presents recommendations → Human approves/modifies
→ Agent executes approved actions
```

**Implementation in Bedrock:** This pattern is implemented using Bedrock Agent's "return of control" feature, where the agent returns a response to the user at a checkpoint, waits for human input, and then continues in the same session.

---

## Chapter 3.3 — Tool Registry Design

### The Tool Registry as an Architectural Component

The tool registry is the catalog of all functions available to an agent. In Bedrock Agents, the tool registry is defined through Action Groups, each backed by a Lambda function (or an OpenAPI schema endpoint).

**Tool registry design principles:**

**1. Each tool should do one thing well.**
A tool called `process_financial_data` that retrieves claims, looks up negotiated rates, checks contribution margins, and forecasts encounter volumes is an anti-pattern. It's expensive (runs even when you only need one piece of information), hard to test, and gives the agent poor decision-making signals (it can't choose to get just the rate data). Split it into four tools.

**2. Tools should be idempotent where possible.**
If an agent calls the same tool twice with the same parameters (due to a reasoning loop or error recovery), should it produce the same result? For read operations, yes. For write operations, you need idempotency guarantees — otherwise a loop can submit the same rate dispute filing multiple times.

**3. Tools should return consistent error structures.**
The LLM reads tool results as text and must interpret what happened. Consistent error structures allow the agent to reason about errors predictably.

**4. Tool descriptions should include negative information.**
Tell the agent when NOT to use a tool, not just when to use it.

```json
{
  "name": "get_negotiated_rates",
  "description": "Retrieves payer-specific contracted rates for a procedure code from CMS Machine Readable Files (MRFs). Use this tool ONLY when you need to compare what a payer is contractually obligated to pay. Do NOT use this tool for historical payment lookups — use get_allowed_amounts instead. Do NOT use this tool for chargemaster gross charges — use get_chargemaster_rates instead.",
  "parameters": {...}
}
```

**5. Consider tool grouping.**
Related tools can be grouped into action groups. This helps the LLM understand the organizational structure and can improve tool selection accuracy for complex tool sets.

---

### Action Schema Design

Every tool exposed to a Bedrock Agent must have an OpenAPI-compatible schema. This schema is what Bedrock uses to:
1. Generate the tool definition the LLM reads
2. Validate tool call parameters
3. Route the call to the correct Lambda function

**Full tool schema example:**

```yaml
openapi: "3.0.0"
info:
  title: "Healthcare Financial Analytics API"
  version: "1.0.0"
paths:
  /get-negotiated-rates:
    post:
      operationId: "getNegotiatedRates"
      summary: "Retrieve payer-specific contracted rates for a procedure code"
      description: >
        Retrieves the current negotiated rate for a procedure code from
        CMS Machine Readable Files (MRFs), including contracted rate,
        rate type (fee schedule vs. percentage of billed charges), and
        effective date. Use when you need to identify whether actual
        payments are consistent with contracted rates or to support
        managed care contract renegotiations.
        Returns rates current as of the most recent MRF publication.
        Do NOT use for historical rate trend analysis — use compare_market_rates instead.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - payer_id
                - procedure_code
              properties:
                payer_id:
                  type: string
                  description: "Payer identifier. Format: alphanumeric payer code (e.g., BCBS-IL-001)."
                procedure_code:
                  type: string
                  description: "CPT, HCPCS, or MS-DRG code (e.g., '27447' for total knee arthroplasty, '470' for MS-DRG major joint replacement)."
      responses:
        "200":
          description: "Rate retrieved successfully"
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    enum: [success, error]
                  rate:
                    type: object
                    properties:
                      payer_name:
                        type: string
                      procedure_code:
                        type: string
                      negotiated_rate:
                        type: number
                      rate_type:
                        type: string
                      effective_date:
                        type: string
                      expiration_date:
                        type: string
                  error_message:
                    type: string
```

---

## Chapter 3.4 — Memory Storage Architecture

### Memory Architecture Decision Tree

```
Question 1: Does this agent need to remember anything beyond the current conversation?
  No → Use only in-context memory (conversation window)
  Yes → Continue

Question 2: Does it need to remember facts from the current session for future steps?
  Yes, within same session → Use session attributes (Bedrock built-in)
  Yes, across sessions → Need external storage → Continue

Question 3: What type of information needs to persist?
  Structured (user prefs, service line IDs, status flags) → DynamoDB
  Unstructured/semantic (past summaries, analysis narratives) → Vector store (OpenSearch)
  Both → Hybrid architecture
```

### In-Context Memory (Conversation Window)

Everything in the current conversation is "in-context memory." It's automatically managed by Bedrock Agents within a session.

**Capacity planning:**
- Claude 3 Sonnet: 200K token context window
- Practical working limit (to preserve reasoning quality): 100K-150K tokens
- Average token consumption per agent step: 2K-8K tokens (depending on tool response sizes)
- Estimated comfortable session depth: 15-40 meaningful steps before context management becomes critical

**When you approach context limits:**
- Implement conversation summarization: replace early conversation segments with a compact summary
- Filter tool results: return only the fields the agent actually needs
- Use structured extraction: instead of returning a full claims data export (5,000 tokens), extract the relevant denial reason and payment summary (500 tokens) in the Lambda function

---

### Session State (Bedrock Session Attributes)

Bedrock Agents supports session attributes — key-value pairs that persist across turns within a session and can be updated by both the caller and the Lambda functions.

**Use cases for session attributes:**
- Storing the current service line identifier after first lookup (avoid re-fetching)
- Tracking which tools have already been called (prevent duplicate calls)
- Storing workflow state flags (e.g., "negotiated_rates_retrieved": true)
- Accumulating a list of identified underpayment discrepancies

**Setting session attributes from Lambda:**

```python
def lambda_handler(event, context):
    session_attributes = event.get('sessionAttributes', {})

    # Process request
    claims_data = query_claims_warehouse(event['parameters']['service_line'],
                                         event['parameters']['date_range'])

    # Update session attributes for use in subsequent steps
    session_attributes['service_line'] = claims_data['service_line']
    session_attributes['payer_id'] = claims_data['top_payer_id']
    session_attributes['analysis_period'] = claims_data['date_range']

    return {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': 200,
        'responseBody': {
            'application/json': {
                'body': json.dumps({
                    'status': 'success',
                    'data': claims_data
                })
            }
        },
        'sessionAttributes': session_attributes
    }
```

---

### External Long-Term Memory (Cross-Session)

For agents that need to remember things across sessions — analyst preferences, historical analysis runs, accumulated rate negotiation context — you need external storage.

**Architecture pattern:**

```python
# On session start: inject relevant memory into context
def load_analyst_agent_context(service_line: str, session_id: str) -> str:
    """
    Called before starting a new agent session.
    Retrieves relevant context from external memory stores.
    """

    # 1. Structured memory from DynamoDB
    ddb_context = get_service_line_agent_history(service_line)

    # 2. Semantic memory from vector store
    embedding = get_embedding("service line financial analysis context")
    semantic_context = vector_search(
        collection="financial_agent_memory",
        vector=embedding,
        filter={"service_line": service_line},
        top_k=3
    )

    # 3. Format as context injection
    memory_context = f"""
    SERVICE LINE HISTORY CONTEXT:
    Previous analyses: {ddb_context['analysis_count']}
    Last analysis run: {ddb_context['last_analysis_date']}
    Known payer issues: {ddb_context['flagged_payers']}
    Outstanding items from last session: {ddb_context['outstanding_items']}
    Previous summaries: {[s['summary'] for s in semantic_context]}
    """

    return memory_context
```

**Data governance consideration:** External memory stores that contain financial data and encounter-level details require appropriate access controls: encryption at rest (KMS), encryption in transit (TLS), access logging (CloudTrail), minimum necessary access (IAM), and retention policies consistent with your organization's data governance standards.

---

## Chapter 3.5 — State Persistence

### The State Machine Perspective

Every non-trivial agent is implicitly a state machine. Making the states explicit and managing transitions explicitly is what separates production agents from demo agents.

**Explicit state management pattern:**

```python
from enum import Enum
from dataclasses import dataclass
from typing import Optional, List
import boto3
import json

class FinancialAnalysisWorkflowState(Enum):
    INITIATED = "initiated"
    CLAIMS_DATA_RETRIEVED = "claims_data_retrieved"
    RATES_FETCHED = "rates_fetched"
    DISCREPANCIES_IDENTIFIED = "discrepancies_identified"
    FORECAST_GENERATED = "forecast_generated"
    DRAFT_CREATED = "draft_created"
    PENDING_REVIEW = "pending_review"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    DISPUTED = "disputed"
    APPEALING = "appealing"
    COMPLETE = "complete"
    FAILED = "failed"

@dataclass
class FinancialAnalysisWorkflowContext:
    workflow_id: str
    service_line: str
    procedure_code: str
    payer_id: str
    state: FinancialAnalysisWorkflowState
    retrieval_results: dict
    draft_content: Optional[str]
    review_approved: bool
    submission_tracking_id: Optional[str]
    error_history: List[dict]
    created_at: str
    last_updated: str

class WorkflowStateManager:
    def __init__(self, table_name: str = "financial-analysis-workflow-states"):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def save_state(self, context: FinancialAnalysisWorkflowContext):
        self.table.put_item(Item={
            'workflow_id': context.workflow_id,
            'service_line': context.service_line,
            'state': context.state.value,
            'context_json': json.dumps(context.__dict__, default=str),
            'ttl': int(time.time()) + (30 * 24 * 60 * 60)  # 30 day TTL
        })

    def load_state(self, workflow_id: str) -> Optional[FinancialAnalysisWorkflowContext]:
        response = self.table.get_item(Key={'workflow_id': workflow_id})
        if 'Item' not in response:
            return None
        return FinancialAnalysisWorkflowContext(**json.loads(response['Item']['context_json']))

    def transition_state(self, workflow_id: str, new_state: FinancialAnalysisWorkflowState,
                         update_data: dict = None):
        context = self.load_state(workflow_id)
        if context is None:
            raise ValueError(f"Workflow {workflow_id} not found")

        # Validate transition is legal
        legal_transitions = {
            FinancialAnalysisWorkflowState.INITIATED: [FinancialAnalysisWorkflowState.CLAIMS_DATA_RETRIEVED, FinancialAnalysisWorkflowState.FAILED],
            FinancialAnalysisWorkflowState.CLAIMS_DATA_RETRIEVED: [FinancialAnalysisWorkflowState.RATES_FETCHED, FinancialAnalysisWorkflowState.FAILED],
            # ... etc.
        }

        if new_state not in legal_transitions.get(context.state, []):
            raise ValueError(f"Illegal state transition: {context.state} → {new_state}")

        context.state = new_state
        context.last_updated = datetime.utcnow().isoformat()
        if update_data:
            for key, value in update_data.items():
                setattr(context, key, value)

        self.save_state(context)
        return context
```

**Why explicit state management matters:**
- You can resume interrupted workflows
- You can audit the complete history of any workflow
- You can implement correct idempotency (check if a step has been completed before re-doing it)
- You can support human override at any state
- You can implement rollback

---

## Chapter 3.6 — Observability and Tracing

### Observability Layers for Agents

An agent without observability is a black box in production. When something goes wrong — and something will go wrong — you need to know: what happened, when, in what sequence, with what inputs, and with what outputs.

**Layer 1: Bedrock Agent Traces**

Amazon Bedrock Agents provides built-in tracing that captures the full reasoning loop. The trace includes:

```json
{
  "traceId": "trace-123-abc",
  "orchestrationTrace": {
    "modelInvocationInput": {
      "text": "[The full prompt sent to the LLM]",
      "traceId": "trace-123-abc-step-1"
    },
    "modelInvocationOutput": {
      "parsedResponse": {
        "isValid": true,
        "value": "[The LLM's response]"
      }
    },
    "rationale": {
      "text": "I need to retrieve the negotiated rates for CPT 27447 before comparing against actual allowed amounts to identify underpayments.",
      "traceId": "trace-123-abc-step-1-rationale"
    },
    "invocationInput": {
      "actionGroupInvocationInput": {
        "actionGroupName": "ClaimsAnalyticsGroup",
        "apiPath": "/get-negotiated-rates",
        "parameters": [
          {"name": "payer_id", "value": "BCBS-IL-001"},
          {"name": "procedure_code", "value": "27447"}
        ]
      }
    },
    "observation": {
      "actionGroupInvocationOutput": {
        "text": "{\"status\": \"success\", \"rate\": {...}}"
      }
    }
  }
}
```

**Layer 2: CloudWatch Logs**

Lambda functions write execution logs to CloudWatch. Every tool call produces log entries. This is separate from Bedrock's trace — it's the tool-side record of what happened.

**Structured logging for Lambda tools:**

```python
import json
import logging
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    start_time = time.time()

    # Extract request info
    action_group = event['actionGroup']
    api_path = event['apiPath']
    # Log only non-sensitive identifiers in CloudWatch
    service_line = event['parameters'].get('service_line', 'unknown')
    payer_id = event['parameters'].get('payer_id', 'unknown')

    logger.info(json.dumps({
        "event": "tool_invoked",
        "tool_name": f"{action_group}{api_path}",
        "request_id": context.aws_request_id,
        "session_id": event.get('sessionId', 'unknown'),
        # Log service line and payer (not individual claim amounts) for audit
        "service_line": service_line,
        "payer_id_prefix": payer_id[:8],  # Truncated for debugging
        "timestamp": time.time()
    }))

    try:
        result = perform_claims_query(service_line, payer_id)
        duration = time.time() - start_time

        logger.info(json.dumps({
            "event": "tool_completed",
            "tool_name": f"{action_group}{api_path}",
            "request_id": context.aws_request_id,
            "duration_ms": duration * 1000,
            "result_status": "success",
            "result_field_count": len(result.keys())
            # DO NOT LOG individual claim payment amounts
        }))

        return build_response(200, result)

    except Exception as e:
        duration = time.time() - start_time
        logger.error(json.dumps({
            "event": "tool_failed",
            "tool_name": f"{action_group}{api_path}",
            "request_id": context.aws_request_id,
            "duration_ms": duration * 1000,
            "error_type": type(e).__name__,
            "error_message": str(e)
        }))
        return build_error_response(500, "Internal error processing request")
```

**Layer 3: CloudWatch Metrics**

Custom metrics for agent-specific monitoring:

```python
import boto3

cloudwatch = boto3.client('cloudwatch')

def publish_agent_metric(metric_name: str, value: float,
                          unit: str, dimensions: dict):
    cloudwatch.put_metric_data(
        Namespace='HealthcareAgent/FinancialAnalytics',
        MetricData=[{
            'MetricName': metric_name,
            'Value': value,
            'Unit': unit,
            'Dimensions': [
                {'Name': k, 'Value': v}
                for k, v in dimensions.items()
            ]
        }]
    )

# Usage examples:
publish_agent_metric('AnalysisWorkflowDuration', 847.3, 'Seconds',
                     {'AgentId': 'FIN-AGENT-01', 'ServiceLine': 'orthopedics'})

publish_agent_metric('ToolCallCount', 7, 'Count',
                     {'AgentId': 'FIN-AGENT-01', 'ToolName': 'get_negotiated_rates'})

publish_agent_metric('UnderpaymentFlagRate', 1, 'Count',
                     {'AgentId': 'FIN-AGENT-01', 'Status': 'success'})
```

**Layer 4: Distributed Tracing with AWS X-Ray**

For complex agents with multiple Lambda functions, X-Ray provides end-to-end request tracing across all components.

---

## Chapter 3.7 — Guardrails

### What Are Guardrails?

Guardrails are safety controls that constrain agent behavior at the inference layer, independent of the prompt engineering or tool design. In Amazon Bedrock, Guardrails is a dedicated service that sits between the caller and the foundation model.

**Categories of Bedrock Guardrails:**

**Content Filters:** Block or flag content in predefined harm categories (hate speech, violence, sexual content, misconduct). For healthcare financial agents, you'll typically use these at lower thresholds than a general-purpose chatbot.

**Topic Denial:** Define specific topics the agent should refuse to discuss. For a financial analytics agent:
- Denied: "Recommend fraudulent billing codes"
- Denied: "Advise on upcoding or unbundling procedures"
- Denied: "Discuss pending litigation with payers"
- Allowed: "Retrieve negotiated rates from CMS MRFs"
- Allowed: "Identify underpayments against contracted rates"

**Sensitive Information Redaction:** Automatically detect and redact PII from outputs. For healthcare financial agents, configure detection of SSN, employee ID, individual patient identifiers, and other sensitive data categories.

**Grounding Check (Hallucination Detection):** Evaluates whether agent responses are grounded in the provided context. Rejects or flags responses where the agent makes claims not supported by its retrieved information.

**Word Filters:** Block specific phrases or terminology from inputs or outputs.

---

### Guardrail Configuration for Healthcare Agents

```python
import boto3

bedrock = boto3.client('bedrock', region_name='us-east-1')

def create_healthcare_agent_guardrail():
    response = bedrock.create_guardrail(
        name='HealthcareAgentGuardrail-FinancialAnalytics',
        description='Guardrail for Healthcare Financial Analytics agent',

        # Content filtering
        contentPolicyConfig={
            'filtersConfig': [
                {'type': 'HATE', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                {'type': 'VIOLENCE', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
                {'type': 'MISCONDUCT', 'inputStrength': 'HIGH', 'outputStrength': 'HIGH'},
            ]
        },

        # Topic-based restrictions
        topicPolicyConfig={
            'topicsConfig': [
                {
                    'name': 'FraudulentBilling',
                    'definition': 'Recommending, advising, or assisting with fraudulent billing, upcoding, unbundling, or other improper coding practices',
                    'examples': [
                        'How can I bill CPT 27447 as CPT 27486 to get a higher rate',
                        'Unbundle this global surgical package to maximize revenue',
                    ],
                    'type': 'DENY'
                },
                {
                    'name': 'ContractNegotiationAdvice',
                    'definition': 'Providing strategic legal advice on active payer contract negotiations or litigation',
                    'examples': [
                        'Tell me exactly what to threaten the payer with in our negotiation',
                        'Help me build a legal case against this payer',
                    ],
                    'type': 'DENY'
                },
                {
                    'name': 'LegalAdvice',
                    'definition': 'Providing legal advice or commentary on litigation',
                    'examples': ['You should sue the payer for breach of contract'],
                    'type': 'DENY'
                }
            ]
        },

        # Sensitive information handling
        sensitiveInformationPolicyConfig={
            'piiEntitiesConfig': [
                {'type': 'SSN', 'action': 'BLOCK'},
                {'type': 'NAME', 'action': 'ANONYMIZE'},
                {'type': 'EMAIL', 'action': 'ANONYMIZE'},
                {'type': 'PHONE', 'action': 'ANONYMIZE'},
            ]
        },

        # Grounding check
        groundingPolicyConfig={
            'filtersConfig': [
                {
                    'type': 'GROUNDING',
                    'threshold': 0.75  # Reject responses with < 75% grounding score
                },
                {
                    'type': 'RELEVANCE',
                    'threshold': 0.75
                }
            ]
        }
    )

    return response['guardrailId']
```

---

## Chapter 3.8 — Failover Patterns

### Designing for Failure

In production healthcare financial systems, your agent will face:
- Lambda timeouts
- Claims data warehouse API unavailability (maintenances, outages)
- LLM API throttling
- Network timeouts
- Malformed responses from external systems

Your architecture must anticipate these failures and define explicit handling for each.

**Failover pattern 1: Graceful degradation**
If a non-critical tool fails, the agent continues with reduced functionality rather than failing completely.

```
If get_contribution_margin() times out:
  → Continue without contribution margin data
  → Note in output: "Contribution margin data temporarily unavailable.
    Analysis proceeds using claims and rate data only."
  → Log warning metric to CloudWatch

If claims data warehouse query fails:
  → Do NOT continue (this is critical data)
  → Log error
  → Return: "Unable to retrieve claims data. Please verify data warehouse availability."
  → Escalate to human
```

**Failover pattern 2: Retry with backoff**

```python
import time
import random
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1.0, backoff_factor=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except TransientError as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (backoff_factor ** attempt)
                    jitter = random.uniform(0, delay * 0.1)
                    time.sleep(delay + jitter)
            return None
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3, base_delay=1.0)
def query_claims_warehouse(service_line: str, date_range: str) -> dict:
    # Claims data warehouse API call
    ...
```

**Failover pattern 3: Human escalation**

Every agent must have a clear path to human escalation. This is not failure — this is the system working correctly.

Define escalation triggers:
- Tool failure after N retries
- Agent reaches maximum orchestration steps without completing
- Confidence score below threshold (if you implement confidence scoring)
- Specific content detected that requires human judgment (contract disputes, compliance flags)

Escalation implementation in Lambda:
```python
def escalate_to_human(reason: str, workflow_id: str, context: dict):
    """
    Creates a human review task and notifies the appropriate queue.
    """
    sns = boto3.client('sns')
    sqs = boto3.client('sqs')

    # Create task in review queue
    sqs.send_message(
        QueueUrl=HUMAN_REVIEW_QUEUE_URL,
        MessageBody=json.dumps({
            'workflow_id': workflow_id,
            'escalation_reason': reason,
            'priority': determine_priority(reason),
            'context': sanitize_for_logging(context),  # Remove sensitive data before logging
            'timestamp': datetime.utcnow().isoformat()
        })
    )

    # Alert on-call revenue cycle analyst
    sns.publish(
        TopicArn=ANALYST_ALERT_TOPIC,
        Message=f"Financial analysis workflow {workflow_id} requires human review: {reason}",
        Subject="Agent Escalation Required"
    )

    return {
        'status': 'escalated',
        'message': f'This request has been escalated for human review. Reference ID: {workflow_id}'
    }
```

---

## Chapter 3.9 — Cost Modeling

### Production Cost Architecture

Before deploying any agent, you must build a cost model. Surprises in production costs are a leading cause of healthcare AI projects being shut down after initial deployment.

**Full cost model template:**

```python
class AgentCostModel:
    """
    Cost model for Amazon Bedrock Agent deployments.
    Prices as of Q1 2026 — verify current pricing at aws.amazon.com/bedrock/pricing
    """

    def __init__(self):
        # Claude 3 Sonnet pricing (us-east-1)
        self.llm_input_price_per_1k = 0.003   # USD per 1K input tokens
        self.llm_output_price_per_1k = 0.015  # USD per 1K output tokens

        # Knowledge base
        self.kb_query_price = 0.0001          # USD per query
        self.embedding_price_per_1k = 0.0001  # Titan Embeddings V2

        # OpenSearch Serverless
        self.oss_ocuh_price = 0.24            # USD per OCU-hour (2 min OCU default)

        # Lambda
        self.lambda_request_price = 0.0000002  # USD per request
        self.lambda_duration_price_per_gb_sec = 0.0000166667

        # Data transfer (assuming within AWS, minimal)
        self.data_transfer = 0.001  # USD per session estimate

    def estimate_session_cost(
        self,
        avg_loop_iterations: int = 6,
        avg_input_tokens_per_step: int = 8000,
        avg_output_tokens_per_step: int = 500,
        num_tool_calls: int = 8,
        num_kb_queries: int = 3,
        avg_lambda_duration_sec: float = 2.0,
        lambda_memory_mb: int = 256
    ) -> dict:

        # LLM costs
        total_input_tokens = avg_loop_iterations * avg_input_tokens_per_step
        total_output_tokens = avg_loop_iterations * avg_output_tokens_per_step
        llm_cost = (
            (total_input_tokens / 1000) * self.llm_input_price_per_1k +
            (total_output_tokens / 1000) * self.llm_output_price_per_1k
        )

        # KB query costs
        kb_cost = num_kb_queries * self.kb_query_price

        # Lambda costs
        lambda_gb_sec = (lambda_memory_mb / 1024) * avg_lambda_duration_sec * num_tool_calls
        lambda_cost = (
            num_tool_calls * self.lambda_request_price +
            lambda_gb_sec * self.lambda_duration_price_per_gb_sec
        )

        total = llm_cost + kb_cost + lambda_cost + self.data_transfer

        return {
            'llm_cost': round(llm_cost, 4),
            'kb_cost': round(kb_cost, 4),
            'lambda_cost': round(lambda_cost, 4),
            'other_cost': self.data_transfer,
            'total_per_session': round(total, 4),
            'total_input_tokens': total_input_tokens,
            'total_output_tokens': total_output_tokens,
            'notes': {
                'daily_cost_at_100_sessions': round(total * 100, 2),
                'monthly_cost_at_100_sessions_day': round(total * 100 * 30, 2),
                'annual_cost_at_100_sessions_day': round(total * 100 * 365, 2)
            }
        }

# Example usage:
model = AgentCostModel()
financial_agent_cost = model.estimate_session_cost(
    avg_loop_iterations=7,
    avg_input_tokens_per_step=10000,
    avg_output_tokens_per_step=800,
    num_tool_calls=10,
    num_kb_queries=4
)

print(f"Estimated cost per financial analysis session: ${financial_agent_cost['total_per_session']}")
print(f"Annual cost at 200 sessions/day: ${financial_agent_cost['notes']['annual_cost_at_100_sessions_day'] * 2}")
```

---

## Chapter 3.10 — Enterprise Risk Discussion

### Risks Unique to Healthcare Agentic Systems

**Risk Category 1: Autonomous Action Risk**

Any agent that can take action in the external world — submitting underpayment disputes, writing to financial systems, sending payer communications — carries execution risk. If the agent takes wrong actions autonomously, the consequences may include financial loss, regulatory violations, or damaged payer relationships.

**Mitigation:** Define an autonomy policy for every action type. Map each tool to a risk tier:
- Tier 0: Read-only operations (fully autonomous)
- Tier 1: Low-consequence writes (human notification, not approval)
- Tier 2: Moderate-consequence writes (human approval required)
- Tier 3: High-consequence writes (finance director or managed care director approval required)

**Risk Category 2: Non-Determinism Risk**

LLMs are non-deterministic. The same input can produce different outputs on different calls. In regulated healthcare financial workflows, this means:
- Compliance audits may find different behavior than you tested for
- Revenue cycle analysts may receive different rate discrepancy assessments for similar claim sets
- You cannot certify the agent's behavior against a fixed specification

**Mitigation:** Log everything. Use guardrails to constrain the decision space. Design for human review at consequential decision points. Never claim the agent is "certified" — frame it as a decision support tool.

**Risk Category 3: Sensitive Financial Data Leakage**

An agent that processes financial data and encounter-level detail can inadvertently expose it through:
- Including payer contract terms in error messages that flow to unsecured logs
- Outputting individually identifiable financial data in response to out-of-scope queries
- Storing sensitive negotiated rate data in session memory beyond its intended retention

**Mitigation:** Sensitive data handling policy must be part of the agent design, not an afterthought. Every component that touches confidential payer contract data or encounter-level financials must be designed with appropriate data governance controls from the beginning.

**Risk Category 4: Model Drift**

The foundation models powering your agent will be updated by the vendor. A model update can change agent behavior in subtle or significant ways.

**Mitigation:** Pin to specific model versions. Run your full evaluation suite against any new model version before switching. Maintain rollback capability.

**Risk Category 5: Supply Chain Risk**

Your agent depends on:
- AWS Bedrock service availability
- Foundation model availability
- Lambda service availability
- Claims data warehouse API availability
- CMS MRF data freshness and availability
- Knowledge base data freshness

If any of these fail, your agent fails. At peak load, all of these fail more than expected.

**Mitigation:** Service level objectives (SLOs) for agent availability. Fallback to manual process documented and staffed. Real-time dependency health monitoring.

---

## Module 3 Reflection Prompts

1. A financial analytics agent has been running successfully for 3 months and suddenly starts completing analysis workflows at 60% of its previous rate. The model hasn't changed. What are the first 5 things you check?

2. Your healthcare organization's data governance team asks: "When the agent queries our claims data warehouse, what information appears in the CloudWatch logs?" Walk through your logging architecture and identify every place sensitive financial data could appear. Then design a logging approach that provides operational visibility without exposing individually identifiable encounter data or confidential payer contract terms.

3. Design the state machine for a rate discrepancy analysis agent that ingests claims data, compares against CMS MRF negotiated rates, and generates an underpayment report for managed care renegotiation. Define all states, valid transitions, and what data must be preserved in each state.

4. A product manager wants to reduce cost per session for the financial analytics agent by 40%. What levers do you have? What are the quality tradeoffs for each approach?

5. The financial analytics agent encounters a case where the CMS MRF file for a specific payer is missing rates for CPT 70553 (MRI brain). The agent cannot complete the underpayment analysis without this data. Walk through exactly what the agent should do, what message should appear to the revenue cycle analyst, and how this case should be tracked and resolved.

---

*End of Module 3 Textbook Content*
