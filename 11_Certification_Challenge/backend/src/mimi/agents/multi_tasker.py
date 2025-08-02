import functools
import logging
from typing import Annotated, List, Optional
import operator
from typing_extensions import TypedDict

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Literal
from langchain_tavily import TavilySearch
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_core.messages import BaseMessage
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from copilotkit.langgraph import copilotkit_emit_message

from mimi.config.models import SUPERVISOR_MODEL_NAME, SUBAGENT_MODEL_NAME
from mimi.agents.base import create_agent, agent_node
from mimi.agents.rag import retrieve_information

logger = logging.getLogger(__name__)


class MultiTaskerState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

def create_multi_tasker_graph():
    logger.info("Creating multi-tasker graph...")
    llm = ChatOpenAI(model=SUPERVISOR_MODEL_NAME)

    multi_tasker_agent = create_agent(
        llm,
        [TavilySearch(max_results=5), retrieve_information, ArxivQueryRun()],
        (
            "You are a research assistant who can search for up-to-date info using the tavily search engine, "
            "provide specific information on mental models for the Intelligence Age, "
            "and search for academic papers using the arxiv search engine. "
            "You will begin by reviewing the mental models for the Intelligence Age and use them to frame your answer. "
            "You will then keep using the other tools until you have gathered enough supplemental information to answer the user request. "
            "You will then return the answer, framed by the mental models, using in-line citations from all sources."
        )
    )
    multi_tasker_node = functools.partial(agent_node, agent=multi_tasker_agent, name="MultiTasker")


    multi_tasker_graph = StateGraph(MultiTaskerState)

    multi_tasker_graph.add_node("MultiTasker", multi_tasker_node)

    multi_tasker_graph.add_edge("MultiTasker", END)

    multi_tasker_graph.set_entry_point("MultiTasker")

    # Add checkpointer configuration
    checkpointer = MemorySaver()
    
    compiled_graph = multi_tasker_graph.compile(checkpointer=checkpointer)
    logger.info("Multi-tasker graph created successfully")
    return compiled_graph
