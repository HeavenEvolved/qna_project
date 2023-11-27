from glob import iglob
from langchain.embeddings import HuggingFaceEmbeddings
import pandas as pd
#embeddings = HuggingFaceEmbeddings()
from ingesters.ingest import ingest

try:
    choice = str(
        input("Write Folder to using Resume Analytics on:")
    )

    folder_path = f"\\res_ai\\files\\{choice}"
    df = pd.DataFrame(columns = ['Name', 'Summary','Qualification'],index = None)
    df  = ingest(folder_path,df)
    df.to_excel("res_ai\data\DS_Resume_Table\DS_Summ.xlsx", index = False)    

except Exception as e:
    pass
