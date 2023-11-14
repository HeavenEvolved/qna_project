from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def loader(file):
    return UnstructuredPDFLoader(file, strategy="ocr_only").load()


def splitter(obj):
    return RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=250
    ).split_documents(obj)


def ingest(fp):
    obj = loader(fp)
    return splitter(obj)
