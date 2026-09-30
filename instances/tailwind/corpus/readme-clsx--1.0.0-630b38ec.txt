# clsx README 1.0.0: clsx [![Build Status](https://travis-ci.org/lukeed/clsx.svg?branch=master)](https://travis-ci.org/lukeed/clsx)
# джерело: https://raw.githubusercontent.com/lukeed/clsx/6c6d8713970b278bfe742b1c684759b30d140455/readme.md
# отримано: 2026-09-30
# версія: 1.0.0

> A tiny (200B) utility for constructing `className` strings conditionally.Also serves as a faster & smaller drop-in replacement for the `classnames` module.

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
clxs(true, false, '', null, undefined, 0, NaN);
//=> ''
```

## Benchmarks

For snapshots of cross-browser results, check out the `bench` directory~!

## Related

- obj-str - Similar utility that is faster and smaller (100B) but only works with Objects.

## License

MIT © Luke Edwards
