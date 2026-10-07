# Zod README 3.26.0-canary.20250528T020633 … 3.25.34
# джерело: https://raw.githubusercontent.com/colinhacks/zod/151242a42ce4f295a048b6fb047a2ed40bd16488/packages/zod/README.md
# отримано: 2026-09-28
# версія: 3.25.34, 3.26.0-canary.20250528T222817, 3.26.0-canary.20250528T222628, 3.26.0-canary.20250528T222428, 3.26.0-canary.20250528T221854, 3.26.0-canary.20250528T221601, 3.26.0-canary.20250528T213231, 3.25.33, 3.26.0-canary.20250528T073512, 3.26.0-canary.20250528T072349, 3.26.0-canary.20250528T072336, 3.26.0-canary.20250528T023515, 3.26.0-canary.20250528T020633

  Zod

    ✨ https://zod.dev ✨

    TypeScript-first schema validation with static type inference

  Documentation
    •
  Discord
    •
  npm
    •
  Issues
    •
  @colinhacks

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
const input = { /* stuff */ };

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
  xp: z.number()
});
```

### Parsing data

Given any Zod schema, use `.parse` to validate an input. If it's valid, Zod returns a strongly-typed *deep clone* of the input.

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
} catch(err){
  if(error instanceof z.ZodError){
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
  result.error;   // ZodError instance
} else {
  result.data;    // { username: string; xp: number }
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
  xp: z.number()
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
