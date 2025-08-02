from typing import Annotated

from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from mimi.tools.retriever import get_retriever
from mimi.config.models import RAG_MODEL_NAME
from mimi.prompts.rag import chat_prompt


class State(TypedDict):
  question: str
  context: list[Document]
  response: str

def retrieve(state: State) -> State:
  retrieved_docs = get_retriever().invoke(state["question"])
  return {"context" : retrieved_docs}

def generate(state: State) -> State:
  openai_chat_model = ChatOpenAI(model=RAG_MODEL_NAME)
  generator_chain = chat_prompt | openai_chat_model | StrOutputParser()
  response = generator_chain.invoke({"query" : state["question"], "context" : state["context"]})
  return {"response" : response}

def create_rag_graph():
  graph_builder = StateGraph(State)
  graph_builder = graph_builder.add_sequence([retrieve, generate])
  graph_builder.add_edge(START, "retrieve")
  
  # Add checkpointer configuration
  checkpointer = MemorySaver()
  rag_graph = graph_builder.compile(checkpointer=checkpointer)
  return rag_graph



@tool
def retrieve_information(
    query: Annotated[str, "query to ask the retrieve information tool"]
    ):
  """Use Retrieval Augmented Generation to retrieve information about mental models for the Intelligence Age"""
  return create_rag_graph().invoke({"question" : query})