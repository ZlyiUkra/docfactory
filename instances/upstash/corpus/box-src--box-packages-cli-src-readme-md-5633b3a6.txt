# box: packages/cli/src/README.md
# джерело: https://github.com/upstash/box/blob/python-sdk-v0.3.0/packages/cli/src/README.md
# отримано: 2026-10-16
# версія: upstash-box-0.3.0, upstash-box-0.2.0, upstash-box-0.1.4, upstash-box-0.1.3, upstash-box-0.1.2, upstash-box-0.1.0, dsh-box-0.1.0, box-pi-0.1.7, box-pi-0.1.6, box-pi-0.1.5, box-pi-0.1.4, box-pi-0.1.3, box-pi-0.1.2, box-pi-0.1.1, box-pi-0.1.0, box-cli-0.2.20, box-cli-0.2.19, box-cli-0.2.18, box-cli-0.2.17, box-cli-0.2.16, box-cli-0.2.15, box-cli-0.2.14, box-cli-0.2.13, box-cli-0.2.12, box-cli-0.2.11, box-cli-0.2.10, box-cli-0.2.9, box-cli-0.2.8, box-cli-0.2.7, box-cli-0.2.6, box-cli-0.2.5, box-cli-0.2.4, box-cli-0.2.3, box-cli-0.2.2, box-cli-0.2.1, box-cli-0.2.0, box-cli-0.1.45, box-cli-0.1.44, box-cli-0.1.43, box-cli-0.1.41, box-cli-0.1.40, box-cli-0.1.39, box-cli-0.1.38, box-cli-0.1.37, box-cli-0.1.36, box-cli-0.1.35, box-cli-0.1.34, box-cli-0.1.33, box-cli-0.1.32, box-cli-0.1.31, box-cli-0.1.30, box-cli-0.1.29, box-cli-0.1.28, box-cli-0.1.27, box-cli-0.1.26, box-cli-0.1.25, box-cli-0.1.24, box-cli-0.1.23, box-cli-0.1.22, box-cli-0.1.21, box-cli-0.1.20, box-cli-0.1.19, box-cli-0.1.18, box-cli-0.1.17, box-cli-0.1.16, box-cli-0.1.15, box-cli-0.1.14, box-cli-0.1.13, box-0.7.1, box-0.7.0, box-0.6.3, box-0.6.2, box-0.6.1, box-0.6.0, box-0.5.5, box-0.5.4, box-0.5.3, box-0.5.2, box-0.5.1, box-0.5.0, box-0.4.8, box-0.4.7, box-0.4.6, box-0.4.5, box-0.4.4, box-0.4.3, box-0.4.2, box-0.4.1, box-0.4.0, box-0.3.0, box-0.2.3, box-0.2.2, box-0.2.0, box-0.1.36, box-0.1.35, box-0.1.34, box-0.1.33, box-0.1.32, box-0.1.31, box-0.1.30, box-0.1.29, box-0.1.28, box-0.1.27, box-0.1.26, box-0.1.25, box-0.1.24, box-0.1.23, box-0.1.22, box-0.1.21, box-0.1.20, box-0.1.19, box-0.1.18, box-0.1.17, box-0.1.16, box-0.1.15, box-0.1.14, box-0.1.13, box-0.1.12, box-0.1.11, box-0.1.10

```
# CLI Source Architecture

```
src/
├── index.ts              CLI entry point (Commander.js)
├── auth.ts               Token resolution (flag → env var)
├── agent-key.ts          Agent API key resolution (flag → BoxApiKey enum)
├── output.ts             Format utilities (JSON, raw)
├── repl/
│   ├── client.ts         BoxREPLClient — exported library for programmatic use
│   ├── terminal.ts       Terminal REPL wiring (readline, colors, spinner)
│   ├── spinner.ts        Braille spinner with random messages
│   └── commands/         REPL command handlers
│       ├── run.ts        Agent prompt streaming
│       ├── exec.ts       Shell command execution
│       ├── files.ts      File operations (read, write, list, upload, download)
│       ├── git.ts        Git operations (clone, diff, create-pr)
│       ├── snapshot.ts   Snapshot creation
│       ├── pause.ts      Box pause (exits REPL)
│       └── delete.ts     Box deletion (exits REPL)
├── commands/             CLI commands
│   ├── connect.ts        Connect to existing box (interactive selector if TTY)
│   ├── create.ts         Create new box
│   ├── create-wizard.ts  Interactive setup wizard for box create
│   ├── from-snapshot.ts  Create box from snapshot
│   ├── list.ts           List all boxes
│   ├── get.ts            Get box details
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
- **`repl/terminal.ts`** is CLI-specific — it wires readline, colors, spinner, and tab completion.
- Optional hooks (`onLoadingStart`, `onSuggestion`, `onCommandComplete`, `onCommandNotFound`) enable features by presence. CLI passes all hooks; UI consumers pass only what they need.
```
