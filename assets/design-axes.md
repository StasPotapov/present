# Design axes — what to decide before the build

Decks came out the same because the assets had a ready sample and the agent recolored it: a dark
background `#0a0b0f`, a drifting aurora, kicker-title-lead on each slide, the same pipeline.
The sample is removed. What remains is this — **a list of questions, not a catalog of answers**.

Below there is no ready solution, and this is intentional: the examples of options come in twos
and threes only to show the range, not to choose from them. The answer is invented for the specific talk.

**How to use:** go through the axes before the build and write down a one-line answer for each
(this is your art direction; on the full path it also goes into `DECK.md`). "As usual" is not an
answer; if you have nothing to say on an axis except the default, the axis is not thought through.

---

## Axis 1 — Frame composition

Where on the screen does the meaning live? One dominant scheme per deck + two or three contrasting
ones for accent slides. (Range: a poster in the center ↔ a narrow column at the edge ↔ a screen cut in half.)

Three slides in a row with the same silhouette are a sign that the axis is not done. Check this
on the storyboard before the layout.

## Axis 2 — Margins and alignment

How much air, and to which side is the text pressed? Tight and businesslike ↔ huge manifesto
margins; centered ↔ left-aligned ↔ right-aligned (rare, and so fresh). A title cut by the screen
edge is a technique.

## Axis 3 — Typography

One system for the whole deck. What exactly carries the character: the contrast of two families,
the weight difference within one grotesque, only mono, an extreme difference in sizes? Tune
`line-height`, `letter-spacing`, case and column width — they change the face more than the choice
of typeface. What is available offline is in `cookbook.md`; which of it to take is the decision of
this axis.

## Axis 4 — Color

Which logic, not "which colors": one accent that always means the same thing ↔ two colors that
divide the screen ↔ a color fixed to an act of the talk ↔ a lightness inversion between parts. A
dark deck is a conscious choice for the topic, not a starting point: if the topic is not about
night, a terminal or cinema, start with a light one.

## Axis 5 — Background `#bg`

An empty background is a valid and often the best answer. If there is a background, it must mean
something (material, environment, rhythm), not be wallpaper. Animate it only when the motion
carries meaning: motion on a slide must belong to the content. Any animation is turned off in
`prefers-reduced-motion`.

## Axis 6 — Motion

Two different decisions: **the transition between slides** and **the appearance inside a slide**.

The transition is overridden in the design layer — the kernel allows this, a rule with the same
name overrides the base one (verified):
```css
@keyframes slidefade{ /* your own entry character; clip-path, scale and "no motion at all" all work */ }
```
Duration and curve are also part of the character. Inside a slide: how much motion the deck gets
at all, and which exactly one technique is the "signature". Expensive animations — one or two for
the whole deck.

## Axis 7 — Details

What runs through the whole deck as a system: rules, act numbers, corner marks, underlines — or
nothing. One technique reads as handwriting, three different ones read as a mess.

## Axis 8 — Deck chrome

`#bar`, `#counter`, `#hint` are part of the visuals, not service parts: the bar thickness, color,
opacity and hint font follow the art direction. **Only the styling** changes; the DOM and the
kernel script do not.

## Axis 9 — Interactivity

HTML can do what PDF cannot: you can click it. The question of this axis — **does this deck have
a moment where the audience understands more if something happens on their command, not by
itself**. If there is no such moment, the axis closes with the answer "the deck is static", and
this is a full answer.

What to decide if there is such a moment:

- **Who clicks.** The speaker on stage — one movement, a large zone, works from two meters away
  and needs no aiming. A reader who opened the link alone — it can be finer and deeper, the reader
  has time. One deck is almost always about one of them; choose which.
- **What the click adds to understanding.** Interaction is justified when it changes the idea of
  the slide: the audience sees a consequence that a static frame does not show. If after the click
  exactly the same thing is said, only with motion, it is an animation, not interactivity, and it
  belongs to axis 6.
- **The slide reads without a click.** Nobody touched it — the idea still got through.
  Interactivity proves, deepens, answers a question from the audience, but it is not a condition of
  understanding: at a rehearsal, in a PDF and on someone else's laptop there can be nobody to click.

(The range, to show the amplitude, not to choose from it: a "before/after" state toggle; a
parameter the audience turns and sees how the consequence changes; opening data that did not fit
into the frame; choosing the branch the story takes next.)

**The dose is the same as for expensive animation: one or two interactive slides for the whole
deck, not more than one widget per slide.** A deck where everything is clickable reads as a form,
not as a talk.

Excess and relapses on this axis: hover effects (a projector has no cursor, a tablet has no
hover); small hit zones you have to aim at with the mouse; a slide that is unclear without a
click; interactivity that replaces a ready kernel animator (counter, cascade, pipeline) without a
reason.

The technical part is the section "Interactivity: the kernel contract" in `cookbook.md`: where to
write the JS, what the kernel does for you and what stays on you (reset on entering the slide,
keyboard, behavior in PDF).

---

## What counts as a relapse

These decisions were already in many decks and are not used by default. Any of them is allowed,
but with a reason written in `DECK.md` (on the short path — said in the finish):

- a dark background near `#0a0b0f` with the surface `#14161f`, amber `#f5b942`, green `#4ade80`;
- drifting blurred blobs in `#bg`;
- a mono kicker in caps with wide tracking above each title;
- the same structure "kicker → h1 → lead" on most slides;
- the base slide transition left as is, when the deck needs character.

## Link to the brief

If `design.md` came, it has priority over the axes: it sets the palette, typography, components.
But a brief is almost always silent about composition, background, transition and chrome — these
axes are still yours. If there is no brief and an interview collects it, ask about axes 1, 4 and 5
(composition, color, background): the person feels these, and asking about tracking makes no sense.
