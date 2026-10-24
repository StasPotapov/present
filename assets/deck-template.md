# DECK.md template — the deck manifest

This file is a template for the skill `/present`. At the start of the full path, the agent creates
`DECK.md` from it in the working folder (next to the sources, not inside `deck/`). At first it has
only the header and the Pipeline section; the other sections appear after the first build
(`stages/build.md`, Step 5). Principle: record **deviations and decisions (what and WHY)**,
do not retell the HTML; the slide map is navigation, so that the next session does not have to
read the whole monolithic file. Replace the `{{…}}` placeholders, delete the hint comments
`<!-- -->`, except the `<!-- present:pipeline -->` marker. Update the manifest at each refinement of the deck (Step 6) and at the end of each stage.

**Language.** The agent writes `DECK.md` in the person's language, headings too. The template
below is in English. The skill reads both the English and the Russian names:
- sections: `## Pipeline` = `## Конвейер`, "Next step" = «Следующий шаг»;
- stages: Context / Design / Build / Voice = Контекст / Дизайн / Сборка / Голос;
- statuses: done / in progress / waiting for the person / not started / skipped = готово / идёт /
  ждёт человека / не начат / пропущен;
- work mode: together / do it yourself = вместе / сделай сам; deck mode: "script" / "by hand" =
  «скрипт» / «руками».
For other languages, the agent maps the names by meaning. Keep the marker line
`<!-- present:pipeline -->` right under the Pipeline heading in any language: the validator finds
the section by the heading (English or Russian) or by this marker, so other languages work too.

---

# {{Deck title}} — manifest

`{{deck/slug-date}}.html` · {{N}} slides · built {{date}} · kernel `{{v8}}` from the skill `/present`

## Pipeline
<!-- present:pipeline -->

<!-- Status of the path. A new session reads this section FIRST and continues from "Next step".
     Stage statuses: done · in progress · waiting for the person: <what> · not started · skipped (<why>).
     Update it at the end of each stage and before each stop at a manual step. -->

- **Work mode:** {{together | do it yourself}}
- **Claude Design:** {{design on the canvas | straight to HTML | not available}} · canvas {{https://claude.ai/artifact/… | —}} · review page {{https://claude.ai/artifact/… | —}}
- **Time budget:** {{20 min}} · pace {{~125 words/min — assumption until the first run-through | N words/min from run-through K}}
- **Next step:** {{Voice — waiting for the person: run-through of the talk to a recording → put the audio into the folder and call /present <folder>}}

| Stage | Status | Summary |
|---|---|---|
| Context | {{done}} | `slides.md`: {{N}} slides, estimate {{~18 min}} |
| Design | {{done}} | `design.md`: {{source — Claude Design canvas / refero "Playful" / interview / self}} |
| Build | {{done}} | `deck/{{slug-date}}.html`, validator and Chrome clean |
| Voice | {{waiting for the person: run-through}} | {{—}} |

Voice laps (each run-through is a row):

| Lap | Date | Recording | Duration | Budget | What was done |
|---|---|---|---|---|---|
| {{1}} | {{date}} | `{{rehearsal-1.m4a}}` | {{24:10}} | {{20:00}} | {{shortened 04, 07, 11; −18 %}} |

## Where things are

<!-- The show folder is self-contained: to take the talk away, take the whole folder. -->

- **Show folder:** `{{deck/}}` — `{{slug-date}}.html`, `{{slug-date}}-notes.js`{{, deck-assets/}}.
- **Working folder:** `slides.md`, `design.md`, `DECK.md`{{, src/, build.py}}, materials and raw input.
- **Claude Design:** {{canvas — the design sketch, the HTML is the main version | review page — a private copy of the deck for comments}}.

## Deck mode: {{"script" | "by hand"}}

<!-- "script": the working folder has a build script and sources → edit the SOURCES and rebuild
     ({{command, for example python3 build.py}}); keep the script and the sources up to date —
     a rebuild must not roll back edits. Do not edit the finished HTML by hand.
     "by hand": there is no script → a targeted Edit directly in the HTML (anchors — see "How to edit"). -->

## Slide map

| No. | Title | Components/classes | Notes |
|---|-------|-------------------|---------|
| 01 | {{Title slide}} | {{composition scheme; which contract classes, if any}} | {{font embedded as base64}} |
| 02 | {{…}} | {{…}} | {{data-dur tuned: 1100→1600}} |
| 07 | {{…}} | {{**interactive:** what is clicked and what happens}} | {{the PDF gets the default state}} |

## Art direction — answers per axis

<!-- one line per axis from assets/design-axes.md; this is a decision for THIS talk,
     not a description of a template. An "as usual" item = the axis is not thought through. -->

- **Composition (axis 1):** {{dominant scheme + how the accent slides differ from it}}
- **Margins and alignment (2):** {{how much air, to which side the text is pressed}}
- **Typography (3):** {{system; what carries the character — weights/sizes/tracking/column width}}
- **Color (4):** {{palette logic; key --tokens from :root}}
- **Background `#bg` (5):** {{what it is and why exactly so; static or moving, and why}}
- **Motion (6):** {{slide transition — is slidefade overridden; one "signature" technique inside}}
- **Details (7):** {{what runs through the whole deck as a system}}
- **Chrome (8):** {{how #bar / #counter / #hint are styled}}
- **Interactivity (9):** {{which slides are interactive and why; who clicks — the speaker or the reader; or "the deck is static"}}
- **Why so for this talk:** {{how the decisions connect to the content, in one or two sentences}}

## Decisions and deviations

<!-- what was done in a non-standard way and WHY — so that the next agent does not "fix" it back -->
- {{changed animations/timings, turned-off effects, custom components outside the cookbook}}
- {{edits of WHEEL_TH/WHEEL_COOLDOWN, if any — the only allowed change inside `<script id="kernel">`}}
- Interactivity: {{what is interactive, WHY exactly here, what the PDF version loses}}
- Known traps: {{for example, "backdrop-filter removed — conflicts with slidefade"}}

## How to edit

- The MODE above sets the way: "script" → sources + rebuild; "by hand" → a targeted Edit.
- Slide text/structure → the sections `<section class="slide">` in `#deck` (search by the title or the slide number).
- Styles → only `<style id="design">`; do not touch `<script id="kernel">`, `<style id="print">` and the chrome DOM (`#bar/#counter/#hint`).
- Interactivity (if any) → `<script id="interactive">` after the kernel script, before the closing `</body>`
  (the kernel has one more `</body>` inside the presenter HTML string — match the last one); clickable zones are marked
  `[data-interactive]`, scrollable ones — `[data-scroll]`. The contract is in `cookbook.md`, the section "Interactivity".
  After edits, click through the widgets by hand: the validator does not check them.
- Speaker notes → `{{slug}}-notes.js` (the source of truth, the presenter window picks it up live);
  `data-notes` in the HTML is a fallback copy: when you edit the structure, sync both.
  The second way is directly in the presenter window, with buttons: "✎" edit (or a double-click) — the note of the current
  slide, "☰" all notes — all at once, "⤓ notes.js" — download `{{slug}}-notes.js` to Downloads
  and put it here over the old one.
  Before a rebuild, READ the current `{{slug}}-notes.js` — it can have edits from a rehearsal.
- Media: {{what is embedded as base64; what is in deck/deck-assets/}}; the originals are in the working folder.
- Check after edits: `python3 <skill folder>/assets/validate.py {{file}}.html`
  plus the visual self-check in Chrome (the procedure is in `cookbook.md`, the section "Visual self-check
  in Chrome"): a local `python3 -m http.server` in the show folder, `?check`, a frame-by-frame pass in capture
  mode. Without Chrome — open the deck with `?check` by hand and scroll through it by eye.
