import pandas as pd
import ast
from ragas.testset.synthesizers.testset_schema import Testset, TestsetSample
from ragas.dataset_schema import SingleTurnSample

def load_ragas_csv(path: str):
    """
    Load a CSV file and reconstruct the original Testset structure.
    """
    # Load dataset and reconstruct original Testset structure
    df = pd.read_csv(path)
    df['reference_contexts'] = df['reference_contexts'].apply(ast.literal_eval)
    
    # Reconstruct the original Testset structure
    samples = []
    for _, row in df.iterrows():
        # Create SingleTurnSample (eval_sample)
        eval_sample = SingleTurnSample(
            user_input=row['user_input'],
            reference_contexts=row['reference_contexts'],
            reference=row['reference']
        )
        
        # Create TestsetSample
        testset_sample = TestsetSample(
            eval_sample=eval_sample,
            synthesizer_name=row['synthesizer_name']
        )
        samples.append(testset_sample)
    
    # Create Testset
    dataset = Testset(samples=samples)

    return dataset