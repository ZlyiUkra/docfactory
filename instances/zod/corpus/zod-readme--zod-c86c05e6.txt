# Zod README 4.2.0-canary.20250911T045735 … 4.4.0-canary.20260125T215152
# джерело: https://raw.githubusercontent.com/colinhacks/zod/2d3671390f6cae4254642cf9ac7f16783eb6ff20/packages/zod/README.md
# отримано: 2026-09-28
# версія: 4.4.0-canary.20260125T215152, 4.4.0-canary.20260125T200840, 4.4.0-canary.20260125T200534, 4.4.0-canary.20260122T192419, 4.3.6, 4.4.0-canary.20260122T190614, 4.4.0-canary.20260122T174815, 4.4.0-canary.20260121T023401, 4.3.5, 4.3.4, 4.4.0-canary.20251231T230035, 4.4.0-canary.20251231T224656, 4.4.0-canary.20251231T211011, 4.3.3, 4.3.2, 4.4.0-canary.20251231T055727, 4.3.1, 4.3.0, 4.3.0-canary.20251231T042704, 4.3.0-canary.20251231T025730, 4.3.0-canary.20251231T012420, 4.3.0-canary.20251231T004216, 4.3.0-canary.20251231T000036, 4.3.0-canary.20251230T223005, 4.3.0-canary.20251230T222919, 4.3.0-canary.20251230T222623, 4.3.0-canary.20251230T221222, 4.3.0-canary.20251230T220815, 4.3.0-canary.20251230T180715, 4.3.0-canary.20251230T173842, 4.3.0-canary.20251230T173255, 4.3.0-canary.20251230T171456, 4.3.0-canary.20251230T021842, 4.3.0-canary.20251229T223913, 4.3.0-canary.20251229T203155, 4.3.0-canary.20251229T201908, 4.3.0-canary.20251229T201822, 4.3.0-canary.20251229T200951, 4.3.0-canary.20251229T193724, 4.3.0-canary.20251229T193106, 4.3.0-canary.20251229T192655, 4.3.0-canary.20251223T202943, 4.3.0-canary.20251223T032816, 4.3.0-canary.20251223T023855, 4.3.0-canary.20251222T205904, 4.3.0-canary.20251222T195342, 4.3.0-canary.20251222T061611, 4.3.0-canary.20251216T172808, 4.3.0-canary.20251216T031837, 4.3.0-canary.20251216T031750, 4.3.0-canary.20251216T030621, 4.2.1, 4.2.0, 4.2.0-canary.20251215T071855, 4.2.0-canary.20251213T203150, 4.2.0-canary.20251207T223211, 4.2.0-canary.20251202T062120, 4.1.13, 4.2.0-canary.20251124T022609, 4.2.0-canary.20251118T192410, 4.2.0-canary.20251118T185426, 4.2.0-canary.20251118T063547, 4.2.0-canary.20251118T062010, 4.2.0-canary.20251118T055751, 4.2.0-canary.20251118T055142, 4.2.0-canary.20251118T055019, 4.2.0-canary.20251118T054932, 4.2.0-canary.20251106T231624, 4.2.0-canary.20251106T214835, 4.2.0-canary.20251106T214242, 4.2.0-canary.20251106T212241, 4.2.0-canary.20251022T022243, 4.2.0-canary.20251021T174027, 4.2.0-canary.20251021T172355, 4.2.0-canary.20251017T221623, 4.2.0-canary.20251016T223057, 4.1.13-beta.0, 4.2.0-canary.20251015T161525, 4.1.12, 4.2.0-canary.20251001T172710, 4.2.0-canary.20250921T171445, 4.1.11, 4.1.10, 4.2.0-canary.20250920T163917, 4.1.9, 4.1.8, 4.1.7, 4.2.0-canary.20250911T052041, 4.2.0-canary.20250911T051520, 4.2.0-canary.20250911T051312, 4.2.0-canary.20250911T045937, 4.2.0-canary.20250911T045735

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
