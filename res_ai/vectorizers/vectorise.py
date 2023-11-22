from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings()


def vectorise(docs):
    db = FAISS.from_documents(docs,embeddings)
    return db