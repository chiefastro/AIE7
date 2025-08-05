# AIE7 Certification Challenge Report

## 0. Loom Video!
https://www.loom.com/share/f8065c23db3643d2a36b805f1258fb7e?sid=92aa90dc-6c1c-4543-ba12-a72238645123

## 1. Problem, Audience, and Solution

### Problem Statement (1 sentence)
Product managers and business strategists struggle to frame effective questions and strategies for the AI era, lacking actionable mental models tailored to the Intelligence Age.

### Why is this a problem for your user?
Product managers and business strategists are inundated with rapid AI advancements, making it difficult to distinguish between hype and actionable opportunities. Without clear frameworks, they risk making poor investment decisions, missing disruptive trends, or building products that are quickly commoditized by AI platforms. The lack of accessible, AI-native mental models leads to confusion, wasted resources, and missed opportunities for competitive advantage.

### Audience
- **Primary:** Product managers, business strategists, and innovation leads at tech-forward companies.
- **Secondary:** Founders, C-suite executives, and consultants navigating AI transformation.

## 2. Proposed Solution

### Solution Overview
Build an agentic RAG application that helps users frame and answer product management and business strategy questions using mental models from the provided blog article. The system uses a supervisor agent to route queries to three subagents:
- A vector DB retriever (for the blog's mental models)
- A Tavily web search agent (for up-to-date info)
- An Arxiv search agent (for academic context)

The prompts are designed to encourage users to ask questions in a way that leverages these mental models, helping them make better decisions in the Intelligence Age.

### User Experience
1. User enters a business/product strategy question.
2. The supervisor agent decides which subagent(s) to use.
3. The system returns a synthesized answer, referencing relevant mental models and optionally supplementing with web/academic sources.

### Tooling Choices

| Stack Component   | Tool/Service         | Rationale |
|-------------------|---------------------|-----------|
| LLM               | OpenAI gpt-4.1       | Strong reasoning, broad knowledge, API support |
| Embedding Model   | OpenAI Embeddings   | High-quality, easy integration with LangChain |
| Orchestration     | LangChain + LangGraph | Flexible agentic workflows, easy multi-agent setup |
| Vector Database   | Qdrant    | Fast, open-source, integrates with LangChain |
| Monitoring        | LangSmith           | Tracks runs, debugging, and evaluation |
| Evaluation        | RAGAS               | Standard for RAG pipeline evaluation |
| UI                | CopilotKit    | Becoming the industry-standard in chat interfaces, simplifies communication between frontend and backend |
| Serving           | Localhost           | Simplicity for prototype phase |

### Where are agents used?
- **Supervisor agent:** routes queries.
- **Subagents:** vector DB retriever, Tavily search, Arxiv search.
- **Agentic reasoning:** Used to decide which tool(s) to use for each user query.

## 3. Data & Chunking

### Data Sources & APIs
- **Primary:** `data/Mental-Models-for-the-Intelligence-Age-Skillenai.md` (chunked and embedded in vector DB)
- **External APIs:** Tavily (web search), Arxiv (academic search)

### Chunking Strategy
- **Naive:** Use the basic recursive text splitter as a baseline.
- **Markdown:** Custom chunker that leverages structure of markdown. Separates paragraphs, bullet points, rows of tables but keeps headings for each (contextual retrieval)
- **Rationale:** The blog article is short and dense (short paragraphs, bullets, and tables). Naive chunkers might mix multiple mental models together into one chunk.

## 4. End-to-End Prototype

### Implementation Status
✅ **Completed:** Built and deployed an end-to-end agentic RAG application to localhost endpoint using the architecture described above.

### Technical Implementation
- Backend: FastAPI with LangChain/LangGraph for agent orchestration
- Frontend: Next.js with CopilotKit for chat interface
- Vector Database: Qdrant with OpenAI embeddings
- External APIs: Tavily for web search, Arxiv for academic papers
- Monitoring: LangSmith integration for debugging and evaluation
- Evaluation: RAGAS for measuring retrieval performance and experimentation

## 5. Golden Test Data Set & RAGAS Evaluation

### Golden Dataset
I used RAGAS synthetic data generation to produce 63 labeled examples related to my data set.

### RAGAS Framework Assessment
I evaluated the pipeline using the RAGAS framework with four key metrics: faithfulness, response relevance, context precision, and context recall. The evaluation compared four different configurations:

| Configuration | Context Recall | Faithfulness | Factual Correctness | Answer Relevancy |
|---------------|----------------|--------------|-------------------|------------------|
| markdown_chunker_cosine | 0.714 | 0.880 | 0.636 | 0.903 |
| markdown_chunker_multi_query | 0.743 | 0.919 | 0.668 | 0.936 |
| naive_chunker_cosine | 0.968 | 0.951 | 0.755 | 0.938 |
| naive_chunker_multi_query | 0.990 | 0.958 | 0.766 | 0.915 |

### Performance Analysis
The results reveal several key insights:

1. **Naive chunking significantly outperforms custom markdown chunking** across all metrics
2. **Multi-query retrieval improves performance** when combined with naive chunking
3. **Context recall is the most sensitive metric** to chunking strategy differences
4. **The best overall performer is naive_chunker_multi_query** with the highest scores in context recall (0.990), faithfulness (0.958), and factual correctness (0.766)

### Conclusions
The evaluation demonstrates that simpler chunking strategies can outperform more sophisticated approaches. The naive chunker's superior performance suggests that larger chunks with more context are more effective than smaller, more granular chunks for this particular content. This challenges the initial hypothesis that custom markdown-aware chunking would be beneficial for the dense, structured content of the mental models article.

## 6. Advanced Retrieval Techniques

### Planned Retrieval Techniques
1. **Baseline (Dense Vectors with Cosine)** - Standard vector-based retrieval using cosine similarity for ranking
2. **Multi-query retrieval** - Generates multiple search queries from the original question to improve recall

### Rationale for Each Technique
- **Multi-query retrieval:** Will help capture different aspects of complex business strategy questions that may require multiple mental models

### Implementation Results
The experimental results show that **multi-query retrieval slightly improves performance** when combined with naive chunking:
- Context recall improved from 0.968 to 0.990
- Faithfulness improved from 0.951 to 0.958
- Factual correctness improved from 0.755 to 0.766

However, multi-query retrieval with markdown chunking showed more modest improvements, suggesting that the chunking strategy is the primary factor in performance.

## 7. Performance Assessment & Future Improvements

### Comparative Performance Analysis
The comprehensive evaluation across all metrics (quality, latency, and cost) reveals:

| Configuration | Quality Rank | Cost/Latency Rank | Overall Rank |
|---------------|--------------|-------------------|--------------|
| naive_chunker_multi_query | 1.50 | 2.75 | 2.125 |
| markdown_chunker_multi_query | 2.75 | 2.00 | 2.375 |
| markdown_chunker_cosine | 4.00 | 1.50 | 2.750 |
| naive_chunker_cosine | 1.75 | 3.75 | 2.750 |

### Key Findings
1. **naive_chunker_multi_query is the optimal configuration** with the best overall balance of quality, latency, and cost
2. **Advanced retrieval (multi-query) provides slight quality improvements** without substantial cost increases
3. **Chunking strategy has a larger impact than retrieval method** on overall performance
4. **There's a clear trade-off between quality and efficiency** - the highest quality configurations have higher latency and cost

### Quantified Improvements
Compared to the baseline naive_chunker_cosine:
- **Context recall improved by 2.2%** (0.968 → 0.990)
- **Faithfulness improved by 0.7%** (0.951 → 0.958)
- **Factual correctness improved by 1.4%** (0.755 → 0.766)
- **Answer relevancy decreased by 2.5%** (0.938 → 0.915)

**Key insight:** Only the multi-query retrieval improvement yielded meaningful gains, while the markdown chunking approach actually degraded performance compared to naive chunking.

### Future Application Improvements
The toy example implemented here has a long way to go before being helpful for a real-world use case. I'm considering two paths forward.

#### Use Cases
1. Expand the dataset to cover my entire blog site, maybe create a Wordpress plugin that others can use to add a chat interface to their blogs that does RAG on their own content.
2. Double down on the use case of helping PMs and strategists generate, test, and refine ideas for AI adoption. I'd like to implement a browser extension that allows PMs to operate across multiple tabs to do research, write PRDs, generate vibe-coded prototypes, solicit feedback, and generate presentations. This browser extension would be a layer on top of tools like JIRA, Confluence, Lovable, Discord, and Gamma.

#### Agent Design
I'd also like to redesign the agent. I started with a supervisor agent that delegates to 3 subagents, each of whom had 1 tool (this was a pattern used in the notebook from session 6). But this is more complex and less effective than a simpler single agent with access to 3 tools because that simple agent can do it's own planning, delegation, and synthesis (while the supervisor design can only delegate with no planning and synthesis). I already implemented this simpler agent design (that's the "multi_tasker" agent used in my main app), but I'd like to take it even further by converting the RAG subagent (which is currently called as a tool) into just a retrieval tool that is called by the main agent. 

#### Evaluation
I'd like to measure performance of the agent end-to-end instead of only evaluating the RAG subagent. I made some attempts to instrument an experimentation framework that would allow experiments to be run on the overall agent design, but I ran out of time. Work remains to set up the proper state management needed to pass context from the various tools to the RAGAS evaluators.