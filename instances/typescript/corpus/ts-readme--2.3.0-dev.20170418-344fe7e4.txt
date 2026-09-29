# TypeScript README 2.3.0-dev.20170311 … 2.3.0-dev.20170418
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/b038d28ed4490924f115b2268086313f67f9d5a5/README.md
# отримано: 2026-09-29
# версія: 2.3.0-dev.20170418, 2.3.0-dev.20170417, 2.3.1-insiders.20170416, 2.3.0-dev.20170416, 2.3.0-dev.20170415, 2.3.0-dev.20170414, 2.3.1-insiders.20170413, 2.3.0-dev.20170413, 2.3.0-dev.20170412, 2.3.0-dev.20170411, 2.3.0, 2.3.0-dev.20170407, 2.3.0-dev.20170406, 2.3.0-dev.20170405, 2.3.0-dev.20170404, 2.3.0-dev.20170403, 2.3.0-dev.20170402, 2.3.0-dev.20170401, 2.3.0-dev.20170331, 2.3.0-dev.20170330, 2.3.0-dev.20170329, 2.3.0-dev.20170328, 2.3.0-dev.20170327, 2.3.0-dev.20170326, 2.3.0-dev.20170325, 2.3.0-dev.20170324, 2.3.0-dev.20170323, 2.3.0-dev.20170322, 2.3.0-dev.20170321, 2.3.0-dev.20170320, 2.3.0-dev.20170319, 2.3.0-dev.20170318, 2.3.0-dev.20170317, 2.3.0-dev.20170316, 2.3.0-dev.20170315, 2.3.0-dev.20170314, 2.3.0-dev.20170313, 2.3.0-dev.20170312, 2.3.0-dev.20170311

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
