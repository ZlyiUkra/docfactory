# TypeScript README 2.9.0-dev.20180502 … 2.9.2
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/da1d3cce6fbf109fd322210901d6bf504fdcf42f/README.md
# отримано: 2026-09-29
# версія: 2.9.2, 3.0.0-dev.20180609, 3.0.0-dev.20180608, 3.0.0-dev.20180607, 3.0.0-dev.20180606, 3.0.0-dev.20180605, 3.0.0-dev.20180602, 3.0.0-dev.20180601, 2.9.1, 3.0.0-dev.20180531, 3.0.0-dev.20180530, 3.0.0-dev.20180526, 2.9.1-insiders.20180525, 2.9.1-insiders.20180523, 3.0.0-dev.20180522, 2.9.1-insiders.20180521, 2.9.0-dev.20180519, 2.9.0-dev.20180518, 2.9.1-insiders.20180516, 2.9.0-rc, 2.9.0-dev.20180516, 2.9.0-dev.20180515, 2.9.0-dev.20180512, 2.9.0-dev.20180511, 2.9.0-insiders.20180510, 2.9.0-dev.20180510, 2.9.0-dev.20180509, 2.9.0-dev.20180506, 2.9.0-dev.20180505, 2.9.0-insiders.20180503, 2.9.0-dev.20180503, 2.9.0-dev.20180502

Build Status
VSTS Build Status
npm version
Downloads

## TypeScript

Join the chat at https://gitter.im/Microsoft/TypeScript

TypeScript is a language for application-scale JavaScript. TypeScript adds optional types, classes, and modules to JavaScript. TypeScript supports tools for large-scale JavaScript applications for any browser, for any host, on any OS. TypeScript compiles to readable, standards-based JavaScript. Try it out at the playground, and stay up to date via our blog and Twitter account.

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
                      # Use host=<hostName> or tests=<testPath>.
gulp runtests-browser # Runs the tests using the built run.js file. Syntax is gulp runtests. Optional
                        parameters 'host=', 'tests=[regex], reporter=[list|spec|json|<more>]'.
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
