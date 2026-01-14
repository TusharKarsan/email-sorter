import fs from "fs";
import path from "path";
import crypto from "crypto";
import { QdrantClient } from "@qdrant/js-client-rest";
import { minimatch } from "minimatch";

const config = require("./config.json");

const client = new QdrantClient({ url: config.vectorDb.url });

function normalize(p: string) {
  return p.replace(/\\/g, "/");
}

async function ensureCollection() {
  try {
    await client.getCollection(config.vectorDb.collection);
    console.log("Collection exists:", config.vectorDb.collection);
  } catch {
    console.log("Creating collection:", config.vectorDb.collection);

    await client.createCollection(config.vectorDb.collection, {
      vectors: {
        size: 768,
        distance: "Cosine"
      }
    });
  }
}

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

  if (!json.embeddings || json.embeddings.length === 0) {
    throw new Error("Embedding failed: empty vector");
  }

  return json.embeddings[0];
}

function chunk(text: string, size: number, overlap: number) {
  const chunks = [];
  let i = 0;
  while (i < text.length) {
    chunks.push(text.slice(i, i + size));
    i += size - overlap;
  }
  return chunks;
}

async function indexFile(filePath: string) {
  const norm = normalize(filePath);

  // 1. Delete old vectors for this file
  await client.delete(config.vectorDb.collection, {
    filter: {
      must: [
        {
          key: "file",
          match: { value: norm }
        }
      ]
    }
  });

  // 2. Read and chunk file
  const text = fs.readFileSync(filePath, "utf8");
  const chunks = chunk(text, config.chunkSize, config.chunkOverlap);

  // 3. Embed and upsert
  for (const chunkText of chunks) {
    const vector = await embed(chunkText);

    await client.upsert(config.vectorDb.collection, {
      points: [
        {
          id: crypto.randomUUID(),
          vector,
          payload: {
            file: norm,
            text: chunkText
          }
        }
      ]
    });
  }
}

function walk(dir: string, fileList: string[] = [], ignore: string[] = []) {
  for (const file of fs.readdirSync(dir)) {
    const full = path.join(dir, file);
    const norm = normalize(full);

    if (ignore.some(ig => minimatch(norm, ig))) {
      continue;
    }

    if (fs.statSync(full).isDirectory()) {
      walk(full, fileList, ignore);
    } else {
      fileList.push(full);
    }
  }
  return fileList;
}

async function main() {
  await ensureCollection();

  const globs = config.fileGlobs;
  const ignore = config.ignore || [];

  const files = walk(path.join(process.cwd(), "src"), [], ignore);

  const matched = files.filter(f => {
    const norm = normalize(f);
    return (
      globs.some((g: string) => minimatch(norm, g)) &&
      !ignore.some((ig: string) => minimatch(norm, ig))
    );
  });

  for (const file of matched) {
    console.log("Indexing:", file);
    await indexFile(file);
  }

  console.log("Done.");
}

main();
