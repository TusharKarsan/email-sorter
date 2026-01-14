import { QdrantClient } from '@qdrant/js-client-rest';
import { glob } from 'glob';
import fs from 'fs';

const QDRANT_URL = 'http://design:6333';
const OLLAMA_URL = 'http://design:11434/api/embeddings';
const COLLECTION_NAME = 'email-sorter-code';

const client = new QdrantClient({ url: QDRANT_URL });

async function getEmbedding(text: string) {
  const res = await fetch(OLLAMA_URL, {
    method: 'POST',
    body: JSON.stringify({ model: 'nomic-embed-text:latest', prompt: text })
  });
  const json = await res.json();
  return json.embedding;
}

async function runIndex() {
  // Ensure collection exists
  const collections = await client.getCollections();
  if (!collections.collections.some(c => c.name === COLLECTION_NAME)) {
    await client.createCollection(COLLECTION_NAME, {
      vectors: { size: 768, distance: 'Cosine' } // Nomic uses 768 dims
    });
  }

  const files = await glob('**/*.{ts,py,js,md}', { ignore: ['node_modules/**', '.continue/**'] });
  
  for (const file of files) {
    const content = fs.readFileSync(file, 'utf-8');
    // Basic chunking: one chunk per file for email-sorter logic
    const vector = await getEmbedding(content);
    
    await client.upsert(COLLECTION_NAME, {
      points: [{
        id: Math.floor(Math.random() * 1e9),
        vector,
        payload: { path: file, content }
      }]
    });
    console.log(`Indexed: ${file}`);
  }
}

runIndex();
