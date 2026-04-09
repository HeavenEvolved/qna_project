from langchain.llms import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain
import os 

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "SECRET"
llm=HuggingFaceHub(repo_id="MBZUAI/LaMini-Flan-T5-248M", model_kwargs={"temperature":0.6, "max_length":512})


#summary_query = "Give the Summary of the document along with work experience and projects worked on"
#qual_query = "What qualification does the candidate have"
qual_query = "What qualification should the candidate have"
summary_query = "Give the Summary of the document for necessary skills required"

def Query(db,query):
    print("Start LLM Querying")
    if query == 'summary':
        query = summary_query
    else:
        query = qual_query
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = db.similarity_search(query)
    response = chain.run(input_documents=docs, question=query).replace(". ", ".\n") 
    return response
