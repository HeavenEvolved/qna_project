from langchain.document_loaders import UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from unstructured.cleaners.core import clean, clean_non_ascii_chars


def loader(file):
    return UnstructuredWordDocumentLoader(
        file,
        post_processors=[
            clean_non_ascii_chars,
            lambda x: clean(
                x,
                extra_whitespace=True,
            ),
        ],
    ).load()


def splitter(obj):
    return RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100
    ).split_documents(obj)


def ingest(fp):
    obj = loader(fp)
    return splitter(obj)
