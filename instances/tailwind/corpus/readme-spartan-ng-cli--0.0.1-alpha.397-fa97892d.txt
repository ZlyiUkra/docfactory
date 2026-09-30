# @spartan-ng/cli README 0.0.1-alpha.367 … 0.0.1-alpha.397: spartan
# джерело: https://raw.githubusercontent.com/spartan-ng/spartan/26ab53c22c780a2e7f0dabbdac88fa9a45354b59/README.md
# отримано: 2026-09-30
# версія: 0.0.1-alpha.397, 0.0.1-alpha.396, 0.0.1-alpha.395, 0.0.1-alpha.394, 0.0.1-alpha.393, 0.0.1-alpha.392, 0.0.1-alpha.391, 0.0.1-alpha.390, 0.0.1-alpha.389, 0.0.1-alpha.388, 0.0.1-alpha.387, 0.0.1-alpha.386, 0.0.1-alpha.382, 0.0.1-alpha.380, 0.0.1-alpha.379, 0.0.1-alpha.374, 0.0.1-alpha.373, 0.0.1-alpha.372, 0.0.1-alpha.371, 0.0.1-alpha.370, 0.0.1-alpha.368, 0.0.1-alpha.367

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
4. ashley-hunter
5. mihajm
6. ajitzero
7. arturgawlik
8. deepakrudrapaul
9. evanfuture
10. AdditionAddict
11. Altamimi-Dev
12. ferat
13. jeremy-js-devweb
14. heddendorp
15. tutkli
16. Pascalmh
17. okkindel
18. marcjulian
19. oidre
20. nartc
21. santoshyadavdev
22. markostanimirovic
23. theo-matzavinos
24. jkuri
25. dongphuong0905
26. DominikPieper
27. brandonroberts
28. izikd-
29. ryancraigmartin
30. gaetanBloch
31. gergobergo
32. rpacheco124
33. benjaminforras
34. jstnjs
35. r3ps4J
36. Celtian
37. miljan-code
38. alexciesielski
39. ty-ler
40. m-risto
41. badsgahhl
42. monacodelisa
43. tomdev9
44. ragul1697
45. snydertechnologies
46. kkamman
47. i-am-the-slime
48. DevWedeloper
49. mrsofiane
50. mateoetchepare
51. DonaldMurillo
52. toniskobic
53. eneajaho
54. Den-dp
55. 0xfraso
56. Muneersahel
57. danilolmc
58. tomalaforge
59. canserkanuren
60. cjosue15
61. hirenchauhan2
62. Roguyt
63. tsironis13
64. 0xfraso
65. guillermoecharri
66. ValentinFunk
67. Femi236
68. dineshkp
69. robingenz
70. Balastrong
71. OlegSuncrown
72. stewones
73. shinkhouse
74. donaldxdonald
75. BenoitPE
76. MerlinMoos

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
pnpm run storybook
```

At the root of each primitive's folder, e.g. `libs/ui/accordion` you will find a stories file, e.g, `accordion.stories.ts`.

Use these files to add stories and drive development of the primitives.

### Testing

spartan uses Jest for tests. To test all projects locally, run the following command from the root
folder:

```shell
pnpm run test
```

### e2e testing

Cypress e2e testing is set up to run on the storybook. You can run it with:

```
pnpm run e2e
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

- You will need `pnpm` as your package manager.
- You will need to set up a Supabase account (it's free)
- You will need NodeJs installed. The version I have working is `20.17.0`.

#### Development server

Then you can run the following command:

```shell
pnpm nx serve app
```

or

```shell
pnpm run dev
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
