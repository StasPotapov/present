#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборщик деки «Слова. Вид. Голос.» (скилл /present, KERNEL v5).

    python3 build.py            # пересобрать деку в deck/ (notes.js НЕ трогается, если он уже есть)
    python3 build.py --notes    # пересобрать И перезаписать notes.js из data-notes

Что делает:
  1. берёт движок kernel.html ДОСЛОВНО (из ассетов скилла /present; фолбэк — src/kernel-v5.html);
  2. вставляет src/design.css в <style id="design">, подставив в него @font-face Inter
     (src/inter-faces.css — base64, cyrillic+latin, roman+italic; сеть не нужна);
  3. вставляет src/slides.html в #deck, заменив маркеры __IMG:файл__ на inline data-URI;
  4. пишет готовую деку и (опционально) файл живых заметок в папку показа deck/.

ВАЖНО про заметки: после первого прогона источник правды — <дека>-notes.js
(его правят прямо в окне докладчика и выгружают кнопкой ⤓). Поэтому по умолчанию
скрипт его НЕ перезаписывает. Если правил заметки в presenter — сначала перенеси
их текст в data-notes внутри src/slides.html, и только потом запускай с --notes.
"""

import base64
import mimetypes
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
DECK_DIR = HERE / "deck"   # папка показа: html + notes.js (+ deck-assets), уносится целиком
SKILL_KERNEL = Path.home() / ".claude/skills/present/assets/kernel.html"

DECK_NAME = "slova-vid-golos-2026-07-28"
TITLE = "Слова. Вид. Голос. — как я делаю доклады с /present"

FORCE_NOTES = "--notes" in sys.argv


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ── 1. движок ────────────────────────────────────────────────────────────────
kernel_path = SKILL_KERNEL if SKILL_KERNEL.exists() else SRC / "kernel-v5.html"
kernel = read(kernel_path)
if "KERNEL v5" not in kernel:
    sys.exit(f"!! {kernel_path} — не похоже на KERNEL v5, сборку остановил")
print(f"движок: {kernel_path}")

# ── 2. design layer ──────────────────────────────────────────────────────────
design = read(SRC / "design.css").replace("/*__INTER_FACES__*/", read(SRC / "inter-faces.css"))

# ── 3. слайды + картинки ─────────────────────────────────────────────────────
slides = read(SRC / "slides.html")


def inline_img(m: re.Match) -> str:
    f = HERE / m.group(1)
    mime = mimetypes.guess_type(f.name)[0] or "image/jpeg"
    data = base64.b64encode(f.read_bytes()).decode()
    print(f"  вшил {f.name}: {len(data) // 1024} КБ base64")
    return f"data:{mime};base64,{data}"


slides = re.sub(r"__IMG:([^_]+?)__", inline_img, slides)

# ── 4. сборка ────────────────────────────────────────────────────────────────
out = kernel.replace("<title>{{ЗАГОЛОВОК}}</title>", f"<title>{TITLE}</title>")

out, n = re.subn(
    r'(<style id="design">)\s*/\*.*?\*/\s*(</style>)',
    lambda m: m.group(1) + "\n" + design + "\n" + m.group(2),
    out,
    count=1,
    flags=re.S,
)
if n != 1:
    sys.exit("!! не нашёл плейсхолдер <style id=\"design\">")

out, n = re.subn(
    r'(<div id="deck">)\s*<!--.*?-->\s*(</div>)',
    lambda m: m.group(1) + "\n" + slides + "\n" + m.group(2),
    out,
    count=1,
    flags=re.S,
)
if n != 1:
    sys.exit("!! не нашёл плейсхолдер #deck")

DECK_DIR.mkdir(exist_ok=True)
deck_file = DECK_DIR / f"{DECK_NAME}.html"
deck_file.write_text(out, encoding="utf-8")
print(f"дека: {deck_file.name} ({len(out.encode()) // 1024} КБ)")

# ── 5. живые заметки ─────────────────────────────────────────────────────────
notes_file = DECK_DIR / f"{DECK_NAME}-notes.js"
if notes_file.exists() and not FORCE_NOTES:
    print(f"заметки: {notes_file.name} на месте — не трогаю (перезапись: --notes)")
else:
    titles = dict(re.findall(r"<!--\s*(\d{2})\s+─\s+(.+?)\s+─+\s*-->", slides))
    notes = re.findall(r'<section class="slide[^"]*" data-notes="(.*?)">', slides, flags=re.S)
    if len(notes) != len(titles):
        print(f"!! слайдов с заметками {len(notes)}, комментариев-заголовков {len(titles)}")
    body = ""
    for i, text in enumerate(notes, 1):
        ttl = titles.get(f"{i:02d}", "")
        text = text.replace("`", "ʼ").replace("${", "$ {").strip()
        body += f"## {i:02d} · {ttl}\n{text}\n\n"
    notes_file.write_text(
        "window.DECK_NOTES = String.raw`\n" + body.strip() + "\n`;\n", encoding="utf-8"
    )
    print(f"заметки: {notes_file.name} ({len(notes)} секций)")
