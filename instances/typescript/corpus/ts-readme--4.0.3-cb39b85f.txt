# TypeScript README 4.0.0-dev.20200620 … 4.0.3: TypeScript
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/v4.0.3/README.md
# отримано: 2026-09-29
# версія: 4.0.3, 4.0.2, 4.1.0-dev.20200820, 4.1.0-dev.20200819, 4.0.2-insiders.20200818, 4.1.0-dev.20200818, 4.1.0-dev.20200817, 4.1.0-dev.20200816, 4.1.0-dev.20200815, 4.1.0-dev.20200814, 4.0.1-insiders.20200813, 4.1.0-dev.20200813, 4.1.0-dev.20200812, 4.1.0-dev.20200811, 4.1.0-dev.20200810, 4.1.0-dev.20200809, 4.1.0-dev.20200808, 4.1.0-dev.20200807, 4.1.0-dev.20200806, 4.1.0-dev.20200805, 4.1.0-dev.20200804, 4.0.0-dev.20200803, 4.0.0-dev.20200802, 4.0.0-dev.20200801, 4.0.0-dev.20200731, 4.0.0-dev.20200730, 4.0.0-dev.20200729, 4.0.0-dev.20200728, 4.0.0-dev.20200727, 4.0.0-dev.20200726, 4.0.0-dev.20200725, 4.0.0-dev.20200724, 4.0.0-dev.20200722, 4.0.0-dev.20200721, 4.0.0-dev.20200720, 4.0.0-dev.20200719, 4.0.0-dev.20200718, 4.0.0-dev.20200717, 4.0.0-dev.20200715, 4.0.0-dev.20200714, 4.0.0-dev.20200712, 4.0.0-dev.20200711, 4.0.0-dev.20200710, 4.0.0-dev.20200709, 4.0.0-dev.20200708, 4.0.0-dev.20200707, 4.0.0-dev.20200706, 4.0.0-dev.20200705, 4.0.0-dev.20200704, 4.0.0-dev.20200703, 4.0.0-dev.20200702, 4.0.0-dev.20200701, 4.0.0-dev.20200630, 4.0.0-dev.20200629, 4.0.0-dev.20200628, 4.0.0-dev.20200627, 4.0.0-dev.20200626, 4.0.0-dev.20200625, 4.0.0-dev.20200624, 4.0.0-dev.20200623, 4.0.0-dev.20200622, 4.0.0-dev.20200621, 4.0.0-dev.20200620

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
* Read the language specification (docx,
 pdf, md).

This project has adopted the Microsoft Open Source Code of Conduct. For more information see
the Code of Conduct FAQ or contact opencode@microsoft.com
with any additional questions or comments.

## Documentation

*  TypeScript in 5 minutes
*  Programming handbook
*  Language specification
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
npm install
```

Use one of the following to build and test:

```
gulp local             # Build the compiler into built/local.
gulp clean             # Delete the built compiler.
gulp LKG               # Replace the last known good with the built one.
                       # Bootstrapping step to be executed when the built compiler reaches a stable state.
gulp tests             # Build the test infrastructure using the built compiler.
gulp runtests          # Run tests using the built compiler and test infrastructure.
                       # Some low-value tests are skipped when not on a CI machine - you can use the
                       # --skipPercent=0 command to override this behavior and run all tests locally.
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
