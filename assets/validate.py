#!/usr/bin/env python3
"""validate.py — статическая проверка готовой деки скилла /present.

Использование: python3 validate.py путь/к/деке.html

Проверяет: целостность kernel (маркер версии, base/print-стили, chrome-DOM, presenter, экспорт в PDF),
остаточные {{…}}-плейсхолдеры, сетевые ссылки (дека должна быть офлайн), синтаксис
JS через node --check (kernel и <slug>-notes.js), синхронность секций notes.js со
слайдами, наличие сопутствующих файлов (slides.md, design.md, DECK.md — рядом с декой
или уровнем выше) и чистоту папки показа deck/ (в ней только html, notes.js, deck-assets/).

Exit 0 — ошибок нет (предупреждения допустимы), exit 1 — есть ошибки.
Динамическую проверку переполнения слайдов делает сам kernel: открой деку с ?check.

Только python3 stdlib; node — опционален.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    deck = Path(sys.argv[1])
    if not deck.is_file():
        print(f"✗ файл не найден: {deck}")
        return 1
    html = deck.read_text(encoding="utf-8")
    errors, warns = [], []

    # ── 1. Целостность kernel ────────────────────────────────────────────────
    if "KERNEL v" not in html:
        warns.append("нет маркера версии KERNEL — движок старый или подменён; возьми свежий assets/kernel.html")
    for anchor, what in [
        ('<style id="base">', "базовый структурный CSS"),
        ('<style id="design">', "design-слой"),
        ('<style id="print">', "print-слой (экспорт в PDF по клавише S)"),
        ('<div id="deck">', "контейнер слайдов"),
        ('<script id="kernel">', "kernel-скрипт"),
        ('id="bar"', "прогресс-бар"),
        ('id="counter"', "счётчик"),
        ('id="hint"', "подсказка"),
    ]:
        if anchor not in html:
            errors.append(f"не найден {anchor} ({what}) — kernel повреждён при сборке")
    if "openPresenter" not in html:
        errors.append("нет openPresenter — kernel-скрипт повреждён или устарел")
    if "freezeForPrint" not in html:
        errors.append("нет freezeForPrint — kernel-скрипт старый (нет экспорта в PDF) или повреждён")
    for fn, what in [("commitEdit", "правки заметок прямо в presenter"), ("exportNotes", "выгрузки notes.js из presenter")]:
        if fn not in html:
            errors.append(f"нет {fn} — kernel-скрипт старее v5 (нет {what}) или повреждён")
    # наследие sed-ловушки: base-стиль не должен оказаться внутри вводного комментария
    first_comment_end = html.find("-->")
    base_pos = html.find('<style id="base">')
    if base_pos != -1 and first_comment_end != -1 and base_pos < first_comment_end:
        errors.append('<style id="base"> оказался внутри вводного комментария — сборка повредила разметку')

    # ── 2. Остаточные плейсхолдеры ───────────────────────────────────────────
    placeholders = sorted(set(re.findall(r"\{\{[^{}]{1,60}\}\}", html)))
    if placeholders:
        errors.append("остаточные плейсхолдеры: " + ", ".join(placeholders[:8]))

    # ── 3. Сетевые ссылки (офлайн-контракт) ─────────────────────────────────
    net = []
    for pat, label in [
        (r'(?:src|href)\s*=\s*["\']https?://', "src/href из сети"),
        (r'@import\s+(?:url\()?["\']?https?://', "@import из сети"),
        (r'url\(\s*["\']?https?://', "url() из сети"),
    ]:
        if re.search(pat, html):
            net.append(label)
    if net:
        errors.append("сетевые ссылки (дека должна быть офлайн): " + "; ".join(net))

    # ── 4. Слайды и заметки ─────────────────────────────────────────────────
    slide_count = len(re.findall(r'<section[^>]*class="[^"]*\bslide\b', html))
    if slide_count == 0:
        errors.append("не найдено ни одной секции .slide")
    else:
        without_notes = slide_count - len(re.findall(r"<section[^>]*data-notes", html))
        if without_notes > 0:
            warns.append(f"{without_notes} слайд(ов) без data-notes (fallback-заметок)")
        if not re.search(r'<section[^>]*class="[^"]*\bactive\b', html):
            warns.append("нет слайда с классом active — пометь первый")

    notes = deck.with_name(re.sub(r"\.html?$", "", deck.name) + "-notes.js")
    if notes.exists():
        ntxt = notes.read_text(encoding="utf-8")
        if "DECK_NOTES" not in ntxt:
            errors.append(f"{notes.name}: нет window.DECK_NOTES — kernel его не увидит")
        secs = [int(m) for m in re.findall(r"^##\s*(\d+)", ntxt, re.M)]
        out_of_range = [n for n in secs if n < 1 or n > slide_count]
        if out_of_range:
            errors.append(f"{notes.name}: секции вне диапазона слайдов {out_of_range} (слайдов: {slide_count})")
        dup = sorted(n for n in set(secs) if secs.count(n) > 1)
        if dup:
            warns.append(f"{notes.name}: дублирующиеся секции {dup}")
        missing = [n for n in range(1, slide_count + 1) if n not in secs]
        if missing:
            warns.append(f"{notes.name}: нет секций для слайдов {missing}")
    else:
        warns.append(f"нет файла живых заметок {notes.name} — presenter будет читать только вшитые data-notes")

    # ── 5. Синтаксис JS (node --check) ──────────────────────────────────────
    node = shutil.which("node")
    if node:
        s = html.rfind("<script")
        if s != -1:
            s = html.index(">", s) + 1
            e = html.rfind("</script>")
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
                f.write(html[s:e])
                js_path = f.name
            r = subprocess.run([node, "--check", js_path], capture_output=True, text=True)
            if r.returncode:
                detail = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "ошибка"
                errors.append(f"node --check (kernel-скрипт): {detail}")
        if notes.exists():
            r = subprocess.run([node, "--check", str(notes)], capture_output=True, text=True)
            if r.returncode:
                errors.append(f"node --check ({notes.name}): синтаксическая ошибка — presenter покажет последнюю удачную версию")
    else:
        warns.append("node не найден — синтаксис JS не проверен")

    # ── 6. Сопутствующие файлы (рабочая папка — рядом или уровнем выше) ─────
    # Раскладка скилла: дека лежит в <рабочая папка>/deck/, а slides.md/design.md/DECK.md — в самой
    # рабочей папке. Старые деки лежат прямо в рабочей папке, поэтому ищем в обоих местах.
    look_in = [deck.parent, deck.parent.parent]
    for name, why in [("slides.md", "текст слайдов"), ("design.md", "дизайн-бриф"), ("DECK.md", "манифест деки")]:
        if not any((d / name).exists() for d in look_in):
            warns.append(f"ни в папке деки, ни в рабочей папке нет {name} ({why})")

    # ── 7. Чистота папки показа ─────────────────────────────────────────────
    # В deck/ должно лежать только нужное для показа: html, его notes.js, sidecar deck-assets/.
    if deck.parent.name.endswith("deck"):
        extra = [
            p.name for p in sorted(deck.parent.iterdir())
            if not p.name.startswith(".")
            and p.name != deck.name
            and p.name != notes.name
            and not (p.is_dir() and p.name == "deck-assets")
        ]
        if extra:
            warns.append(
                "в папке показа лежит лишнее (её должно хватать для показа и ничего больше): "
                + ", ".join(extra[:8])
            )

    # ── Отчёт ────────────────────────────────────────────────────────────────
    for w in warns:
        print("⚠ " + w)
    for e in errors:
        print("✗ " + e)
    if errors:
        print(f"\nFAIL: ошибок {len(errors)}, предупреждений {len(warns)}")
        return 1
    print(f"✓ OK — {slide_count} слайдов, ошибок нет, предупреждений {len(warns)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
