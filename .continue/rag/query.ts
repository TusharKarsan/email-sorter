import { QdrantClient } from '@qdrant/js-client-rest';
import path from 'path';

const QDRANT_URL = 'http://design:6333';
const OLLAMA_URL = 'http://design:11434/api/embeddings';
const GENERATE_URL = 'http://design:11434/api/generate';
const COLLECTION_NAME = path.basename(process.cwd());

const client = new QdrantClient({ url: QDRANT_URL });

/**
 * Stage 1: Convert query to vector
 */
async function getEmbedding(text: string) {
  const res = await fetch(OLLAMA_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: 'nomic-embed-text:latest', prompt: text, stream: false })
  });
  const json = await res.json();
  return json.embedding || (json.embeddings && json.embeddings[0]);
}

/**
 * Stage 2: Rerank using LLM (Llama 3.1)
 * Returns a simple array of indices [0, 2, 5...]
 */
async function rerank(query: string, documents: {path: string, content: string}[]) {
  const prompt = `
    User Query: "${query}"
    
    Code Snippets:
    ${documents.map((d, i) => `[${i}] ${d.path}\n${(d.content || "").substring(0, 300)}...`).join('\n\n')}
    
    Task: Identify the top 5 most relevant snippet indices to answer the query.
    Return ONLY a JSON array of integers, e.g. [0, 5, 2].
  `;

  const res = await fetch(GENERATE_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'llama3.1:latest',
      prompt: prompt,
      stream: false,
      format: 'json'
    })
  });

  const json = await res.json();
  try {
    // Regex to find the array in case the LLM adds text
    const match = json.response.match(/\[.*\]/s);
    if (match) {
      return JSON.parse(match[0]);
    }
    return JSON.parse(json.response);
  } catch (e) {
    console.error("Reranker parse failed, using fallback.");
    return [0, 1, 2, 3, 4];
  }
}

async function main() {
  const userQuery = process.argv.slice(2).join(" ");
  if (!userQuery) return;

  const startTime = Date.now();

  try {
    // 1. Vector Retrieval
    const vector = await getEmbedding(userQuery);
    const searchResults = await client.search(COLLECTION_NAME, {
      vector,
      limit: 15,
      with_payload: true
    });

    if (searchResults.length === 0) {
      process.stdout.write("No relevant code found.");
      return;
    }

    // 2. Prepare for Rerank
    const docsToRerank = searchResults.map(r => ({
      path: r.payload?.path as string,
      content: r.payload?.content as string
    }));

    // 3. Perform Rerank
    const bestIndices = await rerank(userQuery, docsToRerank);

    // 4. Construct Final Context
    const finalContext = (Array.isArray(bestIndices) ? bestIndices : [0, 1, 2, 3, 4])
      .filter((idx: number) => searchResults[idx]) // Prevent out-of-bounds
      .slice(0, 5)
      .map((index: number) => {
        const doc = searchResults[index];
        return `File: ${doc.payload?.path}\n\n${doc.payload?.content}`;
      })
      .join('\n---\n');

    const duration = Date.now() - startTime;
    
    // Add a small header for your own visibility (Continue.dev ignores console.error)
    console.error(`\n[RAG] Query took ${duration}ms\n`);

    process.stdout.write(finalContext);

  } catch (error: any) {
    console.error(`Query Error: ${error.message}`);
    process.exit(1);
  }
}

main();
