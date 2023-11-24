from langchain.embeddings import LlamaCppEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
import os

from utils import timer
import dotenv

import warnings

warnings.filterwarnings("ignore")

# API_KEY = dotenv.dotenv_values()["HF_TOKEN"]
# REPO_ID = dotenv.dotenv_values()["REPO_ID"]


@timer.time_this
def vectorize(data, db="Chroma"):
    model_path = os.path.abspath("doc_ai/llm/llama-2-7b-32k-instruct.Q4_K_S.gguf")

    # print(model_path)

    try:
        embeddings = LlamaCppEmbeddings(
            model_path=model_path,
            n_ctx=32768,
            n_batch=1024,
            n_threads=8,
            verbose=True,
        )
    except Exception as e:
        print(e)

    # embedder = HuggingFaceEmbeddings()

    if db == "Chroma":
        from vectorizers import chroma_vector

        chroma_vector.vectorize(data, embeddings, data[0].metadata)
