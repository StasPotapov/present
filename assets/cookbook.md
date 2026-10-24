# Cookbook — technical reference for the deck

This file has **no ready-made looks and nothing to copy**. Before, this file held a component gallery
and one full art direction example, and decks came out as recolored copies of them. The visuals of
each deck are invented again for its content. What you must decide for that is in `design-axes.md`.
How to read a brief and a reference is in `art-direction.md`.

This file keeps only what you cannot invent on the spot:
- **kernel class contract** — which names the kernel expects and which states your CSS must describe;
- **interactivity contract** — how an author widget lives together with navigation, the presenter window and print;
- **technique** — offline fonts, base64 media, input extraction, checks, PDF, accessibility.

**Self-containment (strict):** the finished deck is offline. No CDN, no `@import` from the network, no
network links. Fonts are system fonts OR embedded base64 `@font-face`. One exception is allowed AT BUILD
TIME: **with the person's consent**, download an **open-source** font and embed it as base64 (recipe
below). After that the deck is self-contained again. No `pip/npm install`. Use only preinstalled tools
(`node`, `python3` stdlib, `base64`, `curl`).

Where to write what: all deck CSS goes into `<style id="design">`; slides go into `#deck`. Do not touch
`<script id="kernel">`, `<style id="print">` (PDF export) and the chrome DOM (`#bar/#counter/#hint`).

---

## Kernel class contract (what the kernel animates)

The animators fire on classes of the active slide. Some of them require that **you define their
CSS/keyframes in the design layer**. If you do not, the animation "plays into nothing". The table
"class → what the JS does → what your CSS must give":

| Class / attribute | What the kernel does | What your CSS MUST give |
|---|---|---|
| `.count` + `data-to="N"` | counts the text up 0→N when the slide opens | nothing (only the number style) |
| `.chain` (auto `.seq`) | shows `.node`/`.arrow` one by one + counts `.count` inside | `.chain.seq .node{opacity:0;transition:…}` and `.node.show{opacity:1}` |
| `.clist` (auto `.cascade`) | child rows fly in one by one through `animation: gitin …` | **`@keyframes gitin`** (row fly-in) + `.clist.cascade>div{opacity:0}` |
| `[data-type]` (+`data-type-speed`) | types the text letter by letter (only the FIRST `[data-type]` on a slide — keep one per slide, a second one stays empty) | nothing (optional cursor `.tcur` with blinking) |
| `.pipeline` (optional) | process diagram: class `.on`/`.done` on `.pstage`; **plays ONCE** (loop only with `data-loop`); counter/dots/feed are optional | styles `.pstage`, `.pstage.on`, `.pstage.done`, `.pstate .ok/.mut` |
| `.reveal` / `[data-anim]` | resets and replays the CSS animation when the slide opens | `.reveal{animation: … }` (you decide what exactly) |
| `.tab`, `.card` | also replay when the slide opens | their `animation:` (for example `rise .4s forwards`) + `@keyframes` |
| `data-notes` on `<section>` | text for the presenter window; remarks `[..]` in grey; the live source is the live notes file `<slug>-notes.js` (`stages/build.md`, Step 4 — Bespoke build, item 5), data-notes = fallback; you can also edit it directly in the presenter window (the edit button ✎, the all-notes button ☰, export `⤓`) | — (not shown on the deck) |

**Without the presenter window (kernel v7+).** The attribute `data-presenter="off"` on the root `<html>`
turns the presenter window off completely: `P` opens nothing, `<slug>-notes.js` does not load, and the
`P` hint disappears from `#hint`. Such a deck does not need `data-notes`. This is the default of the
short path (`stages/quick.md`). The kernel ships with `<html lang="en">`. The build writes
`<html lang="<deck language>">`, and on the short path it adds ` data-presenter="off"`:
`<html lang="<deck language>" data-presenter="off">`. Replace the root tag as one string: since kernel
v7 this string occurs once (the presenter window string builds its own tag in parts). To bring the
window back, remove the attribute, add `data-notes` to all slides and run the validator again. On a
kernel below v7 the attribute has no effect, and the validator reports it as an error.

**Kernel UI language (kernel v8).** Kernel UI strings (presenter window, hints, toasts) follow
`<html lang>`: `ru` or `ru-*` → Russian, any other value → English. The build sets `lang` on the root tag to
the deck language. Edits of the kernel copy outside the design layer and `#deck`: on the root tag —
only `lang` and `data-presenter="off"`; inside `<script id="kernel">` — only `WHEEL_TH`/`WHEEL_COOLDOWN`
(see "Wheel navigation"). Nothing else. The current kernel marker is `KERNEL v8`.

Pipeline attributes on `.pipeline` (ALL optional): `data-total` (how many times to run the stages; default
**1**), `data-loop` (set → loop; by default it plays once and stops), `data-item` (the counter word; default from the kernel UI language: Item / Пункт),
`data-feed` (a line for the feed), `data-fin` (the finale; default Done ✓ / Готово ✓). Each `.pstage` has: `data-state` (working
text), `data-done` (result), `data-dur` (ms). An optional header/feed inside the slide:
`#pipe-counter`, `#pipe-dots`, `#pipe-feed`. You can leave them out completely (the minimal pipeline =
only `.pipeline` with `.pstage`).

Number counter: `<span class="count" data-to="44">0</span>`. Inside `.chain` it counts together with
the appearance of its node; outside, it counts at once when the slide opens. ⚠️ On a slide that HAS a
`.chain`, counters outside the chain do not start (they stay at "0"). Keep them inside the nodes or move
them to another slide.

**Minimal markup of the contract classes** (the structure is required, the look is yours):
```html
<span class="count" data-to="44">0</span>                          <!-- number counter -->
<div class="chain"><div class="node">…</div><span class="arrow">→</span><div class="node">…</div></div>
<div class="clist"><div>row</div><div>row</div></div>          <!-- children = cascade steps -->
<div class="pipeline"><div class="pstage" data-state="…" data-done="…" data-dur="900">…</div></div>
<h2 data-type="Text that will be typed letter by letter"></h2>          <!-- one per slide -->
```
Everything else on the slide is free markup for your composition. The kernel does not require `.kicker`,
`.lead`, `.title-wrap` or any "standard" slide structure.

⚠️ **Hidden until animation — only through kernel hooks.** If an element starts with `opacity:0` and
appears through an animation, put `.reveal`/`[data-anim]` on it (or use `.tab`/`.card`/`.clist`/`.chain`).
The print layer reveals exactly these hooks in the PDF. Your own class with `opacity:0` outside the
contract goes into the PDF invisible.

---

## Typography without downloads (what the system really has)

This is a reference of what is available offline. You decide which face fits which talk (this is
axis 3 in `design-axes.md`). Here are only the availability guarantees. On macOS/Windows these
families are reliably available:

| Category | Stack that will not fail |
|---|---|
| System sans | `-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif` |
| Neutral grotesque | `'Helvetica Neue',Helvetica,Arial,sans-serif` |
| Condensed/poster | `Impact,Haettenschweiler,'Arial Narrow',sans-serif` |
| Serif display | `'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif` |
| Serif text | `Georgia,Cambria,'Times New Roman',serif` |
| Monospace | `'SF Mono',ui-monospace,'JetBrains Mono',Menlo,Consolas,monospace` |
| Rounded (if present) | `'SF Pro Rounded','Segoe UI',system-ui,sans-serif` |

⚠️ For a Russian (Cyrillic) deck, check Cyrillic: some poster faces do not have it. Character comes
less from the choice of family and more from weight, size, `line-height`, `letter-spacing`, case and
column width. Work with those.

## Embed an open-source font (with the person's consent, at build time)

If the brief or art direction depends on a specific face, find an **OSS equivalent** (Druk→Anton/Archivo Black;
Founders Grotesk→Space Grotesk; Söhne→Inter; mono→JetBrains Mono/IBM Plex Mono), **ask for permission** and embed
it as base64 (download it ONCE; the deck stays offline). Only OSS/free, no subscriptions.
⚠️ For a Russian (Cyrillic) deck, take a face **with Cyrillic** and embed the `cyrillic` AND `latin` subsets
(Anton/Archivo Black have no Cyrillic; poster equivalents with Cyrillic: Oswald, Unbounded, Russo One).
```bash
# The css2 response is split into subsets (/* cyrillic */, /* latin */ …) with unicode-range; the first woff2 in it
# is NOT latin, so do not use "grep|head -1": extract the needed subsets by block name. The UA must be
# a full Chrome UA: for a short 'Mozilla/5.0' Google returns TTF without subsets. Example: Oswald 600.
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
Paste the resulting `@font-face` blocks (their `unicode-range` is kept, so the browser takes the needed
subset itself) into `<style id="design">` and use `font-family:'Oswald',<system fallback>`.
The finished deck stays self-contained. No network / no consent / not OSS → system mapping (see above and `art-direction.md`).

## Background (`#bg`)

`#bg` is an empty layer under the slides; you style it in the design layer. **Techniques and the rule of
choice are in `design-axes.md`, axis 5**. Here are only the technique and the prohibitions:

- Drifting blurred blobs ("aurora") are a technique from old decks. By default, do NOT use them.
- An empty `#bg` + a color on `body` is a valid and often the best choice, especially for light decks.
- Animate the background only if the motion carries meaning (flow, process, time). Otherwise keep it static.
- Turn off any background animation in `@media (prefers-reduced-motion:reduce)`.
- The background prints into the PDF as a copy inside each slide (`freezeForPrint`). Because of this,
  heavy blur layers give a muddy spot in print. Check the export if the background is complex.
- **Keep a raster background texture (noise, grid through `background-image:url(data:image/svg+xml…)`)
  on a pseudo-layer `#bg::before/::after`, not on `#bg` itself.** There are as many background copies
  in print as there are slides, and Chrome rasterizes such a pattern into each one: on a live deck,
  16 slides gave a 27 MB PDF instead of 2 MB. `freezeForPrint()` turns off in print exactly the
  pseudo-layers that have a texture (classes `.rb`/`.ra` on the copy), but only if the texture is
  **alone** on the pseudo-element: the layer is turned off completely, so the kernel does not touch
  `background-image:radial-gradient(…), url(…)` at all (otherwise it would remove the gradient together
  with the texture). Keep the texture on its own pseudo-layer and the gradient on its own.

---

## Media: how to embed self-contained

The question "how it looks" is decided by art direction. Here is only the technique that keeps the deck offline.

**Weight rule.** Light files (< ~800 KB) → inline base64 directly in `src`; the deck stays one file:
```bash
python3 -c "import base64,sys,pathlib;p=pathlib.Path(sys.argv[1]);print('data:image/'+p.suffix[1:].replace('jpg','jpeg')+';base64,'+base64.b64encode(p.read_bytes()).decode())" photo.jpg
```
Heavy files (large GIF/video) → into `deck/deck-assets/`, with a relative link (`deck-assets/…`). Warn
the person that the deck now travels only together with its folder. Copy the originals; do not move them.

**What matters technically, whatever the look:**
- do not force the proportions: `object-fit:cover` crops, `contain` fits the whole image. For diagrams and
  screenshots you almost always need `contain`, otherwise the edges of the diagram disappear;
- for a full-frame image, set both `width` and `height` (or `inset:0`), otherwise the slide "slides"
  and overflows. This is one of the frequent causes of `?check` findings;
- insert SVG inline (`<svg>` directly in the markup): it scales without loss and takes color through
  `currentColor`, so it follows the palette;
- a GIF gives its first frame in the PDF. If the demo is important for the print version, add a static duplicate frame;
- always write alt text (`alt`): it is read in the presenter window and goes into the PDF text layer.

## Wheel navigation (tuning)
In `kernel.html`, the constants at the top of the script: `WHEEL_TH` (the delta accumulation threshold per step, default 40;
higher = less sensitive) and `WHEEL_COOLDOWN` (ms of lock after a step, 650; it absorbs the inertial tail
of the touchpad, so that one gesture = one slide). Usually you do not need to change them. ⚠️ This is the ONLY allowed
change inside `<script id="kernel">`, and only when the person asks for it explicitly. Record the fact and the new values
in `DECK.md` (section "Decisions and deviations").

## Speeds (if the person asks for "faster/slower")
- Typing: `data-type-speed` (ms/character). Glitch/drift/cascade: the durations in the matching `@keyframes`
  and `animation` of your design layer. Pipeline: `data-dur` on the stages.

## Accessibility
Wrap large decorative animations (aurora drift, Ken Burns, glitch) in
`@media (prefers-reduced-motion:reduce){ … animation:none }`.

---

## Extracting input material (preinstalled tools only)

### .docx → text (python3 stdlib, no pandoc)
```bash
python3 - "FILE.docx" <<'PY'
import sys,zipfile
from xml.etree import ElementTree as ET
ns='{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
root=ET.fromstring(zipfile.ZipFile(sys.argv[1]).read('word/document.xml').decode('utf-8'))
for p in root.iter(ns+'p'):
    t=''.join(x.text or '' for x in p.iter(ns+'t'))
    if t.strip(): print(t)
PY
```
(`.txt/.md`: read them directly. Use `pandoc` ONLY if it is already installed; do not install it.)

### Numbers from a repository (for proof slides)
```bash
cd REPO
git rev-list --count HEAD                    # total commits
git log --oneline | grep -ciE "story|feat"   # by topic
find . -name '*.kt' | wc -l                  # file count (put in your extension)
```
Take real numbers; do not invent them. If a fact is doubtful, ask or leave it out.

## Check before showing
Run the skill validator (static checks: kernel integrity, leftover `{{…}}`, network links,
`node --check` for the kernel and notes.js, the notes sections in sync with the slides):
```bash
python3 <skill-dir>/assets/validate.py FILE.html
```
The kernel itself checks layout overflow (content taller than the screen): open `file://…/FILE.html?check`
(for the agent: only over http, see below). A plate with the list of problem slides appears.

## Visual self-check in Chrome (claude-in-chrome)

The validator checks the plumbing, but it does not see the layout: it misses overlapping slides, a cut
heading, grey text on dark, a missing image. Because of this, before showing, the agent **looks at the
deck itself**. The check stands on two supports, and both are required: the **auditor** (item 5) gives
numbers — overflow against 16:9, elements out of the frame, broken images, small font size, cut and
overlapping text, empty slides; the **frames** (items 6–7) give what numbers cannot catch — contrast,
rhythm, composition. The procedure below was tested on a live deck; deviations from it cost lost time.

**1. Server.** The extension does not open `file://` (`Can't interact with browser-internal or unparseable
URLs`), so serve the deck over http. Use a free port, and always stop the server at the end:
```bash
cd path/to/deck && nohup python3 -m http.server 8777 --bind 127.0.0.1 >/dev/null 2>&1 &
sleep 1 && curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8777/FILE.html   # wait for 200
# ...check...
pkill -f "http.server 8777"
```

**2. Tab.** `tabs_context_mcp{createIfEmpty:true}` → `navigate` to
`http://127.0.0.1:8777/FILE.html?check`. Close the tab at the end (`tabs_close_mcp`).
You can enter with a batch, but the order matters: an idle `read_console_messages` goes FIRST, before
`navigate`. Otherwise tracking starts after the load, and the `?check` verdict (the kernel prints it
after 400 ms) does not get into the read — see ⚠️ in item 3. Working order:
`read_console_messages` (arms the tracker) → `navigate` → `computer{wait 1}` → both reads from item 3.
On a fresh tab (`chrome://newtab`) the idle read fails with "Can't interact with browser-internal…".
Then: `navigate` → `read_console_messages` → `navigate` to the same URL → `computer{wait 1}` → reads.

**3. Console: the verdict and the errors are two different reads.**
```
read_console_messages{tabId:T,pattern:"deck \?check"}      → the [deck ?check] verdict line (overflow, slide list)
read_console_messages{tabId:T,onlyErrors:true,pattern:"."}  → a design/interactive script that crashed
```
`tabId` is always required. `pattern` is not required by the schema, but set it: without it the whole
log comes out (`"."` = "any message"; only `onlyErrors` filters). You need the second read because
the validator gives only `node --check`, which is syntax. A script that crashes at start
(`querySelector(…)` returned `null`) passes the validator and breaks the deck silently.
**A missing `[deck ?check]` verdict is a diagnosis in itself:** the kernel did not get to it; look for the error above it.
⚠️ The tool counts messages from the moment of ITS first call on the tab ("Console tracking starts
when this tool is first called"), so it can miss errors of the load itself. An empty result
with a missing verdict does not mean "clean"; it means "did not look". Reload the tab (`navigate` to the same URL)
and read again; now tracking is on.

**4. Capture mode.** Kernel functions are global: `go(k)`, `freezeForPrint()`, `unfreezeAfterPrint()`,
`checkOverflow()`, `plate()`. A screenshot right after `go()` catches the slide in the middle of its entry
animation (`slidefade` .55 s): the text is half-transparent and the colors are wrong. But `animation:none`
alone is not enough: the style below fixes two more traps, and **you must not assemble it by hand**.
```js
document.head.insertAdjacentHTML('beforeend','<style id="shotmode">'
+'*{animation:none!important;transition:none!important}'
+'.tab,.card,.reveal,[data-anim],.clist.cascade>*,.chain.seq .node,.chain.seq .arrow{opacity:1!important;transform:none!important}'
+'#deck .bgcopy{display:none!important}'
+'</style>');
freezeForPrint();                                                  // counters finished, cascades/chains/pipeline in the final state
document.querySelectorAll('.deck-plate').forEach(p=>p.remove());   // the ?check plate must not get into the frame
'shotmode on'
```
Why the second line: BY CONTRACT the design layer keeps `.clist.cascade>*` and `.chain.seq .node` at
`opacity:0` until the animation, and a typical card is on `animation:rise .4s forwards` from `opacity:0`. With
`animation:none` there is no animation at all, so there is no final state of it either: without the forced
`opacity:1`, cascade lists and cards are captured EMPTY. The selectors are the same ones the kernel keeps
in `<style id="print">` for exactly this case: **the list is tied to the kernel**. If the print layer
changes, sync `shotmode` too, otherwise it silently drifts apart.
Why the third line: `freezeForPrint()` puts a background copy into each slide, but the copy keeps
`id="bg"`, and the rule `#bg.bgcopy{position:absolute;z-index:-1}` lives only in `@media print`.
On screen the copy matches the base `#bg{position:fixed;z-index:0}` and lies ON TOP of the text: the frame
comes out with a background veil or with no content at all.

**5. Layout auditor.** One `javascript_tool` call for the whole deck. Run it ONLY in capture mode
(otherwise the counters are at zero, `[data-type]` is empty, and the slide is measured in the middle of
`slidefade`; all measurements are wrong). It does not change the active slide and returns only problems:
```js
(()=>{if(!document.getElementById('shotmode'))return'FIRST turn on capture mode (item 4)';
if(document.getElementById('shot169'))return'REMOVE the stage (item 6): it clamps body, and the reference is computed from innerWidth — the numbers will be wrong';
const W=innerWidth,H=W*9/16,MIN=W*H*.01,S=[...document.querySelectorAll('.slide')],out=[],
 live=S.filter(s=>getComputedStyle(s).display!=='none').length;
S.forEach((s,k)=>{const was=s.classList.contains('active');if(!was)s.classList.add('active');
 const p=[],T=[],add=m=>{if(p.length<6&&!p.includes(m))p.push(m)};
 if(s.scrollHeight-H>2)add('taller than 16:9 by '+Math.round(s.scrollHeight-H)+'px');
 if(s.innerText.trim().length<12&&!s.querySelector('img,svg,canvas,video'))add('almost empty: '+s.innerText.trim().length+' chars');
 s.querySelectorAll('*').forEach(e=>{if(e.closest('#bg,.bgcopy'))return;
  if(e.tagName==='IMG'&&e.complete&&!e.naturalWidth)return add('broken image: '+(e.getAttribute('src')||'').slice(0,28));
  const r=e.getBoundingClientRect(),cs=getComputedStyle(e);
  if(!r.width||!r.height||cs.visibility==='hidden')return;
  if(r.right>W+2||r.left<-2||r.top<-2)add('out of frame: '+(e.tagName+'.'+((typeof e.className==='string'?e.className:e.getAttribute('class'))||'').split(' ')[0]).slice(0,24));
  if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return;
  const f=parseFloat(cs.fontSize),t=e.textContent.trim().slice(0,18);
  if(f<H*.013)add('font '+Math.round(f)+'px: '+t);
  if(cs.overflow!=='visible'&&(e.scrollWidth>e.clientWidth+2||e.scrollHeight>e.clientHeight+2))add('clipped: '+t);
  T.push([r,e,t])});
 T.forEach(([a,ea,ta],i)=>T.slice(i+1).forEach(([b,eb,tb])=>{if(ea.contains(eb)||eb.contains(ea))return;
  if(a.width*a.height<MIN||b.width*b.height<MIN)return;
  const w=Math.min(a.right,b.right)-Math.max(a.left,b.left),h=Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top);
  if(w>2&&h>2&&w*h>.3*Math.min(a.width*a.height,b.width*b.height))add('overlap: '+ta+' / '+tb)}));
 if(!was)s.classList.remove('active');if(p.length)out.push({n:k+1,p})});
return{ratio:+(innerWidth/innerHeight).toFixed(3),ideal:Math.round(H),visible:live,bad:out}})()
```
How to read it: `visible` must be `1` (more means the design layer overrode `.slide{display}`, see Don't);
`bad:[]` means clean. Example: `{"ratio":1.828,"ideal":945,"visible":1,"bad":[{"n":3,"p":["taller than 16:9 by 418px","font 9px: source: central bank"]}]}`.
Error margin: `vh` units in padding are computed from the real window, not from the reference (~3 %). This does
not affect the decision "cut or not". Font size and overlaps are **candidates, not a verdict**: many findings
on one slide more likely mean a wrong threshold than a bad deck.

The three thresholds were set on a live deck, not by eye. Do not change them without need:
- **font size `H*0.013`** (≈11 px on a 1512×851 frame). Captions of 12–13 px are valid and common in decks: the
  threshold `0.016` flagged 13 slides out of 17 on a known good deck. Catch what is unreadable, not what is small.
- **overlaps only between blocks larger than 1 % of the frame** (~113×113 px). Without this filter every
  arrow or icon that lies on top of a card counts as an overlap: that is layered composition, not a bug.
- **out of frame is measured per element**, not through the slide `scrollWidth`. `scrollWidth` grows
  from pseudo-elements (a decorative underline, a shadow) that are not in the DOM: there is a finding,
  but nothing to show and nothing to fix.

The auditor does NOT compute contrast and cannot compute it: under the text there is usually `rgba(0,0,0,0)`,
and `#bg` draws the real background as a gradient. Contrast is the job of the frames (item 7).

**6. 16:9 frame and walkthrough.** The browser window is NOT 16:9 (typically ~1.83), and `resize_window` does not fix it.
Do not spend calls on it. The auditor takes the numbers against the reference, but you cannot judge composition
on a frame with wrong proportions. **If the auditor `ratio` is outside 1.70–1.86**, set up the stage:
```js
document.head.insertAdjacentHTML('beforeend','<style id="shot169">'
+'html{background:#808080!important}'
+'body{position:fixed!important;left:50%!important;top:50%!important;transform:translate(-50%,-50%)!important;'
+'width:min(100vw,calc(100vh*16/9))!important;height:min(100vh,calc(100vw*9/16))!important;overflow:hidden!important}'
+'#deck{width:100%!important;height:100%!important}'
+'</style>');'stage on'
```
The stage clamps exactly `body`: its `transform` makes it the containing block for ALL `position:fixed`
descendants, so `#bg` and the deck chrome (`#bar`/`#counter`/`#hint`) move inside the frame. The check
"the counter overlaps the content" stays honest, and you do not need to clamp `#bg` separately. The margin
background comes from an explicit `background` on `html`: while the root background is transparent, the
`body` background spreads over the whole canvas. `#deck` must go to `100%/100%`, otherwise `100vw/100vh`
go out of the stage and the content is clipped. Grey `#808080` is a marker "this is not the deck"; if
the deck itself is grey, take `#ff00ff`. `vh`/`vw` inside slides stay relative to the real window; the
drift equals the ratio deviation (at 1.828 it is 2.7 %). The stage is for composition; the numbers still
come from the auditor. Inside the 1.70–1.86 range do not set up the stage: risk without gain.
The order is required: **the auditor (item 5) runs BEFORE the stage**. It computes the reference from
`innerWidth`, and a `body` clamped by the stage gives numbers that are too low. The auditor checks this
itself and does not run when `shot169` is present.
If you go back to the auditor after fixes (`stages/build.md`, Step 6 — Refinement), first remove the stage (item 10), then measure.

Walkthrough: `browser_batch` in chunks of 4–6 slides. The JS step returns a caption, and it comes as text
right before its frame:
```json
{"actions":[
 {"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":"go(0);'frame 1/10'"}},
 {"name":"computer","input":{"action":"wait","duration":0.2,"tabId":T}},
 {"name":"computer","input":{"action":"screenshot","tabId":T}},
 {"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":"go(1);'frame 2/10'"}},
 {"name":"computer","input":{"action":"wait","duration":0.2,"tabId":T}},
 {"name":"computer","input":{"action":"screenshot","tabId":T}}
]}
```
You need `wait`: in a batch there is no network pause between calls, and the screenshot can catch the previous frame.
Compare the caption with `#counter` in the frame corner; a mismatch is visible at once. A batch saves round trips, not
tokens (10 frames cost the same in one response and in ten), so use chunks: if you see a systemic
problem in the first frames, stop the walkthrough and go fix it. A batch **stops at the first error**
and leaves the deck in capture mode. Exit with a separate step (item 10), not at the end of the batch.

**7. What to look for in the frames.** Content that goes off screen or is cut at the top; several slides
at the same time (see Don't about `.slide`); text on a background without contrast; a heading that breaks
into a line of one word; an empty rectangle instead of an image; deck chrome (`#bar`/`#counter`) that
overlaps the content. Zoom into a small suspect detail with `computer{tabId:T,action:"zoom",region:[x0,y0,x1,y1]}`;
do not guess from the whole frame. When you find a problem, fix it and capture the affected slides again.

**8. What NOT to do.** Do not press `S` or `⌘P`: the system print dialog opens and blocks the
extension until the person closes it by hand. The agent also has no way to check the presenter window (`P`): it is a
separate window and a live scenario of the person (the browser blocks `window.open` from `javascript_tool`:
there is no user gesture). Do not run the auditor outside capture mode. Do not set `save_to_disk` on screenshots:
you need the frames, not the person. Do not fix the aspect ratio through `resize_window`: the window does not obey
("Bounds must be at least 50% within visible screen space"); the stage from item 6 is for that.

**9. PDF — check it with headless print, not by eye in the dialog.** You must not press `S`/`⌘P` in the live
tab (item 8), but you still check the export: Chrome prints from the command line, and
`beforeprint` fires there, so `freezeForPrint()` runs the same way as for the person.
```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --virtual-time-budget=10000 --print-to-pdf=/tmp/deck.pdf "file://$PWD/FILE.html"
pdfinfo /tmp/deck.pdf | grep -E "Pages|Page size"     # pages = slides, sheet 960×540 pts (16:9)
pdfimages -list /tmp/deck.pdf | tail -n +3 | wc -l    # there must be as many rasters as images in the deck
du -h /tmp/deck.pdf                                    # order of magnitude: single MB, not tens
```
`pdfinfo`/`pdfimages`/`pdfseparate` are poppler (`brew install poppler`); a clean macOS does not have it.
Do not install packages yourself (section "Do / Don't" below). Without poppler you have `du -h` and `qlmanage` on the whole
file (it renders the first page). In the report to the person, say honestly what you did not check.
**Look at the pages with the Quartz renderer, not with poppler:** `pdftoppm` shows the PDF
clean even where Preview, Quick Look and any PDF insertion in a macOS app draw garbage.
So the correct check uses the same machinery the person views it with:
```bash
pdfseparate -f 3 -l 3 /tmp/deck.pdf /tmp/p3.pdf && qlmanage -t -s 1400 -o /tmp /tmp/p3.pdf   # /tmp/p3.pdf.png
```
What to look for: grey rectangles over the content (a raster mask, see below), empty places instead of
animated blocks, content cut at the page edge, a white background instead of a colored one, a missing background
on a slide, text over a photo that lost readability (in print `text-shadow` is off, see below).

**Print traps that the kernel removes — know them so that you do not recreate them in the design layer:**
- **Blurred shadow.** Skia writes a `box-shadow` with blur into the PDF as a raster mask (SMask), and Quartz draws
  such a mask as an OPAQUE grey rectangle over the neighbors. At print time (`beforeprint`) the kernel
  replaces blurred layers with a vector hairline `0 0 0 1px` of the same color and restores the originals after;
  it does not touch unblurred layers (rings `0 0 0 2px accent`). `filter:drop-shadow` is correct in Quartz.
  **The limits of the mechanism matter more than the mechanism itself:** it sets an inline style, so it does NOT
  cover a blurred shadow on `::before/::after` (a pseudo-element has no inline style) or a shadow with `!important`. Such
  shadows go into the PDF as a mask and give a grey rectangle. Put blurred shadows on a real element
  and without `!important`. A color in `oklch()/lab()/color()` is used as is, without raising the alpha:
  the hairline comes out paler, but valid.
- **`text-shadow` is off in print completely** (`*{text-shadow:none!important}`): for text, only this cures the raster
  mask. So **you cannot hold contrast on a text shadow**: light text over a
  photo stays without a backing in the PDF. If you need contrast, put a semi-transparent plate or a gradient under it.
- **Mobile breakpoint.** The print layout viewport of a 13.333in page is 756 CSS px, so
  `@media (max-width:900px)` without `screen` fires in EVERY PDF. Write responsive rules only under
  `@media screen and (max-width:…)`.
- **Animation on a pseudo-element.** The print reset `*{animation:none!important}` does not match pseudo-elements:
  a `::before` with `opacity:0` at the animation start goes into the PDF invisible. You need your own pair of rules
  `@media print{…::before{animation:none!important;opacity:1!important;transform:none!important}}`.

**10. Exit.** Return the deck to the live state, close the tab, stop the server:
```js
document.getElementById('shotmode')?.remove();
document.getElementById('shot169')?.remove();
unfreezeAfterPrint();'shotmode off'
```
Then `open FILE.html` (macOS). Check: it pages with arrows/wheel/swipe; `P` opens the presenter window
(on a deck with `data-presenter="off"` it opens nothing)
as a SEPARATE window (not a tab) and it stays in sync; `B` blanks the screen; media are visible; there are no speaker notes on the deck itself. Live notes: change a line in
`<slug>-notes.js` while the presenter window is open; the text updates within a couple of seconds (the
`● notes.js` indicator in the presenter window header is green). Editing from inside is done with mouse buttons (the presenter window
has no letter hotkeys; only arrows, `Esc`, `⌘⏎`): the edit button (✎) or a double click on the text →
the apply button (✓) (the indicator switches to the draft state ✎), the all-notes button (☰) — all text at once, the revert button (↺) —
back to the file, the export button (⤓ notes.js) — save the file to Downloads and put it next to the deck over the old one.
The built-in help (the ? button) explains to the speaker what works and how. If the person asks for a PDF: `S` (or `⌘P`) → "Save as PDF": a page
16:9 without margins, slide = page; counters, cascades, chains, pipeline and typed text freeze
in their final frame on ALL slides, and the `#bg` background is copied into each page. Images from `deck-assets/` get
into the PDF if the deck is opened from its folder (with `deck-assets/` next to it); a GIF gives its first frame.

## Do / Don't
- **Do:** one idea — one slide; short headings; every number is a counter; every slide has `data-notes` (except a deck without the presenter window);
  design the visuals for the CONTENT along the axes (`design-axes.md`), and change the composition across the deck; everything offline.
- **Don't:** do not override `.slide{display:…}` in the design layer. The base keeps slides on
  `.slide{display:none}` + `.slide.active{display:flex}`, and your `display:flex` shows ALL slides at once
  (the validator does not catch this; a screenshot catches it at once). In the design layer set `padding`/`gap`/`justify-content`,
  and set `display` only through `.slide.active`;
  do not put 15 bullets on a slide; do not take visuals from past decks, from other `*.html` in the input folder
  or from your head "as usual": decide the axes again for this talk; do not pull fonts/images from the network; do not edit `<script id="kernel">`
  and the chrome DOM; do not install packages; do not invent statistics; no more than one "loud" animation per slide;
  do not put a click on a `div` without `[data-interactive]`: the kernel takes it as a click on the slide and pages forward;
  do not use `backdrop-filter` in slides: it conflicts with the slide entry transform animation (`slidefade`),
  and the frame renders with a glitch. Use a static radial/linear fill instead.

---

## Interactivity: the kernel contract

There are no ready-made widgets here, and there will be none, for the same reason the component gallery
was removed from here. **What** to make interactive, and whether to do it at all, is axis 9 in `design-axes.md`. Here is
only the plumbing: how a widget lives together with navigation, the presenter window and print.

**Where to write JS.** Into a separate script block `<script id="interactive">` **after**
`<script id="kernel">`, before the closing `</body>`. If you insert it with a build script, match
the LAST occurrence of `</body>`: the first one is inside the kernel, in the string that builds the presenter window. The kernel itself is still not touched. Vanilla JS,
no libraries, offline, like everything else in the deck.
**Wrap your code in an IIFE** (`(()=>{ … })()`): both blocks live in one global scope, and
a second declaration of a name the kernel already uses kills your whole block with a `SyntaxError` before
it runs. Taken names, besides the obvious ones: `go`, `render`, `slides`, `freezeForPrint`,
`unfreezeAfterPrint`, `flattenShadows`, `restoreShadows`, `shadowLayers`, `liftAlpha`,
`markRasterLayers`, `checkOverflow`, `plate`, `savePDF`, `toggleBlank`, `presenterOff`, `I18N`,
`__kT`, `__kLang`, `__kLangAttr`.

**What kernel v6 takes on itself** (v5 and earlier do not have this: on an old kernel interactivity breaks
navigation, and you must move the deck to a fresh `kernel.html`):

| Situation | Kernel behavior |
|---|---|
| click on `a,button,label,summary,details,video,audio,input,textarea,select,[contenteditable],[role="button"]` | the slide does NOT page |
| click on your own zone marked `[data-interactive]` | the slide does NOT page (opt-out for any author markup) |
| any key while focus is in `input/textarea/select/[contenteditable]` | does not reach navigation: `p`, `b`, `s`, space are typed, not used as hotkeys |
| space or Enter while focus is on a button/link/`summary` | activates the element, does not page |
| click, wheel and touch gesture inside `[data-scroll]` | go to the zone: scrolling and text selection do not page the slide |

The `← →` arrows always page the deck, even when focus is on a widget button: after a click, focus
stays on it, and navigation must not be lost there.

**What stays on you:**

- **Reset when the slide opens.** The kernel replays only its own animators; it does not know about your widget.
  If the viewer leaves the slide and comes back, the widget stays in the state in which it was
  left. If you need a clean start, listen for the `active` class:
  ```js
  document.querySelectorAll('.slide').forEach(s=>{
    new MutationObserver(()=>{ if(s.classList.contains('active')) resetWidget(s) })
      .observe(s,{attributes:true,attributeFilter:['class']});
  });
  ```
  The observer fires in a microtask, not instantly. When you check the reset from the console, pause
  between `go()` and reading the state. Otherwise you see the old value and go fix code that works.
- **Keyboard and focus.** A clickable thing is a `<button>`, not a `<div onclick>`: this way
  `Tab` and `Enter` work, and the kernel recognizes the interactive element and does not page the slide. If you use your own markup instead of a button,
  add `[data-interactive]`, `tabindex` and `role="button"`, otherwise the widget cannot be reached
  from the keyboard. And remember: on Enter/Space the browser does NOT send a synthetic `click` to a non-button. The kernel
  does not pass the key to navigation, but you handle the press yourself, with your own `keydown`.
- **Print.** `freezeForPrint()` does not know about the widget: the PDF gets exactly the state that is in the DOM
  at print time. Data hidden behind a press: either duplicate it as static content, or tell
  the person honestly that it will not be in the PDF. Your own class with `opacity:0` outside the contract hooks
  prints invisible (see the warning earlier in this file).
- **`?check` measures the default state.** Check an accordion that opens to half the screen
  in its open state: by hand, by eye and on a real 16:9.
- **Presenter preview.** The mini preview is an iframe with a snapshot of `documentElement.outerHTML`, so your
  script runs there once more. The code must be idempotent, light and without side effects
  outside (`window.open`, writes to `localStorage`, global timers). Otherwise the presenter window
  starts to live its own life.
- **Speaker notes.** On an interactive slide, `data-notes` has a remark about what to press and when
  (`[click "after" — the number changes]`). The speaker reads the notes and does not have to guess.
- **Affordance.** Cursor `pointer`, a visible state (pressed/selected/open), and a micro caption if needed.
  Keep the widget away from the corners: the deck chrome lives there (`#bar`, `#counter`,
  `#hint`, `z-index:50`), and it covers the hit zone.
- **Motion** inside the widget is turned off in `@media (prefers-reduced-motion:reduce)`, like everything
  else.

**Scrollable zone** (a long table, a list, code): the zone itself plus a mark for the kernel:
```html
<div class="ledger" data-scroll style="overflow:auto;max-height:52vh">…</div>
```
Without `[data-scroll]` the wheel goes to navigation and pages the slide instead of scrolling.

---

## Design layer skeleton (structure, NOT a look)

There is intentionally no ready art direction here: while the cookbook held one full example, decks came out
as its recolored copies, down to the literal `--bg:#0a0b0f` and `--accent:#f5b942` in different
talks. Visual decisions are made by `design-axes.md` (9 axes). Below is only the frame: which
slots the design layer must fill so that the kernel does not play into nothing.

```css
/* 1. TOKENS — your own names, values from your art direction (axes 4 and 3) */
:root{ /* background, surface, text, muted, line, 1 accent; font stacks */ }

/* 2. BASE — body and #bg (axis 5: most often #bg is not touched at all) */
body{ /* background and text color, base font */ }

/* 3. TYPOGRAPHY — h1/h2 and a text class; character comes from line-height,
      letter-spacing and column width, not from the choice of face (axis 3) */

/* 4. COMPOSITION — layout classes for DIFFERENT slide types, not one look for all (axis 1) */
.slide.poster{ } .slide.split{ } .slide.hero-num{ }

/* 5. CHROME — part of the visuals, you can change its styling (axis 8) */
#bar{ } #counter{ } #hint{ }

/* 6. SLIDE TRANSITION — overridden by a rule with the same name, the kernel allows this (axis 6) */
@keyframes slidefade{ /* your own entry character: zoom / curtain / shift / plain fade */ }

/* 7. COMPONENTS — only those this deck really needs; by the class contract above
      these states are required: .chain.seq .node/.node.show, @keyframes gitin for .clist,
      .pstage/.pstage.on/.pstage.done for .pipeline, animation on .reveal/.tab/.card */

/* 8. ACCESSIBILITY */
@media (prefers-reduced-motion:reduce){ /* turn off background motion and "loud" animations */ }
```

How each slot looks is decided again for each talk. If you need a sample of someone else's taste, that is the person's
`design.md` or a URL reference (`art-direction.md`), not a neighboring deck.
