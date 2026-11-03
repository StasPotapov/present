# Stage Design — design.md

`SKILL.md` sends you to this file when the working folder of the full path has no `design.md`. The
output is `design.md`: a brief that says how everything must look (palette, fonts, shapes, spacing,
Do/Don't rules). Do not lay out slides at this stage: choose the style. The same `slides.md` under
three different briefs gives three different decks, so `design.md` is the main file, not a
decoration.

If a brief came under a different name (`DESIGN.md`, `decision.md`, `brief.md`), save it as
`design.md`. If the Pipeline says the design goes on the canvas, the brief is input for the canvas
(below); otherwise go to the gate.

## Road "Design preview" — current host

Read `stages/canvas.md` and select the current host's surface: Codex local HTML preview or
optional native artifacts, Claude Code with its verified Claude Design connector. Follow that
route for style options and review; save the chosen style in `design.md`. Do not promise
manual canvas editing or element comments unless that particular surface supports them.

A brief the person already has is input for the canvas, not a separate road: a `DESIGN.md` from
refero, a reference URL, brand colors — round 1 draws its options inside that brief.

## Three roads without the canvas

Use them when no design preview is available or the person chose "straight to HTML". Offer them
with one available question-tool call (or ask in chat). Write the options for this talk:

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
`design.md`. In one or two sentences, show what you chose and why it fits this talk. On the canvas
road the same axes decide the one look you draw.

## What design.md must contain

The format sample is `<real-skill-root>/example/design.md` (an export of the Playful style from
refero). The sample is in Russian; the format is the same in any language. Minimum:
- **Theme:** light or dark, one sentence of mood.
- **Palette:** a table of tokens `name · hex · role`, one or two accents.
- **Typography:** typeface (and a system or OSS substitute), weights, size scale.
- **Shapes and rhythm:** radii, shadows, spacing, density.
- **Do / Don't:** what to do and what not to do.

## Stage gate

- `design.md` is in the working folder;
- preview road: the surface and path/returned ID are in `DECK.md`, the relevant preview is ready, and the person said
  it is ready (or the mode is "do it yourself");
- it has a palette with hex values, a typeface and Do/Don't rules. If something is missing, add it
  together with the person or yourself ("do it yourself") and say what you added;
- if the brief depends on a specific font → ask one time: embed an OSS analogue as base64 (the
  deck stays offline) or take a system substitute (the default is the system one). The recipe is
  in `cookbook.md`.

Then update the Pipeline section of `DECK.md`: "Design — done", summary "source: local preview / native artifact <id> / Claude Design canvas <url> /
refero "<style>" / interview / reference / self". The next stage is Build.
