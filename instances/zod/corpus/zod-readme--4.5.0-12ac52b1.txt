# Zod README 4.5.1 … 4.5.0
# джерело: https://raw.githubusercontent.com/colinhacks/zod/0a69bcb3d9554c6ec382ea9ba6b43c2421f3fa78/packages/zod/README.md
# отримано: 2026-09-28
# версія: 4.5.0, 4.5.1

  Zod

    TypeScript-first schema validation with static type inference

    by @colinhacks

  Docs
    •
  Discord
    •
  𝕏
    •
  Bluesky

### Read the docs →

## What is Zod?

Zod is a TypeScript-first validation library. Define a schema and parse some data with it. You'll get back a strongly typed, validated result.

```ts
import * as z from "zod";

const User = z.object({
  name: z.string(),
});

// some untrusted data...
const input = {
  /* stuff */
};

// the parsed result is validated and type safe!
const data = User.parse(input);

// so you can use it with confidence :)
console.log(data.name);
```

## Features

- Zero external dependencies
- Works in Node.js and all modern browsers
- Tiny: `2kb` core bundle (gzipped)
- Immutable API: methods return a new instance
- Concise interface
- Works with TypeScript and plain JS
- Built-in JSON Schema conversion
- Extensive ecosystem

## Installation

```sh
npm install zod
```

## Basic usage

Before you can do anything else, you need to define a schema. For the purposes of this guide, we'll use a simple object schema.

```ts
import * as z from "zod";

const Player = z.object({
  username: z.string(),
  xp: z.number(),
});
```

### Parsing data

Given any Zod schema, use `.parse` to validate an input. If it's valid, Zod returns a strongly-typed _deep clone_ of the input.

```ts
Player.parse({ username: "billie", xp: 100 });
// => returns { username: "billie", xp: 100 }
```

**Note** — If your schema uses certain asynchronous APIs like `async` refinements or transforms, you'll need to use the `.parseAsync()` method instead.

```ts
const schema = z.string().refine(async (val) => val.length <= 8);

await schema.parseAsync("hello");
// => "hello"
```

### AOT compilation

**Canary only** — compilation has not shipped in a stable release yet. Install with `npm install zod@canary`.

For hot validation paths, `z.compile(schema)` returns a schema clone with an ahead-of-time compiled fast path. Valid inputs take the compiled path; invalid inputs fall back to the regular parser so error reporting stays identical.

Across a 55-schema benchmark the median speedup is **2.4x**, and it scales with how much work the schema does per parse: a large array of objects is ~9x, a 20-key object ~9x, a nested object ~4.5x, while a bare `z.string()` gains nothing — compilation removes per-node dispatch and allocation, and a single `typeof` has none to remove.

```ts
const CompiledPlayer = z.compile(Player);

CompiledPlayer.parse({ username: "billie", xp: 100 });
```

To enable compilation globally for schemas constructed after import:

```ts
import "zod/compile"; // place before modules that define schemas
```

Things to know:

- Compilation uses `new Function`. Global mode is automatically disabled when `z.config({ jitless: true })` is set (e.g. CSP environments); calling `z.compile()` directly is an explicit opt-in.
- Schemas with async refinements or transforms can't be compiled, and neither can a few other constructs. That is not an error: `z.compile()` hands the schema back unchanged and it keeps using the regular parser, exactly as global mode leaves it. Pass `{ strict: true }` to throw `ZodCompileAsyncError` / `ZodCompileUnsupportedError` instead.
- On invalid input, refinements and transforms may run twice (fast path, then fallback).
- Deriving a new schema from a compiled one (`.refine()`, `.extend()`, etc.) returns an uncompiled schema — compile the final schema.

See `compile` docs for details.

### Handling errors

When validation fails, the `.parse()` method will throw a `ZodError` instance with granular information about the validation issues.

```ts
try {
  Player.parse({ username: 42, xp: "100" });
} catch (err) {
  if (err instanceof z.ZodError) {
    err.issues;
    /* [
      {
        expected: 'string',
        code: 'invalid_type',
        path: [ 'username' ],
        message: 'Invalid input: expected string'
      },
      {
        expected: 'number',
        code: 'invalid_type',
        path: [ 'xp' ],
        message: 'Invalid input: expected number'
      }
    ] */
  }
}
```

To avoid a `try/catch` block, you can use the `.safeParse()` method to get back a plain result object containing either the successfully parsed data or a `ZodError`. The result type is a discriminated union, so you can handle both cases conveniently.

```ts
const result = Player.safeParse({ username: 42, xp: "100" });
if (!result.success) {
  result.error; // ZodError instance
} else {
  result.data; // { username: string; xp: number }
}
```

**Note** — If your schema uses certain asynchronous APIs like `async` refinements or transforms, you'll need to use the `.safeParseAsync()` method instead.

```ts
const schema = z.string().refine(async (val) => val.length <= 8);

await schema.safeParseAsync("hello");
// => { success: true; data: "hello" }
```

### Inferring types

Zod infers a static type from your schema definitions. You can extract this type with the `z.infer<>` utility and use it however you like.

```ts
const Player = z.object({
  username: z.string(),
  xp: z.number(),
});

// extract the inferred type
type Player = z.infer<typeof Player>;

// use it in your code
const player: Player = { username: "billie", xp: 100 };
```

In some cases, the input & output types of a schema can diverge. For instance, the `.transform()` API can convert the input from one type to another. In these cases, you can extract the input and output types independently:

```ts
const mySchema = z.string().transform((val) => val.length);

type MySchemaIn = z.input<typeof mySchema>;
// => string

type MySchemaOut = z.output<typeof mySchema>; // equivalent to z.infer<typeof mySchema>
// number
```
