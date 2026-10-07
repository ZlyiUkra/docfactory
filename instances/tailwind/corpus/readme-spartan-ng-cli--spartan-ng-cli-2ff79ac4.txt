# @spartan-ng/cli README 0.0.1-alpha.608 … 0.0.1-alpha.614: spartan
# джерело: https://raw.githubusercontent.com/spartan-ng/spartan/f83a415f25faaf09248aaf5f367ef36c42602ca5/README.md
# отримано: 2026-09-30
# версія: 0.0.1-alpha.614, 0.0.1-alpha.613, 0.0.1-alpha.612, 0.0.1-alpha.611, 0.0.1-alpha.610, 0.0.1-alpha.609, 0.0.1-alpha.608

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
5. zeropsio
6. mihajm
7. ajitzero
8. arturgawlik
9. deepakrudrapaul
10. evanfuture
11. AdditionAddict
12. Altamimi-Dev
13. ferat
14. jeremy-js-devweb
15. heddendorp
16. tutkli
17. Pascalmh
18. okkindel
19. marcjulian
20. oidre
21. nartc
22. santoshyadavdev
23. markostanimirovic
24. theo-matzavinos
25. jkuri
26. dongphuong0905
27. DominikPieper
28. brandonroberts
29. izikd-
30. ryancraigmartin
31. gaetanBloch
32. gergobergo
33. rpacheco124
34. benjaminforras
35. jstnjs
36. r3ps4J
37. Celtian
38. miljan-code
39. alexciesielski
40. ty-ler
41. m-risto
42. badsgahhl
43. monacodelisa
44. tomdev9
45. ragul1697
46. snydertechnologies
47. kkamman
48. i-am-the-slime
49. DevWedeloper
50. mrsofiane
51. mateoetchepare
52. DonaldMurillo
53. toniskobic
54. eneajaho
55. Den-dp
56. 0xfraso
57. Muneersahel
58. danilolmc
59. tomalaforge
60. canserkanuren
61. cjosue15
62. hirenchauhan2
63. Roguyt
64. tsironis13
65. 0xfraso
66. guillermoecharri
67. ValentinFunk
68. Femi236
69. dineshkp
70. robingenz
71. Balastrong
72. OlegSuncrown
73. stewones
74. shinkhouse
75. donaldxdonald
76. BenoitPE
77. MerlinMoos
78. miljan-code
79. Georg632
80. hillin
81. Besbash
82. davidedammino
83. marcindz88
84. thyco
85. hitro11
86. GODrums
87. samsonkumawong
88. PR4SAN
89. JeevanMahesha
90. dlhck
91. tomer953
92. drdreo
93. OlegSuncrown
94. tlandenberger
95. yackinn
96. OmerGronich
97. kubalinio
98. AlexHladin
99. CO97
100. MatanShushan
101. maxhov
102. josueggh
103. namdien177
104. zelenchuk
105. a-malacarne
106. YasinKuralay
107. nico13051995
108. francotalarico
109. koenigderluegner
110. Turtl3e
111. minhnguyen120898
112. liam-langstaff
113. dw-0
114. Khumozin
115. abiramcodes
116. garygrossgarten
117. MatznRisto
118. Oussemasahbeni
119. benpsnyder
120. dhwani1806
121. elite-lucas
122. esteecodes
123. felhag
124. notsufferbutbutter
125. vlrjuan
126. Dafnik
127. hassantayyab
128. mathwizard

Become a spartan today!

## Zerops: The Strategic Alliance

spartan.ng has formed a powerful alliance with Zerops, a developer-first cloud platform that shares our commitment to advancing the Angular ecosystem.

Through their strategic support, Zerops has enabled:

- Dedicated resources for our core development team
- Accelerated component development on our path to v1
- Creation of production-ready templates and starter kits
- Long-term sustainability for the entire project

Zerops eliminates deployment complexity so developers can focus on building great software—a philosophy that perfectly aligns with our mission to create powerful yet easy-to-implement components.

**Experience the cloud platform that's powering Spartan.ng's future →**

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
