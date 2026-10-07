# Zod README 3.26.0-canary.20250609T052512 … 3.25.68-beta.1
# джерело: https://raw.githubusercontent.com/colinhacks/zod/aecd21f6e19dc5b4e64f70b6af4d1b94191f8f99/packages/zod/README.md
# отримано: 2026-09-28
# версія: 3.25.68-beta.1, 3.25.68-beta.0, 3.25.68-alpha.11, 3.25.68-alpha.10, 3.25.68-alpha.9, 3.25.68-alpha.8, 3.25.68-alpha.6, 3.25.68-alpha.5, 3.25.68-alpha.4, 3.25.68-alpha.3, 3.25.68-alpha.2, 3.26.0-canary.20250619T152955, 3.26.0-canary.20250618T044324, 3.25.67, 3.26.0-canary.20250616T222346, 3.25.66, 3.26.0-canary.20250616T185210, 3.25.65, 3.26.0-canary.20250616T170327, 3.25.64, 3.26.0-canary.20250612T071714, 3.25.63, 3.26.0-canary.20250612T065020, 3.26.0-canary.20250612T064810, 3.26.0-canary.20250611T202815, 3.25.62, 3.25.61, 3.25.60, 3.25.59, 3.26.0-canary.20250611T000856, 3.25.58, 3.26.0-canary.20250610T033234, 3.26.0-canary.20250610T031910, 3.26.0-canary.20250610T031755, 3.25.57, 3.26.0-canary.20250610T022604, 3.26.0-canary.20250609T234547, 3.26.0-canary.20250609T052512

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

Featured sponsor: Jazz

  Learn more about featured sponsorships

### Read the docs →

## What is Zod?

Zod is a TypeScript-first validation library. Define a schema and parse some data with it. You'll get back a strongly typed, validated result.

```ts
import { z } from "zod/v4";

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
import { z } from "zod/v4";

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
