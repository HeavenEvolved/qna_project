import pymongo
from glob import iglob
import os
import base64
import gridfs
import hashlib
from langchain.document_loaders import UnstructuredPDFLoader
from unstructured.cleaners.core import clean, clean_non_ascii_chars

client = pymongo.MongoClient("localhost:27017")

db = client["file_store"]

collections = list(filter(lambda x: "." not in x, db.list_collection_names()))
print(collections)


fs = gridfs.GridFS(database=db, collection="data_science")
# Note, open with the "rfs.GridFS(db)
# Note, open with the "rb" flag for "read bytes"
f_path = os.path.abspath("doc_ai/files/")
print(f_path)
files = iglob(f_path + "/**.pdf")


# Function to calculate the MD5 hash of a file's content
def calculate_hash(content):
    md5 = hashlib.md5()
    md5.update(content.encode())
    return md5.hexdigest()


def loader(file):
    return UnstructuredPDFLoader(
        file,
        mode="single",
        post_processors=[
            clean_non_ascii_chars,
            lambda x: clean(
                x,
                extra_whitespace=True,
            ),
        ],
    ).load()


for collection in collections:
    curr_col = db[collection]

    for file in files:
        doc = loader(file)
        content = doc[0].page_content
        source = doc[0].metadata["source"].split("/")[-1]
        del doc
        doc_hash = calculate_hash(content)

        print(source, doc_hash)

        if curr_col.find_one({"hash": doc_hash}):
            print("Duplicate file detected")
            continue

        file_id = fs.put(content, filename=source, encoding="utf8")

        metadata = {
            "filename": source,
            "hash": doc_hash,
            "file_id": file_id,
        }

        curr_col.insert_one(metadata)
        

