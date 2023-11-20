from langchain.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings

from langchain.vectorstores import Chroma

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryBufferMemory

import json
import os
import re

from utils import timer


model_path = os.path.abspath("doc_ai/llm/llama-2-7b-32k-instruct.Q4_K_S.gguf")

buffer_llm = LlamaCpp(
    model_path=model_path,
    max_tokens=32000,
    repeat_penalty=1.2,
    temperature=0.6,
    top_p=0.9,
    n_ctx=32000,
    n_threads=16,
    verbose=False,
    n_batch=16,
    model_kwargs={"n_threads_batch": 16},
)

llm = LlamaCpp(
    model_path=model_path,
    max_tokens=32000,
    n_ctx=32000,
    repeat_penalty=1.2,
    temperature=0.6,
    top_p=0.9,
    n_threads=16,
    top_k=10,
    verbose=False,
    n_batch=16,
    model_kwargs={"n_threads_batch": 16},
)

embeddings = LlamaCppEmbeddings(
    model_path=model_path, n_threads=16, n_ctx=16000, verbose=False
)

db = Chroma(
    persist_directory=os.path.abspath("doc_ai/data"), embedding_function=embeddings
)
memory = ConversationSummaryBufferMemory(
    llm=buffer_llm,
    max_tokens_limit=16000,
    memory_key="chat_history",
    return_messages=True,
)

pdf_qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={"k": 10}),
    memory=memory,
    max_tokens_limit=16000,
)


@timer.time_this
def chat(query=None):
    if not query:
        query = input("Question: ")
    print(
        "",
        *[
            (docs.page_content, score)
            for docs, score in db.similarity_search_with_score(query=query, k=10)
        ],
        sep="\n"
    )

    # if "exit" in query.lower():
    #     print("Exiting!")
    #     return "Completed!"

    # try:
    #     print("\n\nProcessing")
    #     result = pdf_qa({"question": query})
    # except Exception as e:
    #     print("Error:", e)

    # # print("\nHistory\n")
    # # print(memory.moving_summary_buffer)

    # return result["answer"]
