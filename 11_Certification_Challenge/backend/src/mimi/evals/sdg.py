from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from ragas.testset import TestsetGenerator
from mimi.config.models import SDG_LLM_MODEL
from mimi.pipe.load import load_documents
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

def generate_sdg_testset(dataset, testset_size=100):
    generator_llm = LangchainLLMWrapper(ChatOpenAI(model=SDG_LLM_MODEL))
    generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())

    generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)
    dataset = generator.generate_with_langchain_docs(dataset, testset_size=testset_size)

    return dataset

if __name__ == "__main__":

    # data path
    data_path = Path("./data")
    # load documents    
    docs = load_documents(data_path)
    # generate testset
    dataset = generate_sdg_testset(docs)
    # save dataset to data_path/sdg/testset.csv
    os.makedirs(data_path / "sdg", exist_ok=True)
    dataset.to_pandas().to_csv(data_path / "sdg" / "testset.csv", index=False)