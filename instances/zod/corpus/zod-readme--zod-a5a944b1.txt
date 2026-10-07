# Zod README 3.26.0-canary.20250522T214833 … 3.26.0-canary.20250528T013018
# джерело: https://raw.githubusercontent.com/colinhacks/zod/80cfd3a14cb53471783c75f9e4b341ed7e569f0f/README.md
# отримано: 2026-09-28
# версія: 3.26.0-canary.20250528T013018, 3.25.32, 3.26.0-canary.20250528T011954, 3.26.0-canary.20250528T005843, 3.26.0-canary.20250528T004006, 3.26.0-canary.20250528T002643, 3.26.0-canary.20250528T002114, 3.26.0-canary.20250528T002024, 3.25.31, 3.26.0-canary.20250527T212543, 3.26.0-canary.20250527T000523, 3.25.30, 3.26.0-canary.20250526T233714, 3.26.0-canary.20250526T222458, 3.25.29, 3.26.0-canary.20250526T211617, 3.26.0-canary.20250523T230539, 3.25.28, 3.26.0-canary.20250523T211959, 3.26.0-canary.20250523T204554, 3.25.27, 3.26.0-canary.20250523T194707, 3.25.26, 3.26.0-canary.20250523T194456, 3.25.25, 3.26.0-canary.20250523T184331, 3.25.24, 3.26.0-canary.20250523T183622, 3.26.0-canary.20250523T035151, 3.25.24-beta.0, 3.26.0-canary.20250523T001459, 3.26.0-canary.20250523T001348, 3.25.23, 3.26.0-canary.20250522T225330, 3.26.0-canary.20250522T225157, 3.26.0-canary.20250522T221534, 3.25.22, 3.26.0-canary.20250522T214931, 3.26.0-canary.20250522T214857, 3.26.0-canary.20250522T214833

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

```
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
