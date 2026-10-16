# box: packages/cli/src/README.md
# джерело: https://github.com/upstash/box/blob/python-sdk-v0.4.0/packages/cli/src/README.md
# отримано: 2026-10-16
# версія: upstash-box-0.4.0, dsh-box-0.1.8, dsh-box-0.1.7, dsh-box-0.1.6, dsh-box-0.1.5, dsh-box-0.1.4, dsh-box-0.1.3, dsh-box-0.1.2, dsh-box-0.1.1, box-pi-0.1.15, box-pi-0.1.14, box-pi-0.1.13, box-pi-0.1.12, box-pi-0.1.11, box-pi-0.1.10, box-pi-0.1.9, box-pi-0.1.8, box-cli-0.3.5, box-cli-0.3.4, box-cli-0.3.3, box-cli-0.3.2, box-cli-0.3.1, box-cli-0.3.0, box-cli-0.2.24, box-cli-0.2.23, box-cli-0.2.22, box-cli-0.2.21, box-0.7.9, box-0.7.8, box-0.7.7, box-0.7.6, box-0.7.5, box-0.7.4, box-0.7.3, box-0.7.2

```
# CLI Source Architecture

```
src/
├── cli.ts                CLI entry point (Commander.js)
├── auth.ts               Token resolution (flag → env var)
├── agent-key.ts          Agent API key resolution (flag → BoxApiKey enum)
├── output.ts             Format utilities (JSON, raw)
├── repl/
│   ├── client.ts         BoxREPLClient — exported library for programmatic use
│   ├── terminal.ts       Terminal REPL wiring (readline, colors, spinner)
│   ├── spinner.ts        Braille spinner with random messages
│   └── commands/         REPL command handlers
│       ├── run.ts        Agent prompt streaming
│       ├── agent.ts      Agent mode toggle
│       ├── shell.ts      Shell mode toggle (execution lives in client.ts)
│       ├── cd.ts         Working directory for later commands
│       ├── model.ts      Change the agent model
│       ├── console.ts    Open the box in the Upstash console
│       ├── files.ts      File operations (read, write, list, stat, mkdir,
│       │                 rename, remove, upload, download)
│       ├── git.ts        Git operations (clone, status, diff, commit,
│       │                 checkout, push, create-pr, config, exec)
│       ├── snapshot.ts   Snapshots (create, list, delete)
│       ├── public-url.ts Public URLs for ports in the box
│       ├── status.ts     Box state, runs and logs
│       ├── args.ts       Flag/positional splitting for subcommands
│       ├── pause.ts      Box pause (exits REPL)
│       └── delete.ts     Box deletion (exits REPL)
├── core/                 Shared plumbing for the non-interactive commands
│   ├── errors.ts         CliError and the 125 exit code for a CLI failure
│   ├── box-ref.ts        Box resolution (--box → BOX_ID → .box) and pinning
│   ├── io.ts             emit/note (stdout vs stderr), the error boundary
│   └── exec.ts           Collect and stream a command, working directory
├── commands/             CLI commands
│   ├── status.ts         Selected box, where it came from, its state
│   ├── use.ts            Write or remove this directory's .box
│   ├── exec.ts           Run a shell command (streams; --json collects)
│   ├── files.ts          File operations (read, write, list, stat, mkdir,
│   │                     rename, remove, upload, download)
│   ├── git.ts            Git operations (clone, status, diff, commit,
│   │                     checkout, push, create-pr, config, exec)
│   ├── public-url.ts     Public URLs for ports in the box
│   ├── run.ts            Agent prompt, streamed
│   ├── connect.ts        Connect to existing box (interactive selector if TTY)
│   ├── create.ts         Create new box (REPL, or headless with --no-repl)
│   ├── create-wizard.ts  Interactive setup wizard for box create
│   ├── from-snapshot.ts  Create box from snapshot
│   ├── list.ts           List all boxes
│   ├── get.ts            Get box details
│   ├── env.ts            User-level env vars
│   ├── labels.ts         Labels on a box
│   ├── snapshot.ts       Create a snapshot
│   ├── init-demo.ts      Scaffold demo project
│   └── completion.ts     Shell completion script output
├── utils/
│   ├── ansi.ts           ANSI color/cursor escape helpers
│   ├── fuzzy.ts          Levenshtein distance + fuzzy matching
│   └── interactive-select.ts  Arrow-key selector for TTY
└── __tests__/            Mirrors src/ structure
```

## Key Concepts

- **`repl/client.ts`** is the library export (`@upstash/box-cli`). It exposes `BoxREPLClient` and `REPLHooks` for UI consumers.
- **`repl/terminal.ts`** is CLI-specific: it wires readline, colors, spinner, and tab completion.
- **`commands/` + `core/`** is the non-interactive half. Every command there is driven by arguments alone, writes data to stdout and diagnostics to stderr, and reports failure as exit code 125 so a remote command's own exit code stays unambiguous.
- Optional hooks (`onLoadingStart`, `onSuggestion`, `onCommandComplete`, `onCommandNotFound`) enable features by presence. CLI passes all hooks; UI consumers pass only what they need.
```
