# Zod README 1.9.0
# джерело: https://raw.githubusercontent.com/colinhacks/zod/5568a74264726216c0d2a05fc618a2a683ace9e7/README.md
# отримано: 2026-09-28
# версія: 1.9.0

  Zod

if you're happy and you know it, star this repo ⭐

created by @vriad 👋

## Table of contents

- Installation

- Primitives
- Literals
- Parsing
- Type inference
- Custom validation
- Strings
- Numbers
- Objects
  - .shape
  - .merge
  - .extend
  - .pick/.omit
  - .partial/.deepPartial
  - .nonstrict
- Records
- Arrays
  - .nonempty
- Unions
  - .optional
  - .nullable
  - .enum
- Intersections
- Tuples
- Recursive types
  - JSON type
  - Cyclical data
- Promises
- Instanceof
- Function schemas
- Errors
- Comparison
  - Joi
  - Yup
  - io-ts
  - Runtypes
- Changelog

## Installation

To install the latest version:

```sh
npm install --save zod
```

```sh
yarn add zod
```

#### TypeScript requirements

1. Zod 1.x requires TypeScript 3.2+
2. You must configure your project to use TypeScript's **strict mode**. Otherwise Zod can't correctly infer the types of your schemas!
```ts
   // tsconfig.json
   {
     // ...
     "compilerOptions": {
       // ...
       "strict": true
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

`.parse(data:unknown)`

Given any Zod schema, you can call its `.parse` method to check `data` is valid. If it is, a value is returned with full type information! Otherwise, an error is thrown.

> IMPORTANT: As of Zod 1.4, the value returned by `.parse` is _the same variable you passed in_. Previously it returned a deep clone. The only exception to this is `Promise` schemas, which return a new Promise for reasons explained in the documentation.

```ts
const stringSchema = z.string();
stringSchema.parse('fish'); // => returns "fish"
stringSchema.parse(12); // throws Error('Non-string type: number');
```

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

### Custom validation

`.refine(validator: (data:T)=>any, params?: RefineParams)`

Zod was designed to mirror TypeScript as closely as possible. But there are many so-called "refinement types" you may wish to check for that can't be represented in TypeScript's type system. For instance: checking that a number is an Int or that a string is a valid email address.

For this instances, you can define custom a validation check on _any_ Zod schema with `.refine`:

```ts
const myString = z.string().refine(val => val.length <= 255, {
  message: "String can't be more than 255 characters",
});
```

As you can see, `.refine` takes two arguments.

1. The first is the validation function. This function takes one input (of type `T` — the inferred type of the schema) and returns `any`. Any truthy value will pass validation. (Prior to zod@1.6.2 the validation function had to return a boolean.)
2. The second argument is a params object. You can use this to customize certain error-handling behavior:

```ts
   type RefineParams = {
     // override error message
     message?: string;

     // override error path
     path?: (string | number)[];

     // params object you can use to customize message
     // in error map
     params?: object;
   };
```

These params let you define powerful custom behavior. Zod is commonly used for form validation. If you want to verify that "password" and "confirmPassword" match, you can do so like this:

```ts
z.object({
  password: z.string(),
  confirm: z.string(),
})
  .refine(data => data.confirm === data.password, {
    message: "Passwords don't match",
    path: ['confirm'],
  })
  .parse({ password: 'asdf', confirmPassword: 'qwer' });
```

Because you provided a `path` parameter, the resulting error will be:

```ts
ZodError {
  errors: [{
    "code": "custom_error",
    "path": [ "confirm" ],
    "message": "Invalid input."
  }]
}
```

Note that the `path` is set to `["confirm"]`, so you can easily display this error underneath the "Confirm password" textbox.

j

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
  neutered: z.boolean(),
});

type Dog = z.infer<typeof dogSchema>;
/*
equivalent to:
type Dog = {
  name:string;
  neutered: boolean;
}
*/

const cujo = dogSchema.parse({
  name: 'Cujo',
  neutered: true,
}); // passes, returns Dog

const fido: Dog = {
  name: 'Fido',
}; // TypeError: missing required property `neutered`
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

const Teacher = BaseTeacher.merge(HasId);
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

#### Masking

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

By default, Zod object schemas _do not_ allow unknown keys!

```ts
const dogSchema = z.object({
  name: z.string(),
  neutered: z.boolean(),
});

dogSchema.parse({
  name: 'Spot',
  neutered: true,
  color: 'brown',
}); // Error(`Unexpected keys in object: 'color'`)
```

This is an intentional decision to make Zod's behavior consistent with TypeScript. Consider this:

```ts
type Dog = z.infer<typeof dogSchema>;

const spot: Dog = {
  name: 'Spot',
  neutered: true,
  color: 'brown',
};
// TypeError: Object literal may only specify known
// properties, and 'color' does not exist in type Dog
```

TypeScript doesn't allow unknown keys when assigning to an object type, so neither does Zod (by default). If you want to allow this, just call the `.nonstrict()` method on any object schema:

```ts
const dogSchemaNonstrict = dogSchema.nonstrict();

dogSchemaNonstrict.parse({
  name: 'Spot',
  neutered: true,
  color: 'brown',
}); // passes
```

This change is reflected in the inferred type as well:

```ts
type NonstrictDog = z.infer<typeof dogSchemaNonstrict>;
/*
{
  name:string;
  neutered: boolean;
  [k:string]: any;
}
*/
```

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

### Optional types

Unions are the basis for defining optional schemas. An "optional string" is just the union of `string` and `undefined`.

```ts
const A = z.union([z.string(), z.undefined()]);

A.parse(undefined); // => passes, returns undefined
type A = z.infer<typeof A>; // string | undefined
```

Zod provides a shorthand way to make any schema optional:

```ts
const B = z.string().optional(); // equivalent to A

const C = z.object({
  username: z.string().optional(),
});
type C = z.infer<typeof C>; // { username?: string | undefined };
```

### Nullable types

Similarly, you can create nullable types like so:

```ts
const D = z.union([z.string(), z.null()]);
```

Or you can use the shorthand `.nullable()`:

```ts
const E = z.string().nullable(); // equivalent to D
type E = z.infer<typeof D>; // string | null
```

You can create unions of any two or more schemas.

```ts
/* Custom Union Types */

const F = z
  .union([z.string(), z.number(), z.boolean()])
  .optional()
  .nullable();

F.parse('tuna'); // => tuna
F.parse(42); // => 42
F.parse(true); // => true
F.parse(undefined); // => undefined
F.parse(null); // => null
F.parse({}); // => throws Error!

type F = z.infer<typeof F>; // string | number | boolean | undefined | null;
```

### Enums

An enum is just a union of string literals, so you can "build your own enum" like this:

```ts
const FishEnum = z.union([z.literal('Salmon'), z.literal('Tuna'), z.literal('Trout')]);

FishEnum.parse('Salmon'); // => "Salmon"
FishEnum.parse('Flounder'); // => throws
```

But for convenience Zod provides a built-in `z.enum()` function, like so:

```ts
const FishEnum = z.enum(['Salmon', 'Tuna', 'Trout']);
type FishEnum = z.infer<typeof FishEnum>;
// 'Salmon' | 'Tuna' | 'Trout'
```

> You need to pass the literal array directly into z.enum():
>
> ```ts
> const FishEnum = z.enum(['Salmon', 'Tuna', 'Trout']);
> ```
>
> If you define the array as a separate variable, then pass it into z.enum, type inference won't work properly.

#### Autocompletion

You can autocomplete the enum values with the `.enum` property of an enum schema:

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

## Intersections

Intersections are useful for creating "logical AND" types.

```ts
const a = z.union([z.number(), z.string()]);
const b = z.union([z.number(), z.boolean()]);

const c = z.intersection(a, b);
type c = z.infer<typeof C>; // => number

const stringAndNumber = z.intersection(z.string(), z.number());
type Never = z.infer<typeof stringAndNumber>; // => never
```

This is particularly useful for defining "schema mixins" that you can apply to multiple schemas.

```ts
const HasId = z.object({
  id: z.string(),
});

const BaseTeacher = z.object({
  name: z.string(),
});

const Teacher = z.intersection(BaseTeacher, HasId);

type Teacher = z.infer<typeof Teacher>;
// { id:string; name:string };
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

There isn't a built-in method for validating any JSON, because representing that requires recursive type aliases (a feature that TypeScript started supporting with version 3.7). In order to support a wider range of TypeScript versions (see the top of the README for details) we aren't providing a JSON type out of the box at this time. If you want to validate JSON and you're using TypeScript 3.7+, you can use this snippet to achieve that:

```ts
type Literal = boolean | null | number | string;
type Json = Literal | { [key: string]: Json } | Json[];
const literalSchema = z.union([z.string(), z.number(), z.boolean(), z.null()]);
const jsonSchema: z.ZodSchema<Json> = z.lazy(() => z.union([Literal, z.array(Json), z.record(Json)]));

jsonSchema.parse({
  // ...
});
```

Thanks to ggoodman for suggesting this.

#### Cyclical objects

Validation still works as expected even when there are cycles in the data.

```ts
const cyclicalCategory: any = {
  name: 'Category A',
};

// creating a cycle
cyclicalCategory.subcategories = [cyclicalCategory];

const parsedCategory = Category.parse(cyclicalCategory); // parses successfully

parsedCategory.subcategories[0].subcategories[0].subcategories[0];
// => parsedCategory: Category;
```

## Promises

As of zod@1.3, there is also support for Promise schemas!

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

You can create a function schema with `z.function(args, returnType)` which accepts these arguments.

- `args: ZodTuple` The first argument is a tuple (created with `z.tuple([...])` and defines the schema of the arguments to your function. If the function doesn't accept arguments, you can pass an empty tuple (`z.tuple([])`).
- `returnType: any Zod schema` The second argument is the function's return type. This can be any Zod schema.

> You can the special `z.void()` option if your function doesn't return anything. This will let Zod properly infer the type of void-returning functions. (Void-returning function can actually return either undefined or null.)

```ts
const args = z.tuple([z.string()]);

const returnType = z.number();

const myFunction = z.function(args, returnType);
type myFunction = z.infer<typeof myFunction>;
// => (arg0: string)=>number
```

Function schemas have an `.implement()` method which accepts a function as input and returns a new function.

```ts
const myValidatedFunction = myFunction.implement(x => {
  // TypeScript knows x is a string!
  return x.trim().length;
});
```

`myValidatedFunction` now automatically validates both its inputs and return value against the schemas provided to `z.function`. If either is invalid, the function throws.

This way you can confidently write application logic in a "validated function" without worrying about invalid inputs, scattering `schema.validate()` calls in your endpoint definitions,or writing duplicative types for your functions.

Here's a more complex example showing how to write a typesafe API query endpoint:

```ts
const args = z.tuple([
  z.object({ id: z.string() }), // get by ID
]);

const returnType = z.promise(
  z.object({
    id: string(),
    name: string(),
  }),
);

const FetcherEndpoint = z.function(args, returnType);

const getUserByID = FetcherEndpoint.validate(args => {
  args; // => { id: string }

  const user = await User.findByID(args.id);

  // TypeScript statically verifies that value returned by
  // this function is of type Promise<{ id: string; name: string; }>
  return 'salmon'; // TypeError

  return user; // success
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

## Errors

There is a dedicated guide on Zod's error handling system here: ERROR_HANDLING.md

## Comparison

There are a handful of other widely-used validation libraries, but all of them have certain design limitations that make for a non-ideal developer experience.

#### Joi

https://github.com/hapijs/joi

Doesn't support static type inference. Boo. 😕

#### Yup

https://github.com/jquense/yup

Yup is a full-featured library that was implemented first in vanilla JS, with TypeScript typings added later.

Yup supports static type inference! But unfortunately the inferred types aren't actually correct.

##### Incorrect object typing (now fixed!)

This issue was fixed on May 19, 2020 (here).

Currently, the yup package treats all object properties as optional by default:.

```ts
const schema = yup.object({
  asdf: yup.string(),
});
schema.validate({}); // passes
```

Yet the inferred type indicates that all properties are required:

```ts
type SchemaType = yup.InferType<typeof schema>;
// returns { asdf: string }
// should be { asdf?: string }
```

##### Unintuitive `.required()` behavior

In general, Yup's interpretation of `.required()` is odd and non-standard. Instead of meaning "not undefined", Yup uses it to mean "not empty". So `yup.string().required()` will not accept an empty string, and `yup.array(yup.string()).required()` will not accept an empty array. For Zod arrays there is a dedicated `.nonempty()` method to indicate this, or you can implement it with a custom validator.

```ts
const numList = yup
  .array()
  .of(yup.string())
  .required();

// interpreted as a non-empty list
numList.validateSync([]); // fails

// yet the inferred type doesn't reflect this
type NumList = yup.InferType<typeof numList>;
// returns 		string[]
// should be 	[string,...string[]]
```

##### Unions and intersections

Finally, Yup doesn't support any generic `union` or `intersection` operator.

#### io-ts

https://github.com/gcanti/io-ts

io-ts is an excellent library by gcanti. The API of io-ts heavily inspired the design of Zod.

In our experience, io-ts prioritizes functional programming purity over developer experience in many cases. This is a valid and admirable design goal, but it makes io-ts particularly hard to integrate into an existing codebase with a more procedural or object-oriented bias.

For instance, consider how to define an object with optional properties in io-ts:

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

`io-ts` also requires the use of gcanti's functional programming library `fp-ts` to parse results and handle errors. This is another fantastic resource for developers looking to keep their codebase strictly functional. But depending on `fp-ts` necessarily comes with a lot of intellectual overhead; a developer has to be familiar with functional programming concepts, `fp-ts`'s nomenclature, and the `Either` monad to do a simple schema validation. It's just not worth it for many people.

#### Runtypes

https://github.com/pelotom/runtypes

Good type inference support, but limited options for object type masking (no `.pick`, `.omit`, `.extend`, etc.). No support for `Record`s (their `Record` is equivalent to Zod's `object`). They DO support branded and readonly types, which Zod does not.

#### Ow

https://github.com/sindresorhus/ow

Ow is focused on function input validation. It's a library that makes it easy to express complicated assert statements, but it doesn't let you parse untyped data. They support a much wider variety of types; Zod has a nearly one-to-one mapping iwhtwith TypeScript's type system, whereas ow lets you validate several highly-specific types out of the box (e.g. `int32Array`, see full list in their README).

If you want to validate function inputs, use function schemas in Zod! It's a much simpler approach that lets you reuse a function type declaration without repeating yourself (namely, copy-pasting a bunch of ow assertions at the beginning of every function). Also Zod lets you validate your return types as well, so you can be sure there won't be any unexpected data passed downstream.

## Changelog

| zod version | release notes                                                                                                                                                                                              |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| zod@1.9     | Added z.instanceof() and z.custom(). Implemented ZodSchema.array() method.                                                                                                                                 |
| zod@1.8     | Introduced z.void(). Major overhaul to error handling system, including the introduction of custom error maps. Wrote new error handling guide. |
| zod@1.7     | Added several built-in validators to string, number, and array schemas. Calls to `.refine` now return new instance.                                                                                        |
| zod@1.5     | Any and unknown types                                                                                                                                                                                      |
| zod@1.4     | Refinement types (`.refine`), `.parse` no longer returns deep clone                                                                                                                                        |
| zod@1.3     | Promise schemas                                                                                                                                                                                            |
| zod@1.2.6   | `.parse` accepts `unknown`, `bigint` schemas                                                                                                                                                               |
| zod@1.2.5   | `.partial` and `.deepPartial` on object schemas                                                                                                                                                            |
| zod@1.2.3   | Date schemas                                                                                                                                                                                               |
| zod@1.2.0   | `.pick`, `.omit`, and `.extend` on object schemas                                                                                                                                                          |
| zod@1.1.0   | Records                                                                                                                                                                                                    |
| zod@1.0.11  | `.nonstrict`                                                                                                                                                                                               |
| zod@1.0.10  | Type assertions with `.check`                                                                                                                                                                              |
| zod@1.0.4   | Empty tuples                                                                                                                                                                                               |
| zod@1.0.0   | Type assertions, literals, enums, detailed error reporting                                                                                                                                                 |
| zod@1.0.0   | Initial release                                                                                                                                                                                            |
