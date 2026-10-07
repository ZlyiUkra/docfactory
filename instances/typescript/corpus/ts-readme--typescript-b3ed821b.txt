# TypeScript README 3.5.0-dev.20190514 … 3.6.5: TypeScript
# джерело: https://raw.githubusercontent.com/microsoft/TypeScript/v3.6.5/README.md
# отримано: 2026-09-29
# версія: 3.6.5, 3.6.4, 3.6.3, 3.6.3-insiders.20190909, 3.6.2, 3.7.0-dev.20190816, 3.7.0-dev.20190815, 3.6.0-dev.20190814, 3.6.0-dev.20190813, 3.6.0-dev.20190810, 3.6.0-dev.20190809, 3.6.0-dev.20190808, 3.6.0-dev.20190807, 3.6.0-dev.20190806, 3.6.0-dev.20190804, 3.6.0-dev.20190803, 3.6.0-dev.20190802, 3.6.0-dev.20190801, 3.6.0-dev.20190730, 3.6.0-dev.20190727, 3.6.0-dev.20190726, 3.6.0-dev.20190725, 3.6.0-dev.20190724, 3.6.0-dev.20190723, 3.6.0-dev.20190720, 3.6.0-dev.20190719, 3.6.0-dev.20190718, 3.6.0-dev.20190717, 3.6.0-dev.20190716, 3.6.0-dev.20190713, 3.6.0-dev.20190712, 3.6.0-dev.20190711, 3.6.0-dev.20190710, 3.6.0-dev.20190709, 3.5.3, 3.6.0-dev.20190704, 3.6.0-dev.20190703, 3.6.0-dev.20190702, 3.6.0-dev.20190701, 3.6.0-dev.20190629, 3.6.0-dev.20190628, 3.6.0-dev.20190627, 3.6.0-dev.20190626, 3.6.0-dev.20190625, 3.6.0-dev.20190623, 3.6.0-dev.20190622, 3.6.0-dev.20190621, 3.6.0-dev.20190620, 3.6.0-dev.20190619, 3.6.0-dev.20190618, 3.6.0-dev.20190615, 3.6.0-dev.20190614, 3.5.2, 3.6.0-dev.20190613, 3.6.0-dev.20190612, 3.6.0-dev.20190611, 3.6.0-dev.20190608, 3.6.0-dev.20190607, 3.6.0-dev.20190606, 3.6.0-dev.20190604, 3.6.0-dev.20190603, 3.6.0-dev.20190602, 3.6.0-dev.20190601, 3.6.0-dev.20190531, 3.6.0-dev.20190530, 3.5.1, 3.5.0-dev.20190529, 3.5.0-dev.20190525, 3.5.0-dev.20190524, 3.5.0-dev.20190523, 3.5.0-dev.20190522, 3.5.0-dev.20190521, 3.5.0-dev.20190518, 3.5.0-dev.20190517, 3.5.0-dev.20190516, 3.5.0-dev.20190515, 3.5.0-dev.20190514

Join the chat at https://gitter.im/Microsoft/TypeScript
Build Status
VSTS Build Status
npm version
Downloads

TypeScript is a language for application-scale JavaScript. TypeScript adds optional types to JavaScript that support tools for large-scale JavaScript applications for any browser, for any host, on any OS. TypeScript compiles to readable, standards-based JavaScript. Try it out at the playground, and stay up to date via our blog and Twitter account.

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

```bash
git clone https://github.com/Microsoft/TypeScript.git
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
gulp local            # Build the compiler into built/local
gulp clean            # Delete the built compiler
gulp LKG              # Replace the last known good with the built one.
                      # Bootstrapping step to be executed when the built compiler reaches a stable state.
gulp tests            # Build the test infrastructure using the built compiler.
gulp runtests         # Run tests using the built compiler and test infrastructure.
                      # You can override the host or specify a test for this command.
                      # Use --host=<hostName> or --tests=<testPath>.
gulp baseline-accept  # This replaces the baseline test results with the results obtained from gulp runtests.
gulp lint             # Runs tslint on the TypeScript source.
gulp help             # List the above commands.
```

## Usage

```bash
node built/local/tsc.js hello.ts
```

## Roadmap

For details on our planned features and future direction please refer to our roadmap.
