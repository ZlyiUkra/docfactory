# TypeScript README 3.2.0-dev.20181113 … 3.3.0-dev.20190123
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/c2e74ae96eadbe09c997e2ea4c9b1d564162ee00/README.md
# отримано: 2026-09-29
# версія: 3.3.0-dev.20190123, 3.3.0-rc, 3.3.0-dev.20190119, 3.3.0-dev.20190118, 3.2.4, 3.3.0-dev.20190117, 3.3.0-dev.20190116, 3.3.0-dev.20190115, 3.3.0-dev.20190112, 3.3.0-dev.20190111, 3.3.0-dev.20190110, 3.3.0-dev.20190109, 3.3.0-dev.20190108, 3.3.0-dev.20190105, 3.3.0-dev.20190104, 3.3.0-dev.20190103, 3.3.0-dev.20190101, 3.3.0-dev.20181229, 3.3.0-dev.20181228, 3.3.0-dev.20181222, 3.3.0-dev.20181221, 3.3.0-dev.20181220, 3.3.0-dev.20181219, 3.3.0-dev.20181218, 3.3.0-dev.20181214, 3.3.0-dev.20181213, 3.3.0-dev.20181212, 3.3.0-dev.20181211, 3.3.0-dev.20181208, 3.3.0-dev.20181207, 3.2.2, 3.3.0-dev.20181206, 3.3.0-dev.20181205, 3.3.0-dev.20181204, 3.3.0-dev.20181201, 3.3.0-dev.20181130, 3.2.1, 3.3.0-dev.20181129, 3.2.1-insiders.20181128, 3.3.0-dev.20181128, 3.2.1-insiders.20181127, 3.3.0-dev.20181127, 3.3.0-dev.20181122, 3.3.0-dev.20181121, 3.2.0-dev.20181117, 3.2.0-dev.20181116, 3.2.0-rc, 3.2.0-dev.20181115, 3.2.0-dev.20181114, 3.2.0-dev.20181113

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
