# from langchain.embeddings import LlamaCppEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
import os

from utils import timer
import dotenv

API_KEY = dotenv.dotenv_values()["HF_TOKEN"]
REPO_ID = dotenv.dotenv_values()["REPO_ID"]


@timer.time_this
def vectorize(data, db="Chroma"):
    # embedder = LlamaCppEmbeddings(
    #     model_path=os.path.abspath("doc_ai/llm/llama-2-7b-32k-instruct.Q4_K_S.gguf"),
    #     n_threads=16,
    #     n_ctx=16000,
    #     verbose=False,
    # )

    embedder = HuggingFaceEmbeddings()

    if db == "Chroma":
        from vectorizers import chroma_vector

        chroma_vector.vectorize(data, embedder, data[0].metadata)
