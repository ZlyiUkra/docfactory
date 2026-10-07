# @spartan-ng/cli README 0.0.1-alpha.398 … 0.0.1-alpha.461: spartan
# джерело: https://raw.githubusercontent.com/spartan-ng/spartan/f66748e92d5d6eca91a7ff60a76003e7fd3967b2/README.md
# отримано: 2026-09-30
# версія: 0.0.1-alpha.461, 0.0.1-alpha.460, 0.0.1-alpha.459, 0.0.1-alpha.458, 0.0.1-alpha.457, 0.0.1-alpha.456, 0.0.1-alpha.455, 0.0.1-alpha.454, 0.0.1-alpha.453, 0.0.1-alpha.452, 0.0.1-alpha.451, 0.0.1-alpha.450, 0.0.1-alpha.449, 0.0.1-alpha.448, 0.0.1-alpha.447, 0.0.1-alpha.446, 0.0.1-alpha.445, 0.0.1-alpha.444, 0.0.1-alpha.443, 0.0.1-alpha.442, 0.0.1-alpha.441, 0.0.1-alpha.440, 0.0.1-alpha.439, 0.0.1-alpha.438, 0.0.1-alpha.437, 0.0.1-alpha.436, 0.0.1-alpha.435, 0.0.1-alpha.434, 0.0.1-alpha.433, 0.0.1-alpha.432, 0.0.1-alpha.431, 0.0.1-alpha.430, 0.0.1-alpha.429, 0.0.1-alpha.428, 0.0.1-alpha.427, 0.0.1-alpha.426, 0.0.1-alpha.425, 0.0.1-alpha.424, 0.0.1-alpha.423, 0.0.1-alpha.422, 0.0.1-alpha.421, 0.0.1-alpha.420, 0.0.1-alpha.419, 0.0.1-alpha.418, 0.0.1-alpha.417, 0.0.1-alpha.416, 0.0.1-alpha.415, 0.0.1-alpha.414, 0.0.1-alpha.413, 0.0.1-alpha.412, 0.0.1-alpha.411, 0.0.1-alpha.410, 0.0.1-alpha.409, 0.0.1-alpha.408, 0.0.1-alpha.407, 0.0.1-alpha.406, 0.0.1-alpha.405, 0.0.1-alpha.404, 0.0.1-alpha.403, 0.0.1-alpha.402, 0.0.1-alpha.401, 0.0.1-alpha.400, 0.0.1-alpha.399, 0.0.1-alpha.398

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
77. miljan-code
78. Georg632
79. hillin
80. Besbash
81. davidedammino
82. marcindz88
83. thyco
84. hitro11
85. GODrums
86. samsonkumawong
87. PR4SAN
88. JeevanMahesha

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
