# Design Document

## Overview

The AI Mental Models Advisor is a multi-agent RAG system built using LangGraph that helps users apply mental models from the Intelligence Age to their business strategy questions. The system employs a supervisor agent pattern to coordinate three specialized subagents, each responsible for different information sources. The architecture leverages proven patterns from the notebooks, particularly the hierarchical agent teams approach and advanced retrieval techniques.

## Architecture

### High-Level Architecture

The system follows a hierarchical multi-agent architecture with:

1. **Supervisor Agent**: Routes queries and coordinates subagents based on query analysis
2. **Vector RAG Subagent**: Retrieves and processes mental models from the chunked blog article
3. **Web Search Subagent**: Performs real-time web searches using Tavily API
4. **Academic Search Subagent**: Searches academic papers using Arxiv API
5. **Response Synthesizer**: Combines outputs from multiple subagents into coherent responses

### Technology Stack

- **LLM**: OpenAI GPT-4.1-nano (cost-effective, strong reasoning)
- **Embedding Model**: OpenAI text-embedding-3-small (high-quality, LangChain integration)
- **Orchestration**: LangGraph + LangChain (flexible multi-agent workflows)
- **Vector Database**: Qdrant (fast, open-source, in-memory for prototype)
- **Web Search**: Tavily API (optimized for LLM applications)
- **Academic Search**: Arxiv API (free access to academic papers)
- **Monitoring**: LangSmith (run tracking, debugging)
- **Evaluation**: RAGAS (RAG-specific metrics)
- **Frontend**: CopilotKit (industry-standard chat interface)

## Components and Interfaces

### 1. Document Processing Pipeline

**Purpose**: Process and chunk the mental models blog article for optimal retrieval

**Components**:
- Custom Markdown Chunker: Preserves structure (headings, bullets, tables)
- Contextual Retrieval: Maintains heading context for each chunk
- Embedding Generation: Creates vector representations using OpenAI embeddings

**Interface**:
```python
class DocumentProcessor:
    def chunk_markdown(self, content: str) -> List[Document]
    def embed_chunks(self, chunks: List[Document]) -> VectorStore
```

### 2. Supervisor Agent

**Purpose**: Analyze queries and route to appropriate subagents

**Decision Logic**:
- Mental models queries → Vector RAG Subagent
- Current events/market info → Web Search Subagent  
- Academic context needed → Arxiv Search Subagent
- Complex queries → Multiple subagents

**Interface**:
```python
class SupervisorAgent:
    def analyze_query(self, query: str) -> AgentRoutingDecision
    def coordinate_subagents(self, routing: AgentRoutingDecision) -> Response
```

### 3. Vector RAG Subagent

**Purpose**: Retrieve and process mental models content

**Components**:
- Advanced Retrieval: Ensemble retrieval (semantic + BM25)
- Contextual Compression: Cohere reranking for relevance
- Mental Model Extraction: Identify and explain applicable models

**Interface**:
```python
class VectorRAGSubagent:
    def retrieve_mental_models(self, query: str) -> List[Document]
    def extract_applicable_models(self, docs: List[Document]) -> List[MentalModel]
```

### 4. Web Search Subagent

**Purpose**: Gather current information using Tavily API

**Components**:
- Query Optimization: Transform user queries for web search
- Result Processing: Extract relevant information from web results
- Source Attribution: Track and cite web sources

**Interface**:
```python
class WebSearchSubagent:
    def search_web(self, query: str) -> List[WebResult]
    def process_results(self, results: List[WebResult]) -> ProcessedWebInfo
```

### 5. Academic Search Subagent

**Purpose**: Find relevant academic papers using Arxiv API

**Components**:
- Query Translation: Convert business queries to academic search terms
- Paper Processing: Extract abstracts and key findings
- Relevance Filtering: Select most applicable research

**Interface**:
```python
class AcademicSearchSubagent:
    def search_arxiv(self, query: str) -> List[ArxivPaper]
    def extract_insights(self, papers: List[ArxivPaper]) -> AcademicInsights
```

### 6. Response Synthesizer

**Purpose**: Combine multi-source information into coherent responses

**Components**:
- Information Integration: Merge insights from multiple subagents
- Mental Model Application: Connect findings to relevant frameworks
- Follow-up Generation: Suggest related questions and models

**Interface**:
```python
class ResponseSynthesizer:
    def synthesize_response(self, multi_source_data: MultiSourceData) -> FinalResponse
    def generate_followups(self, response: FinalResponse) -> List[FollowUpQuestion]
```

## Data Models

### Core Data Structures

```python
@dataclass
class MentalModel:
    name: str
    description: str
    application_context: str
    source_chunk: Document

@dataclass
class AgentRoutingDecision:
    use_vector_rag: bool
    use_web_search: bool
    use_academic_search: bool
    reasoning: str

@dataclass
class MultiSourceData:
    mental_models: List[MentalModel]
    web_insights: Optional[ProcessedWebInfo]
    academic_insights: Optional[AcademicInsights]
    
@dataclass
class FinalResponse:
    answer: str
    mental_models_used: List[str]
    sources: List[str]
    follow_up_questions: List[str]
```

### LangGraph State Schema

```python
class ConversationState(TypedDict):
    query: str
    conversation_history: List[Dict]
    routing_decision: AgentRoutingDecision
    vector_results: Optional[List[Document]]
    web_results: Optional[ProcessedWebInfo]
    academic_results: Optional[AcademicInsights]
    final_response: Optional[FinalResponse]
```

## Testing Strategy

### Evaluation Framework
- **RAGAS Metrics**: Faithfulness, response relevance, context precision, context recall
- **Mental Model Application**: Custom metrics for framework usage accuracy
- **User Experience**: Response quality and follow-up question relevance
- **Performance**: Response time and resource utilization

### Test Data Strategy
- **Golden Dataset**: Curated business strategy questions with expected mental model applications
- **Synthetic Data**: Generated using LLM to cover edge cases
- **Real User Queries**: Collected during beta testing for continuous improvement

## Deployment Architecture

### Local Development
- In-memory Qdrant for rapid iteration
- Environment-based configuration
- Hot-reloading for development efficiency