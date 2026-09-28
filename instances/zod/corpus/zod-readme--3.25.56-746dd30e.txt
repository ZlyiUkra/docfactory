# Zod README 3.26.0-canary.20250529T003022 … 3.25.56
# джерело: https://raw.githubusercontent.com/colinhacks/zod/64bfb7001cf6f2575bf38b5e6130bc73b4b0e371/packages/zod/README.md
# отримано: 2026-09-28
# версія: 3.25.56, 3.25.55, 3.25.54, 3.26.0-canary.20250606T065527, 3.25.53, 3.26.0-canary.20250606T005819, 3.25.52, 3.26.0-canary.20250606T000146, 3.25.51, 3.26.0-canary.20250604T065310, 3.26.0-canary.20250604T051516, 3.26.0-canary.20250604T004138, 3.25.50, 3.26.0-canary.20250603T215911, 3.26.0-canary.20250603T214808, 3.26.0-canary.20250603T184912, 3.25.50-beta.0, 3.25.49, 3.26.0-canary.20250602T230223, 3.26.0-canary.20250602T225007, 3.26.0-canary.20250602T205719, 3.25.48, 3.26.0-canary.20250602T091550, 3.25.47, 3.26.0-canary.20250602T053849, 3.25.46, 3.26.0-canary.20250601T075015, 3.26.0-canary.20250601T051357, 3.26.0-canary.20250601T043802, 3.25.45, 3.26.0-canary.20250601T014551, 3.26.0-canary.20250601T010058, 3.25.44, 3.26.0-canary.20250601T003936, 3.26.0-canary.20250601T002740, 3.25.43, 3.26.0-canary.20250530T082844, 3.25.42, 3.26.0-canary.20250530T074358, 3.25.42-beta.3, 3.25.42-beta.2, 3.25.42-beta.1, 3.25.42-beta.0, 3.25.41, 3.25.40, 3.26.0-canary.20250530T011657, 3.26.0-canary.20250530T000501, 3.25.39, 3.25.38, 3.25.37, 3.26.0-canary.20250529T215305, 3.25.36, 3.25.35, 3.26.0-canary.20250529T070644, 3.26.0-canary.20250529T003022

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
  if (error instanceof z.ZodError) {
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
