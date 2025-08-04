from typing import Annotated
import functools

from langgraph.graph import START, END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from mimi.tools.retriever import get_retriever
from mimi.config.models import RAG_MODEL_NAME
from mimi.prompts.rag import chat_prompt
from mimi.config.variant_defaults import CHUNKER_TYPE, RETRIEVER_TYPE


class State(TypedDict):
  question: str
  context: list[Document]
  response: str

def retrieve(state: State, config: dict, chunker_type: str = CHUNKER_TYPE, retriever_type: str = RETRIEVER_TYPE, **kwargs) -> State:
  retrieved_docs = get_retriever(
    chunker_type=chunker_type, retriever_type=retriever_type, **kwargs
  ).invoke(state["question"], config=config)
  return {"context" : retrieved_docs}

def generate(state: State, config: dict) -> State:
  openai_chat_model = ChatOpenAI(model=RAG_MODEL_NAME)
  generator_chain = chat_prompt | openai_chat_model | StrOutputParser()
  response = generator_chain.invoke({"query" : state["question"], "context" : state["context"]}, config=config)
  return {"response" : response}

def create_rag_graph(chunker_type: str = CHUNKER_TYPE, retriever_type: str = RETRIEVER_TYPE, **kwargs):
  graph_builder = StateGraph(State)
  
  retrieve_node = functools.partial(retrieve, chunker_type=chunker_type, retriever_type=retriever_type, **kwargs)
  graph_builder.add_node("retrieve", retrieve_node)
  graph_builder.add_node("generate", generate)
  
  graph_builder.add_edge(START, "retrieve")
  graph_builder.add_edge("retrieve", "generate")
  graph_builder.add_edge("generate", END)
  
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