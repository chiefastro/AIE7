from enum import Enum
from typing import Optional, Dict, Any
from dataclasses import dataclass
import threading

from mimi.config.variant_defaults import AGENT_TYPE, CHUNKER_TYPE, RETRIEVER_TYPE

class AgentType(Enum):
    SUPERVISOR = "supervisor"
    MULTI_TASKER = "multi_tasker"

class ChunkerType(Enum):
    NAIVE_CHUNKER = "naive_chunker"
    MARKDOWN_CHUNKER = "markdown_chunker"

class RetrieverType(Enum):
    COSINE = "cosine"
    MULTI_QUERY = "multi_query"

@dataclass(frozen=True)
class ExperimentConfig:
    """Immutable experiment configuration"""
    agent_type: AgentType
    chunker_type: ChunkerType
    retriever_type: RetrieverType
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for logging/serialization"""
        return {
            "agent_type": self.agent_type.value,
            "chunker_type": self.chunker_type.value,
            "retriever_type": self.retriever_type.value,
        }

class ExperimentVariants:
    """Singleton configuration manager for experiment variants"""
    _instance = None
    _lock = threading.Lock()
    _config: Optional[ExperimentConfig] = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self, config: ExperimentConfig) -> None:
        """Initialize the config (can only be done once per thread)"""
        if self._initialized:
            raise RuntimeError("Config already initialized. Cannot change during experiment.")
        
        self._config = config
        self._initialized = True
    
    def get_config(self) -> ExperimentConfig:
        """Get the current config, using defaults if not initialized"""
        if not self._initialized or self._config is None:
            # Create default config from variant_defaults.py
            print(f"Creating default config from variant_defaults.py: {AGENT_TYPE}, {CHUNKER_TYPE}, {RETRIEVER_TYPE}")
            default_config = ExperimentConfig(
                agent_type=AgentType(AGENT_TYPE),
                chunker_type=ChunkerType(CHUNKER_TYPE),
                retriever_type=RetrieverType(RETRIEVER_TYPE)
            )
            return default_config
        return self._config
    
    def reset(self) -> None:
        """Reset the config (useful for testing)"""
        self._config = None
        self._initialized = False
    
    @property
    def agent_type(self) -> AgentType:
        return self.get_config().agent_type
    
    @property
    def chunker_type(self) -> ChunkerType:
        return self.get_config().chunker_type
    
    @property
    def retriever_type(self) -> RetrieverType:
        return self.get_config().retriever_type

# Global instance
variants = ExperimentVariants()
