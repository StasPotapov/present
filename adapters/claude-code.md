# Claude Code adapter

Use the same shared workflow in the current Claude Code session. Clone setup:
`python3 -B scripts/present.py setup --client claude-code --install-skills` from the
resolved package links both skills into `~/.claude/skills/`. Native plugin installs
already include both entry points: do not install duplicate clone links. Update
manager-owned installs through their manager.

Read/Write/Edit/Bash/Glob and the question/image/browser tools are host capabilities;
inspect the live schemas. Load other skills through the supported native mechanism.
The current session performs the stages, with its chosen model. No generated agents
or per-role model settings are needed.

For design, probe the actual Claude Design connector; follow
`adapters/claude-design.md` only if its canvas/read/comment/export capabilities exist.
Legacy Artifact signatures are examples, not a substitute for discovery. Recommend
`/design-login` only if this version's integration documents it. Otherwise use local
design files and browser preview, without asking the person to change clients.

Claude in Chrome is one possible browser adapter; other available browser tools may
provide the required screenshots, DOM audit and interactions. Follow their rules.
The shared `assets/cookbook.md` gives the DOM checks and headless print procedure;
Chrome's binary is a product dependency for that print route, not proof of extension
access. Optional connectors and auth are tested in this session, not by shelling out
to `claude mcp`. Restart/reload skill discovery after installation as needed.

This adapter preserves the original Claude workflow. Fixture tests of installation
do not establish live Claude or Claude Design availability.
