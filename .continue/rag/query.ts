import { QdrantClient } from "@qdrant/js-client-rest";
import { minimatch } from "minimatch";

const config = require("./config.json");

const client = new QdrantClient({ url: config.vectorDb.url });

async function embed(text: string) {
  const response = await fetch("http://design:11434/api/embed", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "nomic-embed-text:latest",
      input: [text]
    })
  });

  const json = await response.json();
  return json.embeddings[0];
}

async function rerank(query: string, docs: any[]) {
  const response = await fetch("http://design:11434/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "dengcao/Qwen3-Reranker-8B:Q8_0",
      prompt: buildRerankPrompt(query, docs)
    })
  });

  const json = await response.json();
  return JSON.parse(json.response);
}

function buildRerankPrompt(query: string, docs: any[]) {
  const items = docs
    .map((d, i) => `Document ${i}:\n${d.payload.text}`)
    .join("\n\n");

  return `
Rank the following documents by relevance to the query.

Query:
${query}

Documents:
${items}

Return ONLY a JSON array of document indices.
  `.trim();
}

export async function retrieve(query: string) {
  const vector = await embed(query);

  const search = await client.search(config.vectorDb.collection, {
    vector,
    limit: 20
  });

  if (!search || !Array.isArray(search) || search.length === 0) {
    return [];
  }

  const reranked = await rerank(query, search);

  return reranked.slice(0, 5).map((i: number) => {
    const item = search[i];
    if (!item || !item.payload) return null;
    return {
      file: item.payload.file,
      text: item.payload.text
    };
  });
}
