from glob import iglob
import os
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
import textwrap
from vectorizers import vectorise
from llm import LLM


from utils import timer

# import threading

ALLOW = ["**.pdf"]

def wrap_text_preserve_newlines(text, width=110):
    lines = text.split('\n')
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text

@timer.time_this
def ingest(path,df):
    data = LLM(1,'summary')
    return
    path = os.getcwd() + path
    for ext in ALLOW:
        files = iglob(path + "/" + ext)
        if ext.endswith("pdf"):
            loader = DirectoryLoader(path , loader_cls=PyPDFLoader)
            files = loader.load()
            for i,file in enumerate(files):
                file.page_content = wrap_text_preserve_newlines(file.page_content)
                text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=300)
                docs = text_splitter.split_documents([file])
                vectorised_db = vectorise(docs)
                summary = LLM(vectorised_db,'summary')
                qual = LLM(vectorised_db,'qual')
                df.loc[len(df.index)] = [files[i].metadata['source'].split('\\')[-1], summary,qual]
            df = df.groupby('Name').agg({'Summary': ' '.join, 'Qualification': ' '.join}).reset_index()

                