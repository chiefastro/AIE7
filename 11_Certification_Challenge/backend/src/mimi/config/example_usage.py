#!/usr/bin/env python3
"""
Example usage of the simple variants configuration system.
"""

from variants import (
    ExperimentConfig, 
    AgentType, 
    ChunkerType, 
    RetrieverType, 
    get_variants
)
import itertools

def run_experiment(experiment_name: str, config: ExperimentConfig):
    """Example experiment runner"""
    print(f"\n🧪 Running experiment: {experiment_name}")
    print(f"Config: {config.to_dict()}")
    
    # Initialize the global config
    variants = get_variants()
    variants.initialize(config)
    
    # Now any code can access the config like this:
    print(f"Agent type: {variants.agent_type.value}")
    print(f"Chunker type: {variants.chunker_type.value}")
    print(f"Retriever: {variants.retriever_type.value}")
    
    # Simulate some work
    print("Running experiment logic...")
    
    # Reset for next experiment
    variants.reset()

def generate_all_combinations():
    """Generate all possible combinations of variants"""
    configs = []
    
    # Get all enum values
    agent_types = list(AgentType)
    chunker_types = list(ChunkerType)
    retriever_types = list(RetrieverType)
    
    # Generate all combinations
    for agent_type, chunker_type, retriever_type in itertools.product(
        agent_types, chunker_types, retriever_types
    ):
        config = ExperimentConfig(
            agent_type=agent_type,
            chunker_type=chunker_type,
            retriever_type=retriever_type
        )
        configs.append(config)
    
    return configs

def main():
    """Example of running different experiment variants"""
    
    # Generate all combinations
    all_configs = generate_all_combinations()
    
    print(f"Generated {len(all_configs)} experiment configurations:")
    print("=" * 60)
    
    # Run all experiments
    for i, config in enumerate(all_configs, 1):
        experiment_name = f"Experiment_{i:02d}_{config.agent_type.value}_{config.chunker_type.value}_{config.retriever_type.value}"
        run_experiment(experiment_name, config)
    
    print(f"\n✅ Completed {len(all_configs)} experiments!")

if __name__ == "__main__":
    main() 