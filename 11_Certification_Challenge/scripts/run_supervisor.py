from mimi.agents.supervisor import create_supervisor_graph
from langchain_core.messages import HumanMessage

if __name__ == "__main__":
    supervisor_graph = create_supervisor_graph()

    supervisor_graph.invoke({
        "messages": [
            HumanMessage(content="How should I use AI to revitalize my supply chain risk management (SCRM) SaaS business?")
        ]
    })

