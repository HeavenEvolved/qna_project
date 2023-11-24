from langchain.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings

from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings

import torch

from langchain.vectorstores import Chroma

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryBufferMemory

import json
import os
import re
import dotenv

from utils import timer

import warnings

warnings.filterwarnings("ignore")

API_KEY = dotenv.dotenv_values()["HF_TOKEN"]
MODEL_ID = dotenv.dotenv_values()["REPO_ID"]


@timer.time_this
def chat():
    try:
        model_path = os.path.abspath("doc_ai/llm/llama-2-7b-32k-instruct.Q4_K_S.gguf")

        llm = LlamaCpp(
            model_path=model_path,
            n_ctx=32768,
            use_mlock=True,
            n_gpu_layers=8,
            repeat_penalty=1.2,
            temperature=0.6,
            top_p=0.9,
            n_threads=16,
            top_k=10,
            verbose=True,
            n_batch=1000,
            device_map="auto",
            model_kwargs={"n_threads_batch": 16},
        )

        embeddings = LlamaCppEmbeddings(
            model_path=model_path,
            n_ctx=32768,
            n_batch=1024,
            n_threads=8,
            verbose=False,
        )

        # llm = HuggingFacePipeline.from_model_id(
        #     model_id=MODEL_ID,
        #     task="text-generation",
        #     device=0,
        #     model_kwargs={
        #         "max_length": 32000,
        #         "temperature": 0.8,
        #         "top_k": 5,
        #         "repetition_penalty": 1.15,
        #         "torch_dtype": torch.bfloat16
        #     },
        #     verbose=False,
        # )

        print("LLM and Embeddings Loaded...")
    except Exception as e:
        print(e)

    # embeddings = HuggingFaceEmbeddings()
    db = Chroma(
        persist_directory=os.path.abspath("doc_ai/data"), embedding_function=embeddings
    )

    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_tokens_limit=4000,
        memory_key="chat_history",
        return_messages=True,
    )

    pdf_qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=db.as_retriever(),
        memory=memory,
    )

    while True:
        query = input("Question: ")

        try:
            print(
                "",
                *[
                    (docs.page_content, score)
                    for docs, score in db.similarity_search_with_score(query=query, k=5)
                ],
                sep="\n"
            )
        except Exception as e:
            print(e)

        if "exit" == query.lower():
            print("Exiting!")
            break

        try:
            print("\n\nProcessing")
            result = pdf_qa({"question": query})
            print("Generated")
        except Exception as e:
            print("Error:", e)
            return "Error"

        # # print("\nHistory\n")
        # # print(memory.moving_summary_buffer)

        print(result["answer"])

    return "Completed!"
