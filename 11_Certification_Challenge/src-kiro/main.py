"""
Main module for the AI Mental Models Advisor.
Entry point for the application.
"""

from typing import Dict, Any
from src.utils.config import Config
from src.models.state import ConversationState


class MentalModelsAdvisor:
    """Main application class for the AI Mental Models Advisor."""
    
    def __init__(self):
        """Initialize the advisor with configuration."""
        self.config = Config()
        if not self.config.validate_api_keys():
            raise ValueError("Required API keys are missing. Please check your environment variables.")
        
        # Components will be initialized in later tasks
        self.supervisor_agent = None
        self.vector_rag_agent = None
        self.web_search_agent = None
        self.academic_search_agent = None
        self.response_synthesizer = None
        self.langgraph_workflow = None
    
    def initialize_components(self):
        """Initialize all system components."""
        # This will be implemented in subsequent tasks
        pass
    
    def process_query(self, query: str, conversation_history: list = None) -> Dict[str, Any]:
        """
        Process a user query and return a response.
        
        Args:
            query: User's question or query
            conversation_history: Previous conversation context
            
        Returns:
            Dictionary containing the response and metadata
        """
        if conversation_history is None:
            conversation_history = []
        
        # Initialize state
        initial_state: ConversationState = {
            "query": query,
            "conversation_history": conversation_history,
            "routing_decision": None,
            "vector_results": None,
            "web_results": None,
            "academic_results": None,
            "final_response": None
        }
        
        # Process through LangGraph workflow (to be implemented)
        # final_state = self.langgraph_workflow.invoke(initial_state)
        
        # For now, return placeholder response
        return {
            "answer": "System is being initialized. Please wait for implementation.",
            "mental_models_used": [],
            "sources": [],
            "follow_up_questions": []
        }


if __name__ == "__main__":
    # Basic test of the system
    advisor = MentalModelsAdvisor()
    print("AI Mental Models Advisor initialized successfully!")
    
    # Test query
    response = advisor.process_query("What mental models should I use for AI strategy?")
    print(f"Response: {response}")