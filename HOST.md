# Host capability contract

Resolve the real directory containing this skill once per run and keep the whole
package: `stages/`, `assets/`, `adapters/`, `scripts/` and `setup/`. A copied SKILL.md
is not an installation. Outputs, temporary files and credentials belong outside the
package. Use Python with `-B`; `scripts/present.py --help`, `--version`, `doctor`,
`setup` and `validate` do not invoke Codex, Claude or any model.

Read the adapter for the actual session: `adapters/codex.md` or
`adapters/claude-code.md`. Unknown hosts can use the local files/validator, but their
UI integration remains unsupported until verified. Never identify a session by
presence of a CLI executable or translate model names across providers.

The shared workflow is `SKILL.md` and `stages/`. Present has no independent model
roles: the current session does the work. No role launcher, fixed model, private
model configuration or AI subprocess is needed. Do not split the stages into new
agents as part of setup. External skills retain their own execution contracts.

Discover tools and inspect their current schemas. Read/Bash/Glob/WebFetch/Skill in
old examples denote capabilities, not required names. Read an installed skill's
instructions and use the host's normal invocation. The scratchpad is a task-owned
temporary directory outside the skill and deliverable, not a Claude-specific path.

The portable baseline needs file access and shell for local HTML authoring. No shell
means no local build here. Questions use the session's supported question API, or
chat. With asynchronous questions, wait for required answers before dependent work.
Use actual image tools for pixels; a DOM audit is not visual QA. Without browser
control, image viewing or a PDF renderer, state exactly which checks were skipped.
Background shell sessions are optional: synchronous commands may use a suitable
timeout. Do not promise work continues after the chat is closed.

Design is routed through `stages/canvas.md`. Preserve the offline HTML kernel and
notes contract on both clients. Design surfaces are optional, not interchangeable
APIs: no invented Artifact call, automatic login, or implicit publishing. Connector
availability is session evidence, never a saved preference or CLI dependency check.
Keep a selected surface and returned IDs in the talk's `DECK.md`; short-path state
stays in the chat/scratchpad. Reuse them on continuation and check access again.

Setup never installs clients, browsers, plugins or hooks, changes authentication,
publishes content, or requires AI Workspace. Use the existing delivery owner for
managed installs; otherwise use `setup/SKILL.md`.
