# @upstash/cli README 1.0.0 … 1.0.2: Upstash CLI
# джерело: https://registry.npmjs.org/@upstash/cli/-/cli-1.0.2.tgz
# отримано: 2026-10-16
# версія: cli-1.0.2, cli-1.0.1, cli-1.0.0

GitHub release
npm downloads

Agent-friendly CLI for managing & debugging Upstash resources from your terminal. Docs.

## Installation

```bash
npm i -g @upstash/cli
```

For agents, pair the CLI with the Upstash Skill, it bundles Upstash docs alongside docs for the `upstash` CLI.

```bash
npx skills add upstash/skills
```

## Authentication

Grab a Developer API key from the Upstash Console, then save it once per machine:

```bash
upstash login
```

Or set `UPSTASH_EMAIL` and `UPSTASH_API_KEY` in your shell or a `.env` file. See the auth docs for env files, per-command flags, and precedence rules.

## Quick examples

All output is JSON, so you can pipe to `jq`. Use `--dry-run` to preview destructive commands.

```bash
# Redis
upstash redis list
upstash redis create --name my-db --region us-east-1
upstash redis exec --db-url $URL --db-token $TOKEN GET key

# Vector
upstash vector list
upstash vector create --name my-index --region us-east-1 --similarity-function COSINE --dimension-count 1536

# Search
upstash search list
upstash search create --name my-search --region us-central1 --type DENSE

# QStash
upstash qstash list
upstash qstash stats --qstash-id $QSTASH_ID --period 7d

# Team
upstash team list
upstash team add-member --team-id $TEAM_ID --member-email you@example.com --role dev
```

Run `upstash --help` (or `--help` on any subcommand) to discover everything else, and check the full docs for the complete catalog.

## Contributing

```bash
npm install
npm run build
node dist/cli.js --help    # try your build
npm link                   # or expose it as `upstash` globally
```

Open an issue, send a PR, or join us on Discord.
