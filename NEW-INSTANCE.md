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
- **Environment before corpus.** Make sure the environment is ready first: the shared venvs (`.venvs/cpu`,
  `.venvs/gpu`) exist and the root `.env` has a `GITHUB_TOKEN` line for GitHub sources (the anonymous API allows 60
  requests an hour). The instance's own venv and `.env` are needed only in the cases of step 1. Do not run
  `refresh`, `vectors`, `smoke` or `quality` before that.
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
  `tar --sort=name -czf <archive>.tar.gz -C instances/<domain> corpus raw` (`--sort=name` puts similar revisions of a
  page next to each other, so gzip compresses a corpus with many revisions about twice as well); unpack it into a
  separate folder and compare with the disk; only then delete the `.txt` files and `raw/`, compress
  `index/passages.json` into `passages.json.gz` and commit the passport and the cache. Keep one current archive per
  instance; unpack it back before an update.
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
- **Man pages in AsciiDoc** (Tesseract `doc/*.asc`: underlined titles, `'FILE'::` definition lists, `....` literal
  blocks, `<<ANCHOR,…>>`): reader `ghdocs-history-asciidoc`. Each definition-list term — an option, a parameter, a
  language code — becomes a subsection, its type and default the first line of text, not part of the heading: as
  bold lines inside a long OPTIONS cut by length, `--oem` was not found at all.
- **A Sphinx site rewritten in MyST Markdown** (OCRmyPDF from 16.0: `:::{note}`, `:::{list-table}`,
  ```` ```{eval-rst} ````, `` {issue}`…` ``): reader `ghdocs-history-myst` together with the field `sphinx` for the `.rst`
  of older tags. A release-notes file that grows with every tag is taken once from the newest tag, and its per-tag
  copies are excluded.
- **`ghdocs-history` with `folders: [""]`** takes only the files at the root even with `recursive`: subfolders
  (`tess3/`, `tess4/`) are named in `folders` one by one. `list` shows it — count the documents per folder.
- **Many tools in one instance** (doc-tools: poppler, ImageMagick, Ghostscript, qpdf, ExifTool and their wrappers):
  every version label carries the tool name (`poppler-26.10.0`, `imagemagick-7.1.1-47`, `ubuntu-24.04`). Otherwise
  `version: "10.0"` mixes Ghostscript 10.0 with qpdf 10.0.
- **A project on GitLab without a GitHub mirror** (poppler on gitlab.freedesktop.org): reader `gitlab-history` —
  the named folders of every tag through the GitLab API by numeric project id, one document per path and blob; a tag
  without the folder yields nothing.
- **A site kept as HTML in the repository** (ImageMagick `www/`, Ghostscript `doc/*.htm`, ExifTool `html/`): reader
  `ghdocs-history-html` with `start`/`end` per site era, `drop` for ads, scripts and SVG icons (their `<title>`
  «Twitter» otherwise became the page title) and `title_strip`. Pages that change once in several releases are taken
  from the last tag of each release line, not from every tag.
- **Changelogs in a dozen formats**: reader `changelog-regex`, the entry heading is a regex in `sources.json` with
  groups `v` and `d`. Man pages in mdoc (`file`) go through `ghdocs-history-roff`; each option of OPTIONS becomes a
  subsection — forty options in one excerpt hid `--mime-type`.
- **A sitemap whose `<loc>` are bare paths** (gvisor.dev, Jekyll without `site.url`:
  `<loc>/blog/2023/06/27/directfs/</loc>`): `sitemap-html` compares `<loc>` with `within` as a string, and not one page
  passes. Reader `sitemap-html-rel` first resolves every `<loc>` against the sitemap address and keeps the trailing
  slash — the bare host without it is not recognised as a page of the site.
- **Markup a verified shared reader does not know** (Jekyll `[TOC]` and Liquid tags in gVisor `g3doc`, Hugo TOML front
  matter `+++` in the archived gvisor-website): a thin module calls `ghdocs_history` through a context wrapper whose
  `text()` cleans every `.md` page before parsing (`ghdocs-history-jekyll`, `ghdocs-history-toml`). A new field in the
  shared reader would risk drift in every instance already built on it; with the wrapper their corpora stay the same
  byte for byte.
- **`site` only for files the site still serves**: the `ghdocs-history` field `site` names the files of the newest tag
  one by one instead of catching everything with `g3doc/(.*)\.md`. A page that moved or vanished
  (`g3doc/checkpoint_restore.md` of 2019) and a file the site never showed (proposals, example READMEs) then cite their
  GitHub blob at their own tag, not a dead site address.
- **Go package reference from pkg.go.dev** (gVisor netstack, `gvisor.dev/gvisor/pkg/tcpip`): reader `pkgsite` takes
  the root package page and every subpackage of its «Directories» table; one document per package with Overview,
  Constants, Variables, Functions and Types, each declaration as a Go code block, methods as subsections. Subpackage
  links carry `@<version>` in the path — strip it, so one `within` prefix covers them all and the links do not age
  every day. pkg.go.dev slows frequent clients down with 429: the reader keeps its own pause (field `pause`, 1.5 s by
  default), while the instance's `pause_sec` for GitHub stays 0. A module without tags shows a pseudo-version
  (`0.0.0-<time>-<commit>`): its documents carry no release version, and the prompt must say «search them without a
  version».
- **The package manager's own description from an APT repository** (gVisor `runsc`): reader `apt-packages` reads the
  `Packages` index of each architecture (`dists/<suite>/<component>/binary-<arch>/Packages`) — one document per
  package with the control fields of every architecture and the long description. Such a repository usually keeps only
  the latest version, so the source answers «what does `apt-get install` put on the machine today» (number, size,
  checksums), not the history; the history comes from the tags.
- **A Sphinx site that publishes every version in a folder of its own** (docs.nvidia.com:
  `…/container-toolkit/1.20.1/`, `…/1.6.0/`): the version list (`versions1.json`) names only the newest few — probe
  the folders by the repository's tag numbers (`index.html` answers 200 or 404). Reader `sphinx-html`: one source with
  `url` holding `{version}` and a `versions` list; the pages of a version are a crawl of `.html` links from its start
  page inside its folder, since page sets differ between years. It drops the heading anchors (`#`, or a font icon
  U+F0C1 in the old theme), takes the code language from the wrapper class (`highlight-console`), labels the tabs
  (sphinx-tabs keeps their names in `<button>`, which HTML parsing drops), keeps table rows on one line and cuts the
  `toctree`. Identical text of a page in several versions becomes one document carrying all of them.
- **A changelog that lists a release's changes under its release candidates** (NVIDIA: «## v1.19.0» says only «Promote
  v1.19.0-rc.7 to v1.19.0»; the changes sit under «## v1.19.0-rc.1» … «-rc.7»): `skip` for `-rc` would leave one line
  per release, and documents labelled «1.19.0-rc.3» are not found by the filter «1.19.0». Reader
  `changelog-prerelease` makes one document per stable release with its candidates as sections; take the file once,
  from the newest tag.
- **An APT repository that keeps every version** (nvidia.github.io/libnvidia-container: 28 versions per package,
  oldest first): `apt-packages` takes the title from the first stanza and would name the oldest version as what
  `apt-get install` puts on the machine. Reader `apt-packages-versions`: the newest by number, a «Versions» section
  with the dependencies of each, labels without the Debian revision (`1.20.1-1` → `1.20.1`) and a `packages` filter.
- **One file — one source.** Command code across every tag and the full code of the newest tag overlap in that tag:
  exclude from the newest-tag source what the all-tags source already takes (`^cmd/.+(?<!_test)\.go$`), or the same
  file becomes two documents under two keys and takes two result slots. Likewise a Go module with no package at its
  root on pkg.go.dev: the `pkgsite` root is a real package (`pkg/nvcdi`), the other public packages go into `pages`.
- **Count the excerpts per source before `vectors`.** An API reference that expands every nested type on every
  endpoint page (platform.claude.com: `messages/create` is 140 KB, and the Python and TypeScript editions repeat it
  in their own syntax) made two thirds of 92 thousand excerpts; at about five excerpts a second that is five hours of
  vectors. The cache `index/passages.json` exists before the first point is computed: group it by source, give the
  user the hours, agree the scope, then start. Pages missing from `llms.txt` and `sitemap.xml` but listed on an index
  page in markdown (nested items, links from the site root) come through the reader `md-index`.
- **Jupyter notebooks** (claude-cookbooks): reader `ghdocs-history-ipynb` — markdown cells as they are, code as blocks
  in the notebook's language, of the output only text, cut to `output_chars`; images and HTML of the output are
  dropped (22 MB of notebooks gave 2.6 MB of text). `extensions` must include `.ipynb`.
- **A repository that changed its tag scheme** (TypeScript SDK `v0.12.3` → `sdk-v0.12.4`, C# SDK `v11.0.0` →
  `Anthropic-v12.0.0`): group the tags by the part before the number before declaring, or the first versions drop out.
  In a monorepo a bare prefix `v` in `ghreleases-stable` also catches `vertex-sdk-v…`: take `v0.` with
  `version_prefix` `typescript-0.`.
- **Two traps of repository readers.** `exclude: ["/"]` drops every path with a folder, a file named in `files` from a
  subfolder (`packages/aws-sdk/README.md`) included — exclude the default `^docs/` instead. `ghexamples` takes only
  projects with `package.json`; examples kept as single files go through `ghcode-history` or `ghcode-history-ts` with
  `include: ["^examples/…"]`.
- **A site that shows code in the language the reader picked** (docs.stripe.com: the markdown twin of a page gives one
  language per `?lang=`): one document per page — the text once, under each section the code of the other languages
  with a label (reader `stripe-md`). A document per language would repeat the page text seven times in the index and
  in vectors. Even so the code made the site 61% of 114 thousand excerpts, and such pages vectorise at about five
  excerpts a second against nine for an API reference: estimate the hours by the rate of each kind of source, not by
  one average.
- **A page that is only a list of variants** ("This article has multiple variants": Checkout or Elements, iOS or
  Android): replace it with the variants, each a document named with its label (`variants: true`). The sitemap may
  list a page twice, plainly and with `.md`: normalise the address before removing duplicates. A page that fails while
  the list is being built must fail only its own document — one 404 cost a whole 26-minute listing.
- **Thousands of tags, a few known files** (Stripe SDKs: over six thousand stable tags against an API quota of five
  thousand calls an hour; GitHub truncates the trees of stripe-ios and stripe-java): read the files straight from
  raw.githubusercontent.com, which spends no API quota — reader `ghraw-history`. Where an SDK has hundreds of minor
  lines, take the last tag of each line.
- **The phrases `smoke` looks for in the prompts** (`description_phrases`) are matched literally, line breaks
  included: when rewrapping `prompts/search.txt` keep each of them on one line ("point by point" split by a wrap
  failed `smoke`).
- **A documentation site that DocFX builds from a public repository** (learn.microsoft.com: AspNetCore.Docs,
  AspNetDocs): read the source, not the site. The site renders pages with JavaScript and serves only the newest
  editions, while the repository holds every edition behind monikers (`monikerRange`, `:::moniker range`), with
  includes and code snippets, some from neighbouring repositories (`~/../AspNetCore.Docs.Samples`) — reader `docfx`.
  Editions the source no longer carries come from the last commit that still had their monikers (ASP.NET Core 1.0–2.2
  and 3.0). Drop HTML comments before expanding includes: an include that names itself inside a comment recursed.
- **An API reference from the packages themselves** (.NET): a NuGet package carries XML documentation next to the
  assembly — the text learn.microsoft.com/dotnet/api is generated from — and the package of each release describes
  exactly that release: reader `nuget-xmldoc`, `ref/` before `lib/`. Count the types first: internal namespaces and
  resource classes (`.Internal`, `CoreStrings`) gave some ten thousand excerpts with no content (`exclude_types`); a
  package without XML gives nothing and leaves `sources.json`.
- **Products that number themselves** (classic ASP.NET: MVC 5.2, Web API 5.3, SignalR 2.4, Katana 4.2 in one instance
  with ASP.NET Core 10.0): the version carries the product as a prefix (`mvc-5.2`; `version_prefixes` in
  `nuget-package`), and packages with their own numbering (OData, SystemWebAdapters) stay out of the per-line sources,
  or OData 8.x lands in ASP.NET Core 8.0. A repository file without front matter takes its title from its first
  heading (`title_from: "heading"` in `ghdocs`); vendored code (googletest under `src/`) is cut with `exclude`.
  Guides of old releases kept in `older-versions*` folders beside the new ones get their lines by path
  (`path_versions` in `docfx`): otherwise the SignalR 1.x guide outranks its 2.x twin, and a search with a version
  finds neither.
- **DocFX monikers without a version number** (learn.microsoft.com/sql: `sql-server-ver16`, `sql-server-linux-ver15`,
  `azuresqldb-current`, `fabric`): the order of a product's versions cannot be read from the name, so the `docfx`
  field `monikers` gives it as lists, one per product, as `learn.microsoft.com/api/familyTrees/bymoniker/<moniker>`
  shows them; `moniker` may be a list (an edition "SQL Server 2022" is what the site shows for both
  `sql-server-ver16` and `sql-server-linux-ver16`). The monikers of a page are its own `monikerRange`, else the
  last matching glob of `build.fileMetadata.monikerRange` in `docfx.json`, else the group's `moniker_range`, minus
  `exclude_monikers`; the page header wins over the folder glob. Check the rule against the site before the fetch:
  every page carries `<meta name="monikers">` (64 random pages, 64 matches).
- **A version the site has dropped** (SQL Server 2016 after its end of support): in a partial clone
  (`--filter=blob:none --shallow-since=…`) count the files whose moniker expressions name it on the first-parent
  commits of the publishing branch; the count stays flat and then falls with a «Retire … monikers» PR. The edition
  comes from the last commit before that PR, with `link: "github"`.
- **Product editions of the same pages** (Azure SQL Database, Managed Instance, Synapse, Fabric): measure first.
  Each edition was thousands of documents, but only about a hundred pages differ in text; identical sections of one
  `families` entry merge, so 85 thousand documents of ten editions gave about 120 thousand distinct excerpts. Count
  the distinct excerpts with a streaming script before `vectors` — documents say little about the hours.
- **A huge DocFX repository from a clone**: `tools/seed_git_store.py` seeds the text blobs of the commit, the tree in
  API form and the files of the dependent repositories the pages reference as `~/../<folder>/…` (shallow partial
  clones fetched by commit SHA, `git fetch --depth=1 --filter=blob:none origin <sha>`); then `build` writes 86
  thousand documents in minutes. Pin the dependent repositories (`repos`) to commits; private ones
  (`reusable-content`) stay out, and their includes drop.
- **A repository whose full tree GitHub truncates** (SupportArticles-docs): the tree of one folder,
  `git/trees/<commit>:support/sql?recursive=1`; `docfx` completes the paths back to the root.
- **YAML pages**: take `YamlMime:FAQ` (questions as sections; a section named «Ignored» has no heading on the site),
  leave Landing, Hub, toc and pivot lists — they are only links (`yaml_pages: true`).
- **Previews with ordinary tags** (mssql-jdbc publishes previews as `v13.5.1`, flagged only on GitHub): `ghreleases`
  field `stable: true`. In a changelog, let the version group of `changelog-regex` capture the word «Preview» and
  `skip` it, so a preview entry does not glue onto the stable entry above it.
- **Build variants inside a Maven version** (`13.6.1.jre8`, `13.6.1.jre11`): `pkg-registry` field `variant`, or every
  version counts as a pre-release.
- **Container image tags** (`mcr.microsoft.com/v2/<image>/tags/list`): reader `registry-tags` — a document per line
  (the SQL Server year) with CU, GDR and OS variants sorted by number, not alphabetically (`CU10` before `CU2`).
- **Vectors: the order of the batch decides the hours.** The model pads every batch of 32 excerpts to its longest
  one; in sql-docs nearly every run of 32 consecutive excerpts held one of 300–512 tokens, and with the same mean
  length as aspnetcore (155 tokens against 139) vectors went at 4.7 excerpts a second instead of 13. `server/setup`
  now computes them shortest first (×2.3 on the CPU, the same vectors to the bit). With an NVIDIA card,
  `fastembed-gpu` and `onnxruntime-gpu[cuda,cudnn]` in the instance's own venv make `common/embed.py` use CUDA
  (~500–800 excerpts a second on an RTX 2070 in WSL, cosine with CPU vectors ≥ 0.99999); venvs with the plain
  `onnxruntime` never take that branch.
- **A crawl of thousands of pages** (`learn-archive`): one page that redirects outside the whitelist must fail
  alone, not the whole listing (archive 2014 died after a thousand pages). The field `workers` fetches a wave of N
  queued pages at once and parses them in order, so the listing is byte-identical; `trust_store` (a day) replays the
  responses already in the raw store without a request after a restart — remove it afterwards, or updates never see
  the site again.
- **A DocFX docset without monikers** (learn.microsoft.com/ef: dotnet/EntityFramework.Docs): the site shows one
  edition, so versions are snapshots of the repository — the last `main` commit a week after `x.y.0` reached NuGet
  (that week the docs are finished for the release), linked to the commit's files on GitHub. A site that lived in
  another format before DocFX (Sphinx until 31.10.2016) takes its first edition from the first commit in the new
  format. Pages of the next major's previews are excluded from every snapshot: the week-after snapshot of the latest
  release may already carry them.
- **C# code of many lines**: `outline: ["csharp"]` in `ghcode-history` — a member with its `///` and attributes is a
  section, so an unchanged method of neighbouring lines is one excerpt. Count after the split: the code and tests of
  efcore across fourteen lines are 224 thousand excerpts (two thirds of the instance) and the server holds 5.6 GB; on
  the GPU the vectors took 11 minutes.
- **NuGet versions with build metadata** (`9.0.15+MySQL9.7.0`): such a package is missing from the semver1
  registration altogether (404) — field `registration: "gz-semver2"` of `nuget-package`.
- **Providers from an official list** are taken from every revision of the list page (the file's history in a bare
  clone), and before declaring `nuget-xmldoc` check that the package of each line carries XML: of 62 provider packages
  18 had it, and only they got an API reference.
- **Release tags carrying a product name or a capital «V»** (`Google.Cloud.EntityFrameworkCore.Spanner-4.1.1`,
  `EFCore-13.0.0.0`, `ef-v0.5.0`, `V4.1.0.0`) are not parsed by `ghreleases` — the version comes out empty; take them
  with `ghreleases-stable` and `tag_prefix`.
- **`ghdocs` strips the first folder of a path**: a sample's `Sample/README.md` and the root `README.md` both get the
  name «readme», and one document overwrites the other — such folders go into separate sources.
- **A MkDocs site that inserts its samples from the tests** (dotnet.testcontainers.org:
  `--8<-- "tests/…/PostgreSqlContainerTest.cs:UsePostgreSqlContainer"`, pymdownx.snippets with
  `dedent_subsections: true`): the sample is only the lines between `// # --8<-- [start:Name]` and `[end:Name]`, the path is relative to the
  repository root. Fields `snippet_sections: true` and `snippets: "."` of `site-history` take the named section
  without its common indent and drop the marker lines; without them such a line looks for a file named «…cs:Name» and
  the sample silently disappears. Declare the test folder in `assets`, and after the fetch grep the corpus for
  leftover `--8<--`. The field `site` (as in `ghdocs-history`) lists the pages of the newest tag by name, so pages
  that were removed cite their file on GitHub.
- **C# with a two-space indent** (Testcontainers: block namespace, type at 2, members at 4; the tests at 4): the rule
  «type plus four» of `outline: ["csharp"]` left a 28-thousand-character builder class as one section.
  `outline_indent: "auto"` takes the members' indent from the first line of the type body. After the split, count the
  headings of the largest class of each repository.
- **A NuGet id that changed owners** (`Testcontainers` 0.0.1–0.0.2.107 of 2018–2019 belong to another author, «Package
  Description», no README, no XML; the library got the id with 2.0.0): before declaring a package, look at
  `authors`, `projectUrl` and the description of its oldest versions in the registration. The field `since` of
  `nuget-package` («package → oldest version taken») cuts them off, otherwise they become a «0.0» line of the product.
- **The API reference of a library Microsoft does not host**: `nuget-xmldoc` links every type to
  learn.microsoft.com/dotnet/api, which knows only Microsoft's packages — `link: "nuget"` links it to the nuget.org
  page of the package version it came from.
- **A page renamed more than once** (`examples/compose.md` → `examples/dind.md` → `dind/index.md`): git sees each step
  between neighbouring tags (`git diff -M --stat <tag> <next> -- docs`, `git log --diff-filter=R --summary`); every
  predecessor gets its own `slug_rewrite` rule to the newest name. A page with the old name and different content
  (`api/compose.md` of 4.15, ComposeBuilder) stays apart.
- **Size before the build.** A passport line costs about 600 bytes, a passage of the gzipped cache 120–200, and GitHub
  refuses files from 100 MiB. Count the pages of every snapshot and the types of every package before writing readers
  (dotnet: 274 thousand documents, a 156 MB passport, 562 thousand passages). When it does not fit, the corpus, the
  cache and the raw store stay local (`corpus/` and `index/` in the instance `.gitignore`, as in `patterns`), with an
  archive outside WSL checked file by file.
- **A DocFX repository with docfx.json at the root** (dotnet/docs): `~/` means the repository root — field
  `tilde_root: ""` of `docfx`; `:::code … id="Assignment":::` points at `// <SnippetAssignment>` —
  `snippet_prefix: "Snippet"`. Before the full build read `.openpublishing.publish.config.json` of every snapshot:
  until 2020 the samples lived in the dependent repository dotnet/samples, and the code of those snapshots vanishes
  silently.
- **The site's API reference from ECMA XML** (dotnet/dotnet-api-docs): reader `ecma-xml`, one document per type with
  the same document name and member headings as `nuget-xmldoc`, so the site reference and the XML of the packages fold
  into one `families` record. `xml/FrameworksIndex` (tens of megabytes) is read with expressions over bytes, not as a
  tree; `skip_monikers` drops preview-only types and members; only C# examples are inserted.
- **Thousands of NuGet packages** (Microsoft.Extensions.*, 1,754 package lines): download them in parallel straight
  into the raw store (`rawstore.put`), noting which carry XML, declare only those and run `build` without network —
  2.5 minutes instead of an hour of `refresh` pauses.
- **Facts of a release line in release metadata** (support phase, end of support) belong to the line document only:
  repeated in each of 285 release documents they took every result for «end of support».
- **Two numberings in one instance** (.NET 8.0 and C# 8): the language carries `csharp-` (`csharp-7` for an edition
  of the standard, `csharp-12.0` for feature specifications). `ghdocs` takes `…/git/trees/TAG:FOLDER` for repositories
  whose full tree GitHub truncates (dotnet/runtime, dotnet/roslyn) and encodes spaces and `#` in file names.
- **Code samples of a DocFX site's dependent repositories** (dotnet/docs until 2020: dotnet/samples laid next to the
  repository as `samples/`): take each snapshot's `.openpublishing.publish.config.json`, point the folder at the
  repository's last commit before the snapshot day through `repos` of `docfx` (a dependent repository that itself kept
  everything in a subfolder gets it as a suffix: `dotnet/samples/<sha>/samples`) and seed only the files the pages
  reference, from a blobless clone. Paths with spaces need `quote_paths: true`: the seeded store keys are encoded, and
  without the field 870 ADO.NET samples per snapshot fell out.
- **`slug_rewrite` from a DocFX site's redirection files** (`.openpublishing.redirection.*.json` of every snapshot plus
  git renames between snapshots): follow the chain to a page alive on the newest branch and keep a pair only when the
  two pages never stand in one snapshot and share a title or the end of the path — about a third of the redirections
  lead to a general section page and are dropped. 1,880 anchored rules add two minutes to the passage cache build.
- **Measure before changing a reader**: one process with the index loaded (`server.quality` with
  `profile.MAX_PER_DOC`/`FUSION_DEPTH` patched, or a filter wrapped around `spec_mcp._dedup` for dropping a kind of
  section) measures every variant in minutes; only what wins goes into the reader or `config.json`.
- **A Docusaurus site that kept every version in its own folder and later deleted the old ones**
  (playwright.dev: `dotnet/versioned_docs/version-1.12` … `version-1.23`, then only `version-stable`): take each
  folder from the repository history in its last edition — the parent of the commit that deleted it, or the commit of
  its last change when that parent is already taken by another version — and write `{version}` in `folders`, so each
  commit gives only its own version's folder, not every version lying next to it. A `slug_rewrite` from
  `version-1-X-` to `version-stable-` and one family in `families` merge the editions of a page. For the
  `version-stable` era the snapshot of a line is its last «roll to 1.X» commit.
- **The same example in tabs for several variants** (NUnit / MSTest / xUnit, npm / yarn / pnpm): `docusaurus_tabs: true`
  puts the tab's label before its content; without it the text holds several identical code blocks with nothing to say
  which is which.
- **Documentation of .NET repositories built with Jekyll, kramdown and mdsnippets** (xunit.net, fluentassertions.com,
  nsubstitute.github.io, Shouldly): kramdown attribute lists `{: .issue-link }`, heading anchors `{ #id }`, Liquid
  tags `{% examplecode csharp %}` with a hidden `{% requiredcode %}` scaffold, «snippet source | anchor» lines under
  mdsnippets inserts — reader `ghdocs-history-kramdown`. The `jekyll_data` field expands
  `{% include … examples=site.data.… %}` inserts whose data lives in YAML (the FluentAssertions tips — over a hundred
  «before — better» pairs); a data file the tag does not have yet renders nothing in Jekyll, and the insert vanishes
  instead of failing the page. Before downloading, take a census of the markup on the newest tag's pages
  (`git grep -o` over a full bare clone).
- **A DocFX site outside learn.microsoft.com** (docs.nunit.org, bunit.dev): the same `docfx` reader; a site with tags
  is one source per last tag of every minor line in one family, seeded from a clone (`seed_git_store.py`). A page with
  only `uid` in its front matter takes its title from the first «# …» (`title_from: "heading"`), and redirect pages
  (`redirect_url:` in the front matter) are excluded up front — each one fails as «body too short».
- **C# indented with tabs** (xUnit.net, bUnit): `outline_tabs: true` in `ghcode-history`, otherwise a class stays one
  section. Check the indentation on a few files of every repository: `git show <tag>:<file> | sed 's/\t/→/g'`.
- **A blobless clone is for trees only.** `git grep` and `git ls-tree -l` in a `--filter=blob:none` clone fetch every
  blob with its own request and hang for minutes: the file sizes of a tag come from the tree through the API
  (`gh api repos/…/git/trees/<tag>?recursive=1`), a markup census from a full bare clone (tens of megabytes, a
  minute).
- **A site without tags in an instance with a version filter** (xunit.net, docs.nunit.org): the pages carry the
  product versions of the build day, and a filter for an older line (`nunit-3.13`) hides them. The prompt tells the
  model to search twice: with the version (API reference, packages, notes, code) and without it (the guides).
- **A release entry still under «Unreleased» on the release's own tag** (the FluentAssertions releases page at
  8.11.0): the versions the page does not name come from `ghreleases` with a `skip` that negates the list of missing
  ones (`^(?!(8\.11\.0|…)$)`); the rest of the GitHub releases would repeat the page.
- **A package that embeds generated wrappers of another library** (bunit.web: 12 thousand `Bunit.Web.AngleSharp`
  members over the AngleSharp DOM) and compiled-in polyfills and annotations (`System.*`, `Microsoft.CodeAnalysis.*`,
  `JetBrains.Annotations` — 81 types in every Shouldly line): count members by namespace before declaring and cut them
  off with `exclude_types`.
- **TypeScript with a four-space indent and no semicolons** (TypeORM: Prettier `semi: false`): `ghcode-history-ts`
  takes class members at two spaces and tells an overload signature from a method by its «;», so the whole
  EntityManager stayed one section, and every overload (`export function Column(): PropertyDecorator`) would become a
  section of its own. `indent: 4` and `join_same: true` split members at four spaces and fold neighbouring sections
  with the same heading into one. Count the headings of the largest class after the split.
- **A Docusaurus component of the site's own around tabs** (`<DatabaseTabs>` with `<DatabaseTab value="postgres">`,
  labels in `src/constants`): `docusaurus_tabs` knows only `<Tabs>`/`<TabItem>`, and the database names vanish. An
  MDX import spread over several lines (`import {` … `} from "@site/…"`) left its tail as the first line of the text,
  so the page title became a section and the file name the title — look at the first lines of the written documents.
  Flat pages that open with a list of links to their own anchors (a table of contents) gave every document an intro
  made of section names; drop it. Reader `ghdocs-history-typeorm` (`custom_tabs`, `drop_toc`).
- **Code and tests outweigh the documentation** (TypeORM: 94 % of 55 thousand excerpts): a query made of identifiers
  alone (`@Column nullable default`, `leftJoinAndSelect`) returns test entities and source files. The prompt tells the
  model to put the topic words of the page next to the names («Column options», «joining relations») and to search
  code by class and method: «as the model» went from 7 to 10 of 10, `max_per_doc` changed nothing.
- **A package README rewritten by the build only cosmetically** (TypeORM swaps ```` ```typescript ```` for
  ```` ```javascript ````): take the README from the publishing commit (`gitHead`) or the tag with `npm-readme`, and
  the tarball (2–3 MB each, 300 MB for 115 versions) only for versions with neither; one `slug_rewrite` rule gives
  both sources one key.
- **Library tests take the results of queries by API names** (dotnet-testing: tests repeat API names in method names
  and code dozens of times; for «xUnit1001 Fact methods cannot have parameters» three tests stood ahead of the rule
  page): the search field `demote` (`{"pattern": a regex over the test documents' names, "places": N}`) moves such
  sections N places down in the list of each search method. The number comes from a one-process measurement (here 5:
  own words 7 → 8, «as the model» 10 of 10, smoke green). `max_per_doc` is powerless here: every test is a separate
  document.
- **Switching from CPU to GPU in the middle of `vectors`**: stop only that process, replace `fastembed` and
  `onnxruntime` with `fastembed-gpu` and `onnxruntime-gpu[cuda,cudnn]` in the instance venv and start `vectors` again
  — it sees the points already computed as unchanged (here 76,800 of 153,060) and computes the rest; CPU and GPU
  numbers agree. Do not delete the collection.
- **Updating an archived instance** (dotnet-testing, second round: +119 sources): unpack the archive back into the
  instance folder and check the counts, add the sources, `refresh` only the new ones
  (`./df <instance> refresh <id…>`), build the API reference from packages fetched beforehand into the raw store with
  `build`, then `manifest`, the shared-key scan, `vectors` (it removes surplus points itself), `smoke`, `quality` and
  a comparison with the first round's numbers. The new archive gets a new name (`…-b.tar.gz`), is extracted separately
  and checked against the disk (`diff -r`); only then are the texts, `raw/` and the old archive deleted.
- **A release entry and a changelog entry of one tag share a name when the tag has no «v»** (`1.0.0`: `ghreleases`
  names the document after the tag, `changelog-regex` after the version): the shared-key scan found it on two
  libraries, and the fix cost a re-fetch of 171 documents. Release names with a `name_prefix` such as
  `<library>-release` do not collide with the changelog's.
- **Tags of one repository in different spellings** («V6.3.1», «v6.2.0», «5.1.0»): `ghreleases` does not parse a
  capital «V», so two sources — `ghreleases-stable` with `tag_prefix: "V"` and `ghreleases` with `skip: "^V"`; for
  documentation from tags one source is enough, because `tags` is «real tag → version label».
- **A package that changed its name** (AngleSharp.Scripting.JavaScript before 0.12 → AngleSharp.Js): tags, changelog
  and releases of one repository go in two sources with different version labels, cutting off the other's versions
  with a `skip` expression; the NuGet package of each name is its own source.
- **An analyzer rule page identical on the site and in the repository** (NUnit.Analyzers: docs.nunit.org and
  `documentation/` of the tags): the repository gets its own `name_prefix` (otherwise its README collides with the
  NuGet package README), `slug_rewrite` maps the rule pages' keys to the site's, and one family in `families` puts the
  section in the results once.

- **A release whose tag is one of many builds** (NuGet.Client: tags `7.9.0.83`, `6.14.3.1` are four-part build
  numbers, and the highest one is not always the release: of 56 versions checked, 11 differed): the commit of a release
  is the `repository commit` attribute in the nuspec of the NuGet package published for it
  (`v3-flatcontainer/<id>/<version>/<id>.nuspec`), and it becomes the key in `tags`. For two versions (5.7.2, 6.0.2) the
  commit from the nuspec is missing from the public repository (the API answers 422), for 4.x–5.10 the nuspec has none at
  all — take the build tag there; check every commit with `gh api repos/…/commits/<sha>` before `list`.
- **Root README files of different repositories in one instance** (NuGetGallery, `mcp/` of NuGet/Home): `ghdocs` names
  each one `readme`, and the intros of several READMEs share a section key — the shared-key scan before `vectors` found
  two. `ghdocs` has no `name_prefix`: the same file through `ghdocs-history` with `tags: {"<sha>": ""}` (no version),
  `files` and `name_prefix` gets its own key; for a file from a subfolder `exclude` is `^docs/`, not `/`.
- **An API reference behind dozens of tests of one class** (`FrameworkReducer.GetNearest`: the reference section is 33rd
  both by words and by meaning, ahead of it are over thirty methods of one test class): `demote` does nothing — it
  reorders only inside the list of depth `k`×6 = 30. A larger `fusion_depth` (40) lets the page into the list, and
  `max_per_doc: 3` stops one test file taking all the places: «as the model» 8 → 10 of 10 (`demote` 5–20 changed
  nothing, 30 helped only with depth from 40). Measure with one process that substitutes `profile.DEMOTE_PLACES`,
  `FUSION_DEPTH` and `MAX_PER_DOC`.
- **Packages whose XML is missing on part of the lines** (NuGet.* 6.5–6.11 and NuGet.VisualStudio 17.5–17.11 shipped
  without XML documentation, 6.12 brought it back): before declaring `nuget-xmldoc`, download the latest version of every
  minor line and note which carry XML (761 package × line pairs — a few minutes on five threads); the prompt names the
  lines that exist and tells the model to answer about a type of the missing ones from the nearest present line.
  Resource tables (`Strings`, `Resources`, `NuGetResources`, `AnalysisResources`, `SR`: 395 documents, the largest) go to
  `exclude_types`; documents that `build` no longer writes stay in `corpus/` as orphans — move them out, do not delete.
- **A `quality` target must exist in the newest edition of the page**: `VersionRange.Satisfies` has XML only in the
  1.0.7 edition (`SimpleVersion`), the members of later lines have no comments and did not become documents — the
  target was picked from the cache listing without looking at `versions`, and nothing in the current API could find it.
  Check the `p.versions` of every target; take a member present in the newest line (`Parse`).
- **All packages of an owner on nuget.org**:
  `https://azuresearch-usnc.nuget.org/query?q=owner:<name>&take=100&prerelease=false` (52 of 54 hits were ours; two
  from other products, `PoliteCaptcha` and `NuGet.Services.Build`, are dropped by `authors`); packages with only
  prereleases show only with `prerelease=true` and give `nuget-package` nothing. Products with their own numbering
  (NuGet.VisualStudio 17.x is the number of Visual Studio, NuGet.Mcp.Server 1.x, NuGet.Server 3.x) get a mark through
  `version_prefixes`, otherwise «1.4» is both the MCP server and NuGet 1.4.
- **When an update moves the tag of code and tests in a major line that is already taken** (e.g. 2.11.3 → 2.12.5): the
  revisions of files that exist only on the old tag become orphans. Move them to a scratchpad folder before `manifest`
  (never delete them); they do not go into the new archive and can be restored from the old tag on GitHub.

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
| `requirements.txt` | the instance venv contents; only when the instance needs a package outside the shared sets | write, listing just that package |
| `.env.example` | placeholders for the instance's own keys (`ANTHROPIC_API_KEY`, agent settings); `GITHUB_TOKEN` lives in the root `.env`; never commit a real `.env` | copy |
| `.gitignore` | `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `out/`, `index/passages.json` | copy |
| `.mcp.json` | HTTP server record for Claude Code | copy, change the port |
| `README.md` | what this domain is and where its docs come from | you |
| `UPDATE.md` | how to refresh this corpus when upstream changes | you |
| `corpus/` | the downloaded documents plus `index.json`, the passport | `refresh`, `manifest` |
| `index/` | the excerpt cache `passages.json` the server starts from; in archive mode it is committed compressed, `passages.json.gz` | built from `corpus/` by the first step that needs it |
| `raw/` | raw site responses for `build` without network, old versions in `raw/_old/`; never in git | `refresh`, `check`, `list` |
| `out/` | the search-mode decision, logs | `setup`, `serve` |
| `.venv/` | the instance's own virtual environment; without it `df` uses the shared one from `.venvs/` | step 1, only if needed |

## Step 1 · Folder and virtual environment

You never activate a venv: `df` picks the right one itself. By default a new instance has no venv of its own and
uses the shared environment (`.venvs/cpu` or `.venvs/gpu`, picked by `DF_VENV`; see the section «Shared environment»
of the root README), so the step is only the folder:

```
mkdir -p instances/<domain>/prompts
cp instances/react/.gitignore instances/react/.env.example instances/<domain>/
```

Build an own venv only when the domain needs a package that is not in `requirements/cpu.txt` and
`requirements/gpu.txt`. Then write a `requirements.txt` that lists just that package and build the venv. This is the
only action done from inside the instance folder, and from now on `df` takes the instance's own `.venv` whenever it
exists:

```
cd instances/<domain>
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cd ../..
```

**Known trap.** On some systems the packaged `python3` ships without the `venv` module. Use a Python that has it,
for example a conda interpreter: `/path/to/miniconda3/bin/python3 -m venv .venv`. Everything afterwards is
unaffected, because the venv is self-contained.

An own `.env` is needed only for private keys (`ANTHROPIC_API_KEY`, agent settings). The `GITHUB_TOKEN` line comes
from the root `.env`; the instance's own file, if it has that line, overrides it.

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
[ ] environment: shared venv ready (own .venv only for packages outside the shared sets)
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
- **Спершу середовище, потім корпус.** Першим — готове середовище: спільні venv (`.venvs/cpu`, `.venvs/gpu`) є, а в
  кореневому `.env` для джерел GitHub стоїть рядок `GITHUB_TOKEN` (анонімний API дає 60 звернень на годину). Власні
  venv і `.env` примірника потрібні лише у випадках кроку 1. До того `refresh`, `vectors`, `smoke` і `quality` не
  запускають.
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
  `tar --sort=name -czf <архів>.tar.gz -C instances/<домен> corpus raw` (`--sort=name` ставить подібні редакції
  сторінок поруч, і gzip стискає корпус із багатьма редакціями приблизно вдвічі краще); розпакувати в окрему теку й
  звірити з диском; лише тоді видалити файли `.txt` і `raw/`, стиснути `index/passages.json` у `passages.json.gz` і
  закомітити паспорт і кеш. Чинний архів у примірника один; перед оновленням його розпаковують назад.
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
- **Сторінки man в AsciiDoc** (Tesseract `doc/*.asc`: заголовки підкресленням, списки означень `'FILE'::`, буквальні
  блоки `....`, `<<ЯКІР,…>>`): читач `ghdocs-history-asciidoc`. Кожен термін списку означень — опція, параметр, код
  мови — стає підрозділом, а тип і змовчання — першим рядком тексту, не заголовком: жирними рядками всередині довгого
  OPTIONS, поділеного за довжиною, `--oem` не знаходився зовсім.
- **Сайт Sphinx, переписаний у MyST Markdown** (OCRmyPDF з 16.0: `:::{note}`, `:::{list-table}`,
  ```` ```{eval-rst} ````, `` {issue}`…` ``): читач `ghdocs-history-myst` разом із полем `sphinx` для `.rst` старих
  тегів. Файл нотаток випусків, що росте з кожним тегом, беруть один раз із найновішого тегу, а його копії в кожному
  тезі виключають.
- **`ghdocs-history` з `folders: [""]`** бере лише файли кореня навіть із `recursive`: вкладені теки (`tess3/`,
  `tess4/`) перелічують у `folders` поіменно. Це видно в `list` — рахуйте документи по теках.
- **Багато інструментів в одному примірнику** (doc-tools: poppler, ImageMagick, Ghostscript, qpdf, ExifTool і їхні
  обгортки): кожна мітка версії — з назвою інструмента (`poppler-26.10.0`, `imagemagick-7.1.1-47`, `ubuntu-24.04`).
  Інакше `version: "10.0"` змішує Ghostscript 10.0 з qpdf 10.0.
- **Проєкт на GitLab без дзеркала на GitHub** (poppler на gitlab.freedesktop.org): читач `gitlab-history` — названі
  теки кожного тегу через API GitLab за числовим id проєкту, документ на пару «шлях, blob»; тег без теки нічого не дає.
- **Сайт, що лежить у репозиторії готовим HTML** (ImageMagick `www/`, Ghostscript `doc/*.htm`, ExifTool `html/`): читач
  `ghdocs-history-html` з `start`/`end` для кожної епохи сайту, `drop` для реклами, скриптів та іконок SVG (їхній
  `<title>` «Twitter» інакше ставав назвою сторінки) і `title_strip`. Сторінки, що міняються раз на кілька випусків,
  беруть з останнього тегу кожної лінії, а не з кожного тегу.
- **Журнали змін десятка форматів**: читач `changelog-regex`, заголовок запису — вираз у `sources.json` з групами
  `v` і `d`. Сторінки man у mdoc (`file`) ідуть через `ghdocs-history-roff`; кожна опція розділу OPTIONS — підрозділ:
  сорок опцій одним фрагментом ховали `--mime-type`.
- **Сайтмап, де `<loc>` — голі шляхи** (gvisor.dev, Jekyll без `site.url`: `<loc>/blog/2023/06/27/directfs/</loc>`):
  `sitemap-html` порівнює `<loc>` з `within` як рядок, і не проходить жодна сторінка. Читач `sitemap-html-rel` спершу
  робить з кожного `<loc>` повну адресу відносно самого сайтмапа й лишає завершальну риску: голий хост без неї білий
  список не впізнає як сторінку сайту.
- **Розмітка, якої не знає звірений спільний читач** (`[TOC]` і теги Liquid Jekyll у `g3doc` gVisor, шапки TOML `+++`
  Hugo в архівному gvisor-website): тонкий модуль викликає `ghdocs_history` через обгортку контексту, чий `text()`
  чистить кожну сторінку `.md` до розбору (`ghdocs-history-jekyll`, `ghdocs-history-toml`). Нове поле в спільному
  читачі — ризик зсуву в кожному вже зібраному на ньому примірнику; з обгорткою їхні корпуси лишаються ті самі байт у
  байт.
- **`site` — лише для файлів, які сайт ще показує**: поле `site` читача `ghdocs-history` перелічує файли найновішого
  тегу поіменно, а не ловить усе виразом `g3doc/(.*)\.md`. Сторінка, що переїхала чи зникла
  (`g3doc/checkpoint_restore.md` 2019 року), і файл, якого сайт не показував (пропозиції, README прикладів), тоді
  цитують свій blob на GitHub у своєму тезі, а не мертву адресу сайту.
- **Довідник пакетів Go з pkg.go.dev** (netstack gVisor, `gvisor.dev/gvisor/pkg/tcpip`): читач `pkgsite` бере сторінку
  кореневого пакета й кожен підпакет із її таблиці «Directories»; документ — пакет з розділами Overview, Constants,
  Variables, Functions і Types, кожне оголошення — блоком коду Go, методи — підрозділами. Посилання на підпакети
  несуть у шляху `@<версія>` — її знімати: тоді один префікс `within` покриває всі, а посилання не старіють щодня.
  pkg.go.dev пригальмовує частих клієнтів відповіддю 429: читач тримає власну паузу (поле `pause`, типово 1,5 с), а
  `pause_sec` примірника для GitHub лишається нуль. Модуль без тегів показує псевдоверсію (`0.0.0-<час>-<коміт>`):
  його документи не мають версії випуску, і промпт мусить казати «шукати без версії».
- **Власний опис пакета з репозиторію APT** (`runsc` gVisor): читач `apt-packages` читає індекс `Packages` кожної
  архітектури (`dists/<набір>/<компонент>/binary-<архітектура>/Packages`) — документ на пакет з полями керування
  кожної архітектури й довгим описом. Такий репозиторій зазвичай тримає лише останню версію, тож джерело відповідає на
  «що сьогодні ставить `apt-get install`» (номер, розмір, контрольні суми), а не на історію; історія — з тегів.
- **Сайт Sphinx, що викладає кожну версію окремою текою** (docs.nvidia.com: `…/container-toolkit/1.20.1/`, `…/1.6.0/`):
  перелік версій (`versions1.json`) називає лише кілька найновіших — теки перебирають за номерами тегів репозиторію
  (`index.html` відповідає 200 чи 404). Читач `sphinx-html`: одне джерело з `{version}` в `url` і переліком `versions`;
  сторінки версії — обхід посилань `.html` від її стартової сторінки в межах її теки, бо набори сторінок різних років
  різні. Він знімає якорі заголовків (`#`, у старій темі — значок шрифту U+F0C1), бере мову коду з класу обгортки
  (`highlight-console`), підписує вкладки (sphinx-tabs тримає їхні назви в `<button>`, які розбір HTML викидає), кладе
  рядок таблиці в один рядок і вирізає `toctree`. Однаковий текст сторінки кількох версій — один документ з усіма ними.
- **Журнал, де зміни випуску записано під його передрелізами** (NVIDIA: «## v1.19.0» каже лише «Promote v1.19.0-rc.7
  to v1.19.0», а зміни — під «## v1.19.0-rc.1» … «-rc.7»): `skip` для `-rc` лишив би від випуску один рядок, а
  документів «1.19.0-rc.3» фільтр «1.19.0» не знаходить. Читач `changelog-prerelease` робить документ на сталий
  випуск, а його передрелізи — розділами; файл беруть один раз, із найновішого тегу.
- **Репозиторій APT, що тримає всі версії** (nvidia.github.io/libnvidia-container: 28 версій кожного пакета, від
  найстарішої): `apt-packages` бере назву з першого запису й назвав би найстарішу версію тією, що ставить
  `apt-get install`. Читач `apt-packages-versions`: найновіша — за номером, розділ «Versions» із залежностями кожної,
  мітки без ревізії Debian (`1.20.1-1` → `1.20.1`) і відбір `packages`.
- **Один файл — одне джерело.** Код команд усіх тегів і повний код найновішого тегу перетинаються в цьому тезі: з
  джерела найновішого тегу виключають те, що вже бере джерело всіх тегів (`^cmd/.+(?<!_test)\.go$`), інакше той самий
  файл стає двома документами під двома ключами й забирає два місця видачі. Так само модуль Go без пакета в корені на
  pkg.go.dev: корінь `pkgsite` — справжній пакет (`pkg/nvcdi`), решта публічних пакетів — у `pages`.
- **Порахувати фрагменти за джерелами до `vectors`.** Довідник API, що на кожній сторінці ендпоінта розгортає всі
  вкладені типи (platform.claude.com: `messages/create` — 140 КБ, а редакції Python і TypeScript повторюють його своїм
  синтаксисом), дав дві третини з 92 тисяч фрагментів; при п'яти фрагментах за секунду це п'ять годин векторів. Кеш
  `index/passages.json` з'являється раніше за першу точку: згрупувати його за джерелами, назвати користувачеві
  години, узгодити склад і лише тоді запускати. Сторінки, яких немає ні в `llms.txt`, ні в `sitemap.xml`, але є на
  сторінці-змісті в markdown (вкладені пункти, посилання від кореня сайту), бере читач `md-index`.
- **Зошити Jupyter** (claude-cookbooks): читач `ghdocs-history-ipynb` — клітинки markdown як є, код блоками мови
  зошита, з виводу лише текст, обрізаний до `output_chars`; картинки й HTML виводу відкидаються (з 22 МБ зошитів —
  2,6 МБ тексту). У `extensions` має бути `.ipynb`.
- **Репозиторій, що змінив вигляд тегів** (TypeScript SDK `v0.12.3` → `sdk-v0.12.4`, C# SDK `v11.0.0` →
  `Anthropic-v12.0.0`): перед оголошенням згрупувати теги за частиною до номера, інакше перші версії випадають. У
  монорепозиторії голий префікс `v` у `ghreleases-stable` ловить і `vertex-sdk-v…`: брати `v0.` з `version_prefix`
  `typescript-0.`.
- **Дві пастки читачів репозиторію.** `exclude: ["/"]` відкидає кожен шлях з текою, зокрема названий у `files` файл
  з підтеки (`packages/aws-sdk/README.md`) — виключати треба типове `^docs/`. `ghexamples` бере лише проєкти з
  `package.json`; приклади окремими файлами йдуть через `ghcode-history` чи `ghcode-history-ts` з
  `include: ["^examples/…"]`.
- **Сайт, що показує код мовою, яку вибрав читач** (docs.stripe.com: markdown-двійник сторінки віддає одну мову за
  `?lang=`): документ один на сторінку — текст один раз, під кожним розділом код інших мов з підписом (читач
  `stripe-md`). Документ на кожну мову повторив би текст сторінки сім разів і в індексі, і у векторах. Навіть так код
  зробив сайт шістьма десятими зі 114 тисяч фрагментів, а такі сторінки рахуються у вектори десь по п'ять фрагментів
  за секунду проти дев'яти для довідника API: години оцінювати за швидкістю кожного роду джерел, а не за однією
  середньою.
- **Сторінка, що є лише переліком варіантів** («This article has multiple variants»: Checkout чи Elements, iOS чи
  Android): замінити її варіантами, кожен — документ з назвою за підписом (`variants: true`). Сайтмап може нести
  сторінку двічі, звичайною адресою і з `.md`: адресу зводити до одного вигляду до того, як прибирати повтори.
  Сторінка, що падає під час складання переліку, має валити лише свій документ — один 404 коштував цілого переліку
  на 26 хвилин.
- **Тисячі тегів і кілька відомих файлів** (SDK Stripe: понад шість тисяч стабільних тегів проти п'яти тисяч звернень
  API за годину; дерева stripe-ios і stripe-java GitHub обрізає): файли брати напряму з raw.githubusercontent.com,
  що не витрачає ліміту API, — читач `ghraw-history`. Де SDK має сотні мінорних ліній, брати останній тег кожної.
- **Фрази, які `smoke` шукає в промптах** (`description_phrases`), порівнюються дослівно, з переносами рядків:
  переносячи рядки `prompts/search.txt`, тримати кожну з них в одному рядку («point by point», розірване
  переносом, провалило `smoke`).
- **Сайт документації, який DocFX збирає з відкритого репозиторію** (learn.microsoft.com: AspNetCore.Docs,
  AspNetDocs): читати джерело, а не сайт. Сайт малює сторінку JavaScript-ом і показує лише найновіші редакції, а
  репозиторій тримає кожну редакцію за монікерами (`monikerRange`, `:::moniker range`), з вставками й прикладами коду,
  частина яких — із сусідніх репозиторіїв (`~/../AspNetCore.Docs.Samples`), — читач `docfx`. Редакції, яких у
  джерелі вже немає, брати з останнього коміту, де їхні монікери ще були (ASP.NET Core 1.0–2.2 і 3.0). HTML-коментарі
  прибирати до розгортання вставок: вставка, що згадує саму себе в коментарі, зациклювалась.
- **Довідник API з самих пакетів** (.NET): пакет NuGet несе поруч зі збіркою XML-документацію — той текст, з якого
  згенеровано learn.microsoft.com/dotnet/api, — і пакет кожного випуску описує саме той випуск: читач
  `nuget-xmldoc`, `ref/` раніше за `lib/`. Типи спершу порахувати: внутрішні простори імен і класи ресурсів
  (`.Internal`, `CoreStrings`) дали близько десяти тисяч фрагментів без змісту (`exclude_types`); пакет без XML не
  дає нічого і йде з `sources.json`.
- **Продукти з власною нумерацією** (класичний ASP.NET: MVC 5.2, Web API 5.3, SignalR 2.4, Katana 4.2 в одному
  примірнику з ASP.NET Core 10.0): версія несе назву продукту префіксом (`mvc-5.2`; `version_prefixes` у
  `nuget-package`), а пакети з власними номерами (OData, SystemWebAdapters) не входять у джерела ліній, інакше OData
  8.x потрапляє в ASP.NET Core 8.0. Файл репозиторію без front matter бере назву з першого заголовка
  (`title_from: "heading"` у `ghdocs`); вбудований чужий код (googletest у `src/`) відрізає `exclude`. Посібники
  старих випусків у теках `older-versions*` поряд з новими дістають лінії за шляхом (`path_versions` у `docfx`):
  інакше посібник SignalR 1.x виходить вище за свого двійника 2.x, а пошук з версією не бачить жодного.
- **Монікери DocFX без номера версії** (learn.microsoft.com/sql: `sql-server-ver16`, `sql-server-linux-ver15`,
  `azuresqldb-current`, `fabric`): порядок версій продукту з імені не прочитати, тож поле `monikers` читача `docfx`
  дає його переліками, по одному на продукт, як їх показує `learn.microsoft.com/api/familyTrees/bymoniker/<монікер>`;
  `moniker` може бути переліком (редакція «SQL Server 2022» — те, що сайт показує і для `sql-server-ver16`, і для
  `sql-server-linux-ver16`). Монікери сторінки — її власний `monikerRange`, інакше останній збіг шаблону
  `build.fileMetadata.monikerRange` у `docfx.json`, інакше `moniker_range` групи, мінус `exclude_monikers`; шапка
  сторінки перемагає шаблон теки. Звірте правило із сайтом до завантаження: кожна сторінка несе
  `<meta name="monikers">` (64 випадкові сторінки — 64 збіги).
- **Версія, яку сайт уже прибрав** (SQL Server 2016 після кінця підтримки): у частковому клоні
  (`--filter=blob:none --shallow-since=…`) порахувати файли, чиї вирази монікерів її називають, на комітах першого
  батька гілки публікації; число стоїть рівно, а тоді падає з PR «Retire … monikers». Редакція — з останнього коміту
  перед цим PR, з `link: "github"`.
- **Редакції тих самих сторінок за продуктом** (Azure SQL Database, Managed Instance, Synapse, Fabric): спершу
  заміряти. Кожна редакція — тисячі документів, але текстом різняться близько сотні сторінок; однакові розділи
  одного запису `families` зливаються, і 85 тисяч документів десяти редакцій дали близько 120 тисяч неповторних
  фрагментів. Неповторні фрагменти рахувати потоковим скриптом до `vectors` — кількість документів про години мало
  що каже.
- **Величезний репозиторій DocFX — з клону**: `tools/seed_git_store.py` кладе текстові blob-и коміту, дерево у вигляді
  відповіді API і файли залежних репозиторіїв, на які сторінки посилаються «~/../<тека>/…» (неглибокі часткові
  клони за SHA коміту, `git fetch --depth=1 --filter=blob:none origin <sha>`); далі `build` пише 86 тисяч документів
  за хвилини. Залежні репозиторії (`repos`) закріплювати на комітах; приватні (`reusable-content`) лишаються поза
  примірником, і їхні вставки випадають.
- **Репозиторій, чиє повне дерево GitHub обрізає** (SupportArticles-docs): дерево однієї теки,
  `git/trees/<коміт>:support/sql?recursive=1`; `docfx` доповнює шляхи назад до кореня.
- **Сторінки YAML**: брати `YamlMime:FAQ` (питання — розділами; розділ «Ignored» сайт показує без заголовка),
  лишати Landing, Hub, змісти й переліки варіантів — там самі посилання (`yaml_pages: true`).
- **Передрелізи зі звичайним тегом** (mssql-jdbc публікує превʼю як `v13.5.1`, позначка лише на GitHub): поле
  `stable: true` читача `ghreleases`. У журналі змін група версії `changelog-regex` хай захоплює слово «Preview», а
  `skip` його відкидає — інакше запис превʼю приклеюється до сталого над ним.
- **Варіанти збірки в номері версії Maven** (`13.6.1.jre8`, `13.6.1.jre11`): поле `variant` читача `pkg-registry`,
  інакше кожна версія рахується передрелізом.
- **Теги образу контейнера** (`mcr.microsoft.com/v2/<образ>/tags/list`): читач `registry-tags` — документ на лінію
  (рік SQL Server) з CU, GDR і варіантами ОС за номером, а не за абеткою (`CU10` перед `CU2`).
- **Вектори: години вирішує порядок у пачці.** Модель доповнює кожну пачку з 32 фрагментів до найдовшого; у sql-docs
  майже кожні 32 фрагменти підряд мали один на 300–512 токенів, і за тієї самої середньої довжини, що в aspnetcore
  (155 токенів проти 139), вектори йшли 4,7 фрагмента за секунду замість 13. `server/setup` тепер рахує їх від
  коротких до довгих (×2,3 на процесорі, вектори ті самі до біта). З відеокартою NVIDIA `fastembed-gpu` і
  `onnxruntime-gpu[cuda,cudnn]` у власному venv примірника вмикають CUDA в `common/embed.py` (~500–800 фрагментів за
  секунду на RTX 2070 у WSL, косинус із процесорними ≥ 0,99999); venv зі звичайним `onnxruntime` цієї гілки не бачать.
- **Обхід тисяч сторінок** (`learn-archive`): сторінка, що переадресовує за межі білого списку, мусить падати сама,
  а не валити весь перелік (архів 2014 упав після тисячі сторінок). Поле `workers` тягне хвилю з N адрес черги разом
  і розбирає по черзі, тож перелік той самий до байта; `trust_store` (день) після перезапуску бере відповіді, що вже
  лежать у сховищі сирого, без звернення — потім його прибрати, інакше оновлення вже не побачить сайту.
- **Набір DocFX без монікерів** (learn.microsoft.com/ef: dotnet/EntityFramework.Docs): сайт показує одну редакцію,
  тож версії — знімки репозиторію: останній коміт `main` за тиждень після появи `x.y.0` у NuGet (у ці дні
  документацію доводять до випуску), посилання — на файли коміту в GitHub. Сайт, що до DocFX жив в іншому форматі
  (Sphinx до 31.10.2016), бере першу редакцію з першого коміту в новому форматі. Сторінки прев'ю наступного мажора
  виключають з усіх знімків: тижневий знімок останнього випуску вже може їх нести.
- **Код C# багатьох ліній**: `outline: ["csharp"]` у `ghcode-history` — член разом із `///` і атрибутами є розділом,
  тож незмінний метод сусідніх ліній — один фрагмент. Рахувати після поділу: код і тести efcore чотирнадцяти ліній —
  224 тисячі фрагментів (дві третини примірника), сервер тримає 5,6 ГБ; на відеокарті вектори — 11 хвилин.
- **Версії NuGet з метаданими збирання** (`9.0.15+MySQL9.7.0`): такого пакета немає в реєстрі semver1 зовсім (404) —
  поле `registration: "gz-semver2"` читача `nuget-package`.
- **Провайдери з офіційного переліку** беруть з усіх редакцій сторінки переліку (історія файла в голому клоні), а
  перш ніж оголошувати `nuget-xmldoc`, перевіряють, чи пакет кожної лінії несе XML: з 62 пакетів провайдерів XML мали
  18, і довідник API дістали лише вони.
- **Теги релізів з назвою продукту чи великою «V»** (`Google.Cloud.EntityFrameworkCore.Spanner-4.1.1`,
  `EFCore-13.0.0.0`, `ef-v0.5.0`, `V4.1.0.0`) `ghreleases` не розбирає — версія виходить порожня; їх бере
  `ghreleases-stable` з `tag_prefix`.
- **`ghdocs` знімає першу теку шляху**: `Sample/README.md` прикладу й кореневий `README.md` дістають одне ім'я
  «readme», і один документ затирає інший — такі теки йдуть окремими джерелами.
- **Сайт MkDocs, що вставляє приклади з тестів** (dotnet.testcontainers.org:
  `--8<-- "tests/…/PostgreSqlContainerTest.cs:UsePostgreSqlContainer"`, pymdownx.snippets з
  `dedent_subsections: true`): приклад — лише рядки між `// # --8<-- [start:Ім'я]` і `[end:Ім'я]`, шлях — від кореня репозиторію. Поля
  `snippet_sections: true` і `snippets: "."` читача `site-history` беруть іменований розділ без спільного відступу й
  прибирають рядки-мітки; без них такий рядок шукає файл «…cs:Ім'я», і приклад мовчки зникає. Теку тестів оголошують в
  `assets`, а після завантаження корпус перевіряють `grep`-ом на залишки `--8<--`. Поле `site` (як у `ghdocs-history`)
  перелічує сторінки найновішого тегу поіменно, і прибрані сторінки цитують свій файл на GitHub.
- **C# з відступом у два пробіли** (Testcontainers: простір імен блоком, тип на 2, члени на 4; тести — на 4): правило
  «тип плюс чотири» з `outline: ["csharp"]` лишало клас будівника на 28 тисяч символів одним розділом.
  `outline_indent: "auto"` бере відступ членів з першого рядка тіла типу. Після поділу перелічіть заголовки
  найбільшого класу кожного репозиторію.
- **Ідентифікатор NuGet, що змінив власника** (`Testcontainers` 0.0.1–0.0.2.107 2018–2019 років — інший автор,
  «Package Description», без README і XML; бібліотека дістала ідентифікатор з 2.0.0): перш ніж оголошувати пакет,
  подивіться в реєстрі `authors`, `projectUrl` і опис його найстаріших версій. Поле `since` читача `nuget-package`
  («пакет → найстаріша версія, що береться») відсікає їх, інакше вони стають лінією «0.0» продукту.
- **Довідник API бібліотеки, якої немає на learn.microsoft.com**: `nuget-xmldoc` посилає кожен тип на
  learn.microsoft.com/dotnet/api, де є лише пакети Microsoft, — `link: "nuget"` посилає його на сторінку тієї версії
  пакета на nuget.org, з якого тип прийшов.
- **Сторінка, перейменована не раз** (`examples/compose.md` → `examples/dind.md` → `dind/index.md`): git бачить кожен
  крок між сусідніми тегами (`git diff -M --stat <тег> <наступний> -- docs`, `git log --diff-filter=R --summary`);
  кожен попередник дістає власне правило `slug_rewrite` до найновішого імені. Сторінка зі старим ім'ям і іншим змістом
  (`api/compose.md` з 4.15, ComposeBuilder) лишається окремою.
- **Розмір до збирання.** Рядок паспорта коштує близько 600 байтів, фрагмент стисненого кешу — 120–200, а GitHub
  відхиляє файли від 100 МіБ. Сторінки кожного знімка й типи кожного пакета рахують до читачів (dotnet: 274 тисячі
  документів, паспорт 156 МБ, 562 тисячі фрагментів). Якщо не влазить, корпус, кеш і сховище сирого лишаються локально
  (`corpus/` і `index/` у `.gitignore` примірника, як у `patterns`), а архів поза WSL звіряють файл за файлом.
- **Репозиторій DocFX з docfx.json у корені** (dotnet/docs): «~/» — корінь репозиторію, поле `tilde_root: ""` читача
  `docfx`; `:::code … id="Assignment":::` вказує на `// <SnippetAssignment>` — `snippet_prefix: "Snippet"`. До повного
  збирання читають `.openpublishing.publish.config.json` кожного знімка: до 2020 року приклади жили в залежному
  репозиторії dotnet/samples, і код тих знімків зникає мовчки.
- **Довідник API сайту з ECMA XML** (dotnet/dotnet-api-docs): читач `ecma-xml`, документ на тип з тим самим ім'ям
  документа й заголовками членів, що в `nuget-xmldoc`, тож довідник сайту й XML пакетів згортаються одним записом
  `families`. `xml/FrameworksIndex` (десятки мегабайтів) читають виразами по байтах, а не деревом; `skip_monikers`
  відкидає типи й члени лише прев'ю; вставляються лише приклади C#.
- **Тисячі пакетів NuGet** (Microsoft.Extensions.*, 1 754 лінії пакетів): завантажити паралельно просто в сховище сирого
  (`rawstore.put`), записавши, які несуть XML, оголосити лише їх і збирати `build` без мережі — 2,5 хвилини замість
  години пауз `refresh`.
- **Факти лінії в метаданих випусків** (фаза й кінець підтримки) — лише в документі лінії: повторені в кожному з 285
  документів випусків, вони забирали всю видачу на «end of support».
- **Дві нумерації в одному примірнику** (.NET 8.0 і C# 8): мова несе `csharp-` (`csharp-7` — видання стандарту,
  `csharp-12.0` — специфікації можливостей). `ghdocs` бере `…/git/trees/ТЕГ:ТЕКА` для репозиторіїв, чиє повне дерево
  GitHub обрізає (dotnet/runtime, dotnet/roslyn), і кодує пробіли й «#» в іменах файлів.
- **Приклади коду залежних репозиторіїв сайту DocFX** (dotnet/docs до 2020 року: dotnet/samples лежав поруч як
  `samples/`): з `.openpublishing.publish.config.json` кожного знімка теку ведуть полем `repos` читача `docfx` на
  останній коміт того репозиторію перед днем знімка (якщо він сам тримав усе в підтеці — з суфіксом:
  `dotnet/samples/<sha>/samples`) і засівають з часткового клону лише файли, на які посилаються сторінки. Шляхам з
  пробілами потрібне `quote_paths: true`: ключі засіяного сховища кодовані, і без поля випадало 870 прикладів ADO.NET
  на кожен знімок.
- **`slug_rewrite` з файлів перенаправлень сайту DocFX** (`.openpublishing.redirection.*.json` усіх знімків і
  перейменування git між знімками): ланцюжком до сторінки, живої на найновішій гілці; пару лишають, лише коли сторінки
  ніколи не стоять в одному знімку й мають спільну назву чи кінець адреси, — близько третини перенаправлень веде на
  загальну сторінку розділу й відкидається. 1 880 правил з якорями додають до збирання кешу фрагментів дві хвилини.
- **Заміряти, перш ніж міняти читача**: один процес із завантаженим індексом (`server.quality` з підміненими
  `profile.MAX_PER_DOC`/`FUSION_DEPTH` чи з відсівом роду розділів обгорткою над `spec_mcp._dedup`) міряє кожен
  варіант за хвилини; у читач чи `config.json` іде лише те, що виграє.
- **Сайт на Docusaurus, що тримав кожну версію у своїй теці, а потім старі видаляв** (playwright.dev:
  `dotnet/versioned_docs/version-1.12` … `version-1.23`, далі лише `version-stable`): кожна тека береться з історії
  репозиторію в останній редакції — з батька коміту, що її видалив, або з коміту її останньої зміни, коли того батька
  вже взяла інша версія, — а `{version}` у `folders` бере на кожному коміті лише теку його версії, не всі версії, що
  лежать поруч. `slug_rewrite` з `version-1-X-` на `version-stable-` і одна родина у `families` зливають редакції
  сторінки. За часів `version-stable` знімок лінії — її останній коміт «roll to 1.X».
- **Той самий приклад у вкладках для кількох варіантів** (NUnit / MSTest / xUnit, npm / yarn / pnpm):
  `docusaurus_tabs: true` ставить підпис вкладки перед її змістом; без поля в тексті стоять кілька однакових блоків
  коду, і не видно, котрий для чого.
- **Документація .NET-репозиторіїв на Jekyll, kramdown і mdsnippets** (xunit.net, fluentassertions.com,
  nsubstitute.github.io, Shouldly): списки атрибутів `{: .issue-link }`, якорі заголовків `{ #id }`, теги Liquid
  `{% examplecode csharp %}` з прихованою заготовкою `{% requiredcode %}`, рядки «snippet source | anchor» під
  вставками mdsnippets — читач `ghdocs-history-kramdown`. Поле `jekyll_data` розгортає вставки
  `{% include … examples=site.data.… %}`, чиї дані лежать у YAML (поради FluentAssertions — понад сотня пар «як було —
  як краще»); файл даних, якого в тезі ще немає, Jekyll не малює, і вставка зникає, а не валить сторінку. До
  завантаження — перепис розмітки сторінок найновішого тегу (`git grep -o` по повному голому клону).
- **Сайт DocFX поза learn.microsoft.com** (docs.nunit.org, bunit.dev): той самий читач `docfx`; сайт із тегами —
  джерело на останній тег кожної мінорної лінії в одній родині, засіяне з клону (`seed_git_store.py`). Сторінка з
  самим `uid` у шапці бере назву з першого «# …» (`title_from: "heading"`), а сторінки-перенаправлення
  (`redirect_url:` у шапці) виключають заздалегідь — кожна дає збій «тіло куце».
- **Код C# з відступом табуляцією** (xUnit.net, bUnit): `outline_tabs: true` у `ghcode-history`, інакше клас лишається
  одним розділом. Відступ перевіряють на кількох файлах кожного репозиторію: `git show <тег>:<файл> | sed 's/\t/→/g'`.
- **Частковий клон — лише для дерев.** `git grep` і `git ls-tree -l` у клоні `--filter=blob:none` тягнуть кожен blob
  окремим запитом і зависають на хвилини: розміри файлів тегу дає дерево через API
  (`gh api repos/…/git/trees/<тег>?recursive=1`), а перепис розмітки — повний голий клон (десятки мегабайтів,
  хвилина).
- **Сайт без тегів у примірнику з фільтром версій** (xunit.net, docs.nunit.org): сторінки несуть версії продуктів на
  день збирання, і фільтр старої лінії (`nunit-3.13`) їх ховає. Промпт велить шукати двічі: з версією (довідник API,
  пакети, нотатки, код) і без неї (посібники).
- **Запис випуску, що на тезі випуску ще стоїть під «Unreleased»** (сторінка releases FluentAssertions на 8.11.0):
  версії, яких сторінка не називає, дає `ghreleases` зі `skip`-запереченням переліку відсутніх (`^(?!(8\.11\.0|…)$)`);
  решта релізів GitHub повторювала б сторінку.
- **Пакет зі згенерованими обгортками чужої бібліотеки** (bunit.web: 12 тисяч членів `Bunit.Web.AngleSharp` поверх DOM
  AngleSharp) і вкомпільовані поліфіли й анотації (`System.*`, `Microsoft.CodeAnalysis.*`, `JetBrains.Annotations` —
  81 тип на кожну лінію Shouldly): члени рахують за просторами імен до оголошення й відсікають `exclude_types`.
- **TypeScript з відступом у чотири пробіли й без «;»** (TypeORM: Prettier `semi: false`): `ghcode-history-ts` бере
  члени класу на двох пробілах і відрізняє сигнатуру перевантаження від методу за «;», тож увесь EntityManager лишався
  одним розділом, а кожне перевантаження (`export function Column(): PropertyDecorator`) ставало б окремим.
  `indent: 4` і `join_same: true` ділять члени на чотирьох пробілах і зливають сусідні розділи з однаковим заголовком.
  Після поділу перелічіть заголовки найбільшого класу.
- **Власний компонент сайту Docusaurus навколо вкладок** (`<DatabaseTabs>` з `<DatabaseTab value="postgres">`,
  підписи в `src/constants`): `docusaurus_tabs` знає лише `<Tabs>`/`<TabItem>`, і назви баз зникають. Імпорт MDX на
  кількох рядках (`import {` … `} from "@site/…"`) лишав хвіст першим рядком тексту, тож назва сторінки ставала
  розділом, а назвою документа — ім'я файла: дивіться на перші рядки записаних документів. Плоскі сторінки, що
  починаються переліком посилань на власні якорі (змістом), давали кожному документу вступ з назв розділів — його
  знімають. Читач `ghdocs-history-typeorm` (`custom_tabs`, `drop_toc`).
- **Код і тести переважують документацію** (TypeORM: 94 % з 55 тисяч фрагментів): запит самими іменами (`@Column
  nullable default`, `leftJoinAndSelect`) приносить сутності з тестів і файли коду. Промпт велить моделі ставити поруч
  з іменами слова теми сторінки («Column options», «joining relations»), а код шукати ім'ям класу й методу: «як
  модель» піднялося з 7 до 10 з 10, `max_per_doc` нічого не змінив.
- **README пакета, який збирання міняє лише косметично** (TypeORM міняє ```` ```typescript ```` на
  ```` ```javascript ````): README береться з коміту публікації (`gitHead`) чи тегу читачем `npm-readme`, а tarball
  (2–3 МБ кожен, 300 МБ на 115 версій) — лише для версій без того й другого; одне правило `slug_rewrite` дає обом
  джерелам один ключ.
- **Тести бібліотек забирають видачу запитів назвами API** (dotnet-testing: тести повторюють імена API в назвах
  методів і в коді десятки разів; на «xUnit1001 Fact methods cannot have parameters» три тести стояли попереду
  сторінки правила): поле пошуку `demote` (`{"pattern": вираз імені документа тестів, "places": N}`) відсуває такі
  розділи на N місць у списку кожного способу. Число — за заміром одним процесом (тут 5: своїми словами 7 → 8, «як
  модель» 10 із 10, smoke зелений). `max_per_doc` тут безсилий: кожен тест — окремий документ.
- **Перехід з процесора на відеокарту посеред `vectors`**: зупинити лише цей процес, у venv примірника замінити
  `fastembed` і `onnxruntime` на `fastembed-gpu` і `onnxruntime-gpu[cuda,cudnn]` і запустити `vectors` знову — уже
  пораховані точки він бачить незмінними (тут 76 800 з 153 060) і дораховує решту; числа процесора й відеокарти
  збігаються. Колекцію не видаляти.
- **Оновлення архівного примірника** (dotnet-testing, друга черга: +119 джерел): розпакувати архів назад у теку
  примірника й звірити лічильники, додати джерела, `refresh` лише нових (`./df <домен> refresh <id…>`), довідник API з
  пакетів, докачаних заздалегідь у сховище сирого, — `build`, далі `manifest`, скан ключів, `vectors` (він сам
  прибирає зайві точки), `smoke`, `quality` і порівняння з числами першої черги. Новий архів — під новою назвою
  (`…-b.tar.gz`), розпакований окремо й звірений з диском (`diff -r`); лише тоді видаляють тексти, `raw/` і старий
  архів.
- **Запис релізу й запис журналу змін одного тегу ділять ім'я, коли тег без «v»** (`1.0.0`: `ghreleases` називає
  документ за тегом, `changelog-regex` — за версією): скан спільних ключів знайшов це на двох бібліотеках, а
  виправлення коштувало перезавантаження 171 документа. Імена релізів з `name_prefix` на кшталт `<бібліотека>-release`
  не збігаються з іменами журналу.
- **Теги одного репозиторію в різних написаннях** («V6.3.1», «v6.2.0», «5.1.0»): `ghreleases` велику «V» не розбирає,
  тож два джерела — `ghreleases-stable` з `tag_prefix: "V"` і `ghreleases` зі `skip: "^V"`; для документації з тегів
  досить одного джерела, бо `tags` — це «справжній тег → мітка версії».
- **Пакет, що змінив ім'я** (AngleSharp.Scripting.JavaScript до 0.12 → AngleSharp.Js): теги, журнал і релізи одного
  репозиторію йдуть двома джерелами з різною міткою версії, відсікаючи чужі версії виразом `skip`; пакет NuGet кожного
  імені — окреме джерело.
- **Сторінка правила аналізатора, однакова на сайті й у репозиторії** (NUnit.Analyzers: docs.nunit.org і
  `documentation/` тегів): репозиторій дістає окремий `name_prefix` (інакше README збігається з README пакета NuGet),
  а `slug_rewrite` зводить ключі сторінок правил до сайтових і одна родина в `families` ставить розділ у видачі на
  одне місце.

- **Випуск, чий тег — один із багатьох збірок** (NuGet.Client: теги `7.9.0.83`, `6.14.3.1` — чотиричленні номери
  збірок, і найвищий не завжди випуск: з 56 звірених версій 11 розійшлися): коміт випуску — атрибут `repository commit`
  у nuspec пакета NuGet, опублікованого для цього випуску (`v3-flatcontainer/<id>/<версія>/<id>.nuspec`), і саме він
  стає ключем у `tags`. Для двох версій (5.7.2, 6.0.2) коміт з nuspec у публічному репозиторії відсутній (API
  відповідає 422), для 4.x–5.10 його в nuspec немає взагалі — там тег збірки; кожен коміт перевіряють
  `gh api repos/…/commits/<sha>` до `list`.
- **README кореня різних репозиторіїв в одному примірнику** (NuGetGallery, `mcp/` NuGet/Home): `ghdocs` називає кожен
  `readme`, і вступи кількох README ділять ключ розділу — скан спільних ключів перед `vectors` знайшов два. У `ghdocs`
  немає `name_prefix`: той самий файл через `ghdocs-history` з `tags: {"<sha>": ""}` (без версії), `files` і
  `name_prefix` дістає свій ключ; для файла з підтеки `exclude` — `^docs/`, а не `/`.
- **Довідник API за десятками тестів одного класу** (`FrameworkReducer.GetNearest`: розділ довідника — 33-й і по
  словах, і за змістом, а перед ним понад тридцять методів одного тестового класу): `demote` нічого не дає — він
  міняє порядок лише всередині списку глибини `k`×6 = 30. Більший `fusion_depth` (40) впускає сторінку в список, а
  `max_per_doc: 3` не дає одному файлові тестів зайняти всі місця: «як модель» 8 → 10 із 10 (`demote` 5–20 не змінив
  нічого, 30 помагав лише з глибиною від 40). Міряти одним процесом, що підміняє `profile.DEMOTE_PLACES`,
  `FUSION_DEPTH` і `MAX_PER_DOC`.
- **Пакети, чий XML бракує на частині ліній** (NuGet.* 6.5–6.11, NuGet.VisualStudio 17.5–17.11 вийшли без
  XML-документації, з 6.12 вона повернулась): до оголошення `nuget-xmldoc` завантажити останню версію кожної мінорної
  лінії й записати, які несуть XML (761 пара пакет × лінія — кілька хвилин на п'яти потоках); промпт називає наявні
  лінії й велить відповідати про тип відсутніх за найближчою наявною. Таблиці ресурсів (`Strings`, `Resources`,
  `NuGetResources`, `AnalysisResources`, `SR`: 395 документів, найбільші) — у `exclude_types`; документи, яких `build`
  уже не пише, лишаються в `corpus/` сиротами — їх виносять, а не видаляють.
- **Ціль `quality` мусить існувати в найновішій редакції сторінки**: `VersionRange.Satisfies` має XML лише в
  редакції 1.0.7 (`SimpleVersion`), члени пізніших ліній коментарів не мають і документами не стали — ціль обрано зі
  списку кешу, не глянувши на `versions`, і в чинному API її не знайшов би ніхто. Версії кожної цілі перевіряють у
  `p.versions`; брати член, що є в найновішій лінії (`Parse`).
- **Усі пакети власника на nuget.org**: `https://azuresearch-usnc.nuget.org/query?q=owner:<ім'я>&take=100&prerelease=false`
  (52 з 54 влучань — наші; два з інших продуктів, `PoliteCaptcha` і `NuGet.Services.Build`, відсіяно за `authors`);
  пакети лише з передрелізами видно тільки з `prerelease=true`, і `nuget-package` вони нічого не дають. Продукти з
  власною нумерацією (NuGet.VisualStudio 17.x — номер Visual Studio, NuGet.Mcp.Server 1.x, NuGet.Server 3.x) дістають
  мітку через `version_prefixes`, інакше «1.4» — і сервер MCP, і NuGet 1.4.
- **Коли оновлення зсуває тег коду й тестів у вже взятій мажорній лінії** (напр. 2.11.3 → 2.12.5): редакції файлів,
  що лишилися лише на старому тезі, стають сиротами. Їх виносять у теку scratchpad до `manifest` (не видаляють); у
  новий архів вони не йдуть і відновлюються зі старого тегу на GitHub.

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
| `requirements.txt` | склад venv примірника; лише коли примірникові потрібен пакет поза спільними наборами | написати, лише цей пакет |
| `.env.example` | заготовка для власних ключів примірника (`ANTHROPIC_API_KEY`, налаштування агента); `GITHUB_TOKEN` лежить у кореневому `.env`; справжній `.env` у git не потрапляє ніколи | копія |
| `.gitignore` | `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `out/`, `index/passages.json` | копія |
| `.mcp.json` | запис HTTP-сервера для Claude Code | копія, змінити порт |
| `README.md` | що це за домен і звідки береться його документація | ви |
| `UPDATE.md` | як оновлювати корпус, коли нагорі щось змінилося | ви |
| `corpus/` | завантажені документи плюс `index.json`, паспорт | `refresh`, `manifest` |
| `index/` | кеш фрагментів `passages.json`, з якого підіймається сервер; в архівному режимі в git іде стисненим, `passages.json.gz` | будується з `corpus/` першим кроком, якому потрібен |
| `raw/` | сирі відповіді сайтів для `build` без мережі, старі версії — у `raw/_old/`; у git не йде ніколи | `refresh`, `check`, `list` |
| `out/` | рішення про спосіб пошуку, журнали | `setup`, `serve` |
| `.venv/` | власне віртуальне середовище примірника; без нього `df` бере спільне з `.venvs/` | крок 1, лише за потреби |

## Крок 1 · Тека і venv

Venv активувати не треба ніколи: `df` сам обирає потрібний. Новий примірник за замовчуванням власного venv не має й
працює на спільному середовищі (`.venvs/cpu` або `.venvs/gpu`, обирає `DF_VENV`; розділ «Спільне середовище»
кореневого README), тож крок — лише тека:

```
mkdir -p instances/<домен>/prompts
cp instances/react/.gitignore instances/react/.env.example instances/<домен>/
```

Власний venv піднімайте, лише коли домену потрібен пакет, якого немає в `requirements/cpu.txt` і
`requirements/gpu.txt`. Тоді напишіть `requirements.txt` лише з цим пакетом і піднімайте venv. Це єдина дія, що
робиться зсередини теки примірника, і відтепер `df` бере власний `.venv` примірника, щойно він є:

```
cd instances/<домен>
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cd ../..
```

**Відома пастка.** На деяких системах пакетний `python3` іде без модуля `venv`. Тоді беріть інтерпретатор, у якого
він є, наприклад conda: `/шлях/до/miniconda3/bin/python3 -m venv .venv`. На все подальше це не впливає, бо venv
самодостатній.

Власний `.env` потрібен лише для приватних ключів (`ANTHROPIC_API_KEY`, налаштування агента). Рядок `GITHUB_TOKEN`
береться з кореневого `.env`; власний файл примірника, якщо в ньому цей рядок є, його перекриває.

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
[ ] середовище: спільний venv готовий (власний .venv — лише для пакетів поза спільними наборами)
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
- **Ambiente antes do corpus.** Primeiro o ambiente pronto: os venvs compartilhados (`.venvs/cpu`, `.venvs/gpu`)
  existem e o `.env` da raiz tem uma linha `GITHUB_TOKEN` para fontes do GitHub (a API anônima permite 60 requisições
  por hora). O venv e o `.env` próprios da instância só são necessários nos casos do passo 1. Antes disso não rode
  `refresh`, `vectors`, `smoke` nem `quality`.
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
  `tar --sort=name -czf <arquivo>.tar.gz -C instances/<domínio> corpus raw` (`--sort=name` coloca revisões parecidas
  de uma página lado a lado, e o gzip comprime um corpus com muitas revisões cerca de duas vezes melhor); descompacte
  numa pasta à parte e compare com o disco; só então apague os `.txt` e `raw/`, comprima `index/passages.json` em
  `passages.json.gz` e faça commit do passaporte e do cache. Um arquivo vigente por instância; antes de uma
  atualização, descompacte-o de volta.
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
- **Páginas man em AsciiDoc** (Tesseract `doc/*.asc`: títulos sublinhados, listas de definição `'FILE'::`, blocos
  literais `....`, `<<ÂNCORA,…>>`): leitor `ghdocs-history-asciidoc`. Cada termo da lista de definição — uma opção, um
  parâmetro, um código de idioma — vira uma subseção, e o tipo e o padrão viram a primeira linha do texto, não o
  título: como linhas em negrito dentro de um OPTIONS longo cortado por tamanho, `--oem` não era encontrado.
- **Um site Sphinx reescrito em MyST Markdown** (OCRmyPDF a partir do 16.0: `:::{note}`, `:::{list-table}`,
  ```` ```{eval-rst} ````, `` {issue}`…` ``): leitor `ghdocs-history-myst` junto com o campo `sphinx` para os `.rst`
  das tags antigas. O arquivo de notas de versão que cresce a cada tag é lido uma vez, da tag mais nova, e as cópias
  em cada tag são excluídas.
- **`ghdocs-history` com `folders: [""]`** pega só os arquivos da raiz mesmo com `recursive`: as subpastas (`tess3/`,
  `tess4/`) são listadas em `folders` uma a uma. O `list` mostra isso — conte os documentos por pasta.
- **Muitas ferramentas numa instância** (doc-tools: poppler, ImageMagick, Ghostscript, qpdf, ExifTool e seus
  wrappers): cada rótulo de versão leva o nome da ferramenta (`poppler-26.10.0`, `imagemagick-7.1.1-47`,
  `ubuntu-24.04`). Senão `version: "10.0"` mistura Ghostscript 10.0 com qpdf 10.0.
- **Um projeto no GitLab sem espelho no GitHub** (poppler em gitlab.freedesktop.org): leitor `gitlab-history` — as
  pastas nomeadas de cada tag pela API do GitLab com o id numérico do projeto, um documento por par «caminho, blob»;
  uma tag sem a pasta não dá nada.
- **Um site guardado como HTML no repositório** (ImageMagick `www/`, Ghostscript `doc/*.htm`, ExifTool `html/`):
  leitor `ghdocs-history-html` com `start`/`end` por era do site, `drop` para anúncios, scripts e ícones SVG (o
  `<title>` «Twitter» deles virava o título da página) e `title_strip`. Páginas que mudam uma vez a cada vários
  lançamentos vêm da última tag de cada linha, não de cada tag.
- **Changelogs em uma dúzia de formatos**: leitor `changelog-regex`, o cabeçalho da entrada é uma regex no
  `sources.json` com os grupos `v` e `d`. Páginas man em mdoc (`file`) passam por `ghdocs-history-roff`; cada opção de
  OPTIONS vira uma subseção — quarenta opções num só trecho escondiam `--mime-type`.
- **Um sitemap cujos `<loc>` são caminhos sem host** (gvisor.dev, Jekyll sem `site.url`:
  `<loc>/blog/2023/06/27/directfs/</loc>`): o `sitemap-html` compara `<loc>` com `within` como texto, e nenhuma página
  passa. O leitor `sitemap-html-rel` primeiro transforma cada `<loc>` em endereço completo relativo ao próprio sitemap
  e mantém a barra final — o host sem ela não é reconhecido como página do site.
- **Marcação que um leitor compartilhado já conferido não conhece** (`[TOC]` e tags Liquid do Jekyll no `g3doc` do
  gVisor, front matter TOML `+++` do Hugo no gvisor-website arquivado): um módulo fino chama `ghdocs_history` através
  de um invólucro do contexto cujo `text()` limpa cada página `.md` antes da análise (`ghdocs-history-jekyll`,
  `ghdocs-history-toml`). Um campo novo no leitor compartilhado seria risco de desvio em cada instância já montada
  sobre ele; com o invólucro o corpus delas fica igual byte a byte.
- **`site` só para arquivos que o site ainda mostra**: o campo `site` do `ghdocs-history` lista os arquivos da tag mais
  nova um a um, em vez de pegar tudo com `g3doc/(.*)\.md`. Uma página que mudou de lugar ou sumiu
  (`g3doc/checkpoint_restore.md` de 2019) e um arquivo que o site nunca mostrou (propostas, READMEs de exemplos) então
  citam o seu blob no GitHub na sua própria tag, não um endereço morto do site.
- **Referência de pacotes Go do pkg.go.dev** (netstack do gVisor, `gvisor.dev/gvisor/pkg/tcpip`): o leitor `pkgsite`
  pega a página do pacote raiz e cada subpacote da sua tabela «Directories»; um documento por pacote com Overview,
  Constants, Variables, Functions e Types, cada declaração como bloco de código Go, métodos como subseções. Os links
  dos subpacotes trazem `@<versão>` no caminho — retire-a: assim um só prefixo `within` cobre todos e os links não
  envelhecem a cada dia. O pkg.go.dev freia clientes frequentes com 429: o leitor mantém a sua própria pausa (campo
  `pause`, 1,5 s por padrão), enquanto o `pause_sec` da instância para o GitHub continua zero. Um módulo sem tags
  mostra uma pseudoversão (`0.0.0-<hora>-<commit>`): os documentos dele não têm versão de lançamento, e o prompt
  precisa dizer «buscar sem versão».
- **A descrição do próprio gerenciador de pacotes, de um repositório APT** (`runsc` do gVisor): o leitor
  `apt-packages` lê o índice `Packages` de cada arquitetura
  (`dists/<suíte>/<componente>/binary-<arquitetura>/Packages`) — um documento por pacote com os campos de controle de
  cada arquitetura e a descrição longa. Um repositório assim costuma manter só a última versão, então a fonte responde
  «o que o `apt-get install` instala hoje» (número, tamanho, somas de verificação), não o histórico; o histórico vem
  das tags.
- **Um site Sphinx que publica cada versão numa pasta própria** (docs.nvidia.com: `…/container-toolkit/1.20.1/`,
  `…/1.6.0/`): a lista de versões (`versions1.json`) cita só as mais novas — teste as pastas pelos números das tags do
  repositório (`index.html` responde 200 ou 404). Leitor `sphinx-html`: uma fonte com `{version}` na `url` e a lista
  `versions`; as páginas de uma versão são uma varredura dos links `.html` a partir da página inicial dentro da pasta
  dela, porque os conjuntos de páginas mudam com os anos. Ele tira as âncoras dos títulos (`#`, ou um ícone de fonte
  U+F0C1 no tema antigo), pega a linguagem do código da classe do invólucro (`highlight-console`), rotula as abas (o
  sphinx-tabs guarda os nomes em `<button>`, que a análise do HTML descarta), mantém cada linha de tabela numa linha e
  corta o `toctree`. O texto idêntico de uma página em várias versões vira um documento com todas elas.
- **Um changelog que lista as mudanças de uma versão sob os seus release candidates** (NVIDIA: «## v1.19.0» diz só
  «Promote v1.19.0-rc.7 to v1.19.0»; as mudanças ficam sob «## v1.19.0-rc.1» … «-rc.7»): `skip` para `-rc` deixaria
  uma linha por versão, e documentos rotulados «1.19.0-rc.3» não são achados pelo filtro «1.19.0». O leitor
  `changelog-prerelease` faz um documento por versão estável com os candidatos como seções; leia o arquivo uma vez, da
  tag mais nova.
- **Um repositório APT que guarda todas as versões** (nvidia.github.io/libnvidia-container: 28 versões por pacote, da
  mais antiga para a mais nova): o `apt-packages` tira o título da primeira entrada e chamaria a versão mais antiga de
  aquela que o `apt-get install` instala. Leitor `apt-packages-versions`: a mais nova pelo número, uma seção
  «Versions» com as dependências de cada uma, rótulos sem a revisão Debian (`1.20.1-1` → `1.20.1`) e o filtro
  `packages`.
- **Um arquivo — uma fonte.** O código dos comandos de todas as tags e o código completo da tag mais nova se
  sobrepõem nessa tag: exclua da fonte da tag mais nova o que a fonte de todas as tags já pega
  (`^cmd/.+(?<!_test)\.go$`), senão o mesmo arquivo vira dois documentos com duas chaves e ocupa dois lugares no
  resultado. Do mesmo modo, um módulo Go sem pacote na raiz no pkg.go.dev: a raiz do `pkgsite` é um pacote de verdade
  (`pkg/nvcdi`), os outros pacotes públicos vão em `pages`.
- **Conte os trechos por fonte antes de `vectors`.** Uma referência de API que expande todos os tipos aninhados em
  cada página de endpoint (platform.claude.com: `messages/create` tem 140 KB, e as edições Python e TypeScript a
  repetem com a própria sintaxe) deu dois terços de 92 mil trechos; a uns cinco trechos por segundo, são cinco horas
  de vetores. O cache `index/passages.json` existe antes do primeiro ponto: agrupe-o por fonte, diga ao usuário as
  horas, combine o escopo e só então comece. Páginas ausentes de `llms.txt` e de `sitemap.xml`, mas listadas numa
  página de índice em markdown (itens aninhados, links a partir da raiz do site), vêm pelo leitor `md-index`.
- **Notebooks Jupyter** (claude-cookbooks): leitor `ghdocs-history-ipynb` — células markdown como estão, código em
  blocos da linguagem do notebook, da saída só o texto, cortado em `output_chars`; imagens e HTML da saída são
  descartados (22 MB de notebooks deram 2,6 MB de texto). `extensions` precisa incluir `.ipynb`.
- **Um repositório que mudou o formato das tags** (TypeScript SDK `v0.12.3` → `sdk-v0.12.4`, C# SDK `v11.0.0` →
  `Anthropic-v12.0.0`): agrupe as tags pela parte antes do número antes de declarar, senão as primeiras versões ficam
  de fora. Num monorepositório o prefixo `v` sozinho em `ghreleases-stable` também pega `vertex-sdk-v…`: use `v0.` com
  `version_prefix` `typescript-0.`.
- **Duas armadilhas dos leitores de repositório.** `exclude: ["/"]` descarta todo caminho com pasta, inclusive um
  arquivo de subpasta nomeado em `files` (`packages/aws-sdk/README.md`) — exclua o padrão `^docs/`. `ghexamples` pega
  só projetos com `package.json`; exemplos em arquivos soltos vão por `ghcode-history` ou `ghcode-history-ts` com
  `include: ["^examples/…"]`.
- **Um site que mostra o código na linguagem escolhida pelo leitor** (docs.stripe.com: o gêmeo markdown da página dá
  uma linguagem por `?lang=`): um documento por página — o texto uma vez, sob cada seção o código das outras
  linguagens com um rótulo (leitor `stripe-md`). Um documento por linguagem repetiria o texto da página sete vezes no
  índice e nos vetores. Mesmo assim o código fez do site 61% de 114 mil trechos, e essas páginas viram vetores a uns
  cinco trechos por segundo contra nove de uma referência de API: estime as horas pela taxa de cada tipo de fonte, não
  por uma média só.
- **Uma página que é só uma lista de variantes** ("This article has multiple variants": Checkout ou Elements, iOS ou
  Android): troque-a pelas variantes, cada uma um documento com o nome do seu rótulo (`variants: true`). O sitemap
  pode listar uma página duas vezes, simples e com `.md`: normalize o endereço antes de tirar repetições. Uma página
  que falha enquanto a lista é montada deve derrubar só o próprio documento — um 404 custou uma listagem inteira de
  26 minutos.
- **Milhares de tags, poucos arquivos conhecidos** (SDKs da Stripe: mais de seis mil tags estáveis contra uma cota de
  cinco mil chamadas de API por hora; o GitHub trunca as árvores de stripe-ios e stripe-java): leia os arquivos
  direto de raw.githubusercontent.com, que não gasta cota de API — leitor `ghraw-history`. Onde um SDK tem centenas
  de linhas menores, pegue a última tag de cada linha.
- **As frases que o `smoke` procura nos prompts** (`description_phrases`) são comparadas literalmente, com quebras de
  linha: ao requebrar `prompts/search.txt`, mantenha cada uma numa linha só ("point by point" partido por uma quebra
  reprovou o `smoke`).
- **Um site de documentação que o DocFX monta a partir de um repositório aberto** (learn.microsoft.com:
  AspNetCore.Docs, AspNetDocs): leia a fonte, não o site. O site desenha a página com JavaScript e mostra só as
  edições mais novas, enquanto o repositório guarda cada edição atrás de monikers (`monikerRange`,
  `:::moniker range`), com inclusões e trechos de código, parte deles de repositórios vizinhos
  (`~/../AspNetCore.Docs.Samples`) — leitor `docfx`. Edições que a fonte já não tem vêm do último commit em que seus monikers ainda existiam (ASP.NET Core
  1.0–2.2 e 3.0). Tire os comentários HTML antes de expandir as inclusões: uma inclusão que cita a si mesma num
  comentário entrou em laço.
- **Uma referência de API tirada dos próprios pacotes** (.NET): um pacote NuGet traz, ao lado do assembly, a
  documentação XML — o texto de que learn.microsoft.com/dotnet/api é gerado — e o pacote de cada versão descreve
  exatamente essa versão: leitor `nuget-xmldoc`, `ref/` antes de `lib/`. Conte os tipos primeiro: namespaces internos
  e classes de recursos (`.Internal`, `CoreStrings`) deram uns dez mil trechos sem conteúdo (`exclude_types`); um
  pacote sem XML não dá nada e sai do `sources.json`.
- **Produtos com numeração própria** (ASP.NET clássico: MVC 5.2, Web API 5.3, SignalR 2.4, Katana 4.2 numa instância
  com o ASP.NET Core 10.0): a versão leva o produto como prefixo (`mvc-5.2`; `version_prefixes` no `nuget-package`), e
  pacotes com números próprios (OData, SystemWebAdapters) ficam fora das fontes por linha, senão o OData 8.x cai no
  ASP.NET Core 8.0. Um arquivo do repositório sem front matter tira o título do primeiro cabeçalho
  (`title_from: "heading"` no `ghdocs`); código alheio embutido (googletest em `src/`) é cortado com `exclude`.
  Guias de versões antigas em pastas `older-versions*` ao lado das novas recebem suas linhas pelo caminho
  (`path_versions` no `docfx`): senão o guia do SignalR 1.x sai acima do seu gêmeo 2.x, e uma busca com versão não
  acha nenhum.
- **Monikers DocFX sem número de versão** (learn.microsoft.com/sql: `sql-server-ver16`, `sql-server-linux-ver15`,
  `azuresqldb-current`, `fabric`): a ordem das versões de um produto não se lê do nome, então o campo `monikers` do
  leitor `docfx` a dá em listas, uma por produto, como `learn.microsoft.com/api/familyTrees/bymoniker/<moniker>` as
  mostra; `moniker` pode ser uma lista (a edição "SQL Server 2022" é o que o site mostra tanto para
  `sql-server-ver16` quanto para `sql-server-linux-ver16`). Os monikers de uma página são o seu próprio
  `monikerRange`, senão o último glob que casa em `build.fileMetadata.monikerRange` do `docfx.json`, senão o
  `moniker_range` do grupo, menos `exclude_monikers`; o cabeçalho da página vence o glob da pasta. Confira a regra
  com o site antes de baixar: toda página traz `<meta name="monikers">` (64 páginas aleatórias, 64 acertos).
- **Uma versão que o site já retirou** (SQL Server 2016 após o fim do suporte): num clone parcial
  (`--filter=blob:none --shallow-since=…`) conte os arquivos cujas expressões de moniker a nomeiam nos commits de
  primeiro pai do branch de publicação; a contagem fica estável e cai com um PR «Retire … monikers». A edição vem do
  último commit antes desse PR, com `link: "github"`.
- **Edições das mesmas páginas por produto** (Azure SQL Database, Managed Instance, Synapse, Fabric): meça antes.
  Cada edição tinha milhares de documentos, mas só uma centena de páginas difere no texto; seções idênticas de uma
  entrada de `families` se fundem, e 85 mil documentos de dez edições deram cerca de 120 mil trechos distintos.
  Conte os trechos distintos com um script em fluxo antes de `vectors` — o número de documentos diz pouco das horas.
- **Um repositório DocFX enorme a partir de um clone**: `tools/seed_git_store.py` grava os blobs de texto do commit,
  a árvore no formato da API e os arquivos dos repositórios dependentes que as páginas citam como `~/../<pasta>/…`
  (clones parciais rasos buscados pelo SHA, `git fetch --depth=1 --filter=blob:none origin <sha>`); depois o `build`
  escreve 86 mil documentos em minutos. Fixe os repositórios dependentes (`repos`) em commits; os privados
  (`reusable-content`) ficam de fora, e seus includes caem.
- **Um repositório cuja árvore completa o GitHub trunca** (SupportArticles-docs): a árvore de uma pasta,
  `git/trees/<commit>:support/sql?recursive=1`; o `docfx` completa os caminhos de volta à raiz.
- **Páginas YAML**: pegue `YamlMime:FAQ` (perguntas como seções; uma seção chamada «Ignored» não tem título no
  site), deixe Landing, Hub, sumários e listas de variantes — são só links (`yaml_pages: true`).
- **Pré-lançamentos com tag comum** (o mssql-jdbc publica previews como `v13.5.1`, marcados só no GitHub): campo
  `stable: true` do `ghreleases`. Num changelog, deixe o grupo de versão do `changelog-regex` capturar a palavra
  «Preview» e o `skip` descartá-la, ou a entrada de preview gruda na entrada estável acima.
- **Variantes de build dentro de uma versão Maven** (`13.6.1.jre8`, `13.6.1.jre11`): campo `variant` do
  `pkg-registry`, senão toda versão conta como pré-lançamento.
- **Tags de imagem de contêiner** (`mcr.microsoft.com/v2/<imagem>/tags/list`): leitor `registry-tags` — um documento
  por linha (o ano do SQL Server) com CU, GDR e variantes de SO ordenados por número, não alfabeticamente (`CU10`
  antes de `CU2`).
- **Vetores: a ordem do lote decide as horas.** O modelo completa cada lote de 32 trechos até o mais longo; no
  sql-docs quase todo grupo de 32 trechos seguidos tinha um de 300–512 tokens, e com o mesmo comprimento médio do
  aspnetcore (155 tokens contra 139) os vetores iam a 4,7 trechos por segundo em vez de 13. O `server/setup` agora os
  calcula do mais curto ao mais longo (×2,3 na CPU, os mesmos vetores bit a bit). Com placa NVIDIA, `fastembed-gpu` e
  `onnxruntime-gpu[cuda,cudnn]` no venv da própria instância ligam o CUDA no `common/embed.py` (~500–800 trechos por
  segundo numa RTX 2070 no WSL, cosseno com os vetores de CPU ≥ 0,99999); venvs com o `onnxruntime` comum nunca entram
  nesse ramo.
- **Uma varredura de milhares de páginas** (`learn-archive`): uma página que redireciona para fora da lista branca
  deve falhar sozinha, não derrubar a listagem inteira (o arquivo 2014 caiu depois de mil páginas). O campo `workers`
  busca uma onda de N endereços da fila de uma vez e os processa em ordem, então a listagem é idêntica byte a byte;
  `trust_store` (um dia), após um reinício, reaproveita as respostas que já estão no armazenamento bruto sem
  requisição — retire-o depois, ou as atualizações nunca mais verão o site.
- **Um docset DocFX sem monikers** (learn.microsoft.com/ef: dotnet/EntityFramework.Docs): o site mostra uma só
  edição, então as versões são instantâneos do repositório — o último commit de `main` uma semana depois de `x.y.0`
  chegar ao NuGet (nessa semana a documentação é concluída para o lançamento), com links para os arquivos do commit no
  GitHub. Um site que antes do DocFX vivia em outro formato (Sphinx até 31.10.2016) tira a primeira edição do primeiro
  commit no formato novo. As páginas de prévia do próximo major são excluídas de todos os instantâneos: o instantâneo
  da semana do último lançamento já pode trazê-las.
- **Código C# de muitas linhas**: `outline: ["csharp"]` no `ghcode-history` — um membro com seu `///` e atributos é
  uma seção, então um método inalterado de linhas vizinhas é um só trecho. Conte depois da divisão: o código e os
  testes do efcore em catorze linhas são 224 mil trechos (dois terços da instância) e o servidor ocupa 5,6 GB; na GPU
  os vetores levaram 11 minutos.
- **Versões NuGet com metadados de build** (`9.0.15+MySQL9.7.0`): um pacote assim nem existe no registro semver1
  (404) — campo `registration: "gz-semver2"` do `nuget-package`.
- **Provedores de uma lista oficial** vêm de todas as revisões da página da lista (o histórico do arquivo num clone
  nu), e antes de declarar `nuget-xmldoc` confira se o pacote de cada linha traz XML: dos 62 pacotes de provedores, 18
  traziam, e só eles ganharam referência de API.
- **Tags de release com nome de produto ou «V» maiúsculo** (`Google.Cloud.EntityFrameworkCore.Spanner-4.1.1`,
  `EFCore-13.0.0.0`, `ef-v0.5.0`, `V4.1.0.0`) o `ghreleases` não interpreta — a versão sai vazia; use
  `ghreleases-stable` com `tag_prefix`.
- **O `ghdocs` tira a primeira pasta do caminho**: o `Sample/README.md` de um exemplo e o `README.md` da raiz ganham o
  mesmo nome «readme», e um documento sobrescreve o outro — essas pastas vão em fontes separadas.
- **Um site MkDocs que insere os exemplos a partir dos testes** (dotnet.testcontainers.org:
  `--8<-- "tests/…/PostgreSqlContainerTest.cs:UsePostgreSqlContainer"`, pymdownx.snippets com
  `dedent_subsections: true`): o exemplo são só as linhas entre `// # --8<-- [start:Nome]` e `[end:Nome]`, o caminho parte da raiz do repositório. Os
  campos `snippet_sections: true` e `snippets: "."` do `site-history` pegam a seção nomeada sem o recuo comum e
  removem as linhas-marcador; sem eles essa linha procura um arquivo «…cs:Nome» e o exemplo some calado. Declare a
  pasta de testes em `assets` e, depois do download, procure com `grep` restos de `--8<--` no corpus. O campo `site`
  (como no `ghdocs-history`) lista pelo nome as páginas da tag mais nova, e as páginas removidas citam o próprio
  arquivo no GitHub.
- **C# com recuo de dois espaços** (Testcontainers: namespace em bloco, tipo em 2, membros em 4; os testes em 4): a
  regra «tipo mais quatro» do `outline: ["csharp"]` deixava uma classe builder de 28 mil caracteres como uma só seção.
  `outline_indent: "auto"` tira o recuo dos membros da primeira linha do corpo do tipo. Depois da divisão, liste os
  títulos da maior classe de cada repositório.
- **Um id NuGet que trocou de dono** (`Testcontainers` 0.0.1–0.0.2.107, de 2018–2019, são de outro autor, «Package
  Description», sem README nem XML; a biblioteca recebeu o id na 2.0.0): antes de declarar um pacote, veja no registro
  `authors`, `projectUrl` e a descrição das versões mais antigas. O campo `since` do `nuget-package` («pacote → versão
  mais antiga que entra») as corta; sem ele viram uma linha «0.0» do produto.
- **A referência de API de uma biblioteca que não está no learn.microsoft.com**: o `nuget-xmldoc` aponta cada tipo
  para learn.microsoft.com/dotnet/api, que só conhece os pacotes da Microsoft — `link: "nuget"` aponta para a página
  da versão do pacote no nuget.org de onde o tipo veio.
- **Uma página renomeada mais de uma vez** (`examples/compose.md` → `examples/dind.md` → `dind/index.md`): o git vê
  cada passo entre tags vizinhas (`git diff -M --stat <tag> <seguinte> -- docs`, `git log --diff-filter=R --summary`);
  cada predecessor ganha a própria regra `slug_rewrite` para o nome mais novo. Uma página com o nome antigo e conteúdo
  diferente (`api/compose.md` da 4.15, ComposeBuilder) fica à parte.
- **Tamanho antes da montagem.** Uma linha do passaporte custa uns 600 bytes, um fragmento do cache comprimido 120–200,
  e o GitHub recusa arquivos a partir de 100 MiB. Conte as páginas de cada snapshot e os tipos de cada pacote antes de
  escrever leitores (dotnet: 274 mil documentos, passaporte de 156 MB, 562 mil fragmentos). Se não couber, o corpus, o
  cache e o armazém do bruto ficam só locais (`corpus/` e `index/` no `.gitignore` da instância, como em `patterns`),
  com um arquivo fora do WSL conferido arquivo por arquivo.
- **Um repositório DocFX com docfx.json na raiz** (dotnet/docs): `~/` é a raiz do repositório — campo
  `tilde_root: ""` do `docfx`; `:::code … id="Assignment":::` aponta para `// <SnippetAssignment>` —
  `snippet_prefix: "Snippet"`. Antes da montagem completa leia o `.openpublishing.publish.config.json` de cada
  snapshot: até 2020 os exemplos moravam no repositório dependente dotnet/samples, e o código desses snapshots some em
  silêncio.
- **A referência de API do site em ECMA XML** (dotnet/dotnet-api-docs): leitor `ecma-xml`, um documento por tipo com o
  mesmo nome de documento e os mesmos títulos de membros do `nuget-xmldoc`, então a referência do site e o XML dos
  pacotes se dobram num registro de `families`. O `xml/FrameworksIndex` (dezenas de megabytes) é lido com expressões
  sobre bytes, não como árvore; `skip_monikers` descarta tipos e membros só de preview; só entram exemplos em C#.
- **Milhares de pacotes NuGet** (Microsoft.Extensions.*, 1.754 linhas de pacotes): baixe-os em paralelo direto no
  armazém do bruto (`rawstore.put`), anotando quais trazem XML, declare só esses e rode `build` sem rede — 2,5 minutos
  em vez de uma hora de pausas do `refresh`.
- **Fatos de uma linha nos metadados de versões** (fase e fim do suporte) ficam só no documento da linha: repetidos em
  cada um dos 285 documentos de versão, tomavam todos os resultados para «end of support».
- **Duas numerações numa instância** (.NET 8.0 e C# 8): a linguagem leva `csharp-` (`csharp-7` para uma edição do
  padrão, `csharp-12.0` para especificações de recursos). O `ghdocs` aceita `…/git/trees/TAG:PASTA` para repositórios
  cuja árvore completa o GitHub trunca (dotnet/runtime, dotnet/roslyn) e codifica espaços e `#` nos nomes.
- **Exemplos de código dos repositórios dependentes de um site DocFX** (dotnet/docs até 2020: o dotnet/samples ficava ao
  lado como `samples/`): a partir do `.openpublishing.publish.config.json` de cada snapshot, aponte a pasta pelo campo
  `repos` do `docfx` para o último commit desse repositório antes do dia do snapshot (se ele mesmo guardava tudo numa
  subpasta, com sufixo: `dotnet/samples/<sha>/samples`) e semeie de um clone parcial só os arquivos que as páginas
  citam. Caminhos com espaços pedem `quote_paths: true`: as chaves do armazém semeado são codificadas, e sem o campo
  sumiam 870 exemplos de ADO.NET por snapshot.
- **`slug_rewrite` a partir dos arquivos de redirecionamento de um site DocFX** (`.openpublishing.redirection.*.json` de
  todos os snapshots e renomeações do git entre snapshots): siga a cadeia até uma página viva no ramo mais novo e
  mantenha o par só quando as páginas nunca estão no mesmo snapshot e compartilham o título ou o fim do endereço —
  cerca de um terço dos redirecionamentos leva a uma página geral da seção e é descartado. 1.880 regras ancoradas
  somam dois minutos à montagem do cache de fragmentos.
- **Medir antes de mudar o leitor**: um processo com o índice carregado (`server.quality` com
  `profile.MAX_PER_DOC`/`FUSION_DEPTH` trocados, ou um filtro em volta do `spec_mcp._dedup` para descartar um tipo de
  seção) mede cada variante em minutos; só o que ganha vai para o leitor ou o `config.json`.
- **Um site Docusaurus que mantinha cada versão na própria pasta e depois apagava as antigas** (playwright.dev:
  `dotnet/versioned_docs/version-1.12` … `version-1.23`, depois só `version-stable`): cada pasta vem do histórico do
  repositório na última edição — o pai do commit que a apagou, ou o commit da sua última mudança quando esse pai já
  foi tomado por outra versão — e `{version}` em `folders` faz cada commit dar só a pasta da sua versão, não todas as
  versões ao lado. Um `slug_rewrite` de `version-1-X-` para `version-stable-` e uma família em `families` fundem as
  edições de uma página. Na era `version-stable`, o retrato de uma linha é o seu último commit «roll to 1.X».
- **O mesmo exemplo em abas para várias variantes** (NUnit / MSTest / xUnit, npm / yarn / pnpm):
  `docusaurus_tabs: true` põe o rótulo da aba antes do conteúdo; sem o campo, o texto traz vários blocos de código
  iguais sem dizer qual é qual.
- **Documentação de repositórios .NET feita com Jekyll, kramdown e mdsnippets** (xunit.net, fluentassertions.com,
  nsubstitute.github.io, Shouldly): listas de atributos kramdown `{: .issue-link }`, âncoras de títulos `{ #id }`,
  tags Liquid `{% examplecode csharp %}` com o esqueleto oculto `{% requiredcode %}`, linhas «snippet source | anchor»
  sob as inserções do mdsnippets — leitor `ghdocs-history-kramdown`. O campo `jekyll_data` expande inserções
  `{% include … examples=site.data.… %}` cujos dados ficam em YAML (as dicas do FluentAssertions — mais de cem pares
  «antes — melhor»); um arquivo de dados que a tag ainda não tem o Jekyll não desenha, e a inserção some em vez de
  derrubar a página. Antes de baixar, faça o censo da marcação das páginas da tag mais nova (`git grep -o` num clone
  bare completo).
- **Um site DocFX fora do learn.microsoft.com** (docs.nunit.org, bunit.dev): o mesmo leitor `docfx`; um site com tags
  vira uma fonte por última tag de cada linha menor numa família, semeada de um clone (`seed_git_store.py`). Uma
  página só com `uid` no cabeçalho tira o título do primeiro «# …» (`title_from: "heading"`), e as páginas de
  redirecionamento (`redirect_url:` no cabeçalho) são excluídas de antemão — cada uma falha como «corpo curto».
- **C# indentado com tabulação** (xUnit.net, bUnit): `outline_tabs: true` no `ghcode-history`, senão a classe fica uma
  seção só. Confira a indentação em alguns arquivos de cada repositório: `git show <tag>:<arquivo> | sed 's/\t/→/g'`.
- **Clone sem blobs serve só para árvores.** `git grep` e `git ls-tree -l` num clone `--filter=blob:none` buscam cada
  blob numa requisição própria e travam por minutos: os tamanhos dos arquivos de uma tag vêm da árvore pela API
  (`gh api repos/…/git/trees/<tag>?recursive=1`), o censo da marcação de um clone bare completo (dezenas de megabytes,
  um minuto).
- **Um site sem tags numa instância com filtro de versão** (xunit.net, docs.nunit.org): as páginas levam as versões
  dos produtos no dia da montagem, e o filtro de uma linha antiga (`nunit-3.13`) as esconde. O prompt manda buscar
  duas vezes: com a versão (referência de API, pacotes, notas, código) e sem ela (os guias).
- **Uma entrada de versão ainda sob «Unreleased» na própria tag da versão** (a página de releases do FluentAssertions
  na 8.11.0): as versões que a página não cita vêm do `ghreleases` com um `skip` que nega a lista das ausentes
  (`^(?!(8\.11\.0|…)$)`); o resto dos releases do GitHub repetiria a página.
- **Um pacote que embute invólucros gerados de outra biblioteca** (bunit.web: 12 mil membros `Bunit.Web.AngleSharp`
  sobre o DOM do AngleSharp) e polyfills e anotações compilados dentro (`System.*`, `Microsoft.CodeAnalysis.*`,
  `JetBrains.Annotations` — 81 tipos em cada linha do Shouldly): conte os membros por namespace antes de declarar e
  corte-os com `exclude_types`.
- **TypeScript com recuo de quatro espaços e sem «;»** (TypeORM: Prettier `semi: false`): o `ghcode-history-ts` pega
  os membros da classe em dois espaços e distingue a assinatura de sobrecarga de um método pelo «;», então o
  EntityManager inteiro ficava uma só seção, e cada sobrecarga (`export function Column(): PropertyDecorator`) viraria
  uma seção própria. `indent: 4` e `join_same: true` dividem os membros em quatro espaços e fundem seções vizinhas com
  o mesmo título. Depois da divisão, liste os títulos da maior classe.
- **Um componente próprio do site Docusaurus em volta das abas** (`<DatabaseTabs>` com `<DatabaseTab
  value="postgres">`, rótulos em `src/constants`): o `docusaurus_tabs` conhece só `<Tabs>`/`<TabItem>`, e os nomes dos
  bancos somem. Um import MDX em várias linhas (`import {` … `} from "@site/…"`) deixava o fim como primeira linha do
  texto, então o título da página virava seção e o nome do arquivo virava o título — olhe as primeiras linhas dos
  documentos gravados. Páginas planas que começam com uma lista de links para as próprias âncoras (um sumário) davam a
  cada documento uma introdução feita de nomes de seções; ela é retirada. Leitor `ghdocs-history-typeorm`
  (`custom_tabs`, `drop_toc`).
- **Código e testes pesam mais que a documentação** (TypeORM: 94 % de 55 mil trechos): uma consulta só de
  identificadores (`@Column nullable default`, `leftJoinAndSelect`) traz entidades de teste e arquivos de código. O
  prompt manda o modelo pôr as palavras do tema da página ao lado dos nomes («Column options», «joining relations») e
  buscar código pelo nome da classe e do método: «como o modelo» subiu de 7 para 10 de 10, `max_per_doc` não mudou
  nada.
- **Um README de pacote que o build muda só na aparência** (o TypeORM troca ```` ```typescript ```` por
  ```` ```javascript ````): o README vem do commit de publicação (`gitHead`) ou da tag pelo `npm-readme`, e o tarball
  (2–3 MB cada, 300 MB para 115 versões) só para versões sem nenhum dos dois; uma regra `slug_rewrite` dá às duas
  fontes uma só chave.
- **Os testes das bibliotecas tomam os resultados de consultas por nomes de API** (dotnet-testing: os testes repetem
  nomes de API nos nomes dos métodos e no código dezenas de vezes; em «xUnit1001 Fact methods cannot have parameters»
  três testes ficavam à frente da página da regra): o campo de busca `demote` (`{"pattern": expressão sobre os nomes
  dos documentos de testes, "places": N}`) desloca essas seções N posições para baixo na lista de cada método de
  busca. O número vem de uma medição num processo só (aqui 5: com as próprias palavras 7 → 8, «como o modelo» 10 de
  10, smoke verde). O `max_per_doc` não ajuda aqui: cada teste é um documento à parte.
- **Passar da CPU para a GPU no meio do `vectors`**: pare só esse processo, troque `fastembed` e `onnxruntime` por
  `fastembed-gpu` e `onnxruntime-gpu[cuda,cudnn]` no venv da instância e rode `vectors` de novo — ele vê os pontos já
  calculados como inalterados (aqui 76.800 de 153.060) e calcula o resto; os números da CPU e da GPU coincidem. Não
  apague a coleção.
- **Atualizar uma instância arquivada** (dotnet-testing, segunda rodada: +119 fontes): desempacote o arquivo de volta
  na pasta da instância e confira as contagens, acrescente as fontes, rode `refresh` só das novas
  (`./df <instância> refresh <id…>`), monte a referência de API a partir de pacotes baixados antes para o armazém do
  bruto com `build`, depois `manifest`, a varredura de chaves comuns, `vectors` (ele mesmo remove os pontos
  excedentes), `smoke`, `quality` e a comparação com os números da primeira rodada. O arquivo novo recebe um nome novo
  (`…-b.tar.gz`), é extraído à parte e conferido com o disco (`diff -r`); só então se apagam os textos, o `raw/` e o
  arquivo antigo.
- **Uma entrada de release e uma entrada de changelog da mesma tag têm o mesmo nome quando a tag não tem «v»**
  (`1.0.0`: o `ghreleases` nomeia o documento pela tag, o `changelog-regex` pela versão): a varredura de chaves comuns
  achou isso em duas bibliotecas, e a correção custou rebaixar 171 documentos. Nomes de release com `name_prefix` como
  `<biblioteca>-release` não colidem com os do changelog.
- **Tags de um repositório em grafias diferentes** («V6.3.1», «v6.2.0», «5.1.0»): o `ghreleases` não lê o «V»
  maiúsculo, então duas fontes — `ghreleases-stable` com `tag_prefix: "V"` e `ghreleases` com `skip: "^V"`; para a
  documentação por tags basta uma fonte, porque `tags` é «tag real → rótulo da versão».
- **Um pacote que mudou de nome** (AngleSharp.Scripting.JavaScript até a 0.12 → AngleSharp.Js): tags, changelog e
  releases de um repositório vão em duas fontes com rótulos de versão diferentes, cortando as versões do outro com uma
  expressão `skip`; o pacote NuGet de cada nome é uma fonte própria.
- **Uma página de regra de analisador igual no site e no repositório** (NUnit.Analyzers: docs.nunit.org e
  `documentation/` das tags): o repositório ganha um `name_prefix` próprio (senão o README colide com o README do
  pacote NuGet), o `slug_rewrite` leva as chaves das páginas de regra às do site e uma família em `families` põe a
  seção uma vez só nos resultados.

- **Uma versão cuja tag é uma entre muitos builds** (NuGet.Client: as tags `7.9.0.83`, `6.14.3.1` são números de build
  de quatro partes, e a mais alta nem sempre é a versão: de 56 versões conferidas, 11 divergiram): o commit de uma
  versão é o atributo `repository commit` do nuspec do pacote NuGet publicado para ela
  (`v3-flatcontainer/<id>/<versão>/<id>.nuspec`), e ele vira a chave em `tags`. Para duas versões (5.7.2, 6.0.2) o
  commit do nuspec não existe no repositório público (a API responde 422), e para 4.x–5.10 o nuspec não traz nenhum —
  ali vale a tag de build; confira cada commit com `gh api repos/…/commits/<sha>` antes do `list`.
- **READMEs da raiz de repositórios diferentes numa instância** (NuGetGallery, `mcp/` do NuGet/Home): o `ghdocs` chama
  cada um de `readme`, e as introduções de vários READMEs dividem a chave de seção — a varredura de chaves comuns antes
  do `vectors` achou duas. O `ghdocs` não tem `name_prefix`: o mesmo arquivo pelo `ghdocs-history` com
  `tags: {"<sha>": ""}` (sem versão), `files` e `name_prefix` ganha chave própria; para um arquivo de subpasta o
  `exclude` é `^docs/`, não `/`.
- **Uma referência de API atrás de dezenas de testes de uma classe** (`FrameworkReducer.GetNearest`: a seção da
  referência é a 33ª tanto por palavras quanto por sentido, e na frente dela há mais de trinta métodos de uma classe de
  teste): o `demote` não faz nada — ele só reordena dentro da lista de profundidade `k`×6 = 30. Um `fusion_depth` maior
  (40) deixa a página entrar na lista, e `max_per_doc: 3` impede que um arquivo de testes ocupe todos os lugares: «como
  o modelo» 8 → 10 de 10 (`demote` 5–20 não mudou nada, 30 só ajudou com profundidade a partir de 40). Meça com um
  processo que substitui `profile.DEMOTE_PLACES`, `FUSION_DEPTH` e `MAX_PER_DOC`.
- **Pacotes cujo XML falta em parte das linhas** (NuGet.* 6.5–6.11 e NuGet.VisualStudio 17.5–17.11 saíram sem
  documentação XML, a 6.12 a trouxe de volta): antes de declarar o `nuget-xmldoc`, baixe a última versão de cada linha
  menor e anote quais levam XML (761 pares pacote × linha — alguns minutos em cinco threads); o prompt nomeia as linhas
  que existem e manda responder sobre um tipo das que faltam pela linha presente mais próxima. As tabelas de recursos
  (`Strings`, `Resources`, `NuGetResources`, `AnalysisResources`, `SR`: 395 documentos, os maiores) vão para
  `exclude_types`; documentos que o `build` já não escreve ficam em `corpus/` como órfãos — tire-os dali, não apague.
- **Um alvo de `quality` precisa existir na edição mais nova da página**: `VersionRange.Satisfies` tem XML só na
  edição 1.0.7 (`SimpleVersion`), os membros das linhas posteriores não têm comentários e não viraram documentos — o
  alvo foi escolhido da listagem do cache sem olhar `versions`, e nada na API atual poderia achá-lo. Confira os
  `p.versions` de cada alvo; escolha um membro presente na linha mais nova (`Parse`).
- **Todos os pacotes de um dono no nuget.org**:
  `https://azuresearch-usnc.nuget.org/query?q=owner:<nome>&take=100&prerelease=false` (52 de 54 resultados eram nossos;
  dois de outros produtos, `PoliteCaptcha` e `NuGet.Services.Build`, saem pelo `authors`); pacotes só com
  pré-lançamentos aparecem apenas com `prerelease=true` e não dão nada ao `nuget-package`. Produtos com numeração
  própria (NuGet.VisualStudio 17.x é o número do Visual Studio, NuGet.Mcp.Server 1.x, NuGet.Server 3.x) ganham uma
  marca por `version_prefixes`, senão «1.4» é ao mesmo tempo o servidor MCP e o NuGet 1.4.
- **Quando uma atualização move a tag de código e testes numa linha maior já tomada** (p. ex. 2.11.3 → 2.12.5): as
  revisões de arquivos que existem só na tag antiga viram órfãs. Tire-as para uma pasta de rascunho antes do `manifest`
  (nunca apague); elas não entram no arquivo novo e se recuperam da tag antiga no GitHub.

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
| `requirements.txt` | conteúdo do venv da instância; só quando a instância precisa de um pacote fora dos conjuntos compartilhados | escrever, só com esse pacote |
| `.env.example` | modelo para as chaves próprias da instância (`ANTHROPIC_API_KEY`, ajustes do agente); o `GITHUB_TOKEN` fica no `.env` da raiz; um `.env` real nunca vai para o git | cópia |
| `.gitignore` | `.env`, `__pycache__/`, `*.pyc`, `.venv/`, `out/`, `index/passages.json` | cópia |
| `.mcp.json` | registro do servidor HTTP para o Claude Code | cópia, trocar a porta |
| `README.md` | o que é este domínio e de onde vem sua documentação | você |
| `UPDATE.md` | como atualizar o corpus quando a origem mudar | você |
| `corpus/` | documentos baixados mais `index.json`, o passaporte | `refresh`, `manifest` |
| `index/` | o cache de trechos `passages.json` do qual o servidor sobe; no modo de arquivo vai para o git comprimido, `passages.json.gz` | montado a partir de `corpus/` pelo primeiro passo que precisa dele |
| `raw/` | respostas brutas dos sites para o `build` sem rede, versões antigas em `raw/_old/`; nunca vai para o git | `refresh`, `check`, `list` |
| `out/` | a decisão sobre o modo de busca, logs | `setup`, `serve` |
| `.venv/` | ambiente virtual próprio da instância; sem ele o `df` usa o compartilhado de `.venvs/` | passo 1, só se necessário |

## Passo 1 · Pasta e ambiente virtual

Nunca é preciso ativar um venv: o `df` escolhe sozinho o certo. Por padrão uma instância nova não tem venv próprio e
usa o ambiente compartilhado (`.venvs/cpu` ou `.venvs/gpu`, escolhido por `DF_VENV`; a seção «Ambiente
compartilhado» do README da raiz), então o passo é só a pasta:

```
mkdir -p instances/<domínio>/prompts
cp instances/react/.gitignore instances/react/.env.example instances/<domínio>/
```

Crie um venv próprio só quando o domínio precisa de um pacote que não está em `requirements/cpu.txt` nem em
`requirements/gpu.txt`. Então escreva um `requirements.txt` só com esse pacote e crie o venv. É a única ação feita de
dentro da pasta da instância, e daí em diante o `df` usa o `.venv` próprio da instância sempre que ele existir:

```
cd instances/<domínio>
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/python -m pip install -r requirements.txt
cd ../..
```

**Armadilha conhecida.** Em alguns sistemas o `python3` do pacote vem sem o módulo `venv`. Use um interpretador que
o tenha, por exemplo o do conda: `/caminho/para/miniconda3/bin/python3 -m venv .venv`. Isso não afeta nada depois,
porque o venv é autocontido.

Um `.env` próprio só é necessário para chaves privadas (`ANTHROPIC_API_KEY`, ajustes do agente). A linha
`GITHUB_TOKEN` vem do `.env` da raiz; o arquivo próprio da instância, se tiver essa linha, a substitui.

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
[ ] ambiente: venv compartilhado pronto (.venv próprio só para pacotes fora dos conjuntos compartilhados)
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
