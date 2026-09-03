/* ══════════════════════════════════════════════════════════════════════════
   09 · «нажми на деку» — единственный виджет этой деки (ось 9).
   Тезис слайда: менялся только design.md. Нажатие показывает это на живом
   объекте: превью — кнопки, и выбранная палитра надевается на ЭТУ деку.
   Слайд читается и без нажатия: три превью с подписями на месте.

   Контракт с kernel v6 (assets/cookbook.md):
     · превью размечены <button> — движок сам не листает слайд по клику в кнопку,
       Enter/Space жмут кнопку, стрелки продолжают листать деку;
     · тема живёт инлайном на <html> (перебивает :root в <style id="design">),
       снимается при любой смене слайда и перед печатью — в PDF и на соседних
       слайдах дека всегда в родной палитре;
     · побочных эффектов наружу нет (ни window.open, ни хранилищ, ни таймеров) —
       скрипт безопасно выполняется второй раз внутри превью окна докладчика.

   Палитры сняты с самих скриншотов (PIL, медианный срез), а не подобраны на глаз.
   ══════════════════════════════════════════════════════════════════════════ */
(function(){
  'use strict';

  var THEMES = {
    /* deck-01-flying-papers.jpg — сиреневый плакат с кислотно-жёлтым */
    acid:{
      '--canvas':'#7a78b5','--paper':'#2a2848','--ink':'#ffffff','--black':'#171533',
      '--slate':'#ece9ff','--charcoal':'#ddd9f5','--stone':'#e4e2f4','--mist':'#3a3760',
      '--sand':'#4b4878','--driftwood':'#b9b6dd',
      '--accent-rgb':'241,236,99','--on-accent':'#171533','--on-ink':'#171533','--on-black':'#ffffff',
      '--cap-on':'#ffffff',   /* жёлтым мелким по сиреневому не почитаешь — подпись выбранной деки белая */
      '--bg-glow':'rgba(241,236,99,.13)','--bg-warm':'rgba(45,42,80,.45)',
      '--bar-grad':'linear-gradient(90deg,#f1ec63,#fff59c)',
      '--sh-xl':'rgba(0,0,0,.34) 0 28px 64px 0, rgba(0,0,0,.12) 0 2px 8px 0',
      '--sh-sm':'rgba(0,0,0,.26) 0 12px 32px 0, rgba(0,0,0,.10) 0 2px 6px 0',
      '--r-card':'20px','--r-node':'14px','--r-img':'10px','--r-pill':'99px',
      '--h-family':'var(--sans)','--h-style':'normal','--h1-w':'900','--h2-w':'800','--h-track':'-.03em'
    },
    /* deck-02-iad-lab.jpg — чёрный swiss: второго цвета нет, углы прямые */
    swiss:{
      '--canvas':'#1e1e1e','--paper':'#2b2b2b','--ink':'#f8f8f8','--black':'#f8f8f8',
      '--slate':'#dcdcdc','--charcoal':'#c9c9c9','--stone':'#9a9a9a','--mist':'#3a3a3a',
      '--sand':'#3a3a3a','--driftwood':'#6f6f6f',
      '--accent-rgb':'248,248,248','--on-accent':'#141414','--on-ink':'#141414','--on-black':'#141414',
      '--bg-glow':'rgba(255,255,255,.05)','--bg-warm':'rgba(255,255,255,.03)',
      '--bar-grad':'linear-gradient(90deg,#f8f8f8,#8a8a8a)',
      /* тень на почти чёрном не видна — её роль берёт волосяная светлая кромка */
      '--sh-xl':'rgba(255,255,255,.11) 0 0 0 1px','--sh-sm':'rgba(255,255,255,.08) 0 0 0 1px',
      '--r-card':'0px','--r-node':'0px','--r-img':'0px','--r-pill':'0px',
      '--h-family':'var(--sans)','--h-style':'normal','--h1-w':'700','--h2-w':'700','--h-track':'-.035em'
    },
    /* deck-03-aptos.jpg — мятный editorial с засечками */
    mint:{
      '--canvas':'#d5f9d3','--paper':'#f1faeb','--ink':'#10240f','--black':'#0f1f0e',
      '--slate':'#24401f','--charcoal':'#37503a','--stone':'#6f8a6d','--mist':'#cfe8cc',
      '--sand':'#bcd9b9','--driftwood':'#9db69b',
      '--accent-rgb':'17,17,17','--on-accent':'#f1faeb','--on-ink':'#f1faeb','--on-black':'#f1faeb',
      '--bg-glow':'rgba(120,190,120,.28)','--bg-warm':'rgba(230,246,225,.85)',
      '--bar-grad':'linear-gradient(90deg,#111111,#4a7a4a)',
      '--sh-xl':'rgba(20,60,20,.17) 0 26px 60px 0, rgba(20,60,20,.07) 0 2px 8px 0',
      '--sh-sm':'rgba(20,60,20,.11) 0 12px 30px 0, rgba(20,60,20,.05) 0 2px 6px 0',
      '--r-card':'6px','--r-node':'4px','--r-img':'4px','--r-pill':'99px',
      '--h-family':'var(--serif)','--h-style':'normal','--h1-w':'400','--h2-w':'400','--h-track':'-.01em'
    }
  };

  var slide = document.getElementById('s09');
  if(!slide) return;
  var picks = [].slice.call(slide.querySelectorAll('.deckpick'));
  var hint  = slide.querySelector('.pickhint');
  var root  = document.documentElement;
  var bg    = document.getElementById('bg');
  if(!picks.length || !hint) return;

  var HINT_IDLE = hint.innerHTML;
  var current = null;

  /* все ключи всех тем — снимаем скопом, чтобы переход между темами не оставлял хвостов */
  var ALL_KEYS = Object.keys(THEMES).reduce(function(acc,name){
    Object.keys(THEMES[name]).forEach(function(k){ if(acc.indexOf(k)<0) acc.push(k); });
    return acc;
  },[]);

  function paint(name, quiet){
    var theme = name ? THEMES[name] : null;
    if(name && !theme) return;                       // опечатка в data-theme не должна убивать виджет
    ALL_KEYS.forEach(function(k){ root.style.removeProperty(k); });
    if(theme) Object.keys(theme).forEach(function(k){ root.style.setProperty(k,theme[k]); });
    current = name;
    picks.forEach(function(b){
      var on = b.dataset.theme===name;
      b.setAttribute('aria-pressed', String(on));
      /* подпись живёт вне кнопки (figcaption обязан лежать в figure) — метим сам figure */
      if(b.parentElement) b.parentElement.classList.toggle('on', on);
    });
    if(name){
      var label = picks.filter(function(b){ return b.dataset.theme===name; })[0].dataset.label || name;
      hint.innerHTML = 'на экране сейчас <b>'+label+'</b> · нажми ещё раз, чтобы вернуть родную';
    }else{
      hint.innerHTML = HINT_IDLE;
    }
    /* фон проявляется заново — смена палитры читается как событие, а не как глюк.
       На сбросе из печати пульс не нужен: это лишний reflow внутри печатного пути. */
    if(bg && !quiet){ bg.classList.remove('swap'); void bg.offsetWidth; bg.classList.add('swap'); }
  }

  picks.forEach(function(b){
    b.addEventListener('click', function(e){
      paint(b.dataset.theme===current ? null : b.dataset.theme);
      if(e.detail) b.blur();   // мышь: снимаем фокус, иначе пробел жмёт кнопку, а не листает дальше
    });
  });

  /* тема глобальная — уходя со слайда, дека обязана вернуться в родную палитру.
     Наблюдатель срабатывает в микротаске: проверяя сброс из консоли, ставь паузу. */
  new MutationObserver(function(){ if(current) paint(null); })
    .observe(slide,{attributes:true,attributeFilter:['class']});

  window.addEventListener('keydown', function(e){
    if(e.metaKey||e.ctrlKey||e.altKey||!current) return;
    if(e.target instanceof Element && e.target.closest('input,textarea,select,[contenteditable]')) return;
    if(e.key.toLowerCase()==='p') paint(null);      // P открывает presenter — снимок должен быть в родной палитре
  }, true);

  /* печать: kernel уже заморозил кадры своим beforeprint — снимаем поверх ещё и тему,
     иначе в PDF уедет случайно нажатая чужая палитра */
  window.addEventListener('beforeprint', function(){ if(current) paint(null, true); });
})();
