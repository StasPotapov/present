#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сборщик деки «Контекст. Дизайн. Голос.» (скилл /present, KERNEL v8).

    python3 build.py            # пересобрать деку в deck/ (notes.js НЕ трогается, если он уже есть)
    python3 build.py --notes    # пересобрать И перезаписать notes.js из data-notes

Что делает:
  1. берёт движок kernel.html ДОСЛОВНО (из ассетов скилла /present; фолбэк — src/kernel-v8.html);
  2. вставляет src/design.css в <style id="design">, подставив в него @font-face Inter
     (src/inter-faces.css — base64, cyrillic+latin, roman+italic; сеть не нужна);
  3. вставляет src/slides.html в #deck, заменив маркеры __IMG:файл__ на inline data-URI;
  4. дописывает <script id="interactive"> (src/interactive.js — виджет слайда 09) ПОСЛЕ
     блока kernel, перед ПОСЛЕДНИМ </body>: первое вхождение лежит внутри самого движка,
     в строке, которая собирает presenter-окно, и вставка туда его ломает;
  5. пишет готовую деку и (опционально) файл живых заметок в папку показа deck/.

ВАЖНО про заметки: после первого прогона источник правды — <дека>-notes.js
(его правят прямо в окне докладчика и выгружают кнопкой ⤓). Поэтому по умолчанию
скрипт его НЕ перезаписывает. Если правил заметки в presenter — сначала перенеси
их текст в data-notes внутри src/slides.html, и только потом запускай с --notes.
"""

import base64
import mimetypes
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "src"
DECK_DIR = HERE / "deck"   # папка показа: html + notes.js, уносится целиком (медиа вшито base64)
SKILL_KERNEL = Path.home() / ".claude/skills/present/assets/kernel.html"

DECK_NAME = "kontekst-dizayn-golos-2026-07-28"
TITLE = "Контекст. Дизайн. Голос. — как я делаю доклады с /present"

FORCE_NOTES = "--notes" in sys.argv


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


# ── 1. движок ────────────────────────────────────────────────────────────────
def kernel_version(p: Path) -> int:
    m = re.search(r"KERNEL v(\d+)", read(p)) if p.exists() else None
    return int(m.group(1)) if m else 0

# берём движок посвежее: старая установка скилла не должна молча откатить деку на прошлую версию
kernel_path = max([SKILL_KERNEL, SRC / "kernel-v8.html"], key=kernel_version)
# v8 обязателен: плейсхолдер {{TITLE}} и UI по lang; интерактиву слайда 09 нужны guard'ы v6+
if kernel_version(kernel_path) < 8:
    sys.exit(f"!! {kernel_path} — не похоже на KERNEL v8+, сборку остановил")
kernel = read(kernel_path)
print(f"движок: {kernel_path}")

# ── 2. design layer ──────────────────────────────────────────────────────────
design = read(SRC / "design.css")
if "/*__INTER_FACES__*/" not in design:
    sys.exit("!! в design.css нет маркера /*__INTER_FACES__*/ — дека уехала бы без вшитых шрифтов")
design = design.replace("/*__INTER_FACES__*/", read(SRC / "inter-faces.css"))

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
if "<title>{{TITLE}}</title>" not in kernel or '<html lang="en">' not in kernel:
    sys.exit("!! в движке нет плейсхолдера <title>{{TITLE}}</title> или корня <html lang=\"en\">")
out = kernel.replace("<title>{{TITLE}}</title>", f"<title>{TITLE}</title>")
out = out.replace('<html lang="en">', '<html lang="ru">', 1)   # язык деки: от него зависят и надписи kernel

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

# ── 4б. интерактив: свой блок скрипта ПОСЛЕ kernel ───────────────────────────
interactive = read(SRC / "interactive.js")
head, sep, tail = out.rpartition("</body>")   # именно последнее </body>, см. шапку файла
if not sep:
    sys.exit("!! не нашёл закрывающий </body>")
out = head + '<script id="interactive">\n' + interactive + '</script>\n' + sep + tail
print(f"интерактив: interactive.js ({len(interactive.encode()) // 1024} КБ)")

DECK_DIR.mkdir(exist_ok=True)
deck_file = DECK_DIR / f"{DECK_NAME}.html"
deck_file.write_text(out, encoding="utf-8")
print(f"дека: {deck_file.name} ({len(out.encode()) // 1024} КБ)")

# ── 5. живые заметки ─────────────────────────────────────────────────────────
notes_file = DECK_DIR / f"{DECK_NAME}-notes.js"
if notes_file.exists() and not FORCE_NOTES:
    print(f"заметки: {notes_file.name} на месте — не трогаю (перезапись: --notes)")
else:
    # Номера заметок раздаются ПО ПОРЯДКУ СЛАЙДОВ, поэтому потерять хоть одну секцию нельзя:
    # пропуск сдвинет речь всех последующих слайдов, и спикер прочитает чужой текст. Отсюда
    # разбор настоящим парсером (порядок атрибутов и лишние data-* его не волнуют) и sys.exit,
    # а не print, на любое расхождение — как у двух других плейсхолдеров выше.
    raw_titles = re.findall(r"<!--\s*(\d{2})\s+─\s+(.+?)\s+─+\s*-->", slides)
    titles = dict(raw_titles)
    if len(titles) != len(raw_titles):
        sys.exit("!! в комментариях-заголовках повторяется номер слайда — перенумеруй секции")

    class SlideNotes(HTMLParser):
        """Собирает data-notes всех <section class="slide …"> по порядку их появления."""

        def __init__(self):
            super().__init__(convert_charrefs=True)   # &lt; в заметке доедет до presenter как <
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
        sys.exit(f"!! слайды без data-notes: {empty} — заметки собрались бы со сдвигом")
    if len(notes) != len(titles):
        sys.exit(f"!! слайдов {len(notes)}, комментариев-заголовков {len(titles)} — заметки уехали бы не к тем слайдам")
    body = ""
    for i, text in enumerate(notes, 1):
        ttl = titles.get(f"{i:02d}", "")
        text = text.replace("`", "ʼ").replace("${", "$ {").strip()
        body += f"## {i:02d} · {ttl}\n{text}\n\n"
    notes_file.write_text(
        "window.DECK_NOTES = String.raw`\n" + body.strip() + "\n`;\n", encoding="utf-8"
    )
    print(f"заметки: {notes_file.name} ({len(notes)} секций)")
