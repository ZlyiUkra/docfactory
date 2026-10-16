# Upstash Box
# джерело: https://github.com/upstash/box/blob/python-sdk-v0.1.0/README.md
# отримано: 2026-10-16
# версія: upstash-box-0.1.0, box-cli-0.2.10, box-cli-0.2.9, box-cli-0.2.8, box-cli-0.2.7, box-cli-0.2.6, box-cli-0.2.5, box-cli-0.2.4, box-cli-0.2.3, box-cli-0.2.2, box-cli-0.2.1, box-cli-0.2.0, box-cli-0.1.45, box-cli-0.1.44, box-cli-0.1.43, box-cli-0.1.41, box-cli-0.1.40, box-cli-0.1.39, box-cli-0.1.38, box-cli-0.1.37, box-cli-0.1.36, box-cli-0.1.35, box-cli-0.1.34, box-cli-0.1.33, box-cli-0.1.32, box-cli-0.1.31, box-cli-0.1.30, box-cli-0.1.29, box-cli-0.1.28, box-cli-0.1.27, box-cli-0.1.26, box-cli-0.1.25, box-cli-0.1.24, box-cli-0.1.23, box-cli-0.1.22, box-cli-0.1.21, box-cli-0.1.20, box-cli-0.1.19, box-cli-0.1.18, box-cli-0.1.17, box-cli-0.1.16, box-cli-0.1.15, box-cli-0.1.14, box-cli-0.1.13, box-cli-0.1.12, box-cli-0.1.11, box-cli-0.1.10, box-cli-0.1.9, box-cli-0.1.8, box-cli-0.1.7, box-cli-0.1.6, box-cli-0.1.5, box-cli-0.1.4, box-cli-0.1.3, box-cli-0.1.2, box-cli-0.1.1, box-0.5.1, box-0.5.0, box-0.4.8, box-0.4.7, box-0.4.6, box-0.4.5, box-0.4.4, box-0.4.3, box-0.4.2, box-0.4.1, box-0.4.0, box-0.3.0, box-0.2.3, box-0.2.2, box-0.2.0, box-0.1.36, box-0.1.35, box-0.1.34, box-0.1.33, box-0.1.32, box-0.1.31, box-0.1.30, box-0.1.29, box-0.1.28, box-0.1.27, box-0.1.26, box-0.1.25, box-0.1.24, box-0.1.23, box-0.1.22, box-0.1.21, box-0.1.20, box-0.1.19, box-0.1.18, box-0.1.17, box-0.1.16, box-0.1.15, box-0.1.14, box-0.1.13, box-0.1.12, box-0.1.11, box-0.1.10, box-0.1.9, box-0.1.8, box-0.1.7, box-0.1.6, box-0.1.5, box-0.1.4, box-0.1.3, box-0.1.2, box-0.1.1

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

1. Create a branch, make your changes, run `pnpm changeset` to create a changeset, and push the branch to GitHub.
2. Go to **Actions → Canary Release → Run workflow**, pick a package and the branch.
3. The workflow creates a snapshot version (e.g. `0.2.0-canary-20260219131415-abc1234`), publishes to npm under the `canary` tag, and creates a GitHub prerelease.

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
