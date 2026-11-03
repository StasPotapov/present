# Design and review in Codex

This replaces the Claude Design recommendation in Codex. Discover available tools
and installed skills at runtime. Do not assume ChatGPT features exist in every Codex
surface. Use one of these routes according to the requested output and capabilities.

| Need | Codex route | Boundary |
|---|---|---|
| Design options and the actual offline HTML deck | Local HTML preview in the Codex browser panel | Default for present; no hosted service |
| A small interactive style comparison in chat | Installed `visualize` skill | Optional sketch, not the finished deck/kernel |
| Editable native slides in ChatGPT/Spaces | Installed Presentations skill and saved-artifact creation/connection tools | Explicit alternative output; not an HTML export API |
| A saved HTML review page with comments | Pages plus its HTML visualization and comment tools | Hosted copy; block comments, not guaranteed slide anchors |
| A hosted interactive deck/site | Sites plugin | Explicit hosted route; publication and access follow Sites |

## Default: design options and local preview

1. Full path: read `slides.md`; short path: use the supplied material without creating
   a file set. Read the user's references and the shared design axes. In "together"
   mode, create a scratch HTML comparison with 2–3 distinct style options, each showing
   a title and a dense content slide with real text. In "do it yourself", choose one
   and continue. A comparison is a temporary sketch outside the final deck folder;
   do not modify the kernel to turn it into an editor.
2. Serve the task-owned preview directory on loopback, with a retained shell session:
   `python3 -m http.server <available-port> --bind 127.0.0.1 --directory <directory>`.
   Check a successful HTTP response, then discover `open_in_codex` and open a browser
   target with that exact URL. Follow the current tool schema. Reuse the URL and panel
   after edits. A `queued` result is not proof the panel opened: inspect the current
   browser state. If necessary, use its documented create-tab API (for example
   `cua.createBrowserTab` for the in-app browser) and verify visible content.
   In remote environments use supported forwarding, never assume the
   user's loopback reaches the executor. Without a preview tool, return the local file.
3. Get the user's style choice in "together" mode. Full path: save `design.md`, then build the
   full deck by `stages/build.md` and show its preview. Short path: keep design choices
   in the scratchpad and build only the requested HTML by `stages/quick.md`. Feedback is by slide number
   and description in chat; native element annotations are not claimed. Keep the
   selected surface in `DECK.md` as `local-html` and its file path on the full path;
   short-path state stays in the chat. A server URL is
   session-local; restart the owned preview when resuming, not an unrelated server.
4. Run the validator, available browser checks and PDF checks. Keep the preview alive
   while reviewing; stop only servers owned by this task when no longer needed.
   A preview opening successfully is not proof of visual correctness.

## Native presentation artifact (when requested)

Read the installed Presentations skill and its Artifact Sessions reference. Discover
all required capabilities: saved presentation creation, connection/read, editing and
rendering. For a new saved deck, the documented route is `create_spaces_artifact`, then
`connect_spaces_artifact`, then `artifact_session.js` using the returned `artifactRef`.
These names are discovery hints: if creation/connection is absent, a bare session
editor does not fill that gap. Reuse observed IDs; never manufacture an artifactRef.

Offer this as an editable presentation destination or an explicitly requested design
prototype. Explain that it does not preserve present's HTML presenter window, live
notes, animations or offline kernel automatically. Follow the Presentations skill's
own output contract if this replaces the HTML deliverable. If the user still wants
HTML from an approved prototype, read current content, record it in `slides.md` and
`design.md`, and rebuild with present's kernel. Inspect the result; do not claim
lossless import/export or automatic synchronization.

If the native route is unavailable, say which capability is missing and continue with
the existing HTML route unless the person explicitly requires native slides. Do not
silently create a PPTX instead of the requested present HTML.

## Saved review Page with comments (opt-in)

Read the installed Pages authoring skill before using it. Create or reuse the exact
Page requested for this deck. Read its current content/guidance before writing. Use
`create_page_visualization` only if discovered and the HTML fits its current size limit
(observed API: 256 KiB UTF-8). Use the exact returned visualization reference and
observed block ID/hash for updates; retain Page ID and reference in `DECK.md`. Read back
an uncertain write before retrying. Do not upload local absolute paths as references.

The Page is a review copy, not the offline show file. Sandbox restrictions may disable
popups, printing, downloads and sidecar notes/media. If needed, prepare an explicitly
labeled static review copy outside `deck/`, with slide numbers and embedded assets;
never alter the final kernel to work around a host sandbox. Do not truncate an oversize
deck. Offer local preview or a separately chosen Sites route instead.

Read Page comments using the actual comment tool. They may anchor a whole block:
include slide numbers in the review copy and ask for clarification when necessary.
After authorized edits, update the sources, rebuild and replace the same visualization
block. Replies/resolution require the authorized comment workflow. No promise of
Claude-style element anchors, manual canvas editing or privacy inferred from a title.

## Hosted Site (opt-in)

Read the installed Sites skill. Pass the explicit scope: local-only preview when no
hosting was requested, or the user's chosen publication/access for a hosted deck.
A local preview does not call create_site, push source or deploy. A hosted route uses
Sites' source/version/deployment workflow and returned IDs. Reuse existing hosting
metadata, preserve audience, and verify deployment before returning its URL.

Package a separate show copy with relative assets; disclose embedded speaker notes
before uploading. The offline deck remains usable independently. Sites provides
hosting; slide annotations and native presentation editing are not assumed.
