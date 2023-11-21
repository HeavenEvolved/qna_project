from langchain.embeddings import LlamaCppEmbeddings
import os

from utils import timer


@timer.time_this
def vectorize(data, db="Chroma"):
    embedder = LlamaCppEmbeddings(
        model_path=os.path.abspath("doc_ai/llm/llama-2-7b-32k-instruct.Q4_K_S.gguf"),
        n_threads=16,  
        n_ctx=16000, 
        verbose=False, 
    )
    if db == "Chroma":
        from vectorizers import chroma_vector

        chroma_vector.vectorize(data, embedder, data[0].metadata)
