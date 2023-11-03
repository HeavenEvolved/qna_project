ALLOW = ['**.pdf', '**.txt', '**.docx', '**.doc']

from glob import iglob
import os
import threading
import time

def ingest(path = '/doc_ai/files'):
    path = os.getcwd() + path
    
    for ext in ALLOW:
        
        files = iglob(path+'/'+ext)
        
        if ext.endswith('pdf'):
            from ingesters import pdf_ingest
            for file in files:
                data = pdf_ingest.ingest(file)
                from main_vector import vectorize
                try:
                    start = time.time()
                    print(f"\nStart time: {start:.3f}\n")
                    vectorize(data)
                    end = time.time()
                    print(f"End time: {end:.3f}\n")
                    
                    print(f"It took {end-start:.3f} seconds to complete the Vectorization.\n\n")
                except Exception as e:
                    print(e)
    
if __name__ == '__main__':
    ingest()