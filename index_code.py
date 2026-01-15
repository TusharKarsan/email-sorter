import os
from qdrant_client import QdrantClient

# Configuration
COLLECTION_NAME = "email-sorter"
DESIGN_PC_URL = "http://design:6333"

client = QdrantClient(url=DESIGN_PC_URL)

def index_files():
    documents = []
    metadata = []
    
    # Loop through your python files
    for root, dirs, files in os.walk("."):
        if ".git" in root or "__pycache__" in root or ".continue" in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    code = f.read()
                    documents.append(code)
                    metadata.append({"path": path, "filename": file})

    # Upload to Qdrant (this will auto-embed them using FastEmbed)
    client.add(
        collection_name=COLLECTION_NAME,
        documents=documents,
        metadata=metadata,
    )
    print(f"✅ Indexed {len(documents)} files to Design PC.")

if __name__ == "__main__":
    index_files()
