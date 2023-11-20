from glob import iglob
import os

from utils import timer

# import threading

ALLOW = ["**.pdf", "**.txt", "**.docx", "**.doc"]


@timer.time_this
def ingest(path="/doc_ai/files"):
    path = os.getcwd() + path
    for ext in ALLOW:
        files = iglob(path + "/" + ext)
        if ext.endswith("pdf"):
            from ingesters import pdf_ingest

            for file in files:
                data = pdf_ingest.ingest(file)
                try:
                    from main_vector import vectorize

                    try:
                        vectorize(data)
                    except Exception as e:
                        print("Error:", e)
                except Exception as e:
                    print("Error:", e)
