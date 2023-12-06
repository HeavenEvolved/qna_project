from glob import iglob
import os

from utils import timer

# import threading

ALLOW = ["**.pdf", "**.txt", "**.docx", "**.doc"]


@timer.time_this
def ingest(path="/doc_ai/files/"):
    path = os.getcwd() + path
    # print(path)
    for ext in ALLOW:
        try:
            files = iglob(path + ext)
            # print(next(files))
        except Exception as e:
            print(e)
        if ext.endswith("pdf"):
            try:
                from ingesters import pdf_ingest

                # print("Loaded Ingester")
            except Exception as e:
                print("Error:", e)

            for file in files:
                try:
                    data = pdf_ingest.ingest(file)
                    # print(data)
                except Exception as e:
                    print(e)
                try:
                    from main_vector import vectorize

                    try:
                        vectorize(data)
                    except Exception as e:
                        print("Error:", e)
                except Exception as e:
                    print("Error:", e)

        elif ext.endswith("txt"):
            try:
                from ingesters import text_ingest

                # print("Loaded Ingester")
            except Exception as e:
                print("Error:", e)

            for file in files:
                try:
                    data = text_ingest.ingest(file)
                    # print(data)
                except Exception as e:
                    print(e)
                try:
                    from main_vector import vectorize

                    try:
                        vectorize(data)
                    except Exception as e:
                        print("Error:", e)
                except Exception as e:
                    print("Error:", e)

        elif ext.endswith("docx") or ext.endswith("doc"):
            try:
                from ingesters import word_ingest

                # print("Loaded Ingester")
            except Exception as e:
                print("Error:", e)

            for file in files:
                try:
                    data = word_ingest.ingest(file)
                    # print(data)
                except Exception as e:
                    print(e)
                try:
                    from main_vector import vectorize

                    try:
                        vectorize(data)
                    except Exception as e:
                        print("Error:", e)
                except Exception as e:
                    print("Error:", e)
