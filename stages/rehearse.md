# Stage Voice — run-through aloud → a sharper slides.md

`SKILL.md` sends you to this file when the deck is built and the person is ready for a run-through
of the talk, or when a new run-through recording appears in the working folder. When the deck is
ready, people usually stop here, but the most valuable part is still ahead: a run-through shows
**how long the talk really takes** and **where the person loses the thread**. Where the person
starts to mumble, the slide is bad, not the person.

Each lap of this stage is one run-through. The number of laps is not limited: with each lap the
talk becomes shorter and sharper, and nothing is rebuilt from zero.

## Step 1 — Run-through (manual step)

If the folder has no new run-through → this is a manual step by the rule from `SKILL.md`. The
essence in one line: open the deck (`open deck/<file>.html`) and go through the slides aloud in
your own words, as if the audience is already in the room; if you make a mistake, say it aloud
immediately. Then, briefly, as a list, offer the ways — the person chooses:
- **by voice directly here** — dictation types the speech into the chat input field: Handy, the
  built-in macOS dictation or any other. The timer of the presenter window shows the run-through
  time;
- **dictaphone → I transcribe** — a recording on the computer or the phone, the file goes into the
  folder as `rehearsal-<N>.m4a` (or another extension). Always offer this way. If the machine has
  no transcription by `stages/transcribe.md`, items 1-2, add to this way: "for this you need
  whisper (`whisper-cli` with a model) or another local speech recognizer — install it if you
  want this way". Do not install it yourself;
- **dictaphone → you transcribe** — Handy, whisper or OpenSuperWhisper. Paste the text here or put
  it as the file `rehearsal-<N>.md`, and tell the run-through duration.
The "Put …" line of the manual step block: "Put the recording or the text into <folder> — or paste the text here".
Say these templates in the person's language.
Update the Pipeline section: "Voice — waiting for the person: run-through <N>". Stop.

If the run-through text came (in the chat or as an `.md` file), no transcription is necessary. Save
text from the chat as `rehearsal-<N>.md`. If the duration is not given, ask. If the person does not
know it either, the pace stays an assumption, write "duration unknown" in the laps table, and
compare with the budget by the estimate from the words. Then go to Step 3; calculate the pace from
Step 2 with this duration.

## Step 2 — Transcript

- Transcribe the recording by `stages/transcribe.md`. The text goes next to it as `<recording name>.md`.
- Recording duration: `afinfo <file> | grep duration` (macOS) or `ffprobe` if it is available. If
  this fails, ask the person.
- Pace = all words of the transcript, with fillers and repetitions, / minutes of the recording:
  this is the real pace of the person. Write it into the header of `slides.md` and into the
  Pipeline section instead of the assumption.

## Step 3 — Edit to the budget

1. Match the transcript to the slides: which part of the speech belongs to which slide. Where the
   border is not clear, use the titles and "On screen".
2. Calculate the time per slide: from the timecodes of the transcript, and without them — from the
   share of the slide's words in the recording. Compare the total with the budget from the Pipeline
   section (the person can change the budget in the same call — see `SKILL.md`).
3. Edit the speech in `slides.md`:
   - **the person's words**, only cleaned: remove filler words, repetitions, over-explanations and
     what the screen already shows. Do not add your own wording;
   - what the person said in the run-through but `slides.md` does not have — add it in the person's words;
   - what the person said aloud as a mistake ("wrong slide here", "remove this") — do it;
   - if it does not fit the budget, shorten what the audience will not miss; tell how much you
     removed on each slide;
   - list the places where the person lost the thread (pauses, "uhm", restarts) in the lap summary
     and in the lap row in `DECK.md`: the slide or its speech needs an edit there. Suggest an edit;
     do not decide for the person.
4. Show the diff of `slides.md` and the summary: "was M:SS, now ~M:SS with budget B". Ask "apply / edits".
   **"Do it yourself":** apply and show the summary.
   If the person said "the structure must change" (slides in a different order, a new slide), this
   is a structure edit: do it in `slides.md`, it goes into the deck at the rebuild.

## Step 4 — Rebuild

`stages/build.md`, Step 6 (refinement), without offers to "tweak the palette": the speech changes.
**First find the person's edits:** compare the sections of `<slug>-notes.js` with `data-notes` of
the current deck — the differences are the person's edits in the presenter window. The new speech
from `slides.md` goes into `notes.js` and `data-notes`; do not overwrite the person's edits — move
them, or ask if they conflict with the new speech.
The check is the same as after any refinement: the validator, the auditor in Chrome (text length
changes the layout only where the speech is visible on the slide, but the auditor costs one call)
and the PDF, if the text on the slides changed.
If `DECK.md` names a review page in Claude Design, republish it to the same URL (`stages/canvas.md`,
"The review page"), so the comments stay on the current deck.

## Step 5 — End of lap

- Add a row to the Voice laps table in `DECK.md`: number, date, recording, duration, budget, what
  was done, where the person lost the thread. Update the estimate in the Context row and the pace
  in the header of the Pipeline section.
- Offer: the next lap (a new run-through) or the finish. Finish → "Voice — done" and the finish from
  `SKILL.md`. If the person is silent or the mode is "do it yourself", the next step is "Voice —
  waiting for the person: run-through <N+1>"; in the manual step block, add the line "or say
  "enough" — we will finish". Match the person's answer by meaning, in any language.
- Suggest the small lap: the person can edit the wording directly in the presenter window during
  the rehearsal (double-click on the text → apply → "⤓ notes.js" → put the file next to the deck).
  No editor and no rebuild. The big lap is this stage: what I say, the order, the structure.
