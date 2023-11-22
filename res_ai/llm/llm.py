from langchain.llms import HuggingFaceHub
from langchain.chains.question_answering import load_qa_chain


llm=HuggingFaceHub(repo_id="MBZUAI/LaMini-Flan-T5-248M", model_kwargs={"temperature":1.0, "max_length":512})


summary_query = "Give the Summary of the document along with work experience and projects worked on"
qual_query = "What qualification does the candidate have"

def LLM(db,query):
    print("this is running")
    return
    if query == 'summary':
        query = summary_query
    else:
        query = qual_query
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = db.similarity_search(query)
    response = chain.run(input_documents=docs, question=query).replace(". ", ".\n") 
    return response