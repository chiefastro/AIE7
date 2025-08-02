# Implementation Plan

- [ ] 1. Set up project structure and core interfaces
  - Create directory structure for agents, models, services, and utilities
  - Define TypedDict state schemas for LangGraph workflows
  - Implement base agent interfaces and data models (follow patterns from notebooks)
  - _Requirements: 1.1, 2.1, 4.1, 5.1_

- [ ] 2. Implement document processing and vector store setup
  - [ ] 2.1 Create custom markdown chunker for mental models content
    - Write chunker that preserves markdown structure (headings, bullets, tables)
    - Implement contextual retrieval by maintaining heading context for chunks
    - _Requirements: 1.2, 1.3_

  - [ ] 2.2 Set up Qdrant vector store with OpenAI embeddings
    - Initialize Qdrant in-memory instance using code from notebooks
    - Implement document embedding and storage pipeline
    - _Requirements: 1.1, 1.2_

- [ ] 3. Build individual subagents
  - [ ] 3.1 Implement Vector RAG Subagent
    - Create LangGraph node for mental models retrieval using notebook patterns
    - _Requirements: 1.1, 1.2, 1.3_

  - [ ] 3.2 Implement Web Search Subagent
    - Copy Tavily tool from notebook
    - _Requirements: 2.1, 2.4_

  - [ ] 3.3 Implement Academic Search Subagent
    - Copy Arxiv tool from notebook
    - _Requirements: 2.2, 2.4_

- [ ] 4. Create supervisor agent and routing logic
  - [ ] 4.1 Implement query analysis and routing decisions
    - Create LLM-based query classifier to determine which subagents to use
    - _Requirements: 1.1, 2.3_

  - [ ] 4.2 Build supervisor agent coordination
    - Create LangGraph supervisor node that manages subagent execution
    - _Requirements: 2.3, 4.2_

- [ ] 5. Implement response synthesis and conversation management
  - [ ] 5.1 Create response synthesizer
    - Implement multi-source information integration logic
    - _Requirements: 1.4, 3.2, 3.3_

- [ ] 6. Build complete LangGraph workflow
  - [ ] 6.1 Integrate all components into unified graph
    - Create main LangGraph workflow combining supervisor and subagents (using Multi_Agent_RAG_LangGraph patterns)
    - Implement state management across all nodes
    - Add conditional edges based on routing decisions
    - _Requirements: 1.1, 2.3, 4.1_

- [ ] 7. Build user interface and API
  - [ ] 7.1 Create FastAPI backend service
    - Implement REST API endpoints for chat interactions using CopilotKit
    - _Requirements: 4.1, 5.3_

  - [ ] 7.2 Implement CopilotKit frontend
    - Set up CopilotKit chat interface with backend integration
    - _Requirements: 4.3, 4.4_
- [ ] 8. Create evaluation and testing framework
  - [ ] 8.1 Implement RAGAS evaluation pipeline
    - Set up RAGAS framework for RAG evaluation using notebook examples
    - Create golden dataset of business strategy questions with expected mental model applications using RAGAS synthetic data generation
    - Implement automated evaluation for faithfulness, relevance, precision, and recall
    - Generate baseline performance metrics and evaluation reports
    - _Requirements: 5.1, 5.2_
  - [ ] 8.2 Implement advanced retrieval techniques
    - Create ensemble retriever combining semantic search and BM25 (from Advanced_Retrieval notebook)
    - Implement contextual compression using Cohere reranking
    - Add multi-query retrieval for query expansion
    - Generate performance metrics and evaluation reports
    - _Requirements: 1.2, 5.2_


