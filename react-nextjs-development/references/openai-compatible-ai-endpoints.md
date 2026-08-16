# OpenAI-compatible AI endpoint pattern

Use this reference when adding an AI-backed feature to a React/Vite/Next app with a TypeScript server/API layer.

## Durable pattern

1. Keep a deterministic fallback path.
   - If `AI_API_KEY` is absent, return heuristic or rules-based output in the same response shape.
   - This keeps local builds, demos, tests, and unauthenticated preview deploys useful.

2. Treat Kimi, DeepSeek, Nous, and similar providers as OpenAI-compatible chat-completions runtimes.
   - Runtime env shape:
     - `AI_PROVIDER=kimi|deepseek|nous|custom`
     - `AI_API_KEY=`
     - `AI_BASE_URL=` optional override
     - `AI_MODEL=` optional override
   - Useful defaults:
     - Kimi/Moonshot: `https://api.moonshot.cn/v1`, model `moonshot-v1-8k`
     - DeepSeek: `https://api.deepseek.com/v1`, model `deepseek-chat`
     - Nous: `https://inference-api.nousresearch.com/v1`, model `Hermes-4-405B`

3. Make the endpoint robust by default.
   - Use a timeout with `AbortController`.
   - Ask for JSON only, but still tolerate fenced/prose responses by extracting the first JSON object.
   - Normalize and validate returned records before sending them to the frontend.
   - On provider error, return deterministic fallback plus an `ai_error` field rather than failing the whole feature.

4. Wire every layer in the same pass.
   - Server handler.
   - Serverless adapter.
   - Local dev router.
   - Deployment redirects/proxy config.
   - `.env.example`.
   - Architecture/API contract doc.
   - Frontend types and typed API client function.

5. Verify both build and runtime.
   - Run the full workspace build after edits.
   - Start the local API server and POST a representative payload to the endpoint.
   - Verify fallback mode works without credentials.

## TypeScript/Node dev-server pitfall

If source files use ESM imports ending in `.js` for TypeScript compile compatibility, running source directly with `node --experimental-strip-types src/server.ts` can fail because Node resolves `./handler.js` next to the `.ts` source.

Preferred dev script for this pattern:

```json
{
  "scripts": {
    "build": "tsc -p tsconfig.json",
    "dev": "npm run build && node dist/src/dev-server.js",
    "start": "node dist/src/dev-server.js"
  }
}
```

This avoids source-time `.js` import resolution failures while preserving ESM-compatible compiled output.

## Minimal response shape for AI feature endpoints

```ts
interface AiFeatureResponse<T> {
  provider: string;
  model: string | null;
  mode: 'ai' | 'heuristic';
  summary: string;
  recommendations: T[];
  ai_error?: string;
}
```

Keep the frontend consuming this stable shape regardless of runtime mode.
