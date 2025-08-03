from ragas import EvaluationDataset
from ragas import evaluate
from ragas.llms import LangchainLLMWrapper
from ragas.metrics import LLMContextRecall, Faithfulness, FactualCorrectness, ResponseRelevancy, ContextEntityRecall, NoiseSensitivity
from ragas import evaluate, RunConfig
import copy
from langchain_openai import ChatOpenAI
from mimi.config.models import RAGAS_EVAL_LLM_MODEL
import uuid

def run_ragas_eval(invocable, invocable_name, dataset):

  dataset_this = copy.deepcopy(dataset)

  for test_row in dataset_this:
    # Provide proper config for the checkpointer
    config = {
        "configurable": {
            "thread_id": f"experiment_{invocable_name}_{uuid.uuid4()}"
        },
        "tags": [invocable_name]
    }
    
    response = invocable.invoke({"question" : test_row.eval_sample.user_input}, config)
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