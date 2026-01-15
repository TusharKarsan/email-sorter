import os
import uuid
from qdrant_client import QdrantClient, models

# --- Configuration ---
QDRANT_URL = "http://design:6333"
COLLECTION_NAME = "email-sorter"
MODEL_NAME = "jinaai/jina-embeddings-v2-base-code"
# This is the EXACT name the library is demanding in your error log:
VECTOR_NAME = "fast-jina-embeddings-v2-base-code"

def main():
    client = QdrantClient(url=QDRANT_URL)
    
    print(f"📥 Loading embedding model: {MODEL_NAME}...")
    client.set_model(MODEL_NAME)

    # 1. DELETE and RECREATE one last time to fix the name mismatch
    print(f"♻️ Resetting collection with correct vector name: {VECTOR_NAME}")
    client.delete_collection(COLLECTION_NAME)
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            VECTOR_NAME: models.VectorParams(size=768, distance=models.Distance.COSINE)
        }
    )

    # 2. Scan files
    documents = []
    metadata = []
    exclude_dirs = {'.git', '__pycache__', '.continue', '.venv', 'node_modules', 'dist', 'build'}

    print(f"🔍 Scanning project...")
    for root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith((".py", ".md")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if content.strip():
                            documents.append(content)
                            metadata.append({"path": path, "filename": file})
                except Exception as e:
                    print(f"⚠️ Error reading {path}: {e}")

    # 3. Upload
    if documents:
        print(f"🚀 Uploading to Design PC...")
        client.add(
            collection_name=COLLECTION_NAME,
            documents=documents,
            metadata=metadata,
            ids=[str(uuid.uuid4()) for _ in range(len(documents))]
            # We don't need to specify vector_name here; 
            # client.add() will pick the Jina name automatically now.
        )
        print("✅ Indexing complete!")
    else:
        print("❌ No files found.")

if __name__ == "__main__":
    main()
