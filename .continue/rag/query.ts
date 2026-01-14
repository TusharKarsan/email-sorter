import { QdrantClient } from '@qdrant/js-client-rest';

const QDRANT_URL = 'http://design:6333';
const OLLAMA_URL = 'http://design:11434/api/embeddings';
const COLLECTION_NAME = 'email-sorter-code';

const client = new QdrantClient({ url: QDRANT_URL });

async function query() {
  const userQuery = process.argv[2]; // Continue passes query as first arg
  
  // 1. Embed the query
  const res = await fetch(OLLAMA_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'nomic-embed-text:latest', prompt: userQuery, stream: false })
  });
  const json = await res.json();
  const embedding = json.embedding || (json.embeddings && json.embeddings[0]);

  // 2. Search Qdrant
  const results = await client.search(COLLECTION_NAME, {
    vector: embedding,
    limit: 3,
    with_payload: true
  });

  // 3. Format for Continue.dev
  const context = results.map(r => (
    `File: ${r.payload?.path}\n\n${r.payload?.content}`
  )).join('\n---\n');

  process.stdout.write(context);
}

query();
