# CAPSTONE PROJECT GUIDE & COURSE INDEX
## Week 12 — Final Project and Complete Course Reference

---

# CAPSTONE PROJECT: Healthcare Agentic AI System

## Project Overview

The capstone project requires students to design, implement, and defend a complete agentic AI system for a healthcare use case. This is the culminating assessment for the 12-week course and is worth 25% of the final grade.

---

## Approved Healthcare Domains

**Domain 1: Revenue Cycle Management**
Potential agents: denial management, prior authorization, claim validation, coding assistance, eligibility verification

**Domain 2: Clinical Decision Support**
Potential agents: clinical guideline adherence, drug interaction screening, order set recommendation, care pathway guidance

**Domain 3: Care Coordination**
Potential agents: patient risk stratification, care gap identification, care brief generation, referral management

**Domain 4: Utilization Management**
Potential agents: inpatient day management, concurrent review, discharge planning support, readmission prevention

**Domain 5: Pharmacy Benefits Management**
Potential agents: formulary management, step therapy compliance, medication reconciliation, specialty drug coordination

**Domain 6: Quality Reporting and Improvement**
Potential agents: HEDIS measure gap identification, quality data abstraction, reporting automation, outreach prioritization

---

## Capstone Requirements

### Technical Requirements

**1. Working Bedrock Agent**
- Minimum 2 Action Groups with distinct functional domains
- Minimum 4 tools total across action groups
- System prompt that clearly defines role, capabilities, and constraints
- Guardrails configuration with at minimum 2 topic restrictions and PII redaction
- Deployed to a named alias (not DRAFT) for the presentation

**2. Lambda Tool Implementation**
- Lambda function(s) backing the action groups
- Proper Bedrock event/response format
- Error handling: all error categories covered
- Unit tests: minimum 5 tests per Lambda handler
- Structured logging without PHI

**3. Knowledge Base**
- At minimum 5 real or synthetic documents ingested
- Metadata companion files for all documents
- Chunking strategy justified in writing
- Retrieval tested with minimum 5 evaluation queries

**4. Evaluation Framework**
- Minimum 20-scenario evaluation set (including happy path, edge cases, adversarial)
- Task completion rate measurement
- Tool correctness rate measurement
- At minimum 5 adversarial scenarios tested
- Written evaluation report with results

**5. Observability Implementation**
- Custom CloudWatch metrics (minimum 3)
- Minimum 2 CloudWatch alarms with defined thresholds
- Cost model for the agent (estimated cost per session, per month)

---

### Documentation Requirements

**Architecture Document (3-5 pages)**
- Architecture diagram (draw.io, Lucidchart, or equivalent)
- Component descriptions
- Data flow description (including where PHI exists and how it's protected)
- IAM roles and policies (described)
- Failure mode analysis (5 failure modes with mitigations)

**Evaluation Report (2-3 pages)**
- Success criteria definition
- Metrics portfolio with targets and actual results
- Test set description and results
- Adversarial test results
- Known limitations and edge cases

**Governance and Risk Memo (2-3 pages)**
- Use case risk assessment
- Autonomy policy (what the agent can do autonomously vs. requires human approval)
- HIPAA compliance approach
- Incident response summary
- Recommended governance oversight process

---

### Presentation Requirements

**Format:** 20-minute presentation + 10-minute Q&A

**Required slides:**
1. Use case overview and business problem
2. Architecture diagram walkthrough
3. Live demo (3-5 minutes) — run 2-3 test scenarios in the Bedrock console
4. Evaluation results
5. Key design decisions and tradeoffs made
6. Governance approach
7. What you would do differently

**Q&A topics to prepare for:**
- Why did you choose this foundation model?
- How did you write this specific tool description?
- What happens when [specific failure scenario]?
- How does this comply with HIPAA?
- What would need to change for this to be production-ready?
- What was the hardest design decision?

---

## Capstone Scoring Rubric

| Component | Points | Criteria |
|-----------|--------|---------|
| Technical Implementation | 40 | Working agent, tools, KB, guardrails |
| Evaluation Framework | 20 | Test set quality, metrics, adversarial coverage |
| Documentation | 20 | Architecture, evaluation report, governance memo |
| Presentation | 10 | Clarity, demo, Q&A handling |
| Innovation / Healthcare Impact | 10 | Novelty, real-world applicability, insight |
| **Total** | **100** | |

**Letter grades:**
- 90-100: A (Distinguished — production-ready quality)
- 80-89: B (Proficient — strong with minor gaps)
- 70-79: C (Satisfactory — functional with significant gaps)
- Below 70: Incomplete

---

## Capstone Milestones

**Week 8: Use Case Proposal** (due by end of week)
- One-page description of chosen use case
- Preliminary agent design (tools list, KB topic)
- Advisor approval required before proceeding

**Week 10: Architecture Review** (in-class presentation, 10 minutes)
- Architecture diagram presented
- Peer and instructor feedback
- Course correction opportunity before implementation

**Week 11: Code Freeze**
- All Lambda code, agent configuration, and KB must be complete
- Evaluation suite completed and run
- Documentation drafted

**Week 12: Final Presentation**
- 20-minute presentation + 10-minute Q&A
- Live demo in Bedrock console
- All deliverables submitted

---

# COMPLETE COURSE INDEX

## Files in This Course Package

| File | Contents |
|------|---------|
| COURSE_OVERVIEW.md | Introduction, prerequisites, structure, assessment |
| MODULE_01_Foundations.md | Agentic AI fundamentals, components, healthcare cases |
| MODULE_02_Goals_and_Metrics.md | Goal decomposition, success metrics, evaluation frameworks |
| MODULE_03_Architecture.md | Agent loop, tool design, memory, state, observability |
| MODULE_04_Bedrock_Deep_Dive.md | Full Bedrock console walkthrough, action groups, testing |
| MODULE_05_Knowledge_Bases.md | RAG architecture, KB creation, chunking, retrieval evaluation |
| MODULE_06_MCP_Servers.md | MCP protocol, server implementation, enterprise patterns |
| MODULE_07_Productionizing.md | CI/CD, monitoring, cost controls, governance |
| CHECKPOINT_QUIZZES.md | All 7 module quizzes with answer keys |
| PRACTICE_EXERCISES.md | All 35+ practice exercises |
| POWERPOINT_OUTLINE.md | Complete slide deck outline with speaker notes |
| CAPSTONE_AND_INDEX.md | This file — capstone guide and course index |

---

## Key Concepts Quick Reference

### Agent Design Principles
1. Right-size your architecture: single call → chain → agent → multi-agent (use the simplest that works)
2. Tool descriptions are code — write them as precisely as code
3. Design for failure at every layer
4. Log everything, PHI never
5. Human override at every consequential action point
6. Cost is a first-class design constraint
7. Evaluate before you deploy, not after

### Bedrock Agent Quick Reference
- Create Agent → Configure model + system prompt + IAM role
- Add Action Group → OpenAPI schema + Lambda function + resource policy
- Add Knowledge Base → S3 + Titan Embeddings + OpenSearch Serverless
- Add Guardrails → Topics + PII + Grounding
- Prepare → Test in console → Create version → Create alias → Invoke via API

### Lambda Tool Contract
```
Input: event['actionGroup'], event['apiPath'], event['parameters']
Output: {actionGroup, apiPath, httpMethod, httpStatusCode, responseBody}
Errors: Return structured JSON error, never raw exceptions
PHI: Never log PHI values, only log metadata/identifiers
```

### Key AWS IAM Rules for Agents
- BedrockAgentRole: least-privilege, tied to specific agent ARN
- Lambda resource policy: requires source-account AND source-arn conditions
- Lambda execution role: separate from agent role, minimal S3/DDB/Secrets access

### Evaluation Targets (Healthcare)
- Task completion rate: ≥ 95%
- Tool correctness: ≥ 98%
- Hallucination rate: < 0.1% clinical claims
- Under-triage rate: < 0.5% (safety constraint, not just metric)
- Adversarial pass rate: 100% required before production

---

## Healthcare Compliance Reference

### HIPAA Technical Safeguards for Agent Systems
- Encryption at rest: All S3, DynamoDB, OpenSearch data encrypted with KMS
- Encryption in transit: All API calls use HTTPS/TLS
- Access controls: IAM policies limiting PHI access to minimum necessary
- Audit controls: CloudTrail API logs + Lambda custom access logs
- Integrity: S3 object versioning for document integrity
- Transmission security: VPC endpoints for AWS service communication

### FDA SaMD Applicability Questions
1. Does the agent's output directly inform clinical treatment decisions?
2. Does the agent replace (vs. support) clinician judgment?
3. Would a clinician act differently based solely on the agent's output?
If any answer is YES → consult regulatory affairs before deployment

### Agent Autonomy Policy Template

| Action Type | Tier | Approval Required |
|------------|------|-------------------|
| Read-only data retrieval | 0 | None |
| Internal draft creation | 0 | None |
| Sending internal notifications | 1 | Notification only |
| Creating external submissions (drafts) | 2 | Human notification + review window |
| Submitting to payers/external systems | 3 | Explicit professional approval |
| Modifying clinical records | 3 | Explicit licensed professional approval |
| Patient-facing communications | 3 | Clinical review and approval |

---

## Recommended Reading by Module

**Module 1 (Foundations):**
- "ReAct: Synergizing Reasoning and Acting in Language Models" — Yao et al. (2022)
- AWS Documentation: Amazon Bedrock Agents overview

**Module 2 (Metrics):**
- "RAGAS: Automated Evaluation of Retrieval Augmented Generation" — Es et al. (2023)
- "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" — Zheng et al. (2023)

**Module 3 (Architecture):**
- AWS Well-Architected Framework: Machine Learning Lens
- "Building LLM Powered Applications" — Valentina Alto (Chapters 6-9)

**Module 4 (Bedrock):**
- Amazon Bedrock Developer Guide (AWS documentation — required reading)
- Bedrock Agents workshop: aws.amazon.com/bedrock/agents/

**Module 5 (Knowledge Bases):**
- "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" — Lewis et al. (2020)
- Amazon Bedrock Knowledge Bases documentation

**Module 6 (MCP):**
- Model Context Protocol Specification: modelcontextprotocol.io
- Anthropic MCP announcement blog post

**Module 7 (Productionizing):**
- NIST AI Risk Management Framework (AI RMF 1.0)
- FDA Draft Guidance: Artificial Intelligence-Enabled Device Software Functions
- "Responsible AI Practices" — Google AI documentation

---

## Student Success Tips

**On Technical Implementation:**
- Build the simplest version that works, then add complexity
- Test each Lambda function independently before connecting to Bedrock
- Use the trace viewer obsessively during development
- Write your tool descriptions last — after you've seen how the agent naturally phrases its needs

**On Evaluation:**
- Write your evaluation set before you build the agent — it clarifies requirements
- Run adversarial tests personally — try to break your own agent
- Never declare victory based only on automated metrics — always do at least some human review

**On Healthcare Governance:**
- Involve compliance and legal from day one, not week 11
- Document every design decision that involves PHI or clinical action
- The question "who is accountable if this makes an error?" must have a specific human answer

**On The Course:**
- Office hours are for architecture review — bring your design problems, not just debugging questions
- Peer review each other's tool descriptions — fresh eyes catch ambiguities the author misses
- The capstone is about the thinking and the tradeoffs, not just the code — articulate your design decisions clearly

---

*This course was designed for healthcare data scientists transitioning to agentic AI engineering.*
*Version 1.0 | Built for Amazon Bedrock (2026)*
*For questions: contact your course instructor*
