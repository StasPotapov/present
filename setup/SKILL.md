---
name: present-setup
description: "Set up the portable present pipeline: install Codex or Claude Code adapters, guide other compatible agents, and verify local resources and preview capabilities."
---

# Set up present

Resolve this directory's real path; the shared root is its parent. Read `../HOST.md`
and the adapter for the actual session. Use `python3 -B ../scripts/present.py doctor`
with the resolved absolute script path. Python 3.9+ is sufficient. Do not infer the
active client from installed executables or run an AI CLI to discover capabilities.
For another agent, keep the complete repository and read its `SKILL.md` and `HOST.md`
in that session. Use its documented skill-loading procedure, if any; do not pass an
unknown client to the bundled installer or invent a native installation path.

1. Identify ownership before installing. For a standalone clone, preview
   `setup --client codex` or `setup --client claude-code`, then repeat with
   `--install-skills` to link both whole skill trees. Existing links to this exact
   root are kept; foreign files, old links and manager-owned destinations stop all
   writes. Preserve them and update through their owner; never force replacement.
   A partial link failure removes links created by this invocation.
2. For a plugin, use its bundled main/setup skills without standalone links. For an
   environment manager, let it package and deliver both entries and all resources.
   AI Workspace is optional delivery infrastructure, never a runtime dependency.
3. There are no independent model roles in present. Use the current session's model;
   do not create role settings, ask about models or change another client's settings.
4. Probe available tools in this session: shell/files, image viewer, browser, design
   and preview. Read `../stages/canvas.md`. Codex uses local HTML preview by default;
   optional Pages, Presentations and Sites have distinct contracts. Claude Code uses
   Claude Design only when its connector is actually available. Missing tools,
   auth failures, network failures and untested access are different states.
5. Check doctor, repeat setup, resolve both links and validate a local deck. Node is
   needed for the validator's JS syntax checks; browser/PDF tools are separate.
   Do not install software or log in as a side effect. Without shell, explain that
   local setup/build is unavailable here; without image access, visual QA is unverified.
6. Verify discovery in a fresh session and perform a safe local preview. Report static,
   fixture and live evidence separately. A written adapter does not prove a live
   Claude session, an authenticated connector, or hosted publication.
