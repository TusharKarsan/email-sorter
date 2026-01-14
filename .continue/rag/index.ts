import { QdrantClient } from '@qdrant/js-client-rest';
import { glob } from 'glob';
import fs from 'fs';
import path from 'path';

const QDRANT_URL = 'http://design:6333';
const OLLAMA_URL = 'http://design:11434/api/embeddings';
const COLLECTION_NAME = path.basename(process.cwd());

const client = new QdrantClient({ url: QDRANT_URL });

async function getEmbedding(text: string) {
  const res = await fetch(OLLAMA_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      model: 'nomic-embed-text:latest', 
      prompt: text,
      stream: false
    })
  });

  const json = await res.json();
  
  // Ollama returns { "embedding": [...] } or { "embeddings": [[...]] }
  // We handle both just in case
  const vector = json.embedding || (json.embeddings && json.embeddings[0]);

  if (!vector || vector.length === 0) {
    throw new Error(`Ollama returned an empty embedding for text: ${text.substring(0, 30)}...`);
  }
  
  return vector;
}

// Helper function to split text into manageable chunks
function chunkText(text: string, size: number = 2000): string[] {
  const chunks: string[] = [];
  for (let i = 0; i < text.length; i += size) {
    chunks.push(text.slice(i, i + size));
  }
  return chunks;
}

async function runIndex() {
  // Ensure collection exists (keep your existing check here...)

  const files = await glob('**/*.{ts,py,js,md}', { 
    ignore: ['node_modules/**', '.continue/**', 'dist/**', 'build/**'] 
  });
  
  for (const file of files) {
    const content = fs.readFileSync(file, 'utf-8');
    
    // Skip empty files
    if (!content.trim()) continue;

    // Split large files into chunks
    const chunks = chunkText(content);
    
    for (let j = 0; j < chunks.length; j++) {
      try {
        const vector = await getEmbedding(chunks[j]);
        
        await client.upsert(COLLECTION_NAME, {
          points: [{
            id: Math.floor(Math.random() * 1e9),
            vector,
            payload: { 
              path: file, 
              content: chunks[j],
              chunkIndex: j 
            }
          }]
        });
      } catch (err: any) {
        console.error(`Failed to index chunk ${j} of ${file}:`, err.message);
      }
    }
    console.log(`Indexed: ${file} (${chunks.length} chunks)`);
  }
}

runIndex();
