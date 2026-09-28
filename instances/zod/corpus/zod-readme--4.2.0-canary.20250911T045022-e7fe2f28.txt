# Zod README 4.0.3 … 4.2.0-canary.20250911T045022
# джерело: https://raw.githubusercontent.com/colinhacks/zod/e87db1322f11ff6907e1789da28933d258ab75fd/packages/zod/README.md
# отримано: 2026-09-28
# версія: 4.2.0-canary.20250911T045022, 4.2.0-canary.20250911T044631, 4.2.0-canary.20250911T044505, 4.1.6, 4.1.6-beta.1, 4.1.6-beta.0, 4.2.0-canary.20250911T000242, 4.1.5, 4.2.0-canary.20250828T181323, 4.1.4, 4.2.0-canary.20250827T203557, 4.2.0-canary.20250827T070334, 4.1.3, 4.2.0-canary.20250826T001214, 4.2.0-canary.20250826T001136, 4.2.0-canary.20250826T000512, 4.2.0-canary.20250825T235836, 4.1.2, 4.2.0-canary.20250825T230433, 4.2.0-canary.20250824T204911, 4.1.1, 4.1.0, 4.1.0-canary.20250823T071728, 4.1.0-canary.20250823T071040, 4.1.0-canary.20250823T064644, 4.1.0-canary.20250821T014930, 4.1.0-canary.20250821T014902, 4.1.0-canary.20250813T051310, 4.0.17, 4.0.16, 4.1.0-canary.20250806T002637, 4.1.0-canary.20250806T000520, 4.0.15, 4.1.0-canary.20250804T184334, 4.1.0-canary.20250804T184136, 4.1.0-canary.20250730T094657, 4.0.14, 4.1.0-canary.20250730T051934, 4.0.13, 4.0.12, 4.1.0-canary.20250729T081926, 4.1.0-canary.20250729T053738, 4.1.0-canary.20250729T053029, 4.0.11, 4.1.0-canary.20250729T005826, 4.0.10, 4.1.0-canary.20250725T001018, 4.1.0-canary.20250724T211341, 4.0.9, 4.0.8, 4.0.7, 4.0.6, 4.1.0-canary.20250723T222937, 4.1.0-canary.20250723T221600, 4.1.0-canary.20250723T215716, 4.1.0-canary.20250723T214008, 4.1.0-canary.20250711T201420, 4.1.0-canary.20250711T200924, 4.1.0-canary.20250711T052917, 4.0.5, 4.1.0-canary.20250710T223408, 4.0.4, 4.1.0-canary.20250710T200141, 4.0.3

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
