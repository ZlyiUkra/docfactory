# @spartan-ng/cli README 0.0.1-alpha.358 … 0.0.1-alpha.366: spartan
# джерело: https://raw.githubusercontent.com/spartan-ng/spartan/1c15964f1b8b9b59c00d66e511196ff842ee8d7b/README.md
# отримано: 2026-09-30
# версія: 0.0.1-alpha.366, 0.0.1-alpha.365, 0.0.1-alpha.364, 0.0.1-alpha.363, 0.0.1-alpha.362, 0.0.1-alpha.361, 0.0.1-alpha.360, 0.0.1-alpha.359, 0.0.1-alpha.358

Discord server Twitter

Welcome to the spartan mono-repo. This Nx repository holds both the
spartan/stack and spartan/ui libraries.

##### Important: This is a work in progress, and we update the README as major development efforts are started.

## The 300 spartans

All of spartan is an MIT-licensed open source project with its ongoing development made possible by contributors and sponsors.

Our initial 300 contributors and sponsors are featured here and on the front page of spartan.ng

1. goetzrobin
2. elite-benni
3. thatsamsonkid
4. mihajm
5. ajitzero
6. arturgawlik
7. deepakrudrapaul
8. evanfuture
9. AdditionAddict
10. Altamimi-Dev
11. ferat
12. jeremy-js-devweb
13. heddendorp
14. tutkli
15. Pascalmh
16. okkindel
17. marcjulian
18. oidre
19. nartc
20. santoshyadavdev
21. markostanimirovic
22. theo-matzavinos
23. jkuri
24. dongphuong0905
25. DominikPieper
26. brandonroberts
27. izikd-
28. ryancraigmartin
29. gaetanBloch
30. gergobergo
31. rpacheco124
32. benjaminforras
33. jstnjs
34. r3ps4J
35. Celtian
36. miljan-code
37. alexciesielski
38. ty-ler
39. m-risto
40. badsgahhl
41. monacodelisa
42. tomdev9
43. ragul1697
44. snydertechnologies
45. kkamman
46. i-am-the-slime
47. DevWedeloper
48. mrsofiane
49. mateoetchepare
50. DonaldMurillo
51. toniskobic
52. eneajaho
53. Den-dp
54. 0xfraso
55. Muneersahel
53. danilolmc
54. tomalaforge

Become a spartan today!

## spartan/ui

spartan/ui is our effort to port the incredible shadcn/ui project over to the Angular ecosystem.

The idea is to create un-styled primitives similar to Radix with the help of the Angular CDK and other proven community solutions
And then add the beautiful shadcn styles with primitives (and components where necessary).

You can find all UI primitives in the `libs/ui` folder.

Each primitive is made up off an un-styled `brain` library, which provides all functionality and a `helm` library, which adds the styles.

There's also a `libs/cli` folder, which contains the Nx-plugin & Angular CLI code that allows users to add spartan/ui to their Nx or Angular workspace in a simple way.

### Install Dependencies

Run `pnpm install` to install the dependencies of this project.

### Development with storybook

A storybook project is set up and is the primary way to develop UI components. You can run it with:

```
pnpm storybook
```

At the root of each primitive's folder, e.g. `libs/ui/accordion` you will find a stories file, e.g, `accordion.stories.ts`.

Use these files to add stories and drive development of the primitives.

### Testing

spartan uses Jest for tests. To test all projects locally, run the following command from the root
folder:

```shell
pnpm test
```

### e2e testing

Cypress e2e testing is set up to run on the storybook. You can run it with:

```
pnpm e2e
```

To add your own `e2e` tests add them to the `apps/ui-storybook-e2e` application.

### Progress (37/43)

We finished porting over 37/43 UI primitives. See a more detailed breakdown here!

## spartan/stack

An example application running
on Supabase, Drizzle, Analog,
tRPC, Tailwind, Angular,
and Nx. It also serves as the documentation page introducing the stack and UI library.

Follow the directions in the official documentation to set up your own project:
https://www.spartan.ng/stack/overview

### Example App

In the `apps` folder of this repository, you can also find an example application of the spartan stack.
It also serves as the documentation page for this project.

For now. The goal is to move the docs to Astro.

Follow the directions below to get it up and running:

#### Prerequisites

- You will need `pnpm` (or a different package manager) installed.
- You will need to set up a Supabase account (it's free)
- You will need NodeJs installed. The version I have working is `18.13.0`.

#### Development server

Then you can run the following command:

```shell
pnpm nx serve app
```

or

```shell
pnpm dev
```

for a dev server. Navigate to http://localhost:4200/. The app will automatically reload
if you change any of the source files.

#### Database

We use Drizzle to connect to a Supabase instance for the example app.

Add an `.env` file to your repo with the following contents:

Add a `.env` file at the root of your Nx workspace and add the connection string like so:

```
DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-SUPABASE-REFERENCE-ID].supabase.co:5432/postgres?schema=public"
```

And make sure to run the following script in your Supabase editor to set up the necessary tables:

```sql
create table
  public.note (
    id bigserial,
    title text not null,
    content text null,
    created_at timestamp with time zone null default current_timestamp,
    constraint notes_pkey primary key (id)
  ) tablespace pg_default;
```

> [!NOTE] > `.env` should be added to `.gitignore`

## Understand this workspace

Run `pnpm nx graph` to see a diagram of the dependencies of the projects.

## Further help

Reach out to me on Twitter or GitHub if you run into
any issues.
