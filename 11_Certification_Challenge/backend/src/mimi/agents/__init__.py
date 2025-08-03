from mimi.agents.supervisor import create_supervisor_graph
from mimi.agents.multi_tasker import create_multi_tasker_graph
from mimi.config.variants import variants, AgentType

def get_agent_graph():
    if variants.agent_type == AgentType.SUPERVISOR:
        return create_supervisor_graph()
    elif variants.agent_type == AgentType.MULTI_TASKER:
        return create_multi_tasker_graph()
    else:
        raise ValueError(f"Invalid agent type: {variants.agent_type}")

__all__ = ["get_agent_graph"]