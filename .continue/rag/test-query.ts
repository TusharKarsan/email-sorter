// test-query.ts
import { retrieve } from "./query";

async function main() {
  const query = process.argv.slice(2).join(" ").trim();
  if (!query) {
    console.error("Usage: npx tsx test-query.ts \"your question here\"");
    process.exit(1);
  }

  const results = await retrieve(query);
  console.log(JSON.stringify(results, null, 2));
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
