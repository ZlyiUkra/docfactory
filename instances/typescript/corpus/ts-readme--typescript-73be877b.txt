# TypeScript README 4.3.0-dev.20210428 … 4.3.5: TypeScript
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/v4.3.5/README.md
# отримано: 2026-09-29
# версія: 4.3.5, 4.3.4, 4.3.3, 4.4.0-dev.20210601, 4.4.0-dev.20210531, 4.4.0-dev.20210530, 4.4.0-dev.20210529, 4.4.0-dev.20210528, 4.4.0-dev.20210527, 4.3.2, 4.4.0-dev.20210526, 4.4.0-dev.20210525, 4.4.0-dev.20210524, 4.4.0-dev.20210523, 4.4.0-dev.20210522, 4.4.0-dev.20210521, 4.4.0-dev.20210520, 4.4.0-dev.20210519, 4.4.0-dev.20210518, 4.4.0-dev.20210517, 4.4.0-dev.20210516, 4.4.0-dev.20210515, 4.4.0-dev.20210514, 4.4.0-dev.20210513, 4.4.0-dev.20210512, 4.4.0-dev.20210511, 4.3.0-dev.20210510, 4.3.0-dev.20210509, 4.3.0-dev.20210508, 4.3.0-dev.20210507, 4.3.0-dev.20210506, 4.3.0-dev.20210505, 4.3.0-dev.20210504, 4.3.0-dev.20210503, 4.3.0-dev.20210502, 4.3.0-dev.20210501, 4.3.0-dev.20210430, 4.3.0-dev.20210429, 4.3.0-dev.20210428

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
