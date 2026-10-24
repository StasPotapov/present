---
name: present
description: "Guides the person from an idea to a finished HTML presentation (deck): slide text, design brief, an offline single-file deck with a presenter window, a run-through aloud and trimming to the time budget. Short path: a one-page presentation in one go. Talks and writes the deck in the person's language."
when_to_use: "\"make a presentation\", \"build slides\", \"a deck for my talk\", \"help me come up with a talk\", \"a simple presentation\", \"go through my run-through / rehearsal\", \"cut the talk to 20 minutes\", \"continue the talk\" — in any language. Input: an idea, a topic, text, a recording, a folder with slides.md and design.md, a repo, a reference URL or an existing deck. If the person needs a .pptx file, this is not the skill."
argument-hint: "[idea / folder / file / recording / deck / reference URL]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch, Skill, AskUserQuestion, Artifact, ArtifactComments, mcp__claude-in-chrome__tabs_context_mcp, mcp__claude-in-chrome__tabs_create_mcp, mcp__claude-in-chrome__tabs_close_mcp, mcp__claude-in-chrome__navigate, mcp__claude-in-chrome__computer, mcp__claude-in-chrome__javascript_tool, mcp__claude-in-chrome__read_console_messages, mcp__claude-in-chrome__browser_batch
---

# present — from an idea to a bespoke HTML presentation

The skill guides the person through the pipeline "Context · Design · Build · Voice". The output is a
self-contained HTML deck, **designed for this content**. The deck opens offline in a browser and
pages with arrows and the wheel. Speaker notes live in the presenter window and in the live notes
file `<slug>-notes.js`. The short path gives a one-page presentation without a presenter window,
in one go.

**Edit slides through Claude Design** — recommend it everywhere. On a Claude Design canvas and on a
review page the person comments right on a slide, and the agent sees which slide and element each
comment refers to. How it works and how to check that it is available: `stages/canvas.md`.

This file is the router: it decides the path and the stage to start from, and it holds the gates
between stages. The stages are in `${CLAUDE_SKILL_DIR}/stages/`, transcription of recordings is in
`stages/transcribe.md`. **Read a stage file only when you enter that stage.**
Paths `assets/…` and `stages/…` below are relative to `${CLAUDE_SKILL_DIR}`.

## Language

- **Talk to the person in the person's language** — the language of their messages. All templates
  in the skill files (questions, manual step blocks, final messages) are in English: say them in
  the person's language.
- **The deck content is in the person's language by default**: slide text, speaker notes,
  `slides.md`, `design.md`, `DECK.md`. The person asks for another language — write in it. A request
  to translate an existing deck is a refinement (`stages/build.md`): translate `slides.md` first,
  then rebuild.
- **Headings and markers in the person's files** are in the deck language: `## Pipeline` /
  `## Конвейер`, "Next step" / «Следующий шаг», `**On screen:**` / `**На экране:**`, stage names
  Context / Design / Build / Voice = Контекст / Дизайн / Сборка / Голос. Read them in any language,
  by meaning. Old Russian folders keep working.
- **The root tag `lang`** of the deck is the deck language. The kernel UI (presenter window, hints)
  follows it: Russian for `ru`, English for any other language.

## Philosophy (main)
**You are a presentation designer, not a template filler.** Different talks → visually different
decks (structure, palette, typography, background, motion), not one look in new colors.
- **The kernel `assets/kernel.html` (from THIS skill's assets, not from copies in the input folder)
  is copied VERBATIM** — navigation, animation, notes and PDF export stay intact. The only edits are
  the root tag `lang` and, on the short path, `data-presenter="off"`. All visuals go into its
  `<style id="design">` and into the slides in `#deck`.
- **`assets/design-axes.md`** — 9 design axes; **`assets/art-direction.md`** — how to read a brief
  and a reference; **`assets/cookbook.md`** — the kernel technical contract, offline fonts, media,
  checks; **`assets/deck-template.md`** — the `DECK.md` skeleton; **`assets/validate.py`** — the deck
  validator.
- **Self-containment (strict):** a finished deck is offline, with no network links. The canon is
  `cookbook.md`.
- **Do not invent content.** Speech is the person's words, numbers come from the materials. If
  something is missing, ask. One exception: in the "do it yourself" mode without material, you can
  write a draft speech from the idea. Mark it in `slides.md` as a model draft. Facts and numbers in
  it are only `[needed: …]`.

## Two paths

| | **Short** — one page | **Full** — a talk |
|---|---|---|
| When | show an idea in pictures, a one-off visual, a draft, a simple presentation | a talk that will be rehearsed and refined |
| Stages | one go: `stages/quick.md` | Context → Design → Build → Voice |
| Output | exactly one `<slug>.html` | working folder: `slides.md`, `design.md`, `DECK.md`, show folder `deck/` |
| Presenter window | none unless asked; the finish offers to add it | yes, with live notes |
| Claude Design | canvas only if asked; the review page is offered once after the build | canvas by default (style options → whole deck → HTML); the review page is offered once after the first build |
| Status | not kept | the Pipeline section in `DECK.md` |

## Intake (silent), then questions

First read `$ARGUMENTS` and the attachments — silently. If the arguments hold a path and a phrase,
separate the path; the phrase is the person's instruction (a new budget, "go on yourself", "enough"),
take it into account. For a folder, scan it (`Glob`/`Read`) and note:
- **`DECK.md`** → read it FIRST: the Pipeline section says where the work stopped, the rest are deck decisions;
- **`slides.md`** (or `content.md` / any `.md` split into slides) — the talk text;
- **`design.md`** (or `DESIGN.md`/`decision.md`/`brief.md` — save as `design.md`) — the brief;
- **recording** — `*.m4a/mp3/wav/mp4/mov`; **transcript** — `transcript*.md`, `rehearsal-*.md`;
- **media** — `*.png/jpg/jpeg/gif/webp/svg`, remember paths and sizes;
- **existing deck** — `*.html` with the `KERNEL v` marker in the head; **reference** — `reference.html`, a URL in the arguments;
- everything else is material: `.docx`, articles, a repo path (real numbers from `git log`), a topic, raw text.

Then questions — in one AskUserQuestion, only those without an answer:
1. **Path** — short or full. Phrase the options from what you saw ("a paragraph came in chat — this
   looks like one page"); the person decides. No question if there is a `DECK.md` (the path is full)
   or an existing deck (the path is known: refinement or promotion, `stages/build.md`).
2. **How we work** — "together" (the stages go through questions) or "do it yourself" (Claude passes
   the stage without questions and shows the result). Only for the full path. If Claude Design is
   available (`stages/canvas.md`) and the folder has no `design.md` yet, add a second question in
   the same AskUserQuestion: "Design on a Claude Design canvas (recommended)" / "Straight to HTML".
   Write the answer into the Pipeline section. The person can switch the mode at any stage with words like "go on yourself" / "let's do it together". "Do it yourself"
   stops only at manual steps and at the finish.
3. **Place** — only if not given. Full path: a folder is given → work in it; not given → offer 2-3
   paths (for example `<current directory>/<slug>/`) plus "my own". Short path: where to put the
   HTML (the current directory is a good first option).

Short path → read `stages/quick.md` and follow it. After that this file is needed only for
"Language" and "How to talk".

## Full path — route

**Which stage to start from** depends on what already exists. Check the table rows top to bottom;
the first match wins. Say in one line which stage you start from and why.

| What exists | Stage | File |
|---|---|---|
| the person says they left comments; `DECK.md` names a canvas or a review page | canvas before the transfer → Design; review page → Build, refinement | `stages/canvas.md`, then by stage |
| a run-through recording or text (`rehearsal-*`) that is not in the laps table of `DECK.md`, next to a built deck | Voice | `stages/rehearse.md` |
| `DECK.md` with a Pipeline section | the stage named in "Next step" | by stage |
| an existing deck, the person asks to finish it | Build → refinement | `stages/build.md` |
| `slides.md` and `design.md` | Build | `stages/build.md` |
| only `slides.md` | Design | `stages/design.md` |
| an idea, topic, text, materials, recording — no `slides.md` | Context | `stages/context.md` |

**At the start of the full path** create `DECK.md` in the working folder: the head and the Pipeline
section from `assets/deck-template.md` (work mode, budget, stages with status, next step). The Build
stage writes the other sections. "Next step" always starts with the stage name: "Voice — waiting
for the person: …".

**The time budget** lives in the Pipeline section — this is the main place; the head of `slides.md`
repeats it. If the person changes the budget mid-way, update both places and the estimate in the
Context row, then continue.

**Gates.** Each stage file ends with a "Stage gate" section. If the check fails, the next stage does
not start: fix it or ask. If it passes, update the Pipeline section and go to the next stage without
a separate "shall we go on?" question. In the "together" mode, say briefly that the stage is closed
and what comes next.

**Main rule:** do not build the deck until the working folder has BOTH files — `slides.md` and
`design.md`.

**Manual step** — something only the person can do: record a run-through, pick a style on refero,
add a picture. Format — three lines, then stop:
```
Your step: <what to do — one sentence>.
Put <what> into <folder>.
Then call /present <folder> — I will continue from the stage "<stage>".
```
If the stage gives details ("how to record a run-through"), they go as a short list right after the
first line. The manual step block is the last thing in the message: the stage result, the path to
the deck, controls and optional offers go above it. Before you stop, write into the Pipeline
section: "<stage> — waiting for the person: <what>" and "Next step". A new session reads this status
and continues from the same place without asking again.

**Finish of the full path** — when the person says "enough" after a Voice lap or declines the
run-through. "Do it yourself" does not choose the finish itself: only the person can do a
run-through, so after a lap the skill stops at the manual step "next run-through" and says that
"enough" is the finish. At the finish: the path to `deck/`, the timing of the last run-through
against the budget, a reminder: to take the talk with you, take the whole `deck/` folder.

## How to talk
- Language: the person's (see "Language"). Short between questions. All clarifications go through
  AskUserQuestion (2-4 options + "Other").
- Do not ask what is already in the materials or in the Pipeline section.
- Do not invent facts and numbers — take them from the materials or ask. From the network — only a
  reference URL and an OSS font with consent.
- Do not install packages yourself; if a tool is missing, say so and offer a workaround.
