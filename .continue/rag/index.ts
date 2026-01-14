import { QdrantClient } from '@qdrant/js-client-rest';
import { glob } from 'glob';
import fs from 'fs';
import crypto from 'crypto';
import path from 'path';

const QDRANT_URL = 'http://design:6333';
const OLLAMA_URL = 'http://design:11434/api/embeddings';
const COLLECTION_NAME = path.basename(process.cwd());

const client = new QdrantClient({ url: QDRANT_URL });

// Helper: Consistent UUID for upserting (overwriting)
function generateId(filePath: string, chunkIndex: number): string {
  const seed = `${filePath}_${chunkIndex}`;
  // Create a consistent UUID v5 using a fixed namespace UUID
  const NAMESPACE = '6ba7b810-9dad-11d1-80b4-00c04fd430c8'; // Standard DNS namespace
  
  // Alternatively, for a quick fix without extra libraries, 
  // format your MD5 hash to look like a UUID:
  const hash = crypto.createHash('md5').update(seed).digest('hex');
  return [
    hash.substring(0, 8),
    hash.substring(8, 12),
    hash.substring(12, 16),
    hash.substring(16, 20),
    hash.substring(20, 32)
  ].join('-');
}

async function getEmbedding(text: string) {
  const res = await fetch(OLLAMA_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'nomic-embed-text:latest', prompt: text, stream: false })
  });
  const json = await res.json();
  const vector = json.embedding || (json.embeddings && json.embeddings[0]);
  if (!vector) throw new Error("Ollama returned empty embedding");
  return vector;
}

async function runIndex() {
  // 1. Ensure Collection exists
  const collections = await client.getCollections();
  if (!collections.collections.some(c => c.name === COLLECTION_NAME)) {
    await client.createCollection(COLLECTION_NAME, {
      vectors: { size: 768, distance: 'Cosine' }
    });
  }

  const files = await glob('**/*.{ts,py,js,md}', { 
    ignore: ['node_modules/**', '.continue/**', 'dist/**'] 
  });

  for (const file of files) {
    const content = fs.readFileSync(file, 'utf-8');
    if (!content.trim()) continue;

    // 2. Clear old vectors for THIS specific file before re-indexing
    await client.delete(COLLECTION_NAME, {
      filter: { must: [{ key: "path", match: { value: file } }] }
    });

    // 3. Chunk and Upsert
    const chunks = content.match(/[\s\S]{1,2000}/g) || [];
    for (let j = 0; j < chunks.length; j++) {
      const vector = await getEmbedding(chunks[j]);
      await client.upsert(COLLECTION_NAME, {
        points: [{
          id: generateId(file, j),
          vector,
          payload: { path: file, content: chunks[j] }
        }]
      });
    }
    console.log(`Indexed: ${file}`);
  }
}

runIndex();
