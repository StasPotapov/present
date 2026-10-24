# Example: a deck built by this skill

The deck is in Russian: it is a real talk given in Russian. The folder layout, the file formats and the pipeline are the same in any language.

A real talk «Контекст. Дизайн. Голос. — как я делаю доклады с /present» ("Context. Design. Voice. — how I make talks with /present"), 16 slides, ~13:35 of speech. It went through the whole pipeline by hand, before the skill learned to run the pipeline itself: dictated into a voice recorder → transcribed → laid out into slides in BMAD → `design.md` taken from styles.refero.design (the Playful style) → built by this skill → refined in Claude Design.

Now one call does the same route. Put the material in a folder and say `/present <folder>`. The skill asks for the path and the work mode, leads you through the stages Context → Design → Build → Voice, and stops where it needs your step, for example to record a run-through. The Pipeline section in [`DECK.md`](DECK.md) shows what the status of such a route looks like (the heading there is the Russian `## Конвейер`).

Slide 09 is interactive: you can click the previews of three earlier decks, and the deck changes to the palette of the selected one right on screen. It is also an example of why the deck needs kernel `v6` or newer.

An example of the short path, one page without the presenter window, is next to this folder, in [`../example-quick/`](../example-quick/).

This folder is also a sample of the correct folder layout: `deck/` is the self-contained show folder, everything else is working material.

## View

```bash
open deck/kontekst-dizayn-golos-2026-07-28.html
```

The file opens offline and does not need the network. To turn slides, use `←` `→`, the mouse wheel or a swipe. `P` opens the presenter window with speaker notes (in a separate window), `S` exports to PDF, `B` shows a black screen, `F` turns on fullscreen. Add `?check` to the address, and the kernel highlights slides with overflow.

To take the talk with you, take the whole `deck/` folder. The HTML and its `notes.js` must be in the same folder, or the live notes do not load (the HTML keeps an embedded fallback copy).

## What is here

| File | Role |
|---|---|
| `deck/kontekst-dizayn-golos-2026-07-28.html` | the deck, 862 KB: four images and the Inter font are embedded as base64 |
| `deck/kontekst-dizayn-golos-2026-07-28-notes.js` | live speaker notes — the source of truth, you edit them directly in the presenter window |
| `slides.md` | **input 1:** slide text + speaker notes, version 2.2 — made from a run-through on a voice recorder, the speech is trimmed |
| `design.md` | **input 2:** the design brief, an export of the Playful style from styles.refero.design |
| `DECK.md` | the manifest: pipeline status, slide map, art direction, decisions with their "why" |
| `build.py`, `src/` | deck mode "script": you edit the sources, and `python3 build.py` rebuilds the deck |
| `deck-0*.jpg` | screenshots of three earlier decks — the build embeds them into slide 09 |
| `refero-scroll.jpg` | the scrolling catalog of styles.refero.design — the build embeds it into the browser window on slide 08 |
| `src/interactive.js` | the slide 09 widget: the palettes of three decks and the live change of the deck palette |
| `slides-cut-15-two-circles.html` | an archive of the removed slide "two circles" with the steps to bring it back — an example of how to remove a slide without losing it |
| `src/kernel-v8.html` | a copy of the kernel — the fallback for a build without the installed skill |

`build.py` takes the kernel from the assets of the installed skill (`~/.claude/skills/present/assets/kernel.html`). If the skill is not installed, it takes `src/kernel-v8.html`, a copy in this folder. So `python3 build.py` builds the deck also for a person who only cloned the repository. Only `transcript.md` and the audio recording of the run-through were not copied. The kit still works without them, but the manifest names them as part of the working folder.

The slide content is the author's personal talk. Use it as a sample of the format and the layout, not as text to reuse. What the MIT license covers and what it does not cover is in [`NOTICE.md`](NOTICE.md).
