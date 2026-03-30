# PRACTICE EXERCISES — All Modules
## Applied Exercises with Detailed Instructions

---

# MODULE 1 EXERCISES: Foundations of Agentic AI

---

## Exercise 1.1 — Agent vs. Workflow Decision Analysis
**Type:** Applied Reasoning | **Difficulty:** Intermediate

**Scenario:**
A large hospital system is considering AI solutions for the following five workflows. For each, classify it as: (a) Single LLM Call, (b) Prompt Chain / Workflow, or (c) Agentic System. Justify each classification with specific reference to the defining characteristics of each pattern.

1. A nurse enters a patient's vital signs. The system generates a brief natural language summary of whether the vitals are within normal range.

2. A coder receives a clinical note and needs ICD-10 and CPT codes. The system: extracts diagnoses, maps each to ICD-10, extracts procedures, maps each to CPT, identifies potential bundling issues, and formats the complete claim.

3. A care manager asks: "Which of my 200 active patients are most at risk of hospital readmission in the next 30 days and why?" The system must check risk scores, review recent encounters, check lab trends, and identify specific risk factors per patient.

4. A billing specialist submits a denied claim. The system must understand the denial reason, search for applicable appeal policies, retrieve clinical documentation, determine whether the documentation supports the appeal, and either draft the appeal letter or recommend alternative action.

5. A physician dictates a brief note: "Patient doing well. Continue current medications." The system formats this as a structured progress note with required documentation elements.

**Deliverables:**
- Classification for each workflow with justification
- For workflows classified as agentic: draft a tool list (minimum 3 tools per agent) with descriptions

---

## Exercise 1.2 — Healthcare Agent Tool Design
**Type:** Implementation | **Difficulty:** Advanced | **Healthcare-Specific**

**Scenario:**
You are designing tools for a prior authorization agent for a specialty pharmacy. The agent needs to collect all information required for a biologic medication PA submission.

**Task:**
Design the complete tool registry for this agent. For each tool, provide:
1. Tool name (snake_case)
2. Natural language description (as would be written for the LLM to read — include when to use it and when NOT to use it)
3. Input schema (all parameters with types, descriptions, and required/optional)
4. Return value schema (status, data fields, error structure)
5. Tier classification (Tier 0: read, Tier 2: low-consequence write, Tier 3: high-consequence write)

**Required tools to design:**
- Patient insurance lookup
- PA requirements lookup by drug/payer
- Step therapy compliance check
- Clinical documentation retrieval
- PA draft creation
- PA submission (note: this is Tier 3)
- PA status check
- Human escalation

**Evaluation criteria:**
- Tool descriptions must be specific enough to prevent incorrect tool selection
- Parameter descriptions must include format requirements and examples
- Return schemas must include both success and error paths
- Tool boundaries must be coherent (each tool does one thing)

---

## Exercise 1.3 — Architecture Diagram Construction
**Type:** Architecture | **Difficulty:** Intermediate

**Task:**
Draw (using draw.io, Lucidchart, or hand-drawn and photographed) a complete architecture diagram for a "Revenue Cycle Denial Management Agent" for a hospital system.

**Requirements your diagram must include:**
- User interface layer (who calls the agent and how)
- Bedrock Agent with model specification
- At least 3 Action Groups with tool descriptions
- Lambda function backends with IAM roles labeled
- At least one Knowledge Base (specify what it contains)
- EHR and payer system integrations
- Observability layer (CloudWatch, CloudTrail)
- Security boundaries (VPC, IAM role boundaries)
- Data flow arrows with labels indicating what data flows on each arrow
- PHI boundary markers (where does PHI exist in this architecture?)

**Deliverables:**
- Completed diagram
- One-page written description of the diagram explaining each component's role
- Failure mode analysis: identify 5 points in the diagram where failures could occur and describe the impact of each failure

---

## Exercise 1.4 — Metric Design for Care Coordination Agent
**Type:** Metric Design | **Difficulty:** Intermediate

**Scenario:**
A care management program deploys a care coordination agent that prepares care briefs for care coordinators. The brief includes: care gaps, upcoming appointments, outstanding referrals, recent lab trends, and recommended actions.

**Task:**
Design the complete metrics portfolio for this agent:

1. **Define the success criteria** for this agent: what does "good performance" mean, specifically?

2. **For each metric below, define:**
   - Exact calculation formula
   - Data source (where does the raw data come from?)
   - Measurement frequency (real-time, daily, weekly)
   - Target value (based on your judgment and the healthcare context)
   - Alarm threshold (when should you be notified something is wrong?)
   - Severity if threshold is breached (warning vs. critical)

   Metrics to design:
   - Brief completeness rate
   - Care gap identification accuracy (compared to manual review)
   - False positive care gap rate
   - Agent session latency (p50, p95, p99)
   - Cost per brief
   - Care coordinator time saved per brief (indirect metric — how would you measure this?)
   - PHI access audit compliance rate

3. **Multi-objective framework:** Define primary objectives, secondary objectives, and hard constraints for this agent.

---

## Exercise 1.5 — Governance Document Draft
**Type:** Implementation Challenge | **Healthcare-Specific**

**Scenario:**
You are proposing a new AI agent to the governance board of a regional hospital system. The agent will assist emergency department nurses in identifying patients who may need escalated attention during high-census periods.

**Task:**
Draft the complete governance submission document including:

1. **Use Case Description** (1 paragraph): What the agent does, how it works, who uses it
2. **Risk Assessment** (table format):
   - Clinical risk (patient harm potential)
   - Compliance risk (regulatory issues)
   - Operational risk (what if it's unavailable)
   - Privacy risk (PHI handling)
   - Reputational risk (public disclosure of failure)
   - For each: likelihood, severity, proposed mitigation
3. **Autonomy Policy**: Map each agent capability to a tier (read-only, notify, approve-before-act)
4. **Human Override Protocol**: Who can override what, under what conditions, using what mechanism
5. **Incident Response Plan**: First 4 hours after a serious agent error is discovered
6. **Success Metrics**: What metrics will you use to demonstrate the agent is performing acceptably
7. **Evaluation Plan**: How will you evaluate the agent before deployment and after deployment

---

# MODULE 2 EXERCISES: Goals and Success Metrics

---

## Exercise 2.1 — Goal Decomposition Workshop
**Type:** Applied Reasoning | **Difficulty:** Advanced

**Scenario:**
An integrated delivery network (IDN) wants an agent to "improve quality measure performance." HEDIS measures are the target.

**Task:**
Decompose this vague organizational goal into agent-level specifications:

1. **Identify three specific HEDIS measures** the agent could support (research actual HEDIS measures)
2. **For each measure, define:**
   - The specific data the agent needs to assess measure compliance
   - The agent's specific proximal goal (one sentence)
   - The specific action the agent can take to support compliance improvement
3. **Identify the constraints** specific to quality measure work:
   - HIPAA considerations
   - Attribution logic complexity
   - Measure exclusion logic
   - Data timeliness requirements
4. **Design a multi-objective framework** for a "HEDIS quality gap identification agent"
5. **Define what "success" looks like** at 90 days post-deployment

---

## Exercise 2.2 — Evaluation Set Construction
**Type:** Implementation | **Difficulty:** Advanced | **Healthcare-Specific**

**Task:**
Build a 20-scenario evaluation set for a clinical documentation assistant agent that generates SOAP notes from encounter transcripts.

**Requirements:**
- 5 happy path scenarios (straightforward encounters with clear documentation)
- 5 edge cases (complex encounters: multiple problems, patient communication challenges, uncertain diagnoses)
- 5 adversarial scenarios (attempts to induce inappropriate clinical statements, PHI leakage, etc.)
- 5 error condition scenarios (missing information, conflicting data, out-of-scope requests)

**For each scenario, provide:**
- Scenario ID and type
- Input transcript (realistic, 100-300 words)
- Expected SOAP note structure
- Specific evaluation criteria (what must the agent get right?)
- What would constitute a failure (be specific)

**For 3 of the adversarial scenarios, specifically test:**
- An attempt to have the agent make a diagnosis
- An attempt to have the agent recommend a specific medication dose
- An attempt to extract PHI for a patient not in the current encounter

---

## Exercise 2.3 — LLM-as-Judge Calibration Exercise
**Type:** Architecture Diagram | **Difficulty:** Intermediate**

**Task:**
Design an LLM-as-judge calibration process for a healthcare agent evaluation system.

The system needs to:
1. Detect when LLM-judge scores are systematically inflated vs. human reviewers
2. Periodically re-calibrate the judge against human baselines
3. Apply score corrections when bias is detected

**Deliverables:**
1. Architecture diagram of the calibration pipeline
2. The calibration prompt you would use for the LLM judge (written for a PA agent)
3. Statistical method for detecting score inflation
4. Process for determining when to recalibrate

---

## Exercise 2.4 — Cost vs. Quality Tradeoff Analysis
**Type:** Metric Design | **Difficulty:** Advanced

**Scenario:**
A prior authorization agent costs an average of $0.85/session using Claude 3 Sonnet. Leadership wants to evaluate switching to a less expensive model (Claude 3 Haiku at ~$0.08/session) without degrading quality.

**Task:**
Design a rigorous A/B evaluation process to determine whether Claude 3 Haiku is acceptable:

1. Define the evaluation methodology (which model handles which sessions, how many sessions, for how long)
2. Define primary success metrics and their thresholds
3. Define the statistical test you would use to determine significance
4. Define what "no statistically significant quality degradation" means in specific numerical terms
5. Identify the specific task types where you would expect Haiku to perform similarly to Sonnet, and where you would expect degradation
6. Design the rollback trigger: what specific result would cause you to stop the Haiku evaluation?

---

## Exercise 2.5 — Adversarial Evaluation for Revenue Cycle Agent
**Type:** Implementation Challenge | **Healthcare-Specific**

**Task:**
Design a 10-scenario adversarial evaluation set specifically for a revenue cycle automation agent that processes denied claims.

Focus on:
- PHI exposure scenarios
- Authority manipulation (claimed administrator tries to bypass controls)
- Scope creep (attempts to process claims outside the agent's designated scope)
- Data integrity manipulation (attempts to alter clinical documentation)
- False identity (claims to be a different type of user with different permissions)

For each scenario, define:
1. The adversarial input
2. The expected safe behavior
3. The failure mode if the agent is not robust
4. The real-world consequence of the failure

---

# MODULE 3 EXERCISES: Agent System Architecture

---

## Exercise 3.1 — State Machine Design
**Type:** Architecture | **Difficulty:** Advanced

**Task:**
Design the complete state machine for a utilization management (UM) agent that handles inpatient admission reviews.

An inpatient UM review involves:
- Initial admission notification
- Criteria-based review (does the admission meet medical necessity criteria?)
- Physician advisor review (for cases not clearly meeting criteria)
- Approval or denial with reason
- Denial notification to hospital and patient
- Appeal intake (if patient/hospital appeals)
- Peer-to-peer request (physician advisor calls)
- Final determination

**Deliverables:**
1. Complete state diagram with all states, transitions, and triggers
2. State definitions (what data is required/available in each state)
3. Legal transitions (including guards/conditions)
4. Illegal transitions (explicitly prohibited transitions with reasoning)
5. Error states and recovery paths
6. DynamoDB schema for persisting the state

---

## Exercise 3.2 — Tool Registry Design and Evaluation
**Type:** Implementation | **Difficulty:** Advanced

**Scenario:**
You have built a care coordination agent with 12 tools. Initial testing shows the agent frequently: (a) calls `get_complete_patient_record` when it only needs insurance information, and (b) calls `get_lab_results` with no date range specified, resulting in 5+ years of data that overwhelms the context window.

**Task:**
1. Diagnose why each of these tool selection errors is occurring (examine the tool descriptions)
2. Rewrite the tool descriptions to prevent each error
3. Design a testing methodology to verify your description changes work (how will you confirm the agent now makes better tool selections?)
4. Identify two other tool design patterns that could have prevented these problems at design time

---

## Exercise 3.3 — Observability Architecture Design
**Type:** Architecture Diagram | **Difficulty:** Advanced

**Task:**
Design the complete observability architecture for a prior authorization agent deployed in a specialty pharmacy, including:

**Architecture diagram must include:**
- All metric sources (Lambda, Bedrock, custom)
- CloudWatch metric namespaces and metric names
- CloudWatch alarms with thresholds
- Alert routing (SNS → PagerDuty/Slack/Email for each alarm level)
- Cost monitoring pipeline
- Human review queue and workflow
- Dashboard layout (describe what's on the main dashboard)

**Define alarm thresholds for:**
- PA workflow completion rate drops below ____%
- Lambda error rate exceeds ___% in __ minutes
- p95 session latency exceeds ____ seconds
- Daily cost exceeds $_____
- Human escalation rate exceeds ____%

Justify each threshold with reasoning about what the threshold indicates operationally.

---

## Exercise 3.4 — Cost Optimization Analysis
**Type:** Metric Design | **Difficulty:** Advanced

**Scenario:**
A care coordinator brief agent generates the following cost breakdown per session:
- LLM: $3.20 (Claude 3 Opus, 8 iterations, 12K tokens/iteration)
- Lambda: $0.04
- Knowledge base: $0.002
- Total: $3.24/session

Target: $0.50/session. The brief quality is currently rated 4.6/5 by care coordinators.

**Task:**
Identify and analyze 5 specific optimization approaches. For each approach:
1. Describe the change
2. Estimate the cost reduction
3. Estimate the potential quality impact (scale: none, minor, moderate, major)
4. Describe how you would measure whether quality was affected
5. Order the approaches by risk-adjusted value (impact/risk)

**Constraint:** Do not recommend approaches that would degrade quality below 4.0/5 coordinator rating.

---

## Exercise 3.5 — Failure Mode Analysis
**Type:** Implementation Challenge | **Healthcare-Specific**

**Task:**
Conduct a Failure Mode and Effects Analysis (FMEA) for a PA submission agent. The FMEA should identify all significant failure modes, their effects, likelihood, and recommended mitigations.

FMEA table structure:
| Failure Mode | Effect | Likelihood (1-5) | Severity (1-5) | RPN (L×S) | Mitigation | Residual Risk |

**Required failure modes to analyze (minimum):**
- EHR API unavailable
- Payer PA portal API unavailable
- LLM produces incorrect clinical information in PA letter
- Agent calls submission tool before pharmacist approval
- Agent submits duplicate PA for same patient/medication
- Session times out mid-workflow (PA partially completed)
- Wrong patient ID used throughout the workflow
- Knowledge base contains outdated PA requirements
- Lambda function exceeds maximum execution time
- LLM returns malformed tool call parameters

Provide complete FMEA table + top 3 priority mitigations with implementation details.

---

# MODULE 4 EXERCISES: Amazon Bedrock Deep Dive

---

## Exercise 4.1 — Bedrock Agent Build Lab
**Type:** Implementation | **Difficulty:** Advanced

**Complete hands-on lab:**

**Part A: Infrastructure Setup (30 minutes)**
1. Create IAM roles: `BedrockAgentExecutionRole`, `PAToolsLambdaRole`
2. Write IAM policies from scratch using least-privilege principles
3. Document every permission and justify why it's needed

**Part B: Lambda Tool Implementation (45 minutes)**
1. Create a Lambda function with at minimum 3 handlers:
   - `get_patient_coverage(patient_id)` — mock EHR data
   - `check_pa_requirements(payer_id, drug_code)` — mock payer rules
   - `search_clinical_guidelines(query)` — returns hardcoded guideline excerpts

2. Implement proper error handling: structured error responses for missing parameters, not-found cases, and simulated API failures

3. Write 5 unit tests for the Lambda handlers

**Part C: Agent Creation (30 minutes)**
1. Create Bedrock Agent with appropriate system prompt
2. Create Action Group with OpenAPI schema
3. Connect Lambda function
4. Prepare and test agent

**Part D: Testing and Debugging (30 minutes)**
1. Run 5 test scenarios and capture traces
2. Identify at least one trace showing tool selection, tool execution, and successful completion
3. Deliberately cause a failure (remove Lambda permission) and capture the error trace
4. Fix the failure and verify

**Deliverables:**
- GitHub repository with Lambda code and tests
- Screenshots of agent trace outputs (4 scenarios)
- One-page reflection: what surprised you during the build?

---

## Exercise 4.2 — OpenAPI Schema Design
**Type:** Implementation | **Difficulty:** Intermediate

**Task:**
Write a complete, production-quality OpenAPI 3.0 schema for a clinical coding tools action group. The schema must define the following operations:

1. `POST /lookup-icd10-code` — Given a diagnosis description, return matching ICD-10 codes with specificity ranking
2. `POST /lookup-cpt-code` — Given a procedure description, return matching CPT codes
3. `POST /validate-code-combination` — Given a set of ICD-10 and CPT codes, check for CCI edits and bundling issues
4. `POST /get-code-documentation-requirements` — Given a procedure code, return documentation requirements for medical necessity

For each operation:
- Write a comprehensive description (must be LLM-readable and specific)
- Define all required and optional parameters with descriptions
- Define the response schema including success and error cases
- Note any format requirements for parameters

Validate your schema at https://editor.swagger.io/ — it must pass validation.

---

## Exercise 4.3 — Production Deployment Design
**Type:** Architecture Diagram | **Difficulty:** Advanced

**Task:**
Design the full deployment architecture for promoting an agent from development to staging to production, including:

1. Three-environment architecture diagram (dev, staging, prod in separate AWS accounts)
2. CodePipeline workflow for agent deployment
3. Evaluation gate configuration (what tests must pass before staging → prod promotion?)
4. Alias configuration for each environment
5. Traffic shifting strategy for production releases
6. Rollback triggers (automated and manual)
7. Cross-account IAM roles and trust relationships needed

---

## Exercise 4.4 — Trace Debugging Workshop
**Type:** Applied Reasoning | **Difficulty:** Intermediate

**Scenario:**
You are given three agent trace excerpts. For each trace, identify what went wrong, explain why, and describe the specific fix.

**Trace 1:**
```
Step 1: Rationale: "I need to check the patient's formulary tier"
        Action: get_patient_demographics(patient_id="MRN-12345")

Step 2: Rationale: "I have the patient's demographics. Now I need the formulary"
        Action: get_patient_demographics(patient_id="MRN-12345")  [Same call again]

Step 3: [Same pattern repeated]
```

**Trace 2:**
```
Step 1: Rationale: "Let me retrieve all available information about this patient"
        Action: get_complete_patient_record(patient_id="MRN-12345",
                include_history_years=50)

[Observation: 45,000 tokens of patient data returned]

Step 2: [Reasoning becomes incoherent — LLM cannot process all context]
```

**Trace 3:**
```
Step 1: Rationale: "I should check the prior authorization requirements"
        Action: check_pa_requirements(payer_id="BCBS", drug_code="adalimumab")

Observation: {"status": "error", "error_message": "Invalid drug code format.
              Expected NDC-11 or HCPCS code. Received: 'adalimumab'"}

Step 2: Rationale: "The PA requirements check was successful. The patient's
        insurance is BlueCross PPO."  [Hallucination — ignoring the error]
```

---

## Exercise 4.5 — IAM Security Audit
**Type:** Implementation Challenge | **Healthcare-Specific**

**Scenario:**
You are auditing the IAM configuration for a deployed Bedrock agent. You find the following configuration. Identify every security issue and propose the least-privilege replacement.

**Existing BedrockAgentRole policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "*",
      "Resource": "*"
    }
  ]
}
```

**Existing Lambda execution role policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:*",
        "dynamodb:*",
        "secretsmanager:*",
        "logs:*"
      ],
      "Resource": "*"
    }
  ]
}
```

**Existing Lambda resource-based policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "bedrock.amazonaws.com"},
      "Action": "lambda:InvokeFunction",
      "Resource": "arn:aws:lambda:us-east-1:123456789012:function:healthcare-pa-tools"
    }
  ]
}
```

Tasks:
1. List every security violation with severity (Critical/High/Medium)
2. Write corrected versions of all three policies
3. Explain what specific attack each correction prevents
4. Identify any missing security controls that should be added

---

# MODULES 5-7 EXERCISES: (Selected)

---

## Exercise 5.1 — Knowledge Base Design for Payer Policy Library
**Type:** Implementation | **Healthcare-Specific**

**Task:**
Design and implement a knowledge base for payer coverage policies for a revenue cycle management agent. The KB should enable the agent to answer: "Does [payer X] cover [procedure/medication Y] for [clinical indication Z]?"

**Deliverables:**
1. Document collection strategy (what documents, from where, how to obtain them)
2. Document preprocessing pipeline (what transformations are needed before ingestion)
3. Metadata schema for all documents
4. Chunking strategy choice with justification
5. 10 test queries with expected retrieval behavior
6. Evaluation methodology for retrieval quality
7. Update cadence and process (payer policies change frequently)

---

## Exercise 6.1 — MCP Server Implementation
**Type:** Implementation Challenge | **Difficulty:** Advanced

**Task:**
Implement a fully functional MCP server for clinical coding tools using the Python MCP SDK.

The server must implement:
- `lookup_icd10` tool
- `lookup_cpt` tool
- `validate_coding_combination` tool
- Tool definitions with production-quality descriptions

**Requirements:**
- Proper error handling with structured error responses
- Input validation for all parameters
- Unit tests for all three tools
- Docker containerization with Dockerfile
- README with setup instructions

Use mock data for the coding lookups (no access to production coding databases required).

---

## Exercise 7.1 — Production Runbook Development
**Type:** Implementation Challenge | **Healthcare-Specific**

**Task:**
Create the complete operations runbook for a production PA agent deployment. A runbook is the step-by-step guide that operations staff use when something goes wrong at 2am on a Sunday.

**The runbook must cover:**

1. **Service Health Check Procedure** — How to verify the agent is functioning normally (step-by-step commands + expected outputs)

2. **Incident Response for Each Alert:**
   For each CloudWatch alarm you defined in Exercise 3.3, provide:
   - What the alarm means (in plain English)
   - Immediate triage steps (first 5 minutes)
   - Investigation procedure (next 30 minutes)
   - Escalation criteria and contacts
   - Resolution options
   - Communication template for affected users

3. **Rollback Procedure** — Step-by-step alias update to roll back to previous version

4. **Emergency Shutdown** — How to immediately stop all agent invocations if needed

5. **Post-Incident Review Template** — Structure for documenting what happened, why, and how to prevent recurrence

---

*End of Practice Exercises*
