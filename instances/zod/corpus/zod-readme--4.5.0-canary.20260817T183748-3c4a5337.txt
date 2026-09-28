# Zod README 4.5.0-canary.20260430T040905 … 4.5.0-canary.20260817T183748
# джерело: https://raw.githubusercontent.com/colinhacks/zod/f300476db2942180206a08af2f093534adfbdffa/packages/zod/README.md
# отримано: 2026-09-28
# версія: 4.5.0-canary.20260817T183748, 4.5.0-canary.20260817T002538, 4.5.0-canary.20260817T001220, 4.5.0-canary.20260817T005319, 4.5.0-canary.20260817T033812, 4.5.0-canary.20260817T002606, 4.5.0-canary.20260817T002539, 4.5.0-canary.20260817T002500, 4.5.0-canary.20260817T002434, 4.5.0-canary.20260817T011047, 4.5.0-canary.20260817T010613, 4.5.0-canary.20260817T013315, 4.5.0-canary.20260817T022854, 4.5.0-canary.20260817T025820, 4.5.0-canary.20260817T005756, 4.5.0-canary.20260816T234705, 4.5.0-canary.20260816T224749, 4.5.0-canary.20260816T230448, 4.5.0-canary.20260816T230440, 4.5.0-canary.20260816T230432, 4.5.0-canary.20260816T225339, 4.5.0-canary.20260816T230800, 4.5.0-canary.20260816T225249, 4.5.0-canary.20260816T230431, 4.5.0-canary.20260816T213049, 4.5.0-canary.20260816T212807, 4.5.0-canary.20260816T215437, 4.5.0-canary.20260816T212054, 4.5.0-canary.20260816T222439, 4.5.0-canary.20260816T221850, 4.5.0-canary.20260814T233931, 4.5.0-canary.20260814T055530, 4.5.0-canary.20260814T055510, 4.5.0-canary.20260814T053909, 4.5.0-canary.20260814T051949, 4.5.0-canary.20260814T023414, 4.5.0-canary.20260814T012954, 4.5.0-canary.20260814T012452, 4.5.0-canary.20260814T002126, 4.5.0-canary.20260814T002237, 4.5.0-canary.20260814T002144, 4.5.0-canary.20260814T000912, 4.5.0-canary.20260814T000703, 4.5.0-canary.20260814T000238, 4.5.0-canary.20260813T234848, 4.5.0-canary.20260813T234521, 4.5.0-canary.20260813T210915, 4.5.0-canary.20260813T210613, 4.5.0-canary.20260813T210419, 4.5.0-canary.20260813T205759, 4.5.0-canary.20260813T204917, 4.5.0-canary.20260813T201212, 4.5.0-canary.20260813T194619, 4.5.0-canary.20260813T184802, 4.5.0-canary.20260813T181206, 4.5.0-canary.20260813T055200, 4.5.0-canary.20260813T055010, 4.5.0-canary.20260813T053716, 4.5.0-canary.20260812T211928, 4.5.0-canary.20260812T201530, 4.5.0-canary.20260812T191817, 4.5.0-canary.20260812T190600, 4.5.0-canary.20260812T185642, 4.5.0-canary.20260812T184719, 4.5.0-canary.20260812T184640, 4.5.0-canary.20260812T183534, 4.5.0-canary.20260809T180500, 4.5.0-canary.20260809T165522, 4.5.0-canary.20260504T180558, 4.5.0-canary.20260504T173427, 4.5.0-canary.20260504T173320, 4.5.0-canary.20260504T165552, 4.4.3, 4.5.0-canary.20260504T070434, 4.5.0-canary.20260503T214107, 4.4.2, 4.5.0-canary.20260430T040905

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
