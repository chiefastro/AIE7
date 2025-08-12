#### ❓ Question:

What is the purpose of the `chunk_overlap` parameter when using `RecursiveCharacterTextSplitter` to prepare documents for RAG, and what trade-offs arise as you increase or decrease its value?

#### Answer:

The purpose is to guard against the beginning and end of a concept being split between two chunks. With overlap, any concept that may have been split on the right (at the end) is unlikely to also be split on the left (at the beginning of the next chunk).

The more overlap, the lower the risk of concepts not being fully contained in either the right or left chunk. But this also produces more total chunks.


#### ❓ Question:

Your retriever is configured with `search_kwargs={"k": 5}`. How would adjusting `k` likely affect RAGAS metrics such as Context Precision and Context Recall in practice, and why?

#### Answer:

As k increases, context recall should increase because there are more chances to retrieve documents containing the correct answers (context recall is num retrieved docs with correct answers / num total docs with correct answers).

As k increases, context precision should decrease because documents with lower similarity scores are less likely to be relevant.

#### ❓ Question:

Compare the `agent` and `agent_helpful` assistants defined in `langgraph.json`. Where does the helpfulness evaluator fit in the graph, and under what condition should execution route back to the agent vs. terminate?

These two agents are identical except that the helpfulness one has an extra node to do a helpfulness check that conditionally will route back to the main agent to try again if the response was not helpful.
It routes back to the agent if helpfulness_node responds with N (meaning not helpful).