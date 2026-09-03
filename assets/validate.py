#!/usr/bin/env python3
"""validate.py — статическая проверка готовой деки скилла /present.

Использование: python3 validate.py путь/к/деке.html

Проверяет: целостность kernel (маркер версии, base/print-стили, chrome-DOM, presenter, экспорт в PDF),
остаточные {{…}}-плейсхолдеры, сетевые ссылки (дека должна быть офлайн)
и локальные ссылки на отсутствующие файлы, синтаксис
JS через node --check (kernel, <script id="interactive"> и <slug>-notes.js), синхронность
секций notes.js со слайдами, интерактив (нужен kernel v6+, клик на не-интерактивных тегах),
наличие сопутствующих файлов (slides.md, design.md, DECK.md — рядом с декой или уровнем выше)
и чистоту папки показа deck/ (в ней только html, notes.js, deck-assets/).

Одиночная дека быстрого режима (лежит не в deck/, рядом нет ни одного файла комплекта)
распознаётся сама: комплект с неё не спрашивается.

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
from urllib.parse import unquote

def node_error(stderr: str) -> str:
    """Строка с сутью ошибки из вывода node --check (последняя строка — версия Node, она бесполезна)."""
    m = re.search(r"^\w*(?:Error|Exception):.*$", stderr, re.M)
    return m.group(0).strip() if m else (stderr.strip().splitlines()[0] if stderr.strip() else "ошибка")

def main():
    if len(sys.argv) != 2:
        print(__doc__.strip())
        return 2
    deck = Path(sys.argv[1]).resolve()
    if not deck.is_file():
        print(f"✗ файл не найден: {deck}")
        return 1
    html = deck.read_text(encoding="utf-8")
    errors, warns = [], []

    # Быстрый режим: дека собрана одним файлом, комплекта под неё нет и быть не должно.
    # Признак — по окружению, без служебных меток внутри деки: файл лежит не в папке показа
    # и рядом (и уровнем выше) нет ни одного файла комплекта.
    notes = deck.with_name(re.sub(r"\.html?$", "", deck.name) + "-notes.js")
    kit_dirs = [deck.parent, deck.parent.parent]
    kit_files = ["slides.md", "design.md", "DECK.md"]
    standalone = (
        deck.parent.name != "deck"
        and not notes.exists()
        and not any((d / n).exists() for d in kit_dirs for n in kit_files)
    )

    # ── 1. Целостность kernel ────────────────────────────────────────────────
    m_ver = re.search(r"KERNEL v(\d+)", html)
    kernel_ver = int(m_ver.group(1)) if m_ver else None
    if kernel_ver is None:
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

    # ── 3b. Ловушки design-слоя (перекрытие плумбинга) ──────────────────────
    m = re.search(r'<style id="design">(.*?)</style>', html, re.S)
    if m:
        design = m.group(1)
        # внутри @media/@supports (print, prefers-reduced-motion) display у .slide законен — вырезаем их
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
        # .slide{display:…} перебивает базовое display:none → все слайды показываются разом
        for rule in re.findall(r"([^{}]*\.slide\b[^{},]*)\{([^{}]*)\}", design):
            sel, body = rule[0].strip(), rule[1]
            if ".active" in sel or ":" in sel.replace(".slide", "").replace(".active", ""):
                continue
            if re.search(r"(?<![\w-])display\s*:", body):
                errors.append(
                    f"design-слой: правило «{sel}{{…display…}}» перекрывает базовое .slide{{display:none}} — "
                    "все слайды покажутся разом; задавай display только через .slide.active"
                )
            if re.search(r"(?<![\w-])position\s*:", body):
                warns.append(
                    f"design-слой: «{sel}{{…position…}}» перекрывает базовое .slide{{position:absolute}} — "
                    "слайды могут разъехаться потоком"
                )

    # ── 3c. Интерактив на слайдах ───────────────────────────────────────────
    # Виджеты в слайдах спорят с навигацией, если движок их не пропускает: guard'ы появились в v6.
    deck_start = html.find('<div id="deck">')
    deck_end = html.find('<div id="counter"')
    if deck_end < deck_start:                      # chrome переименован/переставлен — режем до конца файла
        deck_end = len(html)
    deck_html = html[deck_start:deck_end] if deck_start >= 0 else ""
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
                "в слайдах есть интерактив (" + ", ".join(found) + "), а движок ниже v6 — в нём нет guard'ов: "
                "клик по label пролистает слайд, буквы в поле ввода нажмут хоткеи. Перенеси деку на свежий kernel.html"
            )
        # клик, повешенный атрибутом на не-интерактивный тег: kernel примет его за клик по слайду
        bad_click = [
            t.group(0)[:60] for t in re.finditer(
                r"<(?:div|span|section|p|li|td|h[1-6])\b[^>]*\son(?:click|mousedown|pointerdown)\s*=[^>]*>", deck_html
            ) if "data-interactive" not in t.group(0)
        ]
        if bad_click:
            warns.append(
                "клик на не-интерактивном теге без [data-interactive] — kernel пролистает слайд поверх обработчика: "
                + "; ".join(bad_click[:3])
            )

    # ── 3d. Локальные ссылки на отсутствующие файлы ─────────────────────────
    # Зеркало к разделу 3: там ловятся ссылки НАРУЖУ, тут — ссылки внутрь, ведущие в никуда
    # (переименовали картинку в deck-assets/, забыли положить файл рядом с декой).
    # Скрипты и код-примеры вырезаются: `img.src='frames/'+i+'.png'` и <code>&lt;img src="x.png"&gt;</code>
    # ссылками не являются, а падение валидатора на живой деке дороже пропущенной картинки.
    scan = re.sub(r"(<(script|pre|code)\b[^>]*>).*?(</\2>)", r"\1\3", html, flags=re.S | re.I)
    missing_refs = []
    for m_ref in re.finditer(
        r"""(?:^|[\s"'])(?:src|srcset|href)\s*=\s*["']([^"']+)["']|url\(\s*["']?([^"')]+?)["']?\s*\)""",
        scan, re.I | re.M,
    ):
        raw = (m_ref.group(1) or m_ref.group(2) or "").strip()
        # srcset — список "файл дескриптор, файл дескриптор"; у обычной ссылки список из одного элемента
        for part in raw.split(","):
            ref = part.strip().split()[0] if part.strip() else ""
            if not ref:
                continue
            rel = unquote(ref).split("?")[0].split("#")[0]
            # схему проверяем после unquote: внутри data-URI со встроенным SVG попадается url(%23id) —
            # это ссылка на фрагмент, а не на файл, и до декодирования она на "#" не похожа
            if not rel or rel.startswith(("/", "#")) or re.match(r"[a-z][a-z0-9+.\-]*:", rel, re.I):
                continue                          # любая схема и абсолютный путь — не наше дело
            if not re.search(r"\.[A-Za-z0-9]{1,6}$", rel):
                continue                          # без расширения это не путь к файлу
            if not (deck.parent / rel).exists():
                missing_refs.append(ref[:60])
    if missing_refs:
        errors.append("ссылки на отсутствующие файлы: " + ", ".join(sorted(set(missing_refs))[:6]))

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
    elif not standalone:
        warns.append(f"нет файла живых заметок {notes.name} — presenter будет читать только вшитые data-notes")

    # ── 5. Скрипты деки и синтаксис JS (node --check) ───────────────────────
    # Скриптов в деке максимум два: kernel (плумбинг) и interactive (авторские виджеты).
    # Каждый проверяется отдельно и по своему id — иначе при появлении второго блока
    # kernel молча выпадал бы из проверки.
    blocks, pos, stray = [], {}, []
    for m in re.finditer(r"<script([^>]*)>(.*?)</script>", html, re.S):
        sid = re.search(r"""id\s*=\s*["\']([^"\']+)""", m.group(1))
        sid = sid.group(1) if sid else ""
        blocks.append((sid, m.group(2)))
        pos.setdefault(sid, m.start())
        if sid not in ("kernel", "interactive"):
            stray.append(sid or "без id")
    if "interactive" in pos and "kernel" in pos and pos["interactive"] < pos["kernel"]:
        warns.append('блок скрипта id="interactive" стоит ДО kernel — он должен идти после, иначе виджеты не найдут функции движка')
    if stray:
        warns.append("посторонние script-блоки (в деке ожидаются только kernel и interactive): " + ", ".join(stray[:5]))

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
                errors.append(f'node --check (блок скрипта id="{sid or "без id"}"): {node_error(r.stderr)}')
        if notes.exists():
            r = subprocess.run([node, "--check", str(notes)], capture_output=True, text=True)
            if r.returncode:
                errors.append(
                    f"node --check ({notes.name}): {node_error(r.stderr)} — presenter покажет последнюю удачную версию"
                )
    else:
        warns.append("node не найден — синтаксис JS не проверен")

    # ── 6. Сопутствующие файлы (рабочая папка — рядом или уровнем выше) ─────
    # Раскладка скилла: дека лежит в <рабочая папка>/deck/, а slides.md/design.md/DECK.md — в самой
    # рабочей папке. Старые деки лежат прямо в рабочей папке, поэтому ищем в обоих местах.
    if not standalone:
        for name, why in [("slides.md", "текст слайдов"), ("design.md", "дизайн-бриф"), ("DECK.md", "манифест деки")]:
            if not any((d / name).exists() for d in kit_dirs):
                warns.append(f"ни в папке деки, ни в рабочей папке нет {name} ({why})")

    # ── 7. Чистота папки показа ─────────────────────────────────────────────
    # В deck/ должно лежать только нужное для показа: html, его notes.js, sidecar deck-assets/.
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
    mode = "одиночная дека" if standalone else "дека с комплектом"
    print(f"✓ OK — {slide_count} слайдов, {mode}, ошибок нет, предупреждений {len(warns)}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
