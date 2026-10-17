# Creating a new documentation instance · Новий примірник документації · Criando uma nova instância

Three complete versions of the same guide. Pick your language:

- [English](#english)
- [Українська](#українська)
- [Português](#português)

---

<a name="english"></a>

# English

## What you end up with

A protected MCP server that answers questions about one body of documentation, from a local corpus, with four
protection layers. The shared code is never touched: a new domain adds one data folder under `instances/` and, only
if the target site needs it, one new reader under `engine/readers/`.

## Before you start

| Requirement | Why | Optional? |
|-------------|-----|-----------|
| bash (Linux, macOS or WSL on Windows) | `df` calls the Linux `.venv/bin/python`; a native Windows shell cannot run it | no |
| Python 3.10 or newer | the whole engine | no |
| Docker | meaning search (Qdrant); without it the server searches by words only | yes |
| Anthropic API key | only the `ask` step, the project's own agent | yes |

Everything except the first step runs from the repository root `docfactory/` as `./df <instance> <step>`.

## Practices from the instances built so far

What building sixty-odd instances taught. Each line once cost a re-fetch or a wrong answer.

- **Agree the scope before any work.** Sources, in order of trust: the official site, the official repository, the
  package registry. The npm registry is the base for packages, versions (canary included) and migrations. When the
  documentation covers several versions, the default is the most downloaded one; when two are close, answer for
  both.
- **Environment before corpus.** Build the venv and the instance `.env` first; for GitHub sources add a
  `GITHUB_TOKEN` line to that `.env` (the anonymous API allows 60 requests an hour). Do not run `refresh`,
  `vectors`, `smoke` or `quality` before that.
- **Try the reader on several kinds of pages before the full fetch:** an overview, a task page with tabs or
  accordions, a reference page, a changelog entry. Two pages are not a sample: a reader that missed tab panels once
  cost two full re-fetches of a 3 000-page site.
- **Fix readers offline.** Every response is kept in the raw store `raw/` (step 6); after a reader fix run
  `./df <domain> build`, not a new `refresh`.
- **Long runs outlive the terminal.** Start a fetch of hours detached, e.g.
  `setsid nohup ./df <domain> refresh > refresh.log 2>&1 &`. An interrupted run continues with
  `refresh <source where it stopped>` and then `refresh --missing`.
- **Build order:** documents → `vectors` → `smoke` → `quality` → tuning until «as the model» is 10 of 10 →
  `smoke` and `quality` again → README → learning plans and the map `docs/learning-map.md` last.
- **`config.json` keys** (step 2): `slug_rewrite` when a site renamed its files between versions, `families` for
  sources that are editions of one site, `max_per_doc` and `fusion_depth` only by measuring `quality`;
  `answer_hosts` lists every host the documents link to, pages outside the documentation site included. The source
  field `name_prefix` keeps the «overview» and «line-2» documents of several packages in one instance apart.
- **Generated API references** (TypeDoc and the like): the subheadings «Parameters», «Returns», «Default Value»,
  «Inherited from», «Extends» split every member into one-word excerpts and tear a default value away from its
  option. The `sitemap-html` field `inline_titles` turns them into labels inside the member's section. Pages of type
  aliases and variables are genuinely short; `min_chars` keeps them instead of rejecting them as error pages.
- **A site assembled from repository files** (VitePress: `<!--@include-->`, `<<< @/snippets`, `{{…}}` variables from
  `<script setup>` and `package.json`) is read from the tags with the `ghdocs-history` field `vitepress`: the page
  comes out as the site shows it, and its revision counts the inserted files too. Before the full fetch, try the
  reader on a local bare clone of the repository: every tag and file is there offline. Versions released without a
  tag (changesets) are taken from the release commit, its full SHA standing as the key in `tags`.
- **Generated text inside a page does not make a revision.** A Vocs site (`ghdocs-history` field `vocs`) keeps a
  twoslash type cache of several kilobytes in every code block (`// @twoslash-cache: …`), rebuilt with the types: a
  revision hashed from the raw file gives an unchanged page a new document almost every release. Hash the text the
  reader sees, without such lines; the release commit of an untagged version is the `gitHead` field of that version
  in the npm registry.
- **A documentation site without versions** (Foundry Book: one living branch, no tags) gets versions by release day:
  for each stable release, the last commit of the documentation repository before the release was published
  (`git rev-list -1 --before=<published_at> master` in a bare clone); its full SHA is the key in `tags`. Two releases
  on the same commit share one key: `"<sha>": "1.3.4, 1.3.3"`.
- **A site whose generated pages are synced from the code before a release** (biomejs.dev: rule pages, the CLI and
  configuration references arrive as «synchronize to `<code commit>`» commits): a snapshot «before the next release»
  would already carry the next release's rules. The snapshot of a version is the last commit before the first sync
  of a code commit that is not in the release (`git merge-base --is-ancestor <commit> <gitHead of the version>`);
  while the site lived in the code repository, it is the release commit itself.
- **A component whose text lives in its own file** (`<PackageManagerBiomeCommand command="check" />`): the command
  is built from the component file of the same snapshot, and the page revision includes that file — sites change
  such templates (`npx @biomejs/biome` → `npx biome`).
- **Before the full fetch, list what the pages insert.** `git grep` over a bare clone shows every include target and
  its extension: a reader that took only code extensions silently dropped extension-less command output and
  `foundry.toml`, and a second fetch was needed. Recorded terminal output carries ANSI colour codes. After the fetch,
  `grep` the corpus for leftover `[!include` and `{{#include`.
- **A site that moved its folders** (mdBook `src/` → Vocs `vocs/docs/pages` → `src/pages`): derive the
  `slug_rewrite` rules with a script that matches document titles across the periods, then check in
  `index/passages.json` that a section key (`slug` and `section`) is shared only by sources of one family; an old
  edition under a different key takes a result slot from the new one.
- **Release facts that live in JSON, not in docs** (Node.js: the release schedule and the list of every release with
  the bundled npm, V8, OpenSSL): a small reader copies the dates and versions from the official files and draws no
  conclusions of its own; the schedule changes. Without it the instance cannot answer «is X still supported».
- **A changelog next to a docs corpus**: take the release heading and the notable changes, cut the list of commits,
  and label versions of a second product («npm-11.0.0») so the version filter never mixes them with the first.
- **Two numberings in one instance** (Foundry 1.8 and forge-std 1.8): label the second one (`forge-std-1.17.0`, the
  field `version_prefix` for releases) so the version filter never mixes them.
- **A documentation branch that moved to a prerelease** (Drizzle: in December 2025 the site's `main` merged the 1.0
  beta docs and now installs `drizzle-orm@rc`): an instance of stable versions ends its site snapshots at the last
  commit before that merge, later stable releases share that key, and what changed in them comes from the changelogs.
  Look at the install commands of the newest snapshot (`@rc`, `@beta`, `@next`) before trusting it.
- **Tabs whose names live in the container** (Astro MDX: `<Tabs items={['PostgreSQL', 'MySQL']}>` with bare `<Tab>`,
  `<CodeTabs items>` where every code block is a tab): label every tab from `items`, or the examples of all dialects
  merge into one unlabelled run of code. Imported MDX pieces with properties (`<InstallPackages lib='pg'/>`,
  `{props.lib}`) are expanded with the values substituted, inside table cells too (`ghdocs-history` field
  `astro_mdx`). Before the full fetch, run the reader offline over every snapshot of a bare clone and count leftover
  component tags and `{props.`.
- **Tutorials that repeat a step in every tab under its own heading** (four «Push your changes to the database» on one
  page) take every result slot for a command name: `max_per_doc` 1 leaves such a page one slot.
- **A changelog kept as one file per version** (`changelogs/drizzle-kit/0.31.4.md`) starts straight with a section:
  the title comes from the path (`path_title`) and so does the version (`path_version`), labelled per package.
- **An npm packument above the response ceiling** (drizzle-orm with hundreds of branch builds: 65 MB) is fetched
  compressed: field `gzip` of `npm-versions`.
- **A site that moved pages many times** (Prisma: Gatsby, Docusaurus, Fumadocs, each with its own folders): take the
  rename pairs for `slug_rewrite` from the site's own redirects (`static/_redirects`, `vercel.json`), following
  chains to a page alive in the newest snapshot; keep a pair only when the old and new page share the tail of the
  address or the title, and never appear in the same version. Pages renamed without a redirect pair up the same way
  by title and a tail of two address words.
- **A live tree that keeps copies of older versions or previews of the next one** (`orm/v6`, `docs.v6`, `next/`,
  `v8/`): exclude them, or every snapshot would carry old pages under new version numbers. A patch of an older line
  released after the next major (6.19.1 after 7.0.0) shares the last snapshot of its own line.
- **One branch with a folder per version** (Prisma 1: `docs/1.0` … `docs/1.34`): one tag, the version from the folder
  (`path_version`), and a `slug_rewrite` that drops the version folder so identical text of different versions
  merges.
- **A renamed repository** (prisma/prisma → prisma/orm): the GitHub API answers the old name with a redirect, which
  the whitelist refuses; declare the new name.
- **Shared MDX pieces with conditions on properties** (`{props.database && (<ul>…</ul>)}`, `${props.x.toLowerCase()}`
  inside a `<CodeBlock>` template): evaluate the conditions before substituting, or an empty property leaves raw JSX.
- **A reader tried offline on every snapshot** without downloading images: a partial clone
  (`git clone --bare --filter=blob:none`), then the needed blobs in one batch (`git fetch --stdin origin` with their
  SHAs). `git ls-tree -l` asks for blob sizes and fetches every missing blob one by one — leave `-l` out.
- **TypeDoc reference kept as markdown in the repository** (jose `docs/`): the `ghdocs-history-typedoc` reader turns
  member subheadings ("Parameters", "Returns", "Call Signature") into labels inside the section (`inline_titles`)
  and cuts sections that repeat on every page (`drop_titles`: "💗 Help the project", "Defined in" with a code line
  that shifts with every release and keeps member sections from merging across editions).
- **A version number printed on every page** (the Deno import `deno.land/x/jose@v3.20.4/…`) makes every release a new
  edition of every page; `list` shows the count before the download. Such tags go into a source of their own in the
  same `families` entry and are fetched in parallel; identical sections still merge in the passage cache.
- **`ghdocs-history` without `folders` reads `docs/`**: a source meant only for root files (`files`) needs
  `exclude: ["/"]`, or it repeats the documentation of the neighbouring source.
- **A package version published without its README** (next-themes 0.3.0) takes the README from that version's tag as
  a source of its own; a `slug_rewrite` rule gives it the key of the package README, so unchanged sections merge into
  one passage with every version.
- **Versions with neither a tag nor a `gitHead`** (next-themes 0.0.1–0.2.1) take the repository files from the last
  commit of the main branch before the version's publish time in the npm registry (`time`); two versions on one
  commit share a key: `"<sha>": "0.1.0, 0.0.16"`.
- **A package that never left 0.x** needs `version_line_depth: 2`, or every version falls into the one line «0» and
  the version filter cannot tell 0.4 from 0.3.
- **After a new reader, compare headings of the raw file and the written document** for every page (headings outside
  code blocks, from `raw/`): nuqs pages lost whole sections when a lazy match of a `<HumanContent>`/`<LLMContent>`
  pair ran on to the next block, and a sentence starting with the word "import" swallowed a code fence. A count that
  differs points at the page; an empty demo section explains itself.
- **Independent sources fetch in parallel**: one detached `refresh <id>` per long source (the site, a second
  repository) and one for the rest; each process keeps its own pause per host.
- **A platform with dozens of packages, each numbered on its own** (Upstash: `@upstash/redis` 1.39, `qstash` 2.12,
  `vector` 1.2, the Python clients…): every version carries its package name. Tag values «redis-1.39.0» in
  `ghdocs-history` and `ghcode-history`, `version_prefix` in `npm-versions`, `npm-tarball-files`, `pypi-versions`,
  `ghreleases` and `ghreleases-stable`; a monorepo tag `@scope/pkg@x.y.z` becomes «pkg-x.y.z». Otherwise
  `version: "1"` mixes twenty products and the line list says nothing.
- **An empty `readme` field in the npm registry does not mean the tarball has no README** (20 `@upstash` packages,
  `redis` and `qstash` among them). Decide README sources by the count of stable versions, take the file from the
  tarball with `(?i)^readme(\.\w+)?$`, and treat the few «без файла» as the exception.
- **Example folders with the same names in several repositories** (`examples/nextjs` in seven SDKs) share one
  section key: `name_prefix` of `ghexamples` (the repository name). The shared-keys scan also catches a package that
  lives on npm and on PyPI under the same name (`qstash` → `name_prefix` «qstash-py» for PyPI).
- **A product removed from a documentation site** (Upstash Kafka) comes from the commit before the removal:
  `commits?path=<folder>` gives the deleting commit, its parent is the snapshot; the source carries no version.
  Mintlify writes its «Documentation index» block in either case — the reader matches both.
- **Documentation in Snooty rST** (MongoDB: the server manual, mongosh, Database Tools, the drivers) — the
  `snooty-history` reader: `.txt` pages, `include`/`literalinclude`/`sharedinclude` (shared snippets from
  `10gen/docs-shared`), tabs in both notations, YAML steps and extracts of the old branches, `{+x+}` constants from
  `snooty.toml` and `conf.py`, substitutions with nested values, object directives as headings. Hunt the leftovers
  with a census of the corpus (`|x|`, `{+x+}`, `:ref:`, raw spans) and fix the reader down to zero; what remains are
  literal blocks, where the markup really is raw.
- **Do not fetch a huge documentation repository over the network**: a bare clone (`git clone --bare`) and the
  `tools/seed_snooty_store.py --instance <domain> --clone owner/repo=path` tool seeds the raw store with every blob by
  its sha under its raw.githubusercontent.com address (a sha → address map next to the store), only the branches and
  folders declared in `sources.json`; only the branch trees go via the API; then `build` offline (32 thousand pages
  in 12 minutes instead of seven hours). A blob identical across 20 branches is stored once.
- **The tarball of a scoped package** (`@types/mongodb`) is served at an address with a literal "/"
  (`/@types/mongodb/-/…`), not `%2F`: both forms must be in `within`, otherwise every version is "no file".
  DefinitelyTyped, `@nestjs/*` and precompiled packages (`@mongodb-js/zstd`) ship no README in the tarball: take
  `index.d.ts` for types (`kind: types`), drop the other README sources.
- **A site built from the code repository's own `docs/`** (docs.ollama.com from `ollama/ollama` `docs/*.mdx`): the
  site source and the history of the folder give the current page twice under different keys (`faq` and `docs-faq`),
  and it takes two of five result slots. `slug_rewrite` `^docs-` → `` and one `families` entry for both sources fold
  them into one slot; identical texts merge into one passage.
- **Code in Go or Python**: the `outline` field of `ghcode-history` as a list of languages (`["go"]`, `["python"]`)
  splits a file into top-level declarations together with the comment above them (in Python also methods of a class,
  `@overload` variants as one section). `outline: true` keeps its old meaning for the instances already verified.
- **A family of three or more instances**: one overnight chain of heavy steps (vectors one after another, smoke and
  quality after each), the timed reports go on while the chain lives. `ua_query` in `checks.json` is pure Cyrillic (a
  Latin word breaks the check), and the version probe is a line (`"9.11"`), not a full version, when there are hundreds
  of lines.
- **A monorepo whose packages tag their own releases** (js-contrib: 3 396 tags of 78 packages on 145 commits;
  Collector: 7 094 module tags on 195): key `tags` by the full SHA of the release commit, so a tree is fetched once per
  commit, and give every package its own sources with only its own releases, labelled with its name
  (`instrumentation-pg-0.55.0`); otherwise a README carries the versions of its neighbours on the commit. A package
  removed from `main` takes its changelog from the commit of its last release.
- **Code and tests across hundreds of releases**: tens of thousands of file revisions, hours over the network one by
  one. `./df <domain> list` fetches the trees through the API, `tools/seed_git_store.py --clone owner/repo=path` puts
  every blob of a bare clone into the raw store under the address the reader will request, and `build` runs without
  network (35 thousand files in seconds; a `--filter=blob:none` clone fetches only the selected blobs).
- **A Hugo front matter kept in an HTML comment** (`<!--- Hugo front matter … --->` at the top of every OpenTelemetry
  specification file since 2023): the `ghdocs-history` field `lead_comment`, otherwise the file name becomes the title,
  and with `passage_context` it goes into every vector. Look at the first line of the written documents before
  `vectors`.
- **Documents that moved to another repository** (semantic conventions: out of the specification into their own
  repository at 1.21, then `database/` → `db/`): derive `slug_rewrite` from document titles, keep only the pairs that
  never coexist in one version, and put both sources into one `families` entry; then the old edition stops taking the
  first places from the new one.
- **Quality.** The second ten of `quality` («as the model»: queries in the documentation's own names, the way the
  prompt tells the model to write them) is the main goal: 10 of 10. Targets grow only by genuine answers. A target
  must be a section with its own text: a document that is only a header is never found as a section. `ua_query` is
  purely Cyrillic: no digits, no Latin.
- **Archive mode**, when the texts should not stay in the folder (licence, size):
  `tar -czf <archive>.tar.gz -C instances/<domain> corpus raw`; unpack it into a separate folder and compare with
  the disk; only then delete the `.txt` files and `raw/`, compress `index/passages.json` into `passages.json.gz` and
  commit the passport and the cache. Keep one current archive per instance; unpack it back before an update.
- **Cosmetic reader fixes** that barely change the result wait for the instance's next update rather than a fetch
  of their own.
- **Books and pages** are cited as title, author, publisher, year of the newest edition.
- **The instance report** ends with the commands to raise and register the server: `./df <domain> serve` and
  `claude mcp add …` both for WSL and for Windows — Claude Code keeps separate settings in each.
- **A test suite kept as JSON** (JSON-Schema-Test-Suite: an array of groups «schema + instances marked valid or
  invalid» per file): read as code, a file is cut by length in the middle of a schema. The `json-test-suite` reader
  makes every group a section titled by its description. The same group lives in the folder of every draft; a
  `variant_pattern` on the folder prefix folds the copies into one result slot.
- **One specification in several releases** (JSON Schema draft-03 … 2020-12 from the IETF archive): `ietf-text` with
  `version` per source. Editions -00 and -01 of one release share section keys, and their identical sections merge into
  one excerpt carrying both.
- **A badge inside a heading** (VuePress `### unevaluatedProperties <Badge text="NEW: draft 2019-09" />`) becomes a
  line under the heading, not part of it: otherwise the release that added the badge gives the section a new key, and
  editions stop merging. An indented code fence closes together with its list item, as markdown-it does: one stray
  «```» otherwise turned half a page into code.
- **Help written in XML with includes** (LibreOffice `.xhp`: `<embed href="file#id">`, `<embedvar>`): the page is
  assembled with the includes of the same tag, and its edition is computed from fingerprints of the included elements,
  not of whole files. A collection file of menu paths changes with every release; fingerprinting the file would give a
  new edition to hundreds of unchanged pages. Reader `ghdocs-history-xhp`.
- **A repository whose tree GitHub returns truncated** (`LibreOffice/core`, over a hundred thousand files): take the
  tree folder by folder (`git/trees/<tag>:<folder>?recursive=1`, field `roots`), and locally a partial clone of the
  needed tags only: `git fetch --depth=1 --filter=blob:none origin refs/tags/<tag>:refs/tags/<tag>` — 35 MB of trees
  instead of gigabytes; `tools/seed_git_store.py` fetches only the selected blobs.
- **A reader that reads pages while listing** (includes, editions from fingerprints) is not run through `list`: a store
  seeded from a clone has no validators, and `list` would fetch every page over the network again. The tag trees are
  laid down by `seed_git_store.py --trees`, then `build` without network.
- **An API reference generated from IDL** (UNO, from which api.libreoffice.org is built): the file is split into one
  section per member, the description from the comment next to the declaration; split by length, it tore a method's
  description away from its name.
- **MediaWiki pages** are taken through `?action=render`: templates expanded, no menu and no «edit» links; the field
  `start` cuts the navigation at the top of the content.

## Anatomy of an instance

Fourteen files, identical in shape across instances, plus five folders that create themselves.

| Path | What it holds | Who writes it |
|------|---------------|---------------|
| `config.json` | port, collection, embedding model, domain profile | you |
| `sources.json` | where to fetch from, and the whitelist that bounds the fetcher | **you, the main work** |
| `prompts/search.txt` | tool description the model reads before calling search | you |
| `prompts/read.txt` | tool description for reading one excerpt | you |
| `prompts/loaded.txt` | one line saying what is loaded; `{excerpts}`, `{documents}`, `{versions}` are filled in | you |
| `prompts/agent.txt` | system prompt for the project's own agent (`ask`) | you |
| `prompts/refusal.txt` | the text layer 1 returns when it blocks a request | you |
| `checks.json` | queries and expectations for `smoke`, `check`, `raw` and `quality` | you, after the first corpus |
| `requirements.txt` | the instance venv contents | copy, then trim |
| `.env.example` | key placeholder; never commit a real `.env` | copy |
| `.gitignore` | `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `out/`, `index/passages.json` | copy |
| `.mcp.json` | HTTP server record for Claude Code | copy, change the port |
| `README.md` | what this domain is and where its docs come from | you |
| `UPDATE.md` | how to refresh this corpus when upstream changes | you |
| `corpus/` | the downloaded documents plus `index.json`, the passport | `refresh`, `manifest` |
| `index/` | the excerpt cache `passages.json` the server starts from; in archive mode it is committed compressed, `passages.json.gz` | built from `corpus/` by the first step that needs it |
| `raw/` | raw site responses for `build` without network, old versions in `raw/_old/`; never in git | `refresh`, `check`, `list` |
| `out/` | the search-mode decision, logs | `setup`, `serve` |
| `.venv/` | the instance's own virtual environment | step 1 |

## Step 1 · Folder and virtual environment

This is the only step performed from inside the instance folder. You never activate the venv: `df` calls the right
instance's `.venv/bin/python` itself.

```
mkdir -p instances/<domain>/prompts
cp instances/react/requirements.txt instances/react/.gitignore instances/react/.env.example instances/<domain>/
cd instances/<domain>
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cd ../..
```

**Known trap.** On some systems the packaged `python3` ships without the `venv` module. Use a Python that has it,
for example a conda interpreter: `/path/to/miniconda3/bin/python3 -m venv .venv`. Everything afterwards is
unaffected, because the venv is self-contained.

Trim `requirements.txt` to what the domain actually needs. `pypdf` belongs there only if some source is a PDF;
`fastembed` only if you want meaning search.

## Step 2 · `config.json`

```json
{
  "instance": "<domain>",
  "port": 8762,
  "collection": "docs-<domain>",
  "embed_model": "bge-small",
  "pause_sec": 5,
  "server_name": "<domain>-docs",
  "doc_set": "<domain>",
  "sections": "markdown",
  "versions": true,
  "tools": {"search": "search_docs", "read": "read_section"},
  "answer_hosts": ["example.com"],
  "example_label": "<a section name from your corpus>"
}
```

| Field | Meaning | Default if omitted |
|-------|---------|--------------------|
| `instance` | the folder name, for diagnostics | — |
| `port` | HTTP port of this server; integer 1–65535 | — |
| `collection` | Qdrant collection name | — |
| `embed_model` | embedding model key | — |
| `pause_sec` | seconds between requests to the same site while fetching | — |
| `redact` | list of `{"pattern": regex, "with": text}`: matches are replaced in every document before it is written, and `check` compares the same text. For placeholder tokens the documentation shows in the format of a real one: GitHub push protection blocks them | none |
| `server_name` | the name the MCP client shows | `<folder>-docs` |
| `doc_set` | set label in diagnostics and in the Qdrant collection name | `suite` |
| `sections` | `numbered` for documents with section numbers, `markdown` for `## Heading` sites | `numbered` |
| `versions` | whether documents carry a version and search accepts a version filter | `false` |
| `tools` | the two tool names the model sees | `search_spec`, `read_section` |
| `answer_hosts` | hosts whose links layer 4 leaves intact in an answer | empty |
| `example_label` | a word from a section name, used to build the example identifier | — |
| `passage_context` | `true`: vectors and the word index also see the document title and the heading path, not only the excerpt text; for documentation cut into small sections whose text never names its topic. Changing it means rebuilding the vectors | `false` |
| `fusion_depth` | how many places of each search method the fusion of word search and meaning search sees; a section ranked fifth by words and fourth by meaning drops out of a top five fused from five places each. Measured on `quality` before choosing | `k` of the call |
| `revision_suffix` | `true`: the trailing `-<8 hex>` (a revision hash) is cut from a document name before identical excerpts are merged. For a reader that writes one document per revision of a file (`ghdocs-history`): without it, an unchanged section of two revisions stays two excerpts. Excerpt ids keep the full name | `false` |
| `variant_pattern` | a regular expression with one group that names a variant at the start of a document name, e.g. `^docs-(nextjs\|react\|vue)-` for a site that keeps one page per SDK. Variants of the same section take one place in the results instead of several; when the query names a variant, that variant's copy takes the place. Without the field results are exactly as before | none |
| `variant_aliases` | `{variant: [words]}`: how a query names a variant (`"nextjs": ["next.js"]`); without it, the variant name itself with `-` read as a space | none |
| `variant_strict` | `true`: when the query names a variant, pages of other variants that have no copy for it do not enter the results at all (per-framework API references with their own page names). Without it, variants are only collapsed | `false` |
| `title_match` | `true`: a section whose identifier-like name (`Object.freeze`, `SameValue`, `[[Get]]`) the query contains verbatim goes first; plain words from headings do not count. Without it results are exactly as before | `false` |
| `raw_store` | `false` turns off the raw store (step 6) | `true` |
| `max_per_doc` | how many places in the results one family of documents may take (the same page across versions, a package README across revisions). Chosen by measuring `quality` | no limit |
| `slug_rewrite` | list of `[regex, replacement]` pairs applied to the page key: a site that renamed its files between versions gives one page different names, and without a common key its editions do not merge | none |
| `families` | `{"family": ["source id", …]}`: sources that are editions of one site (`tw-v1` … `tw-v4`); the same section of a family takes one place in the results and shows the newest edition. Each source belongs to at most one family | each source alone |
| `version_line_depth` | how many numbers make a version line for the version filter: 1 (`18`) or 2 (`1.35`, a corpus of many tools) | 1 |

**Ports in use:** in each instance's `config.json`; `grep -h '"port"' instances/*/config.json | sort` lists them.
Take the next free one.

## Step 3 · `sources.json`

This is not a step, it is the work. Everything else is mechanical.

Find out how the target site serves its documentation, then decide whether one of the existing readers fits.
The whitelist principle is absolute: the updater fetches only what `sources.json` declares, and nothing else, ever.

```json
{
  "instance": "<domain>",
  "sources": [
    {
      "id": "docs-current",
      "url": "https://example.com/llms.txt",
      "reader": "llms",
      "version": "1.4",
      "within": ["https://example.com/docs/"],
      "title": "Example 1.4 documentation",
      "added": "2026-09-21",
      "note": "Why this source exists and what it covers."
    }
  ]
}
```

**Required fields:** `id`, `url`, `reader`. The URL must be `https`. Duplicate ids are rejected.

**Common optional fields**

| Field | Purpose |
|-------|---------|
| `within` | the only URL prefixes this source may reach; links outside it are skipped, not fetched |
| `version` | version carried into every document of this source; several may be given comma-separated |
| `frozen` | `true` means a snapshot that must never change; `check` reports any drift as an error |
| `title`, `label`, `note`, `added` | human metadata; `note` explains why the source exists |
| `pages` | extra page URLs alive on the site but missing from its menu |
| `index` | extra table-of-contents pages to harvest links from |
| `folders`, `root`, `recursive`, `files` | repository readers: which folders to take, what prefix to strip |
| `before` | blog readers: keep only posts older than this date |
| `keep_links` | keep URLs in the text; for a sitemap page where the links are the content |
| `expand`, `children`, `alt`, `meta` | specification readers: sub-page expansion and alternate titles |

### Basic readers

| Reader | Source shape |
|--------|--------------|
| `toc` | multi-page ecmarkup edition; chapter URLs taken from the table of contents |
| `page` | one ecmarkup page split into top-level sections |
| `pdf` | standards published only as PDF |
| `rfc` | RFC plain text; page furniture and the index are stripped |
| `report` | Unicode report HTML (UAX/UTS) with numbered headings |
| `ldml` | UTS #35 parts where the markup carries no section numbers |
| `llms` | `llms.txt` page list; each page fetched as its `.md` twin |
| `mdblog` | blog index HTML; posts fetched as markdown |
| `mdpage` | a single markdown page |
| `nextdata` | Next.js site with content in `<script id="__NEXT_DATA__">` |
| `gatsby` | Gatsby site serving `page-data.json` next to each page |
| `gatsby-blog` | the blog half of a Gatsby site |
| `ghdocs` | markdown docs as they stood at a repository tag or commit |
| `changelog` | `CHANGELOG.md` split into one document per version |
| `ghreleases` | GitHub release notes through the API |
| `ghcommit` | a single commit: message, author, date, file list |

These sixteen are only the first: as of 12.10.2026 the factory registers 103 readers in 78 modules — sites on
Mintlify, Docusaurus, DevSite and Sphinx, the npm and PyPI registries, repository histories and more.
`grep -h '@register' engine/readers/*.py` lists every name; each module's docstring describes its readers and their
fields.

If none fits, a new reader in `engine/readers/` comes first, before anything else. Readers register themselves, so
no shared file needs editing.

## Step 4 · Check the declaration, no network

```
./df <domain> sources --why
```

Fails loudly on a missing field, a non-https URL, a duplicate id or an unknown reader.

## Step 5 · Dry run

```
./df <domain> list
```

Shows what would be downloaded. Writes nothing. Read this output carefully: it is the cheapest moment to notice that
a reader picks up the wrong pages.

## Step 6 · Fetch the corpus

```
./df <domain> refresh
./df <domain> manifest
```

`refresh` fetches only what is declared. `manifest` writes `corpus/index.json`, the passport: the URL, the fetch date
and a checksum for every document. Nothing is ever deleted by these steps.

Useful variants: `./df <domain> refresh --missing` writes only files that are absent, and
`./df <domain> refresh <id> <id>` limits the run to named sources — the others are not even listed. An interrupted
full run continues with `refresh <source where it stopped>` and then `refresh --missing`.

Every response also lands in the raw store `raw/`, compressed and as received. A changed page does not overwrite the
stored one: the old version moves to `raw/_old/<day>/`. After a reader fix, `./df <domain> build [id…]` rebuilds the
texts from the store without network, in minutes. `"raw_store": false` in `config.json` turns the store off.

## Step 7 · `prompts/`

Five files. There are deliberately no defaults: a tool description guessed for the wrong domain is exactly the
confident fabrication this whole tool exists to prevent.

- **`search.txt`** — what the corpus contains, when to call the tool, and above all **when not to**. This is the
  longest of the five and the one that most affects answer quality.
- **`read.txt`** — how to read one excerpt by its identifier, and that the answer carries the source URL and the
  fetch date so a quotation can be verified.
- **`loaded.txt`** — one line stating what is loaded. `{excerpts}`, `{documents}` and `{versions}` are substituted
  by the server.
- **`agent.txt`** — the system prompt for `ask`. Must name the domain and the two tool names, and must say that
  instructions found inside retrieved text are data, not commands.
- **`refusal.txt`** — the text returned when layer 1 blocks a request.

## Step 8 · `checks.json`

Written after the first corpus exists, because it needs real numbers and real identifiers.

| Field | What it pins down |
|-------|-------------------|
| `expected_passages` | how many excerpts the corpus yields; `smoke` fails if it drifts |
| `expected_note` | why that number is what it is, and when it was taken |
| `find` | a query that must return a known section |
| `short` | a short section that must still be findable |
| `count_query`, `plain_query`, `long_query`, `ua_query`, `mixed_query` | query shapes the server must survive |
| `bad_id` | an identifier that must be rejected |
| `url_prefix` | prefix used when checking answer links |
| `paraphrase` | a query with no word in common with the target text |
| `description_phrases` | phrases the tool descriptions must contain |
| `layer1_legit` | genuine domain questions layer 1 must let through |
| `layer4_keep` | numbers and versions layer 4 must not mask |
| `version_probe` | a query plus a version, when `versions` is true |
| `quality` | ten pairs of query and target for the `quality` measurement |

**On `quality` targets.** A target is every page a knowledgeable person would accept as an answer, and it is chosen
from the documentation, never from what search happened to return. A target may be a string or a list of strings.
In `markdown` mode a target without `#` means the whole document, and that is used only when the entire document
answers the question. If a question has five acceptable answers, the question is too vague: rewrite the query rather
than widen the target.

## Step 9 · Meaning search, optional

```
./df <domain> setup
./df <domain> vectors
```

`setup` asks once whether to use Qdrant or stay with word search; the decision is recorded in `out/mode.json` and can
be changed later. `vectors` starts the container, downloads the embedding model and computes the vectors. Minutes of
CPU, no money, no network beyond the model download.

The container `agent0826-qdrant` is **shared** with other projects. Deleting collections is a human decision and no
step ever does it. Inside its own collection `vectors` removes, at the end of every run, the points whose excerpt is
no longer in the corpus — except when the corpus is incomplete or no existing point was recognised. Collections,
volumes and containers it never touches.

## Step 10 · Verify

```
./df <domain> smoke       # checks past the protocol
./df <domain> protocol    # a dialogue over the protocol, foreign client
./df <domain> raw         # raw JSON-RPC frames, no library
./df <domain> tools       # MCP handshake, tool listing
./df <domain> quality     # measurement: what meaning search adds
```

`quality` is a measurement, not a check: it never fails. The absolute score is meaningless on its own; only the
comparison between the three columns on the same ten queries carries information.

## Step 11 · Serve and connect

```
./df <domain> serve
```

Leave it running in its own terminal. Then, once:

```
claude mcp add --transport http --scope user <server_name> http://127.0.0.1:<port>/mcp
```

In a Claude Code session, `/mcp` must list the server with its two tools.

## Step 12 · Document it

Write the instance `README.md` and `UPDATE.md`, then add the domain to the instance list in the root `README.md`.
`UPDATE.md` matters more than it looks: it is where you record how to take a snapshot before a version bump, and
what must never be deleted.

The instance `README.md` must spell out how to raise this very server — that is the point of the whole instance,
and it is the first thing looked up: the venv, `./df <domain> serve` with its port, both ways of registering it
in Claude Code (`.mcp.json` of this folder, or `claude mcp add --transport http --scope user`), the `/mcp` check,
and what a taken port and a failed connection look like. A domain list in the root README does not replace it.

## Final checklist

```
[ ] .venv built, dependencies installed
[ ] config.json: free port, own collection, profile filled in
[ ] sources.json: every source declared, whitelist bounded by `within`
[ ] ./df <domain> sources --why  passes
[ ] ./df <domain> list           looks right
[ ] reader tried on several kinds of pages before the full fetch
[ ] corpus fetched, manifest written
[ ] prompts/: all five, none carrying another domain's words
[ ] checks.json: real numbers, targets chosen from documentation
[ ] smoke, protocol, raw, tools all green
[ ] quality: «as the model» 10 of 10
[ ] README.md says how to raise the server and register it in Claude Code
[ ] README.md and UPDATE.md written; root README lists the domain
[ ] archive mode: corpus and raw archived, archive verified, texts and raw/ removed
```

---

<a name="українська"></a>

# Українська

## Що виходить у кінці

Захищений MCP-сервер, який відповідає на питання про один корпус документації, з локальних файлів, за чотирма
шарами захисту. Спільний код при цьому не чіпається: новий домен додає одну теку даних в `instances/` і, лише якщо
цього вимагає цільовий сайт, один новий читач в `engine/readers/`.

## Передумови

| Потрібно | Навіщо | Обов'язково? |
|----------|--------|--------------|
| bash (Linux, macOS або WSL на Windows) | `df` кличе лінуксовий `.venv/bin/python`; з нативного Windows-шелу не піде | так |
| Python 3.10 або новіший | увесь рушій | так |
| Docker | пошук за змістом (Qdrant); без нього сервер шукає лише по словах | ні |
| Ключ Anthropic | лише крок `ask`, власний агент проєкту | ні |

Усе, крім першого кроку, біжить із кореня `docfactory/` через `./df <примірник> <крок>`.

## Практики зібраних примірників

Чого навчило збирання шістдесяти з гаком примірників. Кожен рядок колись коштував перекачування або хибної відповіді.

- **Обсяг погоджують до роботи.** Джерела за довірою: офіційний сайт, офіційний репозиторій, реєстр пакетів. Реєстр
  npm — база пакетів, версій (з canary) і переходів між ними. Коли документація охоплює кілька версій, версія за
  замовчуванням — найпопулярніша за завантаженнями; якщо дві близькі — відповідь для обох.
- **Спершу середовище, потім корпус.** Першими — venv і `.env` примірника; для джерел GitHub у цей `.env` дописують
  рядок `GITHUB_TOKEN` (анонімний API дає 60 звернень на годину). До того `refresh`, `vectors`, `smoke` і `quality`
  не запускають.
- **Читача пробують на кількох типах сторінок до повного завантаження:** огляд, завдання з вкладками чи гармошками,
  довідник, запис журналу змін. Дві сторінки — не вибірка: читач, що не бачив панелей вкладок, якось коштував двох
  повних перекачувань сайту на 3 000 сторінок.
- **Читача правлять без мережі.** Кожна відповідь лежить у сховищі сирого `raw/` (крок 6); після правки читача —
  `./df <домен> build`, а не новий `refresh`.
- **Довгий прогін переживає термінал.** Завантаження на години запускають відокремлено, напр.
  `setsid nohup ./df <домен> refresh > refresh.log 2>&1 &`. Перерваний прогін продовжують командою
  `refresh <джерело, де зупинився>`, а потім `refresh --missing`.
- **Порядок збирання:** документи → `vectors` → `smoke` → `quality` → дотюнінг, доки «як модель» не дасть 10 із 10 →
  знову `smoke` і `quality` → README → плани навчання й карта `docs/learning-map.md` останніми.
- **Ключі `config.json`** (крок 2): `slug_rewrite` — коли сайт між версіями переклав файли, `families` — для джерел,
  що є редакціями одного сайту, `max_per_doc` і `fusion_depth` — лише за заміром `quality`; `answer_hosts`
  перелічує всі хости, на які посилаються документи, зокрема сторінки поза сайтом документації. Поле джерела
  `name_prefix` розводить документи «overview» і «line-2» кількох пакетів одного примірника.
- **Згенерований довідник API** (TypeDoc тощо): підзаголовки «Parameters», «Returns», «Default Value», «Inherited
  from», «Extends» ділять кожен член на фрагменти з одного слова й відривають значення за замовчуванням від опції.
  Поле `inline_titles` читача `sitemap-html` робить з них підписи всередині розділу члена. Сторінки псевдонімів
  типів і змінних справді короткі; `min_chars` лишає їх, а не відкидає як сторінки помилки.
- **Сайт, зібраний із файлів репозиторію** (VitePress: `<!--@include-->`, `<<< @/snippets`, змінні `{{…}}` з
  `<script setup>` і `package.json`), береться з тегів полем `vitepress` читача `ghdocs-history`: сторінка виходить
  такою, як на сайті, а її редакція враховує й вставлені файли. До повного завантаження читача пробують на локальному
  голому клоні репозиторію: усі теги й файли там без мережі. Версії, випущені без тегу (changesets), беруться з коміту
  випуску — його повний SHA стає ключем у `tags`.
- **Згенерований текст усередині сторінки — не нова редакція.** Сайт на Vocs (поле `vocs` читача `ghdocs-history`)
  тримає в кожному блоці коду кеш типів twoslash на кілька кілобайтів (`// @twoslash-cache: …`), який перебудовується
  разом із типами: відбиток із сирого файла давав би незмінній сторінці новий документ ледь не з кожним випуском.
  Відбиток рахують із тексту, який бачить читач, без таких рядків; коміт випуску версії без тегу — поле `gitHead`
  цієї версії в реєстрі npm.
- **Сайт документації без версій** (Foundry Book: одна жива гілка без тегів) дістає версії за днем виходу: для
  кожного стабільного релізу — останній коміт репозиторію документації перед публікацією релізу
  (`git rev-list -1 --before=<published_at> master` у голому клоні); його повний SHA стає ключем у `tags`. Два релізи
  на тому самому коміті ділять один ключ: `"<sha>": "1.3.4, 1.3.3"`.
- **Сайт, чиї згенеровані сторінки синхронізуються з кодом ще до релізу** (biomejs.dev: сторінки правил, довідники
  CLI й конфігурації приходять комітами «synchronize to `<коміт коду>`»): знімок «перед наступною версією» ніс би вже
  правила наступної. Знімок версії — останній коміт перед першою синхронізацією коміту коду, якого в релізі немає
  (`git merge-base --is-ancestor <коміт> <gitHead версії>`); поки сайт жив у репозиторії коду, — сам коміт релізу.
- **Компонент, чий текст лежить у його власному файлі** (`<PackageManagerBiomeCommand command="check" />`): команду
  будують за файлом компонента того самого знімка, і редакція сторінки враховує цей файл — такі шаблони сайти міняють
  (`npx @biomejs/biome` → `npx biome`).
- **До повного завантаження — перелік того, що вставляють сторінки.** `git grep` по голому клону показує кожну ціль
  вставки і її розширення: читач, що брав лише розширення коду, мовчки губив записаний вивід команд без розширення й
  `foundry.toml`, і знадобилося друге завантаження. Записаний вивід терміналу несе кольори ANSI. Після завантаження
  корпус перевіряють `grep`-ом на залишки `[!include` і `{{#include`.
- **Сайт, що переїжджав між теками** (mdBook `src/` → Vocs `vocs/docs/pages` → `src/pages`): правила `slug_rewrite`
  виводять скриптом, що зіставляє назви документів різних періодів, і перевіряють в `index/passages.json`, що ключ
  розділу (`slug` і `section`) спільний лише для джерел однієї родини; стара редакція під іншим ключем забирає у
  видачі місце нової.
- **Факти про релізи, що лежать у JSON, а не в документації** (Node.js: розклад і перелік усіх релізів з версіями npm,
  V8, OpenSSL): малий читач переписує дати й версії з офіційних файлів і не робить власних висновків; розклад
  змінюється. Без нього примірник не відповість, чи ще підтримується версія.
- **Журнал змін поруч із документацією**: беруть заголовок релізу й Notable Changes, перелік комітів відрізають, а
  версії другого продукту позначають («npm-11.0.0»), щоб фільтр версій не змішував їх із першим.
- **Дві нумерації в одному примірнику** (Foundry 1.8 і forge-std 1.8): другу позначають міткою (`forge-std-1.17.0`,
  для релізів — поле `version_prefix`), щоб фільтр версії їх не змішував.
- **Гілка документації, що перейшла на передреліз** (Drizzle: у грудні 2025 у `main` сайту злили документацію бети
  1.0, і тепер вона ставить `drizzle-orm@rc`): примірник стабільних версій закінчує знімки сайту останнім комітом
  перед тим злиттям, пізніші стабільні версії ділять його ключ, а що в них змінилося, дають журнали змін. Перш ніж
  довіряти найновішому знімку, дивляться на його команди встановлення (`@rc`, `@beta`, `@next`).
- **Вкладки, чиї назви лежать у контейнері** (MDX для Astro: `<Tabs items={['PostgreSQL', 'MySQL']}>` з голими
  `<Tab>`, `<CodeTabs items>`, де вкладка — кожен блок коду): кожну вкладку підписують з `items`, інакше приклади всіх
  діалектів злипаються в один код без підписів. Імпортовані шматки MDX із властивостями (`<InstallPackages
  lib='pg'/>`, `{props.lib}`) розкриваються з підставленими значеннями, і в клітинках таблиць теж (поле `astro_mdx`
  читача `ghdocs-history`). До повного завантаження читач проганяють без мережі по всіх знімках голого клону й рахують
  залишки тегів компонентів і `{props.`.
- **Посібники, що повторюють крок у кожній вкладці власним заголовком** (чотири «Push your changes to the database» на
  одній сторінці), забирають усі місця видачі на назву команди: `max_per_doc` 1 лишає такій сторінці одне місце.
- **Журнал змін файлом на версію** (`changelogs/drizzle-kit/0.31.4.md`) починається одразу з розділу: назву дає шлях
  (`path_title`), версію теж (`path_version`), з міткою пакета.
- **Опис пакета npm понад стелю відповіді** (drizzle-orm із сотнями збірок гілок — 65 МБ) тягнуть стиснутим: поле
  `gzip` читача `npm-versions`.
- **Сайт, що багато разів переносив сторінки** (Prisma: Gatsby, Docusaurus, Fumadocs, кожен зі своїми теками): пари
  перейменувань для `slug_rewrite` беруть з перенаправлень самого сайту (`static/_redirects`, `vercel.json`), ідучи
  ланцюжком до сторінки, живої в найновішому знімку; пару лишають, лише коли стара й нова сторінка мають спільний
  кінець адреси чи назву і ніколи не стоять в одній версії. Сторінки, перейменовані без перенаправлення, зводять так
  само — за назвою і двома спільними словами кінця адреси.
- **Жива гілка тримає копії старих версій чи передрелізи наступної** (`orm/v6`, `docs.v6`, `next/`, `v8/`): їх
  виключають, інакше кожен знімок ніс би старі сторінки під новими номерами. Латка старшої лінії, що вийшла після
  нового мажора (6.19.1 після 7.0.0), ділить останній знімок своєї лінії.
- **Одна гілка з текою на кожну версію** (Prisma 1: `docs/1.0` … `docs/1.34`): один тег, версія з теки
  (`path_version`) і правило `slug_rewrite`, що знімає теку версії, — тоді однаковий текст різних версій зливається.
- **Перейменований репозиторій** (prisma/prisma → prisma/orm): на старе ім'я API GitHub відповідає перенаправленням,
  якого білий список не пропускає; в оголошенні — нове ім'я.
- **Спільні шматки MDX з умовами на властивості** (`{props.database && (<ul>…</ul>)}`, `${props.x.toLowerCase()}` у
  шаблоні `<CodeBlock>`): умови зважують до підстановки, інакше порожня властивість лишає сирий JSX.
- **Читача проганяють без мережі по всіх знімках**, не тягнучи картинок: частковий клон (`git clone --bare
  --filter=blob:none`), далі потрібні blob одним пакетом (`git fetch --stdin origin` з їхніми SHA). `git ls-tree -l`
  питає розмір blob і тягне кожен відсутній поодинці — без `-l`.
- **Довідник TypeDoc, що лежить markdown-ом у репозиторії** (тека `docs/` jose): читач `ghdocs-history-typedoc` робить
  підзаголовки членів («Parameters», «Returns», «Call Signature») підписами всередині розділу (`inline_titles`) і
  вирізає розділи, однакові на кожній сторінці (`drop_titles`: «💗 Help the project», «Defined in» з рядком коду, що
  зсувається з кожним релізом і не дає розділам членів злитися між редакціями).
- **Номер версії на кожній сторінці** (імпорт для Deno `deno.land/x/jose@v3.20.4/…`) робить кожен реліз новою
  редакцією кожної сторінки; `list` показує це число до завантаження. Такі теги виносять окремим джерелом у той самий
  запис `families` і тягнуть паралельно; однакові розділи все одно зливаються в кеші фрагментів.
- **`ghdocs-history` без `folders` бере теку `docs/`**: джерелу лише кореневих файлів (`files`) потрібне
  `exclude: ["/"]`, інакше воно повторює документацію сусіднього джерела.
- **Версія пакета, опублікована без README** (next-themes 0.3.0), бере README з тегу цієї версії окремим джерелом;
  правило `slug_rewrite` дає йому ключ README пакета, і незмінні розділи зливаються в один фрагмент з усіма версіями.
- **Версії без тегу й без `gitHead`** (next-themes 0.0.1–0.2.1) беруть файли репозиторію з останнього коміту головної
  гілки перед публікацією версії в реєстрі npm (`time`); дві версії на одному коміті ділять ключ:
  `"<sha>": "0.1.0, 0.0.16"`.
- **Пакет, що ніколи не виходив з 0.x**, потребує `version_line_depth: 2`, інакше всі версії падають в одну лінію «0»
  і фільтр версії не відрізнить 0.4 від 0.3.
- **Після нового читача — звірка заголовків сирого файла й записаного документа** для кожної сторінки (заголовки поза
  блоками коду, з `raw/`): сторінки nuqs губили цілі розділи, коли лінивий збіг пари `<HumanContent>`/`<LLMContent>`
  тягнувся до наступного блоку, а речення, що починалося словом «import», ковтало огорожу коду. Розбіжність числа
  вказує на сторінку; порожній розділ демо пояснює себе сам.
- **Незалежні джерела тягнуть паралельно**: окремий відокремлений `refresh <id>` на кожне довге джерело (сайт, другий
  репозиторій) і один на решту; пауза між зверненнями до хоста — у кожного процесу своя.
- **Платформа з десятками пакетів, кожен зі своєю нумерацією** (Upstash: `@upstash/redis` 1.39, `qstash` 2.12,
  `vector` 1.2, клієнти Python…): кожна версія несе назву пакета. Значення тегів «redis-1.39.0» у `ghdocs-history`
  і `ghcode-history`, поле `version_prefix` у `npm-versions`, `npm-tarball-files`, `pypi-versions`, `ghreleases` і
  `ghreleases-stable`; тег монорепозиторію `@scope/pkg@x.y.z` стає «pkg-x.y.z». Інакше `version: "1"` змішує
  двадцять продуктів, а перелік ліній нічого не каже.
- **Порожнє поле `readme` в реєстрі npm не означає, що README немає в tarball** (20 пакетів `@upstash`, серед них
  `redis` і `qstash`). Джерела README вирішують за числом стабільних версій, файл беруть із tarball за
  `(?i)^readme(\.\w+)?$`, а кілька «без файла» — виняток.
- **Теки прикладів з однаковими назвами в кількох репозиторіях** (`examples/nextjs` у семи SDK) ділять один ключ
  розділу: `name_prefix` читача `ghexamples` (назва репозиторію). Скан спільних ключів ловить і пакет, що живе на npm
  і на PyPI під одним іменем (`qstash` → `name_prefix` «qstash-py» для PyPI).
- **Продукт, прибраний із сайту документації** (Upstash Kafka), беруть із коміту перед видаленням:
  `commits?path=<тека>` дає коміт видалення, його батько — знімок; версії джерело не несе. Блок «Documentation index»
  Mintlify пише і з великої, і з малої літери — читач упізнає обидва.
- **Документація у форматі Snooty rST** (MongoDB: посібник сервера, mongosh, Database Tools, драйвери) — читач
  `snooty-history`: сторінки `.txt`, `include`/`literalinclude`/`sharedinclude` (спільні вставки з
  `10gen/docs-shared`), вкладки обох записів, YAML-кроки й витяги старих гілок, константи `{+x+}` із `snooty.toml` і
  `conf.py`, підстановки з вкладеними значеннями, об'єктні директиви заголовками. Залишки шукати переписом корпусу (`|x|`, `{+x+}`, `:ref:`,
  сирі спани) і правити читач до нуля; що лишається — літеральні блоки, де розмітка справді сира.
- **Великий репозиторій документації не тягти мережею**: голий клон (`git clone --bare`) і засів сховища сирого
  інструментом `tools/seed_snooty_store.py --instance <домен> --clone owner/repo=шлях` — кожен blob за його sha під
  адресою raw.githubusercontent.com (мапа sha → адреса поруч зі сховищем), лише гілки й теки з `sources.json`;
  мережею — лише дерева гілок через API; далі `build` без мережі (32 тисячі сторінок за 12 хвилин замість семи
  годин). Blob, однаковий у 20 гілках, лежить один раз.
- **Tarball пакета з областю** (`@types/mongodb`) реєстр віддає за адресою з літеральною «/» (`/@types/mongodb/-/…`),
  а не з `%2F`: обидві форми мають бути у `within`, інакше всі версії «без файла». Пакети DefinitelyTyped, `@nestjs/*`
  і прекомпільовані (`@mongodb-js/zstd`) README у tarball не кладуть: для типів брати `index.d.ts` (`kind: types`),
  решту джерел README прибрати.
- **Сайт, зібраний із теки `docs/` самого репозиторію коду** (docs.ollama.com з `docs/*.mdx` `ollama/ollama`):
  джерело сайту й історія теки дають чинну сторінку двічі під різними ключами (`faq` і `docs-faq`), і вона забирає два
  місця з п'яти. `slug_rewrite` `^docs-` → `` і один запис `families` для обох джерел згортають їх в одне місце;
  однакові тексти зливаються в один фрагмент.
- **Код Go чи Python**: поле `outline` читача `ghcode-history` переліком мов (`["go"]`, `["python"]`) ділить файл за
  оголошеннями верхнього рівня разом з коментарем над ними (у Python — і методи класу, варіанти `@overload` — одним
  розділом). `outline: true` лишається з колишнім змістом для вже звірених примірників.
- **Родина з трьох і більше примірників**: один ланцюжок важких кроків на ніч (вектори по черзі, за кожними — smoke і
  quality), звіти за таймером тривають, поки ланцюжок живий. `ua_query` у `checks.json` — суто кирилицею (латинське
  слово ламає перевірку), а пробна версія — лінія (`"9.11"`), не повна версія, коли ліній понад сотню.
- **Монорепозиторій, де пакети тегують власні випуски** (js-contrib: 3 396 тегів 78 пакетів на 145 комітах;
  Collector: 7 094 теги модулів на 195): ключ у `tags` — повний SHA коміту випуску, тож дерево тягнеться раз на коміт,
  а кожен пакет — окремими джерелами лише зі своїми випусками й міткою зі своєю назвою (`instrumentation-pg-0.55.0`);
  інакше README дістає версії сусідів по коміту. Знятий з `main` пакет бере журнал змін із коміту свого останнього
  випуску.
- **Код і тести сотень випусків**: десятки тисяч редакцій файлів, мережею по одному — години. `./df <домен> list` бере
  дерева через API, `tools/seed_git_store.py --clone власник/репо=шлях` кладе кожен blob голого клона у сховище сирого
  під тією адресою, яку попросить читач, і `build` іде без мережі (35 тисяч файлів за секунди; клон
  `--filter=blob:none` докачує лише відібрані blob-и).
- **Шапка Hugo в коментарі HTML** («`<!--- Hugo front matter … --->`» нагорі кожного файла специфікацій
  OpenTelemetry з 2023 року): поле `lead_comment` читача `ghdocs-history`, інакше назвою стає ім'я файла, а з
  `passage_context` воно ще й іде в кожен вектор. Перед `vectors` подивіться на перший рядок записаних документів.
- **Документи, що переїхали в інший репозиторій** (семантичні домовленості: зі специфікації у власний репозиторій на
  1.21, потім `database/` → `db/`): `slug_rewrite` виводити з назв документів, лишати лише пари, що ніколи не
  співіснували в одній версії, і обидва джерела — в один запис `families`; тоді стара редакція перестає забирати перші
  місця в нової.
- **Якість.** Друга десятка `quality` («як модель»: запити назвами самої документації, як велить писати промпт) —
  головна мета: 10 із 10. Цілі доповнюють лише справжніми відповідями. Ціль мусить бути розділом із власним текстом:
  документ із самої шапки розділом не знаходиться. `ua_query` — суто кирилицею, без цифр і латиниці.
- **Архівний режим** — коли текстам не місце в теці (ліцензія, розмір):
  `tar -czf <архів>.tar.gz -C instances/<домен> corpus raw`; розпакувати в окрему теку й звірити з диском; лише
  тоді видалити файли `.txt` і `raw/`, стиснути `index/passages.json` у `passages.json.gz` і закомітити паспорт і
  кеш. Чинний архів у примірника один; перед оновленням його розпаковують назад.
- **Косметичні правки читача**, що майже не міняють результат, чекають наступного оновлення примірника, а не
  окремого перекачування.
- **Книжки й сторінки** цитують як назву, автора, видавництво й рік найновішого видання.
- **Звіт про примірник** закінчується командами підняти й записати сервер: `./df <домен> serve` і `claude mcp add …`
  і для WSL, і для Windows — Claude Code тримає там окремі налаштування.
- **Набір тестів у JSON** (JSON-Schema-Test-Suite: у файлі — масив груп «схема + екземпляри з позначкою valid чи
  invalid»): узятий кодом, файл ріжеться за довжиною посеред схеми. Читач `json-test-suite` робить кожну групу
  розділом з описом-заголовком. Та сама група лежить у теці кожного випуску; `variant_pattern` за префіксом теки
  згортає копії в одне місце видачі.
- **Одна специфікація в кількох випусках** (JSON Schema draft-03 … 2020-12 з архіву IETF): `ietf-text` з полем
  `version` на кожне джерело. Видання -00 і -01 одного випуску мають спільні ключі розділів, і однакові розділи
  зливаються в один фрагмент з обома виданнями.
- **Позначка в заголовку** (VuePress `### unevaluatedProperties <Badge text="NEW: draft 2019-09" />`) стає рядком під
  заголовком, а не його частиною: інакше випуск, що додав позначку, дає розділу новий ключ, і редакції перестають
  зливатися. Огорожа коду з відступом закривається разом із пунктом списку, як у markdown-it: один зайвий «```»
  інакше робив кодом пів сторінки.
- **Довідка в XML зі вставками** (LibreOffice `.xhp`: `<embed href="файл#id">`, `<embedvar>`): сторінку збирають зі
  вставками того самого тегу, а її редакцію рахують з відбитків вставлених елементів, не цілих файлів. Файл-збірник
  рядків меню міняється з кожним випуском, і відбиток файла давав би нову редакцію сотням незмінних сторінок. Читач
  `ghdocs-history-xhp`.
- **Репозиторій, чиє дерево GitHub віддає обрізаним** (`LibreOffice/core`, понад сто тисяч файлів): дерево беруть
  потеково (`git/trees/<тег>:<тека>?recursive=1`, поле `roots`), а локально — частковий клон лише потрібних тегів:
  `git fetch --depth=1 --filter=blob:none origin refs/tags/<тег>:refs/tags/<тег>` — 35 МБ дерев замість гігабайтів;
  `tools/seed_git_store.py` докачує лише відібрані blob-и.
- **Читач, що читає сторінки вже під час переліку** (вставки, редакції з відбитків), не проганяють через `list`:
  сховище, засіяне з клону, не має валідаторів, і `list` тягнув би кожну сторінку мережею вдруге. Дерева тегів кладе
  `seed_git_store.py --trees`, далі — `build` без мережі.
- **Довідник API, згенерований з IDL** (UNO, з якого збирають api.libreoffice.org): файл ділиться на розділ на член,
  опис з коментаря — поруч з оголошенням; поділений за довжиною, він відривав опис методу від його імені.
- **Вікі MediaWiki** беруть через `?action=render`: шаблони розгорнуто, меню й посилань «edit» немає; навігацію
  нагорі змісту відрізає поле `start`.

## З чого складається примірник

Чотирнадцять файлів, однакових за складом у всіх примірниках, плюс п'ять тек, що створюються самі.

| Шлях | Що тримає | Хто пише |
|------|-----------|----------|
| `config.json` | порт, колекція, модель векторів, профіль домену | ви |
| `sources.json` | звідки тягнути, і водночас білий список для оновлювача | **ви, головна робота** |
| `prompts/search.txt` | опис інструмента пошуку, який читає модель | ви |
| `prompts/read.txt` | опис інструмента читання одного фрагмента | ви |
| `prompts/loaded.txt` | рядок про те, що завантажено; `{excerpts}`, `{documents}`, `{versions}` підставляє сервер | ви |
| `prompts/agent.txt` | системний промпт власного агента (`ask`) | ви |
| `prompts/refusal.txt` | текст, який шар 1 повертає, коли блокує запит | ви |
| `checks.json` | запити й очікування для `smoke`, `check`, `raw` і `quality` | ви, після першого корпусу |
| `requirements.txt` | склад venv примірника | копія, потім підрізати |
| `.env.example` | заготовка для ключа; справжній `.env` у git не потрапляє ніколи | копія |
| `.gitignore` | `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `out/`, `index/passages.json` | копія |
| `.mcp.json` | запис HTTP-сервера для Claude Code | копія, змінити порт |
| `README.md` | що це за домен і звідки береться його документація | ви |
| `UPDATE.md` | як оновлювати корпус, коли нагорі щось змінилося | ви |
| `corpus/` | завантажені документи плюс `index.json`, паспорт | `refresh`, `manifest` |
| `index/` | кеш фрагментів `passages.json`, з якого підіймається сервер; в архівному режимі в git іде стисненим, `passages.json.gz` | будується з `corpus/` першим кроком, якому потрібен |
| `raw/` | сирі відповіді сайтів для `build` без мережі, старі версії — у `raw/_old/`; у git не йде ніколи | `refresh`, `check`, `list` |
| `out/` | рішення про спосіб пошуку, журнали | `setup`, `serve` |
| `.venv/` | власне віртуальне середовище примірника | крок 1 |

## Крок 1 · Тека і venv

Це єдиний крок, що робиться зсередини теки примірника. Venv активувати не треба ніколи: `df` сам викликає
`.venv/bin/python` потрібного примірника.

```
mkdir -p instances/<домен>/prompts
cp instances/react/requirements.txt instances/react/.gitignore instances/react/.env.example instances/<домен>/
cd instances/<домен>
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cd ../..
```

**Відома пастка.** На деяких системах пакетний `python3` іде без модуля `venv`. Тоді беріть інтерпретатор, у якого
він є, наприклад conda: `/шлях/до/miniconda3/bin/python3 -m venv .venv`. На все подальше це не впливає, бо venv
самодостатній.

`requirements.txt` підріжте під домен. `pypdf` потрібен, лише якщо якесь джерело видається PDF-ом; `fastembed` —
лише якщо потрібен пошук за змістом.

## Крок 2 · `config.json`

```json
{
  "instance": "<домен>",
  "port": 8762,
  "collection": "docs-<домен>",
  "embed_model": "bge-small",
  "pause_sec": 5,
  "server_name": "<домен>-docs",
  "doc_set": "<домен>",
  "sections": "markdown",
  "versions": true,
  "tools": {"search": "search_docs", "read": "read_section"},
  "answer_hosts": ["example.com"],
  "example_label": "<слово з назви розділу вашого корпусу>"
}
```

| Поле | Що означає | Змовчання |
|------|------------|-----------|
| `instance` | ім'я теки, для діагностики | — |
| `port` | HTTP-порт цього сервера; ціле 1–65535 | — |
| `collection` | ім'я колекції Qdrant | — |
| `embed_model` | ключ моделі векторів | — |
| `pause_sec` | пауза в секундах між зверненнями до того самого сайту | — |
| `redact` | перелік `{"pattern": вираз, "with": текст}`: збіги замінюються в кожному документі перед записом, а `check` порівнює той самий текст. Для заглушок токенів, які документація показує у форматі справжнього: GitHub блокує їхній push | немає |
| `server_name` | ім'я, яке бачить MCP-клієнт | `<тека>-docs` |
| `doc_set` | мітка набору в діагностиці й в імені колекції | `suite` |
| `sections` | `numbered` для документів із номерами розділів, `markdown` для сайтів із `## Заголовок` | `numbered` |
| `versions` | чи несуть документи версію і чи приймає пошук фільтр версії | `false` |
| `tools` | два імені інструментів, які бачить модель | `search_spec`, `read_section` |
| `answer_hosts` | домени, посилання на які шар 4 лишає у відповіді | порожньо |
| `example_label` | слово з назви розділу, з якого будується приклад ідентифікатора | — |
| `passage_context` | `true`: вектори й індекс по словах бачать не лише текст уривка, а й назву документа та шлях заголовків; для документації, порізаної на дрібні розділи, чий текст не називає своєї теми. Зміна поля — це перерахунок векторів | `false` |
| `fusion_depth` | скільки місць кожного способу бачить злиття пошуку по словах і за змістом; розділ, п'ятий по словах і четвертий за змістом, зі злиття по п'ять місць випадає. Вибирається за виміром `quality` | `k` виклику |
| `revision_suffix` | `true`: суфікс `-<8 знаків хеша>` зрізається з імені документа перед злиттям однакових фрагментів. Для читача, що пише документ на кожну редакцію файла (`ghdocs-history`): без поля незмінний розділ двох редакцій лишається двома фрагментами. Id фрагмента бере повне ім'я | `false` |
| `variant_pattern` | регулярний вираз з однією групою — ім'я варіанта на початку імені документа, напр. `^docs-(nextjs\|react\|vue)-` для сайту, що тримає сторінку на кожен SDK. Варіанти того самого розділу займають у видачі одне місце замість кількох; якщо запит називає варіант, місце дістається його копії. Без поля видача та сама, що до його появи | немає |
| `variant_aliases` | `{варіант: [слова]}`: як запит називає варіант (`"nextjs": ["next.js"]`); без поля — саме ім'я варіанта, «-» як пробіл | немає |
| `variant_strict` | `true`: коли запит називає варіант, сторінки інших варіантів, що не мають його копії, до видачі не потрапляють зовсім (довідник API кожного фреймворку з власними іменами сторінок). Без поля варіанти лише згортаються | `false` |
| `title_match` | `true`: розділ, чию назву-ідентифікатор (`Object.freeze`, `SameValue`, `[[Get]]`) запит містить дослівно, стає першим; звичайні слова заголовків не рахуються. Без поля видача та сама, що до його появи | `false` |
| `raw_store` | `false` вимикає сховище сирого (крок 6) | `true` |
| `max_per_doc` | скільки місць видачі може зайняти одна родина документів (та сама сторінка всіх версій, README пакета всіх редакцій). Вибирається за виміром `quality` | без обмеження |
| `slug_rewrite` | перелік пар `[вираз, заміна]` для ключа сторінки: сайт, що між версіями переклав файли, дає одній сторінці різні імена, і без спільного ключа редакції не зливаються | немає |
| `families` | `{"родина": ["id джерела", …]}`: джерела, що є редакціями одного сайту (`tw-v1` … `tw-v4`); однаковий розділ родини займає у видачі одне місце й показує найновішу редакцію. Кожне джерело — щонайбільше в одній родині | кожне джерело окремо |
| `version_line_depth` | скільки чисел складають лінію версії для фільтра версій: 1 (`18`) чи 2 (`1.35`, корпус із багатьох інструментів) | 1 |

**Зайняті порти** — у `config.json` кожного примірника; перелік дає `grep -h '"port"' instances/*/config.json | sort`.
Беріть наступний вільний.

## Крок 3 · `sources.json`

Це не крок, це робота. Усе інше механічне.

Треба з'ясувати, як цільовий сайт віддає документацію, і вирішити, чи підходить котрийсь із наявних читачів. Принцип
білого списку непорушний: оновлювач тягне рівно те, що оголошено в `sources.json`, і нічого більше.

```json
{
  "instance": "<домен>",
  "sources": [
    {
      "id": "docs-current",
      "url": "https://example.com/llms.txt",
      "reader": "llms",
      "version": "1.4",
      "within": ["https://example.com/docs/"],
      "title": "Документація Example 1.4",
      "added": "2026-09-21",
      "note": "Навіщо це джерело і що воно покриває."
    }
  ]
}
```

**Обов'язкові поля:** `id`, `url`, `reader`. Адреса мусить бути `https`. Повторений `id` відхиляється.

**Поширені необов'язкові поля**

| Поле | Навіщо |
|------|--------|
| `within` | єдині префікси адрес, куди цьому джерелу можна; посилання поза ними пропускаються, а не тягнуться |
| `version` | версія, яку несе кожен документ джерела; кілька — через кому |
| `frozen` | `true` означає знімок, який не має мінятися; `check` рахує будь-який зсув помилкою |
| `title`, `label`, `note`, `added` | людські дані; `note` пояснює, навіщо джерело існує |
| `pages` | адреси сторінок, живих на сайті, але прибраних із меню |
| `index` | додаткові сторінки-змісти, з яких беруться посилання |
| `folders`, `root`, `recursive`, `files` | читачі репозиторію: які теки брати, який префікс знімати |
| `before` | читачі блогу: лишити лише записи, старші за цю дату |
| `keep_links` | лишити адреси в тексті; для сторінки-мапи, де посилання і є змістом |
| `expand`, `children`, `alt`, `meta` | читачі специфікацій: розгортання підсторінок і запасні назви |

### Основні читачі

| Читач | Форма джерела |
|-------|---------------|
| `toc` | багатосторінкове видання ecmarkup; адреси глав беруться зі змісту |
| `page` | одна сторінка ecmarkup, поділена на верхні розділи |
| `pdf` | стандарти, які видають лише PDF-ом |
| `rfc` | текст RFC; колонтитули й кінцевий покажчик прибираються |
| `report` | HTML звіту Unicode (UAX/UTS) з номерами в заголовках |
| `ldml` | частини UTS #35, де в розмітці номерів розділів немає |
| `llms` | перелік сторінок у форматі `llms.txt`; текст кожної — її markdown-двійник |
| `mdblog` | сторінка-перелік блогу; записи беруться markdown-ом |
| `mdpage` | одна markdown-сторінка |
| `nextdata` | сайт на Next.js, де вміст лежить у `<script id="__NEXT_DATA__">` |
| `gatsby` | сайт на Gatsby, що поруч зі сторінкою віддає `page-data.json` |
| `gatsby-blog` | блогова половина сайту на Gatsby |
| `ghdocs` | markdown-документація на тезі чи коміті репозиторію |
| `changelog` | `CHANGELOG.md`, поділений на версії: одна версія — один документ |
| `ghreleases` | нотатки релізів GitHub через API |
| `ghcommit` | один коміт: повідомлення, автор, дата, склад файлів |

Ці шістнадцять — лише перші: на 12.10.2026 фабрика реєструє 103 читачі в 78 модулях — сайти на Mintlify, Docusaurus,
DevSite і Sphinx, реєстри npm і PyPI, історії репозиторіїв тощо. `grep -h '@register' engine/readers/*.py` перелічує
всі імена; докстрінг кожного модуля описує його читачі та їхні поля.

Якщо не підходить жоден, новий читач в `engine/readers/` йде першим, до всього іншого. Читачі реєструються самі,
тож жодного спільного файлу правити не треба.

## Крок 4 · Перевірка оголошення, без мережі

```
./df <домен> sources --why
```

Голосно падає на відсутньому полі, адресі не-https, повтореному `id` чи невідомому читачі.

## Крок 5 · Пробний перелік

```
./df <домен> list
```

Показує, що завантажилося б. Не пише нічого. Цей вивід варто читати уважно: це найдешевша мить, щоб помітити, що
читач підхоплює не ті сторінки.

## Крок 6 · Завантаження корпусу

```
./df <домен> refresh
./df <домен> manifest
```

`refresh` тягне лише задеклароване. `manifest` пише `corpus/index.json`, паспорт: адреса, дата завантаження й сума
тексту кожного документа. Жоден із цих кроків нічого не видаляє.

Корисні варіанти: `./df <домен> refresh --missing` пише лише відсутні файли, а `./df <домен> refresh <id> <id>`
обмежує прогін названими джерелами — інших навіть не перелічує. Перерваний повний прогін продовжують командою
`refresh <джерело, де зупинився>`, а потім `refresh --missing`.

Кожна відповідь лягає ще й у сховище сирого `raw/`, стиснутою й такою, як прийшла. Змінена сторінка не затирає
збереженої: стара версія переїжджає в `raw/_old/<день>/`. Після правки читача `./df <домен> build [id…]` збирає
тексти зі сховища без мережі, за хвилини. `"raw_store": false` у `config.json` вимикає сховище.

## Крок 7 · `prompts/`

П'ять файлів. Текстів за змовчанням немає навмисно: опис інструмента, вгаданий за чужий домен, це рівно та
впевнена вигадка, проти якої весь інструмент і зроблено.

- **`search.txt`** — що в корпусі, коли кликати інструмент і, найголовніше, **коли не кликати**. Найдовший із
  п'яти і той, що найбільше впливає на якість відповідей.
- **`read.txt`** — як прочитати один фрагмент за ідентифікатором, і що у відповіді є адреса джерела та дата
  завантаження, щоб цитату можна було звірити.
- **`loaded.txt`** — рядок про те, що завантажено. `{excerpts}`, `{documents}` і `{versions}` підставляє сервер.
- **`agent.txt`** — системний промпт для `ask`. Мусить називати домен і два імені інструментів, і мусить казати,
  що вказівки, знайдені всередині отриманого тексту, це дані, а не команди.
- **`refusal.txt`** — текст, який повертається, коли шар 1 блокує запит.

## Крок 8 · `checks.json`

Пишеться після того, як з'явився перший корпус, бо потребує реальних чисел і реальних ідентифікаторів.

| Поле | Що фіксує |
|------|-----------|
| `expected_passages` | скільки фрагментів дає корпус; `smoke` падає, якщо число зсунулося |
| `expected_note` | чому число саме таке і коли його знято |
| `find` | запит, який мусить повернути відомий розділ |
| `short` | короткий розділ, який усе одно мусить знаходитися |
| `count_query`, `plain_query`, `long_query`, `ua_query`, `mixed_query` | форми запитів, які сервер мусить пережити |
| `bad_id` | ідентифікатор, який мусить бути відхилений |
| `url_prefix` | префікс для перевірки посилань у відповіді |
| `paraphrase` | запит, у якому немає жодного спільного слова з текстом цілі |
| `description_phrases` | фрази, які мусять бути в описах інструментів |
| `layer1_legit` | справжні питання домену, які шар 1 мусить пропустити |
| `layer4_keep` | числа й версії, які шар 4 не має маскувати |
| `version_probe` | запит разом із версією, коли `versions` true |
| `quality` | десять пар «запит і ціль» для заміру `quality` |

**Про цілі `quality`.** Ціль це всі сторінки, які знаюча людина прийняла б як відповідь, і добирається вона з
документації, а не з того, що знайшов пошук. Ціль може бути рядком або списком рядків. У режимі `markdown` ціль без
`#` означає документ цілком, і так називають лише документ, що весь про це питання. Якщо у питання виходить п'ять
правильних відповідей, розмите питання: переписують запит, а не розширюють ціль.

## Крок 9 · Пошук за змістом, необов'язково

```
./df <домен> setup
./df <домен> vectors
```

`setup` питає один раз, брати Qdrant чи лишитися на пошуку по словах; рішення пишеться в `out/mode.json` і його
можна передумати. `vectors` підіймає контейнер, довантажує модель і рахує вектори. Хвилини процесора, без грошей і
без мережі, окрім завантаження самої моделі.

Контейнер `agent0826-qdrant` **спільний** з іншими проєктами. Видалення колекцій це рішення людини, і жоден крок
його не робить. У своїй колекції `vectors` наприкінці кожного прогону прибирає точки, чиїх фрагментів у корпусі вже
немає, — крім випадків, коли корпус неповний або жодної наявної точки не впізнано. Колекцій, томів і контейнерів він
не чіпає ніколи.

## Крок 10 · Перевірки

```
./df <домен> smoke       # перевірки повз протокол
./df <домен> protocol    # діалог по протоколу, чужим клієнтом
./df <домен> raw         # сирі кадри JSON-RPC, без бібліотеки
./df <домен> tools       # рукостискання MCP, перелік інструментів
./df <домен> quality     # замір: що додає пошук за змістом
```

`quality` це замір, а не перевірка: він ніколи не падає. Абсолютне число саме по собі нічого не означає; сенс має
лише порівняння трьох стовпців на одній і тій самій десятці запитів.

## Крок 11 · Підняти сервер і під'єднати

```
./df <домен> serve
```

Лишіть жити в окремому терміналі. Далі, один раз:

```
claude mcp add --transport http --scope user <server_name> http://127.0.0.1:<порт>/mcp
```

У сесії Claude Code команда `/mcp` має показати сервер із двома інструментами.

## Крок 12 · Описати

Напишіть `README.md` і `UPDATE.md` примірника, далі додайте домен у перелік примірників кореневого `README.md`.
`UPDATE.md` важливіший, ніж здається: саме там записується, як зробити знімок перед підняттям версії і що не можна
видаляти ніколи.

У `README.md` примірника **обов'язково** має бути, як підняти саме цей сервер: заради нього примірник і робиться,
і шукають це першим. Тобто venv, `./df <домен> serve` із номером порту, обидва способи запису в Claude Code
(`.mcp.json` цієї теки або `claude mcp add --transport http --scope user`), перевірка через `/mcp` і те, який
вигляд має зайнятий порт і невдале під'єднання. Перелік доменів у кореневому README цього не замінює: там опис
фабрики, а не інструкція.

## Підсумковий список

```
[ ] .venv піднято, залежності встановлено
[ ] config.json: вільний порт, власна колекція, профіль заповнено
[ ] sources.json: усі джерела оголошено, білий список обмежено через `within`
[ ] ./df <домен> sources --why  проходить
[ ] ./df <домен> list           виглядає правильно
[ ] читача перевірено на кількох типах сторінок до повного завантаження
[ ] корпус завантажено, паспорт записано
[ ] prompts/: усі п'ять, у жодному немає слів чужого домену
[ ] checks.json: справжні числа, цілі дібрані з документації
[ ] smoke, protocol, raw, tools зелені
[ ] quality: «як модель» 10 із 10
[ ] README.md каже, як підняти сервер і записати його в Claude Code
[ ] README.md і UPDATE.md написані; кореневий README називає домен
[ ] архівний режим: corpus і raw в архіві, архів звірено, тексти й raw/ прибрано
```

---

<a name="português"></a>

# Português

## O que você obtém no final

Um servidor MCP protegido que responde perguntas sobre um corpo de documentação, a partir de um corpus local, com
quatro camadas de proteção. O código compartilhado nunca é alterado: um novo domínio acrescenta uma pasta de dados
em `instances/` e, somente se o site de destino exigir, um novo leitor em `engine/readers/`.

## Pré-requisitos

| Necessário | Para quê | Obrigatório? |
|------------|----------|--------------|
| bash (Linux, macOS ou WSL no Windows) | `df` chama o `.venv/bin/python` do Linux; um shell nativo do Windows não roda | sim |
| Python 3.10 ou mais recente | todo o motor | sim |
| Docker | busca por significado (Qdrant); sem ele o servidor busca apenas por palavras | não |
| Chave da Anthropic | apenas o passo `ask`, o agente próprio do projeto | não |

Tudo, exceto o primeiro passo, roda a partir da raiz `docfactory/` como `./df <instância> <passo>`.

## Práticas das instâncias já montadas

O que a montagem de mais de sessenta instâncias ensinou. Cada linha já custou um novo download ou uma resposta
errada.

- **Combine o escopo antes de qualquer trabalho.** Fontes, em ordem de confiança: o site oficial, o repositório
  oficial, o registro de pacotes. O registro do npm é a base para pacotes, versões (canary incluídas) e migrações.
  Quando a documentação cobre várias versões, a padrão é a mais baixada; se duas estão próximas, responda para
  ambas.
- **Ambiente antes do corpus.** Primeiro o venv e o `.env` da instância; para fontes do GitHub acrescente uma linha
  `GITHUB_TOKEN` a esse `.env` (a API anônima permite 60 requisições por hora). Antes disso não rode `refresh`,
  `vectors`, `smoke` nem `quality`.
- **Teste o leitor em vários tipos de página antes do download completo:** uma visão geral, uma página de tarefa com
  abas ou sanfonas, uma página de referência, uma entrada de changelog. Duas páginas não são amostra: um leitor que
  não via os painéis das abas já custou dois downloads completos de um site de 3 000 páginas.
- **Corrija leitores sem rede.** Cada resposta fica no armazenamento bruto `raw/` (passo 6); depois de corrigir um
  leitor rode `./df <domínio> build`, não um novo `refresh`.
- **Execuções longas sobrevivem ao terminal.** Um download de horas começa desacoplado, p. ex.
  `setsid nohup ./df <domínio> refresh > refresh.log 2>&1 &`. Uma execução interrompida continua com
  `refresh <fonte onde parou>` e depois `refresh --missing`.
- **Ordem da montagem:** documentos → `vectors` → `smoke` → `quality` → ajustes até «como o modelo» dar 10 de 10 →
  `smoke` e `quality` de novo → README → planos de estudo e o mapa `docs/learning-map.md` por último.
- **Chaves do `config.json`** (passo 2): `slug_rewrite` quando o site renomeou arquivos entre versões, `families`
  para fontes que são edições de um mesmo site, `max_per_doc` e `fusion_depth` só medindo com `quality`;
  `answer_hosts` lista todos os domínios para os quais os documentos apontam, inclusive páginas fora do site de
  documentação. O campo de fonte `name_prefix` separa os documentos «overview» e «line-2» de vários pacotes numa
  mesma instância.
- **Referência de API gerada** (TypeDoc e afins): os subtítulos «Parameters», «Returns», «Default Value», «Inherited
  from», «Extends» partem cada membro em trechos de uma palavra e separam o valor padrão da sua opção. O campo
  `inline_titles` do leitor `sitemap-html` os transforma em rótulos dentro da seção do membro. Páginas de aliases
  de tipo e de variáveis são curtas de verdade; `min_chars` as mantém em vez de rejeitá-las como páginas de erro.
- **Um site montado a partir de arquivos do repositório** (VitePress: `<!--@include-->`, `<<< @/snippets`, variáveis
  `{{…}}` de `<script setup>` e de `package.json`) é lido das tags com o campo `vitepress` do leitor `ghdocs-history`:
  a página sai como o site a mostra, e a sua revisão conta também os arquivos inseridos. Antes do download completo,
  teste o leitor num clone *bare* local do repositório: todas as tags e arquivos estão ali sem rede. Versões lançadas
  sem tag (changesets) vêm do commit de lançamento, cujo SHA completo serve de chave em `tags`.
- **Texto gerado dentro da página não é uma nova revisão.** Um site em Vocs (campo `vocs` do leitor
  `ghdocs-history`) guarda em cada bloco de código um cache de tipos twoslash de vários kilobytes
  (`// @twoslash-cache: …`), refeito junto com os tipos: uma revisão calculada do arquivo cru daria a uma página
  inalterada um novo documento quase a cada versão. Calcule a revisão do texto que o leitor vê, sem essas linhas; o
  commit de lançamento de uma versão sem tag é o campo `gitHead` dessa versão no registro npm.
- **Um site de documentação sem versões** (Foundry Book: um único ramo vivo, sem tags) recebe versões pelo dia do
  lançamento: para cada versão estável, o último commit do repositório da documentação antes da publicação do release
  (`git rev-list -1 --before=<published_at> master` num clone *bare*); o SHA completo é a chave em `tags`. Duas
  versões no mesmo commit dividem uma chave: `"<sha>": "1.3.4, 1.3.3"`.
- **Um site cujas páginas geradas são sincronizadas com o código antes do release** (biomejs.dev: páginas de regras e
  as referências da CLI e da configuração chegam como commits «synchronize to `<commit do código>`»): um snapshot
  «antes da próxima versão» já traria as regras da próxima. O snapshot de uma versão é o último commit antes da
  primeira sincronização de um commit do código que não está no release (`git merge-base --is-ancestor <commit>
  <gitHead da versão>`); enquanto o site vivia no repositório do código, é o próprio commit do release.
- **Um componente cujo texto vive no próprio arquivo** (`<PackageManagerBiomeCommand command="check" />`): o comando
  é montado a partir do arquivo do componente do mesmo snapshot, e a revisão da página inclui esse arquivo — sites
  mudam esses templates (`npx @biomejs/biome` → `npx biome`).
- **Antes do download completo, liste o que as páginas inserem.** `git grep` num clone *bare* mostra cada alvo de
  inclusão e a sua extensão: um leitor que aceitava só extensões de código perdeu em silêncio a saída de comandos sem
  extensão e o `foundry.toml`, e foi preciso um segundo download. A saída gravada do terminal traz cores ANSI. Depois
  do download, procure no corpus com `grep` restos de `[!include` e `{{#include`.
- **Um site que mudou de pastas** (mdBook `src/` → Vocs `vocs/docs/pages` → `src/pages`): derive as regras de
  `slug_rewrite` com um script que casa os títulos dos documentos entre os períodos e confira em
  `index/passages.json` que uma chave de seção (`slug` e `section`) só é compartilhada por fontes da mesma família;
  uma edição antiga sob outra chave rouba o lugar da nova nos resultados.
- **Duas numerações numa instância** (Foundry 1.8 e forge-std 1.8): marque a segunda (`forge-std-1.17.0`, campo
  `version_prefix` nos releases) para que o filtro de versão não as misture.
- **Um branch de documentação que passou para uma pré-versão** (Drizzle: em dezembro de 2025 o `main` do site recebeu
  a documentação do beta 1.0 e agora instala `drizzle-orm@rc`): uma instância de versões estáveis termina os
  instantâneos do site no último commit antes dessa fusão, as versões estáveis posteriores compartilham essa chave, e
  o que mudou nelas vem dos changelogs. Antes de confiar no instantâneo mais novo, veja os comandos de instalação dele
  (`@rc`, `@beta`, `@next`).
- **Abas cujos nomes ficam no contêiner** (MDX do Astro: `<Tabs items={['PostgreSQL', 'MySQL']}>` com `<Tab>` sem
  nome, `<CodeTabs items>` em que cada bloco de código é uma aba): rotule cada aba a partir de `items`, senão os
  exemplos de todos os dialetos se juntam num só código sem rótulo. Trechos MDX importados com propriedades
  (`<InstallPackages lib='pg'/>`, `{props.lib}`) são expandidos com os valores substituídos, também dentro de células
  de tabela (campo `astro_mdx` do `ghdocs-history`). Antes do download completo, rode o leitor offline sobre todos os
  instantâneos de um clone bare e conte as sobras de tags de componentes e `{props.`.
- **Tutoriais que repetem um passo em cada aba sob título próprio** (quatro «Push your changes to the database» numa
  página) tomam todas as vagas do resultado para o nome de um comando: `max_per_doc` 1 deixa uma vaga para essa
  página.
- **Um changelog com um arquivo por versão** (`changelogs/drizzle-kit/0.31.4.md`) começa direto numa seção: o título
  vem do caminho (`path_title`), e a versão também (`path_version`), com o rótulo do pacote.
- **Uma descrição de pacote npm acima do teto de resposta** (drizzle-orm com centenas de builds de branch: 65 MB) é
  baixada comprimida: campo `gzip` do `npm-versions`.
- **Um site que mudou páginas de lugar muitas vezes** (Prisma: Gatsby, Docusaurus, Fumadocs, cada um com suas
  pastas): os pares de renomeação para `slug_rewrite` vêm dos redirecionamentos do próprio site (`static/_redirects`,
  `vercel.json`), seguindo a cadeia até uma página viva no instantâneo mais novo; o par fica só quando a página antiga
  e a nova compartilham o fim do endereço ou o título e nunca aparecem na mesma versão. Páginas renomeadas sem
  redirecionamento formam pares do mesmo jeito, pelo título e por duas palavras finais do endereço.
- **Um branch vivo que guarda cópias de versões antigas ou prévias da próxima** (`orm/v6`, `docs.v6`, `next/`, `v8/`):
  exclua-as, senão cada instantâneo traria páginas antigas sob números novos. Um patch de uma linha antiga lançado
  depois do próximo major (6.19.1 depois de 7.0.0) compartilha o último instantâneo da sua própria linha.
- **Um branch com uma pasta por versão** (Prisma 1: `docs/1.0` … `docs/1.34`): uma tag, a versão vinda da pasta
  (`path_version`) e uma regra `slug_rewrite` que remove a pasta da versão, para que o texto idêntico de versões
  diferentes se funda.
- **Um repositório renomeado** (prisma/prisma → prisma/orm): para o nome antigo a API do GitHub responde com um
  redirecionamento, que a lista branca recusa; declare o nome novo.
- **Trechos MDX compartilhados com condições sobre propriedades** (`{props.database && (<ul>…</ul>)}`,
  `${props.x.toLowerCase()}` num template de `<CodeBlock>`): avalie as condições antes da substituição, senão uma
  propriedade vazia deixa JSX cru.
- **O leitor é testado offline em todos os instantâneos** sem baixar imagens: um clone parcial
  (`git clone --bare --filter=blob:none`) e depois os blobs necessários num só lote (`git fetch --stdin origin` com os
  SHAs). `git ls-tree -l` pede o tamanho dos blobs e baixa cada blob ausente um a um — deixe o `-l` de fora.
- **Referência TypeDoc guardada como markdown no repositório** (pasta `docs/` do jose): o leitor
  `ghdocs-history-typedoc` transforma os subtítulos dos membros ("Parameters", "Returns", "Call Signature") em
  rótulos dentro da seção (`inline_titles`) e corta seções repetidas em toda página (`drop_titles`: "💗 Help the
  project", "Defined in" com uma linha de código que muda a cada release e impede a fusão das seções entre edições).
- **Um número de versão impresso em toda página** (o import do Deno `deno.land/x/jose@v3.20.4/…`) faz de cada release
  uma nova edição de cada página; `list` mostra a contagem antes do download. Essas tags vão para uma fonte própria
  na mesma entrada de `families` e baixam em paralelo; seções idênticas ainda se fundem no cache de trechos.
- **`ghdocs-history` sem `folders` lê `docs/`**: uma fonte só de arquivos da raiz (`files`) precisa de
  `exclude: ["/"]`, senão repete a documentação da fonte vizinha.
- **Uma versão do pacote publicada sem README** (next-themes 0.3.0) pega o README da tag dessa versão como fonte
  própria; uma regra `slug_rewrite` dá a ele a chave do README do pacote, e as seções inalteradas se fundem num só
  trecho com todas as versões.
- **Versões sem tag e sem `gitHead`** (next-themes 0.0.1–0.2.1) pegam os arquivos do repositório do último commit do
  branch principal antes da publicação da versão no registro npm (`time`); duas versões no mesmo commit dividem a
  chave: `"<sha>": "0.1.0, 0.0.16"`.
- **Um pacote que nunca saiu do 0.x** precisa de `version_line_depth: 2`, senão todas as versões caem numa só linha
  «0» e o filtro de versão não distingue 0.4 de 0.3.
- **Depois de um leitor novo, compare os títulos do arquivo bruto e do documento gravado** em cada página (títulos
  fora de blocos de código, a partir de `raw/`): páginas do nuqs perdiam seções inteiras quando um casamento
  preguiçoso do par `<HumanContent>`/`<LLMContent>` avançava até o bloco seguinte, e uma frase iniciada pela palavra
  "import" engolia uma cerca de código. Uma contagem diferente aponta a página; uma seção de demo vazia se explica.
- **Fontes independentes baixam em paralelo**: um `refresh <id>` desacoplado para cada fonte longa (o site, um segundo
  repositório) e um para o resto; cada processo tem a sua própria pausa por host.
- **Uma plataforma com dezenas de pacotes, cada um com a própria numeração** (Upstash: `@upstash/redis` 1.39,
  `qstash` 2.12, `vector` 1.2, os clientes Python…): cada versão leva o nome do pacote. Valores de tag «redis-1.39.0»
  em `ghdocs-history` e `ghcode-history`, `version_prefix` em `npm-versions`, `npm-tarball-files`, `pypi-versions`,
  `ghreleases` e `ghreleases-stable`; uma tag de monorrepositório `@scope/pkg@x.y.z` vira «pkg-x.y.z». Senão
  `version: "1"` mistura vinte produtos e a lista de linhas não diz nada.
- **Um campo `readme` vazio no registro npm não significa que o tarball não tem README** (20 pacotes `@upstash`,
  entre eles `redis` e `qstash`). Decida as fontes de README pelo número de versões estáveis, pegue o arquivo do
  tarball com `(?i)^readme(\.\w+)?$` e trate os poucos «без файла» como exceção.
- **Pastas de exemplos com os mesmos nomes em vários repositórios** (`examples/nextjs` em sete SDKs) compartilham
  uma chave de seção: `name_prefix` do `ghexamples` (nome do repositório). A varredura de chaves compartilhadas
  também pega um pacote que vive no npm e no PyPI com o mesmo nome (`qstash` → `name_prefix` «qstash-py» no PyPI).
- **Um produto removido do site de documentação** (Upstash Kafka) vem do commit anterior à remoção:
  `commits?path=<pasta>` dá o commit que apagou, o pai dele é o snapshot; a fonte não leva versão. O Mintlify
  escreve o bloco «Documentation index» com maiúscula ou minúscula — o leitor reconhece os dois.
- **Documentação em Snooty rST** (MongoDB: manual do servidor, mongosh, Database Tools, drivers) — o leitor
  `snooty-history`: páginas `.txt`, `include`/`literalinclude`/`sharedinclude` (trechos partilhados de
  `10gen/docs-shared`), abas nas duas notações, passos e extratos YAML dos ramos antigos, constantes `{+x+}` de
  `snooty.toml` e `conf.py`, substituições com valores aninhados, diretivas de objeto como títulos. Procurar os restos
  com um censo do corpus (`|x|`, `{+x+}`, `:ref:`, spans crus) e corrigir o leitor até zero; o que fica são blocos
  literais, onde a marcação é mesmo crua.
- **Não baixar pela rede um repositório de documentação enorme**: clone bare (`git clone --bare`) e a ferramenta
  `tools/seed_snooty_store.py --instance <domínio> --clone owner/repo=caminho` semeia o depósito bruto com cada blob
  pelo seu sha no endereço raw.githubusercontent.com (mapa sha → endereço junto ao depósito), só os ramos e pastas de
  `sources.json`; pela rede só as árvores dos ramos via API; depois `build` sem rede (32 mil páginas em 12 minutos em
  vez de sete horas). Um blob igual em 20 ramos fica guardado uma vez.
- **O tarball de um pacote com escopo** (`@types/mongodb`) é servido num endereço com "/" literal
  (`/@types/mongodb/-/…`), não `%2F`: as duas formas têm de estar em `within`, senão todas as versões ficam "sem
  arquivo". DefinitelyTyped, `@nestjs/*` e pacotes pré-compilados (`@mongodb-js/zstd`) não trazem README no tarball:
  para tipos usar `index.d.ts` (`kind: types`), remover as outras fontes de README.
- **Site montado a partir da pasta `docs/` do próprio repositório de código** (docs.ollama.com a partir de
  `docs/*.mdx` de `ollama/ollama`): a fonte do site e o histórico da pasta dão a página atual duas vezes com chaves
  diferentes (`faq` e `docs-faq`), e ela ocupa duas de cinco posições. `slug_rewrite` `^docs-` → `` e uma entrada de
  `families` para as duas fontes as juntam numa posição; textos iguais fundem-se num trecho.
- **Código em Go ou Python**: o campo `outline` do leitor `ghcode-history` como lista de linguagens (`["go"]`,
  `["python"]`) divide o arquivo pelas declarações de nível superior junto com o comentário acima delas (em Python
  também os métodos da classe, variantes `@overload` como uma seção). `outline: true` mantém o sentido antigo para as
  instâncias já conferidas.
- **Uma família de três ou mais instâncias**: uma cadeia noturna de passos pesados (vetores um após outro, smoke e
  quality depois de cada), os relatórios por temporizador continuam enquanto a cadeia vive. `ua_query` em `checks.json`
  é só cirílico (uma palavra latina quebra a verificação), e a versão de prova é uma linha (`"9.11"`), não uma versão
  completa, quando há centenas de linhas.
- **Um monorrepositório cujos pacotes marcam os próprios lançamentos** (js-contrib: 3 396 tags de 78 pacotes em 145
  commits; Collector: 7 094 tags de módulos em 195): a chave em `tags` é o SHA completo do commit do lançamento, assim a
  árvore é buscada uma vez por commit, e cada pacote ganha fontes próprias só com os seus lançamentos, rotuladas com o
  seu nome (`instrumentation-pg-0.55.0`); senão o README carrega as versões dos vizinhos no commit. Um pacote retirado
  de `main` pega o changelog do commit do seu último lançamento.
- **Código e testes de centenas de lançamentos**: dezenas de milhares de revisões de arquivos, horas pela rede um a um.
  `./df <domínio> list` busca as árvores pela API, `tools/seed_git_store.py --clone dono/repo=caminho` põe cada blob
  de um clone bare no armazenamento bruto sob o endereço que o leitor vai pedir, e `build` roda sem rede (35 mil
  arquivos em segundos; um clone `--filter=blob:none` baixa só os blobs selecionados).
- **Um front matter do Hugo guardado num comentário HTML** («`<!--- Hugo front matter … --->`» no topo de cada arquivo
  das especificações do OpenTelemetry desde 2023): o campo `lead_comment` do leitor `ghdocs-history`; senão o nome do
  arquivo vira o título e, com `passage_context`, ainda entra em cada vetor. Antes de `vectors`, olhe a primeira linha
  dos documentos escritos.
- **Documentos que mudaram de repositório** (convenções semânticas: da especificação para um repositório próprio na
  1.21, depois `database/` → `db/`): derive o `slug_rewrite` dos títulos dos documentos, mantenha só os pares que nunca
  coexistem numa versão e ponha as duas fontes numa entrada de `families`; então a edição antiga deixa de tomar os
  primeiros lugares da nova.
- **Qualidade.** A segunda dezena de `quality` («como o modelo»: consultas com os nomes da própria documentação, como
  o prompt manda o modelo escrever) é a meta principal: 10 de 10. Os alvos só crescem com respostas genuínas. Um
  alvo precisa ser uma seção com texto próprio: um documento que é só cabeçalho nunca é encontrado como seção. A
  `ua_query` é puramente cirílica: sem dígitos e sem latim.
- **Modo de arquivo**, quando os textos não devem ficar na pasta (licença, tamanho):
  `tar -czf <arquivo>.tar.gz -C instances/<domínio> corpus raw`; descompacte numa pasta à parte e compare com o
  disco; só então apague os `.txt` e `raw/`, comprima `index/passages.json` em `passages.json.gz` e faça commit do
  passaporte e do cache. Um arquivo vigente por instância; antes de uma atualização, descompacte-o de volta.
- **Correções cosméticas de leitor**, que quase não mudam o resultado, esperam a próxima atualização da instância
  em vez de um download próprio.
- **Livros e páginas** são citados como título, autor, editora e ano da edição mais recente.
- **O relatório da instância** termina com os comandos para subir e registrar o servidor: `./df <domínio> serve` e
  `claude mcp add …` tanto para o WSL quanto para o Windows — o Claude Code guarda configurações separadas em cada
  um.
- **Uma suíte de testes em JSON** (JSON-Schema-Test-Suite: por arquivo, um array de grupos «schema + instâncias
  marcadas valid ou invalid»): lido como código, o arquivo é cortado por tamanho no meio de um schema. O leitor
  `json-test-suite` faz de cada grupo uma seção com a descrição como título. O mesmo grupo está na pasta de cada
  draft; um `variant_pattern` no prefixo da pasta junta as cópias numa só posição do resultado.
- **Uma especificação em várias versões** (JSON Schema draft-03 … 2020-12 do arquivo do IETF): `ietf-text` com
  `version` em cada fonte. As edições -00 e -01 de uma versão têm as mesmas chaves de seção, e as seções idênticas se
  fundem num trecho com as duas.
- **Um selo dentro de um título** (VuePress `### unevaluatedProperties <Badge text="NEW: draft 2019-09" />`) vira uma
  linha abaixo do título, não parte dele: senão a versão que acrescentou o selo dá à seção uma chave nova, e as
  edições deixam de se fundir. Uma cerca de código recuada fecha junto com o item da lista, como no markdown-it: um
  «```» sobrando transformava meia página em código.
- **Ajuda escrita em XML com inclusões** (LibreOffice `.xhp`: `<embed href="arquivo#id">`, `<embedvar>`): a página é
  montada com as inclusões da mesma tag, e sua edição é calculada a partir das impressões digitais dos elementos
  incluídos, não de arquivos inteiros. Um arquivo-coletânea de caminhos de menu muda a cada versão; a impressão do
  arquivo daria uma edição nova a centenas de páginas inalteradas. Leitor `ghdocs-history-xhp`.
- **Um repositório cuja árvore o GitHub devolve truncada** (`LibreOffice/core`, mais de cem mil arquivos): a árvore é
  lida pasta por pasta (`git/trees/<tag>:<pasta>?recursive=1`, campo `roots`), e localmente um clone parcial só das
  tags necessárias: `git fetch --depth=1 --filter=blob:none origin refs/tags/<tag>:refs/tags/<tag>` — 35 MB de árvores
  em vez de gigabytes; `tools/seed_git_store.py` baixa só os blobs selecionados.
- **Um leitor que lê páginas já durante a listagem** (inclusões, edições por impressões digitais) não passa por
  `list`: um armazenamento semeado a partir de um clone não tem validadores, e `list` baixaria cada página pela rede de
  novo. As árvores das tags são gravadas por `seed_git_store.py --trees`, depois `build` sem rede.
- **Uma referência de API gerada a partir de IDL** (UNO, da qual se monta api.libreoffice.org): o arquivo é dividido
  em uma seção por membro, a descrição do comentário junto da declaração; dividido por tamanho, ele separava a
  descrição de um método do seu nome.
- **Páginas MediaWiki** são lidas via `?action=render`: modelos expandidos, sem menu e sem links «edit»; o campo
  `start` corta a navegação no topo do conteúdo.

## Anatomia de uma instância

Quatorze arquivos, com a mesma composição em todas as instâncias, mais cinco pastas que se criam sozinhas.

| Caminho | O que contém | Quem escreve |
|---------|--------------|--------------|
| `config.json` | porta, coleção, modelo de vetores, perfil do domínio | você |
| `sources.json` | de onde buscar, e ao mesmo tempo a lista branca do atualizador | **você, o trabalho principal** |
| `prompts/search.txt` | descrição da ferramenta de busca que o modelo lê | você |
| `prompts/read.txt` | descrição da ferramenta que lê um trecho | você |
| `prompts/loaded.txt` | uma linha dizendo o que está carregado; `{excerpts}`, `{documents}`, `{versions}` são preenchidos | você |
| `prompts/agent.txt` | prompt de sistema do agente próprio (`ask`) | você |
| `prompts/refusal.txt` | texto que a camada 1 devolve ao bloquear um pedido | você |
| `checks.json` | consultas e expectativas de `smoke`, `check`, `raw` e `quality` | você, após o primeiro corpus |
| `requirements.txt` | conteúdo do venv da instância | copiar e depois enxugar |
| `.env.example` | modelo para a chave; um `.env` real nunca vai para o git | cópia |
| `.gitignore` | `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `out/`, `index/passages.json` | cópia |
| `.mcp.json` | registro do servidor HTTP para o Claude Code | cópia, trocar a porta |
| `README.md` | o que é este domínio e de onde vem sua documentação | você |
| `UPDATE.md` | como atualizar o corpus quando a origem mudar | você |
| `corpus/` | documentos baixados mais `index.json`, o passaporte | `refresh`, `manifest` |
| `index/` | o cache de trechos `passages.json` do qual o servidor sobe; no modo de arquivo vai para o git comprimido, `passages.json.gz` | montado a partir de `corpus/` pelo primeiro passo que precisa dele |
| `raw/` | respostas brutas dos sites para o `build` sem rede, versões antigas em `raw/_old/`; nunca vai para o git | `refresh`, `check`, `list` |
| `out/` | a decisão sobre o modo de busca, logs | `setup`, `serve` |
| `.venv/` | ambiente virtual próprio da instância | passo 1 |

## Passo 1 · Pasta e ambiente virtual

É o único passo executado de dentro da pasta da instância. Nunca é preciso ativar o venv: o `df` chama sozinho o
`.venv/bin/python` da instância certa.

```
mkdir -p instances/<domínio>/prompts
cp instances/react/requirements.txt instances/react/.gitignore instances/react/.env.example instances/<domínio>/
cd instances/<domínio>
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cd ../..
```

**Armadilha conhecida.** Em alguns sistemas o `python3` do pacote vem sem o módulo `venv`. Use um interpretador que
o tenha, por exemplo o do conda: `/caminho/para/miniconda3/bin/python3 -m venv .venv`. Isso não afeta nada depois,
porque o venv é autocontido.

Enxugue o `requirements.txt` conforme o domínio. `pypdf` só é necessário se alguma fonte for PDF; `fastembed` só se
você quiser busca por significado.

## Passo 2 · `config.json`

```json
{
  "instance": "<domínio>",
  "port": 8762,
  "collection": "docs-<domínio>",
  "embed_model": "bge-small",
  "pause_sec": 5,
  "server_name": "<domínio>-docs",
  "doc_set": "<domínio>",
  "sections": "markdown",
  "versions": true,
  "tools": {"search": "search_docs", "read": "read_section"},
  "answer_hosts": ["example.com"],
  "example_label": "<uma palavra do nome de uma seção do seu corpus>"
}
```

| Campo | Significado | Padrão se omitido |
|-------|-------------|-------------------|
| `instance` | nome da pasta, para diagnóstico | — |
| `port` | porta HTTP deste servidor; inteiro de 1 a 65535 | — |
| `collection` | nome da coleção no Qdrant | — |
| `embed_model` | chave do modelo de vetores | — |
| `pause_sec` | pausa em segundos entre requisições ao mesmo site | — |
| `redact` | lista de `{"pattern": regex, "with": texto}`: as ocorrências são substituídas em cada documento antes de gravar, e `check` compara o mesmo texto. Para tokens de exemplo que a documentação mostra no formato de um real: a proteção de push do GitHub os bloqueia | nenhum |
| `server_name` | nome que o cliente MCP exibe | `<pasta>-docs` |
| `doc_set` | rótulo do conjunto no diagnóstico e no nome da coleção | `suite` |
| `sections` | `numbered` para documentos com seções numeradas, `markdown` para sites com `## Título` | `numbered` |
| `versions` | se os documentos carregam versão e se a busca aceita filtro de versão | `false` |
| `tools` | os dois nomes de ferramentas que o modelo vê | `search_spec`, `read_section` |
| `answer_hosts` | domínios cujos links a camada 4 mantém na resposta | vazio |
| `example_label` | palavra do nome de uma seção, usada para montar o identificador de exemplo | — |
| `passage_context` | `true`: os vetores e o índice por palavras veem também o título do documento e o caminho de títulos, não só o texto do trecho; para documentação cortada em seções pequenas cujo texto não nomeia o tema. Mudar o campo exige recalcular os vetores | `false` |
| `fusion_depth` | quantas posições de cada método a fusão da busca por palavras e por significado vê; uma seção quinta por palavras e quarta por significado cai fora de um top cinco fundido de cinco posições cada. Escolhido medindo com `quality` | `k` da chamada |
| `revision_suffix` | `true`: o sufixo `-<8 hex>` (hash da revisão) é cortado do nome do documento antes de fundir trechos idênticos. Para um leitor que grava um documento por revisão de arquivo (`ghdocs-history`): sem ele, uma seção inalterada de duas revisões fica como dois trechos. O id do trecho usa o nome completo | `false` |
| `variant_pattern` | uma expressão regular com um grupo que nomeia a variante no início do nome do documento, p. ex. `^docs-(nextjs\|react\|vue)-` para um site com uma página por SDK. Variantes da mesma seção ocupam um lugar nos resultados em vez de vários; quando a consulta nomeia uma variante, a cópia dela ocupa o lugar. Sem o campo os resultados são exatamente como antes | nenhum |
| `variant_aliases` | `{variante: [palavras]}`: como a consulta nomeia uma variante (`"nextjs": ["next.js"]`); sem ele, o próprio nome da variante com `-` lido como espaço | nenhum |
| `variant_strict` | `true`: quando a consulta nomeia uma variante, as páginas de outras variantes que não têm cópia dela não entram nos resultados (referências de API por framework com nomes de página próprios). Sem ele, as variantes são apenas agrupadas | `false` |
| `title_match` | `true`: a seção cujo nome em forma de identificador (`Object.freeze`, `SameValue`, `[[Get]]`) aparece literalmente na consulta vem primeiro; palavras comuns de títulos não contam. Sem o campo os resultados são exatamente como antes | `false` |
| `raw_store` | `false` desliga o armazenamento bruto (passo 6) | `true` |
| `max_per_doc` | quantas posições dos resultados uma família de documentos pode ocupar (a mesma página em todas as versões, o README de um pacote em todas as revisões). Escolhido medindo com `quality` | sem limite |
| `slug_rewrite` | lista de pares `[regex, substituição]` aplicados à chave da página: um site que renomeou arquivos entre versões dá nomes diferentes à mesma página, e sem chave comum as edições não se fundem | nenhum |
| `families` | `{"família": ["id da fonte", …]}`: fontes que são edições de um mesmo site (`tw-v1` … `tw-v4`); a mesma seção da família ocupa um lugar nos resultados e mostra a edição mais nova. Cada fonte em no máximo uma família | cada fonte sozinha |
| `version_line_depth` | quantos números formam uma linha de versão para o filtro de versão: 1 (`18`) ou 2 (`1.35`, corpus de muitas ferramentas) | 1 |

**Portas já usadas:** no `config.json` de cada instância; `grep -h '"port"' instances/*/config.json | sort` lista
todas. Pegue a próxima livre.

## Passo 3 · `sources.json`

Isto não é um passo, é o trabalho. Todo o resto é mecânico.

É preciso descobrir como o site de destino entrega a documentação e decidir se algum dos leitores existentes
serve. O princípio da lista branca é inviolável: o atualizador busca exatamente o que está declarado em
`sources.json`, e nada mais.

```json
{
  "instance": "<domínio>",
  "sources": [
    {
      "id": "docs-current",
      "url": "https://example.com/llms.txt",
      "reader": "llms",
      "version": "1.4",
      "within": ["https://example.com/docs/"],
      "title": "Documentação Example 1.4",
      "added": "2026-09-21",
      "note": "Por que esta fonte existe e o que ela cobre."
    }
  ]
}
```

**Campos obrigatórios:** `id`, `url`, `reader`. O endereço precisa ser `https`. `id` repetido é rejeitado.

**Campos opcionais mais usados**

| Campo | Para quê |
|-------|----------|
| `within` | os únicos prefixos de endereço que esta fonte pode alcançar; links fora deles são ignorados, não baixados |
| `version` | versão que cada documento da fonte carrega; várias, separadas por vírgula |
| `frozen` | `true` indica um instantâneo que não deve mudar; `check` trata qualquer desvio como erro |
| `title`, `label`, `note`, `added` | dados para humanos; `note` explica por que a fonte existe |
| `pages` | endereços de páginas vivas no site, porém removidas do menu |
| `index` | páginas de sumário adicionais das quais extrair links |
| `folders`, `root`, `recursive`, `files` | leitores de repositório: quais pastas pegar, qual prefixo remover |
| `before` | leitores de blog: manter apenas posts anteriores a esta data |
| `keep_links` | manter endereços no texto; para uma página-mapa em que os links são o conteúdo |
| `expand`, `children`, `alt`, `meta` | leitores de especificação: expansão de subpáginas e títulos alternativos |

### Leitores básicos

| Leitor | Formato da fonte |
|--------|------------------|
| `toc` | edição ecmarkup em várias páginas; endereços dos capítulos vêm do sumário |
| `page` | uma página ecmarkup dividida em seções de primeiro nível |
| `pdf` | normas publicadas apenas em PDF |
| `rfc` | texto puro de RFC; cabeçalhos de página e índice final são removidos |
| `report` | HTML de relatório Unicode (UAX/UTS) com números nos títulos |
| `ldml` | partes do UTS #35 em que a marcação não traz números de seção |
| `llms` | lista de páginas no formato `llms.txt`; cada página vem do seu gêmeo `.md` |
| `mdblog` | página-índice de blog; os posts vêm em markdown |
| `mdpage` | uma única página markdown |
| `nextdata` | site Next.js com o conteúdo em `<script id="__NEXT_DATA__">` |
| `gatsby` | site Gatsby que serve `page-data.json` ao lado de cada página |
| `gatsby-blog` | a metade de blog de um site Gatsby |
| `ghdocs` | documentação markdown como estava em uma tag ou commit do repositório |
| `changelog` | `CHANGELOG.md` dividido por versão: uma versão, um documento |
| `ghreleases` | notas de release do GitHub via API |
| `ghcommit` | um commit: mensagem, autor, data, lista de arquivos |

Estes dezesseis são só os primeiros: em 12.10.2026 a fábrica registra 103 leitores em 78 módulos — sites em
Mintlify, Docusaurus, DevSite e Sphinx, os registros do npm e do PyPI, históricos de repositório e outros.
`grep -h '@register' engine/readers/*.py` lista todos os nomes; a docstring de cada módulo descreve seus leitores e
os campos deles.

Se nenhum servir, um novo leitor em `engine/readers/` vem primeiro, antes de tudo. Os leitores se registram
sozinhos, então nenhum arquivo compartilhado precisa ser alterado.

## Passo 4 · Conferir a declaração, sem rede

```
./df <domínio> sources --why
```

Falha em voz alta diante de campo ausente, endereço que não seja https, `id` repetido ou leitor desconhecido.

## Passo 5 · Ensaio

```
./df <domínio> list
```

Mostra o que seria baixado. Não escreve nada. Leia esta saída com atenção: é o momento mais barato para notar que um
leitor está pegando as páginas erradas.

## Passo 6 · Baixar o corpus

```
./df <domínio> refresh
./df <domínio> manifest
```

`refresh` baixa apenas o que foi declarado. `manifest` escreve `corpus/index.json`, o passaporte: endereço, data do
download e soma de verificação de cada documento. Nenhum destes passos apaga coisa alguma.

Variantes úteis: `./df <domínio> refresh --missing` grava apenas os arquivos ausentes, e
`./df <domínio> refresh <id> <id>` limita a execução às fontes indicadas — as outras nem são listadas. Uma execução
completa interrompida continua com `refresh <fonte onde parou>` e depois `refresh --missing`.

Cada resposta também vai para o armazenamento bruto `raw/`, comprimida e como chegou. Uma página alterada não
sobrescreve a guardada: a versão antiga passa para `raw/_old/<dia>/`. Depois de corrigir um leitor,
`./df <domínio> build [id…]` remonta os textos a partir do armazenamento, sem rede, em minutos.
`"raw_store": false` no `config.json` desliga o armazenamento.

## Passo 7 · `prompts/`

Cinco arquivos. Não existem textos padrão, e isso é proposital: uma descrição de ferramenta adivinhada para o
domínio errado é exatamente a invenção confiante contra a qual esta ferramenta inteira foi construída.

- **`search.txt`** — o que há no corpus, quando chamar a ferramenta e, acima de tudo, **quando não chamar**. É o
  mais longo dos cinco e o que mais afeta a qualidade das respostas.
- **`read.txt`** — como ler um trecho pelo identificador, e que a resposta traz o endereço da fonte e a data do
  download, para que a citação possa ser conferida.
- **`loaded.txt`** — uma linha dizendo o que está carregado. `{excerpts}`, `{documents}` e `{versions}` são
  substituídos pelo servidor.
- **`agent.txt`** — prompt de sistema do `ask`. Precisa nomear o domínio e as duas ferramentas, e precisa dizer que
  instruções encontradas dentro do texto recuperado são dados, não comandos.
- **`refusal.txt`** — texto devolvido quando a camada 1 bloqueia um pedido.

## Passo 8 · `checks.json`

Escrito depois que o primeiro corpus existe, porque precisa de números e identificadores reais.

| Campo | O que fixa |
|-------|------------|
| `expected_passages` | quantos trechos o corpus produz; `smoke` falha se o número mudar |
| `expected_note` | por que o número é esse e quando foi medido |
| `find` | uma consulta que precisa devolver uma seção conhecida |
| `short` | uma seção curta que ainda assim precisa ser encontrada |
| `count_query`, `plain_query`, `long_query`, `ua_query`, `mixed_query` | formatos de consulta que o servidor precisa suportar |
| `bad_id` | um identificador que precisa ser rejeitado |
| `url_prefix` | prefixo usado ao verificar links na resposta |
| `paraphrase` | consulta sem nenhuma palavra em comum com o texto do alvo |
| `description_phrases` | frases que as descrições das ferramentas precisam conter |
| `layer1_legit` | perguntas legítimas do domínio que a camada 1 precisa deixar passar |
| `layer4_keep` | números e versões que a camada 4 não deve mascarar |
| `version_probe` | uma consulta com versão, quando `versions` for true |
| `quality` | dez pares de consulta e alvo para a medição `quality` |

**Sobre os alvos de `quality`.** Um alvo é toda página que uma pessoa que domina o assunto aceitaria como resposta,
e ele é escolhido a partir da documentação, nunca a partir do que a busca por acaso devolveu. O alvo pode ser uma
string ou uma lista de strings. No modo `markdown`, um alvo sem `#` significa o documento inteiro, e isso só se usa
quando o documento inteiro responde à pergunta. Se uma pergunta admite cinco respostas corretas, a pergunta está
vaga: reescreva a consulta em vez de alargar o alvo.

## Passo 9 · Busca por significado, opcional

```
./df <domínio> setup
./df <domínio> vectors
```

`setup` pergunta uma vez se deve usar o Qdrant ou permanecer na busca por palavras; a decisão fica em
`out/mode.json` e pode ser revista. `vectors` sobe o contêiner, baixa o modelo e calcula os vetores. Minutos de CPU,
sem custo e sem rede além do download do modelo.

O contêiner `agent0826-qdrant` é **compartilhado** com outros projetos. Apagar coleções é decisão humana e nenhum
passo faz isso. Dentro da própria coleção, `vectors` remove ao fim de cada execução os pontos cujo trecho já não está
no corpus — exceto quando o corpus está incompleto ou nenhum ponto existente foi reconhecido. Coleções, volumes e
contêineres ele nunca toca.

## Passo 10 · Verificar

```
./df <domínio> smoke       # verificações fora do protocolo
./df <domínio> protocol    # diálogo pelo protocolo, cliente externo
./df <domínio> raw         # quadros JSON-RPC crus, sem biblioteca
./df <domínio> tools       # handshake MCP, listagem de ferramentas
./df <domínio> quality     # medição: o que a busca por significado acrescenta
```

`quality` é uma medição, não uma verificação: nunca falha. O número absoluto nada significa sozinho; só a comparação
entre as três colunas sobre as mesmas dez consultas carrega informação.

## Passo 11 · Subir e conectar

```
./df <domínio> serve
```

Deixe rodando em um terminal próprio. Depois, uma única vez:

```
claude mcp add --transport http --scope user <server_name> http://127.0.0.1:<porta>/mcp
```

Em uma sessão do Claude Code, `/mcp` precisa listar o servidor com suas duas ferramentas.

## Passo 12 · Documentar

Escreva o `README.md` e o `UPDATE.md` da instância e acrescente o domínio à lista de instâncias do `README.md` da
raiz. O `UPDATE.md` importa mais do que parece: é nele que se registra como tirar um instantâneo antes de subir uma
versão e o que nunca deve ser apagado.

O `README.md` da instância precisa dizer como subir este servidor — é para isso que a instância existe, e é a
primeira coisa que se procura: o venv, `./df <domínio> serve` com a porta, as duas formas de registrá-lo no Claude
Code (o `.mcp.json` desta pasta ou `claude mcp add --transport http --scope user`), a conferência pelo `/mcp` e o
que aparece quando a porta está ocupada ou a conexão falha. A lista de domínios no README da raiz não substitui
isso.

## Lista final de conferência

```
[ ] .venv criado, dependências instaladas
[ ] config.json: porta livre, coleção própria, perfil preenchido
[ ] sources.json: todas as fontes declaradas, lista branca limitada por `within`
[ ] ./df <domínio> sources --why  passa
[ ] ./df <domínio> list           parece correto
[ ] leitor testado em vários tipos de página antes do download completo
[ ] corpus baixado, passaporte escrito
[ ] prompts/: todos os cinco, nenhum com palavras de outro domínio
[ ] checks.json: números reais, alvos escolhidos a partir da documentação
[ ] smoke, protocol, raw, tools todos verdes
[ ] quality: «como o modelo» 10 de 10
[ ] README.md diz como subir o servidor e registrá-lo no Claude Code
[ ] README.md e UPDATE.md escritos; o README da raiz cita o domínio
[ ] modo de arquivo: corpus e raw arquivados, arquivo conferido, textos e raw/ removidos
```
