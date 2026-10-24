#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build script for the deck "Контекст. Дизайн. Голос." (skill /present, KERNEL v8). The deck is in Russian.

    python3 build.py            # rebuild the deck into deck/ (notes.js is NOT touched if it exists)
    python3 build.py --notes    # rebuild AND overwrite notes.js from data-notes

What it does:
  1. takes the kernel kernel.html VERBATIM (from the /present skill assets; fallback: src/kernel-v8.html)
     and sets the root lang to "ru";
  2. puts src/design.css into <style id="design"> with the Inter @font-face inserted
     (src/inter-faces.css: base64, cyrillic+latin, roman+italic; no network needed);
  3. puts src/slides.html into #deck and replaces the __IMG:file__ markers with inline data URIs;
  4. appends <script id="interactive"> (src/interactive.js, the widget of slide 09) AFTER
     the kernel block, before the LAST </body>: the first one is inside the kernel itself,
     in the string that builds the presenter window, and an insert there breaks it;
  5. writes the finished deck and (optionally) the live notes file into the show folder deck/.

IMPORTANT about notes: after the first run-through the source of truth is <deck>-notes.js
(it is edited in the presenter window and exported with the ⤓ button). So by default
the script does NOT overwrite it. If you edited notes in the presenter window, first move
their text into data-notes in src/slides.html, and only then run with --notes.
"""

import base64
import mimetypes
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
DECK_DIR = HERE / "deck"   # show folder: html + notes.js, taken away as a whole (media embedded as base64)
SKILL_KERNEL = Path.home() / ".claude/skills/present/assets/kernel.html"

DECK_NAME = "kontekst-dizayn-golos-2026-07-28"
TITLE = "Контекст. Дизайн. Голос. — как я делаю доклады с /present"

FORCE_NOTES = "--notes" in sys.argv


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ── 1. kernel ────────────────────────────────────────────────────────────────
def kernel_version(p: Path) -> int:
    m = re.search(r"KERNEL v(\d+)", read(p)) if p.exists() else None
    return int(m.group(1)) if m else 0

# take the newest kernel: an old skill install must not silently roll the deck back
kernel_path = max([SKILL_KERNEL, SRC / "kernel-v8.html"], key=kernel_version)
# v8 is required: the {{TITLE}} placeholder and the UI by lang; the slide 09 widget needs the v6+ guards
if kernel_version(kernel_path) < 8:
    sys.exit(f"!! {kernel_path}: does not look like KERNEL v8+, build stopped")
kernel = read(kernel_path)
print(f"kernel: {kernel_path}")

# ── 2. design layer ──────────────────────────────────────────────────────────
design = read(SRC / "design.css")
if "/*__INTER_FACES__*/" not in design:
    sys.exit("!! design.css has no /*__INTER_FACES__*/ marker: the deck would ship without embedded fonts")
design = design.replace("/*__INTER_FACES__*/", read(SRC / "inter-faces.css"))

# ── 3. slides + images ─────────────────────────────────────────────────────
slides = read(SRC / "slides.html")


def inline_img(m: re.Match) -> str:
    f = HERE / m.group(1)
    mime = mimetypes.guess_type(f.name)[0] or "image/jpeg"
    data = base64.b64encode(f.read_bytes()).decode()
    print(f"  embedded {f.name}: {len(data) // 1024} KB base64")
    return f"data:{mime};base64,{data}"


slides = re.sub(r"__IMG:([^_]+?)__", inline_img, slides)

# ── 4. build ────────────────────────────────────────────────────────────────
if "<title>{{TITLE}}</title>" not in kernel or '<html lang="en">' not in kernel:
    sys.exit("!! the kernel has no <title>{{TITLE}}</title> placeholder or no <html lang=\"en\"> root")
out = kernel.replace("<title>{{TITLE}}</title>", f"<title>{TITLE}</title>")
out = out.replace('<html lang="en">', '<html lang="ru">', 1)   # deck language: the kernel UI follows it

out, n = re.subn(
    r'(<style id="design">)\s*/\*.*?\*/\s*(</style>)',
    lambda m: m.group(1) + "\n" + design + "\n" + m.group(2),
    out,
    count=1,
    flags=re.S,
)
if n != 1:
    sys.exit("!! placeholder <style id=\"design\"> not found")

out, n = re.subn(
    r'(<div id="deck">)\s*<!--.*?-->\s*(</div>)',
    lambda m: m.group(1) + "\n" + slides + "\n" + m.group(2),
    out,
    count=1,
    flags=re.S,
)
if n != 1:
    sys.exit("!! placeholder #deck not found")

# ── 4b. interactivity: own script block AFTER the kernel ───────────────────────────
interactive = read(SRC / "interactive.js")
head, sep, tail = out.rpartition("</body>")   # the last </body>, see the file header
if not sep:
    sys.exit("!! closing </body> not found")
out = head + '<script id="interactive">\n' + interactive + '</script>\n' + sep + tail
print(f"interactive: interactive.js ({len(interactive.encode()) // 1024} KB)")

DECK_DIR.mkdir(exist_ok=True)
deck_file = DECK_DIR / f"{DECK_NAME}.html"
deck_file.write_text(out, encoding="utf-8")
print(f"deck: {deck_file.name} ({len(out.encode()) // 1024} KB)")

# ── 5. live notes ─────────────────────────────────────────────────────────
notes_file = DECK_DIR / f"{DECK_NAME}-notes.js"
if notes_file.exists() and not FORCE_NOTES:
    print(f"notes: {notes_file.name} exists, not touched (overwrite: --notes)")
else:
    # Note numbers follow the SLIDE ORDER, so not one section may be lost: a gap shifts
    # the speech of all following slides, and the speaker reads the wrong text. Hence a real
    # parser (attribute order and extra data-* do not matter to it) and sys.exit, not print,
    # on any mismatch, as for the two placeholders above.
    raw_titles = re.findall(r"<!--\s*(\d{2})\s+─\s+(.+?)\s+─+\s*-->", slides)
    titles = dict(raw_titles)
    if len(titles) != len(raw_titles):
        sys.exit("!! a slide number repeats in the title comments: renumber the sections")

    class SlideNotes(HTMLParser):
        """Collects data-notes of all <section class="slide …"> in the order they appear."""

        def __init__(self):
            super().__init__(convert_charrefs=True)   # &lt; in a note reaches the presenter window as <
            self.notes = []

        def handle_starttag(self, tag, attrs):
            if tag != "section":
                return
            a = dict(attrs)
            if "slide" in (a.get("class") or "").split():
                self.notes.append(a.get("data-notes"))

    parser = SlideNotes()
    parser.feed(slides)
    notes = parser.notes
    empty = [i for i, n in enumerate(notes, 1) if not n]
    if empty:
        sys.exit(f"!! slides without data-notes: {empty}: the notes would be shifted")
    if len(notes) != len(titles):
        sys.exit(f"!! {len(notes)} slides, {len(titles)} title comments: the notes would go to the wrong slides")
    body = ""
    for i, text in enumerate(notes, 1):
        ttl = titles.get(f"{i:02d}", "")
        text = text.replace("`", "ʼ").replace("${", "$ {").strip()
        body += f"## {i:02d} · {ttl}\n{text}\n\n"
    notes_file.write_text(
        "window.DECK_NOTES = String.raw`\n" + body.strip() + "\n`;\n", encoding="utf-8"
    )
    print(f"notes: {notes_file.name} ({len(notes)} sections)")
