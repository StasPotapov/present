# Stage Context — material → slides.md

`SKILL.md` sends you to this file when the working folder of the full path has no `slides.md`. The
source of the material does not matter: the output of this stage is `slides.md` in the working
folder. This stage has no design.

## Entry: three roads

Choose the road from what you saw during intake. If it is not clear, ask with one AskUserQuestion
(write the options for this material; in "do it yourself", choose yourself and say it in one line).

- **Invent together** — there is only an idea or a topic. The talk is invented together with the model.
- **Lay out what exists** — the full talk already exists: dictation in the chat, a transcript of a
  recording, a text, articles, documents (`.docx` — snippet in `cookbook.md`), a presentation by
  someone else, a repository (real numbers from `git log` — `cookbook.md`, "Numbers from a
  repository"). The model lays out the material. It does not invent it.
- **Transcribe a recording** — the folder has audio or video (`*.m4a`, `*.mp3`, `*.wav`, `*.mp4`, `*.mov`),
  or the person wants to dictate the talk to a recording. First transcribe (`stages/transcribe.md`), then take the road "Lay out what exists".

If the person wants to dictate but there is no recording yet, this is a manual step: say what to
record with (Handy or the built-in macOS dictation directly into the chat, a dictaphone,
OpenSuperWhisper), where to put the file and how to continue. Then stop.

## First — budget and audience

One AskUserQuestion, only about what you cannot get from the material:
- **time budget** (10 / 20 / 30 minutes or a custom value);
- **audience** and **goal** of the talk — one sentence each.
Write the answer into the Pipeline section of `DECK.md` and into the header of `slides.md`. In "do it
yourself": if the budget is not given, take 20 minutes and write in both places that this is an
assumption.

## Road "Invent together"

Interview with AskUserQuestion, 2-4 options + "Other", one block of questions at a time:
1. Main idea: what the audience must take away (one or two things).
2. Arc: how to start (a pain, a story, a question), where to arrive, where the turn is.
3. Supports: which facts, numbers, examples, demos the person has. No numbers — the slide has no numbers. Do not invent them.
4. Storyboard draft: show the list of slides "No. · title · thesis" and ask "OK / edits".
5. Speech per slide: offer the person to dictate it into the chat along the storyboard. If the
   person dictates, you lay it out. If the person asks you to write it, write a speech draft from
   the person's own answers. Mark in `slides.md` that the speech is a model draft and must get a
   run-through aloud (stage Voice).

**"Do it yourself" on this road:** there is no interview and no answers from the person. Invent the
arc and the storyboard from the idea, write a speech draft and mark in the header of `slides.md`:
"speech is a model draft, do a run-through aloud". Do not invent facts, numbers, names or stories
from the person's life: put `[needed: …]` in their place. These marks do not block the stage gate;
their list goes into the stage summary. You can write illustrations of a concept (a code example,
a dialogue example).

Speaking is easier than typing: the person does not correct themselves in the middle of a word.
Offer this one time.

## Road "Lay out what exists"

1. Divide the material into slides: one idea — one slide, each with a thesis and speech.
2. The speech is **the person's words**, only cleaned: remove repetitions and filler words, keep
   the stories, the intonation and the asides that matter. Do not add your own text. If something
   is missing to connect the parts, mark it `[needed: …]` and ask.
3. Show the storyboard "No. · title · thesis · ~time" and ask "OK / edits".
   "Do it yourself": do not ask, save and show the result.

## slides.md format

Header: topic, budget, audience, goal, pace, timing total. Then the slides, separated by `---`:
```
## 01 · Slide title · ~0:40

**On screen:** what the audience sees — short, no layout.

> The speaker's speech word for word, as the speaker will say it aloud.
> `[note: pause, demo, action]`
```
Write the headings and markers in the person's language (Russian: `**На экране:**`). The format
sample is `${CLAUDE_SKILL_DIR}/example/slides.md`. The sample is in Russian; the format is the same
in any language.

## Stage gate

The stage is finished when all of these are true:
- `slides.md` is saved in the working folder;
- each slide has a title, "On screen" and speech;
- there are no `[needed: …]` marks without an answer (or the person said "leave it as is"; in "do it
  yourself", the marks are listed in the stage summary);
- the **timing** is calculated: speech words / pace + pauses and demos. Before the first
  run-through, the pace is an assumption of ~125 words/min (the skill example is calculated with
  it). Write this in the header directly. The example is a Russian talk; for any language the value
  stays an assumption until the first run-through. After a run-through, the pace comes
  from the real recording (stage Voice).
- the estimate fits the budget. If it does not fit, say how much is extra and suggest which slides
  to shorten or remove. The person decides; in "do it yourself", shorten them yourself and show
  what you removed.

Then update the Pipeline section of `DECK.md`: "Context — done", summary "N slides, estimate ~M min".
The next stage is Design (if `design.md` already exists → go directly to Build).
