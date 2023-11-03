from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def loader(file):
    return UnstructuredPDFLoader(file).load()

def splitter(obj):
    return RecursiveCharacterTextSplitter(chunk_size=250, chunk_overlap=50).split_documents(obj)

def ingest(fp):
    obj = loader(fp)
    return splitter(obj)