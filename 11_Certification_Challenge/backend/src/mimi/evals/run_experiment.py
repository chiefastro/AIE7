#!/usr/bin/env python3
"""
Example usage of the simple variants configuration system.
"""

from mimi.evals.ragas_eval import generate_all_invocables, get_langsmith_stats, run_ragas_eval_parallel, get_score_df
from mimi.evals.ragas_csv_loader import load_ragas_csv
from IPython.display import display
import uuid
import os
from pathlib import Path
import pandas as pd


def main():
    """Example of running different experiment variants"""

    # data path
    data_path = Path("./data")
    os.makedirs(data_path / "experiments", exist_ok=True)
    
    print("Starting experiment...")
    
    # Generate all combinations
    invocables = generate_all_invocables()
    print(f"Generated {len(invocables)} invocables")

    # Load dataset
    dataset = load_ragas_csv(data_path / "sdg" / "testset.csv")
    print(f"Loaded dataset with {len(dataset)} samples")

    # Generate an experiment id
    experiment_id = str(uuid.uuid4())
    print(f"Experiment ID: {experiment_id}")

    # Run all experiments
    print("Running experiments...")
    results_d = run_ragas_eval_parallel(invocables, dataset, experiment_id)
    print("Experiments completed")

    # Format results
    score_df = get_score_df(results_d)
    print(f"Generated score dataframe with shape: {score_df.shape}")

    # Save results
    score_df.to_csv(data_path / "experiments" / f"score_df_{experiment_id}.csv", index=False)
    print(f"Saved results to: {data_path / 'experiments' / f'score_df_{experiment_id}.csv'}")

    # Analyze results
    print("Analyzing results...")
    score_aggs = score_df.groupby('experiment_name').mean()
    langsmith_df = get_langsmith_stats(experiment_id)
    score_aggs_combined = pd.concat([score_aggs, -langsmith_df[['latency_p50', 'latency_p99', 'cost_p50', 'cost_p99']]], axis=1)
    print("Eval rankings:")
    display(score_aggs_combined.rank(ascending=False))
    print("Aggregated rankings for evals only:")
    display(score_aggs.rank(ascending=False).mean(axis=1).sort_values(ascending=True))
    print("Aggregated rankings for cost/latency only:")
    display((-langsmith_df[['latency_p50', 'latency_p99', 'cost_p50', 'cost_p99']]).rank(ascending=False).mean(axis=1).sort_values(ascending=True))
    print("Final ranking: Aggregated rankings for both evals and cost/latency:")
    display(score_aggs_combined.rank(ascending=False).mean(axis=1).sort_values(ascending=True))

    # Save combined results
    score_aggs_combined.to_csv(data_path / "experiments" / f"score_aggs_combined_{experiment_id}.csv")
    print(f"Saved combined results to: {data_path / 'experiments' / f'score_aggs_combined_{experiment_id}.csv'}")

    # Return score dataframe
    return {"score_df" : score_df, "score_aggs_combined" : score_aggs_combined}
    

if __name__ == "__main__":
    main() 