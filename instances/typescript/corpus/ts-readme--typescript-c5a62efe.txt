# TypeScript README 2.5.0-dev.20170629 … 2.5.3
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/94b4f8b79e370020cb31995e8fb0b78f9ba94349/README.md
# отримано: 2026-09-29
# версія: 2.5.3, 2.5.3-insiders.20170922, 2.5.3-insiders.20170919, 2.5.3-insiders.20170909, 2.5.3-insiders.20170908, 2.6.0-dev.20170907, 2.6.0-dev.20170906, 2.6.0-dev.20170904, 2.6.0-dev.20170902, 2.6.0-dev.20170901, 2.5.2, 2.6.0-dev.20170831, 2.6.0-dev.20170830, 2.6.0-dev.20170829, 2.6.0-dev.20170826, 2.5.1-insiders.20170825, 2.6.0-dev.20170825, 2.6.0-dev.20170824, 2.6.0-dev.20170823, 2.6.0-dev.20170822, 2.5.1-insiders.20170822, 2.6.0-dev.20170819, 2.5.1-insiders.20170818, 2.5.1, 2.6.0-dev.20170818, 2.5.0, 2.6.0-dev.20170817, 2.5.0-dev.20170816, 2.5.0-dev.20170815, 2.5.0-dev.20170808, 2.5.0-dev.20170807, 2.5.0-dev.20170803, 2.5.0-dev.20170801, 2.5.0-dev.20170731, 2.5.0-dev.20170727, 2.5.0-dev.20170725, 2.5.0-dev.20170719, 2.5.0-dev.20170712, 2.5.0-dev.20170707, 2.5.0-dev.20170629

Build Status
npm version
Downloads

## TypeScript

Join the chat at https://gitter.im/Microsoft/TypeScript

TypeScript is a language for application-scale JavaScript. TypeScript adds optional types, classes, and modules to JavaScript. TypeScript supports tools for large-scale JavaScript applications for any browser, for any host, on any OS. TypeScript compiles to readable, standards-based JavaScript. Try it out at the playground, and stay up to date via our blog and Twitter account.

## Installing

For the latest stable version:

```
npm install -g typescript
```

For our nightly builds:

```
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

```
git clone https://github.com/Microsoft/TypeScript.git
```

Change to the TypeScript directory:

```
cd TypeScript
```

Install Gulp tools and dev dependencies:

```
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

```shell
node built/local/tsc.js hello.ts
```

## Roadmap

For details on our planned features and future direction please refer to our roadmap.
