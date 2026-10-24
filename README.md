<img width="1324" height="503" alt="Снимок экрана — 2026-08-01 в 21 31 20" src="https://github.com/user-attachments/assets/0c693272-8163-4518-81ea-02a329ef2208" />

**English** · [Русский](README.ru.md)

# present — a skill for Claude Code

An agent skill that walks you from an idea to a finished **bespoke HTML presentation** (a deck): slide text, a design brief, the build, a spoken run-through and trimming to the time budget.

It is not a template filler: Claude reads your material, picks the art direction itself and designs the deck around that specific content — different talks come out as visually different decks (structure, palette, typography, background, character of motion).

The output is a **self-contained HTML file**: it opens offline in a browser, with no CDN and no network references.

There are two paths, and the user picks one when the skill starts: **short** — a one-page presentation as
a single file, with no presenter window, in one go; **full** — a talk that the skill leads through the stages
"Context → Design → Build → Voice", stopping wherever it needs a step from you.

---

## How I make talks: Context · Design · Voice

The skill leads you through this pipeline itself: you call `/present`, and it walks the stages with you. Where it needs a step from you — record a run-through, pick a style — it says what to do and waits. Below is the pipeline itself: what happens at each stage and why.

The core idea: **three files instead of one**. It all used to live in a single PowerPoint — text, design and speech together; pull one thread and everything unravels. Here it is three separate jobs with three artefacts. And there is exactly one rule: **first get `slides.md` by any means, and only then deal with design.**

### 1. Context → `slides.md`

The first step is called "context", not "words", on purpose: **it does not matter where the material came from** — what matters is that `slides.md` comes out the other end. Two main entry points, both **spoken out loud**:

- **Talk the idea through.** Open party mode in [BMAD](https://github.com/bmad-code-org/BMAD-METHOD) on an empty folder and dictate your idea as a free-form monologue: what I want to say, what has to be in there, what to pay attention to. It works the idea over and asks concrete questions — it turns into a session. Out comes `slides.md`: which slides there will be and what I say on each. No design.
- **Straight to the recorder.** If the talk is already in your head — hit record and say the whole thing as it comes. Transcribe it ([OpenSuperWhisper](https://github.com/Starmel/OpenSuperWhisper) locally, model `large-v3` — fast and accurate on an M-chip, punctuation and English loanwords included) and hand the transcript to BMAD: "here is the whole talk, break it into slides".
- **Existing material.** Context can be anything: articles on the topic, an entire repository (then the numbers on your slides come from a real `git log`), internal docs, someone else's presentation. You drop it into BMAD exactly the same way: "here is the material, lay it out as slides".

The difference between the first two: in the first case the talk is **invented** together with the model, in the second the model **lays out** a talk it already has in full. All paths converge on the same point.

**In the skill** this is the "Context" stage. It runs all three entry points itself, no BMAD needed: an interview about the idea, laying out dictation, text or material, transcribing a recording (if whisper is on the machine). It asks for the time budget up front and estimates the running time from the word count. If the talk runs long, it tells you by how much.

> **A piece of advice bigger than this pipeline: talk to the model with your voice.** Not just for talks — for any task. You say everything you have on the problem, dump your thoughts as they come, and it extracts the substance. When you speak, the flow is freer: you don't edit yourself mid-sentence, you don't hunt for the phrasing.

### 2. Design → `design.md` + the deck
<img width="1324" height="503" alt="Снимок экрана — 2026-08-01 в 21 31 30" src="https://github.com/user-attachments/assets/c99fbd81-322a-4a24-9d04-13d386675d4a" />

We are in the AI era — **you don't need PowerPoint, generate HTML**: models write it well and fast, and it gives you animation, motion and interactivity.

- **A reference.** You don't have to do the layout yourself — you have to find a style. For example [styles.refero.design](https://styles.refero.design): you look at how it actually appears, and every style **ships with a ready `design.md`** — copy it into your folder. Design done. `design.md` is by now practically a standard, like `README.md`: a file describing how everything should look (fonts, colours, shapes, spacing). You can go the other way too: write it by hand or put it together with BMAD.
- **The build.** `/present <folder>` — the skill needs exactly two files, `slides.md` and `design.md`. It will ask a question or two if it has to, and build the deck. That is the **baseline**, and a baseline is usually not what you want — but it cost you little time and it is already in your hands.
- **The revision loop.** You look at the deck and fix it **with words**: what you don't like, what to change where, where to add motion. You can keep polishing forever. The easiest way is comments right on the slides in Claude Design — see the next point.
- **Claude Design — strongly recommended.** It is now built into Claude, and the skill works with it itself. The slides are drawn on a Claude Design canvas: you can edit them by hand there and leave comments right on a slide. The agent sees every comment and knows which slide and element it refers to. The skill also offers to publish the finished HTML deck as a private page in Claude — you leave edits to it the same way, as comments. Included in the Claude subscription (Pro / Max / Team / Enterprise). The pipeline works without it too, editing is just less convenient.

`design.md` here is the main file, not decoration: the same material under three different briefs gives three completely different decks.

**In the skill** these are the "Design" and "Build" stages. If Claude Design is available, the design goes on a canvas by default: first 2–3 style options, you pick one and comment; then the whole deck on the canvas, you edit it by hand or with comments. The skill writes `design.md` from the canvas and moves the slides into an offline HTML deck on its own kernel: animations, presenter window, PDF. In the "do it yourself" mode the skill draws one option and goes on without stopping. Without Claude Design — three roads: a ready style from refero (your step: drop the file into the folder), a brief from 3–4 questions, or design taken from a reference URL. Then the build, the check in Chrome and the revision loop.

### 3. Voice → the loop back into `slides.md`

The deck is ready — and this is where most people stop, while the most valuable part is still ahead.

- **A run-through on the recorder.** Start the deck, start recording (on the computer itself) and walk your slides out loud, in your own words, as if the room were already seated. Spot a mistake — say it out loud right there, it all gets recorded. You immediately learn two things: **how long the talk actually runs** and **where you flounder** — where you started mumbling, the slide is bad, not you.
- **Transcription.** [OpenSuperWhisper](https://github.com/Starmel/OpenSuperWhisper) locally → raw text with all the filler and every "uhh". Free, and nothing leaves your machine.
- **The model as an editor.** Back into BMAD: read this, cut what needs cutting, tell me where I'm wrong. And the key trick — **give it the time budget**: "I have twenty minutes, here are the per-slide timings, squeeze it". It trims exactly what you won't miss. What comes out is **your words**, just tidied up — not something the model made up on its own.
- **Back into `slides.md`** and rebuild. Now the deck holds what you actually say — the slides followed the live speech, not the other way round.

That arrow back is the whole reason for splitting into three files: every lap the talk gets shorter and sharper, and nothing has to be rebuilt from scratch.

**In the skill** this is the "Voice" stage. After the build the skill briefly offers three ways to do the run-through: dictate straight into the chat (Handy, macOS dictation), record it and drop the file into the folder — the skill transcribes it itself, it only needs whisper or a similar tool on the machine (if there is none, the skill tells you what to install) — or transcribe the recording yourself and send the text in the chat or as a file. From there it works on its own: transcribes the recording (if needed), compares the length with the budget, trims the speech in your own words, shows a diff of `slides.md` and rebuilds the deck. Every lap is logged in `DECK.md`: date, length, what changed.

### Together or "do it yourself"

At the start of the full path the skill asks how to work. **Together** — every stage goes through questions. **Do it yourself** — the skill runs the stage without questions and shows the result: it lays out the material, picks the style and trims the speech on its own. It stops only at your steps and at the end. Switch modes on the fly by saying "carry on yourself" or "let's do it together".

### Stopped — it picks up again

The state of the path lives in the «Конвейер» (pipeline) section of `DECK.md`: which stages are done, what is waiting on you, the budget and the run-through laps. Closed the session, recorded the run-through a day later — call `/present <folder>`, and the skill continues from the same spot without asking again.

### Two loops

| Loop | What it changes | How |
|---|---|---|
| **Big** | *what* I say — structure, order, design | edit `slides.md` → rebuild the deck |
| **Small** | *in which words* — the phrasing | edit the note right in the presenter window → export `notes.js` → drop it next to the deck. No editor, no rebuild |

The small loop turns as many times as you run the talk out loud.

### Pipeline tools

| Step | Tool | What for | Required? |
|---|---|---|---|
| Context | [BMAD METHOD](https://github.com/bmad-code-org/BMAD-METHOD) | party mode and sub-agents for presentations and storytelling: work the idea up, break a transcript into slides, then tighten the text to the time budget | no — the skill runs the "Context" stage itself |
| Context / Voice | [OpenSuperWhisper](https://github.com/Starmel/OpenSuperWhisper), model `large-v3` | local transcription of your recordings: a whisper.cpp wrapper for macOS — a global dictation hotkey, drag & drop for recordings, models downloaded from inside the app. Fast on an M-chip, punctuation and loanwords included, free and offline | no — the skill transcribes the recording itself if whisper is on the machine; otherwise anything that puts text into an input field works (macOS has built-in dictation too) |
| Design | [styles.refero.design](https://styles.refero.design) | a gallery of clean references, each style shipping a ready `design.md` — copy it into your folder | no — the skill builds a brief from questions or from a reference URL |
| All stages | **this skill** | leads from idea to deck: `slides.md` → `design.md` → one offline HTML with a presenter window and PDF export → run-through and trimming | — |
| Design and edits | Claude Design | a canvas to design the deck and a page to edit the finished deck: edit by hand, comment right on the slides, the agent sees what each comment refers to | no, but strongly recommended — included in the Claude subscription; the pipeline works without it, editing is less convenient |

---

## What the finished deck can do

- Navigate with `←` `→`, the mouse wheel or a swipe; the position lives in the `#hash` — F5 doesn't lose your slide.
- `P` — the **presenter window** (the short path has none unless you ask): notes, next slide, timer, and slide switching from there too. Ideally two monitors: one you share, one in front of you. Share the deck to the screen, not this window.
- Notes are edited **right in that window**: double-click the text → fix it → apply. Mumbled during rehearsal — rephrase it on the spot, while the thought is fresh.
- `B` — black screen, `F` — fullscreen.
- `S` — **export to PDF**: the kernel freezes every slide in its final frame (counters counted up, animations played out), the page is 16:9 with no margins, one slide per page, text stays text. Blurred shadows are deliberately printed flat — Chrome writes them as a raster mask that Preview paints as a grey rectangle over your content — and the deck looks the same as ever on screen. When someone asks you to "send the slides" — you have something to send.
- `?check` in the address bar — highlights slides whose content is taller than the screen.
- **Slides you can poke at.** HTML does things PDF cannot, and the skill uses that sparingly: it goes
  through the slides, looks for places where the audience would understand more if they switched something
  themselves, and offers options — the user decides. The engine yields to widgets: a click on a button or a
  caption doesn't flip the slide, typing in an input doesn't trigger hotkeys, a scrollable area scrolls on
  its own. One or two such slides per deck is the norm, and each one reads fine even if nobody clicks it.
- **Live notes** in a `<slug>-notes.js` file next to the deck: edit them in the presenter window or in an external editor — they are picked up on the fly, no rebuild. A copy is embedded in the HTML as a fallback, so the deck can still be sent as a single file.

The deck runs as a local file, and a browser cannot write to disk from one — so note edits live as a draft in the browser (they survive F5) and reach the disk via the "⤓ notes.js" button: download it, drop it next to the deck over the old one. The file wins over the draft; unsaved edits are not lost — the presenter offers to bring them back.

## Install

**As a Claude Code plugin.** Run in Claude Code:

```
/plugin marketplace add StasPotapov/present
/plugin install present@present
```

The skill is then called `/present:present`. To get a new version: `/plugin marketplace update present`,
then `/plugin update present@present`.

**From a clone.** Pick one way: with both, the skill loads twice.
The skill is installed by copying it into a skills directory — globally (available in every project) or locally in one project.

Globally:

```bash
git clone https://github.com/StasPotapov/present.git ~/.claude/skills/present
```

Or into a specific project:

```bash
git clone https://github.com/StasPotapov/present.git .claude/skills/present
```

To check that Claude Code sees the skill: `/present` in the command list.

## Usage

```
/present <idea | folder | file | recording | deck | reference URL>
```

The skill works out where to start on its own:

| What you give it | What happens |
|---|---|
| an idea or topic in chat | a question about the path; full — the "Context" stage with an interview |
| text, a transcript, articles, a repository | the "Context" stage: laid out as slides |
| an audio recording of the talk | transcription, then layout |
| a folder with `slides.md` | the "Design" stage |
| a folder with `slides.md` and `design.md` | straight to the build |
| a folder with `DECK.md` | continues from the step where it stopped |
| a new run-through recording next to the deck | the "Voice" stage |
| a finished deck (`*.html`) | polishing, or growing it into a talk |
| the folder and "I left comments" | the skill reads the comments on the canvas or the review page, edits the deck and replies in the threads |

The first thing Claude asks about is the path. **Short** — for when you just need to show an idea in
pictures: no `slides.md`, no brief, no interview, no plan to approve; exactly one `<slug>.html` lands on
disk, with no presenter window. At the end the skill offers to add one in a single line. Need it right
away — say so: "with notes". **Full** — everything described above and below. A short deck is not wasted
if you later grow it into a full talk: hand the finished HTML back to the skill and say what to add —
the deck is its own context (text in the slides, art direction in its own styles).

For the full path, the input that works best is a **context folder**:

```
my-talk/
├── slides.md     # slide text + speaker notes
├── design.md     # design brief (art direction)
└── *.png/jpg     # media to embed
```

The two files are a hard requirement for the build. Without them the skill first runs the "Context" and "Design" stages:

- **`slides.md`** — what gets said: a breakdown into slides (`---`, `## Slide N` or headings), pairs of "slide point → speaker note".
- **`design.md`** — how it looks: the design brief. An export from styles.refero.design (palette tokens, type scale, components, Do/Don't, a ready `:root`) is applied precisely.

Every stage ends with a check, and the next one does not start until it passes. If both files already exist, the skill goes straight to the build.

It also works without a folder: raw talk text, a transcript, bullet points, a single topic, a path to a repository (then the numbers on your evidence slides come from a real `git log`), a reference URL to extract design DNA from.

The skill does **not invent content** — numbers and facts come from your material or are confirmed with a question.

## What you get

**Short path** — one file and nothing else:

```
wherever you asked/
└── <slug>.html      engine, styles, slides and base64 media — all inside
```

**Full path.** Your working folder stays yours: material, raw sources and build inputs stay where they are. Everything the deck needs in order to be presented goes into a separate `deck/` subfolder — you can zip that one folder and carry it to any laptop without picking files by hand.

```
talk/
├── slides.md                    input: slide text
├── design.md                    input: design brief
├── transcript.md · *.jpg        raw material — untouched
├── src/ · build.py              build sources (if the deck was built by script)
├── rehearsal-1.m4a · .md        run-through recordings and their transcripts
├── DECK.md                      manifest: pipeline status, slide map, decisions with their "why", how to edit
└── deck/                        ← the self-contained presentation folder
    ├── <slug>-<date>.html       the deck itself
    ├── <slug>-<date>-notes.js   live notes (source of truth after the first generation)
    └── deck-assets/             only if the media didn't fit into base64
```

`DECK.md` exists so that the next session doesn't have to read a monolithic HTML file end to end: it holds the pipeline status, the slide map and the decisions with their rationale. If the deck was built by script, you edit the sources in `src/` and rebuild — never the finished HTML.

## Example
<img width="1324" height="503" alt="Снимок экрана — 2026-07-29 в 22 43 40" src="https://github.com/user-attachments/assets/3b95c197-2d8d-4f89-b73d-229adbe70cb3" />

[`example/`](example/) holds a real deck built by this skill and run through the whole pipeline above — the talk "Context. Design. Voice.", 16 slides. Its inputs (`slides.md`, `design.md`), the `DECK.md` manifest with the pipeline status and the build script with its sources are all there, so you can see both the folder layout and the "script" build mode. The talk itself is in Russian — it is there as a sample of format and layout, not as text to reuse.

[`example-quick/`](example-quick/) shows the short path: one 6-slide page with no presenter window, plus the request that produced it (in Russian too).

```bash
git clone https://github.com/StasPotapov/present.git
open present/example/deck/kontekst-dizayn-golos-2026-07-28.html
open present/example-quick/present-korotkiy-put.html
```

## How the skill is put together

| File | What it is |
|---|---|
| `SKILL.md` | the router: ingest → path and working mode → which stage to start from → gates between stages → your manual steps → status in `DECK.md` |
| `stages/context.md` | the "Context" stage: an idea, dictation, material or a recording → `slides.md` with a running-time estimate |
| `stages/design.md` | the "Design" stage: Claude Design canvas, refero, interview or reference URL → `design.md` |
| `stages/canvas.md` | Claude Design: checking that it is available, the canvas, comments, moving the canvas into HTML, the review page |
| `stages/build.md` | the "Build" stage: art direction → plan → build → check in Chrome and PDF → polish |
| `stages/rehearse.md` | the "Voice" stage: recorded run-through → transcript → trimming to the budget → rebuild |
| `stages/quick.md` | the short path: one page in one go, presenter window on request |
| `stages/transcribe.md` | transcribing recordings for "Context" and "Voice": a transcription skill, `whisper-cli` or text from you |
| `assets/kernel.html` | the deck engine (KERNEL v8): navigation, animators, presenter window and its off switch, PDF export, guards for interactive slides. Copied **verbatim**; all the visual design goes into its `<style id="design">` and the slides into `#deck` |
| `assets/design-axes.md` | 9 axes of design decisions — a list of questions, not a catalogue of answers: composition, margins, typography, colour, background, motion, detail, chrome, interactivity |
| `assets/art-direction.md` | how to design the visuals around the content; how to apply `design.md`; where to get briefs |
| `assets/cookbook.md` | the kernel class contract (`.count`, `.chain`, `.clist`, `.pipeline`, `[data-type]`…), the interactivity contract (where your own JS goes and how it coexists with navigation and printing), offline fonts, media, checks. There are deliberately no ready-made components or art-direction samples in there — otherwise every deck comes out a recoloured copy of them |
| `assets/deck-template.md` | the skeleton of `DECK.md` |
| `assets/validate.py` | the validator for a finished deck |

### Validator

```bash
python3 assets/validate.py <deck>.html
```

It checks kernel integrity (the `KERNEL v8` marker, base and print styles, chrome, presenter, note editing, PDF export), leftover `{{…}}`, network references and local links to missing files, JS syntax (`node --check` on every script block and on `notes.js`), stray script blocks and the order of the interactive block relative to the kernel, interactivity on an engine older than v6, a click bound by attribute to a non-interactive tag, section sync between `notes.js` and the slides, and the presence of `slides.md` / `design.md` / `DECK.md`.

A short-path deck is recognised by the validator on its own — a single file with no companion set — and it doesn't ask for the set. A deck with `data-presenter="off"` needs no notes; such a deck next to a full-path set is an error.

## Requirements

- Claude Code.
- Recommended: **Claude Design** — sign in to Claude Design with `/design-login` in Claude Code. The canvas and the review page go through it. The skill checks for Claude Design in every session. Without it, the skill suggests signing in, in one line, and works without it.
- For the validator — `python3` (stdlib) and `node` (for `--check`; without it the syntax check is simply skipped).
- PDF export is verified in Chrome; from Safari it is worth checking the result by eye.
- Optional: **poppler** (`brew install poppler`) — Claude uses `pdfinfo`/`pdfimages`/`pdfseparate` to check the exported PDF. Without it that check degrades to file size plus a `qlmanage` render of the first page.
- The **Claude in Chrome** extension — this is what Claude uses to check the deck before handing it over:
  it runs the layout audit (overflow, broken images, tiny type, clipped and overlapping text) and looks at
  the frames itself. The check is mandatory on both paths; without the extension Claude says so plainly and
  asks you to page through the deck with `?check` yourself.
- Optional: the **defuddle** skill — used to read a reference URL. Without it, `WebFetch` is used.
- Optional: a transcription skill or **whisper-cli** with a model — used to transcribe recordings. Without it the skill asks you to paste the transcript.

No `npm install` / `pip install`: the skill uses preinstalled tools only. Fonts are system stacks, or one embedded base64 open-source font (with your consent — the only network action allowed during a build).

## License

[MIT](LICENSE) — take it, change it, ship it, only keep the copyright notice. That covers the skill: `SKILL.md`, `stages/`, the assets, the deck engine, the validator, the build script and the [`example-quick/`](example-quick/) sample.

The **talk content** in [`example/`](example/) is not covered: slide text, speaker notes, deck screenshots and the QR code are the author's personal talk, © 2026 Stas Potapov, all rights reserved. Read it as a sample of format and layout, take the techniques — but don't reuse the text as your own. Details in [`example/NOTICE.md`](example/NOTICE.md).

## Language

The skill itself is written in English: `SKILL.md`, the stages and the assets. It talks to you in your language — the one you use when you call it. The deck is written in the same language by default: slide text, speaker notes, `slides.md` and `DECK.md`. Need another language — say so, and the skill writes the deck in it or translates an existing one.

The kernel UI — the presenter window, hints — follows the deck's `lang` attribute: Russian for `ru`, English for any other language. Talk folders with the old Russian headings (`## Конвейер`, «На экране») keep working.

This README has a Russian version: [README.ru.md](README.ru.md).

---

Use it. But using *this* skill is not the point: **write your own**. Once you build something like it yourself and realise you can make anything you want for yourself — that is when you see what these models are actually for.
