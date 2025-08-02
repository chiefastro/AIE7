# AIE7 Certification Challenge Report

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
- **Default:** Custom chunker that leverages structure of markdown. Separates paragraphs, bullet points, rows of tables but keeps headings for each (contextual retrieval)
- **Rationale:** The blog article is short and dense (short paragraphs, bullets, and tables). Naive chunkers might mix multiple mental models together into one chunk.


# Notes
I want to redesign this agent. The supervisor that delegates to 3 subagents, each of whom has 1 tool, is more complex and less effective than a simpler single agent with access to 3 tools because that simple agent can do it's own planning, delegation, and synthesis while the supervisor design can only delegate with no planning and synthesis.