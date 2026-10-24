# Short path — a one-page presentation

`SKILL.md` sends you to this file when the person chose the short path: "show the idea in pictures",
a one-time visualisation, a draft, a simple presentation. There is no pipeline, no file set and no status here:
the path takes one go.

The short path is **a different process, not a worse deck**: the slides are still designed for the content,
the kernel is copied word for word, the deck stays offline and self-contained. It saves steps, not quality.

## Output

**Exactly one file** appears on the disk of the person:
```
where the person said/
└── <slug>.html            ← everything inside: kernel, styles, slides, media in base64
```
Keep drafts (text per slide, intermediate builds) in the scratchpad folder of the session and do **not**
put them next to the deck. Do not create `deck/`, `notes.js`, `DECK.md`, `slides.md`, `design.md`
or a build script: after the short path there is nothing to clean up.

Write the deck content (slide text, `<title>`, `data-notes` if any) in the person's language by default, or in the language
the person asked for.

## Presenter window — off by default

- A short path deck is built **without the presenter window**: `<html>` has `data-presenter="off"`
  (kernel v7+, `cookbook.md` → "Without the presenter window"), and the slides get no `data-notes`.
- Make the window at once only when the person asked for it directly: "with speaker notes", "with the presenter
  window", "I will give a talk with it". Then the attribute is not there, each slide has `data-notes`
  with speech from the material (do not invent your own speech), and there is no `notes.js` file: the speaker notes are embedded.
- If the material shows that this is a talk, but the person did not ask directly, still build without the window. In the final message
  the offer to add the window comes anyway (see "Finish").

## Steps

1. **Concept** — `stages/build.md`, Step 1, but axes 1, 4, 5 are enough (+9, if the content clearly asks for it).
   The answers are still your own, not "as usual". Keep the art direction in your head: there is no `DECK.md` here, and
   references "write it in `DECK.md`" from the assets do not apply on the short path. You lay out the text per slide
   yourself from the given material. If there is no material, do not invent facts and numbers: ask
   one question or make the slides without them. An illustration of a concept (a sample commit, a sample request)
   is not a fact — you can write it yourself.
   Do not name drafts in the scratchpad `slides.md`, `design.md`, `DECK.md`: if the validator finds these names
   next to the deck, it decides that this is the full path.
   If the person gave `design.md` or a URL reference, it is the art direction (`assets/art-direction.md`).
2. **Plan** — without confirmation: one line "building N slides, the arc is such-and-such" and the build at once.
   Do not discuss interactivity: if the content clearly asks for it, make one widget and mention it in the final message.
   If the content does not ask for it, the deck is static.
3. **Build** — `stages/build.md`, Step 4, items 1-3 and 4b, with these differences:
   - the introduction of Step 4 about the folder `deck/` and the build script in the working folder does not apply: build the file
     directly where the person said, intermediate files go to the scratchpad;
   - right after you copy the kernel, set the window switch and the deck language: replace `<html lang="en">` with
     `<html lang="<deck language>" data-presenter="off">` (if nobody asked for the window). In kernel v8 this line appears once;
   - item 3: the slides get **no** `data-notes` (if nobody asked for the window);
   - media — inline base64 only. Media heavier than ~800 KB breaks the single file: warn the person and
     offer to compress it or to go to the full path;
   - item 5 (`notes.js`) is skipped.
4. **Check** — `stages/build.md`, Step 5: shorter, but not shallower. The validator, `?check`, console
   errors, the layout auditor and the headless PDF print are mandatory IN FULL: the auditor costs one call for
   the whole deck. Only the frames are rationed: the title slide + all slides that the auditor flagged + the two or three
   densest slides. Do not skip the check silently. Start the server for Chrome in the folder where the file is,
   not in `deck/`. Skip the items of Step 5 about `DECK.md`, `deck/` and the layout: they do not exist here.
   If there is no claude-in-chrome extension, take the same branch as in Step 5: say so in the final message and ask the person to
   open the deck with `?check` and scroll through it with their eyes. This branch does not cancel the headless PDF print.

## Finish

- Give the path to the file and say that this is the whole deck: to send it, send one file.
- Remind the controls: `← →`/wheel/swipe — go through slides, `B` — black screen, `F` — fullscreen,
  `S` — PDF, `?check` in the address — highlight overflow. Mention `P` only if the window exists.
- **In the last line, offer the presenter window** (if there is none): "I can add a presenter window
  with speaker notes — for giving a talk with this deck. Shall I?". This is one line, not an AskUserQuestion question.

## Add the presenter window later

The person agreed or asked later:
1. Remove the attribute: `<html lang="<deck language>" data-presenter="off">` → `<html lang="<deck language>">` (this line appears once in the file).
2. Add `data-notes` to each slide: speech from the material and from the slide text, stage directions in `[brackets]`.
   If the material is not enough for the speech, ask. Do not invent.
3. Run the check from step 4 in full. The deck stays one file, `notes.js` is not needed.
4. Remind about `P`: it opens as a separate window. Do not share that window, share the deck.

## Refinement and promotion

- Refinement works on the same single file — `stages/build.md`, Step 6. Do not create the folder and the file set.
- If the person needs more — a talk, rehearsals, timing — this is promotion to the full path:
  `stages/build.md` → "Continue work on an existing deck" → "promotion to a full talk".
