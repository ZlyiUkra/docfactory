# TypeScript README 2.1.0-dev.20160817 … 2.0.10
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/790a5c7735373475505dfc98af6d87241b165ed3/README.md
# отримано: 2026-09-29
# версія: 2.0.10, 2.0.9, 2.0.8, 2.0.7, 2.0.6, 2.0.6-insiders.20161017, 2.0.6-insiders.20161014, 2.0.6-insiders.20161012, 2.0.6-insiders.20161007, 2.0.3, 2.1.0-dev.20160913, 2.1.0-dev.20160912, 2.1.0-dev.20160911, 2.1.0-dev.20160910, 2.1.0-dev.20160909, 2.1.0-dev.20160908, 2.1.0-dev.20160907, 2.1.0-dev.20160906, 2.1.0-dev.20160905, 2.1.0-dev.20160904, 2.1.0-dev.20160903, 2.1.0-dev.20160902, 2.1.0-dev.20160901, 2.1.0-dev.20160831, 2.0.2, 2.1.0-dev.20160830, 2.1.0-dev.20160829, 2.1.0-dev.20160828, 2.1.0-dev.20160827, 2.1.0-dev.20160826, 2.1.0-dev.20160825, 2.1.0-dev.20160824, 2.1.0-dev.20160823, 2.1.0-dev.20160822, 2.1.0-dev.20160821, 2.1.0-dev.20160820, 2.1.0-dev.20160819, 2.1.0-dev.20160818, 2.1.0-dev.20160817

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
