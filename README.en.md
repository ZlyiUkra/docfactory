# docfactory — a factory of MCP documentation servers

*The documentation in this repository is written in Ukrainian; this page is the short English entry point. For the
full story see [README.md](README.md) (architecture, protection layers, roadmap) and [UPDATE.md](UPDATE.md) (how
to keep the corpus current).*

One engine, many isolated servers. Each server answers questions about one body of documentation — the ECMAScript
specification (ECMA-262, ECMA-402 and the Unicode, IETF and Ecma documents they build on) and the React
documentation of every version, from 0.3 to 19.3, with its blog, changelog and release notes — over MCP: search
over a local corpus plus four protection layers. Domains never mix: the code is shared, everything else belongs to
one *instance* under `instances/<domain>/`.

## What it is for

Not "documentation search", even though it looks like one. A model that does not know the limits of what it was
given does not stay silent — it invents: asked about a section it does not have, it names the neighbouring one
with the same confidence. Everything here makes such an answer hard to produce:

- the corpus holds normative documents only — the specification and the standards it references; no tutorials,
  no articles, no comments from the web;
- the unit of an answer is a clause with its section number, document title, source URL and fetch date, so every
  quotation can be checked in a minute — and a year later;
- the tool descriptions are long on purpose: they tell the model when *not* to call the tool (browsers, the DOM,
  Node.js, TypeScript — none of it is here, and a search would return unrelated sections with confident-looking
  numbers) and to build the answer out of the excerpts that came back, not out of memory;
- the second of four protection layers rejects `read_section` on an identifier the search never returned.

One boundary worth naming: the corpus says what the standard *requires*, not what browsers *do*.

## Layout

```
docfactory/
  engine/       shared: sources schema and whitelist, readers, corpus builder, passport, updater
  server/       shared: MCP server (HTTP and stdio), four protection layers, the project's own agent
  common/       shared: word search (BM25), meaning search (fastembed + Qdrant), instance config and profile
  instances/
    ecmascript/ one instance: sources.json, corpus/, config.json, prompts/, checks.json, .env, .mcp.json — data only
    react/      the same layout; every document carries the React version it describes
  df            launcher: ./df <instance> <step>, always from this directory
```

What makes one domain differ from another — the server name, the tool names and descriptions, the agent prompt,
the checks of the corpus — lives in the instance (`config.json`, `prompts/`, `checks.json`), not in the code.

## Setup

Prerequisites: Python 3.10+ (tested on 3.14) and bash — Linux, macOS or WSL on Windows. Docker is needed only for
meaning search and is optional. An Anthropic API key is needed only for the `ask` step; everything else runs
without it.

A venv is a folder with a Python interpreter and the packages for this project only; `df` calls it itself, so never
activate it. An instance runs on one of two environments, both Linux (`bin/python`):

- **the shared one** — two venvs in the repository root, `.venvs/cpu` (~525 MB) and `.venvs/gpu` (~2.6 GB, ~2.8 GB
  with OCR, with the CUDA libraries for an NVIDIA card), built from `requirements/cpu.txt` and `requirements/gpu.txt`
  (`gpu` plus `requirements/gpu-ocr.txt`, see below), plus a single `.env` in the root (outside git) holding
  `GITHUB_TOKEN` and `DF_VENV=cpu` or `gpu`. This is the default for a new instance;
- **the instance's own `.venv`** — optional, needed only when the domain wants a package outside
  `requirements/*.txt`; the older instances still have one and are moving to the shared environment gradually.

Build a shared venv once, from the repository root (for `gpu`, the same with `gpu`; the GPU itself is not required —
without one `onnxruntime-gpu` computes on the CPU with the same numbers):

```
python3 -m venv .venvs/cpu
.venvs/cpu/bin/python -m pip install -U pip
.venvs/cpu/bin/python -m pip install -r requirements/cpu.txt
```

Page recognition (OCR) for scanned PDFs is needed by one reader only, `cncfcurriculum` of the `kubernetes` instance,
and only for `refresh` and `build`. `cpu.txt` carries `rapidocr-onnxruntime`; `gpu.txt` does not, on purpose: it
declares a dependency on plain `onnxruntime`, which in one venv with `onnxruntime-gpu` overwrites its files. So the
`gpu` venv gets a second build step, and it must use `--no-deps`:

```
.venvs/gpu/bin/python -m pip install --no-deps -r requirements/gpu-ocr.txt
```

That file pins `rapidocr-onnxruntime` and what it lacks on top of `gpu.txt` (`opencv-python`, `shapely`, `pyclipper`,
`six`, ~145 MB). `onnxruntime-gpu` is the same `onnxruntime` module and keeps the CPU provider, which is all the OCR
needs, so it recognises the same text as on `cpu`. The price is one formal line in `pip check` ("rapidocr-onnxruntime
1.2.3 requires onnxruntime, which is not installed"); there should be no other complaints. Without this step
everything except that reader works, and the reader stops with a hint about what is missing.

`df` picks the environment by three rules, in order: `DF_USE_SHARED=1` forces the shared one; otherwise the
instance's own `.venv`, if it has one; otherwise the shared one named by `DF_VENV` (the environment variable, then
the line in the root `.env`, `cpu` when neither is set). The root `.env` is read after the instance's own `.env` and
never overrides it, so private keys such as `ANTHROPIC_API_KEY` stay in the instance's `.env`. `df <instance> serve`
runs on the CPU by default; `DF_SERVE_GPU=1` brings the GPU back. Details are in the section "Спільне середовище"
of [README.md](README.md).

An own venv, when one is needed, is built from the instance folder:

```
cd instances/ecmascript
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cd ../..
```

## Run the server and connect Claude Code

```
./df ecmascript serve                                                  # separate terminal, keep it running
claude mcp add --transport http ecma-spec http://127.0.0.1:8760/mcp    # once; port comes from config.json

./df react serve
claude mcp add --transport http react-docs http://127.0.0.1:8761/mcp
```

In a Claude Code session `/mcp` should list each server with two tools: `search_spec` and `read_section` for
ecmascript, `search_docs` and `read_section` for react (whose search also takes an optional `version`, such as
"18" or "0.14"). The server itself never talks to a model: when the client is Claude Code, Claude Code is the model
and pays with its own tokens.

## Steps and what they cost

| Step | Does | Costs |
|------|------|-------|
| `sources`, `list`, `check`, `refresh`, `manifest` | build and update the corpus; network only to the URLs declared in `sources.json` | $0 |
| `setup`, `vectors`, `status` | optional meaning search: Qdrant in Docker, vectors computed locally | $0, minutes of CPU |
| `serve`, `tools`, `smoke`, `protocol`, `quality`, `raw` | the server and its checks | $0 |
| `ask "question"` | the project's own agent with all four protection layers | **paid** — model tokens, needs the key |

Updating the corpus is five commands — `check`, `refresh`, `manifest`, `vectors`, restart `serve` — described step
by step in [UPDATE.md](UPDATE.md).

## License

MIT — see [LICENSE](LICENSE). The corpus texts keep the licenses of their publishers (Ecma, IETF Trust, Unicode,
Meta Platforms for the React documentation).
