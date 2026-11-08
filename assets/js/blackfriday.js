/* ===== Black Friday 2026 — מודול עצמאי ================================= */
/* נוסף בסוף main.js. לא נוגע בקוד קיים ולא תלוי בו.                      */

(() => {
  'use strict';

  /* ---------- הגדרות שדורשות ערך ממך ---------- */
  const ENDPOINT = '';                  // ← כתובת ה-webhook מ-Make
  const PRIVACY  = 'privacy.html';      // ← לאמת מול הנתיב האמיתי באתר
  const CATALOG  = 'collection.html';
  const CAMPAIGN = 'bf2026';
  const KEY      = 'atod.bf2026';

  /* ---------- טקסטים מאושרים — לא לשנות ---------- */
  const T = {
    kicker  : 'BLACK FRIDAY',
    h1      : 'איזה גוף תאורה<br>ייכנס אליכם הביתה?',
    perk1   : '25% על גוף התאורה הראשון',
    perk2   : '30% על כל גוף נוסף · משלוח חינם',
    body    : 'בחרו את הגוף שלכם. את פתיחת<br>המבצע כבר לא תצטרכו לזכור.<br>השאירו מייל וקבלו קישור ישיר<br>לרכישה ברגע שהמבצע נפתח.',
    ph      : 'כתובת המייל',
    consent : 'אני מסכים/ה לקבל מיילים<br>על המבצע · ',
    privacy : 'מדיניות הפרטיות',
    submit  : 'הרשמה',
    okH     : 'ההרשמה התקבלה.',
    okBody  : 'קישור למבצע יישלח<br>למייל עם פתיחתו.',
    okHint  : 'רוצים קישור ישיר לדגם מסוים?<br>בדף המוצר לוחצים על<br>״תזכירו לי לימי המבצע״.',
    okBtn   : 'למציאת גוף התאורה שלי',
    remind  : 'תזכירו לי לימי המבצע',
    inline  : n => `קבלו למייל קישור ישיר ל־<bdi>${n}</bdi> עם פתיחת המבצע.`,
    saved   : n => `קישור ל־<bdi>${n}</bdi> יישלח<br>למייל עם פתיחת המבצע.`,
    remindBtn:'תזכירו לי'
  };

  /* ---------- הודעות מערכת ---------- */
  const M = {
    badMail : 'כתובת המייל אינה תקינה.',
    noConsent:'יש לאשר קבלת מיילים כדי להירשם.',
    failed  : 'השמירה נכשלה. אפשר לנסות שוב.',
    sending : 'שולח…'
  };

  /* ---------- אחסון מקומי, עמיד לחסימה ---------- */
  const store = {
    read(){
      try{ return JSON.parse(localStorage.getItem(KEY) || 'null'); }
      catch(e){ return null; }
    },
    write(v){
      try{ localStorage.setItem(KEY, JSON.stringify(v)); return true; }
      catch(e){ return false; }
    }
  };
  // לאיפוס בפיתוח:  window.__bfReset()
  window.__bfReset = () => { try{ localStorage.removeItem(KEY); }catch(e){} };

  const state = () => store.read() || { seen:false, email:null, models:[] };

  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const validMail = v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(String(v).trim());

  /* ---------- שליחה ---------- */
  async function send(payload){
    if(!ENDPOINT) throw new Error('no endpoint');
    const res = await fetch(ENDPOINT, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify(payload)
    });
    if(!res.ok) throw new Error('http ' + res.status);
    return true;
  }

  function payload(email, source, models){
    const now = new Date().toISOString();
    return {
      campaign: CAMPAIGN,
      email: String(email).trim(),
      consent: true,
      consentText: 'אני מסכים/ה לקבל מיילים על המבצע · מדיניות הפרטיות',
      consentVersion: 'v10',
      consentAt: now,
      source,                 // 'popup' | 'product page'
      models,                 // [{id,name,url}] — הרשימה המצטברת
      modelsText: models.map(m => m.name).join(', '),          // לשימוש ישיר במייל
      modelsLinks: models.map(m => m.name + ': ' + m.url).join('\n'),
      ts: now
    };
  }

  /* ---------- מלכודת מיקוד ---------- */
  function trap(root, onEsc){
    const sel = 'a[href],button:not([disabled]),input,select,textarea,[tabindex]:not([tabindex="-1"])';
    function key(e){
      if(e.key === 'Escape'){ e.preventDefault(); onEsc(); return; }
      if(e.key !== 'Tab') return;
      const f = [...root.querySelectorAll(sel)].filter(el => el.offsetParent !== null);
      if(!f.length) return;
      const first = f[0], last = f[f.length-1];
      if(e.shiftKey && document.activeElement === first){ e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && document.activeElement === last){ e.preventDefault(); first.focus(); }
    }
    root.addEventListener('keydown', key);
    return () => root.removeEventListener('keydown', key);
  }

  /* ================= הפופאפ ================= */
  function openPopup(){
    const prev = document.activeElement;
    const ov = document.createElement('div');
    ov.className = 'bf bf-overlay';
    ov.innerHTML = `
      <div class="bf-modal" role="dialog" aria-modal="true" aria-labelledby="bf-t" dir="rtl">
        <button type="button" class="bf-x" aria-label="סגירה">
          <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M1 1l14 14M15 1L1 15" stroke="currentColor" stroke-width="1.5" fill="none"/></svg>
        </button>
        <div data-step="1">
          <p class="bf-kicker" id="bf-t">${T.kicker}</p>
          <h2 class="bf-h">${T.h1}</h2>
          <div class="bf-perks"><span>${T.perk1}</span><span>${T.perk2}</span></div>
          <p class="bf-p">${T.body}</p>
          <form novalidate>
            <div class="bf-field">
              <label class="bf-sr" for="bf-mail" hidden>${T.ph}</label>
              <input class="bf-input" id="bf-mail" name="email" type="email"
                     inputmode="email" autocomplete="email" placeholder="${T.ph}"
                     aria-describedby="bf-err">
            </div>
            <p class="bf-err" id="bf-err" role="alert" hidden></p>
            <div class="bf-consent">
              <input type="checkbox" id="bf-ok">
              <label for="bf-ok">${T.consent}<a href="${PRIVACY}" target="_blank" rel="noopener">${T.privacy}</a></label>
            </div>
            <button type="submit" class="bf-btn">${T.submit}</button>
          </form>
        </div>
        <div data-step="2" hidden>
          <p class="bf-kicker">${T.kicker}</p>
          <h2 class="bf-h">${T.okH}</h2>
          <p class="bf-p">${T.okBody}</p>
          <hr class="bf-rule">
          <p class="bf-p">${T.okHint}</p>
          <button type="button" class="bf-btn" data-go>${T.okBtn}</button>
        </div>
      </div>`;

    document.body.appendChild(ov);
    document.documentElement.classList.add('bf-lock');
    requestAnimationFrame(() => ov.setAttribute('data-open',''));

    const modal = ov.querySelector('.bf-modal');
    const s1 = ov.querySelector('[data-step="1"]');
    const s2 = ov.querySelector('[data-step="2"]');
    const form = ov.querySelector('form');
    const mail = ov.querySelector('#bf-mail');
    const okbx = ov.querySelector('#bf-ok');
    const err  = ov.querySelector('#bf-err');
    const btn  = form.querySelector('.bf-btn');

    const untrap = trap(modal, close);
    setTimeout(() => mail.focus(), 60);

    function close(){
      const st = state(); st.seen = true; store.write(st);
      untrap();
      ov.removeAttribute('data-open');
      setTimeout(() => {
        ov.remove();
        document.documentElement.classList.remove('bf-lock');
        if(prev && prev.focus) prev.focus();
      }, 200);
    }

    function fail(msg, el){
      err.textContent = msg; err.hidden = false;
      if(el){ el.setAttribute('aria-invalid','true'); el.focus(); }
    }

    mail.addEventListener('input', () => {
      err.hidden = true; mail.removeAttribute('aria-invalid');
    });

    ov.querySelector('.bf-x').addEventListener('click', close);
    ov.addEventListener('mousedown', e => { if(e.target === ov) close(); });

    form.addEventListener('submit', async e => {
      e.preventDefault();
      err.hidden = true; mail.removeAttribute('aria-invalid');
      const v = mail.value.trim();
      if(!validMail(v)) return fail(M.badMail, mail);
      if(!okbx.checked) return fail(M.noConsent, okbx);

      btn.disabled = true; const label = btn.textContent; btn.textContent = M.sending;
      try{
        const st = state();
        await send(payload(v, 'popup', st.models || []));
        st.email = v; st.seen = true; store.write(st);
        s1.hidden = true; s2.hidden = false;
        s2.querySelector('.bf-h').setAttribute('tabindex','-1');
        s2.querySelector('.bf-h').focus();
      }catch(ex){
        btn.disabled = false; btn.textContent = label;
        fail(M.failed, mail);
      }
    });

    ov.querySelector('[data-go]').addEventListener('click', () => {
      const target = document.querySelector('#models, [data-models], .collection, .cards');
      close();
      setTimeout(() => {
        if(target) target.scrollIntoView({behavior:'smooth', block:'start'});
        else location.href = CATALOG;
      }, 230);
    });
  }

  /* ================= דף מוצר ================= */
  function productBlock(){
    const cta = document.querySelector('[data-add]');
    if(!cta) return;

    const id   = cta.getAttribute('data-add');
    const name = cta.getAttribute('data-name') || id;
    const url  = (document.querySelector('link[rel="canonical"]') || {}).href || location.href;

    const wrap = document.createElement('div');
    wrap.className = 'bf bf-remind';
    wrap.dir = 'rtl';
    wrap.innerHTML = `
      <button type="button" class="bf-btn" data-bf-remind>${T.remind}</button>
      <p class="bf-note" data-bf-note role="status" hidden></p>
      <div class="bf-inline" data-bf-inline hidden>
        <p class="bf-p">${T.inline(esc(name))}</p>
        <form novalidate>
          <div class="bf-field">
            <label for="bf-pmail" hidden>${T.ph}</label>
            <input class="bf-input" id="bf-pmail" type="email" inputmode="email"
                   autocomplete="email" placeholder="${T.ph}" aria-describedby="bf-perr">
          </div>
          <p class="bf-err" id="bf-perr" role="alert" hidden></p>
          <div class="bf-consent">
            <input type="checkbox" id="bf-pok">
            <label for="bf-pok">${T.consent}<a href="${PRIVACY}" target="_blank" rel="noopener">${T.privacy}</a></label>
          </div>
          <button type="submit" class="bf-btn">${T.remindBtn}</button>
        </form>
      </div>`;

    cta.parentElement.insertBefore(wrap, cta.nextSibling);

    const bRemind = wrap.querySelector('[data-bf-remind]');
    const note    = wrap.querySelector('[data-bf-note]');
    const inline  = wrap.querySelector('[data-bf-inline]');
    const iform   = inline.querySelector('form');
    const imail   = inline.querySelector('#bf-pmail');
    const iok     = inline.querySelector('#bf-pok');
    const ierr    = inline.querySelector('#bf-perr');

    const model = { id, name, url };

    function already(){
      return (state().models || []).some(m => m.id === id);
    }
    function showSaved(){
      note.innerHTML = T.saved(esc(name));
      note.hidden = false;
      bRemind.disabled = true;
    }
    if(already()) showSaved();

    function addLocal(){
      const st = state();
      st.models = st.models || [];
      if(!st.models.some(m => m.id === id)) st.models.push(model);
      store.write(st);
      return st;
    }

    bRemind.addEventListener('click', async () => {
      if(already()){ showSaved(); return; }
      const st = state();
      if(!st.email){ inline.hidden = false; imail.focus(); return; }

      bRemind.disabled = true;
      const label = bRemind.textContent; bRemind.textContent = M.sending;
      try{
        const models = (st.models || []).concat([model]);
        await send(payload(st.email, 'product page', models));
        addLocal();
        bRemind.textContent = label;
        showSaved();
      }catch(ex){
        bRemind.disabled = false; bRemind.textContent = label;
        note.textContent = M.failed; note.hidden = false;
      }
    });

    imail.addEventListener('input', () => {
      ierr.hidden = true; imail.removeAttribute('aria-invalid');
    });

    iform.addEventListener('submit', async e => {
      e.preventDefault();
      ierr.hidden = true; imail.removeAttribute('aria-invalid');
      const v = imail.value.trim();
      if(!validMail(v)){ ierr.textContent = M.badMail; ierr.hidden=false; imail.setAttribute('aria-invalid','true'); imail.focus(); return; }
      if(!iok.checked){ ierr.textContent = M.noConsent; ierr.hidden=false; iok.focus(); return; }

      const sb = iform.querySelector('.bf-btn');
      sb.disabled = true; const label = sb.textContent; sb.textContent = M.sending;
      try{
        const st = state();
        const models = (st.models || []).concat([model]);
        await send(payload(v, 'product page', models));
        st.email = v; store.write(st);
        addLocal();
        inline.hidden = true;
        showSaved();
      }catch(ex){
        sb.disabled = false; sb.textContent = label;
        ierr.textContent = M.failed; ierr.hidden = false;
      }
    });
  }

  /* ================= הפעלה ================= */
  function init(){
    // ללא כתובת webhook הקמפיין רדום לגמרי — שום דבר לא מוצג ושום דבר לא נשלח.
    if(!ENDPOINT) return;
    productBlock();
    const st = state();
    if(!st.seen && !st.email) setTimeout(openPopup, 1200);
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
