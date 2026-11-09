# Speaker notes: speech, cues and audience discussion

For every slide with a presenter window, prepare three separate fields in the deck language.
The audience sees none of these fields. The presenter opens **Cues** by default; **Full text**
is the other tab. A separate **Discuss with the audience** block appears on both tabs.
Switching tabs preserves the choice while navigating; reopening the presenter starts with Cues.

## Writing the content

- **Full text** is the complete speech, with the speaker's wording, examples, transitions and
  stage directions. Keep the existing rules about sources, draft labels and missing facts.
- **Cues** cover every main thought the speaker intends to convey on this slide, in speaking
  order. Use a bullet list. Each bullet has a short, specific heading on its own line and
  **1–2 short sentences beneath it** to jog the speaker's memory. Put the explanation below
  the heading, not in parentheses. A glance at headings should recall the arc; the explanation
  should restore a forgotten thought. Do not copy the whole speech, merely repeat the on-screen
  text, or impose a fixed number of bullets that drops important thoughts. No new factual claims.
- **Discussion** is optional per slide. Consider it on every slide, but add it only when useful
  to the talk and audience: a question about their experience, a prediction before a reveal,
  a concrete example to debate, or a related detour. Prefer one focused question/topic, with
  a short facilitation prompt underneath: what to ask next or how to connect answers back to
  the slide. Do not invent audience answers, personal stories or facts. Preserve questions from
  the source speech, including any reveal/timing instructions. Optional suggested questions
  should be marked as suggestions in slides.md; do not silently turn them into the speaker's words.
  An empty Discussion is valid. Avoid generic filler questions on every slide.

Cues are derived from the speech; they do not replace it. Existing discussion in the speech may
stay there for context, but the common Discussion block is its visible reminder on both tabs.
Budget discussion pauses separately; do not count cues as additional spoken words.
After speech or slide-order changes, reconcile cues and discussion with the final content.
Preserve the person's edits in all three fields; ask about conflicts instead of overwriting them.

## Embedded fallback

Each slide stores HTML-escaped strings in `data-notes` (speech), `data-cues` and
`data-discussion` (optional). Cues and discussion are plain text, not HTML:

```text
- **Start with the audience's experience**
  Recall the familiar situation before explaining the mechanism. Connect it to the slide's example.
- **Explain the turning point**
  Name what changes and why it matters.
```

The first line of each bullet is its heading; following lines are its explanation. `-` and `*`
are accepted bullets; wrapping a heading in `**` is optional. HTML is displayed literally in these
lists. The common block has its own edit button. Editing the active tab changes only that field.
Tab switches and slide navigation apply the open edit; Cancel/Esc discard it.

## Live notes format (kernel v9)

Keep `window.DECK_NOTES` as a string, with `## NN · Title` slide sections. Inside each section:

```js
window.DECK_NOTES = String.raw`
## 01 · A familiar problem
### Cues
- **Recognize the situation**
  Recall the example from the speech. Explain why it matters to this audience.

### Full text
The complete speech… [pause]

### Discussion
- **When have you encountered this?**
  Invite one example, then connect it back to the slide.
`;
```

Russian headings: `### Тезисы`, `### Полный текст`, `### Обсудить с залом`.
Use these exact reserved headings in that order; `### Cues` / `### Тезисы` is the first line
of the section body. Empty Cues or Discussion is allowed by the runtime, but new talks must have
meaningful cues. Do not use backticks or `${` inside a String.raw payload.
The notes file, browser draft, all-notes editor, copy/download and revert preserve all three fields.
The file remains the source of truth; embedded fields are fallbacks when no file is available.

Legacy sections without the structured headings remain complete speech in Full text. Their
Cues and Discussion are empty, with an explicit empty-state message; the runtime does not
summarize speech automatically. On an authorized rebuild, derive cues from the current speech
and bring all three fields into this format. To add tabs to an old deck, rebuild on kernel v9;
installing the skill alone does not modify already generated decks.
