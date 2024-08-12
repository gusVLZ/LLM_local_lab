import chromadb
from chromadb.config import Settings

# Initialize the Chroma DB client
client = chromadb.PersistentClient(path="./db_data")

collection = client.get_or_create_collection("historia")

def change_collection(collection_name):
    global client
    global collection
    collection = client.get_or_create_collection(collection_name)
    return True

def batch_insert(ids, document, metadata):
    global client
    global collection
    collection.add(ids=ids, documents=document, metadatas=metadata)

def read(query):
    global client
    global collection
    return collection.query(query)

def update(query, updated_vector):
    global client
    global collection
    collection.update(query, updated_vector)

def delete(query):
    global client
    global collection
    collection.delete(query)

def delete_collection(collection_name):
    global client
    client.delete_collection(collection_name)
