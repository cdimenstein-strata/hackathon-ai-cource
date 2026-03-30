# Designing and Deploying Agentic AI Systems with Amazon Bedrock
## A Postgraduate Course for Practicing Data Scientists

---

## COURSE OVERVIEW

### Institutional Context and Rationale

Healthcare AI has entered a second inflection point. The first was the broad adoption of supervised machine learning — predictive models for readmission risk, sepsis scores, claims fraud detection, and imaging interpretation. These systems were fundamentally reactive: they processed inputs and produced outputs, and a human decided what to do next.

The second inflection point is agentic AI: systems that reason about tasks, decompose goals, select and invoke tools, maintain context across multi-step workflows, and operate with degrees of autonomy that were previously the exclusive domain of human specialists. A care coordination agent that can review discharge instructions, check for medication conflicts against a formulary API, draft a care plan, flag it for clinician review, and schedule a follow-up call — this is not a chatbot. It is an orchestrated intelligent system that interacts with real infrastructure, real data, and real consequences.

This course exists because the skills required to build such systems are fundamentally different from the skills required to train and evaluate ML models. Data scientists who have spent years building excellent predictive pipelines routinely struggle when asked to design, implement, and govern agentic systems. The reasons for this are structural, not intellectual: they have never needed to think about tool registries, action schemas, memory architectures, observability for non-deterministic systems, or the governance implications of autonomous action.

This course closes that gap. It is built around Amazon Bedrock because Bedrock represents the most complete managed platform for enterprise-grade agentic AI currently available — with native support for agents, knowledge bases, guardrails, model evaluation, and the observability infrastructure necessary for regulated healthcare deployments.

---

### Prerequisites

Students entering this course should be comfortable with:

- Python 3.9+ including async patterns, decorators, and type annotations
- REST API design and consumption
- Cloud fundamentals — specifically AWS (S3, Lambda, IAM, CloudWatch at basic level)
- Machine learning pipelines — data preprocessing, model training, evaluation loops
- Basic prompt engineering — few-shot prompting, chain-of-thought
- JSON schema design
- Familiarity with SQL or NoSQL data stores

Students are NOT expected to know:
- Agent architectures or orchestration frameworks
- AWS Bedrock beyond basic model invocation
- Lambda as a tool backend
- Knowledge base or vector store construction
- MCP (Model Context Protocol)
- Enterprise AI governance
- Healthcare compliance implications for AI systems (HIPAA, FDA software guidance)

---

### Course Structure: 12-Week Program

| Week | Module | Title | Delivery |
|------|--------|-------|----------|
| 1–2  | 1      | Foundations of Agentic AI | Lecture + Lab |
| 3    | 2      | Defining Agent Goals and Success Metrics | Lecture + Workshop |
| 4–5  | 3      | Agent System Architecture | Lecture + Architecture Lab |
| 6–7  | 4      | Amazon Bedrock Deep Dive | Hands-On Console Lab |
| 8    | 5      | Knowledge Bases in Bedrock | Build Lab |
| 9    | 6      | MCP (Model Context Protocol) Servers | Design + Implementation |
| 10–11| 7      | Productionizing Agent Systems | Enterprise Deployment Lab |
| 12   | —      | Capstone: Healthcare Agent System | Defended Project |

---

### Learning Outcomes

Upon completing this course, students will be able to:

1. **Explain** the architectural difference between a language model, a chatbot, and an agentic AI system, and justify which pattern fits a given healthcare use case.

2. **Design** complete agent system architectures including reasoning engine selection, tool registry design, memory strategy, and observability instrumentation.

3. **Implement** production-grade Bedrock agents with action groups backed by AWS Lambda, connected to knowledge bases, with guardrails and CloudWatch observability.

4. **Evaluate** agent performance using task completion rate, tool correctness, hallucination rate, latency, and cost-per-interaction metrics, using both automated and human evaluation pipelines.

5. **Deploy** agents in enterprise environments with CI/CD integration, cost controls, rate limiting, and human override capabilities.

6. **Govern** agentic AI systems under healthcare compliance frameworks, including HIPAA, FDA software guidance for AI/ML, and responsible AI principles.

7. **Architect** multi-agent systems using Model Context Protocol (MCP) and explain when MCP is and is not the right pattern.

---

### Assessment Structure

| Component | Weight | Timing |
|-----------|--------|--------|
| Module Checkpoint Quizzes (7 × 10 points) | 35% | End of each module |
| Practice Exercises (7 × 5 exercises) | 25% | Weekly submissions |
| Architecture Review Presentation | 15% | Week 6 |
| Capstone Project | 25% | Week 12 |

---

### Capstone Project Brief

Students will design, implement, and defend a complete agentic AI system for a healthcare use case of their choosing. Acceptable domains include:

- Revenue cycle management
- Clinical decision support
- Care coordination
- Utilization management and prior authorization
- Quality reporting and HEDIS measure tracking
- Patient communication and chronic disease management
- Pharmacy benefits management

The capstone must include:
1. Architecture document with diagram
2. Working Bedrock agent with at minimum two action groups
3. Knowledge base with at least one real or synthetic document corpus
4. Evaluation report against defined success metrics
5. Governance and risk assessment memo
6. 20-minute defended presentation

---

### A Note on Healthcare Context

This course is taught with deep respect for the complexity of healthcare. The stakes in healthcare AI are not abstract: a poorly designed agent that makes incorrect prior authorization recommendations, misclassifies a clinical note, or generates hallucinated medication guidance can harm patients. Every technical decision in this course — tool design, guardrail configuration, human override patterns, evaluation frameworks — will be examined through the lens of what happens when that decision is wrong at scale.

Students are encouraged to be skeptical of hype, to understand failure modes before celebrating capabilities, and to approach production deployment with the rigor of a regulated industry, not the pace of a startup demo.

---

### Required Tools and Access

Before Week 1, students must provision:

1. **AWS Account** with the following services enabled:
   - Amazon Bedrock (with model access requested for Claude 3 Sonnet, Titan Embeddings V2)
   - AWS Lambda
   - Amazon S3
   - Amazon OpenSearch Serverless (for vector store)
   - Amazon CloudWatch
   - AWS IAM

2. **Local Development Environment**:
   - Python 3.11+
   - AWS CLI v2 configured with appropriate credentials
   - boto3 >= 1.34
   - VS Code or equivalent IDE

3. **AWS Permissions**: IAM user or role with the following managed policies:
   - `AmazonBedrockFullAccess`
   - `AWSLambda_FullAccess`
   - `AmazonS3FullAccess`
   - `CloudWatchFullAccess`
   - `IAMFullAccess` (for role creation during labs)

> **Healthcare Note**: In production, you would never grant FullAccess policies. This is a learning environment. All labs include a section on production-appropriate least-privilege IAM configurations.

---

### Recommended Reading

- *Designing Machine Learning Systems* — Chip Huyen (background on ML system design patterns)
- *Building LLM Powered Applications* — Valentina Alto
- Amazon Bedrock Developer Guide (official documentation — required reading alongside course)
- AWS Well-Architected Framework — Machine Learning Lens
- NIST AI Risk Management Framework (AI RMF 1.0)
- FDA Draft Guidance: Artificial Intelligence-Enabled Device Software Functions
- ONC Trusted Exchange Framework (for interoperability context)

---

*End of Course Overview*
