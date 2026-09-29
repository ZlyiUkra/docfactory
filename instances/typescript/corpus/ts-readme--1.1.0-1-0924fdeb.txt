# TypeScript README 1.1.0-1: TypeScript
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/4d63fde84a48561f3d886a1e46b7eadb92fbfbbc/README.md
# отримано: 2026-09-29
# версія: 1.1.0-1

TypeScript is a language for application-scale JavaScript. TypeScript adds optional types, classes, and modules to JavaScript. TypeScript supports tools for large-scale JavaScript applications for any browser, for any host, on any OS. TypeScript compiles to readable, standards-based JavaScript. Try it out at the playground, and stay up to date via our blog and twitter account.

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
jake local           # Build the compiler into built/local
jake clean           # Delete the built compiler
jake LKG             # Replace the last known good with the built one.
                     # Bootstrapping step to be executed when the built compiler reaches a stable state.
jake tests           # Build the test infrastructure using the built compiler.
jake runtests        # Run tests using the built compiler and test infrastructure.
                     # You can override the host or specify a test for this command.
                     # Use host=<hostName> or tests=<testPath>.
jake baseline-accept # This replaces the baseline test results with the results obtained from jake runtests.
jake -T              # List the above commands.
```

## Usage

```shell
node built/local/tsc.js hello.ts
```

## Roadmap

For details on our planned features and future direction please refer to our roadmap.
