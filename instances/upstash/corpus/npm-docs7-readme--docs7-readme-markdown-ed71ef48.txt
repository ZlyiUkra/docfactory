# @upstash/docs7 README 0.1.0: @upstash/docs7
# джерело: https://registry.npmjs.org/@upstash/docs7/-/docs7-0.1.0.tgz
# отримано: 2026-10-16
# версія: docs7-0.1.0

The Docs7 command line. Preview a `docs.json` (or legacy `mint.json`) documentation project on your machine.

```bash
npx @upstash/docs7 dev
```

or install it once and use the `docs7` command:

```bash
npm install -g @upstash/docs7
docs7 dev
```

Run it inside a docs project, or pass the project directory. The preview runs at `http://localhost:3333` and reloads pages as you edit them.

```bash
docs7 dev ./docs -p 4000
```

## Commands

| Command | What it does |
| --- | --- |
| `docs7 dev [dir]` | Preview the project with live reload. `-p, --port <port>` (default 3333), `--host <host>` (default 127.0.0.1). |

## How it works

The package is small on purpose. On the first `docs7 dev` it downloads the Docs7 renderer — a prebuilt production build of the same renderer that publishes Docs7 sites — into `~/.docs7/renderer/` (about 30 MB) and reuses it after that. Every run checks for a newer renderer; when you are offline it keeps using the installed one.

Environment variables:

| Variable | Purpose |
| --- | --- |
| `DOCS7_HOME` | Cache directory. Default `~/.docs7`. |
| `DOCS7_RELEASES_URL` | Where renderer releases come from. Default `https://releases.docs7.io`. |
| `DOCS7_RENDERER_VERSION` | Pin one renderer release. |
| `DOCS7_ASSISTANT_PROXY_URL` | Backend for the Ask AI panel while previewing. |

Requires Node.js 20.19 or newer.

## Development (this repository)

The renderer that `dev` runs is built from `renderer/` with `npm run release --prefix renderer` and lands in `renderer/.release/renderer`. Run the CLI against it without downloading anything:

```bash
node cli/bin/docs7.mjs dev renderer/docs/mock --renderer renderer/.release/renderer
```

`npm test --prefix cli` runs the CLI's tests. Publishing is described in `.github/workflows/publish-cli.yml`; renderer releases in `.github/workflows/release-renderer.yml`.
