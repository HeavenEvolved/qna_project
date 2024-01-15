from glob import iglob
import pandas as pd

import pymongo
import os

from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain
from unstructured.cleaners.core import clean, clean_non_ascii_chars

import dotenv
import textwrap
import json

import warnings

warnings.simplefilter("ignore")

mongo_url = "mongodb://localhost:27017/"

os.environ["TOKENIZERS_PARALLELISM"] = "True"


def time_this(f):
    from functools import wraps
    from time import time

    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(
            "\nfile:%r | func:%r | took: %2.4f sec\n"
            % (f.__globals__["__file__"].split("/")[-1], f.__name__, te - ts)
        )
        return result

    return wrap


def load_files_collection(folder_web_id):
    client = pymongo.MongoClient(mongo_url)
    files_data = client["files_data"]
    curr_files_metadata = files_data[f"{folder_web_id}_metadata"]
    curr_files = list(
        curr_files_metadata.find({"category": "resume", "uploaded": 1, "processed": 0})
    )
    return curr_files


def get_file_paths(files_coll):
    paths = [x["file_path"] for x in files_coll]
    return paths


def read_file(file_path, files_collection):
    file_data = (
        UnstructuredFileLoader(
            file_path,
            strategy="ocr_only",
            post_processors=[
                clean_non_ascii_chars,
                lambda x: clean(
                    x,
                    extra_whitespace=True,
                ),
            ],
        )
        .load()[0]
        .page_content
    )
    return file_data


def wrap_text_preserve_newlines(content, width=110):
    lines = content.split("\n")
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
    wrapped_text = "\n".join(wrapped_lines)
    return wrapped_text


def vectorize(chunks):
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_texts(chunks, embedding=embeddings)
    return db


def split_content(content, chunk_size=4000, chunk_overlap=300):
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    chunks = text_splitter.split_text(content)
    return chunks


def qa_chain(db, query):
    config = dotenv.dotenv_values(".env")
    llm = HuggingFaceHub(
        repo_id=config["REPO_ID"],
        huggingfacehub_api_token=config["HF_TOKEN"],
        model_kwargs={
            "temperature": float(config["MODEL_KWARGS_TEMPERATURE"]),
            "min_length": int(config["MODEL_KWARGS_MIN_LENGTH"]),
            "max_length": int(config["MODEL_KWARGS_MAX_LENGTH"]),
            "repetition_penalty": float(config["MODEL_KWARGS_REPETITION_PENALTY"]),
        },
    )
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    docs = db.max_marginal_relevance_search(
        query=query, k=20, fetch_k=50, lambda_mult=0.4
    )
    response = chain.run(input_documents=docs, question=query)
    return response


@time_this
def get_summary(db):
    query = "Summarize the given document while including all the qualifications and skills of the candidate and nothing else. Give just the answer and do not add any context."
    summary = qa_chain(db, query)
    return summary


@time_this
def get_qualification(db):
    query = "What qualification does the candidate have? Give just the answer and do not add any context."
    qualification = qa_chain(db, query)
    return qualification


@time_this
def process(folder_web_id, type=""):
    files_collection = load_files_collection(folder_web_id)
    paths = get_file_paths(files_collection)
    for i, path in enumerate(paths):
        content = read_file(path, files_collection[i])
        content = wrap_text_preserve_newlines(content)
        chunks = split_content(content)
        db = vectorize(chunks)
        summary = get_summary(db)
        qualification = get_qualification(db)
        # data = {
        #     "file_name": path.split("/")[-1],
        #     "file_path": path,
        #     "summary": summary,
        #     "qualification": qualification,
        # }
        with open("outputs.txt", "a+") as fp:
            fp.write(
                f"""
                {path.split('/')[-1]}\n\n
                Summary\n\n
                {summary}\n\n
                -----------------------------------------------------\n\n
                Qualification\n\n
                {qualification}\n\n
                -----------------------------------------------------\n\n
                """
            )


if __name__ == "__main__":
    process("business_analyst")
