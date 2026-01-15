import os
from qdrant_client import QdrantClient
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore

# Connection to your Design PC
client = QdrantClient(url="http://design:6333")
collection_name = "email-sorter"

# Load your local code
documents = SimpleDirectoryReader("./", recursive=True, required_exts=[".py", ".md"]).load_data()

# Setup Qdrant as the storage backend
vector_store = QdrantVectorStore(client=client, collection_name=collection_name)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# Create the index (This performs the bulk upload)
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)

print(f"Successfully indexed {len(documents)} documents to {collection_name} on Design PC.")
