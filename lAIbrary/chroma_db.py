import chromadb
from chromadb.config import Settings

# Initialize the Chroma DB client
client = chromadb.Client(Settings())

def create_collection(collection_name):
    global client
    return client.get_or_create_collection(collection_name)

def insert_vector(collection, document, metadata):
    global client
    collection.insert(document, metadata)

def read_vectors(collection, query):
    global client
    return collection.query(query)

def update_vector(collection, query, updated_vector):
    global client
    collection.update(query, updated_vector)

def delete_vector(collection, query):
    global client
    collection.delete(query)

def delete_collection(collection_name):
    global client
    client.delete_collection(collection_name)
