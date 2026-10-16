# Browser examples
# джерело: https://github.com/upstash/box/blob/python-sdk-v0.4.0/packages/sdk/examples/browser/README.md
# отримано: 2026-10-16
# версія: upstash-box-0.4.0, upstash-box-0.3.0, dsh-box-0.1.8, dsh-box-0.1.7, dsh-box-0.1.6, dsh-box-0.1.5, dsh-box-0.1.4, dsh-box-0.1.3, dsh-box-0.1.2, dsh-box-0.1.1, dsh-box-0.1.0, box-pi-0.1.15, box-pi-0.1.14, box-pi-0.1.13, box-pi-0.1.12, box-pi-0.1.11, box-pi-0.1.10, box-pi-0.1.9, box-pi-0.1.8, box-pi-0.1.7, box-pi-0.1.6, box-cli-0.3.5, box-cli-0.3.4, box-cli-0.3.3, box-cli-0.3.2, box-cli-0.3.1, box-cli-0.3.0, box-cli-0.2.24, box-cli-0.2.23, box-cli-0.2.22, box-cli-0.2.21, box-cli-0.2.20, box-cli-0.2.19, box-0.7.9, box-0.7.8, box-0.7.7, box-0.7.6, box-0.7.5, box-0.7.4, box-0.7.3, box-0.7.2, box-0.7.1, box-0.7.0

Runnable examples for the Box browser, grouped by use case. Every file is
self-contained: paste it, run it, read the output.

```bash
export UPSTASH_BOX_API_KEY=...   # or use: node --env-file=.env <file>
node retrieval/01-catalog-extraction.ts
```

## Prerequisites

- All examples need `UPSTASH_BOX_API_KEY`.
- Examples marked **AI** below use metered browser AI (`act`, `extract`,
  `observe`) and need a model provider key configured on the box or account.
- `agentic/01-in-box-agent.ts` is different: it drives the browser through the
  box's coding agent, so it needs an agent harness + key and bills coding-agent
  tokens, not browser-AI metering.
- Everything else runs with the Box key alone.

## agentic/ — goal-driven browsing (replacing the removed agent loop)

Stagehand v4 removed the built-in agent loop. Two replacements, matching v4's
guidance:

| File | AI | What it shows |
| --- | --- | --- |
| `01-in-box-agent.ts` | coding agent | Hand a goal to the box's in-sandbox agent; `browser: true` wires the chrome-devtools MCP, so it drives the browser itself and writes results to the box. Needs an agent harness + key |
| `02-build-your-own-loop.ts` | yes | A live `observe` then `act(action)` then `extract` loop you own, bounded by a step budget with `extract` as the stop check. Model in the loop |

## automation/ — forms, files, and durable sessions

| File | AI | What it shows |
| --- | --- | --- |
| `01-checkout-with-one-ai-step.ts` | one `act` | Script the deterministic steps, delegate the judgment call, assert the result |
| `02-download-and-process.ts` | no | A download lands on the box filesystem and is processed in place |
| `03-upload-from-box.ts` | no | Upload a box-generated file through a real form via CDP |
| `04a-login-once-keep-alive.ts` + `04b-reuse-session.ts` | no | Log in once into a keep-alive box; any later script reuses the session. **04a leaves a box running** (id in `.box-workspace`) — delete it when done |

## retrieval/ — structured data out of rendered pages

| File | AI | What it shows |
| --- | --- | --- |
| `01-catalog-extraction.ts` | yes | One `extract` call, schema-validated typed output, screenshot provenance |
| `02-ai-compiled-scraper.ts` | first run only | AI compiles selectors once; every later run scrapes deterministically. Run twice. **Leaves a box** holding the recipe (`.box-compiled-scraper`) |
| `03-crawl-to-dataset.ts` | no | Crawl a client-rendered docs section into chunked JSONL via `tab.content()` |
| `04-evidence-pack.ts` | no | Full-page captures + hashed manifest, assembled in the box, downloaded as one archive |

## testing/ — the box as a test environment

| File | AI | What it shows |
| --- | --- | --- |
| `01-playwright-migration.ts` | no | An existing Playwright test where only the launch line changes |
| `02-test-your-own-app.ts` | no | The box hosts the app under test and browses it on its own localhost |
| `04-visual-regression.ts` | no | Pixelmatch diffs against baselines stored on the box. Run twice. **Leaves a box** holding baselines (`.box-visual-regression`) |

## Cleanup

Three examples intentionally keep a box between runs. Remove them when done:

```bash
for f in .box-workspace .box-compiled-scraper .box-visual-regression; do
  [ -f "$f" ] && node --input-type=module -e "
import { Box } from '@upstash/box';
import { readFile, unlink } from 'node:fs/promises';
const id = (await readFile('$f', 'utf8')).trim();
await (await Box.get(id)).delete(); await unlink('$f');
console.log('deleted', id);"
done
```
