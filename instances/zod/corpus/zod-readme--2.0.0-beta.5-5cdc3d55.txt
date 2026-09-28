# Zod README 2.0.0-beta.3 … 2.0.0-beta.5
# джерело: https://raw.githubusercontent.com/colinhacks/zod/9ee0d7928c544fecc2808bff5a6a3bf13609681e/README.md
# отримано: 2026-09-28
# версія: 2.0.0-beta.5, 2.0.0-beta.4, 2.0.0-beta.3

  Zod

if you're happy and you know it, star this repo ⭐

### **Sept 17 — Zod 2 is now in beta!**

You should be able to upgrade from v1 to v2 without any breaking changes to your code. Zod 2 is recommended for all new projects.

```
npm install zod@beta
yarn add zod@beta
```

Here are some of the new features.

- Transformers! These let you provide default values, do casting/coersion, and a lot more. Read more here: Transformers
- Asynchronous refinements and new `.parseAsync` and `.safeParseAsync` methods. Read more here: Refinements
- New object methods: `.passthrough()`, `.strict()`, and `.catchall()`. Read more here: Objects

In almost all cases, you'll be able to upgrade to Zod 2 without changing any code. Here are some of the (very minor) breaking changes:

- Parsing now returns a _deep clone_ of the data you pass in. Previously it returned the exact same object you passed in.
- Relatedly, Zod _no longer_ supports cyclical _data_. Recursive schemas are still supported, but Zod can't properly parse nested objects that contain cycles.
- Object schemas now strip unknown keys by default, instead of throwing an error
- Optional and nullable schemas are now represented with the dedicated ZodOptional and ZodNullable classes, instead of using ZodUnion.

---

Aug 30 — zod@1.11 was released with lots of cool features!

- All schemas now have a `.safeParse` method. This lets you validate data in a more functional way, similar to `io-ts`: https://github.com/vriad/zod#safe-parse
- String schemas have a new `.regex` refinement method: https://github.com/vriad/zod#strings
- Object schemas now have two new methods: `.primitives()` and `.nonprimitives()`. These methods let you quickly pick or omit primitive fields from objects, useful for validating API inputs: https://github.com/vriad/zod#primitives-and-nonprimitives
- Zod now provides `z.nativeEnum()`, which lets you create z Zod schema from an existing TypeScript `enum`: https://github.com/vriad/zod#native-enums

## What is Zod

Zod is a TypeScript-first schema declaration and validation library. I'm using the term "schema" to broadly refer to any data type/structure, from a simple `string` to a complex nested object.

Zod is designed to be as developer-friendly as possible. My goal is to eliminate duplicative type declarations wherever possible. With Zod, you declare a validator _once_ and Zod will automatically infer the static TypeScript type. It's easy to compose simpler types into complex data structures.

Some other great aspects:

- Zero dependencies
- Plain JavaScript: works in browsers and Node.js
- Tiny: 8kb minified + zipped
- Immutability: methods (i.e. `.optional()` return a new instance
- Concise, chainable interface
- Functional approach: parse, don't validate

## Sponsorship

I work on Zod in my free time, so if you're making money from a product that is built with Zod, I'd massively appreciate sponsorship at any level. For solo devs, I recommend the Chipotle Bowl tier or the Cup of Coffee tier.

### Sponsors

      Kevin Simper

      @kevinsimper

      Brandon Bayer

      @flybayer,
      creator of Blitz.js

_To get your name + Twitter + website here, sponsor Zod at the Freelancer or Consultancy tier._

## Table of contents

- Installation

- Primitives
- Literals
- Parsing
- Type inference
- Refinements
- Strings
- Numbers
- Objects
  - .shape
  - .merge
  - .extend
  - .pick/.omit
  - .partial/.deepPartial
  - .passthrough
  - .strict
  - .primitives/.nonprimitives
- Records
- Arrays
  - .nonempty
- Unions
  - .optional
  - .nullable
- Enums
- Intersections
- Tuples
- Recursive types
  - JSON type
  - Cyclical data
- Promises
- Instanceof
- Function schemas
- Transformers
- Errors
- Comparison
  - Joi
  - Yup
  - io-ts
  - Runtypes
- Changelog

## Installation

To use the beta of Zod 2 (recommended for new projects).

```
yarn add zod@beta
npm install zod@beta
```

To install the most recent v1 version:

```sh
yarn add zod
npm install zod
```

#### TypeScript requirements

- Zod 2.x requires TypeScript 3.7+
- Zod 1.x requires TypeScript 3.3+

> Support for TS 3.2 was dropped with the release of zod@1.10 on 19 July 2020

You must enable `strictNullChecks` or use `strict` mode which includes `strictNullChecks`. Otherwise Zod can't correctly infer the types of your schemas!

```ts
// tsconfig.json
{
  // ...
  "compilerOptions": {
    // ...
    "strictNullChecks": true
  }
}
```

## Usage

Zod is a validation library designed for optimal developer experience. It's a TypeScript-first schema declaration library with rigorous inferred types, incredible developer experience, and a few killer features missing from the existing libraries.

- Zero dependencies (5kb compressed)
- Immutability; methods (i.e. `.optional()` return a new instance
- Concise, chainable interface
- Functional approach ("Parse, don't validate!")

## Primitives

You can create a Zod schema for any TypeScript primitive.

```ts
import * as z from 'zod';

// primitive values
z.string();
z.number();
z.bigint();
z.boolean();
z.date();

// empty types
z.undefined();
z.null();
z.void();

// catch-all types
z.any();
z.unknown();
```

## Literals

```ts
const tuna = z.literal('tuna');
const twelve = z.literal(12);
const tru = z.literal(true);
```

> Currently there is no support for Date or bigint literals in Zod. If you have a use case for this feature, please file an issue.

## Validation

### Parsing

`.parse(data:unknown): T`

Given any Zod schema, you can call its `.parse` method to check `data` is valid. If it is, a value is returned with full type information! Otherwise, an error is thrown.

> IMPORTANT: In Zod 2 and Zod 1.11+, the value returned by `.parse` is a _deep clone_ of the variable you passed in. This was also the case in zod@1.4 and earlier.

```ts
const stringSchema = z.string();
stringSchema.parse('fish'); // => returns "fish"
stringSchema.parse(12); // throws Error('Non-string type: number');
```

### Safe parse

`.safeParse(data:unknown): { success: true; data: T; } | { success: false; error: ZodError; }`

If you don't want Zod to throw when validation errors occur, you can use `.safeParse`. This method returns an object, even if validation errors occur:

```ts
stringSchema.safeParse(12);
// => { successs: false; error: ZodError }

stringSchema.safeParse('billie');
// => { successs: true; data: 'billie' }
```

There is also an asynchronous version:

```ts
await stringSchema.safeParseAsync('billie');
```

> You must use .parseAsync() or .safeParseAsync() if your schema contains asynchronous refinements for transformers.

The result is a _discriminated union_ so you can handle errors very conveniently:

```ts
const result = stringSchema.safeParse('billie');
if (!result.success) {
  // handle error then return
  return;
}

// underneath the if statement, TypeScript knows
// that validation passed
console.log(result.data);
```

> Errors thrown from within refinement functions will _not_ be caught.

### Type guards

`.check(data:unknown)`

You can also use a Zod schema as a type guard using the schema's `.check()` method, like so:

```ts
const stringSchema = z.string();
const blob: any = 'Albuquerque';
if (stringSchema.check(blob)) {
  // blob is now of type `string`
  // within this if statement
}
```

You can use the same method to check for invalid data:

```ts
const stringSchema = z.string();

const process = (blob: any) => {
  if (!stringSchema.check(blob)) {
    throw new Error('Not a string');
  }

  // blob is now of type `string`
  // underneath the if statement
};
```

### Refinements

`.refine(validator: (data:T)=>any, params?: RefineParams)`

Zod let you provide custom validation logic via _refinements_.

Zod was designed to mirror TypeScript as closely as possible. But there are many so-called "refinement types" you may wish to check for that can't be represented in TypeScript's type system. For instance: checking that a number is an Int or that a string is a valid email address.

For example, you can define a custom validation check on _any_ Zod schema with `.refine`:

```ts
const myString = z.string().refine(val => val.length <= 255, {
  message: "String can't be more than 255 characters",
});
```

Refinements can also be async:

```ts
const userId = z.string().refine(async id => {
  // verify that ID exists in database
  return true;
});
```

> If you use async refinements, you must use the `.parseAsync` method to parse data! Otherwise Zod will throw an error.

As you can see, `.refine` takes two arguments.

1. The first is the validation function. This function takes one input (of type `T` — the inferred type of the schema) and returns `any`. Any truthy value will pass validation. (Prior to zod@1.6.2 the validation function had to return a boolean.)
2. The second argument accepts some options. You can use this to customize certain error-handling behavior:

```ts
   type RefineParams = {
     // override error message
     message?: string;

     // appended to error path
     path?: (string | number)[];

     // params object you can use to customize message
     // in error map
     params?: object;
   };
```

These options let you define powerful custom behavior. Zod is commonly used for form validation. If you want to verify that "password" and "confirm" match, you can do so like this:

```ts
const passwordForm = z
  .object({
    password: z.string(),
    confirm: z.string(),
  })
  .refine(data => data.password === data.confirm, {
    message: "Passwords don't match",
    path: ['confirm'], // path of error
  })
  .parse({ password: 'asdf', confirm: 'qwer' });
```

Because you provided a `path` parameter, the resulting error will be:

```ts
ZodError {
  errors: [{
    "code": "custom_error",
    "path": [ "confirm" ],
    "message": "Passwords don't match"
  }]
}
```

Note that the `path` is set to `["confirm"]`, so you can easily display this error underneath the "Confirm password" textbox.

Important note, the value passed to the `path` option is _concatenated_ to the actual error path. So if you took `passwordForm` from above and nested it inside another object, you would still get the error path you expect.

```ts
const allForms = z.object({ passwordForm }).parse({
  passwordForm: {
    password: 'asdf',
    confirm: 'qwer',
  },
});
```

would result in

```
ZodError {
  errors: [{
    "code": "custom_error",
    "path": [ "passwordForm", "confirm" ],
    "message": "Passwords don't match"
  }]
}
```

## Type inference

You can extract the TypeScript type of any schema with `z.infer<typeof mySchema>`.

```ts
const A = z.string();
type A = z.infer<typeof A>; // string

const u: A = 12; // TypeError
const u: A = 'asdf'; // compiles
```

We'll include examples of inferred types throughout the rest of the documentation.

## Strings

There are a handful of string-specific validations.

All of these validations allow you to _optionally_ specify a custom error message.

```ts
z.string().min(5);
z.string().max(5);
z.string().length(5);
z.string().email();
z.string().url();
z.string().uuid();
z.string().regex(regex);
```

> Check out validator.js for a bunch of other useful string validation functions.

### Custom error messages

Like `.refine`, The final (optional) argument is an object that lets you provide a custom error in the `message` field.

```ts
z.string().min(5, { message: 'Must be 5 or more characters long' });
z.string().max(5, { message: 'Must be 5 or fewer characters long' });
z.string().length(5, { message: 'Must be exactly 5 characters long' });
z.string().email({ message: 'Invalid email address.' });
z.string().url({ message: 'Invalid url' });
z.string().uuid({ message: 'Invalid UUID' });
```

> To see the email and url regexes, check out this file. To use a more advanced method, use a custom refinement.

## Numbers

There are a handful of number-specific validations.

```ts
z.number().min(5);
z.number().max(5);

z.number().int(); // value must be an integer

z.number().positive(); //     > 0
z.number().nonnegative(); //  >= 0
z.number().negative(); //     < 0
z.number().nonpositive(); //  <= 0
```

You can optionally pass in a params object as the second argument to provide a custom error message.

```ts
z.number().max(5, { message: 'this👏is👏too👏big' });
```

## Objects

```ts
// all properties are required by default
const dogSchema = z.object({
  name: z.string(),
  age: z.number(),
});

type Dog = z.infer<typeof dogSchema>;
/*
equivalent to:
type Dog = {
  name: string;
  age: number;
}
*/

const cujo = dogSchema.parse({
  name: 'Cujo',
  age: 4,
}); // passes, returns Dog

const fido: Dog = {
  name: 'Fido',
}; // TypeError: missing required property `age`
```

#### `.shape` property

Use `.shape` to access an object schema's property schemas.

```ts
const Location = z.object({
  latitude: z.number(),
  longitude: z.number(),
});

const Business = z.object({
  location: Location,
});

Business.shape.location; // => Location schema
```

#### Merging

You can combine two object schemas with `.merge`, like so:

```ts
const BaseTeacher = z.object({ subjects: z.array(z.string()) });
const HasID = z.object({ id: z.string() });

const Teacher = BaseTeacher.merge(HasID);
type Teacher = z.infer<typeof Teacher>; // => { subjects: string[], id: string }
```

You're able to fluently chain together many `.merge` calls as well:

```ts
// chaining mixins
const Teacher = BaseTeacher.merge(HasId)
  .merge(HasName)
  .merge(HasAddress);
```

> IMPORTANT: the schema returned by `.merge` is the _intersection_ of the two schemas. The schema passed into `.merge` does not "overwrite" properties of the original schema. To demonstrate:

```ts
const Obj1 = z.object({ field: z.string() });
const Obj2 = z.object({ field: z.number() });

const Merged = Obj1.merge(Obj2);

type Merged = z.infer<typeof merged>;
// => { field: never }
// because no type can simultaneously be both a string and a number
```

To "overwrite" existing keys, use `.extend` (documented below).

#### Extending objects

You can add additional fields an object schema with the `.extend` method.

> Before zod@1.8 this method was called `.augment`. The `augment` method is still available for backwards compatibility but it is deprecated and will be removed in a future release.

```ts
const Animal = z
  .object({
    species: z.string(),
  })
  .extend({
    population: z.number(),
  });
```

> ⚠️ You can use `.extend` to overwrite fields! Be careful with this power!

```ts
// overwrites `species`
const ModifiedAnimal = Animal.extend({
  species: z.array(z.string()),
});

// => { population: number, species: string[] }
```

#### Pick and omit

Object masking is one of Zod's killer features. It lets you create slight variations of your object schemas easily and succinctly. Inspired by TypeScript's built-in `Pick` and `Omit` utility types, all Zod object schemas have `.pick` and `.omit` methods that return a "masked" version of the schema.

```ts
const Recipe = z.object({
  id: z.string(),
  name: z.string(),
  ingredients: z.array(z.string()),
});
```

To only keep certain keys, use `.pick`.

```ts
const JustTheName = Recipe.pick({ name: true });

type JustTheName = z.infer<typeof JustTheName>;
// => { name: string }
```

To remove certain keys, use `.omit`.

```ts
const NoIDRecipe = Recipe.omit({ id: true });

type NoIDRecipe = z.infer<typeof NoIDRecipe>;
// => { name: string, ingredients: string[] }
```

This is useful for database logic, where endpoints often accept as input slightly modified versions of your database schemas. For instance, the input to a hypothetical `createRecipe` endpoint would accept the `NoIDRecipe` type, since the ID will be generated by your database automatically.

> This is a vital feature for implementing typesafe backend logic, yet as far as I know, no other validation library (yup, Joi, io-ts, runtypes, class-validator, ow...) offers similar functionality as of this writing (April 2020). This is one of the must-have features that inspired the creation of Zod.

#### Partials

Inspired by the built-in TypeScript utility type Partial, all Zod object schemas have a `.partial` method that makes all properties optional.

Starting from this object:

```ts
const user = z.object({
  username: z.string(),
  location: z.object({
    latitude: z.number(),
    longitude: z.number(),
  }),
});
/*
  { username: string, location: { city: number, state: number } }
*/
```

We can create a partial version:

```ts
const partialUser = user.partial();
/*
{
  username?: string | undefined,
  location?: {
    city: number;
    state: number;
  } | undefined
}
*/

// equivalent to:
const partialUser = z.object({
  username: user.shape.username.optional(),
  location: user.shape.location.optional(),
});
```

Or you can use `.deepPartial`:

```ts
const deepPartialUser = user.deepPartial();

/*
{
  username?: string | undefined,
  location?: {
    latitude?: number | undefined;
    longitude?: number | undefined;
  } | undefined
}
*/
```

> Important limitation: deep partials only work as expected in hierarchies of object schemas. It also can't be used on recursive schemas currently, since creating a recursive schema requires casting to the generic `ZodSchema` type (which doesn't include all the methods of the `ZodObject` class). Currently an improved version of Zod is under development that will have better support for recursive schemas.

#### Unknown keys

By default Zod object schema strip unknown keys from the output.

> ⚠️ Before version 2, Zod did NOT allow unknown keys by default.

Zod will return

```ts
const person = z.object({
  name: z.string(),
});

person.parse({
  name: 'bob dylan',
  extraKey: 61,
});
// => { name: "bob dylan" }
```

#### Pass through unknown keys

If you want to pass through unknown keys, use `.passthrough()`.

> For backwards compatibility, you can also use `.nonstrict()` which behaves identically.

```ts
const person = z
  .object({
    name: z.string(),
  })
  .passthrough();

person.parse({
  name: 'bob dylan',
  extraKey: 61,
});
// => { name: "bob dylan", extraKey: 61 }
```

#### Disallow unknown keys

You can _disallow_ unknown keys with `.strict()`. If there are any unknown keys in the input, Zod will throw an error.

```ts
const person = z
  .object({
    name: z.string(),
  })
  .strict();

person.parse({
  name: 'bob dylan',
  extraKey: 61,
});
// => throws ZodError
```

#### Primitives and nonprimitives

Zod provides a convenience method for automatically picking all primitive or non-primitive fields from an object schema.

```ts
const Post = z.object({
  title: z.string()
});

const User = z.object({
  id: z.number(),
  name: z.string(),
  posts: z.array(Post)
});

const UserFields = User.primitives();
typeof UserFields = z.infer<typeof UserFields>;
// => { id: number; name; string; }

const UserRelations = User.nonprimitives();
typeof UserFields = z.infer<typeof UserFields>;
// => { posts: Post[] }
```

These schemas are considering "primitive":

- string
- number
- boolean
- bigint
- date
- null/undefined
- enums
- any array of the above types
- any union of the above types

#### Catchall

You can add a `catchall` schema with `.catchall()`. All unknown keys will be validated against the catchall schema.

```ts
const person = z
  .object({
    name: z.string(),
  })
  .catchall(z.number());

person.parse({
  name: 'bob dylan',
  validExtraKey: 61, // works fine
});
// => { name: "bob dylan" }
```

> Using `.catchall()` overrides `.passsthrough()`, `.strip()`, or `.strict()`. All keys are now considered "known".

## Records

Record schemas are used to validate types such as this:

```ts
type NumberCache = { [k: string]: number };
```

If you want to validate that all the _values_ of an object match some schema, without caring about the keys, you should use a Record.

```ts
const User = z.object({
  name: z.string(),
});

const UserStore = z.record(User);

type UserStore = z.infer<typeof UserStore>;
// => { [k: string]: User }
```

This is particularly useful for storing or caching items by ID.

```ts
const userStore: UserStore = {};

userStore['77d2586b-9e8e-4ecf-8b21-ea7e0530eadd'] = {
  name: 'Carlotta',
}; // passes

userStore['77d2586b-9e8e-4ecf-8b21-ea7e0530eadd'] = {
  whatever: 'Ice cream sundae',
}; // TypeError
```

And of course you can call `.parse` just like any other Zod schema.

```ts
UserStore.parse({
  user_1328741234: { name: 'James' },
}); // => passes
```

#### A note on numerical keys

You may have expected `z.record()` to accept two arguments, one for the keys and one for the values. After all, TypeScript's built-in Record type does: `Record<KeyType, ValueType>`. Otherwise, how do you represent the TypeScript type `Record<number, any>` in Zod?

As it turns out, TypeScript's behavior surrounding `[k: number]` is a little unintuitive:

```ts
const testMap: { [k: number]: string } = {
  1: 'one',
};

for (const key in testMap) {
  console.log(`${key}: ${typeof key}`);
}
// prints: `1: string`
```

As you can see, JavaScript automatically casts all object keys to strings under the hood.

Since Zod is trying to bridge the gap between static and runtime types, it doesn't make sense to provide a way of creating a record schema with numerical keys, since there's no such thing as a numerical key in runtime JavaScript.

## Arrays

There are two ways to define array schemas:

#### `z.array(arg: ZodSchema)`

First, you can create an array schema with the `z.array()` function; it accepts another ZodSchema, which defines the type of each array element.

```ts
const stringArray = z.array(z.string());
// inferred type: string[]
```

#### the `.array()` method

Second, you can call the `.array()` method on **any** Zod schema:

```ts
const stringArray = z.string().array();
// inferred type: string[]
```

You have to be careful with the `.array()` method. It returns a new `ZodArray` instance. This means you need to be careful about the _order_ in which you call methods. These two schemas are very different:

```ts
z.string()
  .undefined()
  .array(); // (string | undefined)[]
z.string()
  .array()
  .undefined(); // string[] | undefined
```

#### Non-empty lists

```ts
const nonEmptyStrings = z
  .string()
  .array()
  .nonempty();
// [string, ...string[]]

nonEmptyStrings.parse([]); // throws: "Array cannot be empty"
nonEmptyStrings.parse(['Ariana Grande']); // passes
```

#### Length validations

```ts
// must contain 5 or more items
z.array(z.string()).min(5);

// must contain 5 or fewer items
z.array(z.string()).max(5);

// must contain exactly 5 items
z.array(z.string()).length(5);
```

## Unions

Zod includes a built-in `z.union` method for composing "OR" types.

```ts
const stringOrNumber = z.union([z.string(), z.number()]);

stringOrNumber.parse('foo'); // passes
stringOrNumber.parse(14); // passes
```

Zod will test the input against each of the "options" in order and return the first value that validates successfully.

## Optional types

You can make any schema optional with `z.optional()`:

```ts
const A = z.optional(z.string());

A.parse(undefined); // => passes, returns undefined
type A = z.infer<typeof A>; // string | undefined
```

You can also call the `.optional()` method on an existing schema:

```ts
const B = z.boolean().optional();

const C = z.object({
  username: z.string().optional(),
});
type C = z.infer<typeof C>; // { username?: string | undefined };
```

## Nullable types

Similarly, you can create nullable types like so:

```ts
const D = z.nullable(z.string());
D.parse('asdf'); // => "asdf"
D.parse(null); // => null
```

Or you can use the `.optional()` method on any existing schema:

```ts
const E = z.string().nullable(); // equivalent to D
type E = z.infer<typeof D>; // string | null
```

You can create unions of any two or more schemas.

## Enums

There are two ways to define enums in Zod.

### Zod enums

An enum is just a union of string literals, so you _could_ define an enum like this:

```ts
const FishEnum = z.union([
  z.literal('Salmon'),
  z.literal('Tuna'),
  z.literal('Trout'),
]);

FishEnum.parse('Salmon'); // => "Salmon"
FishEnum.parse('Flounder'); // => throws
```

For convenience Zod provides a built-in `z.enum()` function. Here's is the equivalent code:

```ts
const FishEnum = z.enum(['Salmon', 'Tuna', 'Trout']);

type FishEnum = z.infer<typeof FishEnum>;
// 'Salmon' | 'Tuna' | 'Trout'
```

> Important! You need to pass the literal array _directly_ into z.enum(). Do not define it separately, than pass it in as a variable! This is required for proper type inference.

**Autocompletion**

To get autocompletion with a Zod enum, use the `.enum` property of your schema:

```ts
FishEnum.enum.Salmon; // => autocompletes

FishEnum.enum;
/*
=> {
  Salmon: "Salmon",
  Tuna: "Tuna",
  Trout: "Trout",
}
*/
```

You can also retrieve the list of options as a tuple with the `.options` property:

```ts
FishEnum.options; // ["Salmon", "Tuna", "Trout"]);
```

### Native enums

> ⚠️ `nativeEnum()` requires TypeScript 3.6 or higher!

Zod enums are the recommended approach to defining and validating enums. But there may be scenarios where you need to validate against an enum from a third-party library, or perhaps you don't want to rewrite your existing enums. For this you can use `z.nativeEnum()`.

**Numeric enums**

```ts
enum Fruits {
  Apple,
  Banana,
}

const FruitEnum = z.nativeEnum(Fruits);
type FruitEnum = z.infer<typeof FruitEnum>; // Fruits

FruitEnum.parse(Fruits.Apple); // passes
FruitEnum.parse(Fruits.Banana); // passes
FruitEnum.parse(0); // passes
FruitEnum.parse(1); // passes
FruitEnum.parse(3); // fails
```

**String enums**

```ts
enum Fruits {
  Apple = 'apple',
  Banana = 'banana',
  Cantaloupe, // you can mix numerical and string enums
}

const FruitEnum = z.nativeEnum(Fruits);
type FruitEnum = z.infer<typeof FruitEnum>; // Fruits

FruitEnum.parse(Fruits.Apple); // passes
FruitEnum.parse(Fruits.Cantaloupe); // passes
FruitEnum.parse('apple'); // passes
FruitEnum.parse('banana'); // passes
FruitEnum.parse(0); // passes
FruitEnum.parse('Cantaloupe'); // fails
```

**Const enums**

The `.nativeEnum()` function works for `as const` objects as well. ⚠️ `as const` required TypeScript 3.4+!

```ts
const Fruits = {
  Apple: 'apple',
  Banana: 'banana',
  Cantaloupe: 3,
} as const;

const FruitEnum = z.nativeEnum(Fruits);
type FruitEnum = z.infer<typeof FruitEnum>; // "apple" | "banana" | 3

FruitEnum.parse('apple'); // passes
FruitEnum.parse('banana'); // passes
FruitEnum.parse(3); // passes
FruitEnum.parse('Cantaloupe'); // fails
```

## Intersections

Intersections are useful for creating "logical AND" types.

```ts
const a = z.union([z.number(), z.string()]);
const b = z.union([z.number(), z.boolean()]);
const c = z.intersection(a, b);

type c = z.infer<typeof c>; // => number

const stringAndNumber = z.intersection(z.string(), z.number());
type Never = z.infer<typeof stringAndNumber>; // => never
```

## Tuples

These differ from arrays in that they have a fixed number of elements, and each element can have a different type.

```ts
const athleteSchema = z.tuple([
  // takes an array of schemas
  z.string(), // name
  z.number(), // jersey number
  z.object({
    pointsScored: z.number(),
  }), // statistics
]);

type Athlete = z.infer<typeof athleteSchema>;
// type Athlete = [string, number, { pointsScored: number }]
```

## Recursive types

You can define a recursive schema in Zod, but because of a limitation of TypeScript, their type can't be statically inferred. If you need a recursive Zod schema you'll need to define the type definition manually, and provide it to Zod as a "type hint".

```ts
interface Category {
  name: string;
  subcategories: Category[];
}

const Category: z.ZodSchema<Category> = z.lazy(() =>
  z.object({
    name: z.string(),
    subcategories: z.array(Category),
  }),
);

Category.parse({
  name: 'People',
  subcategories: [
    {
      name: 'Politicians',
      subcategories: [{ name: 'Presidents', subcategories: [] }],
    },
  ],
}); // passes
```

Unfortunately this code is a bit duplicative, since you're declaring the types twice: once in the interface and again in the Zod definition.

If your schema has lots of primitive fields, there's a way of reducing the amount of duplication:

```ts
// define all the non-recursive stuff here
const BaseCategory = z.object({
  name: z.string(),
  tags: z.array(z.string()),
  itemCount: z.number(),
});

// create an interface that extends the base schema
interface Category extends z.infer<typeof BaseCategory> {
  subcategories: Category[];
}

// merge the base schema with
// a new Zod schema containing relations
const Category: z.ZodSchema<Category> = BaseCategory.merge(
  z.object({
    subcategories: z.lazy(() => z.array(Category)),
  }),
);
```

#### JSON type

If you want to validate any JSON value, you can use the snippet below. This requires TypeScript 3.7 or higher!

```ts
type Literal = boolean | null | number | string;
type Json = Literal | { [key: string]: Json } | Json[];
const literalSchema = z.union([z.string(), z.number(), z.boolean(), z.null()]);
const jsonSchema: z.ZodSchema<Json> = z.lazy(() =>
  z.union([literalSchema, z.array(jsonSchema), z.record(jsonSchema)]),
);

jsonSchema.parse({
  // data
});
```

Thanks to ggoodman for suggesting this.

#### Cyclical objects

As of Zod 2, Zod _no longer_ supports cyclical objects. If you absolutely need this feature you can still use Zod v1.

## Promises

```ts
const numberPromise = z.promise(z.number());
```

"Parsing" works a little differently with promise schemas. Validation happens in two parts:

1. Zod synchronously checks that the input is an instance of Promise (i.e. an object with `.then` and `.catch` methods.).
2. Zod _waits for the promise to resolve_ then validates the resolved value.

```ts
numberPromise.parse('tuna');
// ZodError: Non-Promise type: string

numberPromise.parse(Promise.resolve('tuna'));
// => Promise<number>

const test = async () => {
  await numberPromise.parse(Promise.resolve('tuna'));
  // ZodError: Non-number type: string

  await numberPromise.parse(Promise.resolve(3.14));
  // => 3.14
};
```

#### Non-native promise implementations

When "parsing" a promise, Zod checks that the passed value is an object with `.then` and `.catch` methods — that's it. So you should be able to pass non-native Promises (Bluebird, etc) into `z.promise(...).parse` with no trouble. One gotcha: the return type of the parse function will be a _native_ `Promise`, so if you have downstream logic that uses non-standard Promise methods, this won't work.

## Instanceof

You can use `z.instanceof` to create a schema that checks if the input is an instance of a class.

```ts
class Test {
  name: string;
}

const TestSchema = z.instanceof(Test);

const blob: any = 'whatever';
if (TestSchema.check(blob)) {
  blob.name; // Test instance
}
```

## Function schemas

Zod also lets you define "function schemas". This makes it easy to validate the inputs and outputs of a function without intermixing your validation code and "business logic".

You can create a function schema with `z.function(args, returnType)`.

```ts
const myFunction = z.function();

type myFunction = z.infer<typeof myFunction>;
// => ()=>unknown
```

You can use the `.args` and `.returns` methods to refine your function schema:

```ts
const myFunction = z
  .function()
  .args(z.string(), z.number()) // accepts an arbitrary number of arguments
  .returns(z.boolean());
type myFunction = z.infer<typeof myFunction>;
// => (arg0: string, arg1: number)=>boolean
```

> You can use the special `z.void()` option if your function doesn't return anything. This will let Zod properly infer the type of void-returning functions. (Void-returning function can actually return either undefined or null.)

Function schemas have an `.implement()` method which accepts a function and returns a new function.

```ts
const trimmedLength = z
  .function()
  .args(z.string()) // accepts an arbitrary number of arguments
  .returns(z.number())
  .implement(x => {
    // TypeScript knows x is a string!
    return x.trim().length;
  });

trimmedLength('sandwich'); // => 8
trimmedLength(' asdf '); // => 4
```

`myValidatedFunction` now automatically validates both its inputs and return value against the schemas provided to `z.function`. If either is invalid, the function throws. This way you can confidently write application logic in a "validated function" without worrying about invalid inputs, scattering `schema.validate()` calls in your endpoint definitions,or writing duplicative types for your functions.

Here's a more complex example showing how to write a typesafe API query endpoint:

```ts
const FetcherEndpoint = z
  .function(args, returnType)
  .args(z.object({ id: z.string() }))
  .returns(
    z.promise(
      z.object({
        id: string(),
        name: string(),
      }),
    ),
  );

const getUserByID = FetcherEndpoint.validate(args => {
  args; // => { id: string }

  const user = await User.findByID(args.id);

  // TypeScript statically verifies that value returned by
  // this function is of type Promise<{ id: string; name: string; }>
  return 'salmon'; // TypeError

  return user; // compiles successfully
});
```

> This is particularly useful for defining HTTP or RPC endpoints that accept complex payloads that require validation. Moreover, you can define your endpoints once with Zod and share the code with both your client and server code to achieve end-to-end type safety.

```ts
// Express example
server.get(`/user/:id`, async (req, res) => {
  const user = await getUserByID({ id: req.params.id }).catch(err => {
    res.status(400).send(err.message);
  });

  res.status(200).send(user);
});
```

## Transformers

You can integrate custom data transformations into your schemas with transformers. Transformers are just another type of Zod schema.

### z.transformer()

```ts
const countLength = z.transformer(
  z.string(),
  z.number(),
  myString => myString.length,
);

countLength.parse('string'); // => 6
```

This lets you perform coercion, similar to Yup. You still need to provide the coercion logic yourself.

```ts
const coercedString = z.transformer(z.unknown(), z.string(), val => {
  return `${val}`;
});

coercedString.parse(false); // => "false"
coercedString.parse(12); // => "12"
```

Transformations can also be async.

```ts
const IdToUser = z.transformer(
  z.string().uuid(),
  UserSchema,
  userId => async id => {
    return await getUserById(id);
  },
);
```

> ⚠️ If your schema contains asynchronous transformers, you must use .parseAsync() or .safeParseAsync() to parse data. Otherwise Zod will throw an error.

### .transform()

For convenience, ALL Zod schemas (not just transformers) has a `.transform` method. The first argument lets you specify a "destination schema" which defines the type that the data should be transformed _into_.

```ts
const lengthChecker = z.string().transform(z.boolean(), val => {
  return val.length > 5;
});

lengthChecker.parse('asdf'); // => false;
lengthChecker.parse('qwerty'); // => true;
```

You can omit the first argument, in which case Zod assumes you aren't transforming the data type:

```ts
z.string()
  .transform(val => val.replace('pretty', 'extremely'))
  .transform(val => val.toUpperCase())
  .transform(val => val.split(' ').join('👏'))
  .parse('zod 2 is pretty cool');

// => "ZOD👏2👏IS👏EXTREMELY👏COOL"
```

### Default values

Using transformers, Zod lets you supply default values for your schemas.

```ts
const stringWithDefault = z.transformer(
  z.string().optional(),
  z.string(),
  val => val || 'default value',
);
```

Equivalently you can express this using the built-in `.default()` method, available on all Zod schemas.

```ts
z.string().default('default value');
```

### Type inference for transformers

There are special rules surrounding type inference for transformers.

```ts
const stringToNumber = z.transformer(
  z.string(),
  z.number(),
  myString => myString.length,
);

// z.infer<> gives the return type
type type = z.infer<stringToNumber>; // number

// it is equivalent to z.output<>
type out = z.output<stringToNumber>; // number

// you can use z.input<> to get the input type
type in = z.input<stringToNumber>; // string
```

## Errors

There is a dedicated guide on Zod's error handling system here: ERROR_HANDLING.md

## Comparison

There are a handful of other widely-used validation libraries, but all of them have certain design limitations that make for a non-ideal developer experience.

#### Joi

https://github.com/hapijs/joi

Doesn't support static type inference 😕

#### Yup

https://github.com/jquense/yup

Yup is a full-featured library that was implemented first in vanilla JS, with TypeScript typings added later.

Differences

- Supports for casting and transformation
- All object fields are optional by default
- Non-standard `.required()`¹
- Missing object methods: (pick, omit, partial, deepPartial, merge, extend)
- Missing nonempty arrays with proper typing (`[T, ...T[]]`)
- Missing promise schemas
- Missing function schemas
- Missing union & intersection schemas

¹ Yup has a strange interpretation of the word `required`. Instead of meaning "not undefined", Yup uses it to mean "not empty". So `yup.string().required()` will not accept an empty string, and `yup.array(yup.string()).required()` will not accept an empty array. For Zod arrays there is a dedicated `.nonempty()` method to indicate this, or you can implement it with a custom refinement.

#### io-ts

https://github.com/gcanti/io-ts

io-ts is an excellent library by gcanti. The API of io-ts heavily inspired the design of Zod.

In our experience, io-ts prioritizes functional programming purity over developer experience in many cases. This is a valid and admirable design goal, but it makes io-ts particularly hard to integrate into an existing codebase with a more procedural or object-oriented bias. For instance, consider how to define an object with optional properties in io-ts:

```ts
import * as t from 'io-ts';

const A = t.type({
  foo: t.string,
});

const B = t.partial({
  bar: t.number,
});

const C = t.intersection([A, B]);

type C = t.TypeOf<typeof C>;
// returns { foo: string; bar?: number | undefined }
```

You must define the required and optional props in separate object validators, pass the optionals through `t.partial` (which marks all properties as optional), then combine them with `t.intersection`.

Consider the equivalent in Zod:

```ts
const C = z.object({
  foo: z.string(),
  bar: z.string().optional(),
});

type C = z.infer<typeof C>;
// returns { foo: string; bar?: number | undefined }
```

This more declarative API makes schema definitions vastly more concise.

`io-ts` also requires the use of gcanti's functional programming library `fp-ts` to parse results and handle errors. This is another fantastic resource for developers looking to keep their codebase strictly functional. But depending on `fp-ts` necessarily comes with a lot of intellectual overhead; a developer has to be familiar with functional programming concepts and the `fp-ts` nomenclature to use the library.

- Supports codecs with serialization & deserialization transforms
- Supports branded types
- Supports advanced functional programming, higher-kinded types, `fp-ts` compatibility
- Missing object methods: (pick, omit, partial, deepPartial, merge, extend)
- Missing nonempty arrays with proper typing (`[T, ...T[]]`)
- Missing lazy/recursive types
- Missing promise schemas
- Missing function schemas
- Missing union & intersection schemas
- Missing support for parsing cyclical data (maybe)
- Missing error customization

#### Runtypes

https://github.com/pelotom/runtypes

Good type inference support, but limited options for object type masking (no `.pick`, `.omit`, `.extend`, etc.). No support for `Record`s (their `Record` is equivalent to Zod's `object`). They DO support branded and readonly types, which Zod does not.

- Supports "pattern matching": computed properties that distribute over unions
- Supports readonly types
- Missing object methods: (pick, omit, partial, deepPartial, merge, extend)
- Missing nonempty arrays with proper typing (`[T, ...T[]]`)
- Missing lazy/recursive types
- Missing promise schemas
- Missing union & intersection schemas
- Missing error customization
- Missing record schemas (their "record" is equivalent to Zod "object")

#### Ow

https://github.com/sindresorhus/ow

Ow is focused on function input validation. It's a library that makes it easy to express complicated assert statements, but it doesn't let you parse untyped data. They support a much wider variety of types; Zod has a nearly one-to-one mapping with TypeScript's type system, whereas ow lets you validate several highly-specific types out of the box (e.g. `int32Array`, see full list in their README).

If you want to validate function inputs, use function schemas in Zod! It's a much simpler approach that lets you reuse a function type declaration without repeating yourself (namely, copy-pasting a bunch of ow assertions at the beginning of every function). Also Zod lets you validate your return types as well, so you can be sure there won't be any unexpected data passed downstream.

## Changelog

View the changelog at CHANGELOG.md
