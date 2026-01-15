import os
import uuid
from qdrant_client import QdrantClient, models

# --- Configuration ---
QDRANT_URL = "http://design:6333"
COLLECTION_NAME = "email-sorter"
MODEL_NAME = "jinaai/jina-embeddings-v2-base-code"

def main():
    client = QdrantClient(url=QDRANT_URL)
    
    # 1. Setup the model locally on Small_One
    print(f"📥 Loading embedding model: {MODEL_NAME}...")
    client.set_model(MODEL_NAME)

    # 2. Ensure Collection exists (Does NOT delete existing data)
    if not client.collection_exists(COLLECTION_NAME):
        print(f"🏗️ Creating collection {COLLECTION_NAME}...")
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=client.get_fastembed_vector_params() 
        )
    else:
        print(f"📚 Using existing collection {COLLECTION_NAME}...")

    # 3. Scan files
    documents = []
    metadata = []
    exclude_dirs = {'.git', '__pycache__', '.continue', '.venv', 'node_modules'}

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

    # 4. The Reliable Upload via Generator
    if documents:
        print(f"🚀 Embedding and Uploading {len(documents)} items to Design PC...")
        
        # We use add() but wrap documents properly to let FastEmbed handle the 'embed' call internally
        client.add(
            collection_name=COLLECTION_NAME,
            documents=documents,
            metadata=metadata,
            ids=[str(uuid.uuid4()) for _ in range(len(documents))]
        )
        print("✅ Indexing complete! Your Agent is now fully synchronized.")
    else:
        print("❌ No files found.")

if __name__ == "__main__":
    main()
