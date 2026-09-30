# clsx README 2.1.1: clsx [![CI](https://github.com/lukeed/clsx/workflows/CI/badge.svg)](https://github.com/lukeed/clsx/actions?query=workflow%3ACI) [![codecov](https://badgen.net/codecov/c/github/lukeed/clsx)](https://codecov.io/gh/lukeed/clsx) [![licenses](https://licenses.dev/b/npm/clsx)](https://licenses.dev/npm/clsx)
# джерело: https://raw.githubusercontent.com/lukeed/clsx/925494cf31bcd97d3337aacd34e659e80cae7fe2/readme.md
# отримано: 2026-09-30
# версія: 2.1.1

> A tiny (239B) utility for constructing `className` strings conditionally.Also serves as a faster & smaller drop-in replacement for the `classnames` module.

This module is available in three formats:

* **ES Module**: `dist/clsx.mjs`
* **CommonJS**: `dist/clsx.js`
* **UMD**: `dist/clsx.min.js`

## Install

```
$ npm install --save clsx
```

## Usage

```js
import clsx from 'clsx';
// or
import { clsx } from 'clsx';

// Strings (variadic)
clsx('foo', true && 'bar', 'baz');
//=> 'foo bar baz'

// Objects
clsx({ foo:true, bar:false, baz:isTrue() });
//=> 'foo baz'

// Objects (variadic)
clsx({ foo:true }, { bar:false }, null, { '--foobar':'hello' });
//=> 'foo --foobar'

// Arrays
clsx(['foo', 0, false, 'bar']);
//=> 'foo bar'

// Arrays (variadic)
clsx(['foo'], ['', 0, false, 'bar'], [['baz', [['hello'], 'there']]]);
//=> 'foo bar baz hello there'

// Kitchen sink (with nesting)
clsx('foo', [1 && 'bar', { baz:false, bat:null }, ['hello', ['world']]], 'cya');
//=> 'foo bar hello world cya'
```

## API

### clsx(...input)

Returns: `String`

#### input

Type: `Mixed`

The `clsx` function can take ***any*** number of arguments, each of which can be an Object, Array, Boolean, or String.

> **Important:** _Any_ falsey values are discarded!Standalone Boolean values are discarded as well.

```js
clsx(true, false, '', null, undefined, 0, NaN);
//=> ''
```

## Modes

There are multiple "versions" of `clsx` available, which allows you to bring only the functionality you need!

#### `clsx`

> **Size (gzip):** 239 bytes
> **Availability:** CommonJS, ES Module, UMD

The default `clsx` module; see API for info.

```js
import { clsx } from 'clsx';
// or
import clsx from 'clsx';
```

#### `clsx/lite`

> **Size (gzip):** 140 bytes
> **Availability:** CommonJS, ES Module
> **CAUTION:** Accepts **ONLY** string arguments!

Ideal for applications that ***only*** use the string-builder pattern.

Any non-string arguments are ignored!

```js
import { clsx } from 'clsx/lite';
// or
import clsx from 'clsx/lite';

// string
clsx('hello', true && 'foo', false && 'bar');
// => "hello foo"

// NOTE: Any non-string input(s) ignored
clsx({ foo: true });
//=> ""
```

## Benchmarks

For snapshots of cross-browser results, check out the `bench` directory~!

## Support

All versions of Node.js are supported.

All browsers that support `Array.isArray` are supported (IE9+).

>**Note:** For IE8 support and older, please install `clsx@1.0.x` and beware of #17.

## Tailwind Support

Here some additional (optional) steps to enable classes autocompletion using `clsx` with Tailwind CSS.

  Visual Studio Code

1. Install the "Tailwind CSS IntelliSense" Visual Studio Code extension

2. Add the following to your `settings.json`:

```json
   {
    "tailwindCSS.experimental.classRegex": [
      ["clsx\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
    ]
   }
```

You may find the `clsx/lite` module useful within Tailwind contexts. This is especially true if/when your application **only** composes classes in this pattern:

```js
clsx('text-base', props.active && 'text-primary', props.className);
```

## Related

- obj-str - A smaller (96B) and similiar utility that only works with Objects.

## License

MIT © Luke Edwards
