# TypeScript README 1.7.0-dev.20150920 … 1.7.5
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/1a8406d8b05e8efea768a1788cc9024f9425a1e5/README.md
# отримано: 2026-09-29
# версія: 1.7.5, 1.7.3, 1.8.0-dev.20151112, 1.8.0-dev.20151111, 1.8.0-dev.20151110, 1.8.0-dev.20151109, 1.8.0-dev.20151108, 1.8.0-dev.20151107, 1.8.0-dev.20151106, 1.8.0-dev.20151105, 1.8.0-dev.20151104, 1.8.0-dev.20151103, 1.8.0-dev.20151102, 1.8.0-dev.20151101, 1.8.0-dev.20151031, 1.8.0-dev.20151030, 1.8.0-dev.20151029, 1.8.0-dev.20151028, 1.8.0-dev.20151027, 1.8.0-dev.20151026, 1.8.0-dev.20151025, 1.8.0-dev.20151024, 1.8.0-dev.20151023, 1.8.0-dev.20151022, 1.8.0-dev.20151021, 1.8.0-dev.20151020, 1.8.0-dev.20151019, 1.8.0-dev.20151018, 1.8.0-dev.20151017, 1.7.0-dev.20151016, 1.7.0-dev.20151015, 1.7.0-dev.20151014, 1.7.0-dev.20151006, 1.7.0-dev.20151005, 1.7.0-dev.20151004, 1.7.0-dev.20151003, 1.7.0-dev.20151002, 1.7.0-dev.20151001, 1.7.0-dev.20150930, 1.7.0-dev.20150929, 1.7.0-dev.20150928, 1.7.0-dev.20150927, 1.7.0-dev.20150926, 1.7.0-dev.20150925, 1.7.0-dev.20150924, 1.7.0-dev.20150923, 1.7.0-dev.20150922, 1.7.0-dev.20150921, 1.7.0-dev.20150920

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
