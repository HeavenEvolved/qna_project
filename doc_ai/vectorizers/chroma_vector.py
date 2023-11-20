from langchain.vectorstores import Chroma
import os

from utils import timer


@timer.time_this
def vectorize(data, embedder, source):
    ds_path = os.getcwd() + "/doc_ai/data"
    if "chroma.sqlite3" in os.listdir(ds_path):
        db = Chroma(embedding_function=embedder, persist_directory=ds_path)
        if len(db.get(where=source, include=["metadatas"])["ids"]) > 0:
            print("Document already exists! Skipping...")
        else:
            db.add_documents(data)
    else:
        db = Chroma.from_documents(data, embedding=embedder, persist_directory=ds_path)

    db.persist()
