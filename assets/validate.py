#!/usr/bin/env python3
"""validate.py — static check of a finished deck built by the /present skill.

Usage: python3 validate.py path/to/deck.html

Checks: kernel integrity (version marker, base/print styles, chrome DOM, presenter window, PDF export),
leftover {{…}} placeholders, network links (the deck must work offline)
and local links to missing files, JS syntax
with node --check (kernel, <script id="interactive"> and <slug>-notes.js), notes.js sections
in sync with the slides, interactivity (needs kernel v6+, clicks on non-interactive tags),
the companion files (slides.md, design.md, DECK.md — next to the deck or one level up),
the Pipeline section of DECK.md (`## Pipeline` / `## Конвейер` or the line <!-- present:pipeline -->)
and a clean show folder deck/ (only the html, notes.js, deck-assets/).

A single short-path deck (not in deck/, no kit file next to it) is detected
automatically: the kit is not required for it. A deck without the presenter window
(data-presenter="off" on <html>, kernel v7+) does not need data-notes and notes.js.

Exit 0 — no errors (warnings are allowed), exit 1 — errors found.
The kernel itself does the dynamic slide overflow check: open the deck with ?check.

Python 3 stdlib only; node is optional.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote

# The Pipeline section of DECK.md: a heading (## to ######) in English or Russian, any case and trailing text, or a marker line.
PIPELINE_RE = re.compile(r"^[ \t>*-]*(?:#{2,6}[ \t]+(?:pipeline|конвейер)|<!--[ \t]*present:pipeline[ \t]*-->)", re.I | re.M)

def node_error(stderr: str) -> str:
    """The line with the error from node --check output (the last line is the Node version, it is not useful)."""
    m = re.search(r"^\w*(?:Error|Exception):.*$", stderr, re.M)
    return m.group(0).strip() if m else (stderr.strip().splitlines()[0] if stderr.strip() else "error")

def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    deck = Path(sys.argv[1]).resolve()
    if not deck.is_file():
        print(f"✗ file not found: {deck}")
        return 1
    html = deck.read_text(encoding="utf-8")
    errors, warns = [], []

    # Short path: the deck is one file, it has no kit and must not have one.
    # Detected from the surroundings, not from markers in the deck: the file is not in the show folder
    # and no kit file is next to it (or one level up).
    notes = deck.with_name(re.sub(r"\.html?$", "", deck.name) + "-notes.js")
    kit_dirs = [deck.parent, deck.parent.parent]
    kit_files = ["slides.md", "design.md", "DECK.md"]
    standalone = (
        deck.parent.name != "deck"
        and not notes.exists()
        and not any((d / n).exists() for d in kit_dirs for n in kit_files)
    )
    m_root = re.search(r"<html\b[^>]*>", html, re.I)   # root tag only: a second <html> lives in a string of the presenter window
    presenter_off = bool(m_root and re.search(r"\bdata-presenter\s*=\s*[\"']off[\"']", m_root.group(0)))   # the kernel compares strictly: 'off'
    # A full-path kit is detected by the show folder or the manifest: slides.md/DESIGN.md also exist in other projects
    full_kit = deck.parent.name == "deck" or any((d / "DECK.md").exists() for d in kit_dirs)

    # ── 1. Kernel integrity ──────────────────────────────────────────────────
    m_ver = re.search(r"KERNEL v(\d+)", html)
    kernel_ver = int(m_ver.group(1)) if m_ver else None
    if kernel_ver is None:
        warns.append("no KERNEL version marker — the kernel is old or replaced; take a fresh assets/kernel.html")
    for anchor, what in [
        ('<style id="base">', "base structural CSS"),
        ('<style id="design">', "design layer"),
        ('<style id="print">', "print layer (PDF export with the S key)"),
        ('<div id="deck">', "slide container"),
        ('<script id="kernel">', "kernel script"),
        ('id="bar"', "progress bar"),
        ('id="counter"', "counter"),
        ('id="hint"', "hint"),
    ]:
        if anchor not in html:
            errors.append(f"{anchor} not found ({what}) — the build damaged the kernel")
    if "openPresenter" not in html:
        errors.append("no openPresenter — the kernel script is damaged or outdated")
    if "freezeForPrint" not in html:
        errors.append("no freezeForPrint — the kernel script is old (no PDF export) or damaged")
    # The version marker stayed v6 while printing was fixed: without this check a deck built on an old v6
    # looks the same, but it prints with grey rectangles over the content and is ten times larger
    # (Skia writes blurred shadows as a raster mask, Quartz draws it opaque).
    elif "flattenShadows" not in html:
        warns.append("kernel without flattenShadows — a kernel from before the print fix: the PDF gets grey "
                     "overlays and tens of MB; rebuild the deck on a fresh assets/kernel.html")
    if presenter_off and (kernel_ver is None or kernel_ver < 7):
        errors.append('only kernel v7+ knows data-presenter="off" — this kernel does not turn off the presenter window')
    if presenter_off and full_kit:
        errors.append('the presenter window is off (data-presenter="off"), but the deck is in a full-path kit '
                      "(deck/ or DECK.md) — you cannot rehearse a talk without speaker notes; remove the attribute")
    for fn, what in [("commitEdit", "speaker notes editing in the presenter window"), ("exportNotes", "notes.js export from the presenter window")]:
        if fn not in html:
            errors.append(f"no {fn} — the kernel script is older than v5 (no {what}) or damaged")
    # legacy of a sed trap: the base style must not end up inside the opening comment
    first_comment_end = html.find("-->")
    base_pos = html.find('<style id="base">')
    if base_pos != -1 and first_comment_end != -1 and base_pos < first_comment_end:
        errors.append('<style id="base"> is inside the opening comment — the build damaged the markup')

    # ── 2. Leftover placeholders ─────────────────────────────────────────────
    placeholders = sorted(set(re.findall(r"\{\{[^{}]{1,60}\}\}", html)))
    if placeholders:
        errors.append("leftover placeholders: " + ", ".join(placeholders[:8]))

    # ── 3. Network links (offline contract) ─────────────────────────────────
    net = []
    for pat, label in [
        (r'(?:src|href)\s*=\s*["\']https?://', "src/href from the network"),
        (r'@import\s+(?:url\()?["\']?https?://', "@import from the network"),
        (r'url\(\s*["\']?https?://', "url() from the network"),
    ]:
        if re.search(pat, html):
            net.append(label)
    if net:
        errors.append("network links (the deck must work offline): " + "; ".join(net))

    # ── 3b. Design layer traps (overriding the plumbing) ────────────────────
    m = re.search(r'<style id="design">(.*?)</style>', html, re.S)
    if m:
        design = m.group(1)
        # inside @media/@supports (print, prefers-reduced-motion) display on .slide is legal — cut them out
        def strip_at_blocks(css):
            out, i = [], 0
            while i < len(css):
                at = css.find("@", i)
                if at == -1:
                    out.append(css[i:]); break
                brace = css.find("{", at)
                if brace == -1 or "\n" in css[at:brace] and ";" in css[at:brace]:
                    out.append(css[i:at + 1]); i = at + 1; continue
                out.append(css[i:at])
                depth, j = 1, brace + 1
                while j < len(css) and depth:
                    depth += (css[j] == "{") - (css[j] == "}")
                    j += 1
                i = j
            return "".join(out)
        design = strip_at_blocks(design)
        # .slide{display:…} overrides the base display:none → all slides show at once
        for rule in re.findall(r"([^{}]*\.slide\b[^{},]*)\{([^{}]*)\}", design):
            sel, body = rule[0].strip(), rule[1]
            if ".active" in sel or ":" in sel.replace(".slide", "").replace(".active", ""):
                continue
            if re.search(r"(?<![\w-])display\s*:", body):
                errors.append(
                    f"design layer: the rule \"{sel}{{…display…}}\" overrides the base .slide{{display:none}} — "
                    "all slides show at once; set display only through .slide.active"
                )
            if re.search(r"(?<![\w-])position\s*:", body):
                warns.append(
                    f"design layer: \"{sel}{{…position…}}\" overrides the base .slide{{position:absolute}} — "
                    "slides can fall into normal flow"
                )

    # ── 3c. Interactivity on slides ─────────────────────────────────────────
    # Widgets on slides conflict with navigation if the kernel does not skip them: the guards appeared in v6.
    deck_start = html.find('<div id="deck">')
    deck_end = html.find('<div id="counter"')
    if deck_end < deck_start:                      # chrome renamed or moved — cut to the end of the file
        deck_end = len(html)
    deck_html = html[deck_start:deck_end] if deck_start >= 0 else ""
    # The kernel UI follows the root lang: a Cyrillic deck left on the kernel's lang="en" gets an English UI.
    if deck_html and m_root:
        m_lang = re.search(r"\blang\s*=\s*[\"']([^\"']*)[\"']", m_root.group(0))
        lang = (m_lang.group(1) if m_lang else "").lower()
        text = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", " ", deck_html, flags=re.S | re.I))
        cyr = len(re.findall(r"[а-яё]", text, re.I))
        lat = len(re.findall(r"[a-z]", text, re.I))
        if not lang:
            warns.append("the root html tag has no lang — set it to the deck language (the kernel UI follows it)")
        elif cyr > lat and not re.match(r"ru(-|$)", lang):
            warns.append(f'the slides are mostly Cyrillic, but the root tag has lang="{lang}" — set the deck language '
                         '(for Russian lang="ru"), otherwise the kernel UI stays English')
    if deck_html:
        found = [
            what for pat, what in [
                (r"<input\b", "<input>"), (r"<textarea\b", "<textarea>"), (r"<select\b", "<select>"),
                (r"<label\b", "<label>"), (r"<details\b", "<details>"), (r"contenteditable", "contenteditable"),
                (r"data-interactive", "[data-interactive]"), (r"data-scroll", "[data-scroll]"),
            ] if re.search(pat, deck_html)
        ]
        if found and (kernel_ver is None or kernel_ver < 6):
            warns.append(
                "the slides have interactive elements (" + ", ".join(found) + "), but the kernel is older than v6 — it has no guards: "
                "a click on a label turns the slide, letters in an input field trigger hotkeys. Move the deck to a fresh kernel.html"
            )
        # a click handler attribute on a non-interactive tag: the kernel takes it as a click on the slide
        bad_click = [
            t.group(0)[:60] for t in re.finditer(
                r"<(?:div|span|section|p|li|td|h[1-6])\b[^>]*\son(?:click|mousedown|pointerdown)\s*=[^>]*>", deck_html
            ) if "data-interactive" not in t.group(0)
        ]
        if bad_click:
            warns.append(
                "click on a non-interactive tag without [data-interactive] — the kernel turns the slide over the handler: "
                + "; ".join(bad_click[:3])
            )

    # ── 3d. Local links to missing files ────────────────────────────────────
    # Mirror of section 3: that one catches links OUT, this one catches local links to nowhere
    # (an image in deck-assets/ was renamed, a file was not put next to the deck).
    # Scripts and code samples are cut out: `img.src='frames/'+i+'.png'` and <code>&lt;img src="x.png"&gt;</code>
    # are not links, and a false failure on a working deck costs more than a missed image.
    scan = re.sub(r"(<(script|pre|code)\b[^>]*>).*?(</\2>)", r"\1\3", html, flags=re.S | re.I)
    missing_refs = []
    for m_ref in re.finditer(
        r"""(?:^|[\s"'])(?:src|srcset|href)\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+?)["']?\s*\)""",
        scan, re.I | re.M,
    ):
        raw = (m_ref.group(1) or m_ref.group(2) or "").strip()
        # srcset is a list "file descriptor, file descriptor"; a plain link is a list of one item
        for part in raw.split(","):
            ref = part.strip().split()[0] if part.strip() else ""
            if not ref:
                continue
            rel = unquote(ref).split("?")[0].split("#")[0]
            # check the scheme after unquote: a data URI with inline SVG can contain url(%23id) —
            # a fragment link, not a file, and before decoding it does not start with "#"
            if not rel or rel.startswith(("/", "#")) or re.match(r"[a-z][a-z0-9+.\-]*:", rel, re.I):
                continue                          # any scheme or absolute path — not ours to check
            if not re.search(r"\.[A-Za-z0-9]{1,6}$", rel):
                continue                          # without an extension it is not a file path
            if not (deck.parent / rel).exists():
                missing_refs.append(ref[:60])
    if missing_refs:
        errors.append("links to missing files: " + ", ".join(sorted(set(missing_refs))[:6]))

    # ── 4. Slides and speaker notes ─────────────────────────────────────────
    slide_count = len(re.findall(r'<section[^>]*class="[^"]*\bslide\b', html))
    if slide_count == 0:
        errors.append("no .slide section found")
    else:
        without_notes = slide_count - len(re.findall(r"<section[^>]*data-notes", html))
        if without_notes > 0 and not presenter_off:
            warns.append(f"{without_notes} slide(s) without data-notes (fallback speaker notes)")
        if not re.search(r'<section[^>]*class="[^"]*\bactive\b', html):
            warns.append("no slide with the class active — mark the first one")

    if notes.exists() and presenter_off:
        warns.append(f'{notes.name} is next to the deck, but the presenter window is off — the file is not read; '
                     "if you do not need it, delete it; if you need it, remove data-presenter=\"off\"")
    elif notes.exists():
        ntxt = notes.read_text(encoding="utf-8")
        if "DECK_NOTES" not in ntxt:
            errors.append(f"{notes.name}: no window.DECK_NOTES — the kernel does not see it")
        secs = [int(m) for m in re.findall(r"^##\s*(\d+)", ntxt, re.M)]
        out_of_range = [n for n in secs if n < 1 or n > slide_count]
        if out_of_range:
            errors.append(f"{notes.name}: sections out of the slide range {out_of_range} (slides: {slide_count})")
        dup = sorted(n for n in set(secs) if secs.count(n) > 1)
        if dup:
            warns.append(f"{notes.name}: duplicate sections {dup}")
        missing = [n for n in range(1, slide_count + 1) if n not in secs]
        if missing:
            warns.append(f"{notes.name}: no sections for slides {missing}")
    elif not standalone and not presenter_off:
        warns.append(f"no live notes file {notes.name} — the presenter window reads only the embedded data-notes")

    # ── 5. Deck scripts and JS syntax (node --check) ────────────────────────
    # A deck has at most two scripts: kernel (plumbing) and interactive (author widgets).
    # Each one is checked separately by its id — otherwise, with a second block present,
    # the kernel would silently drop out of the check.
    blocks, pos, stray = [], {}, []
    for m in re.finditer(r"<script([^>]*)>(.*?)</script>", html, re.S):
        sid = re.search(r"""id\s*=\s*["\']([^"\']+)""", m.group(1))
        sid = sid.group(1) if sid else ""
        blocks.append((sid, m.group(2)))
        pos.setdefault(sid, m.start())
        if sid not in ("kernel", "interactive"):
            stray.append(sid or "no id")
    if "interactive" in pos and "kernel" in pos and pos["interactive"] < pos["kernel"]:
        warns.append('the script block id="interactive" is BEFORE the kernel — it must come after, or the widgets do not find the kernel functions')
    if stray:
        warns.append("unexpected script blocks (a deck has only kernel and interactive): " + ", ".join(stray[:5]))

    node = shutil.which("node")
    if node:
        for sid, body in blocks:
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
                f.write(body)
                js_path = f.name
            try:
                r = subprocess.run([node, "--check", js_path], capture_output=True, text=True)
            finally:
                Path(js_path).unlink(missing_ok=True)
            if r.returncode:
                errors.append(f'node --check (script block id="{sid or "no id"}"): {node_error(r.stderr)}')
        if notes.exists():
            r = subprocess.run([node, "--check", str(notes)], capture_output=True, text=True)
            if r.returncode:
                errors.append(
                    f"node --check ({notes.name}): {node_error(r.stderr)} — the presenter window shows the last valid version"
                )
    else:
        warns.append("node not found — JS syntax not checked")

    # ── 6. Companion files (working folder — next to the deck or one level up) ─
    # Skill layout: the deck is in <working folder>/deck/, and slides.md/design.md/DECK.md are in the
    # working folder itself. Old decks are directly in the working folder, so look in both places.
    if not standalone and not (presenter_off and not full_kit):
        for name, why in [("slides.md", "slide text"), ("design.md", "design brief"), ("DECK.md", "deck manifest")]:
            if not any((d / name).exists() for d in kit_dirs):
                warns.append(f"no {name} ({why}) in the deck folder or in the working folder")
        manifest = next((d / "DECK.md" for d in kit_dirs if (d / "DECK.md").exists()), None)
        if manifest and not PIPELINE_RE.search(manifest.read_text(encoding="utf-8")):
            warns.append("DECK.md has no Pipeline section (## Pipeline / ## Конвейер or <!-- present:pipeline -->) — "
                         "a new session does not know where the work stopped (template: assets/deck-template.md)")

    # ── 7. Clean show folder ────────────────────────────────────────────────
    # deck/ holds only what the show needs: the html, its notes.js, the sidecar deck-assets/.
    if deck.parent.name == "deck":
        extra = [
            p.name for p in sorted(deck.parent.iterdir())
            if not p.name.startswith(".")
            and p.name != deck.name
            and p.name != notes.name
            and not (p.is_dir() and p.name == "deck-assets")
        ]
        if extra:
            warns.append(
                "the show folder has extra files (it must hold what the show needs and nothing more): "
                + ", ".join(extra[:8])
            )

    # ── Report ───────────────────────────────────────────────────────────────
    for w in warns:
        print("⚠ " + w)
    for e in errors:
        print("✗ " + e)
    if errors:
        print(f"\nFAIL: errors {len(errors)}, warnings {len(warns)}")
        return 1
    mode = "single deck" if standalone or (presenter_off and not full_kit) else "deck with kit"
    if presenter_off:
        mode += ", no presenter window"
    print(f"✓ OK — {slide_count} slides, {mode}, no errors, warnings {len(warns)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
