# Old Code Commented Out

Old scripts for reference:

```json
scripts: {
    "index": "conda activate email-sorter && python index_code.py",
    "index2": "tsx .continue/rag/index.ts",
    "query": "tsx .continue/rag/query.ts",
    "watch": "npx chokidar \"**/*.{py,ts,md}\" -c \"npm run index\" --ignore \".continue/**\" --delay 5000"
}
```

To see pakcages installed, run:

```PowerShell
conda list -n email-sorter
```
