# Stage Design — design.md

`SKILL.md` sends you to this file when the working folder of the full path has no `design.md`. The
output is `design.md`: a brief that says how everything must look (palette, fonts, shapes, spacing,
Do/Don't rules). Do not lay out slides at this stage: choose the style. The same `slides.md` under
three different briefs gives three different decks, so `design.md` is the main file, not a
decoration.

If a brief came under a different name (`DESIGN.md`, `decision.md`, `brief.md`), save it as
`design.md` and go to the gate.

## Three roads

Offer them with one AskUserQuestion. Write the options for this talk:

- **A ready style from styles.refero.design** — the main road. This is a manual step: the person
  sees how the style looks live, downloads its `DESIGN.md` and puts it into the working folder. Say
  where to put it and how to continue, and stop. Other free sources — `assets/art-direction.md`,
  "Sources of references".
- **Own brief from an interview** — 3-4 questions: mood and look, light or dark, brand colors, a
  font or "your choice". Collect the answers into `design.md` by the sample below.
- **From a reference** — the person gave a site URL or an image: extract the design DNA (`defuddle`
  → `WebFetch`, see `art-direction.md`) and write it as `design.md`.

**"Do it yourself":** do not ask about the road. Go through the axes from `assets/design-axes.md` for
this `slides.md` (your own answers, not "as usual"), choose the art direction and write it as
`design.md`. In one or two sentences, show what you chose and why it fits this talk.

## What design.md must contain

The format sample is `${CLAUDE_SKILL_DIR}/example/design.md` (an export of the Playful style from
refero). The sample is in Russian; the format is the same in any language. Minimum:
- **Theme:** light or dark, one sentence of mood.
- **Palette:** a table of tokens `name · hex · role`, one or two accents.
- **Typography:** typeface (and a system or OSS substitute), weights, size scale.
- **Shapes and rhythm:** radii, shadows, spacing, density.
- **Do / Don't:** what to do and what not to do.

## Stage gate

- `design.md` is in the working folder;
- it has a palette with hex values, a typeface and Do/Don't rules. If something is missing, add it
  together with the person or yourself ("do it yourself") and say what you added;
- if the brief depends on a specific font → ask one time: embed an OSS analogue as base64 (the
  deck stays offline) or take a system substitute (the default is the system one). The recipe is
  in `cookbook.md`.

Then update the Pipeline section of `DECK.md`: "Design — done", summary "source: refero "<style>" /
interview / reference / self". The next stage is Build.

## Claude Design — an option

Claude Design is not necessary at this stage, and the gate does not depend on it. After the first
build (stage Build, Step 7), the skill offers one time to run the deck together with `design.md`
through Claude Design: it suggests its own solution, and then the edits are moved into the deck
sources and rebuilt.
