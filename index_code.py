import os
import uuid
from qdrant_client import QdrantClient, models

# --- Configuration ---
QDRANT_URL = "http://design:6333"
COLLECTION_NAME = "email-sorter"
MODEL_NAME = "jinaai/jina-embeddings-v2-base-code"
VECTOR_NAME = "fast-jina-embeddings-v2-base-code"
BATCH_SIZE = 1

def main():
    client = QdrantClient(url=QDRANT_URL, timeout=60)
    
    # 1. Ensure Collection exists
    print(f"🏗️ Recreating collection {COLLECTION_NAME}...")
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=client.get_fastembed_vector_params(),
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
            ids=[str(uuid.uuid4()) for _ in range(len(documents))],
            batch_size=BATCH_SIZE
        )
        print("✅ Indexing complete!")
    else:
        print("❌ No files found.")

if __name__ == "__main__":
    main()
