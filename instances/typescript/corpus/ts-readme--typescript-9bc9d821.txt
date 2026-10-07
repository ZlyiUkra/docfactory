# TypeScript README 4.2.0-dev.20201104 … 4.2.0-dev.20210129: TypeScript
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/9dbfaeef2d83463c1051561f21b3cd8033b9f481/README.md
# отримано: 2026-09-29
# версія: 4.2.0-dev.20210129, 4.2.0-dev.20210128, 4.2.0-dev.20210127, 4.2.0-dev.20210126, 4.2.0-dev.20210125, 4.2.0-dev.20210124, 4.2.0-dev.20210123, 4.2.0-dev.20210122, 4.2.0-dev.20210121, 4.2.0-dev.20210120, 4.2.0-dev.20210119, 4.2.0-dev.20210115, 4.2.0-dev.20210114, 4.2.0-dev.20210113, 4.2.0-dev.20210112, 4.2.0-dev.20210111, 4.2.0-dev.20210108, 4.2.0-dev.20210107, 4.2.0-dev.20210106, 4.2.0-dev.20210105, 4.2.0-dev.20210104, 4.2.0-dev.20210103, 4.2.0-dev.20210102, 4.2.0-dev.20210101, 4.2.0-dev.20201231, 4.2.0-dev.20201230, 4.2.0-dev.20201229, 4.2.0-dev.20201228, 4.2.0-dev.20201227, 4.2.0-dev.20201226, 4.2.0-dev.20201225, 4.2.0-dev.20201224, 4.2.0-dev.20201223, 4.2.0-dev.20201222, 4.2.0-dev.20201221, 4.2.0-dev.20201220, 4.2.0-dev.20201219, 4.2.0-dev.20201211, 4.2.0-dev.20201210, 4.2.0-dev.20201209, 4.2.0-dev.20201208, 4.2.0-dev.20201207, 4.2.0-dev.20201206, 4.2.0-dev.20201205, 4.2.0-dev.20201204, 4.2.0-dev.20201202, 4.2.0-dev.20201201, 4.2.0-dev.20201130, 4.2.0-dev.20201129, 4.2.0-dev.20201128, 4.2.0-dev.20201127, 4.2.0-dev.20201126, 4.2.0-dev.20201124, 4.2.0-dev.20201123, 4.2.0-dev.20201122, 4.2.0-dev.20201121, 4.2.0-dev.20201120, 4.2.0-dev.20201119, 4.2.0-dev.20201118, 4.2.0-dev.20201117, 4.2.0-dev.20201116, 4.2.0-dev.20201115, 4.2.0-dev.20201114, 4.2.0-dev.20201113, 4.2.0-dev.20201112, 4.2.0-dev.20201109, 4.2.0-dev.20201108, 4.2.0-dev.20201107, 4.2.0-dev.20201106, 4.2.0-dev.20201105, 4.2.0-dev.20201104

Build Status
Devops Build Status
npm version
Downloads

TypeScript is a language for application-scale JavaScript. TypeScript adds optional types to JavaScript that support tools for large-scale JavaScript applications for any browser, for any host, on any OS. TypeScript compiles to readable, standards-based JavaScript. Try it out at the playground, and stay up to date via our blog and Twitter account.

Find others who are using TypeScript at our community page.

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
* Help each other in the TypeScript Community Discord.
* Join the #typescript discussion on Twitter.
* Contribute bug fixes.
* Read the archived language specification (docx,
 pdf, md).

This project has adopted the Microsoft Open Source Code of Conduct. For more information see
the Code of Conduct FAQ or contact opencode@microsoft.com
with any additional questions or comments.

## Documentation

*  TypeScript in 5 minutes
*  Programming handbook
*  Homepage

## Building

In order to build the TypeScript compiler, ensure that you have Git and Node.js installed.

Clone a copy of the repo:

```bash
git clone https://github.com/microsoft/TypeScript.git
```

Change to the TypeScript directory:

```bash
cd TypeScript
```

Install Gulp tools and dev dependencies:

```bash
npm install -g gulp
npm ci
```

Use one of the following to build and test:

```
gulp local             # Build the compiler into built/local.
gulp clean             # Delete the built compiler.
gulp LKG               # Replace the last known good with the built one.
                       # Bootstrapping step to be executed when the built compiler reaches a stable state.
gulp tests             # Build the test infrastructure using the built compiler.
gulp runtests          # Run tests using the built compiler and test infrastructure.
                       # You can override the specific suite runner used or specify a test for this command.
                       # Use --tests=<testPath> for a specific test and/or --runner=<runnerName> for a specific suite.
                       # Valid runners include conformance, compiler, fourslash, project, user, and docker
                       # The user and docker runners are extended test suite runners - the user runner
                       # works on disk in the tests/cases/user directory, while the docker runner works in containers.
                       # You'll need to have the docker executable in your system path for the docker runner to work.
gulp runtests-parallel # Like runtests, but split across multiple threads. Uses a number of threads equal to the system
                       # core count by default. Use --workers=<number> to adjust this.
gulp baseline-accept   # This replaces the baseline test results with the results obtained from gulp runtests.
gulp lint              # Runs eslint on the TypeScript source.
gulp help              # List the above commands.
```

## Usage

```bash
node built/local/tsc.js hello.ts
```

## Roadmap

For details on our planned features and future direction please refer to our roadmap.
