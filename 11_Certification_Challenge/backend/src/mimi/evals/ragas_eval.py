from collections import defaultdict
import os
from tqdm import tqdm
import pandas as pd
import copy
import uuid
import itertools
from concurrent.futures import ThreadPoolExecutor

from langsmith import Client
from ragas import EvaluationDataset
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, ResponseRelevancy
from ragas import evaluate, RunConfig
from langchain_openai import ChatOpenAI

from mimi.config.models import RAGAS_EVAL_LLM_MODEL
from mimi.config.variants import (
    ExperimentConfig, 
    AgentType,
    ChunkerType, 
    RetrieverType, 
)
from mimi.agents.rag import create_rag_graph



def run_ragas_eval(invocable, invocable_name, dataset, experiment_id):

  dataset_this = copy.deepcopy(dataset)

  for test_row in dataset_this:
    # Provide proper config for the checkpointer
    config = {
        "configurable": {
            "thread_id": f"experiment_{invocable_name}_{uuid.uuid4()}"
        },
        "tags": [invocable_name, experiment_id]
    }
    
    response = invocable.invoke({"question" : test_row.eval_sample.user_input}, config=config)
    test_row.eval_sample.response = response["response"]
    test_row.eval_sample.retrieved_contexts = [context.page_content for context in response["context"]]

  evaluation_dataset = EvaluationDataset.from_pandas(dataset_this.to_pandas())
  evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model=RAGAS_EVAL_LLM_MODEL))

  custom_run_config = RunConfig(timeout=360)
  result = evaluate(
      dataset=evaluation_dataset,
      metrics=[LLMContextRecall(), Faithfulness(), FactualCorrectness(), ResponseRelevancy()],
      llm=evaluator_llm,
      run_config=custom_run_config
  )
  return result

def run_ragas_eval_parallel(invocables, dataset, experiment_id):
  results = []
  with ThreadPoolExecutor() as executor:
      futures = [
          executor.submit(run_ragas_eval, invocable, invocable_name, dataset, experiment_id)
          for invocable_name, invocable in invocables.items()
      ]
      results = [f.result() for f in futures]

  results_d = {invocable_name: result for invocable_name, result in zip(invocables.keys(), results)}
  return results_d

def run_ragas_eval_sequential(invocables, dataset, experiment_id):
  """Run evaluations sequentially to avoid Qdrant client conflicts"""
  results_d = {}
  for invocable_name, invocable in invocables.items():
      result = run_ragas_eval(invocable, invocable_name, dataset, experiment_id)
      results_d[invocable_name] = result
  return results_d


def generate_all_invocables():
    """Generate invocables for all possible combinations of variants"""
    invocables = {}
    
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
        agent_graph = create_rag_graph(
            chunker_type=config.chunker_type.value, 
            retriever_type=config.retriever_type.value
        )
        invocables[config.chunker_type.value + "_" + config.retriever_type.value] = agent_graph
    
    return invocables




def get_langsmith_stats(experiment_id):
  client = Client()

  invocables = generate_all_invocables()
  tags = list(invocables.keys())
  by_tag = defaultdict(dict)

  for t in tqdm(tags):
      filter = f"and(has(tags, '{t}'), has(tags, '{experiment_id}'))"
      print(filter)
      by_tag[t] = client.get_run_stats(
          project_names=[os.environ["LANGSMITH_PROJECT"]],
          # filter syntax lets you match an element in the tags array
          filter=filter
      )

  langsmith_df = pd.DataFrame(by_tag).T
  return langsmith_df


def get_score_df(results_d):
    score_dfs = []
    for name, result in results_d.items():
        score_df = pd.DataFrame(result.scores)
        score_df['experiment_name'] = name
        score_dfs.append(score_df)

    score_df = pd.concat(score_dfs)
    return score_df

