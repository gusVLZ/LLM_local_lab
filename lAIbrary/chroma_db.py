import chromadb
from chromadb.config import Settings
import ollama

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

    embeddings = []
    print("starting embedding of ", len(document), " documents")
    for i, d in enumerate(document):
        embedding = ollama.embeddings(
            model='mxbai-embed-large',
            prompt=d,
        )
        print(embedding)
        embeddings.append(embedding["embedding"] if len(embedding["embedding"]) > 0 else ([0] * 1024))
        print(i, len(document))


    collection.add(ids=ids, documents=document, metadatas=metadata, embeddings=embeddings)

def read(query, size=3):
    global client
    global collection

    embedding = ollama.embeddings(
        model='mxbai-embed-large',
        prompt=query,
    )

    return collection.query(
        query_embeddings = [embedding["embedding"]],
        #query_texts=[query],
        n_results=size
    )

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

if __name__ == "__main__":
    id = "meucachorro:0:0"
    documento = """
Cachorros usam chatgpt para conversar com seus donos, pedir comida no ifood e para estudar formas de conseguir convencer seu dono a alimentá-lo com um osso 
"""
    meta={
        "title": "cachorro gpt",
        "page": 1,
        "paragraph": 1,
        "subject": "dogs"
    }
    batch_insert([id], [documento], [meta])