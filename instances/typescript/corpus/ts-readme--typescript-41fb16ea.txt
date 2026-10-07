# TypeScript README 1.9.0-dev.20160624-1.0 … 2.1.0-dev.20160816
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/80c04f8e97aa7ab6c0e1fb604bf1551e7057183c/README.md
# отримано: 2026-09-29
# версія: 2.1.0-dev.20160816, 2.1.0-dev.20160815, 2.1.0-dev.20160814, 2.1.0-dev.20160813, 2.1.0-dev.20160812, 2.1.0-dev.20160811, 2.1.0-dev.20160810, 2.1.0-dev.20160809, 2.1.0-dev.20160808, 2.1.0-dev.20160807, 2.1.0-dev.20160806, 2.1.0-dev.20160805, 2.1.0-dev.20160804, 2.1.0-dev.20160803, 2.1.0-dev.20160802, 2.1.0-dev.20160801, 2.1.0-dev.20160731, 2.1.0-dev.20160730, 2.1.0-dev.20160729, 2.1.0-dev.20160728, 2.1.0-dev.20160727, 2.1.0-dev.20160726, 2.1.0-dev.20160725, 2.1.0-dev.20160724, 2.1.0-dev.20160723, 2.1.0-dev.20160722, 2.1.0-dev.20160721, 2.1.0-dev.20160720, 2.1.0-dev.20160719, 2.1.0-dev.20160718, 2.1.0-dev.20160717, 2.1.0-dev.20160716, 2.1.0-dev.20160715, 2.1.0-dev.20160714, 2.1.0-dev.20160713, 2.1.0-dev.20160712, 2.0.0, 2.0.0-dev.20160711, 2.0.0-dev.20160707, 2.0.0-dev.20160706, 2.0.0-dev.20160705, 2.0.0-dev.20160704, 2.0.0-dev.20160703, 2.0.0-dev.20160702, 2.0.0-dev.20160701, 2.0.0-dev.20160630, 2.0.0-dev.20160629, 2.0.0-dev.20160628, 1.9.0-dev.20160627-1.0, 1.9.0-dev.20160626-1.0, 1.9.0-dev.20160625-1.0, 1.9.0-dev.20160624-1.0

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
* Read the language specification (docx, pdf, md).

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
