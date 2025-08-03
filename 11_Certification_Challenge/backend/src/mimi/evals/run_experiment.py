#!/usr/bin/env python3
"""
Example usage of the simple variants configuration system.
"""

from mimi.config.variants import (
    ExperimentConfig, 
    AgentType, 
    ChunkerType, 
    RetrieverType, 
    variants
)
from mimi.evals.ragas_eval import run_ragas_eval
import itertools
from mimi.agents.rag import create_rag_graph
from mimi.evals.ragas_csv_loader import load_ragas_csv

def run_experiment(experiment_name: str, config: ExperimentConfig):
    """Example experiment runner"""
    print(f"\n🧪 Running experiment: {experiment_name}")
    print(f"Config: {config.to_dict()}")
    
    # Initialize the global config
    variants.initialize(config)
    
    # Now any code can access the config like this:
    print(f"Chunker type: {variants.chunker_type.value}")
    print(f"Retriever: {variants.retriever_type.value}")

    # Get agent graph
    agent_graph = create_rag_graph()

    # Load dataset
    dataset = load_ragas_csv(f"./data/sdg/testset.csv")

    # Run the experiment
    run_ragas_eval(agent_graph, experiment_name, dataset)
    
    # Reset for next experiment
    variants.reset()

def generate_all_combinations():
    """Generate all possible combinations of variants"""
    configs = []
    
    # Get all enum values
    chunker_types = list(ChunkerType)
    retriever_types = list(RetrieverType)
    
    # Generate all combinations
    for chunker_type, retriever_type in itertools.product(
        chunker_types, retriever_types
    ):
        config = ExperimentConfig(
            agent_type=AgentType.MULTI_TASKER,
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
    for i, config in enumerate(all_configs[0:1], 1):
        experiment_name = f"Experiment_{i:02d}_{config.chunker_type.value}_{config.retriever_type.value}"
        run_experiment(experiment_name, config)
    
    print(f"\n✅ Completed {len(all_configs)} experiments!")

if __name__ == "__main__":
    main() 