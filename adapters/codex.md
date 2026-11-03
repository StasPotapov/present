# Codex adapter

Use the shared workflow in the current Codex session. For a clone, use
`python3 -B scripts/present.py setup --client codex --install-skills` from the
resolved package; this links complete `present` and `present-setup` directories into
`~/.agents/skills/`. A managed installation must be updated by its owner.

Discover file/shell/image/browser tools in the current session. Desktop may expose
`exec_command`, `view_image`, `cua_repl` and `open_in_codex`; these are examples to
verify, not universal Codex APIs. Follow the browser tool's initialization contract.
An available question tool may return asynchronously: required answers gate work.

Use `stages/codex-design.md` for design and review. The baseline is a local HTML
preview in a browser panel, reusing the same URL after edits. Optional native
Presentations, Pages visualizations and Sites are discovered separately. The
presence of `artifact_session.js` alone does not prove saved presentation creation
or connection is available. Do not invoke Claude login commands in Codex.

For browser QA, run the shared cookbook DOM checks only through a tool whose
documented API allows those operations. If the browser restricts script execution,
use supported interaction and screenshots, report the unperformed DOM audit, and
keep the local validator/PDF checks. Do not bypass tool restrictions through another
channel. Missing Claude in Chrome is not a missing Codex browser.

No subprocess calls to `codex exec` or `claude`; no model configuration is installed.
Discovery after reload, browser interaction, images and connector access are separate
checks. CLI-only Codex can still build the local deck without desktop preview.
