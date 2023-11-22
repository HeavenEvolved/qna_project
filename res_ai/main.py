from glob import iglob
from langchain.embeddings import HuggingFaceEmbeddings
import pandas as pd
#embeddings = HuggingFaceEmbeddings()

from ingesters import ingest

try:
    choice = str(
        input("Write Folder to using Resume Analytics on:")
    )

    folder_path = "\\res_ai\\files\\" + choice
    df = pd.DataFrame(columns = ['Name', 'Summary','Qualification'],index = None)
    
    df  = ingest(folder_path,df)


    

except Exception as e:
    pass
