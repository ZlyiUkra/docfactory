# Upstash Box
# джерело: https://github.com/upstash/box/blob/@upstash%2Fbox-cli@0.1.0/README.md
# отримано: 2026-10-16
# версія: box-cli-0.1.0, box-0.1.0

TypeScript SDK and CLI for Upstash Box — sandboxed AI coding agents with streaming, structured output, file I/O, git, and snapshots.

## Packages

| Package | Description |
|---------|-------------|
| `@upstash/box` | TypeScript SDK — programmatic access to the Box API |
| `@upstash/box-cli` | CLI — REPL-first terminal interface wrapping the SDK |

## Quick start

```bash
# Install dependencies
pnpm install

# Build all packages
pnpm build

# Watch mode (both packages)
pnpm dev
```

## Repository structure

```
.
├── packages/
│   ├── sdk/          # @upstash/box — TypeScript SDK
│   │   ├── src/
│   │   └── examples/
│   └── cli/          # @upstash/box-cli — CLI + interactive REPL
│       └── src/
├── pnpm-workspace.yaml
├── tsconfig.base.json
└── package.json
```

## Testing

Tests use Vitest. There are two test suites:

- **Unit tests** — mock all API calls, fast, no credentials needed
- **Integration tests** — hit the real Box API, require env vars

### Environment variables

Create a `.env` file at the repository root:

```
UPSTASH_BOX_API_KEY=abx_...
AGENT_API_KEY=sk-ant-...
```

Integration tests are automatically skipped when these variables are not set.

### Commands

```bash
# Run all tests (unit + integration if .env is present)
pnpm test

# Run only integration tests
pnpm test:integration

# Run tests for a single package
cd packages/sdk && pnpm test
cd packages/cli && pnpm test
```

## Releasing

This repo uses Changesets for versioning and automated npm publishing via OIDC.

### Stable release

1. Create a changeset while working on your feature:
```bash
   pnpm changeset
```
2. Merge your PR to `main`. The **Changeset** workflow creates a "Version Packages" PR that bumps versions and updates changelogs.
3. Merge the version PR. The workflow tags the release, creates a GitHub Release, and triggers **npm Publish** which publishes to npm.

### Canary release

1. Go to **Actions → Canary Release → Run workflow**, pick a package and branch.
2. The workflow creates a snapshot version (e.g. `0.2.0-canary-20260219131415-abc1234`), publishes to npm under the `canary` tag, and creates a GitHub prerelease.

### Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| `ci.yml` | PR + push to main | Build and test (Node 18/20/22) |
| `changeset.yml` | Push to main | Version PR or tag + GitHub Release |
| `canary.yml` | Manual dispatch | Snapshot version + GitHub prerelease |
| `npm-publish.yml` | `workflow_run` (after changeset/canary) | Publish to npm with OIDC provenance |

`npm-publish.yml` is the sole npm trusted publisher — configure it on npmjs.com for both packages. No npm tokens or PATs required.

## Requirements

- Node.js >= 18
- pnpm

## License

MIT
