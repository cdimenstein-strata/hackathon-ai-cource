# POWERPOINT SLIDE DECK OUTLINE
## Designing and Deploying Agentic AI Systems with Amazon Bedrock
## Complete Slide Deck — 12-Week Course

**Deck Structure:** ~120 slides across all modules
**Format:** Keynote / PowerPoint compatible
**Visual style:** Dark professional theme, AWS blue (#232F3E) with white text, orange (#FF9900) accents

---

# SECTION 1: COURSE INTRODUCTION SLIDES

---

## SLIDE 1 — Title Slide

**Title:** Designing and Deploying Agentic AI Systems with Amazon Bedrock

**Subtitle:** A Postgraduate Course for Healthcare Data Scientists

**Visual Description:**
Background: Abstract neural network visualization fading to AWS dark theme. Lower left: AWS Bedrock logo. Lower right: organization/institution logo placeholder.

**Speaker Notes:**
Welcome everyone. This course is designed for experienced data scientists who are making a career transition that I believe is one of the most important transitions in enterprise AI right now: from building models to building intelligent systems. The next 12 weeks will challenge the mental models you've developed building ML pipelines. Agentic systems require a completely different way of thinking about software, about evaluation, about failure, and about risk — especially in healthcare. Let's get into it.

---

## SLIDE 2 — The Second Inflection Point

**Title:** We Are at a Second Inflection Point

**Content:**
Inflection 1 (2015-2023): Supervised ML
- Predictive models, classification, regression
- Model-centric thinking
- You control the inputs and outputs

Inflection 2 (2024+): Agentic AI
- Intelligent systems that reason, act, and learn
- System-centric thinking
- The system controls its own path

**Visual Description:**
Timeline diagram showing two curves inflecting upward. First labeled "ML Era" with icons for prediction, classification. Second labeled "Agent Era" with icons for orchestration, tools, memory. Both timelines annotated with healthcare examples.

**Speaker Notes:**
We didn't get here suddenly. The first inflection — supervised ML — gave us risk scores, imaging AI, fraud detection. These were real improvements. But they were fundamentally reactive: input goes in, prediction comes out. An agentic system is different. It reads a goal, figures out what to do, does it, reads what happened, and adapts. This course is about building those systems, in healthcare, in production, under regulatory constraints.

---

## SLIDE 3 — What You Will Build

**Title:** By Week 12, You Will Build

**Content:**
✓ A production-grade Bedrock agent with multiple action groups
✓ A knowledge base with clinical documentation
✓ Evaluation pipelines with automated and human review
✓ Complete monitoring and observability stack
✓ A healthcare-specific capstone system

**Visual Description:**
Centered on a completed Bedrock agent architecture diagram (simplified). Four callout boxes around it pointing to: Lambda tools (bottom left), Knowledge base (bottom right), Guardrails (top right), CloudWatch (top left). Each callout shows a small icon of what students will build.

**Speaker Notes:**
This is not a survey course. You will build real things. The capstone will be a working Bedrock agent system for a healthcare use case of your choice. By the time you present it in Week 12, you'll have something you could take into a real organization.

---

# SECTION 2: MODULE 1 SLIDES — FOUNDATIONS

---

## SLIDE 4 — The Spectrum

**Title:** Not All AI Systems Are Agents

**Content:** (minimal text — the visual carries this slide)

**Visual Description:**
Wide horizontal spectrum bar from left to right:
- Left: "Single LLM Call" — icon of a single arrow
- Middle-left: "Prompt Chain" — icon of linked arrows
- Middle-right: "Tool-Using Agent" — icon of a node with multiple arms
- Right: "Multi-Agent System" — icon of interconnected nodes

Below the bar, for each point on the spectrum:
- Cost: $ → $$ → $$$ → $$$$
- Reliability: High → Medium → Medium-Low → Requires Design
- Flexibility: None → Low → High → Very High

A pulsing dot on the spectrum at "Tool-Using Agent" labeled "Where Bedrock Agents Live"

**Speaker Notes:**
Before we can build agents, we have to understand where they fit in the landscape. There's a habit in this industry of calling everything an "agent" when most of what people build is actually a prompt chain. The distinction matters because: the right solution for a fixed, known workflow is a chain. The right solution for a dynamic, multi-step, unknown-path workflow is an agent. Using the wrong pattern wastes money, increases latency, and makes your system harder to test. This slide is the foundation of that decision.

---

## SLIDE 5 — The Six Components

**Title:** Every Agent Has Six Components

**Content:**
1. Reasoning Engine (LLM) — decides what to do
2. Tools — acts on the world
3. Memory — remembers across steps
4. Knowledge — knows the domain
5. Planning — decomposes goals
6. State — tracks current progress

**Visual Description:**
Hexagon with each component at a vertex, connected by lines. Each vertex has a small icon: brain (reasoning), wrench (tools), filing cabinet (memory), book (knowledge), map (planning), database (state). The center of the hexagon shows "AGENT" with arrows flowing from all six points inward.

**Speaker Notes:**
Every agent, regardless of what framework it's built in, regardless of what model it uses, has these six components. You can evaluate any vendor's "agent product" by asking: how does it handle each of these? Bedrock Agents has explicit support for all six: the foundation model is the reasoning engine, action groups are tools, session attributes handle state and short-term memory, knowledge bases handle semantic memory, the ReAct pattern handles planning. Understanding this framework means you can understand any agent architecture on day one.

---

## SLIDE 6 — ReAct Pattern (The Core Loop)

**Title:** The ReAct Loop: How Bedrock Agents Think

**Content:**
Think → Act → Observe → Repeat

**Visual Description:**
Circular flow diagram with 5 stages:
1. THINK (LLM bubble): "What should I do next?"
2. ACT (Lambda icon): Call a tool
3. OBSERVE (document icon): Read the result
4. UPDATE (context icon): Add result to context
5. DECIDE (fork icon): Conclude or continue?
→ Arrow back to THINK if continue
→ Arrow to RESPOND if conclude

Sidebar: "In Bedrock, every Thought + Action + Observation = one orchestration step (visible in trace)"

**Speaker Notes:**
The ReAct pattern is the backbone of Bedrock Agents. Every single thing Bedrock does when running your agent follows this loop. Think: the foundation model reads all context and produces a thought and an action. Act: the orchestrator calls your Lambda function. Observe: the Lambda result comes back and is added to the conversation. Then the model sees the updated context and decides whether to act again or respond. This loop is what you see in the trace viewer. Understanding this loop is what allows you to debug agents.

---

## SLIDE 7 — Why Data Scientists Struggle (Part 1)

**Title:** The Hardest Mental Shift

**Content:**
ML Mindset                    Agent Mindset
────────────────              ────────────────
Optimize the model     →      Orchestrate the system
Model fails = bad model →     System fails = multiple possible causes
Evaluate on test set   →      Evaluate on behavioral scenarios
Version the model      →      Version the system
Monitor model drift    →      Monitor system behavior

**Visual Description:**
Two-column layout with a sharp dividing line (or contrasting colors). Left column: traditional ML workflow with "Model → Evaluate → Deploy" linear path. Right column: agent system with a complex web of interconnected components.

**Speaker Notes:**
This slide captures the transition most clearly. When your ML model has poor performance, you improve the model — better features, better architecture, better training. When your agent has poor performance, you investigate: was it the model's reasoning? A bad tool description? A Lambda error? A knowledge base gap? A state management bug? The failure could be anywhere in the system. This is a different debugging discipline entirely. Your existing ML debugging intuition won't tell you which component failed. You need system-level observability.

---

## SLIDE 8 — Healthcare Case Study: PA Agent

**Title:** Case Study: Prior Authorization in 22 Minutes

**Content:**
Before: 3.5 hours per PA initiation (pharmacy staff)
After: 22 minutes (agent + pharmacist review)

What the agent does:
→ Retrieves patient demographics and coverage
→ Looks up PA requirements for drug/payer
→ Gathers clinical documentation
→ Checks step therapy compliance
→ Drafts PA package
→ Routes for pharmacist review

**Visual Description:**
Before/after comparison. Left: cluttered desk with multiple system windows, phone, paper forms — overwhelmed pharmacist. Right: clean dashboard showing PA package ready for review with checkmarks on each gathered element. Timeline bars: Before (3.5h bar, red), After (22min bar, green).

**Speaker Notes:**
This is a real-world outcome from a specialty pharmacy deployment. What I want you to notice is what the agent does and does NOT do. It gathers, retrieves, cross-references, and drafts. It does NOT submit. The pharmacist still reviews and approves before submission. That architectural decision — human review before submission — is not a limitation. It is correct risk management. As you design your own agents, you will make these same decisions about where human oversight belongs.

---

## SLIDE 9 — Module 1 Summary

**Title:** Module 1: What to Take Away

**Content:**
□ Agents are NOT chatbots or prompt chains
□ Use agents when the workflow path is variable and unknown
□ Every agent has 6 components — design each explicitly
□ The mental shift: model-centric → system-centric
□ Healthcare context changes every design decision

**Speaker Notes:**
Before we move to Module 2, questions? The concepts in this module are foundational. If the spectrum (when to use an agent) and the six components are clear, everything that follows will make sense. If they're fuzzy, revisit this before Module 2.

---

# SECTION 3: MODULE 2 SLIDES — METRICS

---

## SLIDE 10 — The Metric Problem

**Title:** Why Agent Metrics Are Hard

**Content:**
ML Metrics:                    Agent Metrics:
• Accuracy: ✓ clear            • Task completion: what counts as complete?
• AUC-ROC: ✓ well-defined      • Tool correctness: requires ground truth
• RMSE: ✓ calculable           • Hallucination: hard to detect at scale
• Cross-validate: ✓            • Latency: multiplicative across steps
                               • Safety: requires domain expertise

→ Agents need a PORTFOLIO of metrics, not a single score

**Visual Description:**
Left panel: Clean ML evaluation funnel — data → train → test → single number. Right panel: Agent evaluation web — multiple evaluation pathways (automated, LLM judge, human review, adversarial) feeding into a central "metrics portfolio" circle.

**Speaker Notes:**
There's a temptation to find the single number that tells you whether your agent is performing well. Resist it. There is no single number. A high task completion rate with high hallucination rate is a dangerous agent. A high accuracy score with catastrophically high under-triage rate is a dangerous agent. You need a portfolio. The skill is knowing what to include in that portfolio and how to interpret it together.

---

## SLIDE 11 — The Six Core Metrics

**Title:** Core Agent Metrics

**Content:**

| Metric | Measures | Healthcare Threshold |
|--------|----------|---------------------|
| Task Completion Rate | % sessions with complete output | ≥ 95% |
| Tool Correctness | % correct tool calls | ≥ 98% |
| Hallucination Rate | % outputs with unsupported claims | < 0.1% clinical |
| Latency p95 | 95th percentile session time | Use case dependent |
| Cost/Session | USD per agent interaction | Budget-dependent |
| Safety Score | Compliance with safety constraints | 100% |

**Visual Description:**
Six tiles in a 2×3 grid. Each tile: metric name at top, large percentage/number in center, bar graph showing current vs. target at bottom. Two tiles should be highlighted red (indicating below threshold) to reinforce that monitoring matters.

**Speaker Notes:**
Walk through each metric. Note the hallucination rate threshold: less than 0.1% for clinical claims means out of 1,000 clinical statements, fewer than 1 can be wrong. That sounds strict because it is strict. In a PA letter, if the agent hallucinate a lab value, the payer may deny the authorization. In a clinical decision support context, if the agent hallucinate a drug interaction, a patient could be harmed. Set thresholds appropriate to stakes.

---

## SLIDE 12 — Evaluation Framework

**Title:** Three Complementary Evaluation Approaches

**Content:**
1. Synthetic Test Sets
   → 500+ predefined scenarios
   → Automated, fast, repeatable

2. Human Review Pipeline
   → Sampled outputs reviewed by domain experts
   → Catches clinical accuracy issues automation misses

3. LLM-as-Judge
   → Scales between automated and human
   → Use with calibration (bias correction)

**Visual Description:**
Pyramid diagram. Base: "Synthetic Test Sets" (widest, highest volume). Middle: "LLM-as-Judge" (medium). Top: "Human Review" (narrowest, highest fidelity). Arrows on each side of the pyramid: left side "Volume" (high at base, low at top), right side "Accuracy / Clinical Fidelity" (low at base, high at top).

**Speaker Notes:**
Think of this as a pyramid. The synthetic tests are wide — you run them on every deployment. They catch regressions quickly and cheaply. LLM-as-judge catches quality issues at scale — 1,000 sessions a day sampled at 10% = 100 sessions reviewed automatically. Human review is narrow but deep — you sample maybe 2-5% of sessions, but a clinical expert is actually reading the output and judging clinical correctness. All three layers are necessary. None is sufficient alone.

---

## SLIDE 13 — Adversarial Evaluation for Healthcare

**Title:** Healthcare Agents Require Adversarial Testing

**Content:**
Must test before deployment:
• Prompt injection (bypass safety instructions)
• Scope creep (exceed agent's defined role)
• Authority manipulation ("I'm the admin")
• Hallucination inducement ("Confirm this false fact")
• PHI cross-contamination (access wrong patient)

Target: 100% refusal rate on adversarial scenarios

**Visual Description:**
Red "attack" arrows coming in from multiple angles against a green "defense" shield in the center. Each attack arrow labeled with attack type. Behind the shield: the agent architecture diagram. Below: "Every adversarial scenario must fail to breach the shield BEFORE production deployment."

**Speaker Notes:**
You will test adversarial scenarios. This is not optional. Before anything goes near production in a healthcare context, you need an adversarial evaluation set with at least 50 scenarios. I've seen agents fail all of these in demos that were "ready for production." An agent that can be manipulated into accessing the wrong patient's data is a HIPAA breach waiting to happen.

---

# SECTION 4: MODULE 3 SLIDES — ARCHITECTURE

---

## SLIDE 14 — Context Assembly Deep Dive

**Title:** What Goes Into Every LLM Call

**Content:**
Every single LLM reasoning step includes:
→ System prompt (full, every time)
→ Tool definitions (all tools, every time)
→ Full conversation history
→ Memory injections
→ Latest user input + prior tool observations

Implication: A 10,000-token system prompt × 8 steps = 80,000 tokens of system prompt cost alone

**Visual Description:**
Stack diagram showing layers of context building up. At bottom: System Prompt (large block). Above it: Tool Definitions (medium block). Above: Conversation History (growing arrow). Above: Memory. At top: Current Step Context. Total token count shown on the right side as a growing counter. A cost calculator in the corner showing "$X per step" updating with each layer.

**Speaker Notes:**
This is the insight that changes how you write system prompts. Every character in your system prompt costs money — not once, but on every single LLM call in every agent session. If your system prompt is 15,000 tokens and your agent runs 10 iterations, that's 150,000 input tokens just from the system prompt. At $0.003/1K tokens for Claude 3 Sonnet, that's $0.45 of your session cost just from system prompt. Trim it ruthlessly. Remove anything that doesn't actively guide behavior.

---

## SLIDE 15 — The Tool Description Is Code

**Title:** Tool Descriptions Are Not Documentation — They Are Code

**Content:**
BAD:
```
name: insurance_tool
description: Gets insurance info
```

GOOD:
```
name: get_patient_insurance_coverage
description: Retrieves current active insurance coverage
for a patient. Use BEFORE checking PA requirements or
recommending procedures. Returns plan name, payer ID,
PA requirements, formulary tier.
Do NOT use for historical coverage — use get_historical_coverage.
```

**Visual Description:**
Side by side code blocks. Left: red-bordered, labeled "POOR (will cause tool selection failures)". Right: green-bordered, labeled "PRODUCTION QUALITY (clear when, what, and what NOT to use)". An arrow below showing the same query being routed incorrectly with the bad description and correctly with the good description.

**Speaker Notes:**
I cannot overstate this. In production Bedrock deployments, the most common failure I see is poor tool descriptions. The LLM reads these descriptions to decide what to do. If the description is vague, the LLM makes vague tool selections. If the description says when NOT to use the tool, the LLM respects that. Write tool descriptions the same way you'd write a detailed method comment for a very junior developer who needs to understand not just what the function does but when and how to use it correctly.

---

## SLIDE 16 — Memory Types

**Title:** Four Types of Agent Memory

**Content:**
1. In-Context Memory
   → Conversation window | Fast | Bounded by context limit

2. Session State (Bedrock Session Attributes)
   → Current session only | Automatic | Key-value

3. External Short-Term (DynamoDB)
   → Hours/days | Queryable | Cross-turn

4. Semantic Long-Term (Vector Store)
   → Persistent | Searchable by meaning | Cross-session

**Visual Description:**
Four horizontal layers, like geological strata. Top layer (thin, fast, volatile): "In-Context Memory" — flashing animation suggesting volatility. Second layer: "Session State" — moderate thickness, session-scoped bracket. Third: "External Short-Term" — thicker, DynamoDB icon. Bottom: "Semantic Long-Term" — thickest, most stable, OpenSearch icon. Depth arrows on right side: "Persistence" increases downward.

**Speaker Notes:**
Most demos use only the first type. In-context memory is simple and fast, but it's gone when the session ends. For healthcare use cases — a patient coaching agent that should remember that a patient declined statins last month, or a PA agent that should remember a workflow it started yesterday — you need external memory. The architecture decision is: what needs to persist, for how long, and in what queryable format?

---

## SLIDE 17 — Guardrails Architecture

**Title:** Guardrails: Safety at the Inference Layer

**Content:**
Bedrock Guardrails provides:
→ Content filters (harm categories)
→ Topic restrictions ("never prescribe")
→ PII/PHI redaction from outputs
→ Grounding checks (hallucination detection)

Applies to: every model call, every direction (input AND output)

**Visual Description:**
The Bedrock agent architecture diagram from Module 1, but with a "Guardrails" layer visible as a transparent orange shield around the Foundation Model component. Input arrow passes through the shield; output arrow passes through the shield. Small icons on the shield indicating: filter (content), stop sign (topic), mask (PII), checkmark (grounding).

**Speaker Notes:**
Guardrails are your last line of defense. Everything else in your architecture can fail and guardrails can still catch safety violations. For healthcare agents, you want AT MINIMUM: topic denials for clinical prescribing, PII redaction from outputs, and grounding checks. Configure these before you deploy anything to production. The healthcare-specific guardrails I recommend: deny "prescribe medication," deny "provide diagnosis," deny "legal advice," redact SSN and full name from outputs, set grounding threshold at 75%.

---

## SLIDE 18 — Failure Mode Analysis

**Title:** Six Ways Agents Fail in Production

**Content:**
1. Tool selection error — wrong tool called
2. Parameter extraction failure — correct tool, wrong inputs
3. Context overflow — too many steps, degraded reasoning
4. Tool execution failure — Lambda error, API down
5. Reasoning loop — agent repeats same actions
6. Premature conclusion — agent stops too early

**Visual Description:**
Six failure mode cards arranged in a 2×3 grid. Each card: failure name (bold), brief description, example trace snippet showing the failure signature, and a small icon (red X). Below the grid: a progress bar showing "One of these WILL occur in your first production deployment. Plan for all of them."

**Speaker Notes:**
You will see all six of these in the trace viewer at some point. Let me tell you what each looks like in practice so you can recognize it immediately. [Walk through each failure mode with trace examples.] The key insight: each failure mode has a different root cause and a different fix. Tool selection errors → fix the tool description. Context overflow → reduce response sizes, add summarization. Reasoning loops → add max iteration limits and detect repeated calls in session state.

---

# SECTION 5: MODULE 4 SLIDES — BEDROCK HANDS-ON

---

## SLIDE 19 — Bedrock Architecture Overview

**Title:** Amazon Bedrock: More Than a Model API

**Content:**
Foundation Models ←— The model portfolio (Claude, Titan, Llama)
Bedrock Agents ←— Managed orchestration (what we're building)
Knowledge Bases ←— Managed RAG (next module)
Guardrails ←— Safety layer (deployed today)
Model Evaluation ←— Offline evaluation tools
Bedrock Flows ←— Visual pipeline builder

**Visual Description:**
AWS service diagram showing Bedrock as a central hub with spokes to each service. Each spoke labeled with the service name. Small icons representing what each service does. Highlight ring around "Bedrock Agents" to indicate current focus.

**Speaker Notes:**
Bedrock is not just an API endpoint for Claude. It's a platform. For this course, we focus primarily on Agents and Knowledge Bases because those are the components for building production healthcare systems. But understanding the full platform helps you make architecture decisions: when do you use Flows vs. custom agent? When is Model Evaluation useful? We'll touch these appropriately.

---

## SLIDE 20 — Bedrock Console: Create Agent

**Title:** Creating Your First Bedrock Agent

**Content:**
Console Path: Amazon Bedrock → Builder tools → Agents → Create Agent

Required fields:
• Agent name (permanent)
• Foundation model (can change later)
• IAM role (pre-create this!)
• Instructions / System prompt

**Visual Description:**
AWS Console mockup showing the Create Agent form. Key fields highlighted with colored boxes: Agent name (red box + "permanent"), Foundation model (orange box + "Claude 3 Sonnet recommended"), IAM role (blue box + "pre-create as least-privilege"), Instructions (green box + "this is the most important field"). Note at bottom: "Status will be NOT_PREPARED after creation — you must Prepare before testing."

**Speaker Notes:**
[SCREENSHOT TIME: Show actual console] Three things to emphasize here. One: the agent name is permanent. Cannot be changed. Name it descriptively from the start. Include environment in the name. Two: IAM role — DO NOT let Bedrock create a default role. Pre-create a least-privilege role. The auto-created role is too permissive for healthcare deployments. Three: the Instructions field — this is your system prompt. This is the most important thing you write for this agent. Every word here is read by the LLM on every single call. Write it carefully.

---

## SLIDE 21 — Action Groups

**Title:** Action Groups: Your Agent's Toolbox

**Content:**
Action Group = Named collection of tools + Lambda backend + OpenAPI schema

Your agent can have multiple action groups:
• PatientDataGroup → patient-data-lambda
• InsuranceGroup → insurance-tools-lambda
• ClinicalCodingGroup → coding-lambda

All tools across all groups available to agent simultaneously

**Visual Description:**
Three-tier diagram:
Top: "Bedrock Agent" oval
Middle: Three "Action Group" boxes (PatientDataGroup, InsuranceGroup, ClinicalCodingGroup) connected to agent by lines
Bottom: Three "Lambda" icons, one under each action group
Between action groups and Lambda: "OpenAPI Schema" document icons

**Speaker Notes:**
An action group is the bridge between the Bedrock orchestrator and your Lambda code. The OpenAPI schema tells Bedrock what functions exist and how to call them. The Lambda function actually runs the code. One Lambda function can handle multiple operations — your Lambda handler routes to different internal functions based on the apiPath. In the lab today, you'll create one action group with one Lambda function handling three operations.

---

## SLIDE 22 — Lambda Event Structure

**Title:** What Bedrock Sends to Your Lambda

**Content:**
```python
event = {
  "actionGroup": "PatientDataGroup",
  "apiPath": "/get-patient-coverage",
  "httpMethod": "POST",
  "parameters": [
    {"name": "patient_id", "value": "MRN-12345"}
  ],
  "sessionAttributes": { ... }
}
```

Your Lambda must return:
```python
return {
  "actionGroup": event["actionGroup"],
  "apiPath": event["apiPath"],
  "httpMethod": event["httpMethod"],
  "httpStatusCode": 200,
  "responseBody": {
    "application/json": {
      "body": json.dumps(result)
    }
  }
}
```

**Visual Description:**
Two code blocks side by side. Left: "What you receive (event structure)" with syntax highlighting. Right: "What you must return" with syntax highlighting. Arrow from left to right showing the transformation. Warning callout at bottom: "If your response doesn't match this structure, Bedrock cannot parse it and the agent will fail."

**Speaker Notes:**
This slide is going to save you an hour of debugging. The Bedrock Lambda integration requires a very specific event structure and an equally specific response structure. I have seen countless developers spend hours debugging agent failures that turned out to be a malformed Lambda response. Print this slide out and keep it next to your keyboard during the lab. Every key in that response object is required.

---

## SLIDE 23 — Trace Viewer Deep Dive

**Title:** Reading the Bedrock Trace

**Content:**
Each orchestration step shows:
• Rationale: "What the agent was thinking"
• Action invocation: tool name + parameters
• Observation: tool result

Look for:
✓ Logical rationale → correct reasoning
✓ Correct tool selection → description is working
✓ Correct parameters → extraction is working
✗ Repeated calls → reasoning loop
✗ Wrong parameters → description needs improvement
✗ Ignored errors → agent not handling failures

**Visual Description:**
Annotated trace screenshot (mockup). Each component of one orchestration step is labeled with callout boxes explaining what it means. Color coding: green = healthy, red = failure signature. Three example trace snippets shown as inserts, each with annotation: "Healthy trace," "Reasoning loop," "Tool selection error."

**Speaker Notes:**
The trace viewer is the most powerful debugging tool you have for Bedrock Agents. Once you understand what you're looking at, you can debug most agent failures in under 5 minutes just by reading the trace. Let me walk through each component. The rationale is the agent's internal monologue — what it thinks it's doing. If the rationale is wrong, you need to look at your system prompt or the context the agent has at that point. If the rationale is right but the action is wrong, you need to look at your tool descriptions. If the action is right but the result is wrong, you need to look at your Lambda code.

---

## SLIDE 24 — What Happens When You Click "Prepare"

**Title:** Behind the Scenes: Agent Preparation

**Content:**
When you click Prepare, Bedrock:
1. Validates system prompt (token count, format)
2. Validates all action group schemas
3. Compiles tool definitions into LLM-readable format
4. Validates knowledge base connections
5. Compiles guardrail configuration
6. Creates the "executable agent" snapshot

Status: NOT_PREPARED → PREPARING → PREPARED

**Visual Description:**
Flowchart showing the preparation pipeline with status transitions. Each step in the pipeline has a checkmark (success) or X (failure). A "compilation" metaphor: raw source files (system prompt, schemas, KB connections) going through a compiler symbol producing an "executable agent" artifact. Timeline showing typical preparation time: "5-30 seconds."

**Speaker Notes:**
Preparation is compilation. Just like compiling code converts source to executable, Preparing an agent converts your configuration into something the Bedrock runtime can execute. If preparation fails, you get an error message telling you what's wrong — usually an invalid schema, an unreachable Lambda ARN, or a token limit exceeded on the system prompt. If preparation succeeds, your agent is ready. One important note: the DRAFT version must be Prepared before every test, even if you just made a small change.

---

# SECTION 6: MODULE 5 SLIDES — KNOWLEDGE BASES

---

## SLIDE 25 — The RAG Promise

**Title:** RAG: The LLM Knows Where to Look It Up

**Content:**
Without RAG: LLM answers from training data
→ Training cutoff, organization-agnostic, unauditable

With RAG: LLM retrieves from YOUR documents
→ Current, organization-specific, citable

Formula: Better clinical answers = Retrieve from authoritative source + Generate grounded response

**Visual Description:**
Two-path comparison. Left path: "Without RAG" — LLM brain icon with fog overlay, output with "?" question mark, citation "(training data, unknown date)". Right path: "With RAG" — document icon → vector search → LLM → output with checkmark, citation "(AHA Guidelines 2024, Page 47)". Bottom: "HIPAA note: The knowledge base contains guidelines, NOT patient data."

**Speaker Notes:**
RAG changes the reliability equation for healthcare AI. Without RAG, the LLM is doing medicine from memory — and its memory may be out of date, inaccurate for your specific formulary, or inconsistent with your organization's protocols. With RAG, the LLM is reading from your approved, current, curated documents. It can fail — if the document doesn't contain the answer, or if chunking splits the answer across two chunks that don't both get retrieved — but the failure modes are understandable and addressable.

---

## SLIDE 26 — Chunking Strategy

**Title:** Chunking: The Most Important KB Configuration Decision

**Content:**
Chunk too large:
→ Irrelevant content dilutes the answer
→ Expensive retrieval

Chunk too small:
→ Context is incomplete
→ Answer is split across chunks

**Sweet spot for clinical documents:**
Fixed size: 512 tokens, 100-token overlap

Test: does a retrieved chunk contain enough to answer a question?

**Visual Description:**
Three document strip visualizations side by side. Left: "Too large" — entire multi-page document as one chunk, retrieval returns too much context (visualization: a wide, messy blob). Middle: "Too small" — thin slices, key sentence split at boundary, retrieval misses the complete thought. Right: "Just right (512 tokens, 20% overlap)" — clean chunks with highlighted overlap zones. Bottom: graph showing Retrieval Quality vs. Chunk Size with a peak in the middle.

**Speaker Notes:**
I've seen healthcare knowledge bases fail entirely because of poor chunking. A clinical guideline that says "Use beta-blockers in heart failure unless [contraindication that starts on the next page]" — if the chunk boundary is between "beta-blockers in heart failure" and the contraindication, any query about beta-blocker use in heart failure gets the first half and misses the essential caveat. Overlap exists specifically to address this. Test your chunking by looking at actual retrieved chunks for representative queries. If retrieved chunks contain partial thoughts, your chunks are too small or don't have enough overlap.

---

## SLIDE 27 — What Happens at Sync

**Title:** Knowledge Base Sync: Step by Step

**Content:**
1. Document Discovery — scan S3, find new/changed/deleted
2. Text Extraction — parse PDF/Word/HTML to plain text
3. Chunking — split into configured chunk size
4. Embedding — Titan Embeddings V2 converts each chunk to vector
5. Indexing — write vectors to OpenSearch Serverless
6. Deletion — remove old vectors for deleted docs

Cost: per 1K tokens of content embedded (~$0.10/1M tokens)
First sync of 200 guideline documents ≈ $4-10

**Visual Description:**
Pipeline diagram: S3 bucket → Document Loader → Text Chunker → Titan Embeddings API → OpenSearch Serverless. Each stage shows timing estimate below. After the pipeline: OpenSearch icon showing "k-NN Index" with sample vectors visualized as colored dots in a 2D projection. "Now ready for semantic search" annotation.

**Speaker Notes:**
The sync is the most critical ongoing operation for a knowledge base. Every time guidelines update, you sync. Every time a payer policy changes, you sync. Understanding what sync does helps you reason about cost (it scales with document volume) and timing (large corpora can take hours). Automate your sync cadence: monthly for clinical guidelines, quarterly for formulary. And always validate after sync: run your retrieval evaluation set immediately after sync to confirm the updated documents are being retrieved correctly.

---

# SECTION 7: MODULE 6 SLIDES — MCP

---

## SLIDE 28 — The MCP Vision

**Title:** Model Context Protocol: Universal Tool Standard

**Content:**
Problem: Every AI framework has different tool formats
• Bedrock Action Groups: OpenAPI schema
• LangChain: Python function + docstring
• Claude Desktop: MCP JSON format
• AutoGen: Custom definition

Solution: MCP = one standard format for all

Build once, use everywhere

**Visual Description:**
Before MCP: Five different AI clients each with their own connecting wires to five different tool backends — 25 different connections, chaotic. After MCP: Same five clients and five backends, but all communicating through a central MCP protocol layer — clean, standardized. Caption: "MCP reduces N×M connections to N+M."

**Speaker Notes:**
MCP is to AI tools what HTTP is to web services. Before HTTP, every application had a different way of communicating over networks. HTTP standardized it. MCP standardizes tool communication. The practical impact for enterprise healthcare: if you have five AI applications and ten tool services, without MCP you potentially need 50 integration pairs. With MCP, you need 5+10=15 implementations. The savings scale with complexity.

---

## SLIDE 29 — MCP vs. Direct Lambda

**Title:** When to Use MCP vs. Direct Lambda

**Content:**

| | Direct Lambda | MCP Server |
|-|--------------|------------|
| Clients | Bedrock only | Any MCP client |
| Latency | Lower | Higher (+50-150ms) |
| Complexity | Lower | Higher |
| Standardization | Bedrock-specific | Universal |
| Best for | Bedrock-centric teams | Multi-client ecosystems |

**Decision rule:** If you have ONLY Bedrock clients → use Lambda directly. If you have multiple AI clients → consider MCP.

**Visual Description:**
Decision tree diagram. Root: "How many AI clients need these tools?" → One (Bedrock only) → Direct Lambda → "Simpler, faster, cheaper". → Multiple clients → "Consider MCP" → Evaluate complexity/latency tradeoff → MCP Server.

**Speaker Notes:**
Don't over-engineer. I see teams reaching for MCP when they have a single Bedrock agent. That's solving a problem they don't have while introducing complexity they don't need. The right question is: who else will need these tools? If the answer is "only our Bedrock agent," use Lambda directly. If the answer is "our internal Bedrock agent, a Claude Desktop for our developers, and possibly a future customer-facing chat application," start thinking about MCP architecture now.

---

# SECTION 8: MODULE 7 SLIDES — PRODUCTIONIZING

---

## SLIDE 30 — The Demo Gap

**Title:** The Demo Gap Is Real and It Is Wide

**Content:**
Demo environment:
→ Controlled inputs
→ Dependencies always available
→ Single user
→ You're watching

Production environment:
→ Real user inputs (surprising)
→ Dependencies fail
→ Concurrent users
→ Nobody's watching

The gap is widest for agentic systems because non-determinism compounds across all these factors simultaneously.

**Visual Description:**
Chasm visualization. Left cliff labeled "Demo" with a cheerful character. Right cliff labeled "Production" — wider, more distant. The gap labeled "THE DEMO GAP." On the demo cliff: controlled scenario checkboxes. On the production cliff: real-world challenges (multiple users, cascading failures, unexpected inputs). Bridge between them labeled "Systematic Engineering" with five support pillars: Evaluation, Monitoring, Rate Limiting, Error Handling, Governance.

**Speaker Notes:**
Every healthcare AI deployment I've seen has encountered this gap. Every single one. The teams that cross it successfully are the ones who plan for it systematically: they build evaluation suites before deploying, not after. They configure monitoring before they go live, not when the first incident happens. They write the runbook before they need it. The teams that struggle are the ones who treat these as nice-to-haves that they'll get to "once the agent is stable." There is no stable without these foundations.

---

## SLIDE 31 — CI/CD for Agents

**Title:** The Agent CI/CD Pipeline

**Content:**
Stage 1: Static Validation (fast, deterministic)
→ Schema, IAM, Lambda tests

Stage 2: Integration Tests (real services, mock data)
→ Tool correctness, error paths

Stage 3: Agent Evaluation (non-deterministic)
→ 100+ scenarios, TCR, hallucination, latency

Stage 4: Human Review Gate ← Healthcare requirement
→ Clinical sign-off on sampled outputs

Stage 5: Staging Deployment + Canary

Stage 6: Production Promotion + Monitoring

**Visual Description:**
Horizontal pipeline diagram with six stages as connected blocks. Arrows between blocks. At Stage 4: prominent human icon with "GATE" flag — this stage requires human approval to proceed. Red X after Stage 3 and 4 with labels: "Rollback triggers." Terminal stage (Stage 6) shows: monitoring dashboard thumbnail + alarm bell.

**Speaker Notes:**
The human review gate — Stage 4 — is what makes this pipeline different from a normal software CI/CD pipeline. For software, you might not need human review between staging and production. For healthcare AI, you do. A clinical expert reviewing a sample of evaluation outputs is your last line of defense against clinical inaccuracies that your automated metrics didn't catch. Budget time for this. Budget the clinical reviewer's time. This is not a bottleneck — it is appropriate governance.

---

## SLIDE 32 — Observability Architecture

**Title:** Five Layers of Agent Observability

**Content:**
1. Business Metrics — Are users getting value?
2. Technical Performance — Is the system healthy?
3. Cost Monitoring — Is the system affordable?
4. Quality Metrics — Is the agent correct?
5. Security/Compliance — Is the system safe?

→ All five layers, all five environments, from day one

**Visual Description:**
Five horizontal layers like a monitoring stack. Each layer labeled and colored:
1. Business: Green (PA completions, briefs generated)
2. Technical: Blue (latency, error rate, throughput)
3. Cost: Yellow (cost per session, daily spend)
4. Quality: Purple (completion rate, human review score)
5. Security: Red (guardrail triggers, auth failures)

Each layer shows a sample CloudWatch metric name. Alarm bell icon on right of each layer.

**Speaker Notes:**
All five layers from day one. I want to emphasize this. It's tempting to start with just the technical performance layer — is the Lambda working? Is Bedrock responding? But in healthcare, you need quality metrics to catch clinical problems, cost metrics to catch runaway sessions, and security metrics to catch safety violations. The governance board and the compliance team will ask you for all five layers. Better to build them before deployment than scramble to add them after your first incident.

---

## SLIDE 33 — Responsible AI in Healthcare

**Title:** Responsible AI Is a Design Requirement, Not an Afterthought

**Content:**
Required governance elements:
□ AI Ethics Committee / governance process
□ Use case risk assessment (before building)
□ Model cards and transparency documentation
□ Human override at all consequential decision points
□ Incident response process
□ Audit trail for all agent actions (PHI access logging)
□ Defined accountability: who owns this system?

**Visual Description:**
Circular governance framework diagram. Center: "Healthcare AI System." Ring around it: eight governance elements as tiles, each with icon. Outside the ring: "Regulatory Context" notes (HIPAA, FDA SaMD, CMS). Arrows flowing from center outward showing "Agent Actions" and arrows flowing inward showing "Governance Controls."

**Speaker Notes:**
I want to end on this slide because it's where we need to start when we're building for healthcare. Every time you're about to make a design decision — how autonomous should this action be? how do we handle failures? who reviews the outputs? — ask yourself: is this the decision a responsible organization would make? The technical capability to do something autonomously does not mean the governance approval has been obtained for it. Build the governance structures. Involve compliance and legal from the beginning, not as an afterthought at the end.

---

## SLIDE 34 — Capstone Project Brief

**Title:** Week 12 Capstone: Build, Deploy, Defend

**Content:**
Requirements:
→ Working Bedrock agent with 2+ action groups
→ Knowledge base with real/synthetic documents
→ Evaluation report against defined metrics
→ Governance memo (risk, oversight, compliance)
→ 20-minute defended presentation

Healthcare domains:
Revenue cycle | Clinical decision support | Care coordination
Utilization management | Pharmacy | Quality reporting

**Visual Description:**
Presentation podium in center, surrounded by five components a student must present: Architecture diagram, Working demo, Metrics dashboard, Governance document, and Technical deep-dive section. A timeline to the right showing "Week 10: Architecture review," "Week 11: Final code freeze," "Week 12: Defense."

**Speaker Notes:**
The capstone is the proof point for everything we've covered. You choose the healthcare domain that's most relevant to your career goals. You design the architecture, implement it, evaluate it, and defend the design decisions. The "defend" part is important — you'll have experts in the room asking: why did you choose Claude 3 Sonnet over Haiku? Why this chunking strategy? What's your escalation policy? These are the questions you'll face in real enterprise deployments. Practice them here in a safe environment.

---

## SLIDE 35 — Final Slide: The Standard

**Title:** The Standard We Hold Ourselves To

**Content (quote):**
"Every technical decision in a healthcare AI system ultimately affects a patient somewhere. When you're uncertain about a design trade-off, ask: what happens to the patient if I'm wrong at scale? Let that question be your guide."

**Visual Description:**
Full-bleed background: a hospital corridor, slightly blurred. Centered text of the quote in large white type. Below: course name in smaller text. Small AWS Bedrock logo in lower right corner.

**Speaker Notes:**
This is the standard. Not the accuracy percentage. Not the latency SLA. Not the cost per session. All of those matter. But the deepest question for everyone in this room — every architecture decision, every governance call, every tradeoff discussion — is this one. In 12 weeks, you will have the technical skills to build production healthcare agents. The judgment to use those skills responsibly is the hardest thing to teach and the most important thing to earn. Welcome to the course.

---

*END OF POWERPOINT SLIDE DECK OUTLINE*

---

# ADDITIONAL SLIDE TOPICS BY MODULE

(Abbreviated outlines — expand as needed for each lecture)

## Module 2 Additional Slides:
- "The False Positive Trap" — clinical impact of high FP rate with calculation
- "Synthetic vs. Production Evaluation Data" — when synthetic misleads you
- "Designing for Low Hallucination" — architecture choices that reduce hallucination rate

## Module 3 Additional Slides:
- "Context Window Math" — running cost calculation exercise
- "State Machine Patterns" — from simple to complex state management
- "The Idempotency Requirement" — PA submission idempotency walk-through

## Module 4 Additional Slides:
- "Live Lab: IAM Role Creation" — screenshot-by-screenshot walkthrough
- "Live Lab: Action Group Schema" — writing and validating OpenAPI schema
- "Debugging Case Study" — real trace with identified failure and fix

## Module 5 Additional Slides:
- "Metadata Strategy for Multi-Topic KBs" — design exercise
- "Retrieval Evaluation Live Demo" — testing KB in console
- "KB Currency Pipeline" — document update governance

## Module 6 Additional Slides:
- "Writing Your First MCP Server" — live code walkthrough
- "MCP Security Architecture" — OAuth2 + Cognito design

## Module 7 Additional Slides:
- "Incident Post-Mortem Case Study" — fictional but realistic agent failure
- "Healthcare AI Regulatory Timeline" — FDA guidance evolution
- "Building the Governance Submission" — template walkthrough

---

*End of PowerPoint Slide Deck Outline*
