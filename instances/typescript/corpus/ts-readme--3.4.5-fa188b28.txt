# TypeScript README 3.4.0-dev.20190221 … 3.4.5
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/v3.4.5/README.md
# отримано: 2026-09-29
# версія: 3.4.5, 3.4.4, 3.5.0-dev.20190418, 3.5.0-dev.20190417, 3.5.0-dev.20190416, 3.5.0-dev.20190413, 3.5.0-dev.20190412, 3.5.0-dev.20190411, 3.5.0-dev.20190410, 3.4.3, 3.5.0-dev.20190409, 3.4.3-insiders.20190408, 3.5.0-dev.20190407, 3.5.0-dev.20190406, 3.4.2, 3.5.0-dev.20190405, 3.5.0-dev.20190404, 3.4.0-dev.20190403, 3.4.0-dev.20190330, 3.4.1, 3.4.0-dev.20190329, 3.4.0-dev.20190328, 3.4.0-dev.20190327, 3.4.0-dev.20190326, 3.4.0-dev.20190323, 3.4.0-dev.20190322, 3.4.0-dev.20190321, 3.4.0-dev.20190320, 3.4.0-dev.20190319, 3.4.0-dev.20190316, 3.4.0-dev.20190315, 3.4.0-dev.20190314, 3.4.0-dev.20190313, 3.4.0-dev.20190312, 3.4.0-dev.20190311, 3.4.0-dev.20190310, 3.4.0-dev.20190309, 3.4.0-dev.20190308, 3.4.0-dev.20190307, 3.4.0-dev.20190306, 3.4.0-dev.20190305, 3.4.0-dev.20190302, 3.4.0-dev.20190301, 3.4.0-dev.20190228, 3.4.0-dev.20190227, 3.4.0-dev.20190226, 3.4.0-dev.20190223, 3.4.0-dev.20190222, 3.4.0-dev.20190221

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

Install Gulp tools and dev dependencies:

```bash
npm install -g gulp
npm install
```

Use one of the following to build and test:

```
gulp local            # Build the compiler into built/local
gulp clean            # Delete the built compiler
gulp LKG              # Replace the last known good with the built one.
                      # Bootstrapping step to be executed when the built compiler reaches a stable state.
gulp tests            # Build the test infrastructure using the built compiler.
gulp runtests         # Run tests using the built compiler and test infrastructure.
                      # You can override the host or specify a test for this command.
                      # Use --host=<hostName> or --tests=<testPath>.
gulp runtests-browser # Runs the tests using the built run.js file. Syntax is gulp runtests. Optional
                        parameters '--host=', '--tests=[regex], --reporter=[list|spec|json|<more>]'.
gulp baseline-accept  # This replaces the baseline test results with the results obtained from gulp runtests.
gulp lint             # Runs tslint on the TypeScript source.
gulp help             # List the above commands.
```

## Usage

```bash
node built/local/tsc.js hello.ts
```

## Roadmap

For details on our planned features and future direction please refer to our roadmap.
