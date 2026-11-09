// Run with node --test tests/test_presenter.cjs; no browser dependency.
const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');
const html=fs.readFileSync(path.join(__dirname,'../assets/kernel.html'),'utf8');
const script=html.match(/<script id="kernel">([\s\S]*?)<\/script>/)[1];
function fixture(){
  const elements={};
  function el(id){return elements[id]??=( {innerHTML:'',style:{},value:'',attributes:{},setAttribute(k,v){this.attributes[k]=v},focus(){},setSelectionRange(){}} )}
  const slides=[{dataset:{notes:'Full speech [pause]',cues:'- **Main idea**\n  A short reminder.',discussion:'- **What do you think?**\n  Invite an example.'},querySelector(){return null}},
    {dataset:{notes:'Second speech'},querySelector(){return null}}];
  const storage=new Map();
  const ctx=vm.createContext({slides,i:0,window:{frameElement:true},location:{href:'file:///talk.html'},
    localStorage:{setItem(k,v){storage.set(k,v)},getItem(k){return storage.get(k)||null},removeItem(k){storage.delete(k)}},
    fmt:n=>String(n+1).padStart(2,'0'),setTimeout:()=>0,clearTimeout(){},
    __kLangAttr:'en',__kT:{pCues:'Cues',pFull:'Full text',pDiscussion:'Discuss with the audience',noCues:'No cues',noDiscussion:'No discussion',tipDraft:'draft',tipDraftF5:'',tipDraftDl:'',plFileNew:n=>n,help:[]}});
  vm.runInContext(script.slice(script.indexOf('  let presenter='),script.indexOf('  // ── live notes: sidecar')),ctx);
  const modelStart=script.indexOf('  let notesEverOk=');
  const modelEnd=script.indexOf('  // ── keyboard and click',modelStart);
  assert.ok(modelEnd>modelStart,'live-notes region must exist');
  vm.runInContext(script.slice(modelStart,modelEnd),ctx);
  ctx.pd={getElementById:el};
  vm.runInContext('presenter={document:pd,closed:false};notePlate=()=>{}',ctx);
  const run=code=>vm.runInContext(code,ctx);
  return {run,slides,el,storage};
}
test('opens with cues and keeps discussion on both tabs',()=>{
  const {run,el}=fixture();run('updatePresenter()');
  assert.match(el('note').innerHTML,/Main idea/);assert.doesNotMatch(el('note').innerHTML,/Full speech/);
  const discussion=el('discussion').innerHTML;
  assert.match(discussion,/What do you think/);
  run("selectNoteMode('notes')");assert.match(el('note').innerHTML,/Full speech/);
  assert.equal(el('discussion').innerHTML,discussion);assert.equal(el('tab-notes').attributes['aria-selected'],'true');
  run('i=1;updatePresenter()');assert.match(el('note').innerHTML,/Second speech/);
  assert.match(el('discussion').innerHTML,/No discussion/);
});
test('structured notes round-trip all fields, including empty values',()=>{
 const {run,slides}=fixture();const before=JSON.stringify(slides.map(s=>({notes:s.dataset.notes||'',cues:s.dataset.cues||'',discussion:s.dataset.discussion||''})));
 run('parseNotesMD(notesToMD())');assert.equal(JSON.stringify(slides.map(s=>({notes:s.dataset.notes,cues:s.dataset.cues,discussion:s.dataset.discussion}))),before);
 const output=run('notesFileText()');assert.match(output,/### Discussion/);assert.match(output,/What do you think/);
});
test('Russian headings, CRLF and blank cues/discussion parse without leaking headings into speech',()=>{
 const {run}=fixture();
 const body='### Тезисы\r\n- **Мысль**\r\n  Подсказка.\r\n\r\n### Полный текст\r\nРечь.\r\n### Обсудить с залом\r\n- Вопрос?';
 const result=run('parseNoteBody('+JSON.stringify(body)+')');assert.equal(result.notes,'Речь.');assert.match(result.cues,/Мысль/);assert.equal(result.discussion,'- Вопрос?');
 assert.equal(run('parseNoteBody("### Cues\\n\\n### Full text\\n\\n### Discussion\\n").notes'),'');
});
test('legacy notes remain complete speech, without stale cues/discussion',()=>{
 const {run,slides}=fixture();run('parseNotesMD("## 01 · Title\\nLegacy speech\\n### My heading\\nMore text")');
 assert.equal(slides[0].dataset.notes,'Legacy speech\n### My heading\nMore text');assert.equal(slides[0].dataset.cues,'');assert.equal(slides[0].dataset.discussion,'');
 run('updatePresenter()');assert.equal(run('noteMode'),'cues');
});
test('tab switch saves only the active field; cancel keeps previous discussion',()=>{
 const {run,el,slides}=fixture();run('startEdit()');el('noteedit').value='- Updated cue\n  Remember this.';run("selectNoteMode('notes')");
 assert.match(slides[0].dataset.cues,/Updated cue/);assert.equal(slides[0].dataset.notes,'Full speech [pause]');
 run("startEdit('discussion')");el('discussionedit').value='- Changed question';run('cancelEdit()');assert.match(slides[0].dataset.discussion,/What do you think/);
 run("startEdit('discussion')");el('discussionedit').value='- Changed question';run('commitEdit()');assert.equal(slides[0].dataset.discussion,'- Changed question');
 assert.match(run('draftMD'),/Updated cue/);assert.match(run('draftMD'),/Changed question/);
});
test('revert and restore preserve all three embedded fields',()=>{
 const {run,el,slides}=fixture();run("startEdit('discussion')");el('discussionedit').value='- New question';run('commitEdit();revertDraft()');
 assert.match(slides[0].dataset.discussion,/What do you think/);run('restoreStale()');assert.equal(slides[0].dataset.discussion,'- New question');
});
test('changed live file waits for editing, then wins and keeps the complete draft recoverable',()=>{
 const {run,el,slides}=fixture();run('draftChecked=true;draftBase=notesToMD();startEdit()');el('noteedit').value='- Draft cue';
 run('window.DECK_NOTES="## 01\\n### Cues\\n- File cue\\n### Full text\\nFile speech\\n### Discussion\\n- File question";applyNotes(true)');
 assert.match(slides[0].dataset.cues,/Main idea/);run('commitEdit()');assert.equal(slides[0].dataset.cues,'- File cue');assert.equal(slides[0].dataset.discussion,'- File question');
 assert.match(run('staleDraft'),/Draft cue/);run('restoreStale()');assert.equal(slides[0].dataset.cues,'- Draft cue');assert.match(slides[0].dataset.discussion,/What do you think/);
});
test('bullets display headings and explanations as text, not executable HTML',()=>{
 const {run}=fixture();const text='- **A <script>**\n  <img src=x onerror=alert(1)>\n- Another thought\n  Brief explanation.';
 const result=run('renderBullets('+JSON.stringify(text)+',"empty")');assert.equal((result.match(/<li>/g)||[]).length,2);assert.match(result,/&lt;img/);assert.doesNotMatch(result,/<script>|<img/);assert.match(result,/class="cue-detail"/);
});

test('equivalent legacy and structured speech do not create a false file conflict',()=>{
 const {run}=fixture();
 const legacy='## 01\nUpdated speech';
 const structured='## 01\n### Cues\n\n### Full text\nUpdated speech\n\n### Discussion\n';
 assert.equal(run('notesMap('+JSON.stringify(legacy)+')'),run('notesMap('+JSON.stringify(structured)+')'));
});
