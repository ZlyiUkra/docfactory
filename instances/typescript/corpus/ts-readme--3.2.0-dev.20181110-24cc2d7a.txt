# TypeScript README 3.2.0-dev.20181002 … 3.2.0-dev.20181110
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/02ca5bebbf4ba40938d22d68cbbe548332d67e15/README.md
# отримано: 2026-09-29
# версія: 3.2.0-dev.20181110, 3.2.0-dev.20181107, 3.2.0-dev.20181106, 3.2.0-dev.20181103, 3.2.0-dev.20181102, 3.2.0-dev.20181101, 3.2.0-dev.20181031, 3.2.0-dev.20181030, 3.2.0-dev.20181027, 3.2.0-dev.20181026, 3.2.0-dev.20181025, 3.2.0-dev.20181024, 3.2.0-dev.20181023, 3.2.0-dev.20181020, 3.2.0-dev.20181019, 3.2.0-dev.20181018, 3.2.0-dev.20181017, 3.2.0-dev.20181011, 3.2.0-dev.20181010, 3.2.0-dev.20181009, 3.2.0-dev.20181006, 3.2.0-dev.20181004, 3.2.0-dev.20181003, 3.2.0-dev.20181002

Build Status
VSTS Build Status
npm version
Downloads

## TypeScript

Join the chat at https://gitter.im/Microsoft/TypeScript

TypeScript is a language for application-scale JavaScript. TypeScript adds optional types to JavaScript that support tools for large-scale JavaScript applications for any browser, for any host, on any OS. TypeScript compiles to readable, standards-based JavaScript. Try it out at the playground, and stay up to date via our blog and Twitter account.

## Installing

For the latest stable version:

```bash
npm install -g typescript
```

For our nightly builds:

```bash
npm install -g typescript@next
```

## Contribute

There are many ways to contribute to TypeScript.
* Submit bugs and help us verify fixes as they are checked in.
* Review the source code changes.
* Engage with other TypeScript users and developers on StackOverflow.
* Join the #typescript discussion on Twitter.
* Contribute bug fixes.
* Read the language specification (docx,
 pdf, md).

This project has adopted the Microsoft Open Source Code of Conduct. For more information see
the Code of Conduct FAQ or contact opencode@microsoft.com
with any additional questions or comments.

## Documentation

*  Quick tutorial
*  Programming handbook
*  Language specification
*  Homepage

## Building

In order to build the TypeScript compiler, ensure that you have Git and Node.js installed.

Clone a copy of the repo:

```bash
git clone https://github.com/Microsoft/TypeScript.git
```

Change to the TypeScript directory:

```bash
cd TypeScript
```

Install Jake tools and dev dependencies:

```bash
npm install -g jake
npm install
```

Use one of the following to build and test:

```
jake local            # Build the compiler into built/local
jake clean            # Delete the built compiler
jake LKG              # Replace the last known good with the built one.
                      # Bootstrapping step to be executed when the built compiler reaches a stable state.
jake tests            # Build the test infrastructure using the built compiler.
jake runtests         # Run tests using the built compiler and test infrastructure.
                      # You can override the host or specify a test for this command.
                      # Use host=<hostName> or tests=<testPath>.
jake runtests-browser # Runs the tests using the built run.js file. Syntax is jake runtests. Optional
                        parameters 'host=', 'tests=[regex], reporter=[list|spec|json|<more>]'.
jake baseline-accept  # This replaces the baseline test results with the results obtained from jake runtests.
jake lint             # Runs tslint on the TypeScript source.
jake help             # List the above commands.
```

## Usage

```bash
node built/local/tsc.js hello.ts
```

## Roadmap

For details on our planned features and future direction please refer to our roadmap.
