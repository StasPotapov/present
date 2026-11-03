#!/usr/bin/env python3
"""Local setup and diagnostics. No AI client, service or package-manager dependency."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION = "1.1.0"
CLIENTS = {"codex": ".agents", "claude-code": ".claude"}
RESOURCES = (
    "SKILL.md", "HOST.md", "setup/SKILL.md", "scripts/present.py",
    "stages/context.md", "stages/design.md", "stages/build.md", "stages/quick.md",
    "stages/rehearse.md", "stages/transcribe.md", "stages/canvas.md", "stages/codex-design.md",
    "adapters/codex.md", "adapters/claude-code.md", "adapters/claude-design.md",
    "assets/kernel.html", "assets/validate.py", "assets/cookbook.md",
    "assets/design-axes.md", "assets/art-direction.md", "assets/deck-template.md",
    "example/slides.md", "example/design.md",
)


def doctor():
    missing = [name for name in RESOURCES if not (ROOT / name).is_file()]
    chrome = next((str(p) for p in (
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path(shutil.which("chromium") or shutil.which("google-chrome") or "/nonexistent")
    ) if p.is_file()), None)
    return {"version": VERSION, "root": str(ROOT), "missing_resources": missing,
            "python": sys.version.split()[0], "node": shutil.which("node"),
            "chrome": chrome, "pdfinfo": shutil.which("pdfinfo"),
            "host_capabilities": "unknown: inspect the actual session's tools",
            "ai_client_cli_required": False}


def setup(client, install):
    if doctor()["missing_resources"]:
        raise ValueError("incomplete package; restore the full resource tree")
    native = Path.home() / CLIENTS[client] / "skills"
    pairs = [(native / "present", ROOT), (native / "present-setup", ROOT / "setup")]
    pending = []
    # All conflicts are checked before writing either entry point.
    for target, source in pairs:
        if os.path.lexists(target):
            if not target.is_symlink() or target.resolve() != source:
                raise ValueError(f"foreign or manager-owned installation: {target}; update through its owner")
        else:
            pending.append((target, source))
    made = []
    if install:
        try:
            for target, source in pending:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(source, target_is_directory=True)
                made.append(target)
        except OSError:
            for target in reversed(made):
                target.unlink()
            raise
    return {"client": client, "installed": [str(p) for p in made],
            "planned": [str(p) for p, _ in pending], "apply": install,
            "adapter": str(ROOT / "adapters" / (client + ".md")),
            "settings": "none: present uses the current session; no model roles"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="local dependencies and resource integrity; no network")
    p = sub.add_parser("setup", help="preview or install complete standalone skill links")
    p.add_argument("--client", choices=CLIENTS, required=True)
    p.add_argument("--install-skills", action="store_true")
    p = sub.add_parser("validate", help="run the independent HTML deck validator")
    p.add_argument("deck", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "validate":
            return subprocess.call([sys.executable, "-B", str(ROOT / "assets/validate.py"), str(args.deck)])
        result = doctor() if args.command == "doctor" else setup(args.client, args.install_skills)
        print(json.dumps(result, indent=2))
        return 1 if result.get("missing_resources") else 0
    except (OSError, ValueError) as error:
        print(f"present: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
