# MODULE 4: Amazon Bedrock Deep Dive
## Weeks 6–7 | Full UI Walkthrough

---

## Chapter 4.1 — Bedrock Foundations

### What is Amazon Bedrock?

Amazon Bedrock is AWS's fully managed foundational model service. It provides API access to a curated portfolio of state-of-the-art LLMs from Anthropic (Claude), Meta (Llama), Mistral, Stability AI, AI21 Labs, Cohere, and Amazon's own Titan models — all without requiring you to manage infrastructure.

Beyond model access, Bedrock provides enterprise-grade services layered on top:
- **Bedrock Agents:** Managed agentic orchestration with ReAct loops, tool calling, memory management
- **Bedrock Knowledge Bases:** Managed RAG infrastructure with vector storage and embedding
- **Bedrock Guardrails:** Managed content filtering, topic control, and grounding checks
- **Bedrock Model Evaluation:** Automated evaluation frameworks for model comparison
- **Bedrock Flows:** Visual workflow builder for multi-step LLM pipelines
- **Bedrock Studio:** Collaborative workspace for prompt and agent development

**Why Bedrock for healthcare?**
1. HIPAA-eligible — AWS has BAA provisions covering Bedrock
2. No model training on your data — Bedrock API calls do not train the underlying models
3. VPC integration — API calls can remain within your network perimeter
4. AWS native IAM — all access control uses standard AWS IAM policies
5. CloudTrail audit logging — every API call is logged automatically
6. Existing AWS security controls apply — your existing CSPM, SIEM, and DLP tools cover Bedrock

---

### Available Models and Tradeoffs

| Model | Provider | Context Window | Strengths | Healthcare Fit |
|-------|----------|---------------|-----------|----------------|
| Claude 3 Opus | Anthropic | 200K tokens | Highest reasoning quality, complex analysis | Complex clinical reasoning, document analysis |
| Claude 3 Sonnet | Anthropic | 200K tokens | Balanced quality/speed/cost | General-purpose agent backbone (recommended) |
| Claude 3 Haiku | Anthropic | 200K tokens | Fastest, cheapest | High-volume simple tasks, classification |
| Claude 3.5 Sonnet | Anthropic | 200K tokens | Improved coding, analysis | Agent development, code generation |
| Llama 3 70B | Meta | 8K tokens | Open weights, fine-tunable | On-premise/custom deployment scenarios |
| Titan Text Express | Amazon | 8K tokens | Cost-effective | Simple extraction tasks |
| Titan Embeddings V2 | Amazon | N/A | Vector embeddings | Knowledge base (standard choice) |
| Cohere Embed | Cohere | N/A | Multilingual embeddings | Multi-language clinical content |

**Recommended stack for healthcare agents:**
- **Agent backbone:** Claude 3 Sonnet (best quality/cost balance for multi-step reasoning)
- **Simple classification tasks:** Claude 3 Haiku or Titan Text Express
- **Embeddings:** Titan Embeddings V2 (default, cost-effective, native Bedrock integration)
- **High-stakes clinical reasoning:** Claude 3 Opus (for cases requiring maximum accuracy)

---

### Enabling Model Access in Bedrock

Before you can use any model in Bedrock, you must explicitly request access. Models are not available by default.

**Step 1 — Navigate to the AWS Console and open Amazon Bedrock:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.20.34 PM.png" alt="AWS Console Home showing Amazon Bedrock in recently visited services" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> AWS Console Home — Amazon Bedrock appears under "Recently visited." Click it, or search "Bedrock" in the top search bar. Ensure your region is set to <strong style="color:#5b8dee;">US East (N. Virginia)</strong> — us-east-1 has the broadest model availability.</p>
</div>

**Step 2 — The Amazon Bedrock Overview page:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.20.55 PM.png" alt="Amazon Bedrock Overview page showing Quickstart, Model catalog, and left navigation" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The Bedrock Overview page. The left navigation panel is your primary guide — it contains <strong style="color:#5b8dee;">Model catalog</strong>, <strong style="color:#5b8dee;">Playgrounds</strong>, and the <strong style="color:#5b8dee;">Build</strong> section (Agents, Knowledge Bases, Guardrails). Before doing anything else, go to <strong style="color:#5b8dee;">Model access</strong> under "Configure and learn."</p>
</div>

**On Screen You Should See:**
- Left navigation: Model access, Playgrounds, Agents, Knowledge bases, Guardrails, Settings
- Main content: Table of model providers with columns: Model name, Model ID, Status, Pricing, Modalities
- Request model access button (top right of content area)
- Filter options by provider and modality
- Important: Some models show "Available" but require accepting terms — read them for healthcare-relevant restrictions

**Console Navigation:**
1. Sign in to AWS Console at console.aws.amazon.com
2. Search "Bedrock" in the services search bar
3. Click "Amazon Bedrock"
4. In the left navigation, click "Model access" under "Bedrock configurations"
5. Click "Request model access"
6. Select checkboxes for: Anthropic Claude (all tiers), Amazon Titan (all), Meta Llama 3
7. Click "Request model access" at the bottom
8. Wait for approval (Anthropic models typically approve within minutes)

> ⚠️ **Model access can take minutes to hours to approve — request before labs begin.**

---

### Prompt Engineering vs. Agent Configuration

**Prompt engineering** is the discipline of crafting inputs to LLMs to reliably produce desired outputs. It includes:
- Role definition ("You are an expert healthcare financial analyst...")
- Task instruction ("Analyze this payer rate variance report...")
- Format specification ("Return your response as JSON with these fields...")
- Few-shot examples ("Here are 3 examples of correct responses...")
- Chain-of-thought elicitation ("Think step by step before responding...")

**Agent configuration** is different. It involves:
- System prompt: The standing instructions for the agent's role and behavior
- Tool definitions: The schema of what the agent can do
- Knowledge base connections: What the agent can retrieve
- Guardrails: What the agent is constrained from doing
- Memory configuration: How the agent maintains state
- Orchestration parameters: How many steps, what timeout

The relationship: prompt engineering principles apply to the system prompt you write for the agent. But the agent configuration itself is a structural, architectural decision that goes far beyond what's in the prompt.

**The system prompt for a Bedrock Agent should include:**

```
You are a healthcare financial analytics specialist assistant for [Organization Name] revenue cycle and finance operations. You support revenue cycle directors, managed care contracting teams, and finance analysts by analyzing claims data, identifying payer rate discrepancies, and generating utilization and price forecasts.

Your role:
- Retrieve and analyze claims data by service line, payer, and procedure code
- Compare actual allowed amounts against CMS MRF negotiated rates to identify underpayments
- Pull GL and payroll data to compute contribution margins by service line
- Generate encounter volume, price escalation, and utilization forecasts
- Prepare rate variance reports and financial briefings for managed care leadership

Constraints (strictly enforced):
- NEVER submit a payer dispute or rate correction without explicit analyst approval in the current session
- NEVER modify source financial data or GL entries
- NEVER access data outside the scope of the current analysis request
- NEVER provide legal advice on contract interpretation
- If you cannot complete a task, clearly explain what data is missing or inaccessible

Format:
- Always state what data you retrieved vs. what you calculated or inferred
- Flag data quality issues (missing MRF rates, incomplete claims) before proceeding
- For financial reports, use the format requested by the analyst
- Confirm your understanding of the analysis scope before proceeding on complex requests
```

---

## Chapter 4.2 — Creating a Bedrock Agent: Complete Console Walkthrough

### Pre-Lab Setup: IAM Role Creation

Before creating your first Bedrock Agent, you need a service role that allows Bedrock to:
1. Invoke foundation models on your behalf
2. Invoke Lambda functions for action groups
3. Query knowledge bases

**Required IAM Role: BedrockAgentExecutionRole**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowBedrockModelInvocation",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
      ]
    },
    {
      "Sid": "AllowLambdaInvocation",
      "Effect": "Allow",
      "Action": [
        "lambda:InvokeFunction"
      ],
      "Resource": [
        "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:claims-analytics-tools-*"
      ]
    },
    {
      "Sid": "AllowKnowledgeBaseQuery",
      "Effect": "Allow",
      "Action": [
        "bedrock:Retrieve",
        "bedrock:RetrieveAndGenerate"
      ],
      "Resource": [
        "arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:knowledge-base/*"
      ]
    }
  ]
}
```

**Trust relationship for the role (allows Bedrock to assume it):**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock.amazonaws.com"
      },
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "YOUR_ACCOUNT_ID"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:agent/*"
        }
      }
    }
  ]
}
```

**Why the Condition block matters:** The `ArnLike` condition prevents confused deputy attacks — it ensures that only Bedrock agents in your specific account can assume this role, not any Bedrock service across all accounts.

---

### Step-by-Step: Creating Your First Bedrock Agent

#### Navigate to Bedrock Agents

**Step 3 — Open the Build section and navigate to Agents:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.21.02 PM.png" alt="Bedrock left navigation showing the Build section with Agents, Flows, Knowledge Bases, and other options" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The Bedrock left navigation expanded to show the <strong style="color:#5b8dee;">Build</strong> section. Click <strong style="color:#5b8dee;">Agents</strong> to reach the agent management console. You can also see Flows, Knowledge Bases, Automated Reasoning, Guardrails, Prompt Management, Data Automation, and AgentCore listed here.</p>
</div>

**Step 4 — The Agents list page:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.21.14 PM.png" alt="Bedrock Agents list page showing existing agents with Create agent button in the top right" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The Agents landing page lists all agents in your account. The orange <strong style="color:#5b8dee;">Create agent</strong> button is in the top right. The table shows agent name, status, description, and last updated timestamp. Click <strong style="color:#5b8dee;">Create agent</strong> to begin.</p>
</div>

**On Screen You Should See:**
- Left navigation panel with: Playgrounds (text, chat, image), Builder tools (Agents, Knowledge bases, Flows, Prompt management), Deployment, Evaluation, Settings
- Main content: "Agents" header, "Create Agent" button, agents list with columns: Agent name, Status, Model, Last updated
- If no agents exist: "No agents" message with "Create Agent" CTA

**Navigation path:** Amazon Bedrock → (left sidebar) → Builder tools → Agents → Create Agent

---

#### Agent Creation: Basic Configuration

**Step 5 — The Create agent dialog:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.21.23 PM.png" alt="Create agent dialog showing Name, Description, and Multi-agent collaboration fields" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The Create agent modal dialog. Enter a descriptive <strong style="color:#5b8dee;">Name</strong> (e.g., <code>financial-analytics-agent</code>) — valid characters are a-z, A-Z, 0-9, underscore, and hyphen, max 100 characters. The optional <strong style="color:#5b8dee;">Description</strong> can be up to 500 characters. <strong style="color:#5b8dee;">Multi-agent collaboration</strong> (disabled by default) allows this agent to delegate subtasks to other agents — leave disabled for now. Click <strong style="color:#5b8dee;">Create</strong>.</p>
</div>

**Step 6 — The Agent Builder page (after creation):**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.21.45 PM.png" alt="Agent Builder page showing all configuration fields: Agent name, description, Agent resource role, Select model, and Instructions" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The <strong style="color:#5b8dee;">Agent Builder</strong> page after successful creation — note the green "Agent: Test_Agent was successfully created" banner at the top. This is your full configuration workspace. The right panel is the <strong style="color:#5b8dee;">Test Agent</strong> pane for live testing as you build. Fill in the Agent resource role, select a model, and write your Instructions (system prompt) here.</p>
</div>

**On Screen You Should See:**
- "Create agent" page header
- Section 1: "Agent details"
  - Agent name field (required) — use lowercase, hyphens allowed
  - Description field (optional but recommended)
- Section 2: "Agent resource role"
  - "Create and use a new service role" (default) OR "Use an existing service role"
  - If using existing: IAM role dropdown
- Section 3: "Select model"
  - Foundation model dropdown
  - Model version (if applicable)
- Section 4: "Instructions" — your system prompt
- "Next" button at bottom

**Field-by-field explanation:**

**Agent name:** This is a permanent identifier. Use a descriptive, environment-specific name: `financial-analytics-agent-prod` vs `financial-analytics-agent-dev`. You cannot rename an agent after creation; you must delete and recreate.

**IAM role:** You can let AWS create a role (convenient but creates a permissive role) or specify an existing role (recommended for production). **Always use a pre-created, least-privilege role for anything beyond a personal demo.**

**Foundation model:** Select the model for the agent's reasoning engine. For healthcare use cases, start with Claude 3 Sonnet. The model can be changed later without recreating the agent.

**Selecting a model — the model picker dialog:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.22.12 PM.png" alt="Select model dialog showing categories (Amazon, Anthropic), model list, and inference options" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The model picker dialog has three columns: <strong style="color:#5b8dee;">1. Categories</strong> (filter by provider — Amazon, Anthropic, etc.), <strong style="color:#5b8dee;">2. Models</strong> (select the specific model), and <strong style="color:#5b8dee;">3. Inference</strong> (choose inference options). For healthcare agent work, select <strong style="color:#5b8dee;">Anthropic</strong> → <strong style="color:#5b8dee;">Claude 3.5 Sonnet</strong> or Claude 3 Sonnet for best reasoning quality.</p>
</div>

**Instructions (System Prompt):** This is the most important field. It defines the agent's role, capabilities, constraints, and behavioral guidelines. It is what the LLM reads to understand who it is and what it should do. Write this carefully.

---

#### Entering the System Prompt

In the Instructions field, enter your agent's system prompt. For the financial analytics agent lab:

```
You are a healthcare financial analytics specialist assistant for [Organization Name]
revenue cycle and finance operations. You support revenue cycle directors, managed care
contracting teams, and finance analysts by analyzing claims data, identifying payer rate
discrepancies, and generating utilization and price forecasts.

Your role:
- Retrieve and analyze claims data by service line, payer, and procedure code
- Compare actual allowed amounts against CMS MRF negotiated rates to identify underpayments
- Pull GL and payroll data to compute contribution margins by service line
- Generate encounter volume, price escalation, and utilization forecasts
- Prepare rate variance reports and financial briefings for managed care leadership

Constraints (strictly enforced):
- NEVER submit a payer dispute or rate correction without explicit analyst approval in the current session
- NEVER modify source financial data or GL entries
- NEVER access data outside the scope of the current analysis request
- NEVER provide legal advice on contract interpretation
- If you cannot complete a task, clearly explain what data is missing or inaccessible

Format:
- Always state what data you retrieved vs. what you calculated or inferred
- Flag data quality issues (missing MRF rates, incomplete claims) before proceeding
- For financial reports, use the format requested by the analyst
- Confirm your understanding of the analysis scope before proceeding on complex requests
```

---

#### What Happens When You Click "Create Agent"

This is a critical architectural moment. Understanding what Bedrock does when you click this button demystifies the system.

When you click Create Agent, Bedrock:

1. **Creates an agent resource** in the Bedrock control plane. This is a managed resource with a unique Agent ID (`ABCDEFGHIJ`).

2. **Associates the IAM role** with the agent. Bedrock stores the role ARN and will use this role when the agent executes.

3. **Stores the system prompt** and model configuration in encrypted storage.

4. **Creates a "DRAFT" alias** for the agent. The agent starts in DRAFT status. DRAFT is the working version you edit. When ready for production, you create a named alias (e.g., "v1") that points to a specific, immutable version.

5. **Does NOT yet prepare the agent** for invocation. The agent is in DRAFT status and must be "Prepared" before it can be called. (Preparation compiles all configuration into an executable format.)

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.21.45 PM.png" alt="Agent Builder after creation showing the Manual/Assistant/Test/Prepare/Save/Save and exit buttons at the top" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> After creation, the agent is in an unprepared <strong style="color:#5b8dee;">DRAFT</strong> state. Notice the action buttons at the top: <strong style="color:#5b8dee;">Manual</strong>, <strong style="color:#5b8dee;">Assistant</strong>, <strong style="color:#5b8dee;">Test</strong>, <strong style="color:#5b8dee;">Prepare</strong>, <strong style="color:#5b8dee;">Save</strong>, and <strong style="color:#5b8dee;">Save and exit</strong>. You must click <strong style="color:#5b8dee;">Prepare</strong> before the agent can be tested. Preparation compiles the full configuration into an executable format and takes 10–60 seconds.</p>
</div>

**On Screen You Should See:**
- Agent name and description
- Agent ID (10-character alphanumeric)
- Agent ARN
- Status: "NOT_PREPARED" (orange badge)
- Model: "Anthropic Claude 3 Sonnet v1"
- Agent version: DRAFT
- Sections: Overview, Working draft, Aliases, Versions, Monitoring

---

## Chapter 4.3 — Action Groups

### What is an Action Group?

An action group is a named collection of tools (functions) that an agent can invoke. Each action group is backed by a Lambda function (the execution environment) and defined by an OpenAPI schema (the tool specification).

**The relationship:**
```
Agent
  ├── Action Group: "ClaimsAnalyticsGroup"
  │     ├── Lambda: arn:aws:lambda:...:function:claims-analytics-tools
  │     └── OpenAPI Schema: {query_claims_data, get_denial_patterns, get_allowed_amounts, get_payer_mix}
  │
  ├── Action Group: "RateTransparencyGroup"
  │     ├── Lambda: arn:aws:lambda:...:function:rate-transparency-tools
  │     └── OpenAPI Schema: {get_negotiated_rates, compare_market_rates, get_chargemaster_rates}
  │
  └── Knowledge Base: "ManagedCareContractsKB"
```

The agent can call tools from any action group during a single session. The LLM reads all action group schemas at the start of each reasoning step to understand its full tool set.

**The Action Groups section in the Agent Builder:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.21.55 PM.png" alt="Agent Builder scrolled down showing Action groups section (0), Memory - New section, and Knowledge Bases section (0)" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> Scrolling down the Agent Builder reveals the <strong style="color:#5b8dee;">Action groups</strong>, <strong style="color:#5b8dee;">Memory</strong>, and <strong style="color:#5b8dee;">Knowledge Bases</strong> configuration sections. Both Action groups and Knowledge Bases start at 0 — use the <strong style="color:#5b8dee;">Add</strong> button in each section to attach them. The <strong style="color:#5b8dee;">Memory</strong> section (marked "New") allows the agent to retain conversation context across multiple sessions.</p>
</div>

---

### Creating an Action Group: Console Walkthrough

**Step 7 — Click "Add" in the Action groups section to open the Create Action group form:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.22.25 PM.png" alt="Create Action group page showing Action group name, description, Action group type (Define with function details / Define with API schemas), and Action group invocation options" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The Create Action group page. Enter a descriptive <strong style="color:#5b8dee;">Action group name</strong> (e.g., <code>claims-data-retrieval</code>). Under <strong style="color:#5b8dee;">Action group type</strong>, choose between <em>Define with function details</em> (simple, single-function) or <em>Define with API schemas</em> (multi-function, recommended for production). Under <strong style="color:#5b8dee;">Action group invocation</strong>, "Quick create a new Lambda function" is recommended for new setups — Bedrock will scaffold the Lambda for you.</p>
</div>

**On Screen You Should See in the Add Action Group form:**

1. **Action group name:** Free-form identifier. Use descriptive names: `claims-data-retrieval`, `rate-transparency`, `financial-forecasting`

2. **Action group type:**
   - "Define with function details" — for simple single-function groups
   - "Define with API schemas" — for multi-function groups (RECOMMENDED)

3. **Lambda function:**
   - Select from existing functions in the same account/region
   - OR enter the Lambda ARN directly
   - NOTE: You must add a resource-based policy to the Lambda function to allow Bedrock to invoke it

4. **API Schema:**
   - Upload an OpenAPI YAML/JSON file
   - OR define inline (for simple cases)

5. **Description:** Helps the LLM understand when to use this action group as a whole

**Step 8 — Define the Action Group Function:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.22.30 PM.png" alt="Action Group function 1 definition form showing Name, Description, Enable confirmation checkbox, and Parameters table" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The <strong style="color:#5b8dee;">Action Group function 1</strong> definition panel. Give each function a <strong style="color:#5b8dee;">Name</strong> and a detailed <strong style="color:#5b8dee;">Description</strong> — the LLM uses the description to decide when to invoke this function. The <strong style="color:#5b8dee;">Enable confirmation</strong> toggle (optional) prompts the user for approval before invoking — useful for write operations. Click <strong style="color:#5b8dee;">Add parameter</strong> to define inputs the function accepts (name, type, required flag). Up to 3 functions can be created per action group.</p>
</div>

---

### Lambda Function Setup for Action Groups

Before connecting a Lambda function to Bedrock Agents, you must:

1. **Create the Lambda function** with the correct handler format
2. **Add a resource-based policy** to allow Bedrock to invoke it
3. **Configure the function** with appropriate IAM execution role

**Step 9 — Navigate to AWS Lambda to view or create your function:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.23.19 PM.png" alt="AWS Lambda Functions list showing multiple existing Lambda functions with runtime and last modified details" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The AWS Lambda Functions list. Navigate here via the AWS Console search bar (type "Lambda") or from the Bedrock action group form. Click <strong style="color:#5b8dee;">Create function</strong> (orange button, top right) to build a new Lambda function that will serve as your action group's backend.</p>
</div>

**Step 10 — Create a new Lambda function:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.23.28 PM.png" alt="Create function page showing Author from scratch option selected, Function name field, Runtime dropdown (nodejs24.x), Architecture selection (x86_64)" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The Create function page. Select <strong style="color:#5b8dee;">Author from scratch</strong>. Enter a <strong style="color:#5b8dee;">Function name</strong> (e.g., <code>claims-analytics-tools</code>). Choose your <strong style="color:#5b8dee;">Runtime</strong> — Python 3.12 is recommended for Bedrock agent integrations. Set architecture to <strong style="color:#5b8dee;">x86_64</strong> for maximum library compatibility. The default execution role will be created automatically with CloudWatch Logs permissions.</p>
</div>

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.23.36 PM.png" alt="Create function Additional configurations showing Compute type, Networking (Function URL, VPC), Security and governance options" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The Additional configurations section. For healthcare workloads: leave <strong style="color:#5b8dee;">Compute type</strong> as Lambda (default). Enable <strong style="color:#5b8dee;">VPC</strong> if your function needs to reach private claims databases or data warehouses on an internal network. <strong style="color:#5b8dee;">Do not</strong> enable Function URL — Bedrock invokes the function directly via IAM, not via HTTP. Click <strong style="color:#5b8dee;">Create function</strong> when ready.</p>
</div>

**Lambda handler format required by Bedrock Agents:**

```python
import json

def lambda_handler(event, context):
    """
    Amazon Bedrock Agents Lambda handler.

    Bedrock passes a specific event structure that your handler must parse.
    You must return a specific response structure that Bedrock can parse.
    """

    # Parse Bedrock event
    action_group = event['actionGroup']
    api_path = event['apiPath']
    http_method = event['httpMethod']
    parameters = {
        param['name']: param['value']
        for param in event.get('parameters', [])
    }
    request_body = event.get('requestBody', {})

    # Route to the correct handler based on apiPath
    if api_path == '/get-claims-summary' and http_method == 'POST':
        result = handle_get_claims_summary(parameters, request_body)
    elif api_path == '/get-negotiated-rates' and http_method == 'POST':
        result = handle_get_negotiated_rates(parameters, request_body)
    else:
        result = {'error': f'Unsupported path: {api_path}'}

    # Build required response structure
    response = {
        'actionGroup': action_group,
        'apiPath': api_path,
        'httpMethod': http_method,
        'httpStatusCode': 200,
        'responseBody': {
            'application/json': {
                'body': json.dumps(result)
            }
        }
    }

    return response


def handle_get_claims_summary(parameters: dict, body: dict) -> dict:
    payer_id = parameters.get('payer_id')
    service_line = parameters.get('service_line')
    date_range = parameters.get('date_range')

    if not payer_id or not service_line:
        return {
            'status': 'error',
            'error_code': 'MISSING_PARAMETER',
            'error_message': 'payer_id and service_line are required'
        }

    # Your actual business logic here
    # In production: query claims data warehouse, adjudication system, etc.
    # For lab: return mock data

    summary = query_claims_database(payer_id, service_line, date_range)

    return {
        'status': 'success',
        'claims_summary': {
            'payer_id': summary['payer_id'],
            'service_line': summary['service_line'],
            'total_claims': summary['total_claims'],
            'total_billed': summary['total_billed'],
            'total_allowed': summary['total_allowed'],
            'denial_rate': summary['denial_rate'],
            'top_denial_codes': summary['top_denial_codes']
        }
    }


def handle_get_negotiated_rates(parameters: dict, body: dict) -> dict:
    payer_id = parameters.get('payer_id')
    procedure_code = parameters.get('procedure_code')

    if not payer_id or not procedure_code:
        return {
            'status': 'error',
            'error_code': 'MISSING_PARAMETER',
            'error_message': 'payer_id and procedure_code are required'
        }

    # Your actual business logic here
    # In production: query CMS Machine Readable File (MRF) data store
    # For lab: return mock data

    rate = query_mrf_database(payer_id, procedure_code)

    return {
        'status': 'success',
        'negotiated_rate': {
            'payer_id': rate['payer_id'],
            'procedure_code': rate['procedure_code'],
            'negotiated_rate': rate['negotiated_rate'],
            'rate_type': rate['rate_type'],
            'effective_date': rate['effective_date'],
            'expiration_date': rate['expiration_date']
        }
    }
```

**Adding Bedrock permission to invoke your Lambda (resource-based policy):**

```bash
aws lambda add-permission \
  --function-name claims-analytics-tools \
  --statement-id AllowBedrockAgentInvoke \
  --action lambda:InvokeFunction \
  --principal bedrock.amazonaws.com \
  --source-arn "arn:aws:bedrock:us-east-1:YOUR_ACCOUNT_ID:agent/YOUR_AGENT_ID" \
  --source-account YOUR_ACCOUNT_ID
```

**Why `source-arn` AND `source-account` matter:** The `source-arn` ensures only your specific agent can invoke the function. The `source-account` prevents the confused deputy problem. Both conditions must be satisfied.

---

### Adding the Action Group

**On Screen You Should See after defining functions:**
- Function name and description fields filled in
- Parameters table with defined inputs (name, type, required)
- "Add action group function" link to add additional functions (up to 3 per group)
- Cancel and Create buttons at the bottom

**Common schema validation errors (when using API schemas):**
- Missing `operationId` — every path+method combination needs a unique operation ID
- Missing `description` on operation — required for agent reasoning
- Parameter types not in supported set (string, number, integer, boolean, array, object)
- Required fields not marked as required in schema
- Operation response schema not defined

---

### Attaching a Knowledge Base to Your Agent

After configuring action groups, scroll down to the **Knowledge Bases** section of the Agent Builder to connect your agent to a knowledge base.

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.22.46 PM.png" alt="Add Knowledge Base page showing Knowledge Base selection dropdown and Knowledge Base instructions for Agent text field" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The <strong style="color:#5b8dee;">Add knowledge base</strong> form. Select a previously created Knowledge Base from the dropdown (or create one by visiting Knowledge Bases in the left nav). The <strong style="color:#5b8dee;">Knowledge Base instructions for Agent</strong> field is critical — tell the agent exactly when and how to use this knowledge base (e.g., "Use this knowledge base to look up payer-specific managed care contract terms, fee schedule references, and rate negotiation history"). Max 200 characters.</p>
</div>

The Knowledge Bases overview page is accessible from the left navigation:

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.25.23 PM.png" alt="Bedrock Knowledge Bases page showing list of existing knowledge bases with type (Vector store), status (Available), data source, and last sync information" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The <strong style="color:#5b8dee;">Knowledge Bases</strong> management page (Build → Knowledge Bases). Each knowledge base shows its name, status (Available = ready to use), type (Vector store), data source, and last sync date. You must create a Knowledge Base here before you can attach it to an agent. See Module 5 for the full Knowledge Base creation walkthrough.</p>
</div>

---

### Orchestration Strategy and Advanced Settings

Scrolling further down the Agent Builder reveals Guardrail, Orchestration, and Multi-agent configuration:

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.22.01 PM.png" alt="Agent Builder lower section showing Guardrail details, Orchestration strategy (Default/Custom), and Multi-agent collaboration settings" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The lower portion of the Agent Builder. <strong style="color:#5b8dee;">Guardrail details</strong> lets you attach a guardrail (content filter). <strong style="color:#5b8dee;">Orchestration strategy</strong> controls how the agent processes information — leave as <em>Default</em> unless you have advanced orchestration requirements. <strong style="color:#5b8dee;">Multi-agent collaboration</strong> enables this agent to act as a supervisor that delegates to sub-agents; note the warning that enabling this requires the agent to be associated with other agent collaborators.</p>
</div>

When you save and finalize your agent configuration, Bedrock presents the **Orchestration strategy** confirmation page:

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.22.58 PM.png" alt="Orchestration strategy page showing Agent details summary, Default orchestration enabled, and Session summarization option with Save and exit button" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The <strong style="color:#5b8dee;">Orchestration strategy</strong> confirmation view shows a summary of your agent's configuration alongside the orchestration options. <strong style="color:#5b8dee;">Default orchestration</strong> is the standard ReAct loop — the correct choice for most healthcare agents. <strong style="color:#5b8dee;">Session summarization</strong> (optional) generates a summary at the end of each test session to improve agent accuracy in multi-turn workflows. Click <strong style="color:#5b8dee;">Save and exit</strong> to finalize.</p>
</div>

---

### Diagram: Agent → Orchestrator → Lambda → Response

```
Diagram Title: Bedrock Agent Action Group Invocation Flow

Components:
  [User/Caller Application]
  [Amazon Bedrock Agent API] - InvokeAgent endpoint
  [Bedrock Orchestrator] - Managed Bedrock service
  [Foundation Model (Claude 3 Sonnet)]
  [Action Group Router] - Part of orchestrator
  [AWS Lambda] - Your function code
  [External Data Source] - EHR, payer API, database

Detailed Flow:

1. User Application → Bedrock Agent API
   Request: InvokeAgent({agentId, agentAliasId, sessionId, inputText})
   Protocol: HTTPS, signed with SigV4

2. Bedrock Agent API → Orchestrator
   Orchestrator retrieves: agent config, system prompt, tool schemas,
   KB connection, guardrail config

3. Orchestrator → Foundation Model
   Sends: assembled context (system prompt + tools + conversation + user input)
   Token count: typically 5,000-15,000 tokens on first call

4. Foundation Model → Orchestrator
   Returns: reasoning trace + action decision
   Example: {"thought": "Need claims summary to identify denial patterns", "action": "getClaimsSummary",
              "inputs": {"payer_id": "BCBS-001", "service_line": "Orthopedics", "date_range": "2025-Q4"}}

5. Orchestrator → Action Group Router
   Router looks up: which Lambda handles the "ClaimsAnalyticsGroup" action group

6. Orchestrator → Lambda Function
   Invocation type: RequestResponse (synchronous)
   Payload: Bedrock-formatted event with action, path, parameters
   IAM authorization: Orchestrator assumes BedrockAgentRole,
                     Lambda has resource policy allowing bedrock.amazonaws.com

7. Lambda → External Data Source
   Lambda uses its own execution role (LambdaClaimsRole) to query the claims data warehouse
   Lambda execution role is separate from BedrockAgentRole

8. External Data Source → Lambda
   Returns: requested data as JSON

9. Lambda → Orchestrator
   Returns: Bedrock-formatted response with status and body

10. Orchestrator → Foundation Model
    Sends: updated context including tool result as "observation"
    The tool result is a new message in the conversation

11. Foundation Model → Orchestrator
    Returns: next action OR final answer

12. [Loop continues until final answer or stopping condition]

13. Orchestrator → Bedrock Agent API
    Returns: final answer + full trace

14. Bedrock Agent API → User Application
    Returns: response text + optional trace JSON

Security Boundaries and IAM Roles:

User Application → Bedrock API:
  Caller needs: bedrock:InvokeAgent permission on the specific agent ARN
  Bedrock API validates: caller identity via SigV4

Orchestrator → Lambda:
  Uses: BedrockAgentRole (service role you created)
  Lambda has: resource-based policy permitting bedrock.amazonaws.com from your account

Lambda → Claims Data Warehouse:
  Uses: Lambda execution role (separate from agent role)
  Data warehouse credentials: stored in Secrets Manager, not in Lambda env vars

Logging:
  Step 3,10,11: Token usage logged to CloudWatch (Bedrock native)
  Step 6,9: Lambda CloudWatch log group
  Step 1-14: CloudTrail API audit log
  Full trace: Available in Bedrock trace response (enable in InvokeAgent call)
```

---

## Chapter 4.4 — Testing and Debugging

### The Bedrock Console Test Interface

The Bedrock console includes a built-in test interface for interacting with your agent before building a production caller.

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.21.45 PM.png" alt="Agent Builder page with the Test Agent panel open on the right side showing Enter your message here input and Run button" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The <strong style="color:#5b8dee;">Test Agent</strong> panel is always visible on the right side of the Agent Builder. Type a test query in the <strong style="color:#5b8dee;">"Enter your message here"</strong> field and click <strong style="color:#5b8dee;">Run</strong>. Before testing, always click <strong style="color:#5b8dee;">Prepare</strong> in the top button bar — an unprepared agent will return an error. The test pane shows a live chat with your agent and can display the full reasoning trace.</p>
</div>

**On Screen You Should See:**
- Test pane slides in from the right
- Session ID auto-generated (shown at top)
- "New session" button to reset context
- Text input field at bottom
- Chat-style message display
- "Show trace" toggle (enable this)
- Trace panel (separate collapsible section)

**How to test your agent:**

1. Prepare button: Before testing, click "Prepare" in the agent's main page. The agent will enter PREPARING status (takes 10-60 seconds) then PREPARED. Only PREPARED agents can be tested.

2. Enter test query: In the test input, type a realistic user query:
   ```
   Pull the Q4 2025 claims summary for BlueCross PPO across our Orthopedics service line,
   then compare our actual allowed amounts against their CMS MRF negotiated rates
   and flag any procedure codes where we appear to be underpaid.
   ```

3. Run the query and watch the response build

4. Open the trace to see the agent's reasoning

---

### Interpreting the Trace Output

The trace is your primary debugging tool for understanding agent behavior. Every reasoning step is captured.

> **Enable "Show trace"** during every development session. The trace reveals the agent's internal ReAct loop: Thought → Action → Observation → Thought → ... It's the only way to see which tools were called, with what parameters, and what they returned.

**On Screen You Should See in the trace:**

Each orchestration step shows:
```
Orchestration step N
├── Rationale: [The agent's reasoning text]
│   "I need to retrieve the claims summary for this payer and service line before
│    I can compare allowed amounts against the CMS MRF negotiated rates."
├── Action invocation:
│   Action group: ClaimsAnalyticsGroup
│   API path: /get-claims-summary
│   HTTP method: POST
│   Parameters: [{name: "payer_id", value: "BCBS-001"}, {name: "service_line", value: "Orthopedics"}, {name: "date_range", value: "2025-Q4"}]
└── Observation:
    {
      "status": "success",
      "claims_summary": {
        "payer_id": "BCBS-001",
        "service_line": "Orthopedics",
        "total_claims": 1842,
        "total_billed": 4210500.00,
        "total_allowed": 2876320.00,
        "denial_rate": 0.087,
        "top_denial_codes": ["CO-97", "PR-96", "CO-4"]
      }
    }
```

**What to look for in the trace:**

✅ **Correct reasoning:** Does the agent's rationale make logical sense? Is it reasoning toward the goal?

✅ **Correct tool selection:** Is the agent calling the right tool for the right reason?

✅ **Correct parameters:** Are the parameters correctly extracted from the context?

✅ **Observation utilization:** Does the agent actually USE the tool result in its next step?

❌ **Tool selection errors:** Agent calls the wrong tool, or calls tools unnecessarily

❌ **Parameter extraction failures:** Agent passes wrong values (wrong patient ID, wrong date format)

❌ **Reasoning loops:** Agent repeats the same tool call with the same parameters

❌ **Premature conclusions:** Agent stops before gathering all needed information

❌ **Hallucination in rationale:** Agent's rationale contains information not in any observation

---

### Common Failure Signatures and Their Causes

**Failure Signature 1: "I don't have a tool for that"**
```
Rationale: "I would need to check the formulary, but I don't have a tool
available to perform this action."
```
Cause: Either (a) the tool exists but its description doesn't match the agent's current need, or (b) the tool truly doesn't exist and needs to be added.
Fix: Improve tool description language to better match how the agent phrases the need.

**Failure Signature 2: Parameter Format Errors**
```
Action invocation error: Parameter 'as_of_date' expects format YYYY-MM-DD,
received 'March 5, 2026'
```
Cause: Tool schema specifies a format but the description doesn't make it clear enough for the LLM to always comply.
Fix: In the parameter description, include both the format and an explicit example:
```
"Date in YYYY-MM-DD format. Example: 2026-03-05. Do not use natural language dates."
```

**Failure Signature 3: Repeated Tool Calls**
```
Step 4: query_claims_data(payer_id=BCBS-001, service_line=Orthopedics, date_range=2025-Q4)
Step 5: [reasoning about other things]
Step 6: query_claims_data(payer_id=BCBS-001, service_line=Orthopedics, date_range=2025-Q4)  ← duplicate
```
Cause: The observation from Step 4 was not effectively integrated into context, or the system prompt doesn't instruct against re-fetching already-retrieved data.
Fix: Add to system prompt: "Do not retrieve data you have already retrieved in this session." Also consider using session attributes to track what has been fetched.

**Failure Signature 4: Lambda Invocation Error**
```
Observation: {
  "errorType": "ResourceNotFoundException",
  "errorMessage": "Function not found: arn:aws:lambda:us-east-1:123456789:function:wrong-function-name"
}
```
Cause: Lambda function ARN in action group is incorrect, function doesn't exist in the right region, or function name is wrong.
Fix: Verify Lambda function exists, is in the same region as the agent, and the ARN in the action group is exact.

**Failure Signature 5: Lambda Permission Denied**
```
Observation: {
  "errorType": "AccessDeniedException",
  "errorMessage": "User: arn:aws:sts::123:assumed-role/BedrockAgentRole/... is not authorized to perform lambda:InvokeFunction"
}
```
Cause: BedrockAgentRole doesn't have permission to invoke the Lambda function, OR Lambda doesn't have a resource-based policy allowing Bedrock to invoke it.
Fix: Check both (a) BedrockAgentRole IAM policy includes lambda:InvokeFunction on the function ARN, AND (b) the Lambda function has a resource-based policy allowing bedrock.amazonaws.com.

---

### CloudWatch Logs Analysis

For deeper debugging, Lambda execution logs in CloudWatch provide details the trace doesn't show.

**Navigation:** CloudWatch → Log groups → search "/aws/lambda/claims-analytics-tools" → Most recent log stream → Expand entries

**Key log entries to look for:**

```
START RequestId: 3a4b5c6d ... Version: $LATEST

{"event": "tool_invoked", "tool_name": "ClaimsAnalyticsGroup/get-claims-summary",
 "request_id": "3a4b5c6d", "session_id": "sess-xyz-123", "timestamp": 1709000000.123}

{"event": "claims_warehouse_query_start", "request_id": "3a4b5c6d",
 "payer_id": "BCBS-001", "service_line": "Orthopedics"}

{"event": "claims_warehouse_query_complete", "request_id": "3a4b5c6d",
 "duration_ms": 234.5, "result_status": "success"}

{"event": "tool_completed", "tool_name": "ClaimsAnalyticsGroup/get-claims-summary",
 "request_id": "3a4b5c6d", "duration_ms": 241.2, "result_status": "success"}

END RequestId: 3a4b5c6d
REPORT RequestId: 3a4b5c6d  Duration: 241.23 ms  Billed Duration: 300 ms
       Memory Size: 256 MB  Max Memory Used: 89 MB
```

---

## Chapter 4.5 — Versions and Aliases

### Why Versions and Aliases Matter

In production, you never want users calling the DRAFT version of your agent. The DRAFT version is your working development copy — it changes every time you edit. Production callers must use a stable, immutable version.

**Versions:** A snapshot of your agent configuration at a specific point in time. Versions are immutable — once created, a version's configuration cannot be changed.

**Aliases:** Named pointers to a version. Your application code should always target an alias, not a specific version. When you want to deploy a new version, update the alias to point to the new version — your application code doesn't change.

**The production deployment flow:**

```
1. Edit agent configuration (working on DRAFT)
2. Test DRAFT thoroughly using the console test interface
3. Create new Version (snapshot of current DRAFT)
   → Creates v1, v2, etc. (immutable)
4. Update alias to point to new version:
   - "production" alias: was v1, now v2
   - "staging" alias: was v2, now v3
5. Your application code calls the "production" alias
   → Automatically uses v2 after alias update
6. If v2 has issues: Update "production" alias back to v1
   → Instant rollback without code changes
```

**Creating a version:**
1. Navigate to your agent → Versions tab
2. Click "Create version"
3. Add a description (required — use semantic versioning description)
4. Click "Create version"
5. Wait for version status: CREATING → Created

**Creating an alias:**
1. Navigate to agent → Aliases tab
2. Click "Create alias"
3. Name: "production" or "v1-stable"
4. Route traffic to: Select your new version
5. Advanced: Enable A/B testing to route percentage traffic to two versions

---

## Chapter 4.6 — Guardrails

Guardrails attach to your agent to enforce content policies and protect against misuse. For healthcare agents, guardrails are a critical compliance control.

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.25.40 PM.png" alt="Bedrock Guardrails page showing list of existing guardrails with description, status (Ready), creation time, and last edited columns" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> The <strong style="color:#5b8dee;">Guardrails</strong> management page (Build → Guardrails). The table shows each guardrail's name, description, status (Ready), creation time, and last edited date. Pre-existing guardrails like "HR Metric Analysis," "content safety filtering," and "information access" are visible here. Click <strong style="color:#5b8dee;">Create guardrail</strong> to build a new one.</p>
</div>

**Creating a Guardrail:**

<div style="margin:24px 0;border-radius:10px;overflow:hidden;border:1px solid #2e3147;box-shadow:0 4px 16px rgba(0,0,0,0.3);">
<img src="AWS Bedrock Screenshots/Screenshot 2026-03-02 at 2.25.50 PM.png" alt="Create guardrail step 1 - Provide guardrail details showing Name, Description, Messaging for blocked prompts fields with an 8-step wizard on the left" style="width:100%;display:block;">
<p style="margin:0;padding:10px 14px;background:#222538;font-size:0.82rem;color:#8b90a8;border-top:1px solid #2e3147;font-style:italic;"><strong style="color:#5b8dee;">📸</strong> Step 1 of the Create guardrail wizard. The left panel shows all 8 steps: provide guardrail details, configure content filters, add denied topics, add word filters, add sensitive information filters, add word filters, add contextual grounding check, review and create. <strong style="color:#5b8dee;">Messaging for blocked prompts</strong> is the message your agent returns when a guardrail blocks a request — for healthcare, use something like "Sorry, the model cannot answer this question."</p>
</div>

**Key guardrail configuration options for healthcare agents:**
- **Content filters:** Block harmful content (hate, violence, sexual content) — set thresholds per category
- **Denied topics:** Explicitly block topics outside agent scope (e.g., "legal advice," "investment recommendations")
- **Sensitive information filters:** Automatically detect and mask PII (SSN, credit card numbers, phone numbers)
- **Contextual grounding check:** Prevent hallucination by requiring responses to be grounded in retrieved context

---

## Chapter 4.7 — Programmatic Agent Invocation

### Calling Bedrock Agents from Python

```python
import boto3
import json
import uuid

def invoke_financial_analytics_agent(
    user_query: str,
    session_id: str = None,
    include_trace: bool = False
) -> dict:
    """
    Invokes the Financial Analytics agent and returns the response.

    Args:
        user_query: The user's input text
        session_id: Session ID for conversation continuity.
                   Generate a new UUID for new sessions.
                   Reuse the same ID for follow-up turns.
        include_trace: If True, returns full orchestration trace.

    Returns:
        dict with 'response' (str) and optionally 'trace' (list)
    """

    bedrock_agent_runtime = boto3.client(
        'bedrock-agent-runtime',
        region_name='us-east-1'
    )

    AGENT_ID = 'ABCDEFGHIJ'        # Your agent ID
    AGENT_ALIAS_ID = 'TSTALIASID'  # Your alias ID (use specific alias for prod)

    if session_id is None:
        session_id = str(uuid.uuid4())

    response = bedrock_agent_runtime.invoke_agent(
        agentId=AGENT_ID,
        agentAliasId=AGENT_ALIAS_ID,
        sessionId=session_id,
        inputText=user_query,
        enableTrace=include_trace,
        # Optional: inject session-level context
        sessionState={
            'sessionAttributes': {
                'user_type': 'revenue_cycle_analyst',
                'facility_id': 'FAC-001',
                'workflow_context': 'claims_rate_analysis'
            }
        }
    )

    # The response is a streaming EventStream
    # Collect all chunks
    full_response = ""
    trace_events = []

    for event in response['completion']:
        if 'chunk' in event:
            # Response text chunks
            chunk = event['chunk']
            full_response += chunk['bytes'].decode('utf-8')

        elif 'trace' in event and include_trace:
            # Trace events (reasoning steps)
            trace_events.append(event['trace'])

    result = {
        'session_id': session_id,
        'response': full_response,
        'token_usage': extract_token_usage(response)
    }

    if include_trace:
        result['trace'] = trace_events

    return result


# Example usage:
if __name__ == "__main__":
    # New session
    session = str(uuid.uuid4())

    result = invoke_financial_analytics_agent(
        user_query="Pull Q4 2025 claims for BCBS PPO in Orthopedics and compare allowed amounts to MRF rates",
        session_id=session,
        include_trace=True
    )

    print(f"Agent response: {result['response']}")
    print(f"Session ID: {result['session_id']}")

    if 'trace' in result:
        print(f"Orchestration steps: {len(result['trace'])}")
        for i, step in enumerate(result['trace']):
            if 'orchestrationTrace' in step:
                orch = step['orchestrationTrace']
                if 'rationale' in orch:
                    print(f"  Step {i+1} rationale: {orch['rationale']['text'][:100]}...")
```

---

## Chapter 4.8 — Module 4 Reflection Prompts

1. You have built a Financial Analytics Agent with two action groups: `ClaimsAnalyticsGroup` (containing `query_claims_data`, `get_denial_patterns`, `get_allowed_amounts`) and `RateTransparencyGroup` (containing `get_negotiated_rates`, `compare_market_rates`, `get_chargemaster_rates`). During testing you find the agent sometimes calls `get_chargemaster_rates` when it should call `get_allowed_amounts` — even for questions clearly about what was actually paid versus billed. What are the likely causes and how would you diagnose and fix the tool selection error?

2. Your Financial Analytics Agent is in production and has been accurately flagging underpayments for three months. This week, revenue cycle analysts report the agent is no longer finding rate discrepancies it previously caught. No agent configuration or Lambda code was deployed. What do you investigate first, and what CMS MRF or claims data pipeline changes would you check?

3. Your Financial Analytics Agent averages 52 seconds per analysis session when running a full payer rate variance report (claims summary → MRF negotiated rates → market comparison → contribution margin). The managed care contracting director needs this under 30 seconds. Without changing the underlying model, what architectural changes would you consider to reduce latency? What are the tradeoffs of parallel tool invocation, pre-computed rate caches, and streaming responses?

4. Design the IAM trust relationship and permissions for a Financial Analytics Agent that needs to: (a) query a claims data warehouse via Lambda, (b) retrieve CMS MRF negotiated rates from an S3-backed data store via a second Lambda, (c) pull GL and payroll data from a Redshift cluster via a third Lambda. Write the IAM policies for the BedrockAgentRole and each Lambda execution role, applying least-privilege principles.

5. A junior analyst on your revenue cycle team wants to embed the Redshift cluster credentials and claims database connection string directly in Lambda environment variables for simplicity. Write a detailed explanation of why this approach is wrong in a healthcare financial data context, what the correct approach is using AWS Secrets Manager and IAM roles, and how you would implement and rotate those credentials without Lambda redeployment.

---

*End of Module 4 Textbook Content*
