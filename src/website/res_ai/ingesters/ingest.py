from glob import iglob
import os
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import textwrap
from vectorizers.vectorise import vectorise
from llm.llm import Query




# import threading

ALLOW = ["**.pdf"]

def wrap_text_preserve_newlines(text, width=110):
    lines = text.split('\n')
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text

def ingest(path,df):
    print("Starting Ingestion")
    path = os.getcwd() + path
    loader = DirectoryLoader(path , loader_cls=PyPDFLoader)
    files = loader.load()
    for i,file in enumerate(files):
        file.page_content = wrap_text_preserve_newlines(file.page_content)
        text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=300)
        docs = text_splitter.split_documents([file])
        vectorised_db = vectorise(docs)
        summary = Query(vectorised_db,'summary')
        qual = Query(vectorised_db,'qual')
        df.loc[len(df.index)] = [files[i].metadata['source'].split('\\')[-1], summary,qual]
    df = df.groupby('Name').agg({'Summary': ' '.join, 'Qualification': ' '.join}).reset_index()
    return df