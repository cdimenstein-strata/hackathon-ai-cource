# MODULE 5: Knowledge Bases in Amazon Bedrock
## Week 8 | Textbook Content

---

## Chapter 5.1 — What Is a Knowledge Base?

### The Fundamental Problem Knowledge Bases Solve

Language models are trained on a static corpus with a training cutoff date. They cannot know:
- Your organization's current payer contract escalation terms
- CMS MRF rate updates published last quarter
- IPPS final rule changes from last month
- Your organization's internal rate methodology documentation
- Your organization's internal billing guidelines

More critically, they can't be trusted to accurately recall financial and coding details even from their training data — they may hallucinate plausible-sounding but incorrect rate or coding information.

A Knowledge Base solves this by providing a retrieval system: the agent doesn't need to "know" the information in the model weights — it can look it up. This is the fundamental promise of Retrieval Augmented Generation (RAG).

**The analogy:** The difference between asking a financial analyst to recall a payer's negotiated rate methodology from memory versus handing them the current rate schedule to look it up. The lookup is more reliable, more current, and more auditable.

---

### RAG Architecture in Amazon Bedrock

```
Diagram Title: Full RAG Architecture in Amazon Bedrock

Ingestion Pipeline (run once, then on updates):
  [Document Store (S3)]
    ├── CMS IPPS final rule PDFs
    ├── Payer contract methodology summaries
    ├── MS-DRG weight tables and grouper documentation
    └── Market rate intelligence reports
           │
           ▼
  [Document Loader]
    Extracts text from PDF, Word, HTML, text, Markdown
           │
           ▼
  [Text Chunker]
    Splits documents into overlapping chunks
    (default: 300 tokens per chunk, 20% overlap)
           │
           ▼
  [Amazon Titan Embeddings V2]
    Converts each chunk to a 1,536-dimensional vector representation
    (semantic fingerprint of the chunk's meaning)
           │
           ▼
  [Amazon OpenSearch Serverless]
    Stores vectors in a k-NN index
    Also stores original text and metadata (source doc, page number, etc.)

Query Pipeline (run at inference time):
  [User Query / Agent Query]
           │
           ▼
  [Amazon Titan Embeddings V2]
    Converts query to same 1,536-dimensional vector space
           │
           ▼
  [OpenSearch Serverless: k-NN Search]
    Finds N most semantically similar chunk vectors
    Returns: chunks + similarity scores + source metadata
           │
           ▼
  [Ranking/Filtering Layer (optional)]
    Re-ranks results using more accurate cross-encoder model
    Filters by metadata (only return CMS rate documents, etc.)
           │
           ▼
  [Bedrock Agent Orchestrator]
    Injects retrieved chunks into agent context
           │
           ▼
  [Foundation Model]
    Generates response grounded in retrieved information
    Cites sources in response

Security Boundaries:
  S3 bucket → Knowledge Base sync: S3 bucket policy + Knowledge Base role
  Embeddings generation: Titan Embeddings called via Bedrock API (HIPAA eligible)
  Vector store (OpenSearch): VPC-accessible, IAM-authenticated
  Knowledge Base → Agent: Agent role has bedrock:Retrieve permission
```

---

### Why RAG for Healthcare Financial Analytics?

**Accuracy:** Rate methodology and coding information retrieved from authoritative sources is more accurate than information recalled from model training. A 2023 study in JAMA found GPT-4 had 93% accuracy on USMLE-style questions — impressive, but 7% errors in clinical settings can cause harm. Grounding in retrieved authoritative sources reduces this.

**Currency:** CMS rate rules change annually. Payer contracts escalate quarterly. MRF data updates monthly. RAG-based systems can be updated without retraining by simply updating the document corpus and re-syncing the knowledge base.

**Auditability:** When the agent makes a claim, it can cite the specific source document and passage it retrieved. This is not optional in regulated healthcare — you must be able to audit where rate and coding information came from.

**Scope control:** RAG constrains the agent to information you've curated. An agent without RAG can generate plausible-sounding rate methodology from its training data. An agent with RAG is constrained to your approved corpus — it will say "I couldn't find information about this in the rate documentation" rather than hallucinating an answer.

---

## Chapter 5.2 — Creating a Knowledge Base: Console Walkthrough

### Pre-requisites

1. **S3 Bucket** with your documents uploaded
2. **IAM Role** for the Knowledge Base (allows reading S3, invoking Titan Embeddings, writing to OpenSearch)
3. **Amazon OpenSearch Serverless Collection** (or let Bedrock create one)
4. **Documents** in supported formats: PDF, TXT, MD, HTML, DOC, DOCX, PPTX, CSV

### Supported Document Formats and Financial Analytics Considerations

| Format | Common Financial Analytics Use | Notes |
|--------|-------------------------------|-------|
| PDF | IPPS final rules, payer contract summaries, market intelligence reports | Most common; quality depends on PDF structure |
| DOCX | Internal rate methodology docs, contract term summaries | Good structure preservation |
| HTML | CMS web-published rate tables, payer portal pages (scraped) | Works well for structured content |
| TXT | CPT code descriptor files, NDC-to-HCPCS crosswalks | Pure text, best extraction quality |
| CSV | CCI edit tables, DRG weight tables, MRF rate data excerpts | Limited to simple table structures |
| MD | Internal wikis, technical documentation | Excellent structure preservation |

**Financial analytics-specific considerations for document preparation:**
- IPPS final rules in PDF often have complex table structures. Bedrock's PDF parser may not correctly extract tabular data. Pre-process with a specialized PDF parser if tables are critical.
- MRF JSON files are often extremely large (multi-GB). Extract relevant rate excerpts and convert to CSV or structured text before ingestion.
- Remove or redact any proprietary payer contract rate figures that are competitively sensitive before ingesting into a shared knowledge base. The knowledge base is for methodology and reference information, not live negotiated rate data.

---

### Step 1: Navigate to Knowledge Bases

```
Screenshot Placeholder:
Filename: kb-nav-01.png
Capture: Amazon Bedrock → Builder tools → Knowledge bases → "Create knowledge base" button
Highlight: Left navigation "Knowledge bases" item, "Create knowledge base" orange button
Annotation Notes:
  - Arrow to "Knowledge bases" in left nav
  - Circle "Create knowledge base" button
  - Note: Any existing knowledge bases would appear in the list with status indicators
```

**On Screen You Should See:**
- "Knowledge bases" header
- "Create knowledge base" button (top right)
- Empty list (or existing KBs) with columns: Name, Status, Last sync time, Data source count

---

### Step 2: Configure Knowledge Base

```
Screenshot Placeholder:
Filename: kb-create-01.png
Capture: Create knowledge base form — Step 1: Name and IAM role configuration
Highlight: Knowledge base name field, "Create and use a new service role" option, description field
Annotation Notes:
  - Box around name field: "financial-analytics-kb"
  - Arrow to IAM role section with note: "Use pre-created role for production"
  - Note on description: "Describe content type — agents use this to decide when to query this KB"
```

**On Screen You Should See:**
- Step 1 of create flow: "Knowledge base details"
- Knowledge base name (required)
- Description (important — used by agent to decide when to query this KB)
- IAM role selection
- Tags (optional)

**Knowledge base name best practices:**
- Include content type: `financial-analytics-kb`, `payer-contracts-kb`, `cms-rate-methodology-kb`
- Include environment: `financial-analytics-kb-prod`
- Use hyphens, not underscores (Bedrock naming convention)

**Description for agent routing:**
The description you write here is what the Bedrock Agent reads to decide whether to query this knowledge base. Write it like a tool description — specify exactly what information is in this KB and when it should be used.

```
This knowledge base contains CMS rate-setting methodology documentation, coding reference
materials (MS-DRG, CPT, ICD-10), payer contract methodology summaries, and market rate
intelligence reports. Query this knowledge base when you need to understand how rates are
calculated, interpret contract escalation terms, look up code definitions, or benchmark
against market reimbursement trends. Do NOT query for live negotiated rate data — use the
get_negotiated_rates tool for that.
```

---

### Step 3: Configure Data Source

```
Screenshot Placeholder:
Filename: kb-datasource-01.png
Capture: Create knowledge base — Data source configuration step, showing S3 bucket selection
Highlight: S3 URI field, "Add data source" button, sync frequency options
Annotation Notes:
  - Box around S3 URI field with example: s3://org-financial-analytics-kb/
  - Arrow to "Add data source" button
  - Note: Multiple data sources from different S3 locations are supported
  - Warning box: "Ensure S3 bucket and KB are in the same AWS region"
```

**On Screen You Should See:**
- Data source type selection: "Amazon S3" (primary option), "Web crawler" (beta), others
- S3 URI field (s3://bucket-name/optional-prefix/)
- Data source name
- Content chunking configuration (critical — see next section)
- Metadata and filtering configuration

**S3 Bucket Structure Recommendation:**

```
s3://org-financial-analytics-kb/
├── cms-rate-transparency/
│   ├── cms-ipps-final-rule-2026.pdf
│   ├── cms-opps-final-rule-2026.pdf
│   └── cms-mrf-methodology-guide.pdf
├── coding-references/
│   ├── ms-drg-v42-definitions-manual.pdf
│   ├── cpt-2026-code-descriptors.txt
│   └── cci-edit-table-2026.csv
├── payer-contracts/
│   ├── bcbs-contract-methodology-summary.pdf
│   └── aetna-rate-schedule-2026.pdf
└── market-intelligence/
    ├── hfma-rate-trend-report-2025.pdf
    └── mgma-physician-comp-survey-2025.pdf
```

**Metadata file pattern:** For each document, create a companion `.metadata.json` file to enable filtered retrieval:

```json
{
  "metadataAttributes": {
    "data_category": "cms_rate_transparency",
    "payer": "all",
    "effective_year": "2026",
    "is_current": "true",
    "document_type": "regulatory"
  }
}
```

Filename must match: `cms-ipps-final-rule-2026.pdf.metadata.json`

This metadata enables filtered queries: "Search only CMS rate transparency documents effective in 2026 or later."

---

### Step 4: Chunking Strategy Configuration

**This is the most impactful configuration decision in knowledge base design.**

Chunking is how Bedrock splits your documents into pieces for embedding. The chunk size and overlap affect:
- Retrieval accuracy (how precisely the right content is retrieved)
- Context completeness (whether retrieved chunks contain enough context to be useful)
- Storage cost (smaller chunks = more chunks = more vectors stored)
- Query cost (more precise retrieval = fewer irrelevant chunks returned)

```
Screenshot Placeholder:
Filename: kb-chunking-01.png
Capture: Knowledge base data source configuration — chunking section showing all options
Highlight: Chunking strategy dropdown, chunk size slider, chunk overlap slider
Annotation Notes:
  - Box around chunking strategy dropdown showing: "Default", "Fixed size", "Hierarchical", "Semantic", "None"
  - Arrow to chunk size field (tokens)
  - Arrow to chunk overlap field
  - Recommendation annotation: "Start with 'Fixed size' 512 tokens, 20% overlap for regulatory and contract documents"
```

**On Screen You Should See:**
- Chunking strategy options:
  - **Default:** Bedrock decides (similar to Fixed size, 300 tokens)
  - **Fixed size:** You specify token count and overlap
  - **Hierarchical:** Creates parent and child chunks for multi-level retrieval
  - **Semantic:** Uses NLP to find semantically coherent break points
  - **None:** No chunking — each document is one chunk (only for very short documents)
- Chunk size (tokens): typically 256-1024
- Chunk overlap (tokens or percentage): typically 10-25%

**Chunking strategy selection for financial analytics documents:**

| Document Type | Recommended Strategy | Chunk Size | Rationale |
|--------------|---------------------|------------|-----------|
| IPPS final rules (long PDFs) | Fixed size | 512 tokens | Balances completeness and precision |
| MS-DRG definitions manual | Hierarchical | 256 child / 1024 parent | DRG manuals have clear section structure |
| Payer contract methodology summaries | Semantic | Auto | Contract language has semantic structure |
| CCI edit tables / DRG weight tables | Fixed size | 256 tokens | Tables need small chunks for precise retrieval |
| Rate escalation methodology docs | Hierarchical | 512/2048 | Methodology docs have logical steps structure |

**Fixed-size chunking configuration for regulatory documents:**
- Chunk size: 512 tokens (~380 words)
- Chunk overlap: 100 tokens (~75 words, ~20%)

The overlap ensures that information at a chunk boundary is not split — context from the end of one chunk carries into the start of the next, so the retrieval system can find the complete thought.

---

### Step 5: Embedding Model Selection

```
Screenshot Placeholder:
Filename: kb-embedding-01.png
Capture: Knowledge base configuration — Embeddings model section
Highlight: Embedding model dropdown with Titan Embeddings V2 selected, dimension field
Annotation Notes:
  - Box around "Amazon Titan Embeddings Text V2" selection
  - Arrow to "Dimensions" field set to 1024
  - Note: "Higher dimensions = better accuracy but more storage cost"
  - Arrow to OpenSearch collection configuration below
```

**On Screen You Should See:**
- Embedding model dropdown: Amazon Titan Embeddings V2 (recommended), Cohere Embed English v3, Cohere Embed Multilingual v3
- Embedding dimensions: 256, 512, 1024 (for Titan V2)
- Vector store selection: Amazon OpenSearch Serverless, Amazon Aurora (pgvector), Pinecone, MongoDB Atlas, Redis Enterprise

**Embedding model selection:**
- **Titan Embeddings Text V2:** Default choice. Native AWS, HIPAA-eligible, no data egress outside AWS, 1024 dimensions (strong quality), lower cost than alternatives. Recommended for most healthcare use cases.
- **Cohere Embed Multilingual:** If your documents include non-English content (Spanish patient education materials, international clinical guidelines).
- **Cohere Embed English:** Higher accuracy for English content but with external API calls (data leaves AWS — verify BAA coverage).

**Dimension selection for Titan V2:**
- 1024 dimensions: Best accuracy, highest storage cost (1024 floats × 4 bytes = 4KB per chunk)
- 512 dimensions: Good accuracy, moderate cost
- 256 dimensions: Lower accuracy, lowest cost

For healthcare financial analytics content: use 1024 dimensions. The accuracy improvement is worth the modest storage cost increase.

---

### Step 6: Vector Store Configuration

```
Screenshot Placeholder:
Filename: kb-vectorstore-01.png
Capture: Knowledge base — Vector store selection and configuration, with OpenSearch Serverless highlighted
Highlight: "Amazon OpenSearch Serverless" option selected, "Create new collection" vs "Select existing" radio
Annotation Notes:
  - Circle "Amazon OpenSearch Serverless" as the recommended selection
  - Box around "Quick create new vector store" option
  - Note: "Quick create is fine for development; for production, pre-create the collection"
  - Arrow to estimated cost information
```

**Amazon OpenSearch Serverless for Knowledge Bases:**

OpenSearch Serverless is the recommended vector store for Bedrock Knowledge Bases because:
1. Fully managed — no cluster sizing or maintenance
2. HIPAA-eligible
3. Native AWS integration — no credentials to manage
4. Scales automatically with query volume

**Cost model for OpenSearch Serverless:**
- OCU (OpenSearch Capacity Units) charged per hour: ~$0.24/OCU-hour
- Minimum: 0.5 OCU for indexing + 0.5 OCU for search = 1 OCU minimum
- **Monthly baseline cost for a single knowledge base: ~$175/month** (24/7 × 2 OCUs × $0.24)
- This is a significant fixed cost — factor into project budgeting
- For development: create the collection only when testing, delete when not in use

---

### Step 7: Review and Create

Before clicking Create, review:
- Knowledge base name and description
- Data source (S3 path)
- Chunking strategy and parameters
- Embedding model and dimensions
- Vector store

Click "Create knowledge base."

**What happens during creation:**
- OpenSearch Serverless collection created (if new)
- Vector index created in the collection
- Knowledge base metadata stored in Bedrock control plane
- No documents are processed yet — that happens on sync

---

### The Sync Process

```
Screenshot Placeholder:
Filename: kb-sync-status-01.png
Capture: Knowledge base detail page → Data sources → "Sync" button → showing In Progress status
Highlight: Sync button, status indicator (In Sync / Complete / Failed), document count, last sync time
Annotation Notes:
  - Circle "Sync" button
  - Arrow to status showing "In sync" with spinning indicator
  - Box around statistics: Total documents, Total chunks created, Failed documents
  - Note: "First sync can take minutes to hours depending on document count and size"
```

**On Screen You Should See:**
- Data sources list with sync status columns
- "Sync now" button
- Status options: "Complete" (green), "In sync" (blue, spinning), "Failed" (red), "Never synced" (gray)
- Statistics after sync: Documents processed, Chunks created, Errors

---

### What Happens When You Click Sync

This is architecturally important to understand.

When you initiate a sync, Bedrock:

**Step 1: Document Discovery**
Scans the S3 location (and subdirectories). Identifies documents that are new since the last sync (by comparing ETags/modification timestamps). Identifies documents that have been deleted from S3.

**Step 2: Document Loading**
For each new/changed document:
- Downloads the document from S3
- Parses the format (PDF text extraction, Word document parsing, HTML stripping)
- Extracts document text and any companion metadata JSON

**Step 3: Chunking**
Applies your chunking configuration to split the document into chunks. Each chunk retains metadata about its source document, page number, and position.

**Step 4: Embedding Generation**
For each chunk, calls the Titan Embeddings V2 API:
- Input: chunk text
- Output: 1,024-dimensional vector representation
- Cost: charged per 1K tokens embedded

**Step 5: Vector Indexing**
Writes each (vector, text, metadata) triple to OpenSearch Serverless. This creates the searchable index.

**Step 6: Deletion Handling**
For documents deleted from S3 since last sync: removes their vectors from the index.

**Storage cost implications:**
A 500-page IPPS final rule document:
- ~500 × 300 words/page × 1.3 tokens/word ≈ 195,000 tokens of content
- At 512 tokens per chunk ≈ 380 chunks
- At 1,024 dimensions × 4 bytes/float ≈ 4KB per vector
- Total vector storage: 380 × 4KB ≈ 1.5MB per document
- For 200 documents: ~300MB of vector storage
- OpenSearch storage: ~$0.11/GB-month → ~$0.033/month for 300MB (negligible)
- Sync (embedding) cost: 195K tokens × 200 documents / 1M × $0.10 ≈ $3.90 per full sync

---

## Chapter 5.3 — Retrieval Evaluation

### Measuring RAG Performance

Your knowledge base can fail in two ways:

**Precision failure:** The knowledge base retrieves chunks that are not relevant to the query. The agent's context gets polluted with irrelevant information.

**Recall failure:** The knowledge base fails to retrieve chunks that are relevant to the query. The agent doesn't have the information it needs.

**Standard RAG metrics:**

| Metric | Formula | Target |
|--------|---------|--------|
| Precision@K | Relevant retrieved / K retrieved | > 0.75 |
| Recall@K | Relevant retrieved / Total relevant | > 0.85 |
| MRR (Mean Reciprocal Rank) | Mean of 1/rank_of_first_relevant | > 0.80 |
| NDCG (Normalized Discounted Cumulative Gain) | Graded relevance measure | > 0.80 |

**Building a retrieval evaluation set:**

```python
# Evaluation set example
retrieval_test_cases = [
    {
        "query": "What is the MS-DRG relative weight for DRG 470 (Major Joint Replacement) under the CMS IPPS 2026 final rule?",
        "expected_docs": [
            "cms-ipps-final-rule-2026.pdf",  # Must be retrieved
        ],
        "expected_content_keywords": [
            "DRG 470", "relative weight", "major joint replacement", "IPPS", "wage index"
        ],
        "anti_expected_docs": [
            "cms-opps-final-rule-2026.pdf",  # Should NOT be retrieved for this inpatient query
        ]
    },
    # ... more cases
]

def evaluate_retrieval(kb_id: str, test_cases: list) -> dict:
    bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')

    precision_scores = []
    recall_scores = []

    for case in test_cases:
        # Retrieve from KB
        response = bedrock_agent_runtime.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={'text': case['query']},
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': 5
                }
            }
        )

        retrieved_docs = set(
            result['location']['s3Location']['uri'].split('/')[-1]
            for result in response['retrievalResults']
        )

        expected_docs = set(case['expected_docs'])
        anti_expected = set(case.get('anti_expected_docs', []))

        # Calculate precision (relevant / retrieved)
        relevant_retrieved = retrieved_docs & expected_docs
        unwanted_retrieved = retrieved_docs & anti_expected

        precision = len(relevant_retrieved) / len(retrieved_docs) if retrieved_docs else 0
        recall = len(relevant_retrieved) / len(expected_docs) if expected_docs else 0

        precision_scores.append(precision)
        recall_scores.append(recall)

        if unwanted_retrieved:
            print(f"WARNING: Anti-expected docs retrieved: {unwanted_retrieved}")

    return {
        'mean_precision': sum(precision_scores) / len(precision_scores),
        'mean_recall': sum(recall_scores) / len(recall_scores),
        'num_cases': len(test_cases)
    }
```

---

## Chapter 5.4 — Advanced Knowledge Base Patterns

### Metadata Filtering

Metadata filtering allows the agent to constrain knowledge base retrieval to specific subsets of the document corpus. This is critical for:
- Multi-payer agents (return only BCBS contract methodology when processing a BCBS analysis)
- Multi-year agents (return only 2026 rate data, not 2025)
- Versioned content (return only current-year DRG weight tables, not prior-year)
- Hybrid knowledge bases (both regulatory and contract content in one KB)

**Programmatic retrieval with metadata filter:**

```python
def retrieve_with_filter(
    kb_id: str,
    query: str,
    specialty: str = None,
    payer_id: str = None,
    year_min: int = None
) -> list:

    retrieval_filter = {"andAll": []}

    if specialty:
        retrieval_filter["andAll"].append({
            "equals": {
                "key": "specialty",
                "value": specialty
            }
        })

    if payer_id:
        retrieval_filter["andAll"].append({
            "in": {
                "key": "applies_to_payers",
                "value": [payer_id, "all"]
            }
        })

    if year_min:
        retrieval_filter["andAll"].append({
            "greaterThanOrEquals": {
                "key": "publication_year",
                "value": str(year_min)
            }
        })

    # If no filters, remove the empty andAll
    if not retrieval_filter["andAll"]:
        retrieval_filter = {}

    bedrock_runtime = boto3.client('bedrock-agent-runtime')

    request = {
        'knowledgeBaseId': kb_id,
        'retrievalQuery': {'text': query},
        'retrievalConfiguration': {
            'vectorSearchConfiguration': {
                'numberOfResults': 5,
            }
        }
    }

    if retrieval_filter:
        request['retrievalConfiguration']['vectorSearchConfiguration']['filter'] = retrieval_filter

    response = bedrock_runtime.retrieve(**request)
    return response['retrievalResults']
```

---

### Hybrid Retrieval: Semantic + Keyword Search

By default, Bedrock Knowledge Bases uses pure vector (semantic) search. For financial analytics content, a hybrid approach — combining semantic similarity with keyword matching — often outperforms pure semantic search.

**When keyword matching is important in healthcare financial analytics:**
- Specific DRG codes: "DRG 470" must match "DRG 470" (not just "joint replacement")
- CPT codes: "27447" must match exactly
- ICD codes: "M06.9" must match exactly
- Payer names: "Aetna" must retrieve Aetna-specific contract terms

**Bedrock Knowledge Bases supports hybrid retrieval** as a configurable option that combines vector similarity with BM25 keyword matching in OpenSearch.

Enable in the retrieval configuration:
```python
'vectorSearchConfiguration': {
    'numberOfResults': 5,
    'overrideSearchType': 'HYBRID'  # 'SEMANTIC' (default) or 'HYBRID'
}
```

---

### Financial Data Compliance Considerations for Knowledge Bases

**1. Proprietary payer contract terms must be access-controlled.**
The knowledge base may contain commercially sensitive payer contract rate methodologies, escalation terms, and carve-out provisions. Ingesting detailed negotiated rate figures into a broadly accessible knowledge base could expose competitive intelligence. Implement S3 bucket policies to restrict which agents and users can query contract-specific content.

**2. Document currency is a financial accuracy issue.**
If a payer contract summary or DRG weight table in your knowledge base is outdated, the agent may retrieve and cite superseded rate information that leads to incorrect financial projections. Implement:
- Annual sync schedule aligned with CMS rule publication cycles (typically October)
- Metadata field for "effective_year" and "is_current" flag
- Pre-sync review process to validate new documents before ingestion
- Monitoring to alert when documents approach contract renewal or CMS update dates

**3. Source attribution is mandatory.**
When the agent provides rate methodology or coding information from the knowledge base, it must attribute the source. Configure your agent's system prompt to always cite the source document when making claims from retrieved content. Bedrock Knowledge Bases automatically includes source URIs in retrieval results — extract and surface these in agent responses.

**4. Separation of rate methodology from live rate data.**
The knowledge base is appropriate for rate methodology documentation, coding references, and contract term descriptions. It is not appropriate for live negotiated rate lookups — those belong in a structured data tool (`get_negotiated_rates`). Mixing methodology documentation with live rate data creates confusion about data freshness and authority. Keep these concerns separate: KB for methodology context, tools for live data.

---

## Chapter 5.5 — Lab: Building a Financial Analytics Knowledge Base

### Lab Objective

Build a functioning financial analytics knowledge base using publicly available CMS documentation and connect it to a Bedrock Agent. Test retrieval quality and evaluate grounding.

### Lab Steps

**Part 1: Document Preparation**

1. Download publicly available CMS documentation (no proprietary data required):
   - CMS IPPS Final Rule for the current fiscal year (available on cms.gov)
   - MS-DRG Definitions Manual (publicly available from CMS)
   - CPT code descriptor files (available via AMA or CMS crosswalk files)

2. Create metadata companion files for each document

3. Upload documents and metadata to S3

4. Verify S3 structure:
   ```
   aws s3 ls s3://your-kb-bucket/ --recursive
   ```

**Part 2: Knowledge Base Creation**

Complete the console walkthrough from Chapter 5.2:
1. Create knowledge base with descriptive name
2. Configure S3 data source
3. Set chunking: Fixed size, 512 tokens, 100 token overlap
4. Select Titan Embeddings V2, 1024 dimensions
5. Create OpenSearch Serverless collection (Quick create)
6. Initiate first sync

**Part 3: Retrieval Testing**

Use the Bedrock Knowledge Base test console to evaluate retrieval:

```
Screenshot Placeholder:
Filename: kb-test-console-01.png
Capture: Knowledge base detail page → "Test knowledge base" section → query input and results
Highlight: Query input field, "Run" button, retrieval results with relevance scores, source citations
Annotation Notes:
  - Box around query field with example query
  - Arrow to "Number of results" setting
  - Box around first result showing: Score, Text excerpt, Source document name and page
  - Note: "Compare results with different chunk sizes by testing the same queries"
```

Test queries to evaluate:
1. "What is the MS-DRG relative weight for DRG 470 (Major Joint Replacement) under the CMS IPPS 2026 final rule?"
2. "How does CMS calculate the blended payment rate for outlier cases under IPPS?"
3. "What are the common contract escalation methodologies used by commercial payers for hospital inpatient services?"

For each query, evaluate:
- Was the relevant document retrieved?
- Was the relevant passage (not just the document) retrieved?
- Would this passage be sufficient for an agent to answer the question accurately?

**Part 4: Agent Integration**

1. Create a Bedrock Agent with system prompt focused on financial analytics and rate methodology lookup
2. Attach the knowledge base to the agent
3. Test with financial analytics questions
4. Enable trace to verify the agent is actually querying the KB (not answering from model knowledge)
5. Check: does the agent cite the source document?

---

## Module 5 Reflection Prompts

1. Your financial analytics knowledge base has 150 documents covering CMS rate methodology, MS-DRG references, and payer contract summaries. A financial analyst asks about the MS-DRG relative weight for a rare, low-volume procedure and the agent answers confidently with information that sounds reasonable but is incorrect. The knowledge base doesn't contain documents that cover this specific DRG. What failed? How do you design the agent to handle gaps in the knowledge base gracefully — for example, by falling back to the `get_negotiated_rates` tool or clearly communicating that the rate could not be verified?

2. You are choosing between chunking strategies: Fixed size (512 tokens) vs. Semantic. For payer contract documents that describe multi-clause escalation methodologies with cross-references between sections, which strategy would you choose and why? How would you evaluate whether your choice correctly preserves the relationships between escalation trigger clauses and the corresponding rate adjustment formulas?

3. Your organization wants to use the knowledge base for both CMS rate methodology documentation AND proprietary payer contract term summaries. Should these be in the same knowledge base or separate knowledge bases? Consider: access control requirements, metadata filtering complexity, the risk that a query about "BCBS reimbursement methodology" retrieves both public CMS guidance and confidential BCBS contract language, and what the agent description would need to say to route correctly.

4. A finance director asks: "How do we know the contract rate schedules and DRG weight tables in the knowledge base are current?" Design a document currency monitoring and management process for a financial analytics knowledge base — including how you would detect when a new CMS IPPS final rule has been published, validate the new document, update the S3 source, trigger a sync, and confirm the old rule's chunks have been replaced.

5. The Bedrock Knowledge Base sync fails with "400 errors" on 15 of your documents — several of which are large MRF JSON files you converted to CSV excerpts. What are the most common causes of sync failures for large, structured financial data files? How do you diagnose which documents failed, whether the issue is file size, encoding, unsupported characters in rate data, or malformed metadata JSON, and what preprocessing steps would prevent these failures on the next sync?

---

*End of Module 5 Textbook Content*
