# @upstash/bootstrapper README 1.0.1
# джерело: https://registry.npmjs.org/@upstash/bootstrapper/-/bootstrapper-1.0.1.tgz
# отримано: 2026-10-16
# версія: bootstrapper-1.0.1

Certainly! Here's a README file for your Upstash Bootstrapper:

```markdown
# Upstash Bootstrapper

Upstash Bootstrapper is a command-line tool designed to quickly set up new TypeScript projects with a selection of popular development tools and configurations.

## Features

- Interactive CLI for easy project setup
- Support for multiple package managers (Bun and pnpm)
- Configurable tool selection:
  - Prettier
  - ESLint
  - Commitlint
  - Husky
  - tsup

## Prerequisites

- Node.js (version 14 or later)
- Bun or pnpm package manager

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/upstash-bootstrapper.git

# Navigate to the project directory
cd upstash-bootstrapper

# Install dependencies
bun install
```
```

## Usage

Run the bootstrapper with:

```bash
bun start
```

Follow the interactive prompts to:

1. Enter your project name
2. Select the development tools you want to set up
3. Choose your preferred package manager (Bun or pnpm)

The bootstrapper will then:

- Create a new project directory
- Initialize a Git repository
- Set up the selected tools with sensible default configurations
- Update the `package.json` with appropriate scripts

## Configured Tools

### Prettier

- Consistent code formatting
- Configuration file: `prettier.config.mjs`

### ESLint

- Static code analysis
- Configuration file: `.eslintrc.json`

### Commitlint

- Enforces conventional commit messages
- Configuration file: `commitlint.config.js`

### Husky

- Git hooks for running scripts before commits and pushes
- Configured hooks:
  - pre-commit: Runs linting, formatting, and tests
  - pre-push: Runs the build script
  - commit-msg: Checks commit message format

### tsup

- TypeScript build tool
- Configuration file: `tsup.config.ts`

## Scripts

The bootstrapper adds several npm scripts to your `package.json`:

- `prepare`: Installs Husky hooks
- `lint`: Runs ESLint
- `fmt`: Runs Prettier
- `build`: Runs tsup build
- `test`: Runs tests (using the selected package manager)
- `format`: Runs Prettier (write mode)
- `format:check`: Runs Prettier (check mode)
- `lint:fix`: Runs ESLint with auto-fix
- `lint:format`: Runs both linting and formatting fixes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
