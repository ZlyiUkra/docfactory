# TypeScript README 1.6.0-dev.20150725 … 1.6.0-dev.20150820
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/069d2dc724798d1249c334aa13b02a3c2f1617ea/README.md
# отримано: 2026-09-29
# версія: 1.6.0-dev.20150820, 1.6.0-dev.20150819, 1.6.0-dev.20150818, 1.6.0-dev.20150817, 1.6.0-dev.20150816, 1.6.0-dev.20150815, 1.6.0-dev.20150814, 1.6.0-dev.20150813, 1.6.0-dev.20150812, 1.6.0-dev.20150811, 1.6.0-dev.20150810, 1.6.0-dev.20150809, 1.6.0-dev.20150808, 1.6.0-dev.20150807, 1.6.0-dev.20150806, 1.6.0-dev.20150805, 1.6.0-dev.20150804, 1.6.0-dev.20150803, 1.6.0-dev.20150802, 1.6.0-dev.20150801, 1.6.0-dev.20150731, 1.6.0-dev.20150730, 1.6.0-dev.20150729, 1.6.0-dev.20150728, 1.6.0-dev.20150727, 1.6.0-dev.20150726, 1.6.0-dev.20150725

Build Status
npm version
Downloads

## TypeScript

Join the chat at https://gitter.im/Microsoft/TypeScript

TypeScript is a language for application-scale JavaScript. TypeScript adds optional types, classes, and modules to JavaScript. TypeScript supports tools for large-scale JavaScript applications for any browser, for any host, on any OS. TypeScript compiles to readable, standards-based JavaScript. Try it out at the playground, and stay up to date via our blog and twitter account.

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
* Read the language specification (docx, pdf).

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

Install Jake tools and dev dependencies:

```
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
jake -T               # List the above commands.
```

## Usage

```shell
node built/local/tsc.js hello.ts
```

## Roadmap

For details on our planned features and future direction please refer to our roadmap.
