# Stage Build — slides.md + design.md → deck

`SKILL.md` sends you to this file when the stages Context and Design passed their gates: the working folder
has `slides.md` and `design.md`. Refinement of an existing deck also comes here. The short path (`stages/quick.md`)
takes Steps 4 and 5 from this file by its own rules. It does not create the folder layout and the file set of the full path.

## Folder layout (strict)

The working folder of the person holds the person's materials and sources. They stay where they are. **Everything
the deck needs for the show goes into a separate subfolder `deck/`.** The person can archive this folder as a whole,
take it to a different laptop and show the deck from there, without picking files by hand.

```
talk/                            ← working folder (the person gave it)
├── slides.md                    input: text per slide
├── design.md                    input: design brief
├── transcript.md · *.jpg · *.m4a   raw material, references, audio — stay where they were
├── src/ · build.py              build sources (deck mode "script")
├── DECK.md                      manifest: slide map and decisions
└── deck/                        ← SELF-CONTAINED show folder
    ├── <slug>-<date>.html
    ├── <slug>-<date>-notes.js
    └── deck-assets/             only if media did not fit into base64 (sidecar)
```

Rules: **put nothing extra into `deck/`** — only what the deck cannot be shown without (the HTML, its `notes.js`,
sidecar media). **Do not move and do not delete** materials and sources in the working folder. The build script and `src/`
stay outside. `DECK.md` also stays outside (it is a process document, not a runtime file). If another deck already
uses the folder `deck/`, name the folder `<slug>-deck/` and write this in `DECK.md`. Paths inside the deck are relative only
(`deck-assets/…`), so that the folder can move as a whole. If you continue a deck that was built with the old layout (the HTML is
directly in the working folder), move it into `deck/` together with `notes.js` and the sidecar media, and correct the paths in the build script.


## Step 1 — Concept + art direction (internal)
**The first build from a Claude Design canvas** (`DECK.md` names a canvas, and the Pipeline does not say "Build — done"):
the canvas IS the structure and the art direction. In Step 1 only axis 9 (interactivity) remains. In Step 3 skip
the slide list (the canvas shows it) but keep the interactivity question in the mode "together". Then build by
`stages/canvas.md`, "Transfer", and go on to Step 5. Once the deck is built, the HTML is the main version: later
builds are refinement (Step 6) and never transfer the canvas again, unless the person asks for it.

Make: (a) the **structure** — the split into slides, what is on each slide, where the strong frames are; (b) the **art direction** —
go through the axes in `assets/design-axes.md` (composition, margins, typography, color, background, motion, details, chrome,
interactivity) and write one line of answer per axis. How to read the brief and the reference: `assets/art-direction.md`.
The skill made `design.md` itself in the stage Design, axis by axis. The answers per axis are already in it. Do not decide them a second time:
here only the structure and axis 9 per slide remain.
This is design for the material, not a choice from a menu. The assets contain no ready-made looks. Do not take looks
from past decks or from other files in the input folder. The answer "as usual" on any axis means
that you did not think the axis through — decide it again. **If `design.md` exists, IT IS the art direction. Do not invent your own.** How exactly
to apply it (palette, type scale, fonts): the canonical section in `art-direction.md`. If the person gave a
URL reference, extract the design DNA (`defuddle`→`WebFetch`; see art-direction.md).

**Go through axis 9 slide by slide, not in general.** Go through the storyboard and mark the candidates: a slide
with a "before/after" comparison; a dependency where the viewer could change a parameter and see the
result; data that does not fit into the frame as a whole; a fork where the talk can go different ways.
Check each candidate with the three questions of axis 9: does a click add UNDERSTANDING (not only motion);
who clicks — the speaker on stage or a reader through a link; can the viewer read the slide with no click at all.
Keep two or three survivors at most — these go into the plan. If no candidate survives, that is a normal answer:
the deck is static, and there is no question to the person.

## Step 2 — Entry gate
Make sure that the folder has BOTH files — `slides.md` and `design.md`. No `slides.md` — go back to the stage
Context (`stages/context.md`). No `design.md` — go back to the stage Design (`stages/design.md`). Do not collect them
here and do not invent content. Report briefly what you understood and which deck you propose (topic, arc,
art direction in one sentence).

**At the same time (advise, do not block the build; in the mode "do it yourself" decide yourself and say it in the final message):**
- **Missing assets:** "a diagram/screenshot/hero would work well here — will you add it to the folder, or do we go without it?"
- **Missing facts/numbers:** "there are no numbers for the results slide — give real ones, or we remove the slide."
- **Ambiguities:** audience / timing→number of slides / tone — only if the content does not answer them.
- **Fonts (if the brief depends on a specific typeface):** embed an **OSS equivalent** in base64 (the deck stays offline) or use a system
  substitute (the default is the system substitute).
Do not ask what the materials already contain. As soon as `slides.md` and `design.md` exist, go to the plan (Step 3).

## Step 3 — Deck plan (show, confirm)
Show the list of slides (for each slide: title, what is on screen, which animation/component, one line of the speaker notes) +
the art direction in one sentence + which slides use media + one line about interactivity. Ask "Build / changes".
Do not build HTML before approval. **Mode "do it yourself":** show the plan and build at once. Choose the interactivity yourself
(one or two widgets at most, only if they add understanding) and name it in the final message.

**Interactivity is a separate question, and only if there are candidates** (Step 1, axis 9). One
AskUserQuestion, multiple choice, 2-4 options written for THIS talk — "slide 07: a load
slider, the latency number recalculates", not "add interactivity". The last option is mandatory —
"keep the deck static". Build what the person chose. If the person chose nothing, the deck is static.
If there were no candidates, there is no question. Do not invent an extra step.

## Step 4 — Bespoke build
From a canvas: the method is `stages/canvas.md`, "Transfer"; the rules below (folder, kernel, language, checks) still apply.
Build **into the subfolder `deck/`** of the working folder (see "Folder layout"). Create it if it does not exist.
**Deck language:** write the deck content (slide text, `data-notes`, `<title>`, the live notes file) in the person's language
by default, or in the language the person asked for.
**Build method — as is convenient:** targeted `Edit` calls on a copy of the kernel OR your own build script. If you write
a script, save it **in the working folder** (not in the scratchpad and not in `deck/`!) together with the sources
it builds from. Keep it up to date after every change (a rebuild must not roll the deck back). Record the deck mode in
`DECK.md` (Step 5).
1. Copy `assets/kernel.html` **of THIS skill** (from its `assets/` folder) **word for word** as the base — the whole
   `<script id="kernel">` and the chrome DOM stay unchanged. **The kernel source is ONLY the assets of the skill.** If the talk is about
   `present` itself and the input folder has a copy of the skill (`present/`, another `kernel.html`, a finished `*.html` deck), that is
   CONTENT/reference, NOT the kernel: do NOT copy the kernel from there. If you are not sure, compare the marker `KERNEL v8` in the header
   of the freshly copied file. If you insert CSS/slides with a script, match the real blocks by their placeholder content
   (`<style id="design">\s*/\*…\*/\s*</style>`, `<div id="deck">\s*<!--…-->\s*</div>`). `assets/validate.py` confirms
   the integrity later (Step 5). Put the real `<title>` in place of `{{TITLE}}`.
   Replace `<html lang="en">` with `<html lang="<deck language>">` (for example `<html lang="ru">`): the kernel picks its
   UI strings by this attribute. On the root tag, this and `data-presenter="off"` are the only allowed edits
   (the full list of kernel edits — `cookbook.md`, "Kernel UI language").
2. In `<style id="design">` write your own CSS for the art direction: palette (`:root`), `body`/`#bg`, typography
   (system stacks OR an embedded base64 OSS font with the consent of the person — the recipe is in `cookbook.md`), components, layouts.
   Compare with the class contract in `cookbook.md`: components that
   the kernel animates must get their CSS/keyframes (especially `@keyframes gitin` for `.clist`).
3. Put the designed slides into `#deck`: one thought — one slide, short titles, numbers → `.count`,
   EACH `<section>` has `data-notes` with the speech word for word (stage directions in `[brackets]`). The first slide has the class `active`.
   Lay out each slide for ITS thought: the kernel requires no "standard" slide structure, and
   many slides are only large typography or their own layout without named components. Take classes
   from the contract (`cookbook.md`) only when the thought of the slide really needs a counter,
   a cascade or a process diagram. Remember that an expensive animation is good once or twice in the whole deck.
   The composition of the slides must change through the deck (axis 1): three identical silhouettes in a row are a defect.
4. **Media** (smart default): light media (< ~800 KB) → inline base64 (the deck stays one offline file);
   heavy media (> ~800 KB, large GIFs/video) → the sidecar folder `deck/deck-assets/` (relative link
   `deck-assets/…`) + **warn** the person that the deck is no longer one file and moves only together with its folder.
   Do not touch the source images in the working folder — copy them, do not move them.
4b. **Interactivity** (if it is in the plan). Put your own JS into a separate block `<script id="interactive">`
   AFTER `<script id="kernel">`, before the closing `</body>`. You still do not touch the kernel.
   ⚠️ If you insert it with a script, match the LAST occurrence (`rfind`/`rsplit`): the first one is inside
   the kernel, in the string that builds the presenter window, and an insert there breaks the kernel. Clickable areas are
   `<button>` or your own markup with `[data-interactive]`. Scrollable areas are `[data-scroll]`. Otherwise the click and
   the wheel go to the navigation. State reset when the slide opens, the behavior in PDF, the work in the
   presenter preview, the stage direction in `data-notes` — all of this is your job. The full contract and the snippets are in
   `cookbook.md`, section "Interactivity: the kernel contract". Use one widget per slide. The slide
   must be readable even if nobody clicks it.

5. **Generate the live notes file** `<slug>-notes.js` next to the deck, in the same `deck/`, from data-notes
   (name = name of the deck html file + `-notes.js` — the kernel looks for exactly this name):
   ```js
   window.DECK_NOTES = String.raw`
   ## 01 · Slide title
   Note text… [stage directions in brackets]
   `;
   ```
   It is both a prompter for reading (phone/paper) and a live source: the kernel reads the file again on the fly —
   changes appear in the presenter window without a rebuild. The section key is the number `NN` (the same as the slide number).
   The title after `·` is for the human. Do not use the backtick and `${` in the note text.
   `data-notes` in the HTML stay as a fallback copy (the deck also works as one file).
   **`<slug>-notes.js` is the source of truth after the first generation.** The person edits the speaker notes directly
   in the presenter window (button "✎ edit") and downloads the file with the button "⤓ notes.js". That file can have changes that are not
   in `data-notes`. So on every rebuild/refinement **first read the existing `notes.js`**
   and copy its text into `data-notes` of the deck you build. Do not overwrite the file from old `data-notes`.

## Step 5 — Check and show
- **Run the validator:** `python3 <skill folder>/assets/validate.py <deck>.html`. It checks the integrity of
  the kernel (the marker `KERNEL v8`, base/print styles, chrome, presenter, note editing, PDF export), leftover `{{…}}`,
  network links and local links to missing files, JS syntax (`node --check` on each script block — kernel, interactive — and on notes.js),
  extra script blocks and the order of interactive relative to kernel, interactivity on a kernel below v6, a click
  attached with an ATTRIBUTE handler (`onclick=…`) to a non-interactive tag, the match of the sections of
  `<slug>-notes.js` with the slides, the presence of `slides.md`/`design.md`/`DECK.md`. Fix the errors before you show the deck.
  The validator recognises a single deck of the short path by itself (it is not in `deck/`, and no file of the file set is next to it)
  and does not ask for the file set. It reports an error for a deck with `data-presenter="off"` next to a file set. What it does NOT catch: broken widget logic and clicks attached with
  `addEventListener` — you check these by hand, in the next item.
- **Visual self-check in Chrome (mandatory step).** YOU look at the deck, not the person: start a
  local server in `deck/`, open a tab, get the `?check` verdict and the JS errors from the console, enter capture
  mode, run the layout auditor (ONE call for the whole deck) and look at the frames with your eyes. The check stands on two
  supports, both are mandatory: the **auditor** gives numbers (overflow against the 16:9 reference, content outside the frame, broken
  images, small font size, clipped and overlapping text, empty slides), the **frames** give what numbers do not catch (contrast,
  rhythm, composition, "hanging" lines). Fix what you find and capture again, until the auditor is silent and the frames
  are clean. **The third pass is the PDF:** neither `?check` nor the auditor sees its print layout.
  Check it with a headless print from the terminal (`cookbook.md`, item 9) and render it through `qlmanage` —
  the same Quartz engine that the viewer will open it with. The exact procedure with snippets is in `cookbook.md`, section "Visual self-check
  in Chrome". Four things that people trip over:
  **(1)** the extension does not open `file://` (`Can't interact with browser-internal or unparseable URLs`) —
  use only `python3 -m http.server` from the folder `deck/` and `http://127.0.0.1:PORT/…`;
  **(2)** the browser window is NOT 16:9 and `resize_window` does not correct it — measure overflow with the auditor
  against the reference `innerWidth/16*9`, not by eye on a screenshot. A window with a very disproportional ratio
  (outside 1.70–1.86) is brought to a 16:9 frame with the stand from `cookbook.md`;
  **(3)** build capture mode ONLY with the `shotmode` style from `cookbook.md`: a home-made `animation:none`
  captures cascades and cards EMPTY (the design layer keeps them at `opacity:0` until the animation) and leaves a copy
  of the background on top of the content — you will then fix things that do not exist;
  **(4)** do NOT press `S` and `⌘P` in this mode — the system print dialog blocks the extension
  until somebody closes it by hand. Check the PDF with a headless print from the terminal (`cookbook.md`, item 9). This is
  part of the check, not a task for the person: `?check` and the auditor do not see the print layout at all.
  Look at the pages through `qlmanage` (the Quartz engine, as in Preview): `pdftoppm` draws clean
  even a PDF that Preview shows with grey rectangles.
  If there is no claude-in-chrome extension / Chrome is not available, say so and ask the person to open
  the deck with `?check` and scroll through it with their eyes. Do not skip the check silently. This is not a manual step: the path does not
  stop, the request goes into the stage result, and the Pipeline section gets "Chrome not checked" (in the person's language;
  Russian: «Chrome не проверен»). **This branch does not cancel
  the PDF check:** the headless print needs neither the extension nor a live tab — only the Chrome binary.
  If that binary is also missing, say that the PDF is not checked.
- **Check interactivity by hand, not by eye** (if there is interactivity): in the open tab click each
  widget and make sure that the deck did NOT go to another slide, the state changed visibly, and going to
  the next slide and back leaves the widget in a sensible state. If there is an input field, type
  "psb" into it and check that presenter/blackout/print did not open. Check an expandable block
  for overflow when it is open: open it and run the layout auditor (`cookbook.md`, item 5) — it measures
  the slide in the open state. A deck on a kernel below v6 cannot hold interactivity —
  the kernel must be updated.
- Manual check (the person does it, not you): `P` opens the presenter as a separate window (not a tab)
  and it is in sync, `B` blanks the screen, the live notes load.
- **Complete `DECK.md`** in the working folder (not in `deck/`) by `assets/deck-template.md`. The router created
  it at the start of the path with the Pipeline section. If there is no file, create it fully. Write its sections in the person's
  language: deck mode ("script"/"by hand"), slide map, art direction in short, decisions/deviations with "why", how to edit.
  If you built with a script, check that the script and its sources are in the working folder next to `DECK.md`.
- **Check the layout:** `deck/` contains only the HTML, its `notes.js` and (if any) `deck-assets/`. Nothing
  extra got there, and the sources and materials stay unchanged in the working folder.
- The deck is in `deck/<slug>-<date>.html`. Open it: `open deck/<file>` (macOS). Tell the person directly: to
  take the talk away, take **the whole folder `deck/`** (archive, USB stick, other laptop). There is no need to pick files.
- Remind the controls: `← →`/wheel/swipe — go through slides, `P` — presenter window with speaker notes (do NOT share it, share the deck),
  `B` — black screen, `F` — fullscreen, `S` — save the deck as PDF. The position is kept in the `#hash` — F5 does not lose the slide.
  **Edit the speaker notes directly in the presenter window with mouse buttons** (there are intentionally no letter hotkeys there: people
  type in this window; only the arrows, `Esc` and `⌘⏎` work): "✎ edit" or a double click on the text → "✓ apply",
  "☰ all notes" — all the text at once, "↺ revert" — drop your changes and go back to the file (if you change your mind,
  the plate brings them back), "⤓ notes.js" — download the file to Downloads, "⧉ copy" — its text to the clipboard.
  From `file://` the browser cannot write to disk,
  so the changes live as a draft in the browser (they survive F5, the indicator `✎ draft` is in the presenter header). They
  go to disk as the downloaded file — put it next to the deck over the old one, and the indicator turns green again.
  The built-in help in the presenter window explains all of this: the button "? help" (when the presenter opens for the first time,
  a hint about it appears at the bottom). There is no need to describe each button to the person.
  The old alternative still works: edit `<slug>-notes.js` in an external editor — the presenter loads it in a couple of seconds
  (the file wins over the draft; unsaved changes are not lost — the presenter offers to bring them back).
  The person can send the deck as one HTML (embedded fallback notes), but must give the talk from the folder `deck/`, next to notes.js.
- **If the person asks for a PDF** — the key `S` in the open deck (the same with `⌘P`): the kernel freezes ALL slides in the final
  frame (counters finished, cascades/chains/pipeline shown, typed text typed, background laid out
  per page) and opens the print dialog → choose "Save as PDF". The page is 16:9 (13.333×7.5″) without
  margins, slide = page, colors/background/images print, text in the PDF stays text. Warn about these details:
  a sidecar GIF gives its first frame, and the deck must be next to its `deck-assets/`; a slide with
  overflow is cut at the page edge — run `?check` first; if the browser still printed white,
  turn on "Background graphics" in the dialog. Tested in Chrome; from Safari compare the result by eye.
  Shadows in the PDF are flat on purpose: Chrome writes a blurred shadow as a raster mask, and Preview draws it
  as a grey rectangle over the content. So during print the kernel replaces it with a thin outline
  of the same color (on screen everything comes back). All print traps: `cookbook.md`, item 9.

## Step 6 — Refinement
**Comments on the review page** (the person says "I left comments", or `DECK.md` names a review page): read and apply them
by `stages/canvas.md`, "Read the canvas and its comments", then rebuild here and republish the page to the same URL.
Offer to adjust: palette/density/motion, the treatment of the background, add/remove a slide, timings.
**Before any change, read `<slug>-notes.js` again** — the person could edit the speaker notes in the presenter window
and download the file. Copy these changes into `data-notes`. Do not overwrite them with old text from the HTML.
First find the deck mode (from `DECK.md` — deck mode "script" / "by hand", Russian: «скрипт» / «руками» — or from the presence of a build script): mode "script" → edit the SOURCES
and rebuild, do not touch the finished HTML by hand, keep the script up to date; mode "by hand" → a targeted Edit —
only in `<style id="design">` and `#deck`, without touching the kernel. If you added/removed slides, renumber the sections in
`<slug>-notes.js` (it is the source of truth for the speaker notes; update `data-notes` in the HTML as the fallback). Put the rebuilt
deck into the same `deck/` — do not make copies in the working folder and do not leave old html/notes from
past builds in `deck/`. **After changes — the visual self-check in Chrome again** (Step 5): run the layout auditor
on the whole deck (this is one call). Capture the frames again for the slides you changed. If you changed
the palette/typography/density, capture them for the whole deck: layout edits made blind are the main
source of overflow. After changes, update `DECK.md` (the slide map and the decisions section) if you changed
the structure/animations/timings. If there is interactivity, it is also a subject of refinement (what is clickable, how
large, what happens). After any change, click it through again: the validator does not
catch a broken widget. Refinement of a short path deck works on the same single file (`stages/quick.md`) — do not create the folder and
the file set until the person asks for promotion.

## Step 7 — End of stage
- In `DECK.md`, update the Pipeline section (in the person's language; Russian: «Конвейер»): "Build — done"
  (Russian: «Сборка — готово»), the result in one line, the next step.
- The order of the final message of the stage: result and path to the deck → controls (short, `? help` in the presenter
  window explains the rest) → the review page offer → the manual step block last.
  Do not run `open` in the mode "do it yourself": the person did not ask for a window on their screen.
- Recommend editing through Claude Design: if it is available and the deck has no review page yet, offer the review page
  in one line (`stages/canvas.md`, "The review page"). It is the recommended way to edit: comments right on the slides,
  and you see what each one refers to. It is an option, not a gate; if the person refuses or says nothing, do not repeat.
  Claude Design is not available → the one-line hint from `stages/canvas.md`, once per session.
- The default next step is the stage Voice (`stages/rehearse.md`). It starts with a manual step:
  a run-through of the talk aloud. The ways to do the run-through and the block format are in `stages/rehearse.md`, Step 1: read
  it, give the manual step from there, then stop.
  If the person says that the talk is ready and there will be no run-through, write "Voice — skipped (<why>)"
  (Russian: «Голос — пропущен (<почему>)»).

## Continue work on an existing deck
The person gave a path to a `*.html` (the marker `KERNEL v` in the header) and a prompt about what to finish. This is not a new talk, it is a
continuation. **Nothing internal is embedded in the deck and there is nothing to look for: the deck is its own context.** Read it:
- slide text — the sections `<section class="slide">` in `#deck`;
- the speaker's speech — `data-notes` on the sections (if `<slug>-notes.js` is next to the deck, it wins — read it);
- art direction — `<style id="design">`: the `:root` palette, typography, composition classes;
- the kernel version — the marker `KERNEL v` in the header. `DECK.md` can be next to the deck — then it is the main source of decisions.

Then act by the request:
- **targeted refinement** ("change the palette", "add a slide", "rewrite the third one") — edit the same file
  by Step 6, do not change the mode and the layout;
- **promotion to a full talk** — ask where to create the working folder, and set up the file set: restore
  `slides.md` from the markup and the speaker notes (if there are no speaker notes, write the speech by the stage Context), complete `design.md`
  (the stage Design, or record the art direction that the deck already has as the brief), remove from `<html>` the attribute
  `data-presenter="off"` if it is there, add `data-notes` with the speech from `slides.md` to each slide,
  move the deck into `deck/`, generate `<slug>-notes.js` from `data-notes`, create `DECK.md` with the
  Pipeline section. Then the usual refinement and the stage Voice.

**The kernel is old.** The deck was built on a kernel below v6, and the person adds interactivity to it — the old kernel
has no guards, and the widget will fight with the navigation. Say this directly and move the slides with the design layer
into a fresh `assets/kernel.html`; keep the deck language on the root tag (old Russian decks: `lang="ru"`,
the fresh kernel ships `lang="en"`). Without interactivity there is no reason to touch the old deck. The same applies to the switch
of the presenter window: only kernel v7+ understands `data-presenter="off"`.

