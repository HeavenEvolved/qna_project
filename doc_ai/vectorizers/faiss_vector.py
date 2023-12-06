from langchain.vectorstores import Faiss
import os

from utils import timer


@timer.time_this
def vectorize(data, embedder, source):
    ds_path = os.getcwd() + "/doc_ai/data"
    # print(os.listdir(ds_path))
    if "index.faiss" in os.listdir(ds_path):
        db = Faiss.load_local(folder_path=ds_path, embeddings=embedder)
        print("Loaded Old DB")
        if len(db.get(where=source, include=["metadatas"])["ids"]) > 0:
            print("Document already exists! Skipping...")
        else:
            db.add_documents(data)
    else:
        db = Faiss.from_documents(data, embedding=embedder)
        print("Created New DB")

    db.save_local(ds_path)
