import chromadb

def load_chroma_collection(persist_dir, collection_name="estonian_laws"):
    client = chromadb.PersistentClient(path=persist_dir)
    return client.get_collection(collection_name)