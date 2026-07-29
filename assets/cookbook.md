# Cookbook — библиотека рецептов для деки

Это **рецепты, а не форма**. Бери, ремикси, расширяй или игнорируй. Движок (`kernel.html`) даёт
надёжную навигацию/анимации/заметки; здесь — готовые компоненты и один полный пример-арт-дирекшн.
Каждую деку ты **проектируешь заново** под её контент (см. `art-direction.md`), а не заполняешь шаблон.

> ⚠️ **НЕ собирай деку из одного и того же набора** (`title → enemy → cards → chain → clist → pipeline → typed`).
> Это ПРИМЕРЫ сценариев, а не обязательная последовательность. Многие слайды — просто крупная типографика
> или своя раскладка **без named-компонента**. Анимированные компоненты (pipeline, chain, glitch) — «фирменные»,
> дорогие: 1–2 на всю деку максимум. Разные доклады → разные наборы слайдов. Копировать пример «под копирку» — плохо.

**Самодостаточность (жёстко):** готовая дека — офлайн, без CDN / `@import` из сети / сетевых ссылок. Шрифты —
системные ИЛИ вшитые base64 `@font-face`. Одно исключение разрешено НА СБОРКЕ: **с согласия пользователя**
скачать **open-source** шрифт и вшить его base64 (рецепт ниже) — после этого дека снова автономна. Никаких
`pip/npm install`. Инструменты — только преустановленные (`node`, `python3` stdlib, `base64`, `curl`).

Куда что писать: весь CSS деки — в `<style id="design">`; слайды — в `#deck`. `<script id="kernel">`,
`<style id="print">` (экспорт в PDF) и chrome-DOM (`#bar/#counter/#hint`) — не трогать.

---

## Контракт классов kernel (что оживляет движок)

Аниматоры срабатывают по классам активного слайда. Часть требует, чтобы **ты определил их CSS/keyframes
в design layer** — иначе анимация «сыграет в пустоту». Таблица «класс → что делает JS → что нужно от твоего CSS»:

| Класс / атрибут | Что делает kernel | Что ОБЯЗАН дать твой CSS |
|---|---|---|
| `.count` + `data-to="N"` | накручивает текст 0→N при заходе на слайд | ничего (только стиль числа) |
| `.chain` (авто-`.seq`) | показывает `.node`/`.arrow` по очереди + считает `.count` внутри | `.chain.seq .node{opacity:0;transition:…}` и `.node.show{opacity:1}` |
| `.clist` (авто-`.cascade`) | влёт строк-детей по очереди через `animation: gitin …` | **`@keyframes gitin`** (влёт строки) + `.clist.cascade>div{opacity:0}` |
| `[data-type]` (+`data-type-speed`) | печатает текст по буквам (только ПЕРВЫЙ `[data-type]` на слайде — держи один на слайд, второй останется пустым) | ничего (опц. курсор `.tcur` с миганием) |
| `.pipeline` (опц.) | схема-процесс: класс `.on`/`.done` на `.pstage`; **играет ОДИН раз** (цикл — только `data-loop`); счётчик/точки/лента — опциональны | стили `.pstage`, `.pstage.on`, `.pstage.done`, `.pstate .ok/.mut` |
| `.reveal` / `[data-anim]` | сбрасывает и переигрывает CSS-анимацию при заходе на слайд | `.reveal{animation: … }` (что именно — решаешь ты) |
| `.tab`, `.card` | тоже переигрываются при заходе на слайд | их `animation:` (напр. `rise .4s forwards`) + `@keyframes` |
| `data-notes` у `<section>` | текст в presenter-окно; ремарки `[..]` серым; живой источник — sidecar `<slug>-notes.js` (SKILL.md Шаг 4.5), data-notes = fallback; правится и прямо в presenter (кнопками «✎ править»/«☰ все заметки», выгрузка `⤓`) | — (на деке не показывается) |

Pipeline-атрибуты на `.pipeline` (ВСЕ опциональны): `data-total` (сколько раз прогнать этапы; по
умолчанию **1**), `data-loop` (задан → зациклить; по умолчанию играет один раз и стоит), `data-item`
(слово счётчика), `data-feed` (строка в ленту), `data-fin` (финал). У каждого `.pstage`: `data-state`
(рабочий текст), `data-done` (итог), `data-dur` (мс). Опциональная шапка/лента внутри слайда:
`#pipe-counter`, `#pipe-dots`, `#pipe-feed` — их можно вообще не добавлять (минимальный pipeline = только
`.pipeline` c `.pstage`).

Счётчик-число: `<span class="count" data-to="44">0</span>`. Внутри `.chain` считается синхронно с
появлением узла; вне — сразу при заходе. ⚠️ На слайде, где ЕСТЬ `.chain`, счётчики вне цепочки не
запускаются (останутся «0») — держи их внутри узлов или выноси на другой слайд.

⚠️ **Скрытое до анимации — только через хуки kernel.** Если элемент стартует с `opacity:0` и проявляется
анимацией, вешай на него `.reveal`/`[data-anim]` (или используй `.tab`/`.card`/`.clist`/`.chain`): print-слой
раскрывает в PDF именно эти хуки. Свой класс с `opacity:0` вне контракта уедет в PDF невидимым.

---

## Типографика без загрузок (системные стеки)

Разнообразие даёт **тип шрифта**, а не скачивание. Готовые системные стеки:

- **Гуманистический sans (модерн/корпоратив):** `-apple-system,BlinkMacSystemFont,'Segoe UI','Inter',system-ui,sans-serif`
- **Гротеск/нейтральный (swiss):** `'Helvetica Neue',Helvetica,Arial,'Segoe UI',system-ui,sans-serif`
- **Serif-дисплей (editorial/эссе):** `'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif`
- **Georgia-serif (тёплый текст):** `Georgia,Cambria,'Times New Roman',serif`
- **Моноширинный (terminal/технично):** `'SF Mono',ui-monospace,'JetBrains Mono',Menlo,Consolas,monospace`
- **Rounded/дружелюбный (там где есть):** `'SF Pro Rounded','Segoe UI',system-ui,sans-serif`

Приёмы: контраст serif-заголовок × sans-текст (editorial); всё моно (terminal); тяжёлый вес + отрицательный
`letter-spacing` для гротеск-крупняка (swiss); `text-transform:uppercase`+широкий трекинг для kicker'ов.

---

## Вшить open-source шрифт (с согласия пользователя, на сборке)

Если бриф/арт-дирекшн держится на конкретном фейсе — подбери **OSS-аналог** (Druk→Anton/Archivo Black;
Founders Grotesk→Space Grotesk; Söhne→Inter; моно→JetBrains Mono/IBM Plex Mono), **спроси разрешение** и вшей
base64 (качаем ОДИН РАЗ; дека остаётся офлайн). Только OSS/free, без подписок.
⚠️ Для русской деки бери фейс **с кириллицей** и вшивай сабсеты `cyrillic` И `latin` (у Anton/Archivo Black
кириллицы нет — плакатные аналоги с кириллицей: Oswald, Unbounded, Russo One).
```bash
# Ответ css2 разбит на сабсеты (/* cyrillic */, /* latin */ …) с unicode-range; первый woff2 в нём —
# НЕ latin, поэтому не «grep|head -1», а вытаскиваем нужные сабсеты по имени блока. UA обязан быть
# полным Chrome-UA: на короткий 'Mozilla/5.0' Google отдаёт TTF без сабсетов. Пример: Oswald 600.
python3 - 'https://fonts.googleapis.com/css2?family=Oswald:wght@600&display=swap' cyrillic latin <<'PY'
import sys,re,base64,urllib.request
url,*subs=sys.argv[1:]
ua={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}
css=urllib.request.urlopen(urllib.request.Request(url,headers=ua)).read().decode()
for m in re.finditer(r'/\* ([\w-]+) \*/\s*(@font-face\s*\{[^}]+\})',css):
    if m.group(1) not in subs: continue
    u=re.search(r'url\((https://[^)]+\.woff2)\)',m.group(2)).group(1)
    b=base64.b64encode(urllib.request.urlopen(urllib.request.Request(u,headers=ua)).read()).decode()
    print(re.sub(r'url\(https://[^)]+\)\s+format\([^)]+\)',"url(data:font/woff2;base64,"+b+") format('woff2')",m.group(2)),'\n')
PY
```
Вставь полученные `@font-face`-блоки (их `unicode-range` сохранён — браузер сам возьмёт нужный сабсет)
в `<style id="design">` и используй `font-family:'Oswald',<системный фолбэк>`.
Готовая дека остаётся автономной. Нет сети/согласия / не OSS → системный маппинг (см. выше и `art-direction.md`).

## Фон (`#bg`)

`#bg` — пустой слой над которым лежат слайды; стилизуй его в design layer. Идеи (все офлайн, чистый CSS):

- **Aurora-пятна** (пример Cinematic ниже): три размытых `<span>` с `drift`-дрейфом.
- **Grid / сетка:** `#bg{background:linear-gradient(#0001 1px,transparent 1px) 0 0/40px 40px, linear-gradient(90deg,#0001 1px,transparent 1px) 0 0/40px 40px}` (swiss/tech).
- **Scanlines / CRT:** `#bg{background:repeating-linear-gradient(#0000 0 2px,#00ff9910 2px 3px)}` (terminal).
- **Мягкий радиальный градиент:** `#bg{background:radial-gradient(1200px 800px at 70% 20%,#1b2a4a55,transparent)}` (corporate).
- **Ничего:** оставь `#bg` пустым, крась `body` (editorial/minimal light).

Если фон анимирован — гаси его в `@media (prefers-reduced-motion:reduce)`.

---

## Компоненты-рецепты

Ниже — разметка. Стили компонентов пиши под свой арт-дирекшн (пример полной реализации — блок
«Cinematic Dark» в конце). Классы, которые ждёт kernel, помечены.

### Титул
```html
<section class="slide active" data-notes="Молчи 3 сек, дай прочитать. [пауза]">
  <div class="title-wrap">
    <div class="badge mono">{{надзаголовок}}</div>
    <h1>{{Заголовок}}<br><span class="accent">{{акцент}}</span></h1>
    <div class="title-sub">{{подзаголовок}}</div>
  </div>
</section>
```

### Kicker (надстрочная метка акта)
`<div class="kicker"><span class="dot">●</span> акт I</div>` — ставь вверху смыслового слайда.

### Хаос / проблема — `.tabs`
Вкладки пишем прямо в HTML (kernel переиграет их появление). Каждой — свой `animation-delay`.
```html
<div class="tabs">
  <div class="tab" style="animation-delay:.04s">вкладка 1</div>
  <div class="tab" style="animation-delay:.12s">ещё чат</div>
  <div class="tab" style="animation-delay:.20s">docs??</div>
  <div class="tab" style="animation-delay:.28s">final v2</div>
</div>
```

### Громкое слово — `.enemy` (глитч)
`<div class="enemy">СЛОВО</div>` — одно слово-враг, постоянный RGB-глитч.

### Карточки — `.cards`
```html
<div class="cards">
  <div class="card" style="animation-delay:.05s"><div class="ic">📋</div><div class="nm">{{Имя}}</div><div class="rl">{{роль}}</div></div>
  <div class="card" style="animation-delay:.18s"><div class="ic">🏗️</div><div class="nm">{{Имя}}</div><div class="rl">{{роль}}</div></div>
</div>
```

### Цитата / тезис — `.quote`
`<div class="quote"><b>{{Тезис:}}</b> {{мысль.}}</div>`

### Цепочка «идея→результат» — `.chain` (узлы по очереди + счётчики)
```html
<div class="chain">
  <div class="node"><span class="big">{{слово}}</span><span class="lbl">{{подпись}}</span></div>
  <div class="arrow">→</div>
  <div class="node"><span class="big count" data-to="26">0</span><span class="lbl">{{подпись}}</span></div>
  <div class="arrow">→</div>
  <div class="node"><span class="big accent count" data-to="44">0</span><span class="lbl">{{подпись}}</span></div>
</div>
```

### Список / «стена» — `.clist` (каскадный влёт; ТРЕБУЕТ `@keyframes gitin`)
```html
<div class="clist">
  <div><span class="h">id1</span> <span class="s">{{пункт}}</span> <span class="t">{{деталь}}</span></div>
  <div><span class="h">id2</span> <span class="s">{{пункт}}</span> <span class="t">{{деталь}}</span></div>
  <div><span class="t">… ещё N</span></div>
</div>
```

### Крупные цифры-итоги — `.stats`
```html
<div class="stats">
  <div class="stat"><div class="n count" data-to="96">0</div><div class="l">{{подпись}}</div></div>
  <div class="stat"><div class="n count" data-to="44">0</div><div class="l">{{подпись}}</div></div>
</div>
```

### Терминал (статичный кадр) — `.term`
```html
<div class="term">
  <div class="top"><i></i><i></i><i></i></div>
  <div class="body"><span class="pr">❯</span> <span class="cmd">{{команда}}</span><br>
    <span class="step">→ {{шаг}} …</span><br><span class="ok">✓ {{итог}}</span> <span class="cursor"></span></div>
</div>
```

### Процесс по шагам (живой) — `.pipeline` ⟨ОПЦИОНАЛЬНО, максимум 1 на деку⟩
> Не обязательный элемент. Часто уместнее **статичный** `.flow`/`.chain` (ниже) — они не «тикают» и не
> отвлекают. Бери `.pipeline` только если живой прогон этапов реально несёт смысл. По умолчанию проходит
> **один раз** и останавливается (цикл — только с `data-loop`).

**Минимальный вид** (только этапы, один проход — без счётчика/точек/ленты):
```html
<div class="pipeline" data-fin="Готово ✓">
  <div class="pstage" data-state="готовлю…" data-done="✓" data-dur="1100"><div class="pic">01</div><div class="pname">{{Этап 1}}</div><div class="pdesc">{{деталь}}</div><div class="pstate"></div></div>
  <div class="parrow">→</div>
  <div class="pstage" data-state="проверяю…" data-done="✓" data-dur="1200"><div class="pic">02</div><div class="pname">{{Этап 2}}</div><div class="pdesc">{{деталь}}</div><div class="pstate"></div></div>
</div>
```

**Опциональные добавки** (по желанию, не по умолчанию): шапка-счётчик `#pipe-counter` + шкала точек
`#pipe-dots`, лента `#pipe-feed`, прогон N предметов `data-total="N"`, бесконечный цикл `data-loop`:
```html
<div class="pipehead"><span class="lbl">{{метка}}</span><span class="cnt" id="pipe-counter">Item 1/6</span>
  <span class="dots" id="pipe-dots"></span></div>
<div class="pipeline" data-total="6" data-loop data-item="Item" data-feed="готово" data-fin="Готово ✓"> … </div>
<div class="feed" id="pipe-feed"></div>
```

### Финал / панчлайн — `[data-type]` (печать по буквам)
```html
<div class="typed"><span data-type="{{команда или фраза}}" data-type-speed="105"></span><span class="tcur">▋</span></div>
<div class="closer">«{{Финальная фраза-крючок.}}»</div>
```

---

## Ещё сценарии слайдов (примеры для разных жанров, НЕобязательные)

Чтобы деки не были «под копирку». Классы — просто хуки для твоего CSS; стилизуй под арт-дирекшн. Числа → `.count`;
появление по заходу → `.reveal`.

**Деловые / аналитика**
- `.metric-hero` — одна огромная цифра-KPI на весь экран: `<div class="metric-hero"><span class="count" data-to="87">0</span><span class="unit">%</span><p class="lead">подпись</p></div>`
- `.ctable` — сравнительная таблица: обычная `<table class="ctable">…</table>` (стилизуй хедер/строки под тему).
- `.beforeafter` — «до/после»: `<div class="beforeafter"><div class="ba a">…</div><div class="ba b">…</div></div>`

**Сторителлинг / питч**
- `.pullquote` — цитата-герой: `<blockquote class="pullquote">«…»<cite>— автор</cite></blockquote>`
- `.statement` — один крупный тезис на весь экран (чистая типографика): `<div class="statement"><h1>Одна мысль.</h1></div>`
- `.timeline` — вехи во времени: `<div class="timeline"><div class="mile reveal"><b>2019</b> событие</div> …</div>`

**Структура / схемы**
- `.flow` — статичная блок-схема (боксы+стрелки, НЕ анимированный pipeline): `<div class="flow"><div class="box">A</div><span class="fa">→</span><div class="box">B</div></div>`
- `.divider` — перебивка-раздел «глава N»: `<div class="divider"><span class="ch">02</span><h2>Название раздела</h2></div>`

**Сдержанное**
- `.blist` — чистый список с иконками (не «стена кода»): `<ul class="blist"><li><span class="ic">✓</span> пункт</li> …</ul>`
- `.cta` — деловой финал без терминала: `<div class="cta"><h2>Призыв</h2><p class="lead">контакт / ссылка</p></div>`

## Медиа-рецепты (картинки/гифки, самодостаточно)

### Встраивание (правило: лёгкое — inline, тяжёлое — рядом)
- **Лёгкое (< ~800 КБ: фото, логотипы, скриншоты, диаграммы)** → **inline base64**, дека остаётся одним офлайн-файлом:
  ```bash
  # печатает data-URI в stdout (macOS); mime определяет file по содержимому
  f=path/img.png; printf 'data:%s;base64,' "$(file --mime-type -b "$f")"; base64 -i "$f"
  ```
  Вставляй как `<img src="data:image/png;base64,iVBORw0K…">`.
- **Тяжёлое (> ~800 КБ: крупные GIF/видео)** → **sidecar-папка** рядом с HTML (`deck-assets/`), ссылка относительным путём `<img src="deck-assets/demo.gif">`. ⚠️ Предупреди пользователя: дека больше **не автономна** — пересылать надо вместе с папкой.

Не тяни картинки из сети (`src="http…"`) — нарушает самодостаточность.

### `.photo-full` — полноэкранное фото-подложка + текст поверх
```html
<section class="slide" data-notes="…">
  <img class="photo-bg" src="data:image/jpeg;base64,…" alt="">
  <div class="scrim"></div>
  <div class="photo-cap"><h2>{{Заголовок поверх фото}}</h2><p class="lead">{{строка}}</p></div>
</section>
```
CSS-идея: `.photo-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-1}`
`.scrim{position:absolute;inset:0;background:linear-gradient(90deg,#000c,#0000);z-index:-1}`. Опц.
Ken-Burns: `.photo-bg.reveal{animation:kenburns 12s ease both}` + `@keyframes kenburns{from{transform:scale(1)}to{transform:scale(1.12)}}` (класс `.reveal` → kernel переиграет; гаси в reduced-motion).

### `.split` — фото + текст в две колонки (`.split.reverse` зеркалит)
```html
<div class="split">
  <div class="split-media"><img src="data:…" alt=""></div>
  <div class="split-text"><h2>{{Заголовок}}</h2><p class="lead">{{текст}}</p></div>
</div>
```
CSS-идея: `.split{display:grid;grid-template-columns:1fr 1fr;gap:3vw;align-items:center}`
`.split-media img{width:100%;border-radius:16px}` · `.split.reverse{direction:rtl}.split.reverse>*{direction:ltr}`
· `@media(max-width:760px){.split{grid-template-columns:1fr}}`.

### `.gallery` — сетка изображений (каскад через `.reveal`)
```html
<div class="gallery">
  <img class="reveal" style="animation-delay:.05s" src="data:…" alt="">
  <img class="reveal" style="animation-delay:.15s" src="data:…" alt="">
</div>
```
CSS-идея: `.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem}`
`.gallery img{width:100%;border-radius:12px}` · `.gallery .reveal{animation:rise .5s both}`.

### `.figure` — одиночная картинка (диаграмма/скриншот) без кропа + подпись
```html
<div class="figure"><img src="data:…" alt=""><figcaption>{{подпись}}</figcaption></div>
```
CSS-идея: `.figure img{max-width:100%;max-height:64vh;object-fit:contain;border-radius:12px}`
`.figure figcaption{color:var(--muted);font-size:.9rem;margin-top:.8rem}`.

### `.gif-demo` / `.device` — GIF-демо в рамке-хроме (браузер/телефон)
```html
<div class="device browser"><div class="chrome"><i></i><i></i><i></i></div>
  <img src="deck-assets/demo.gif" alt=""></div>
```
CSS-идея: рамка + шапка с тремя кружками; `img{display:block;width:100%}`.

---

## Навигация колесом (крутилки)
В `kernel.html`, константы вверху скрипта: `WHEEL_TH` (порог накопления дельты на шаг, по умолч. 40 —
больше = менее чувствительно) и `WHEEL_COOLDOWN` (мс блокировки после шага, 650 — гасит инерционный хвост
тачпада, чтобы один жест = один слайд). Обычно менять не нужно. ⚠️ Это ЕДИНСТВЕННОЕ санкционированное
изменение внутри `<script id="kernel">` — только по явной просьбе пользователя; факт и новые значения
зафиксируй в `DECK.md` (раздел «Принятые решения»).

## Скорости (если просят «быстрее/медленнее»)
- Печать: `data-type-speed` (мс/символ). Глитч/дрейф/каскад — длительности в соответствующих `@keyframes`
  и `animation` твоего design layer. Pipeline: `data-dur` на этапах.

## Доступность
Оборачивай крупные декоративные анимации (aurora-дрейф, Ken-Burns, глитч) в
`@media (prefers-reduced-motion:reduce){ … animation:none }`.

---

## Извлечение материала на входе (только преустановленное)

### .docx → текст (python3 stdlib, без pandoc)
```bash
python3 - "ФАЙЛ.docx" <<'PY'
import sys,zipfile
from xml.etree import ElementTree as ET
ns='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
root=ET.fromstring(zipfile.ZipFile(sys.argv[1]).read('word/document.xml').decode('utf-8'))
for p in root.iter(ns+'p'):
    t=''.join(x.text or '' for x in p.iter(ns+'t'))
    if t.strip(): print(t)
PY
```
(`.txt/.md` — читай напрямую. `pandoc` использовать ТОЛЬКО если он уже установлен — не ставить.)

### Цифры из репозитория (для слайдов-доказательств)
```bash
cd РЕПО
git rev-list --count HEAD                    # всего коммитов
git log --oneline | grep -ciE "story|feat"   # тематические
find . -name '*.kt' | wc -l                  # счёт файлов (подставь расширение)
```
Бери реальные числа, не выдумывай. Сомнительный факт — спроси или опусти.

## Проверка перед показом
Прогони валидатор скилла (статические проверки: целостность kernel, `{{…}}`-остатки, сетевые ссылки,
`node --check` для kernel и notes.js, синхронность секций заметок со слайдами):
```bash
python3 <каталог-скилла>/assets/validate.py ФАЙЛ.html
```
Переполнение вёрстки (контент выше экрана) проверяет сам kernel: открой `file://…/ФАЙЛ.html?check` —
появится плашка со списком проблемных слайдов.
Затем `open ФАЙЛ.html` (macOS). Проверь: листается стрелками/колесом/свайпом, `P` открывает presenter
ОТДЕЛЬНЫМ окном (не вкладкой) и оно синхронно, `B` гасит экран, медиа видны, заметок на самой деке нет. Живые заметки: измени строку в
`<slug>-notes.js` при открытом presenter — текст обновится в течение пары секунд (индикатор
`● notes.js` в шапке presenter зелёный). Правка изнутри — кнопками мышью (буквенных хоткеев в окне
докладчика нет; из клавиш только стрелки, `Esc`, `⌘⏎`): «✎ править» или двойной клик по тексту →
«✓ применить» (индикатор станет `✎ черновик`), «☰ все заметки» — весь текст разом, «↺ откатить» —
вернуться к файлу, «⤓ notes.js» — выгрузить файл в загрузки и положить рядом с декой поверх старого.
Что и как работает, докладчику объясняет встроенная справка: кнопка «? справка». Просят PDF — `S` (или `⌘P`) → «Сохранить как PDF»: страница
16:9 без полей, слайд = страница; счётчики, каскады, цепочки, pipeline и печатный текст замораживаются
в финальном кадре на ВСЕХ слайдах, фон `#bg` копируется в каждую страницу. Sidecar-картинки попадают
в PDF, если дека открыта из своей папки (рядом `deck-assets/`); GIF даёт первый кадр.

## Do / Don't
- **Do:** одна мысль — один слайд; короткие заголовки; каждое число — счётчик; у каждого слайда `data-notes`;
  проектируй визуал под КОНТЕНТ (разные доклады → разные деки); всё офлайн.
- **Don't:** не вали 15 буллетов на слайд; не тяни шрифты/картинки из сети; не редактируй `<script id="kernel">`
  и chrome-DOM; не ставь пакеты; не выдумывай статистику; не более одной «громкой» анимации на слайд;
  не используй `backdrop-filter` в слайдах — конфликтует с входной transform-анимацией слайда (`slidefade`),
  рамка рендерится с глитчем; вместо него статичная радиальная/линейная заливка.

---

## ПРИМЕР готового арт-дирекшна: «Cinematic Dark»
Тёмный кинематографичный стиль (дрейф-аврора, янтарный акцент, моно-акценты). Это ОДИН из возможных
языков — копируй/адаптируй, но не считай дефолтом. Вставляется целиком в `<style id="design">`.
Фон требует три `<span>` в `#bg`: `<div id="bg"><span class="a1"></span><span class="a2"></span><span class="a3"></span></div>`.

```css
:root{
  --bg:#0a0b0f; --surface:#14161f; --surface2:#1c1f2b;
  --text:#eceef3; --muted:#878b99; --line:#2a2e3c;
  --accent:#f5b942; --green:#4ade80; --danger:#f4604f; --blue:#6aa8ff;
  --mono:'SF Mono',ui-monospace,'JetBrains Mono',Menlo,monospace;
  --sans:-apple-system,BlinkMacSystemFont,'Segoe UI','Inter',system-ui,sans-serif;
}
body{background:#000;color:var(--text);font-family:var(--sans)}
.slide{padding:7vh 9vw}
h1{font-size:clamp(2.4rem,6vw,5rem);font-weight:800;line-height:1.02;letter-spacing:-.02em}
h2{font-size:clamp(1.8rem,4.2vw,3.4rem);font-weight:750;line-height:1.08;letter-spacing:-.015em}
.lead{font-size:clamp(1.1rem,2vw,1.6rem);color:var(--muted);line-height:1.5;max-width:48ch;margin-top:1.4rem}
.accent{color:var(--accent)} .green{color:var(--green)} .danger{color:var(--danger)} .blue{color:var(--blue)} .muted{color:var(--muted)} .mono{font-family:var(--mono)}
.kicker{font-family:var(--mono);font-size:.85rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);margin-bottom:1.6rem}
.kicker .dot{color:var(--accent)}
#bar{background:linear-gradient(90deg,var(--accent),var(--green))}
#counter{color:var(--muted);opacity:1} #hint{color:#4a4e5c;opacity:1}
/* фон-аврора */
#bg{filter:blur(85px);opacity:.4}
#bg span{position:absolute;width:46vw;height:46vw;border-radius:50%;mix-blend-mode:screen;animation:drift 26s ease-in-out infinite}
#bg .a1{background:#b8862e;top:-8%;left:-6%}
#bg .a2{background:#1f6d45;bottom:-18%;right:-4%;animation-delay:-9s}
#bg .a3{background:#26407a;top:28%;right:22%;animation-delay:-17s}
@keyframes drift{0%,100%{transform:translate(0,0) scale(1)}33%{transform:translate(8%,10%) scale(1.2)}66%{transform:translate(-7%,-8%) scale(.85)}}
@keyframes rise{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:none}}
/* title */
.title-wrap{display:flex;flex-direction:column;gap:.4rem}
.title-wrap h1{margin-top:1.8rem}
.title-sub{font-size:clamp(1rem,1.7vw,1.4rem);color:var(--muted);margin-top:2rem;font-family:var(--mono)}
.badge{display:inline-flex;align-items:center;gap:.5rem;font-family:var(--mono);font-size:.8rem;color:var(--muted);border:1px solid var(--line);border-radius:99px;padding:.4rem .9rem;width:fit-content}
/* tabs */
.tabs{display:flex;gap:6px;flex-wrap:wrap;max-width:60ch;margin-top:.5rem}
.tab{font-family:var(--mono);font-size:.72rem;color:var(--muted);background:var(--surface);border:1px solid var(--line);border-top-color:#3a3030;border-radius:7px 7px 0 0;padding:.35rem .7rem;opacity:0;animation:rise .4s forwards}
/* enemy */
.enemy{font-size:clamp(3rem,11vw,9rem);font-weight:850;letter-spacing:-.03em;color:var(--danger);line-height:.95;animation:enemyglitch 2s infinite}
@keyframes enemyglitch{0%,88%,100%{text-shadow:none;transform:none}90%{text-shadow:-3px 0 #06b6d4,3px 0 #f4604f;transform:translateX(2px) skewX(-1deg)}94%{text-shadow:3px 0 #06b6d4,-3px 0 #f4604f;transform:translateX(-2px)}97%{text-shadow:-2px 0 #06b6d4,2px 0 #f4604f;transform:none}}
/* cards */
.cards{display:flex;gap:1.1rem;flex-wrap:wrap;margin-top:2.4rem}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;padding:1.3rem 1.5rem;min-width:160px;opacity:0;animation:rise .5s forwards}
.card .ic{font-size:2rem}.card .nm{font-weight:700;margin-top:.5rem;font-size:1.1rem}.card .rl{color:var(--muted);font-size:.85rem;margin-top:.15rem}
.quote{margin-top:2.4rem;border-left:3px solid var(--accent);padding:.5rem 0 .5rem 1.3rem;max-width:60ch}.quote b{color:var(--accent)}
/* chain */
.chain{display:flex;align-items:stretch;gap:0;flex-wrap:wrap;margin-top:3rem;font-family:var(--mono)}
.node{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:1rem 1.3rem;display:flex;flex-direction:column;gap:.3rem}
.node .big{font-size:1.7rem;font-weight:800;color:var(--accent)}
.node .lbl{font-size:.75rem;color:var(--muted);text-transform:uppercase;letter-spacing:.1em}
.arrow{display:flex;align-items:center;color:var(--line);font-size:1.6rem;padding:0 .7rem}
.chain.seq .node{opacity:0;transform:translateY(24px);transition:opacity .6s ease,transform .6s ease}
.chain.seq .node.show{opacity:1;transform:none}
.chain.seq .arrow{opacity:.18;transition:opacity .5s ease,color .5s ease,text-shadow .5s ease}
.chain.seq .arrow.show{opacity:1;color:var(--accent);text-shadow:0 0 16px rgba(245,185,66,.85)}
/* clist — ТРЕБУЕТ @keyframes gitin */
.clist{font-family:var(--mono);font-size:clamp(.6rem,1.15vw,.92rem);line-height:1.55;background:#070809;border:1px solid var(--line);border-radius:12px;padding:1.4rem 1.6rem;margin-top:1.4rem;max-height:62vh;overflow:hidden;column-count:2;column-gap:2.4rem}
.clist .h{color:#5a6cf5}.clist .s{color:var(--green)}.clist .t{color:var(--muted)}
.clist.cascade>div{opacity:0}
@keyframes gitin{from{opacity:0;transform:translateX(-22px)}to{opacity:1;transform:none}}
/* stats */
.stats{display:flex;gap:2.5rem;flex-wrap:wrap;margin-top:2.2rem}
.stat .n{font-size:clamp(2rem,4.5vw,3.6rem);font-weight:850;color:var(--green)}
.stat .l{color:var(--muted);font-size:.9rem;margin-top:.2rem}
/* term */
.term{font-family:var(--mono);background:#070809;border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-top:2rem;max-width:80ch}
.term .top{background:var(--surface);padding:.6rem 1rem;display:flex;gap:.5rem;border-bottom:1px solid var(--line)}
.term .top i{width:11px;height:11px;border-radius:50%;display:inline-block;background:var(--line)}
.term .top i:nth-child(1){background:#f4604f}.term .top i:nth-child(2){background:#f5b942}.term .top i:nth-child(3){background:#4ade80}
.term .body{padding:1.4rem 1.6rem;font-size:clamp(.8rem,1.4vw,1.05rem);line-height:1.85}
.term .cmd{color:var(--text)}.term .pr,.term .ok{color:var(--green)}.term .step{color:var(--muted)}
.cursor{display:inline-block;width:9px;height:1.1em;background:var(--green);vertical-align:-2px;animation:blink 1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
/* pipeline */
.pipehead{display:flex;align-items:center;gap:.8rem;font-family:var(--mono);font-size:.85rem;margin:.6rem 0 1.1rem;flex-wrap:wrap}
.pipehead .lbl{color:var(--muted);letter-spacing:.15em}.pipehead .cnt{color:var(--accent);font-weight:700}.pipehead .cnt .ok{color:var(--green)}
.dots{display:flex;gap:5px}.sdot{width:18px;height:6px;border-radius:3px;background:var(--line);display:inline-block;transition:background .3s}.sdot.full{background:var(--green)}
.pipeline{display:flex;align-items:stretch;gap:0;margin-top:.3rem;font-family:var(--mono);flex-wrap:wrap}
.pstage{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:.9rem 1rem;min-width:122px;transition:opacity .3s,border-color .3s,box-shadow .3s;opacity:.4}
.pstage.on{opacity:1;border-color:var(--accent);box-shadow:0 0 0 1px var(--accent),0 0 26px -8px var(--accent)}
.pstage.guard.on{border-color:var(--green);box-shadow:0 0 0 1px var(--green),0 0 26px -8px var(--green)}
.pstage.done{opacity:.92;border-color:#2f6b43}
.pstage .pic{font-size:1.3rem}.pstage .pname{font-weight:700;margin-top:.35rem;font-size:.92rem}.pstage .pdesc{color:var(--muted);font-size:.68rem;margin-top:.15rem;line-height:1.3}.pstage .pstate{font-size:.72rem;margin-top:.5rem;min-height:1.15em}
.pstate .mut{color:var(--muted)}.pstate .ok{color:var(--green)}
.parrow{display:flex;align-items:center;color:var(--line);padding:0 .4rem;font-size:1.2rem}
.feed{font-family:var(--mono);font-size:.8rem;margin-top:1rem;min-height:3.4em;line-height:1.75;color:var(--muted)}.feed .ok{color:var(--green)}
/* typed + closer */
.typed{font-family:var(--mono);font-size:clamp(1.3rem,3.4vw,2.6rem);font-weight:700;color:var(--bg);background:var(--accent);border-radius:14px;padding:1.1rem 1.8rem;width:fit-content;margin-top:2.2rem;animation:typedglow 2.6s ease-in-out infinite}
@keyframes typedglow{0%,100%{box-shadow:0 18px 50px -18px rgba(245,185,66,.6)}50%{box-shadow:0 18px 70px -10px rgba(245,185,66,.95)}}
.tcur{display:inline-block;color:var(--bg);font-weight:800;animation:blink 1s steps(1) infinite}
.closer{font-size:clamp(1.3rem,2.6vw,2rem);font-style:italic;margin-top:2.4rem;max-width:42ch;line-height:1.4}
@media (max-width:760px){.clist{column-count:1}.chain{gap:.4rem}}
@media (prefers-reduced-motion:reduce){#bg span,.enemy,.typed{animation:none}}
```
