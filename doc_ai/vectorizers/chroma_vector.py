from langchain.vectorstores import Chroma
import os

def vectorize(data, embedder, source):
    ds_path = os.getcwd() + '/doc_ai/data'
    if 'chroma.sqlite3' in os.listdir(ds_path):
        db = Chroma(embedding_function=embedder, persist_directory=ds_path)
        if len(db.get(where=source, include=["metadatas"])["ids"]) > 0:
            print("Document already exists! Skipping...\n")
        else:
            db.add_documents(data)
    else:
        db = Chroma.from_documents(data, embedding_function=embedder, persist_directory=ds_path)
        
    db.persist()