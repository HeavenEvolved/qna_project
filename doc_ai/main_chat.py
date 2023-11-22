# from langchain.llms import LlamaCpp
# from langchain.embeddings import LlamaCppEmbeddings

from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings

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

# model_path = os.path.abspath("doc_ai/llm/llama-2-7b-32k-instruct.Q4_K_S.gguf")

# buffer_llm = LlamaCpp(
#     model_path=model_path,
#     max_tokens=32000,
#     repeat_penalty=1.2,
#     temperature=0.6,
#     top_p=0.9,
#     n_ctx=32000,
#     n_threads=16,
#     verbose=False,
#     n_batch=16,
#     model_kwargs={"n_threads_batch": 16},
# )

# llm = LlamaCpp(
#     model_path=model_path,
#     max_tokens=32000,
#     n_ctx=32000,
#     repeat_penalty=1.2,
#     temperature=0.6,
#     top_p=0.9,
#     n_threads=16,
#     top_k=20,
#     verbose=False,
#     n_batch=16,
#     model_kwargs={"n_threads_batch": 16},
# )

# embeddings = LlamaCppEmbeddings(
#     model_path=model_path, n_threads=16, n_ctx=16000, verbose=False
# )

API_KEY = dotenv.dotenv_values()["HF_TOKEN"]
MODEL_ID = dotenv.dotenv_values()["REPO_ID"]


@timer.time_this
def chat():
    try:
        buffer_llm = HuggingFacePipeline.from_model_id(
            model_id=MODEL_ID,
            task="text-generation",
            batch_size=4,
            model_kwargs={"max_length": 32000},
            pipeline_kwargs={
                "max_new_tokens": 16000,
                "temperature": 0.3,
                "top_p": 0.95,
                "repetition_penalty": 1.15,
            },
            device_map="auto",
            verbose="False",
        )

    except Exception as e:
        print(e)

    llm = HuggingFacePipeline.from_model_id(
        model_id=MODEL_ID,
        task="text-generation",
        batch_size=4,
        model_kwargs={"max_length": 32000},
        pipeline_kwargs={
            "max_new_tokens": 16000,
            "temperature": 0.6,
            "top_p": 0.95,
            "repetition_penalty": 1.15,
        },
        device_map="auto",
        verbose="False",
    )

    embeddings = HuggingFaceEmbeddings(device_map="auto")

    db = Chroma(
        persist_directory=os.path.abspath("doc_ai/data"), embedding_function=embeddings
    )
    print("Here")
    memory = ConversationSummaryBufferMemory(
        llm=buffer_llm,
        max_tokens_limit=4000,
        memory_key="chat_history",
        return_messages=True,
    )

    pdf_qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={"k": 10}),
        memory=memory,
        max_tokens_limit=16000,
    )

    while True:
        query = input("Question: ")

        print(
            "",
            *[
                (docs.page_content, score)
                for docs, score in db.similarity_search_with_score(query=query, k=20)
            ],
            sep="\n"
        )

        if "exit" == query.lower():
            print("Exiting!")
            break

        try:
            print("\n\nProcessing")
            result = pdf_qa({"question": query})
        except Exception as e:
            print("Error:", e)
            return "Error"

        # # print("\nHistory\n")
        # # print(memory.moving_summary_buffer)

        print(result["answer"])

    return "Completed!"
