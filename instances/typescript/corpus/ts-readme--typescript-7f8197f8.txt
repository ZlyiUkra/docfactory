# TypeScript README 3.0.0-dev.20180628 … 3.0.3-insiders.20180829
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/9faffc92d21c57835c8a270044c7e7d8f8282bb4/README.md
# отримано: 2026-09-29
# версія: 3.0.3-insiders.20180829, 3.0.3, 3.1.0-dev.20180803, 3.1.0-dev.20180802, 3.1.0-dev.20180801, 3.1.0-dev.20180731, 3.0.1, 3.1.0-dev.20180728, 3.1.0-dev.20180727, 3.0.1-insiders.20180726, 3.1.0-dev.20180726, 3.1.0-dev.20180725, 3.1.0-dev.20180724, 3.0.1-insiders.20180723, 3.1.0-dev.20180721, 3.1.0-dev.20180717, 3.0.1-insiders.20180713, 3.0.0-rc, 3.0.0-dev.20180712, 3.0.0-dev.20180711, 3.0.0-dev.20180710, 3.0.0-dev.20180707, 3.0.0-insiders.20180706, 3.0.0-dev.20180706, 3.0.0-dev.20180705, 3.0.0-dev.20180704, 3.0.0-dev.20180703, 3.0.0-dev.20180630, 3.0.0-dev.20180629, 3.0.0-dev.20180628

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
