# Example: the short path

The deck is in Russian: the request that built it was in Russian, and the skill writes the deck in the person's language. The short path works the same in any language.

A deck of 6 slides about the shortest path of `/present`, built by `stages/quick.md`. The short path gives exactly one file, and here it is:

```bash
open present-korotkiy-put.html
```

The file opens offline and is 76 KB: it holds the kernel, the styles and the slides. To turn slides, use `←` `→`, the mouse wheel or a swipe. `B` shows a black screen, `F` turns on fullscreen, `S` exports to PDF. `?check` in the address highlights overflow.

The deck has no presenter window: `<html>` has `data-presenter="off"`, the `P` key opens nothing, and the deck has no speaker notes. This is the default of the short path. At the end, the skill offers in one line to add the window with speaker notes.

## The request that built it

```
/present Сделай простую презентацию на 6 слайдов: что такое короткий путь скилла present.
Когда его брать, что получается на диске, какие шаги проходит скилл, почему нет окна
докладчика и как раскрутить такую деку до доклада.
```

In English:

```
/present Make a simple presentation of 6 slides: what the short path of the present skill is.
When to use it, what you get on disk, which steps the skill goes through, why there is no
presenter window, and how to promote such a deck to a full talk.
```

For this request, the skill asks two questions: the path (short) and where to put the file. Then it builds the deck and checks it: the validator, `?check`, the layout auditor, frames in Chrome, a headless PDF print. This deck passed all five checks.

## How it differs from `../example/`

| | `example-quick/` | `example/` |
|---|---|---|
| Path | short | full |
| Files | one `.html` | working folder: `slides.md`, `design.md`, `DECK.md`, `build.py`, `src/`, `deck/` |
| Presenter window | no | yes, with live notes |
| Pipeline status | not kept | the Pipeline section in `DECK.md` |

This `README.md` is documentation of the repository. On the short path the skill itself puts nothing next to the deck.

The slide text was written for this repository and the MIT license covers it together with the skill.
