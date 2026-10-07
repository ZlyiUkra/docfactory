# TypeScript README 4.2.0-dev.20210130 … 4.3.0-dev.20210427: TypeScript
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/353dc1814fa9b75d341768439b8ba2490a072f50/README.md
# отримано: 2026-09-29
# версія: 4.3.0-dev.20210427, 4.3.0-dev.20210426, 4.3.0-dev.20210425, 4.3.0-dev.20210424, 4.3.0-dev.20210423, 4.3.0-dev.20210422, 4.3.0-dev.20210420, 4.3.0-dev.20210419, 4.3.0-dev.20210418, 4.3.0-dev.20210417, 4.3.0-dev.20210416, 4.3.0-dev.20210415, 4.3.0-dev.20210414, 4.3.0-dev.20210413, 4.3.0-dev.20210412, 4.3.0-dev.20210411, 4.3.0-dev.20210410, 4.3.0-dev.20210409, 4.3.0-dev.20210408, 4.2.4, 4.3.0-dev.20210407, 4.3.0-dev.20210406, 4.3.0-dev.20210405, 4.3.0-dev.20210404, 4.3.0-dev.20210403, 4.3.0-dev.20210402, 4.3.0-dev.20210401, 4.3.0-dev.20210331, 4.3.0-dev.20210330, 4.3.0-dev.20210329, 4.3.0-dev.20210328, 4.3.0-dev.20210327, 4.3.0-dev.20210326, 4.3.0-dev.20210325, 4.3.0-dev.20210324, 4.3.0-dev.20210323, 4.3.0-dev.20210322, 4.3.0-dev.20210319, 4.3.0-dev.20210318, 4.3.0-dev.20210317, 4.3.0-dev.20210316, 4.3.0-dev.20210315, 4.3.0-dev.20210314, 4.3.0-dev.20210313, 4.3.0-dev.20210312, 4.3.0-dev.20210311, 4.3.0-dev.20210310, 4.3.0-dev.20210309, 4.3.0-dev.20210308, 4.3.0-dev.20210307, 4.3.0-dev.20210306, 4.3.0-dev.20210305, 4.2.3, 4.3.0-dev.20210304, 4.3.0-dev.20210303, 4.3.0-dev.20210302, 4.3.0-dev.20210228, 4.3.0-dev.20210227, 4.3.0-dev.20210226, 4.3.0-dev.20210225, 4.3.0-dev.20210224, 4.2.2, 4.3.0-dev.20210223, 4.3.0-dev.20210222, 4.3.0-dev.20210221, 4.3.0-dev.20210220, 4.3.0-dev.20210219, 4.3.0-dev.20210218, 4.3.0-dev.20210217, 4.3.0-dev.20210216, 4.3.0-dev.20210215, 4.3.0-dev.20210214, 4.3.0-dev.20210213, 4.3.0-dev.20210212, 4.3.0-dev.20210211, 4.3.0-dev.20210210, 4.2.0-insiders.20210210, 4.2.0-dev.20210209, 4.2.0-dev.20210208, 4.2.0-dev.20210207, 4.2.0-dev.20210206, 4.2.0-dev.20210205, 4.2.0-dev.20210204, 4.2.0-dev.20210203, 4.2.0-dev.20210202, 4.2.0-dev.20210201, 4.2.0-dev.20210131, 4.2.0-dev.20210130

GitHub Actions CI
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
