## RAG Process Diagram

The following diagram illustrates the complete RAG (Retrieval Augmented Generation) process:

```mermaid
flowchart TD
    A["Load Source Documents"] --> B["Split Documents into Chunks"]
    B --> C["Generate Embeddings for Chunks"]
    C --> D["Store Embeddings in Vector Database"]
    E["User Query"] --> F["Embed Query"]
    F --> G["Retrieve Top-k Similar Chunks from Vector DB"]
    G --> H["Construct Prompt with Retrieved Context"]
    H --> I["LLM Generates Answer"]
    D -.-> G
    G -.-> H
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style I fill:#bbf,stroke:#333,stroke-width:2px
    style E fill:#bfb,stroke:#333,stroke-width:2px
    style D fill:#ffd,stroke:#333,stroke-width:2px
    style G fill:#ffd,stroke:#333,stroke-width:2px
    style H fill:#ffd,stroke:#333,stroke-width:2px
    style F fill:#bfb,stroke:#333,stroke-width:2px
    style C fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#f9f,stroke:#333,stroke-width:2px
```

This diagram shows the two main phases:
1. **Preprocessing Phase** (A→B→C→D): Documents are loaded, chunked, embedded, and stored
2. **Query Phase** (E→F→G→H→I): User queries are processed, relevant chunks retrieved, and answers generated 