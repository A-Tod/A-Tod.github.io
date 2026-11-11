/* ===== Black Friday 2026 — התנהגות =====================================
   נוסף כקובץ נפרד. לא נוגע בקוד קיים ולא תלוי בו.

   1. מפעיל את הסינון בעמוד הדגמים (הבאנר והרשת עצמם הם HTML בעמוד).
   2. מטפל בשני טפסי ההרשמה — הכללי שבבאנר, והפרטני שבדף מוצר.
   3. שולח כל הרשמה ל-webhook. האישור מוצג אך ורק אחרי תשובה חיובית.

   אין שמירה מקומית של הרשמות. מקור האמת הוא הגיליון שמאחורי ה-webhook.
   ========================================================================= */

(() => {
  'use strict';

  /* ---------- הגדרות ---------- */
  // כתובת ה-webhook של Make. היא גלויה בקוד המקור של האתר — זה בלתי נמנע
  // בטופס שרץ בדפדפן. היא יודעת רק להוסיף שורה לגיליון, ואפשר להחליף אותה
  // ב-Make בכל רגע. ריק = הטפסים מושבתים.
  const ENDPOINT = 'https://hook.eu2.make.com/y76so83sptz4iv3wei11vr9pkn3hknnq';
  const CAMPAIGN = 'bf2026';
  const CONSENT_VERSION = 'v11';
  const CONSENT_TEXT =
    'אני מאשר/ת קבלת תזכורת במייל על מבצע הבלאק פריידי של A-Tod.';

  /* ---------- הודעות ---------- */
  const MSG = {
    badMail  : 'כתובת המייל אינה תקינה. אפשר לתקן ולנסות שוב.',
    noConsent: 'יש לאשר את קבלת התזכורת כדי להירשם.',
    failed   : 'ההרשמה לא נשמרה. אפשר לנסות שוב.',
    offline  : 'ההרשמה עדיין לא חוברה. בקרוב.',
    sending  : 'שומר…',
    okGeneral: 'נרשמתם. הקישור יישלח אליכם עם פתיחת המבצע.',
    okModel  : name => 'נרשמתם לתזכורת עבור ' + name +
                       '. הקישור יישלח אליכם עם פתיחת המבצע.'
  };

  const validMail = v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(v).trim());

  /* ---------- שליחה ---------- */
  async function save(data){
    if(!ENDPOINT){ const e = new Error('not connected'); e.offline = true; throw e; }
    const res = await fetch(ENDPOINT, {
      method : 'POST',
      headers: {'Content-Type':'application/json'},
      body   : JSON.stringify(Object.assign({
        campaign       : CAMPAIGN,
        consent        : true,
        consentText    : CONSENT_TEXT,
        consentVersion : CONSENT_VERSION,
        consentAt      : new Date().toISOString(),
        ts             : new Date().toISOString(),
        pageUrl        : location.href
      }, data))
    });
    if(!res.ok) throw new Error('http ' + res.status);
    return true;
  }

  /* ---------- טופס אחד ----------
     מצופה בתוך form[data-bf-form]: input[type=email], input[type=checkbox],
     button[type=submit]; ולידו p[data-bf-msg] להודעות.                    */
  function wireForm(form){
    const mail = form.querySelector('input[type="email"]');
    const ok   = form.querySelector('input[type="checkbox"]');
    const btn  = form.querySelector('button[type="submit"]');
    const msg  = form.parentElement.querySelector('[data-bf-msg]');
    if(!mail || !ok || !btn || !msg) return;

    const source    = form.getAttribute('data-bf-form')    || 'unknown';
    const modelId   = form.getAttribute('data-model-id')   || '';
    const modelName = form.getAttribute('data-model-name') || '';
    const modelUrl  = form.getAttribute('data-model-url')  || '';

    function show(kind, text){
      msg.className = 'bf-msg bf-msg--' + kind;
      msg.textContent = text;
      msg.hidden = false;
    }
    function clear(){
      msg.hidden = true;
      mail.removeAttribute('aria-invalid');
    }

    mail.addEventListener('input', clear);
    ok.addEventListener('change', clear);

    form.addEventListener('submit', async e => {
      e.preventDefault();
      clear();

      const value = mail.value.trim();
      if(!validMail(value)){
        mail.setAttribute('aria-invalid','true');
        show('err', MSG.badMail);
        mail.focus();
        return;
      }
      if(!ok.checked){
        show('err', MSG.noConsent);
        ok.focus();
        return;
      }

      const label = btn.textContent;
      btn.disabled = true;
      btn.textContent = MSG.sending;

      try{
        await save({
          email    : value,
          source   : source,
          modelId  : modelId,
          modelName: modelName,
          modelUrl : modelUrl
        });
        // אישור רק אחרי שמירה בפועל.
        // מדידה: אירוע Lead אחד לכל דפדפן, גם אם נרשמו לכמה דגמים.
        // נשלח רק כאן, אחרי תשובה חיובית מה-webhook.
        try{
          if(!localStorage.getItem('atod_bf_lead')){
            localStorage.setItem('atod_bf_lead', new Date().toISOString());
            window.atodTrack && window.atodTrack('bf_signup',
              { method: source, item_id: modelId || undefined, item_name: 'Black Friday 2026' });
          }
        }catch(_){}
        form.hidden = true;
        show('ok', modelName ? MSG.okModel(modelName) : MSG.okGeneral);
        msg.setAttribute('tabindex','-1');
        msg.focus();
      }catch(err){
        btn.disabled = false;
        btn.textContent = label;
        show('err', err && err.offline ? MSG.offline : MSG.failed);
      }
    });
  }

  /* ---------- סינון בעמוד הדגמים ----------
     הכרטיסים נושאים data-bf-type, הכפתורים data-bf-filter.               */
  function wireFilters(){
    const bar = document.querySelector('[data-bf-filters]');
    if(!bar) return;

    const cards = [].slice.call(document.querySelectorAll('[data-bf-type]'));
    if(!cards.length) return;

    const count = document.querySelector('[data-bf-count]');
    const chips = [].slice.call(bar.querySelectorAll('[data-bf-filter]'));

    function apply(key){
      let shown = 0;
      cards.forEach(card => {
        const types = (card.getAttribute('data-bf-type') || '').split(/\s+/);
        const on = key === 'all' || types.indexOf(key) >= 0;
        card.hidden = !on;
        if(on) shown++;
      });
      chips.forEach(c =>
        c.setAttribute('aria-pressed',
          String(c.getAttribute('data-bf-filter') === key)));
      if(count){
        count.textContent = (shown === cards.length)
          ? ''
          : shown + ' מתוך ' + cards.length + ' דגמים';
      }
    }

    chips.forEach(c =>
      c.addEventListener('click', () => apply(c.getAttribute('data-bf-filter'))));
    apply('all');
  }

  /* ---------- גלילה לרשת הדגמים ---------- */
  function wireScroll(){
    document.querySelectorAll('[data-bf-scroll]').forEach(btn => {
      btn.addEventListener('click', e => {
        const sel = btn.getAttribute('data-bf-scroll');
        const target = sel && document.querySelector(sel);
        if(!target) return;
        e.preventDefault();
        const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        target.scrollIntoView({behavior: reduce ? 'auto' : 'smooth', block:'start'});
        const focusable = target.querySelector('a,button') || target;
        focusable.setAttribute('tabindex','-1');
        setTimeout(() => focusable.focus({preventScroll:true}), reduce ? 0 : 450);
      });
    });
  }

  /* ---------- הבאנר מתכווץ תוך כדי גלילה ----------
     --bf-p נע מ-0 (באנר מלא) ל-1 (פס דק) לאורך RANGE פיקסלים ראשונים.
     ה-CSS גוזר ממנו את הריפוד, גודל הכותרת ושקיפות הטקסט.          */
  function wireShrink(){
    const hero = document.querySelector('.bf-hero');
    if(!hero) return;

    /* הבאנר דביק, ולכן כשהוא מתכווץ גובה העמוד מתקצר והתוכן עולה.
       אם הוא מתכווץ מהר יותר מקצב הגלילה, הדפדפן מושך את הגלילה אחורה
       והבאנר "נתקע". לכן טווח הגלילה חייב להיות גדול מהפרש הגבהים —
       מודדים אותו בפועל ומכפילים, במקום לנחש מספר קבוע.              */
    let range = 220;
    function measure(){
      const before = hero.style.getPropertyValue('--bf-p');
      hero.style.setProperty('--bf-p', '0');
      const full = hero.getBoundingClientRect().height;
      hero.style.setProperty('--bf-p', '1');
      const min = hero.getBoundingClientRect().height;
      hero.style.setProperty('--bf-p', before || '0');
      range = Math.max(180, Math.round((full - min) * 1.8));
    }

    let queued = 0;
    function update(){
      queued = 0;
      const p = Math.min(1, Math.max(0, window.scrollY / range));
      hero.style.setProperty('--bf-p', p.toFixed(3));
    }
    function remeasure(){ measure(); update(); }

    measure();
    update();
    window.addEventListener('scroll', () => {
      if(!queued) queued = requestAnimationFrame(update);
    }, {passive:true});
    window.addEventListener('resize', remeasure, {passive:true});
    if(document.fonts && document.fonts.ready) document.fonts.ready.then(remeasure);
  }

  /* ---------- הפעלה ---------- */
  function init(){
    wireShrink();
    wireFilters();
    wireScroll();
    document.querySelectorAll('form[data-bf-form]').forEach(wireForm);

    // ללא webhook: הטפסים מושבתים ומסבירים למה. לא מעמידים פנים שזה עובד.
    if(!ENDPOINT){
      document.querySelectorAll('form[data-bf-form]').forEach(f => {
        f.querySelectorAll('input,button').forEach(el => { el.disabled = true; });
        const msg = f.parentElement.querySelector('[data-bf-msg]');
        if(msg){
          msg.className = 'bf-msg bf-msg--err';
          msg.textContent = MSG.offline;
          msg.hidden = false;
        }
      });
    }
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
