# CHECKPOINT QUIZZES — All Modules
## With Complete Answer Keys

---

# MODULE 1 QUIZ: Foundations of Agentic AI

**Instructions:** 10 questions. Mix of multiple choice, short answer, and applied reasoning. Time: 30 minutes.

---

**Q1. (Multiple Choice)** Which of the following is the most accurate description of the difference between a prompt chain and an agentic system?

A. A prompt chain uses multiple LLM models; an agent uses one model
B. A prompt chain has a developer-defined sequence of steps; an agent dynamically determines its next step based on reasoning
C. A prompt chain is faster; an agent is more accurate
D. A prompt chain requires no API calls; an agent requires many

---

**Q2. (Multiple Choice)** In the ReAct pattern, what does "Observe" mean?

A. The human reviews the agent's output
B. The agent runs a monitoring function
C. The agent reads the result of the tool it just called and incorporates it into the next reasoning step
D. The agent checks its internal state

---

**Q3. (Short Answer)** Name the six fundamental components of any agent system and provide a one-sentence description of each.

---

**Q4. (Multiple Choice)** A clinical documentation agent must process sensitive patient encounter transcripts. Which AWS service must be under a Business Associate Agreement (BAA) before deploying this agent on AWS?

A. AWS CloudFormation only
B. Amazon S3 only
C. Amazon Bedrock (and all services where PHI is processed or stored)
D. AWS Lambda only

---

**Q5. (Multiple Choice)** What is the primary reason data scientists struggle to transition to agentic AI system design compared to building traditional ML models?

A. Agents require more advanced Python skills
B. Agents require expensive GPU infrastructure
C. The shift from model-centric to system-centric thinking — evaluating and optimizing a distributed system with multiple interacting components, not a single function
D. Agents require knowledge of distributed databases

---

**Q6. (Applied Reasoning)** A hospital wants to build an agent to help nurses look up patient medication histories during a shift. The workflow is: (1) nurse asks about a patient, (2) agent retrieves medication history from EHR, (3) agent presents results. There are no variable steps — the agent always does exactly these three things in this order. Is this best implemented as an agent, a prompt chain, or a single LLM call? Justify your answer.

---

**Q7. (Multiple Choice)** In the prior authorization case study, the agent was designed to "initiate and complete the prior authorization process" autonomously. Which action type was explicitly excluded from autonomous execution?

A. Checking step therapy compliance
B. Submitting the PA request to the payer
C. Retrieving patient demographics
D. Looking up PA requirements

---

**Q8. (Architecture Debugging)** An agent for care coordination is returning empty responses to many queries. The trace shows the agent running 15 orchestration steps before stopping. What are the two most likely architectural failure modes, and how would you diagnose each?

---

**Q9. (Short Answer)** Explain the difference between "episodic memory" and "semantic memory" in an agent system. Provide a healthcare-specific example of each.

---

**Q10. (Multiple Choice)** For a patient triage agent that classifies patient severity into Low, Medium, and High categories, which failure mode is most safety-critical?

A. Over-triaging a low-severity case as medium
B. Under-triaging a high-severity case as medium or low
C. Returning results slightly too slowly
D. Generating a longer explanation than necessary

---

## MODULE 1 ANSWER KEY

**A1: B**
Explanation: The defining characteristic of an agent vs. a chain is dynamic step determination. In a prompt chain, the developer defines every step; in an agent, the LLM determines what to do next at each step.

**A2: C**
Explanation: "Observe" in ReAct refers to the agent reading the tool's output and using it in the next reasoning step. It is not human review or internal monitoring.

**A3:**
- Reasoning Engine (LLM): The language model that reads context and decides what to do next
- Tools: External functions the agent can invoke to act on the world
- Memory: Storage of information across steps (working memory) or sessions (long-term memory)
- Knowledge: Domain information the agent draws on — pre-trained, retrieved via RAG, or injected via system prompt
- Planning: The agent's ability to decompose a goal into steps and determine execution sequence
- State: The totality of information the agent holds about the current task and session at any moment

**A4: C**
Explanation: Any service where PHI is processed, stored, or transmitted must be under BAA. For a Bedrock-based agent processing patient transcripts, at minimum Amazon Bedrock is required. All other services in the PHI data path (Lambda, S3 for logs, CloudWatch for logs) also require BAA coverage.

**A5: C**
Explanation: Data scientists are trained to think about optimizing a single function (the model). Agentic systems require thinking about multiple interacting components, each of which can fail independently. This is a systems engineering mindset, not a model optimization mindset.

**A6:**
This is best implemented as a **prompt chain** (or possibly a single tool call pattern), not a full agent. The workflow is fixed: three predetermined steps in a fixed order. An agent would be over-engineered for this use case — it would add cost (multiple LLM reasoning steps), latency, and complexity without providing value, since there is no dynamic decision-making required. The correct implementation is: a Python function that (1) calls the EHR API, (2) passes the result to the LLM for formatting/summarization, and (3) returns the response.

**A7: B**
Explanation: In Case Study 4, PA submission required pharmacist review and explicit approval. All information gathering and PA package creation were autonomous, but the submission action itself required human authorization.

**A8:**
Failure Mode 1: **Context window overflow / reasoning degradation.** If each of the 15 steps adds 5-8K tokens to the context, the agent may be approaching or exceeding the model's effective reasoning capacity. Diagnosis: examine the trace and count total tokens consumed. If above ~100K tokens, context management is the issue. Fix: implement tool response truncation and context summarization.

Failure Mode 2: **Maximum orchestration steps limit reached.** Bedrock Agents has a configurable maximum steps limit. 15 steps may be the configured maximum. If the workflow genuinely requires more steps, the limit needs to be increased. If the workflow is looping (same tools called repeatedly), the agent is in a reasoning loop. Diagnosis: look at the trace — are tool calls repeating? Is the agent making progress toward the goal at each step?

**A9:**
- Episodic memory: Memory of what the agent has done or experienced. Healthcare example: A patient coaching agent that remembers that the patient declined to discuss weight management at the last session, so it approaches the topic differently this time.
- Semantic memory: Encoded knowledge about the world/domain. Healthcare example: A clinical decision support agent's knowledge base containing treatment guidelines — this is knowledge about medicine, not memory of specific interactions.

**A10: B**
Explanation: Under-triaging a high-severity case is safety-critical because it could result in a patient with a life-threatening condition being placed in a lower-priority queue, delaying treatment. Over-triaging (classifying low-acuity as higher) creates inefficiency but not direct patient harm. This is the key asymmetry in clinical triage AI: errors in one direction are catastrophically worse than errors in the other.

---

# MODULE 2 QUIZ: Defining Agent Goals and Success Metrics

**Q1. (Multiple Choice)** Your claims validation agent achieves a 96% error detection rate but generates false positives (incorrectly flagging clean claims) 40% of the time. A billing department processes 1,000 claims per day. How many clean claims are being incorrectly flagged daily?

A. 40
B. 400
C. 960
D. Cannot be calculated from this information

---

**Q2. (Multiple Choice)** In LLM-as-judge evaluation, which of the following is a well-documented systematic problem?

A. LLM judges cannot evaluate code quality
B. LLM judges from the same model family as the agent under evaluation tend to rate outputs more leniently
C. LLM judges run too slowly for production evaluation
D. LLM judges require access to clinical expertise

---

**Q3. (Short Answer)** Define "hallucination rate" in the context of a healthcare agent. Why is measuring it particularly difficult?

---

**Q4. (Multiple Choice)** For a patient triage agent, which metric is most critical to monitor as a SAFETY constraint rather than a performance target?

A. Over-triage rate
B. Latency p95
C. Under-triage rate
D. Cost per session

---

**Q5. (Applied Reasoning)** A product manager says: "Our PA agent has a 4.8/5 LLM-judge score on factual grounding, which is excellent. We don't need human review." Identify at least three specific failure modes that LLM-as-judge would NOT detect in a healthcare PA context.

---

**Q6. (Multiple Choice)** In the multi-objective framework, what is the difference between a "secondary objective" and a "constraint"?

A. Secondary objectives are more important than constraints
B. Constraints are hard limits — violation means failure regardless of other metrics. Secondary objectives are optimized but can be traded off within limits.
C. Constraints are soft targets; secondary objectives are hard targets
D. There is no meaningful distinction

---

**Q7. (Short Answer)** Describe the structure of a complete evaluation scenario for a synthetic test set (include all required fields as described in the module).

---

**Q8. (Architecture Debugging)** Your evaluation pipeline shows task completion rate of 93% and tool correctness rate of 99%, but your human reviewers are finding a 15% rate of clinically inaccurate outputs. These numbers seem inconsistent. Explain how all three numbers could be simultaneously accurate.

---

**Q9. (Multiple Choice)** Which evaluation method is most appropriate for detecting prompt injection attacks against a healthcare agent?

A. LLM-as-judge
B. Human review of sampled outputs
C. Adversarial evaluation set with known injection patterns
D. Latency monitoring

---

**Q10. (Multiple Choice)** A research summarization agent's RAG performance is measured as: "Total performance = KB retrieval quality × LLM synthesis quality." If KB retrieval quality = 0.7 and LLM synthesis quality = 0.9, what is total performance? If you could only improve one factor to 1.0 (perfect), which improvement has greater absolute impact?

A. 0.63 total; improving LLM quality has greater impact
B. 0.63 total; improving KB quality has greater impact
C. 1.6 total; both have equal impact
D. 0.79 total; improving KB quality has greater impact

---

## MODULE 2 ANSWER KEY

**A1: B**
Calculation: 1,000 claims/day × 40% false positive rate = 400 clean claims incorrectly flagged. These 400 claims require staff time to review and clear — significant operational burden.

**A2: B**
Explanation: Same-family model bias (leniency bias) is well-documented. When you use Claude 3 Opus to judge Claude 3 Sonnet's outputs, the judge tends to rate them more highly than human reviewers would. Always calibrate LLM judges against human review samples.

**A3:**
Hallucination rate = the percentage of agent outputs that contain factual claims not supported by information retrieved from tools or knowledge bases. It is difficult to measure because: (1) you need ground truth to compare against (requires human review of each claim); (2) some hallucinations are subtle — plausible-sounding but wrong details that only an expert would catch; (3) at scale, human review of every output is infeasible; (4) automated checking requires structured claim extraction, which is itself an imperfect process; (5) the same factual error may appear in some sessions but not others due to non-determinism.

**A4: C**
Explanation: Under-triage rate is a SAFETY constraint (hard limit — should be < 0.5%), not a performance target. Over-triage rate is a secondary performance metric. Latency and cost are important but not safety constraints.

**A5:**
Three failure modes LLM-as-judge would miss in PA context:
1. **Numerical accuracy in retrieved clinical values:** If the agent correctly retrieves a lab value but transcribes it wrong (e.g., CRP = 12 mg/L written as 1.2 mg/L), the judge sees that the agent mentioned the CRP test and rates grounding highly without checking the number.
2. **Payer policy currency:** The agent may cite an outdated payer policy from the knowledge base. The judge cannot verify whether the retrieved policy is current.
3. **Step therapy requirement completeness:** The agent may correctly document one of three required prior medication trials but miss the others. The judge sees that step therapy was discussed and rates favorably.

**A6: B**
Explanation: Constraints are non-negotiable. A safety constraint like "no PHI exposure" means the system fails if that constraint is violated, regardless of how well it performs on other metrics. Secondary objectives like "minimize cost per session" are optimized but may be traded off against each other.

**A7:**
Complete evaluation scenario fields:
- scenario_id (unique identifier)
- scenario_type (happy_path, edge_case, adversarial, error_condition)
- description
- input (user query)
- expected_tool_sequence (ordered list of expected tools and parameters)
- acceptable_tool_order_variations
- expected_output_characteristics (what must be present, absent, accurate)
- evaluation_metrics (which metrics to measure for this scenario)

**A8:**
These numbers are consistent. Here's how:
- 93% task completion: The agent produces a complete output 93% of the time. 7% of sessions time out or produce incomplete outputs.
- 99% tool correctness: Of the tool calls the agent makes, 99% call the right tool with the right parameters.
- 15% clinical inaccuracy: The agent correctly selects and calls tools, but the information retrieved from the EHR may be correct while the SYNTHESIS of that information in the PA draft is clinically inaccurate. Tool correctness measures tool selection and parameter accuracy — it does not measure whether the agent correctly interprets or synthesizes the tool results. A clinically inaccurate PA package that was assembled from correctly-retrieved data reflects a reasoning or synthesis failure, not a tool-calling failure.

**A9: C**
Explanation: Adversarial evaluation sets with known injection patterns are the systematic way to test prompt injection resistance. Human review might catch some, but cannot scale to test all injection patterns. LLM-as-judge is unreliable for security testing (may be manipulated itself). Latency monitoring doesn't detect injection attempts.

**A10: B**
Total: 0.7 × 0.9 = 0.63. Improving KB from 0.7 to 1.0 → 1.0 × 0.9 = 0.90 (improvement of +0.27). Improving LLM from 0.9 to 1.0 → 0.7 × 1.0 = 0.70 (improvement of +0.07). KB quality improvement has greater absolute impact.

---

# MODULE 3 QUIZ: Agent System Architecture

**Q1. (Multiple Choice)** In the agent loop, what is the purpose of the "context assembly" step that occurs before the first LLM call?

A. To compress the conversation history
B. To combine the system prompt, tool definitions, conversation history, and user input into a single context window for the LLM
C. To authenticate the user's identity
D. To select which tool the agent should call first

---

**Q2. (Short Answer)** Explain why a tool that creates records (e.g., submits a PA request) should be idempotent. What could go wrong if it is not?

---

**Q3. (Multiple Choice)** Which state management pattern is appropriate for an agent that needs to resume an interrupted PA workflow three hours after it started?

A. In-context memory only
B. Session attributes (Bedrock built-in)
C. External state persistence (DynamoDB with workflow_id key)
D. No state is needed — restart the workflow

---

**Q4. (Applied Reasoning)** A production agent's Lambda tools are structured to return raw Python exceptions when an error occurs. Why is this architecturally wrong? What should they return instead?

---

**Q5. (Multiple Choice)** In a Plan-then-Execute agent, step 3 of the plan discovers that step 4 is now incorrect given new information. What happens?

A. The agent replans from step 4 onward
B. The agent stops and asks the user what to do
C. The agent executes step 4 as planned, regardless
D. The agent rolls back to step 1

---

**Q6. (Short Answer)** Name three CloudWatch metrics you would implement for a healthcare agent, explain what each measures, and explain what an alarm on each would indicate.

---

**Q7. (Multiple Choice)** What is the "confused deputy problem" in the context of the Bedrock agent IAM configuration, and how does the `ConditionExpression` in the Lambda resource policy address it?

A. It prevents the Lambda from calling other AWS services without permission; solved by least-privilege IAM
B. It is a risk where a privileged service (Bedrock) is tricked into performing actions on behalf of an unauthorized caller; addressed by requiring source-account and source-arn conditions on the resource policy
C. It is a naming conflict between agent action groups; solved by unique naming conventions
D. It prevents Lambda timeouts; solved by increasing timeout configuration

---

**Q8. (Architecture Debugging)** An agent for care coordination successfully completes 95% of sessions but has unacceptably high costs: $4.20 per session vs. a $0.75 budget. The agent uses Claude 3 Opus and a knowledge base with 200 documents. What are three specific, actionable architectural changes you would investigate first?

---

**Q9. (Multiple Choice)** In the state machine for a PA workflow, which transition is likely illegal?

A. INITIATED → PATIENT_RETRIEVED
B. DOCUMENTATION_GATHERED → DRAFT_CREATED
C. SUBMITTED → INITIATED
D. PENDING_REVIEW → SUBMITTED

---

**Q10. (Short Answer)** What is the difference between Bedrock Agent "traces" and Lambda CloudWatch logs? What does each one capture that the other does not?

---

## MODULE 3 ANSWER KEY

**A1: B**
Explanation: Context assembly is the pre-processing step where all relevant information — system prompt, tool definitions (JSON schemas), conversation history, and current user input — is assembled into the full prompt that will be sent to the LLM.

**A2:**
An idempotent tool produces the same result when called multiple times with the same parameters. PA submission tools must be idempotent because: (1) agent reasoning loops can cause the same tool to be called multiple times; (2) network errors may cause the caller to retry; (3) if the submission tool is not idempotent, each retry submits a duplicate PA request, potentially causing duplicate approvals, billing errors, duplicate claims to payers, and workflow chaos. Implementation: check if a PA for this patient/medication/date already exists before submitting, and return the existing record rather than creating a duplicate.

**A3: C**
Explanation: Session attributes (Bedrock built-in) only persist within an active session. After 3 hours, the session has likely expired. For cross-session persistence, external state management (DynamoDB) with a workflow_id is required. In-context memory doesn't persist between sessions.

**A4:**
Raw Python exceptions are architecturally wrong because the LLM reads tool responses as text and must interpret them. A stack trace like `AttributeError: 'NoneType' object has no attribute 'insurance_id' at line 45 of ehr_client.py` provides no actionable information for the agent. The agent cannot reason about what this means or how to handle it. The correct pattern is a structured error response: `{"status": "error", "error_code": "PATIENT_NOT_FOUND", "error_message": "No patient found with identifier MRN-12345. Please verify the patient ID.", "data": null}`. This gives the agent: the failure type, the reason, and a suggested remediation — information it can reason about.

**A5: C**
Explanation: In Plan-then-Execute, the plan is fixed after the planning phase. The agent executes each step in sequence regardless of what each step reveals. This is the fundamental limitation of Plan-then-Execute and the reason ReAct (iterative planning) is preferred for healthcare use cases where unexpected findings are common.

**A6:**
Example answers (multiple valid options):
1. **PAWorkflowDuration (Seconds):** Measures total time from session initiation to completion. Alarm if p95 > 120 seconds → indicates performance degradation (slow EHR API, high LLM latency, or excessive loop iterations).
2. **ToolCallErrors (Count):** Measures Lambda function errors per 5-minute window. Alarm if > 5 errors in 5 minutes → indicates tool integration failures (API down, permissions issue, data quality problem).
3. **HumanEscalationRate (Count):** Measures how often the agent routes to human review. Alarm if > 15% of sessions → indicates the agent is encountering cases it cannot handle, possibly due to gaps in knowledge base, missing tools, or changing input distribution.

**A7: B**
Explanation: The confused deputy problem occurs when a service with broad privileges (like Bedrock, which can invoke many Lambda functions) is tricked by a malicious actor into invoking resources on their behalf. By adding `StringEquals: aws:SourceAccount: YOUR_ACCOUNT` and `ArnLike: aws:SourceArn: arn:aws:bedrock:...:agent/*` conditions, the Lambda resource policy ensures only Bedrock agents in your specific account can invoke the function — not any Bedrock service call originating from any account.

**A8:**
Three actionable changes:
1. **Downgrade from Claude 3 Opus to Claude 3 Sonnet:** Claude 3 Opus is 5-10x more expensive than Sonnet. For most care coordination queries, Sonnet provides sufficient quality. Estimated cost reduction: ~70-80% of LLM cost.
2. **Reduce system prompt token count:** Every LLM call includes the full system prompt. A 10,000-token system prompt adds significant cost on each of 7+ iterations. Trim system prompt to essential instructions only. Every 1,000 tokens removed from the system prompt saves tokens × (LLM input price / 1000) × iteration_count per session.
3. **Implement tool response truncation:** If EHR tools return complete patient records (5,000+ tokens) but the agent only needs 500 tokens of relevant information, implement server-side filtering to return only the requested fields. This reduces context growth per iteration significantly.

**A9: C**
Explanation: `SUBMITTED → INITIATED` is an illegal backward transition. A submitted PA should transition to APPROVED, DENIED, or APPEALING — not back to the beginning. The state machine must enforce that states progress forward through the workflow (with specific exception paths for error/failure states).

**A10:**
Bedrock Agent traces capture: the LLM's reasoning (rationale text), the agent's action decisions (which tool to call), the tool parameters the LLM generated, and the high-level orchestration flow — all from the agent's perspective.

Lambda CloudWatch logs capture: the actual execution inside the Lambda function — specifically, what happened when the tool code ran, including: function start/end, external API call timing, data processing steps, errors with stack traces, and any custom log statements. The trace shows what Bedrock decided; CloudWatch shows what the Lambda code did.

Together: trace for debugging agent reasoning; CloudWatch for debugging tool execution.

---

# MODULE 4 QUIZ: Amazon Bedrock Deep Dive

**Q1. (Multiple Choice)** After creating a Bedrock Agent, what must you do before you can test it in the console?

A. Enable CloudWatch logging
B. Create an alias
C. Prepare the agent
D. Upload a test file

---

**Q2. (Screenshot Interpretation)** You are looking at a Bedrock Agent trace and see the following in Step 3:

```
Action invocation:
  Action group: PatientDataGroup
  API path: /get-patient-coverage
  Parameters: [{name: "patient_id", value: "John Smith"}]

Observation:
  {"status": "error", "error_code": "INVALID_MRN_FORMAT",
   "error_message": "Invalid MRN format: John Smith. Expected: MRN-XXXXXXXX"}
```

What happened and how would you fix it?

---

**Q3. (Multiple Choice)** In a Bedrock Action Group backed by Lambda, when the LLM makes a tool call, who ultimately makes the decision to invoke Lambda?

A. The user
B. The Bedrock Orchestrator
C. The Lambda function itself
D. The IAM role

---

**Q4. (Short Answer)** Explain the difference between a Bedrock Agent "version" and a "alias." How would you use these to safely deploy a change to a production agent?

---

**Q5. (Multiple Choice)** Your Lambda tool is returning this error:

```
{"errorType": "AccessDeniedException",
 "errorMessage": "User: arn:aws:sts::123456789:assumed-role/BedrockAgentRole/...
  is not authorized to perform: lambda:InvokeFunction on resource:
  arn:aws:lambda:us-east-1:123456789:function:healthcare-pa-tools"}
```

What are the two things you need to check/fix?

A. Increase Lambda timeout and add more memory
B. Check that BedrockAgentRole has lambda:InvokeFunction in its IAM policy, AND check that the Lambda function has a resource-based policy allowing bedrock.amazonaws.com invocation
C. Redeploy the Lambda function and recreate the agent
D. Add the Lambda function ARN to the Bedrock model access list

---

**Q6. (Multiple Choice)** Why should production application code always call a Bedrock Agent alias rather than the agent's version or DRAFT directly?

A. Aliases are faster than direct version calls
B. Aliases allow traffic to be routed to a specific version, enabling instant rollback by updating the alias without changing application code
C. DRAFT versions are not accessible via API
D. Aliases provide additional IAM security

---

**Q7. (Applied Reasoning)** Write the complete IAM trust relationship policy that allows Amazon Bedrock to assume a role for a specific agent (your account ID is 123456789012, agent ID is ABCDEFGHIJ). Explain why each condition is necessary.

---

**Q8. (Multiple Choice)** A Bedrock Agent trace shows "Rationale: I need to check the formulary." followed by the agent calling `get_patient_demographics`. What is this an example of?

A. A context window overflow
B. A tool description mismatch — the formulary check tool's description didn't match the agent's phrasing and it selected the wrong tool
C. Correct behavior — checking demographics before formulary
D. A Lambda invocation error

---

**Q9. (Short Answer)** In the Bedrock Action Group OpenAPI schema, what is the purpose of the `description` field at the operation level, and what is the consequence of leaving it blank or writing a vague description?

---

**Q10. (Multiple Choice)** Which Bedrock component provides automatic content filtering for a deployed agent, including blocking specific topics and redacting PII from outputs?

A. Lambda environment variables
B. IAM policies
C. Amazon Bedrock Guardrails
D. CloudWatch Alarms

---

## MODULE 4 ANSWER KEY

**A1: C**
Explanation: After creation, an agent is in "NOT_PREPARED" status. You must click "Prepare" which compiles the agent configuration into an executable form. Only PREPARED agents can be tested or invoked.

**A2:**
What happened: The LLM extracted the patient identifier as "John Smith" (the patient's name) rather than their MRN. The user probably phrased their query with the patient's name, and the agent couldn't correctly identify which parameter to use. The tool correctly rejected this input with a structured error.

How to fix: (1) Improve the tool description to be more explicit: "Requires the patient's Medical Record Number (MRN), not their name. Format: MRN-XXXXXXXX. If you only have the patient's name, use the search_patient_by_name tool first." (2) Add a `search_patient_by_name` tool that accepts a name and returns the MRN. (3) Update the system prompt to clarify that all patient references should be by MRN, and that the agent should retrieve the MRN before calling clinical tools.

**A3: B**
Explanation: The Bedrock Orchestrator parses the LLM's tool call response, routes it to the correct action group, and invokes Lambda. The LLM decides WHAT to call; the Orchestrator performs the actual invocation.

**A4:**
A version is an immutable snapshot of the agent's configuration at a specific point in time. Once created, a version cannot be changed.

An alias is a named pointer (like a pointer in a programming language) that references a specific version. The alias can be updated to point to a different version at any time.

Safe deployment process: (1) Edit the agent in DRAFT and test thoroughly. (2) Create a new version (snapshot the DRAFT). (3) Update the "production" alias to point to the new version. Application code always calls the "production" alias. If the new version has issues, update the alias back to the previous version — instant rollback without any code deployment.

**A5: B**
Explanation: AccessDeniedException for lambda:InvokeFunction means either: (a) BedrockAgentRole lacks the lambda:InvokeFunction permission for this function ARN in its identity-based policy, OR (b) the Lambda function itself lacks a resource-based policy granting bedrock.amazonaws.com the right to invoke it. Both conditions must be satisfied: the caller needs permission to call AND the resource must allow being called.

**A6: B**
Explanation: Aliases decouple application code from specific versions. Application code calls "production" alias. When you deploy v2, you update the alias — no application code changes required. Instant rollback = update alias back to v1. DRAFT is accessible via API but should never be used in production because it changes every time you edit the agent.

**A7:**
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
          "aws:SourceAccount": "123456789012"
        },
        "ArnLike": {
          "aws:SourceArn": "arn:aws:bedrock:us-east-1:123456789012:agent/ABCDEFGHIJ"
        }
      }
    }
  ]
}
```

Why each condition:
- `StringEquals: aws:SourceAccount`: Ensures only Bedrock service calls originating from your account can assume this role. Prevents cross-account confused deputy attacks.
- `ArnLike: aws:SourceArn`: Ensures only your specific agent (not any Bedrock agent in your account, and not Bedrock calls for other purposes) can assume this role. Provides principle of least privilege at the agent level.

**A8: B**
Explanation: The agent correctly identified that it needs to check the formulary, but then called the demographics tool instead of the formulary tool. This is tool description mismatch — the description of the formulary tool doesn't clearly match the agent's current reasoning. The agent found demographics as the closest match. Fix: improve the formulary tool description to explicitly mention keywords the agent would use when reasoning about formulary checks.

**A9:**
The `description` field at the operation level is read by the LLM to determine when and whether to use this tool. It is functionally equivalent to code documentation — except that a human reads regular documentation while the LLM reads the operation description to make tool selection decisions.

If blank or vague: The agent cannot reliably determine when to use the tool. It may (a) never use it because it doesn't match any query it receives, (b) over-use it on queries it shouldn't answer, or (c) use the wrong tool entirely. In practice, vague tool descriptions are the single most common cause of poor agent performance in production Bedrock deployments.

**A10: C**
Explanation: Amazon Bedrock Guardrails is a dedicated safety service that can be attached to agents. It provides content filtering (harm categories), topic denial lists, sensitive information redaction, and grounding checks. IAM policies control access but not content. Lambda environment variables are just configuration. CloudWatch Alarms monitor metrics but don't filter content.

---

# MODULE 5 QUIZ: Knowledge Bases

**Q1. (Multiple Choice)** What is the primary architectural advantage of RAG over relying on an LLM's pre-trained knowledge for clinical information?

A. RAG is faster than model recall
B. RAG allows retrieval of current, organization-specific, auditable information that was not in the model's training data
C. RAG is less expensive than model inference
D. RAG eliminates hallucinations completely

---

**Q2. (Short Answer)** Define "chunk overlap" in the context of knowledge base chunking strategy. What problem does it solve?

---

**Q3. (Multiple Choice)** You are building a knowledge base containing clinical guidelines for cardiology, pulmonology, and endocrinology. A query about beta-blocker use in heart failure patients should retrieve cardiology guidelines, not pulmonology or endocrinology documents. What KB feature enables this?

A. Semantic search
B. Keyword matching
C. Metadata filtering
D. Hybrid retrieval

---

**Q4. (Screenshot Interpretation)** During a knowledge base sync, you see the following status: "125 documents processed successfully, 8 documents failed." What are the three most likely causes of the 8 failures, and how would you investigate each?

---

**Q5. (Multiple Choice)** "What Happens When You Click Sync" in Bedrock Knowledge Bases includes embedding generation. Which model performs this embedding for a standard Bedrock KB configuration?

A. The same foundation model as the agent
B. Claude 3 Haiku
C. Amazon Titan Embeddings Text V2
D. OpenSearch Serverless

---

**Q6. (Applied Reasoning)** A physician asks the clinical guidelines agent: "What is the standard of care for newly diagnosed metastatic pancreatic adenocarcinoma?" The agent confidently responds with a detailed treatment protocol, but you know this specific rare condition is NOT in your knowledge base. What should have happened instead? What design change would produce the correct behavior?

---

**Q7. (Multiple Choice)** For clinical formulary data stored as CSV files in an S3 knowledge base, which chunking strategy is most appropriate?

A. Hierarchical (large parent / small child chunks)
B. Fixed size (256 tokens)
C. Semantic (NLP-based boundaries)
D. No chunking (each file is one chunk)

---

**Q8. (Short Answer)** Explain the difference between knowledge base "precision" and "recall" in the retrieval context. Give an example of a system with high recall but low precision in a healthcare knowledge base.

---

**Q9. (Multiple Choice)** The organization's compliance team asks: "Can patient records be stored in the knowledge base?" What is the correct answer?

A. Yes, with patient consent
B. Yes, if encrypted
C. No — knowledge bases are for reference information (guidelines, policies, protocols). PHI should be accessed through tools that query authorized EHR systems with proper access controls and audit logging.
D. Yes, if the knowledge base is in a private VPC

---

**Q10. (Multiple Choice)** Which combination of embedding dimensions and number of results would provide the best retrieval accuracy for clinical guidelines?

A. 256 dimensions, top 3 results
B. 1024 dimensions, top 5 results
C. 512 dimensions, top 1 result
D. 256 dimensions, top 10 results

---

## MODULE 5 ANSWER KEY

**A1: B**
Explanation: LLM pre-trained knowledge has three problems: it has a training cutoff, it isn't organization-specific, and it cannot be audited (you can't cite where the model learned something). RAG solves all three: you control the corpus, can update it, and can cite specific source documents.

**A2:**
Chunk overlap is when consecutive chunks share a portion of text. For example, with 512-token chunks and 100-token overlap: Chunk 1 = tokens 1-512, Chunk 2 = tokens 413-924 (overlap on tokens 413-512). Overlap solves the "boundary problem": relevant information often spans a chunk boundary. Without overlap, a clinical recommendation described across the end of one chunk and the beginning of the next might not be fully retrieved. Overlap ensures that the key context at any boundary is present in both adjacent chunks.

**A3: C**
Explanation: Metadata filtering uses document-level metadata (tags) to restrict retrieval to specific subsets of the corpus. If each cardiology document has metadata tag `specialty: cardiology`, a query can specify `filter: specialty = cardiology` to retrieve only from that subset.

**A4:**
Three likely causes and investigation approaches:
1. **Unsupported format / corrupt file:** The document parser couldn't read the file (damaged PDF, password-protected document, unsupported format). Investigation: Check the KB sync error log (available in the data source detail page after sync). Filter for 400-level errors.
2. **File too large:** Individual documents exceeding Bedrock's size limits (typically tens of MB). Investigation: Check file sizes in S3 for the 8 failing documents.
3. **Text extraction failure (complex PDF):** PDFs with scanned images (no text layer), complex tables, or unusual encoding. Investigation: Open the failing documents and check if text is selectable. Attempt to extract text with a local PDF parser. Preprocess with AWS Textract for image-heavy PDFs.

**A5: C**
Explanation: Amazon Titan Embeddings Text V2 is the standard embedding model used by Bedrock Knowledge Bases. It converts text chunks into vector representations. This is separate from the foundation model used for the agent itself.

**A6:**
What should have happened: The agent should have queried the knowledge base, found no relevant documents, and responded: "I couldn't find specific guidelines for this condition in my clinical guidelines library. For rare conditions like metastatic pancreatic adenocarcinoma, please consult the NCCN guidelines directly or refer to a specialist."

The problem: The agent answered from pre-trained model knowledge rather than from retrieved knowledge. This is a grounding failure.

Design change: (1) Enable and configure Bedrock Guardrails grounding check — set grounding threshold to require responses to be supported by retrieved context. (2) Add to system prompt: "When you cannot find information in the knowledge base to support an answer, explicitly state that you don't have guidelines for this condition and direct the user to appropriate external resources. NEVER provide clinical recommendations from general knowledge that you cannot cite from the knowledge base." (3) Set the knowledge base retrieval to always retrieve (not optionally retrieve) when clinical information is requested.

**A7: B**
Explanation: CSV formulary data typically has short, structured rows. Fixed-size small chunks (256 tokens) capture individual drugs or small groups without mixing unrelated drugs in the same chunk, enabling precise retrieval. Hierarchical is overkill for tabular data. Semantic may struggle with repetitive CSV structure.

**A8:**
Precision: of the N chunks retrieved, what fraction are actually relevant to the query? High precision = mostly relevant results returned.

Recall: of all chunks in the knowledge base that ARE relevant to the query, what fraction were actually retrieved? High recall = few relevant chunks missed.

High recall / low precision example: A query about "beta blocker contraindications in heart failure" retrieves 5 results: 3 are directly relevant (high recall on those), but also retrieves 2 chunks about beta blockers in hypertension and 1 about heart failure medications generally. 3/6 precision = 50%. All 3 relevant chunks retrieved = 100% recall (if those 3 were all that were relevant). The low precision means the agent's context is polluted with semi-relevant content.

**A9: C**
Explanation: Knowledge bases are designed for reference information — static documents that ground agent responses. Patient records are dynamic, access-controlled PHI that must be accessed through EHR integrations with proper authentication, authorization, and audit logging. Mixing them would create compliance, access control, and governance problems.

**A10: B**
Explanation: 1024 dimensions provides the highest embedding quality (best semantic representation). Top 5 results provides enough context for the agent without overwhelming it. 256 dimensions sacrifices accuracy for cost. Retrieving only 1 result risks missing relevant context. 10 results with 256 dimensions provides too much potentially irrelevant content.

---

# MODULE 6 QUIZ: MCP Servers

**Q1. (Multiple Choice)** MCP uses which wire protocol for message formatting?

A. REST/JSON
B. gRPC
C. JSON-RPC 2.0
D. SOAP/XML

---

**Q2. (Short Answer)** Name three capabilities that MCP servers can expose to MCP clients, and describe a healthcare use case for each.

---

**Q3. (Multiple Choice)** You are building an AI ecosystem where multiple client applications (Bedrock agent, Claude Desktop, a React web app with AI capabilities) all need access to the same EHR query functions. Which integration pattern is most appropriate?

A. Direct Lambda for each client separately
B. MCP server, implemented once and called by all clients
C. API Gateway with one endpoint per client
D. Separate agent per client

---

**Q4. (Applied Reasoning)** Compared to a Bedrock Action Group backed by Lambda, what is the network path when an MCP server handles a tool call from a Bedrock agent? How many additional network hops does this create, and what is the latency implication?

---

**Q5. (Multiple Choice)** In a healthcare MCP server deployment, which authentication mechanism is most appropriate for enterprise clinical applications?

A. No authentication (internal network only)
B. API key in request header
C. OAuth2 with Cognito, using scope-based authorization per tool type
D. IP allowlisting

---

**Q6. (Multiple Choice)** An organization has Bedrock Agents as its ONLY AI client. There are no other AI applications or developers outside the organization. What is the best argument AGAINST implementing MCP servers in this scenario?

A. MCP is not compatible with Bedrock
B. MCP adds deployment complexity, authentication overhead, and latency without providing value since there is no multi-client need
C. MCP doesn't support healthcare data
D. MCP is too expensive

---

**Q7. (Short Answer)** Describe the MCP tool initialization sequence. What happens between when a client connects and when it makes its first tool call?

---

**Q8. (Multiple Choice)** Which transport mechanism is appropriate for an MCP server deployed as a shared enterprise service accessed by multiple remote clients?

A. stdio (standard input/output)
B. HTTP with Server-Sent Events (SSE) or WebSocket
C. TCP direct socket
D. UNIX domain socket

---

## MODULE 6 ANSWER KEY

**A1: C**
Explanation: MCP uses JSON-RPC 2.0 as its message format. This provides a standardized request/response structure with IDs for correlation, error codes, and method names.

**A2:**
Three MCP capabilities with healthcare use cases:
1. **Tools:** Executable functions the AI can call. Healthcare example: An EHR query tool that lets any MCP client retrieve patient demographics, labs, or medications by invoking the organization's FHIR API.
2. **Resources:** Data sources the AI can read (files, database records, URLs). Healthcare example: A clinical guidelines resource that exposes the organization's approved protocol documents as readable resources, allowing AI applications to load specific guidelines on demand.
3. **Prompts:** Pre-written prompt templates the AI can use. Healthcare example: A PA support prompt template that structures the AI's approach to prior authorization workflows, ensuring consistent framing across different AI applications.

**A3: B**
Explanation: When multiple AI clients need the same functions, implementing them once as an MCP server and having all clients connect to it eliminates duplicate implementation and ensures consistency. Direct Lambda per client creates N copies of the same code with N maintenance burdens. API Gateway with one endpoint per client doesn't standardize the tool interface.

**A4:**
Direct Lambda: Bedrock → Lambda (one hop, within AWS region, typically 10-50ms)
MCP server: Bedrock → API Gateway → ECS/Lambda (MCP server) → backend Lambda → result → back through MCP server → API Gateway → Bedrock

Additional hops: 2-3 additional network hops.
Latency implication: Roughly 50-150ms additional overhead per tool call for intra-AWS calls; potentially 100-300ms if the MCP server is in a different region or external network.

At 8 tool calls per session, this adds 400-1,200ms total session overhead. For a PA workflow where total target is 30 seconds, this is 1.3-4% overhead — manageable if the multi-client benefits justify it.

**A5: C**
Explanation: OAuth2 with Cognito provides: (1) identity verification of each client, (2) token-based authentication (not static API keys), (3) scope-based authorization (read-only clients can't call write tools), (4) token expiration and rotation, (5) revocation capability. IP allowlisting is too coarse and doesn't identify individual clients. API keys are static and difficult to rotate. No authentication is never appropriate for PHI access.

**A6: B**
Explanation: MCP provides value primarily when multiple clients need the same tools. In a Bedrock-only environment, adding MCP introduces additional infrastructure (ECS service or Lambda for MCP server), authentication management, additional network latency, and operational complexity — without the cross-client standardization benefit that justifies these costs.

**A7:**
MCP initialization sequence:
1. Client connects to server (stdio or HTTP)
2. Client sends `initialize` request with client capabilities and protocol version
3. Server responds with `initialize` result including server capabilities and supported protocol version
4. Client sends `initialized` notification (acknowledging the exchange)
5. Client sends `tools/list` request to discover available tools
6. Server responds with array of Tool objects (name, description, inputSchema for each)
7. Client caches the tool list
8. Client is now ready to make tool calls

**A8: B**
Explanation: stdio is only appropriate for local processes on the same machine (developer tools like Claude Desktop). For enterprise shared services accessed by remote clients, HTTP with SSE or WebSocket transport is required — it supports multiple simultaneous clients, works across network boundaries, and can be secured with standard HTTPS controls.

---

# MODULE 7 QUIZ: Productionizing Agent Systems

**Q1. (Multiple Choice)** In a CI/CD pipeline for a Bedrock Agent, what is the purpose of the "human review gate" stage?

A. To test Lambda function performance
B. To have a clinical or domain expert review sampled evaluation outputs and provide sign-off before production deployment
C. To manually approve AWS costs
D. To verify CloudWatch alarms are configured

---

**Q2. (Short Answer)** Name the five AWS observability layers described in Module 7 and identify the primary data source for each.

---

**Q3. (Multiple Choice)** A production PA agent session generates 250,000 input tokens across 10 LLM calls. Using Claude 3 Sonnet pricing of $0.003/1K input tokens, what is the LLM input token cost for this single session?

A. $0.75
B. $7.50
C. $0.075
D. $3.00

---

**Q4. (Applied Reasoning)** Define the three tiers of the human override architecture described in Module 7. Give a specific example of a healthcare agent action that belongs in each tier.

---

**Q5. (Multiple Choice)** Under the HIPAA minimum necessary standard, which of the following describes the most compliant behavior for a PA agent retrieving patient information?

A. Retrieve the complete patient record to ensure nothing is missed
B. Retrieve only the specific fields (insurance information, relevant clinical documentation) needed for the PA workflow in question
C. Retrieve the last 5 years of all clinical encounters
D. Retrieve information for all active patients, not just the one in the current request

---

**Q6. (Multiple Choice)** Your agent deployment uses an alias "production" pointing to version v3. Version v4 is released and the alias is updated to point to v4. Three hours later, a critical bug is found. What is the fastest remediation?

A. Redeploy v3 from source code
B. Update the "production" alias to point back to v3 — application code doesn't need to change
C. Hotfix v4 and create v5
D. Stop the production alias and wait for the fix

---

**Q7. (Short Answer)** Describe three specific scenarios where a healthcare agent should escalate to human review rather than attempting to complete the workflow autonomously.

---

**Q8. (Multiple Choice)** The "demo gap" in agentic AI systems is widest for which reason?

A. Demo environments use faster computers
B. Production users ask harder questions than demos
C. Non-determinism, integration failure points, load-dependent behaviors, and real user behavioral diversity all compound to create failure modes that demos with controlled inputs and dependencies don't reveal
D. Demos use better models than production

---

**Q9. (Applied Reasoning)** A healthcare organization's AI governance board asks: "What prevents this agent from accessing records for patients who are not part of the current request?" Write a complete technical answer covering all layers of protection.

---

**Q10. (Multiple Choice)** Which of the following is a HIPAA-compliant approach to logging for a healthcare agent?

A. Log every tool call with complete input and output for full audit trail
B. Log tool call metadata (tool name, session ID, timestamp, duration, status) without logging PHI data values
C. Disable logging to prevent PHI exposure
D. Log all inputs but encrypt outputs

---

## MODULE 7 ANSWER KEY

**A1: B**
Explanation: The human review gate is a stage in the CI/CD pipeline where clinical or domain experts review a sample of the evaluation set outputs. For healthcare AI, automated metrics alone cannot guarantee clinical correctness. Human expert sign-off provides the domain validation that automated systems cannot.

**A2:**
Five observability layers:
1. Business Metrics — Source: Lambda functions publishing custom metrics (PA workflows completed, submission rates, escalations)
2. Technical Performance — Source: Bedrock native metrics + Lambda native metrics (latency, error rates, throttling)
3. Cost Monitoring — Source: AWS Cost Explorer + custom cost tracking per session in Lambda/DynamoDB
4. Quality Metrics — Source: Evaluation pipeline + human review queue (task completion rate, human scores)
5. Security and Compliance — Source: CloudTrail + Bedrock Guardrail metrics (blocked content, auth failures)

**A3: A**
Calculation: 250,000 tokens / 1,000 × $0.003 = $0.75. Note: this is input tokens only. Add output tokens at $0.015/1K for total LLM cost.

**A4:**
Tier 0: Read-only operations — fully autonomous. Example: Retrieving patient insurance information, checking PA requirements, querying the formulary. No action is taken on the external world; only data is read.

Tier 2: Moderate-consequence writes — human notification required. Example: Sending an informational message to a patient about their care plan. Action has external effect but is reversible/low-consequence.

Tier 3: High-consequence writes — licensed professional approval required. Example: Submitting a prior authorization request to a payer. This action initiates an external business process and requires pharmacist or clinical review and explicit approval.

**A5: B**
Explanation: HIPAA's minimum necessary principle requires accessing only the information necessary for the specific purpose. For a PA workflow, you need the patient's insurance details and specific clinical documentation — not their complete medical history, not their records from 10 years ago, and not records for other patients.

**A6: B**
Explanation: This is exactly what aliases enable. The "production" alias still exists; you simply point it back to v3. Application code calls the "production" alias and immediately gets v3 behavior. No code deployment, no build time, instantaneous rollback.

**A7:**
Three valid escalation scenarios (many answers possible):
1. Tool failure after retries: Three consecutive failures to retrieve a required piece of documentation (EHR API down). The agent cannot complete the PA without this information and escalates with context about what was retrieved successfully and what is missing.
2. Clinical complexity flag: The PA involves an off-label indication or a combination therapy not covered in the knowledge base, and the agent cannot find matching clinical criteria. It escalates rather than guessing.
3. Business rule conflict: The patient's clinical documentation contradicts itself (two notes with conflicting diagnoses) and the agent cannot determine which to use for the PA. Requires human clinical judgment.

**A8: C**
Explanation: The demo gap is caused by the compound effect of multiple production-specific factors: non-determinism that becomes visible at scale, dependencies that fail at inconvenient times, load patterns that reveal concurrency assumptions, and real user behavior that differs from test cases. None of these typically appear in a controlled demo.

**A9:**
Complete technical answer:
Layer 1 (Tool Design): Each EHR tool requires a specific patient_id parameter. The agent must provide this ID explicitly — there is no "get all patients" function.
Layer 2 (IAM): The Lambda function's IAM execution role has access only to query the EHR API with patient-level authorization. It cannot perform bulk patient queries.
Layer 3 (EHR API): The EHR API is FHIR-compliant and enforces patient-level access control. Queries without a valid patient scope return 403.
Layer 4 (Agent Scope): The system prompt constrains the agent to "only access records relevant to the current request." Guardrails monitor for out-of-scope queries.
Layer 5 (Audit Logging): Every EHR API call from Lambda is logged with the session_id and patient identifier (last 4 chars for debugging only). Any access pattern that retrieves multiple patients in a single session triggers a CloudWatch alarm for human review.
Layer 6 (Rate Limiting): The rate limiter prevents excessive tool calls per session, which would be needed for bulk record access.

**A10: B**
Explanation: Logging metadata about tool calls (what tool was called, when, how long it took, whether it succeeded) provides operational visibility without exposing PHI. Option A (logging complete inputs/outputs) would log patient data in CloudWatch, creating a HIPAA issue. Option C (disabling logging) prevents audit trails required by HIPAA. Option D is inconsistent — inputs often contain PHI (patient IDs, query context).

---

*End of All Checkpoint Quizzes*
