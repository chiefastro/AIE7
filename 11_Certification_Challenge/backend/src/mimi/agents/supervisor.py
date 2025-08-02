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


class RouteDecision(BaseModel):
    next: Literal["FINISH", "RAG", "Search", "Arxiv"] = Field(
        description="The next role to act or FINISH to end the conversation"
    )

def create_team_supervisor(llm: ChatOpenAI, system_prompt, members) -> str:
    """An LLM-based router."""
    options = ["FINISH"] + members
    
    # Create the output parser
    output_parser = JsonOutputParser(pydantic_object=RouteDecision)
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "system",
                "Given the conversation above, who should act next?"
                " Or should we FINISH? Respond with a JSON object containing the 'next' field with one of: {options}",
            ),
        ]
    ).partial(options=str(options), team_members=", ".join(members))

    chain = (
        prompt
        | llm
        | output_parser
    )
    return chain


class ResearchTeamState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: List[str]
    next: Optional[str]

def create_supervisor_graph():
    logger.info("Creating supervisor graph...")
    supervisor_llm = ChatOpenAI(model=SUPERVISOR_MODEL_NAME)
    subagent_llm = ChatOpenAI(model=SUBAGENT_MODEL_NAME)

    search_agent = create_agent(
        subagent_llm,
        [TavilySearch(max_results=5)],
        "You are a research assistant who can search for up-to-date info using the tavily search engine.",
    )
    search_node = functools.partial(agent_node, agent=search_agent, name="Search")


    rag_agent = create_agent(
        subagent_llm,
        [retrieve_information],
        "You are a research assistant who can provide specific information on mental models for the Intelligence Age",
    )
    rag_node = functools.partial(agent_node, agent=rag_agent, name="RAG")

    # arxiv search agent
    arxiv_agent = create_agent(
        subagent_llm,
        [ArxivQueryRun()],
        "You are a research assistant who can search for academic papers using the arxiv search engine.",
    )
    arxiv_node = functools.partial(agent_node, agent=arxiv_agent, name="Arxiv")

    supervisor_agent = create_team_supervisor(
        supervisor_llm,
        ("You are a supervisor tasked with managing a conversation between the"
        " following workers:  RAG, Search, Arxiv. Given the following user request,"
        " determine the subject to be researched and respond with the worker to act next. Each worker will perform a"
        " task and respond with their results and status. "
        " You should never ask your team to do anything beyond research. They are not required to write content or posts."
        " You should only pass tasks to workers that are specifically research focused."
        "\n\nHere is more information about the workers:\n"
        "RAG: They can provide specific information on mental models for the Intelligence Age.\n"
        "Search: They can search for up-to-date info using the tavily search engine.\n"
        "Arxiv: They can search for academic papers using the arxiv search engine.\n\n"
        " When finished, respond with FINISH."),
        ["RAG", "Search", "Arxiv"],
    )
    supervisor_node = functools.partial(agent_node, agent=supervisor_agent, name="Supervisor")

    supervisor_graph = StateGraph(ResearchTeamState)

    supervisor_graph.add_node("Search", search_node)
    supervisor_graph.add_node("RAG", rag_node)
    supervisor_graph.add_node("Arxiv", arxiv_node)
    supervisor_graph.add_node("supervisor", supervisor_node)

    supervisor_graph.add_edge("Search", "supervisor")
    supervisor_graph.add_edge("RAG", "supervisor")
    supervisor_graph.add_edge("Arxiv", "supervisor")
    supervisor_graph.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {"Search": "Search", "RAG": "RAG", "Arxiv": "Arxiv", "FINISH": END},
    )

    supervisor_graph.set_entry_point("supervisor")

    # Add checkpointer configuration
    checkpointer = MemorySaver()
    
    compiled_graph = supervisor_graph.compile(checkpointer=checkpointer)
    logger.info("Supervisor graph created successfully")
    return compiled_graph
