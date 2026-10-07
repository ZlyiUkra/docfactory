# TypeScript README 3.1.0-dev.20180804 … 3.1.8
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/v3.1.8/README.md
# отримано: 2026-09-29
# версія: 3.1.8, 3.1.7, 3.1.6, 3.1.5, 3.1.4, 3.1.3-insiders.20181024, 3.1.3, 3.1.2, 3.2.0-dev.20180929, 3.2.0-dev.20180928, 3.1.1, 3.2.0-dev.20180927, 3.1.1-insiders.20180926, 3.2.0-dev.20180926, 3.1.1-insiders.20180925, 3.1.0-dev.20180925, 3.1.0-dev.20180922, 3.1.0-dev.20180921, 3.1.0-insiders.20180920, 3.1.0-dev.20180920, 3.1.0-dev.20180919, 3.1.0-dev.20180918, 3.1.0-dev.20180915, 3.1.0-dev.20180914, 3.1.0-rc.20180911, 3.1.0-dev.20180913, 3.1.0-dev.20180912, 3.1.0-dev.20180907, 3.1.0-dev.20180906, 3.1.0-dev.20180905, 3.1.0-dev.20180904, 3.1.0-dev.20180901, 3.1.0-dev.20180831, 3.1.0-dev.20180830, 3.1.0-dev.20180829, 3.1.0-dev.20180828, 3.1.0-dev.20180825, 3.1.0-dev.20180824, 3.1.0-dev.20180823, 3.1.0-dev.20180822, 3.1.0-dev.20180821, 3.1.0-dev.20180818, 3.1.0-dev.20180817, 3.1.0-dev.20180813, 3.1.0-dev.20180810, 3.1.0-dev.20180809, 3.1.0-dev.20180808, 3.1.0-dev.20180807, 3.1.0-dev.20180804

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
