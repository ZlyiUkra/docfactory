# TypeScript README 2.3.0-dev.20170419 … 2.4.2
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/6105867bb05abc365d8d7f4fbd03e14a8d50117e/README.md
# отримано: 2026-09-29
# версія: 2.4.2, 2.4.2-insiders.20170719, 2.4.2-insiders.20170630, 2.4.1-insiders.20170630, 2.5.0-dev.20170628, 2.4.1, 2.5.0-dev.20170627, 2.5.0-dev.20170626, 2.5.0-dev.20170625, 2.5.0-dev.20170624, 2.5.0-dev.20170623, 2.5.0-dev.20170622, 2.5.0-dev.20170621, 2.5.0-dev.20170619, 2.5.0-dev.20170618, 2.5.0-dev.20170617, 2.5.0-dev.20170616, 2.4.1-insiders.20170615, 2.5.0-dev.20170615, 2.4.1-insiders.20170614, 2.5.0-dev.20170614, 2.5.0-dev.20170613, 2.4.0, 2.4.0-dev.20170612, 2.4.0-dev.20170611, 2.4.0-dev.20170610, 2.4.0-dev.20170609, 2.4.0-dev.20170608, 2.4.0-dev.20170607, 2.4.0-dev.20170606, 2.4.0-dev.20170605, 2.4.0-dev.20170604, 2.4.0-dev.20170603, 2.4.0-dev.20170602, 2.4.0-dev.20170601, 2.4.0-dev.20170531, 2.3.4, 2.4.0-dev.20170530, 2.4.0-dev.20170529, 2.4.0-dev.20170528, 2.4.0-dev.20170527, 2.4.0-dev.20170526, 2.4.0-dev.20170525, 2.4.0-dev.20170524, 2.4.0-dev.20170523, 2.3.3, 2.4.0-dev.20170519, 2.4.0-dev.20170518, 2.4.0-dev.20170517, 2.4.0-dev.20170516, 2.4.0-dev.20170515, 2.4.0-dev.20170514, 2.4.0-dev.20170513, 2.3.3-insiders.20170512, 2.4.0-dev.20170512, 2.4.0-dev.20170511, 2.4.0-dev.20170510, 2.4.0-dev.20170509, 2.4.0-dev.20170508, 2.4.0-dev.20170507, 2.4.0-dev.20170506, 2.4.0-dev.20170505, 2.4.0-dev.20170504, 2.4.0-dev.20170503, 2.4.0-dev.20170502, 2.4.0-dev.20170501, 2.4.0-dev.20170430, 2.4.0-dev.20170429, 2.3.2, 2.4.0-dev.20170428, 2.3.1, 2.4.0-dev.20170427, 2.3.0-dev.20170426, 2.3.1-insiders.20170425.1, 2.3.1-insiders.20170425, 2.3.0-dev.20170425, 2.3.0-dev.20170424, 2.3.0-dev.20170423, 2.3.0-dev.20170422, 2.3.0-dev.20170421, 2.3.1-insiders.20170420, 2.3.0-dev.20170420, 2.3.0-dev.20170419

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
