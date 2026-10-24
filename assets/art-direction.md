# Art Direction — how to design the deck visuals for the content

The goal of the skill is decks that are **visually different for their content**, not variations
of one template. You are the designer: you read the material and `design.md`, choose a visual
language and design from zero. Everything is offline: only system fonts and embedded assets (see `cookbook.md`).

## Where art direction comes from

1. **From the content and tone.** Read the material and ask yourself: how is this talk different
   from the next one on the same topic? What is the main thing in it — a proof, a feeling, a
   process, an argument, an admission of a mistake? How must it stay in memory after a week? The
   answer becomes visual decisions by `design-axes.md`. **There are intentionally no ready
   mappings "genre → look" here**: as soon as a table "technical talk = mono and grid" appears, all
   technical talks become the same. Two talks about infrastructure can and must look different.
2. **From `design.md` / a reference document.** This is the main source of "character". Take from it:
   the mentioned colors/brand, the tone (restrained/bold), the structure of the argument, the
   mood keywords. `design.md` can set anything — follow it, not habit.
3. **From an optional reference (URL/HTML).** Only if the person gave a link/file. Borrow the
   **design DNA**, NOT a pixel clone:
   - **URL** → first the Skill `defuddle` (clean text/structure), if necessary `WebFetch` (raw HTML:
     take the `:root` variables, `color`/`background`, `font-family`, radii, the character of the layout).
     ⚠️ This is a network action — only when the person gave the URL; offline — ask for a local HTML/screenshot.
   - **HTML file** → Read → palette, font stack, radii, background, visible layout.
   - **Screenshot** (if attached) → assess the mood, palette, density visually.

## If the folder has design.md (a structured brief), it is the LAW

`design.md` (if it came as `decision.md`/`DESIGN.md`/`brief.md`, save it as `design.md`) is the authoritative art direction. Do not invent
your own. A frequent source is an export from **styles.refero.design**: palette tokens (name/hex/role), type scale
(fonts + substitute, weights, sizes, leading, tracking, OpenType), radii/spacing/density, components
with specs, Do/Don't, surfaces, imagery, layout, sometimes a ready `:root` with CSS variables.

Apply it EXACTLY, but adapt it to the slide format:
- **Palette / surfaces / radii / spacing** — take them as is (you can copy a ready `:root` almost word for word).
- **Type scale** — briefs give WEB sizes (for example, display 341px for a landing page). **Do NOT copy px literally**:
  convert to the slide scale with `clamp()/vw`, KEEP the proportions, weight, `line-height` (leading) and
  `letter-spacing` (tracking) — they carry the character. For example, display → `clamp(3rem,12vw,12rem)` with the same leading 0.8.
- **Fonts — first open-source + embed, otherwise system.** Do not download a custom face from the brief (ObviouslyVariable,
  Druk, Söhne…) as is, but find its **OSS version or a close OSS analogue** and **ask
  the person whether to embed it as base64** (`@font-face` in the design layer — downloaded ONE TIME at the build with `curl`,
  the finished deck stays offline; the recipe is in `cookbook.md`). Examples of analogues: Druk/Knockout → **Anton**/**Archivo Black**;
  Founders Grotesk → **Space Grotesk**; Söhne/Inter-like → **Inter**; mono → **JetBrains Mono**/**IBM Plex Mono**.
  ⚠️ For a deck in Russian (or another language in Cyrillic script), the analogue must have **Cyrillic** (Anton/Archivo Black do not have it; poster faces with Cyrillic are
  Oswald, Unbounded, Russo One) — and embed both subsets, `cyrillic` and `latin` (the recipe is in `cookbook.md`).
  - The person agrees → embed as base64, the character is kept, the deck is self-contained.
  - The person does not agree / no OSS analogue / no network → **system substitute** (start the substitute chain from the brief
    with a close system face):
    - wide/heavy poster display → `Impact,Haettenschweiler,'Arial Narrow',sans-serif`
    - grotesque/neutral → `'Helvetica Neue',Arial,sans-serif` · humanist sans → `system-ui,'Segoe UI',sans-serif`
    - serif → `Georgia,'Palatino Linotype',serif` · mono → `ui-monospace,Menlo,monospace`
  In the finished deck, in any case — no CDN/`@import` from the network, only system faces or embedded base64.
- **Do/Don't, imagery, elevation, layout** — follow them literally (flat/shadows/borders/"one thesis per screen" and so on).
- **Similar Brands / vibe** — keep the mood in mind, do not copy someone else's content.

Result: the deck must look like "this brand made a presentation", not like our default.

## What to decide

The full list of decisions is in `design-axes.md` (9 axes: composition, margins, typography, color, background,
motion, details, chrome, interactivity). Go through them before the build and write down a one-line answer per axis — this is the
art direction of the deck, and it also goes into `DECK.md`.

The only things to keep strict here, no matter which visual language you chose:
- text-to-background contrast — not lower than AA, check it on a real frame, not in your head;
- motion is turned off in `@media (prefers-reduced-motion:reduce)`;
- the content explains the decisions: behind each "why like this" there is an idea of the talk, not a habit.

## How it goes into the file

All styling goes into `<style id="design">` (palette as `:root` variables, `body`/`#bg`, typography,
components, layouts). Slides go into `#deck`. Do not touch `<script id="kernel">` and the chrome DOM. Components
that the kernel animates must get their own CSS/keyframes — check the class contract in `cookbook.md`
(especially `@keyframes gitin` for `.clist`, `.chain.seq .node`, `.pstage.on` and so on).

## Sources of references and design.md (all free, no subscriptions)

Only open/free sources — no paid subscriptions, nothing to pay for.

A ready **design.md** (a structured brief, drop-in):
- **styles.refero.design** — search by brand / mood / color / URL → download DESIGN.md (free beta). The main source.
- **designmd.app** — a library of ready design systems under a permissive license.

Galleries to "choose a look" → then give the URL as a reference (we extract the design DNA) or collect a brief together:
- **Awwwards**, **Godly** (godly.website), **SiteInspire**, **Land-book**, **Lapa Ninja**, **Httpster** — web design showcases.
- **Dribbble**, **Behance** — concepts and slide design.

⚠️ Do not offer paid/subscription catalogs (for example, **Mobbin**) — only open sources.

Flow: the person chooses a look → puts `design.md` into the folder OR gives a URL → the skill builds the deck in this style.

## Principle
Different talks → noticeably different decks (structure, palette, typography, background, motion). If two
presentations with different meaning came out similar, the art direction is not done. Rely on the content and design.md,
not on "like last time".
