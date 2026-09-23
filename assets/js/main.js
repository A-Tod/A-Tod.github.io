/* a-tod — site behaviour. Vanilla, no dependencies. */
(() => {
  'use strict';
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const ILS = n => '₪' + n.toLocaleString('he-IL', { minimumFractionDigits: 2 });

  /* ---------- mobile nav ---------- */
  const burger = $('.burger'), nav = $('.nav');
  if (burger && nav) {
    burger.addEventListener('click', () => {
      const open = burger.getAttribute('aria-expanded') === 'true';
      burger.setAttribute('aria-expanded', String(!open));
      nav.dataset.open = String(!open);
      document.body.style.overflow = !open ? 'hidden' : '';
    });
  }

  /* ---------- shop submenu ---------- */
  $$('.nav__group').forEach(group => {
    const btn = $('.nav__toggle', group);
    const set = v => { group.dataset.open = String(v); btn.setAttribute('aria-expanded', String(v)); };
    btn.addEventListener('click', e => { e.preventDefault(); set(group.dataset.open !== 'true'); });
    group.addEventListener('mouseenter', () => { if (matchMedia('(min-width:861px)').matches) set(true); });
    group.addEventListener('mouseleave', () => { if (matchMedia('(min-width:861px)').matches) set(false); });
    document.addEventListener('click', e => { if (!group.contains(e.target)) set(false); });
  });
  document.addEventListener('keydown', e => {
    if (e.key !== 'Escape') return;
    $$('.nav__group').forEach(g => { g.dataset.open = 'false'; $('.nav__toggle', g)?.setAttribute('aria-expanded', 'false'); });
    closeCart(); closeLightbox();
  });

  /* ---------- accordions ---------- */
  $$('.acc__btn').forEach(btn => btn.addEventListener('click', () => {
    btn.setAttribute('aria-expanded', String(btn.getAttribute('aria-expanded') !== 'true'));
  }));

  /* ---------- product gallery ---------- */
  const main = $('.pdp__main img');
  if (main) $$('.pdp__thumb').forEach(t => t.addEventListener('click', () => {
    $$('.pdp__thumb').forEach(o => o.setAttribute('aria-current', 'false'));
    t.setAttribute('aria-current', 'true');
    main.src = t.dataset.full || $('img', t).src;
    main.alt = $('img', t).alt;
  }));

  /* ---------- quantity ---------- */
  $$('.qty__box').forEach(box => {
    const val = $('.qty__val', box);
    $$('.qty__btn', box).forEach(b => b.addEventListener('click', () => {
      const n = Math.max(1, Math.min(99, (+val.value || 1) + (+b.dataset.step)));
      val.value = n;
    }));
    val.addEventListener('change', () => { val.value = Math.max(1, Math.min(99, +val.value || 1)); });
  });

  /* ---------- toast ---------- */
  let toastT;
  const toast = msg => {
    let el = $('.toast');
    if (!el) { el = document.createElement('div'); el.className = 'toast'; el.setAttribute('role','status'); document.body.appendChild(el); }
    el.textContent = msg;
    requestAnimationFrame(() => { el.dataset.open = 'true'; });
    clearTimeout(toastT);
    toastT = setTimeout(() => { el.dataset.open = 'false'; }, 2600);
  };

  /* ---------- cart (localStorage) ---------- */
  const KEY = 'atod_cart_v1';
  const read = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; } };
  const write = c => { try { localStorage.setItem(KEY, JSON.stringify(c)); } catch {} ; paint(); };

  function paint() {
    const cart = read();
    const count = cart.reduce((s, l) => s + l.qty, 0);
    $$('.cart__count').forEach(b => { b.textContent = count; b.dataset.empty = String(count === 0); });

    const body = $('.drawer__body'), foot = $('.drawer__foot');
    if (!body) return;
    if (!cart.length) {
      body.innerHTML = '<p class="drawer__empty">העגלה ריקה</p>';
      if (foot) foot.hidden = true;
      return;
    }
    if (foot) foot.hidden = false;
    body.innerHTML = cart.map(l => `
      <div class="line">
        <img src="${l.img}" alt="" loading="lazy">
        <div>
          <div class="line__n">${l.name}</div>
          <div class="line__p">${l.qty} × ${ILS(l.price)}</div>
          <button class="line__x" data-remove="${l.sku}">הסרה</button>
        </div>
      </div>`).join('');

    const sub = cart.reduce((s, l) => s + l.price * l.qty, 0);
    const items = cart.reduce((s, l) => s + l.qty, 0);
    const ship = items >= 2 ? 0 : 50;
    $('#sum-sub').textContent = ILS(sub);
    $('#sum-ship').textContent = ship ? ILS(ship) : 'חינם';
    $('#sum-total').textContent = ILS(sub + ship);
    $('#sum-hint').textContent = items >= 2 ? 'משלוח חינם — שני פריטים ומעלה' : 'הוספת פריט נוסף מזכה במשלוח חינם';
  }

  document.addEventListener('click', e => {
    const rm = e.target.closest('[data-remove]');
    if (rm) { write(read().filter(l => l.sku !== rm.dataset.remove)); return; }

    const add = e.target.closest('[data-add]');
    if (!add) return;
    const d = add.dataset;
    const qty = +($('.qty__val')?.value || 1);
    const cart = read();
    const hit = cart.find(l => l.sku === d.add);
    if (hit) hit.qty = Math.min(99, hit.qty + qty);
    else cart.push({ sku: d.add, name: d.name, price: +d.price, img: d.img, qty });
    write(cart);
    toast(`${d.name} נוסף להזמנה`);
    openCart();
  });

  const drawer = $('.drawer'), scrim = $('.scrim');
  function openCart() { if (drawer) { drawer.dataset.open = 'true'; scrim.dataset.open = 'true'; } }
  function closeCart() { if (drawer) { drawer.dataset.open = 'false'; scrim.dataset.open = 'false'; } }
  $$('[data-cart-open]').forEach(b => b.addEventListener('click', openCart));
  $$('[data-cart-close]').forEach(b => b.addEventListener('click', closeCart));
  scrim?.addEventListener('click', closeCart);
  paint();

  /* ---------- lightbox ---------- */
  const lb = $('.lb');
  let shots = [], idx = 0;
  function openLightbox(i) {
    if (!lb) return;
    idx = i; $('img', lb).src = shots[idx].full; $('img', lb).alt = shots[idx].alt;
    lb.dataset.open = 'true'; document.body.style.overflow = 'hidden';
  }
  function closeLightbox() { if (lb) { lb.dataset.open = 'false'; document.body.style.overflow = ''; } }
  function step(d) { idx = (idx + d + shots.length) % shots.length; $('img', lb).src = shots[idx].full; }
  if (lb) {
    shots = $$('.masonry img').map(i => ({ full: i.dataset.full || i.src, alt: i.alt }));
    $$('.masonry figure').forEach((f, i) => {
      f.tabIndex = 0; f.setAttribute('role', 'button');
      // שם נגיש מפורש לכל תמונה, כדי שקורא מסך יבחין ביניהן (WCAG 4.1.2).
      f.setAttribute('aria-label', `הגדלת תמונה ${i + 1} מתוך ${shots.length}`);
      f.addEventListener('click', () => openLightbox(i));
      f.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openLightbox(i); } });
    });
    $('.lb__x').addEventListener('click', closeLightbox);
    $('.lb__prev').addEventListener('click', () => step(-1));
    $('.lb__next').addEventListener('click', () => step(1));
    lb.addEventListener('click', e => { if (e.target === lb) closeLightbox(); });
    document.addEventListener('keydown', e => {
      if (lb.dataset.open !== 'true') return;
      if (e.key === 'ArrowRight') step(-1);
      if (e.key === 'ArrowLeft') step(1);
    });
  }

  /* ---------- forms ---------- */
  const setErr = (field, msg) => {
    field.dataset.error = msg ? 'true' : 'false';
    const e = $('.field__err', field); if (e) e.textContent = msg || '';
  };
  const emailOk = v => /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);

  /* ---------- הטפסים ----------
     FORM = כתובת ה-endpoint שקולט את הפניות (Formspree או שווה ערך).
     כל עוד הוא ריק, הטפסים נופלים חזרה לפתיחת הודעת מייל אצל הגולש —
     מה שאומר שאף כתובת לא נאספת בפועל. עם endpoint, הפנייה נשלחת
     ברקע ונשמרת, גם אם לגולש אין תוכנת מייל מוגדרת. */
  const FORM = '';

  async function post(fields, subject) {
    if (!FORM) return false;
    try {
      const fd = new FormData();
      Object.entries(fields).forEach(([k, v]) => v && fd.append(k, v));
      fd.append('_subject', subject);
      const r = await fetch(FORM, { method: 'POST', body: fd, headers: { Accept: 'application/json' } });
      return r.ok;
    } catch { return false; }
  }

  function mailFallback(to, subject, body) {
    location.href = `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  }

  $('#contact-form')?.addEventListener('submit', async e => {
    e.preventDefault();
    let bad = false;
    const name = $('#f-name'), mail = $('#f-mail'), tel = $('#f-tel');
    setErr(name.closest('.field'), name.value.trim() ? '' : (bad = true, 'נא למלא שם'));
    setErr(mail.closest('.field'), emailOk(mail.value.trim()) ? '' : (bad = true, 'נא למלא כתובת מייל תקינה'));
    if (tel.value.trim() && !/^[\d\-+() ]{7,}$/.test(tel.value.trim()))
      setErr(tel.closest('.field'), (bad = true, 'מספר טלפון לא תקין'));
    else setErr(tel.closest('.field'), '');
    if (bad) { $('[data-error="true"] input')?.focus(); return; }

    const form = e.currentTarget;
    const btn = form.querySelector('.btn-send');
    const msg = $('#f-msg')?.value.trim() || '';
    const sent = document.querySelector('.form-sent');
    if (btn) { btn.disabled = true; btn.textContent = 'שולח…'; }

    const ok = await post({ שם: name.value.trim(), מייל: mail.value.trim(),
                            טלפון: tel.value.trim(), הודעה: msg,
                            email: mail.value.trim() }, 'פנייה מהאתר');
    if (btn) { btn.disabled = false; btn.textContent = 'שלח'; }

    if (ok) {
      form.reset();
      if (sent) { sent.textContent = 'הפנייה נשלחה. נחזור אליכם תוך יום עסקים אחד.'; sent.hidden = false; }
      return;
    }
    const body = [`שם: ${name.value.trim()}`, `מייל: ${mail.value.trim()}`,
                  tel.value.trim() ? `טלפון: ${tel.value.trim()}` : null,
                  '', msg].filter(v => v !== null).join('\n');
    mailFallback(form.dataset.mailto, 'פנייה מהאתר', body);
    if (sent) sent.hidden = false;
  });

  $('#news-form')?.addEventListener('submit', async e => {
    e.preventDefault();
    const i = $('#news-mail'), m = $('.news__msg'), form = e.currentTarget;
    const v = i.value.trim();
    if (!emailOk(v)) { m.textContent = 'נא להזין כתובת מייל תקינה'; m.style.color = '#7a2718'; return; }

    m.style.color = ''; m.textContent = 'רושם…';
    const ok = await post({ email: v, סוג: 'הרשמה לרשימת התפוצה' }, 'הרשמה לרשימת התפוצה · 10%');
    if (ok) {
      form.reset();
      m.textContent = 'נרשמתם. קוד ההנחה יישלח אליכם למייל.';
      return;
    }
    mailFallback(form.dataset.mailto, 'הרשמה לרשימת התפוצה',
      'אשמח להצטרף לרשימת התפוצה ולקבל את קוד ההנחה.\nכתובת המייל שלי: ' + v);
    m.textContent = 'פתחנו לכם הודעה מוכנה. שלחו אותה ונחזור אליכם עם הקוד.';
  });

  /* ---------- reveal on scroll ---------- */
  if (!matchMedia('(prefers-reduced-motion:reduce)').matches && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(en => {
      if (!en.isIntersecting) return;
      en.target.style.opacity = '1'; en.target.style.transform = 'none';
      io.unobserve(en.target);
    }), { rootMargin: '0px 0px -8% 0px' });
    $$('.feature, .story__media, .story__body, .card').forEach(el => {
      el.style.cssText += 'opacity:0;transform:translateY(18px);transition:opacity .7s cubic-bezier(.22,.61,.36,1),transform .7s cubic-bezier(.22,.61,.36,1)';
      io.observe(el);
    });
  }
})();

/* hero slideshow — crossfade */
(() => {
  const box = document.querySelector('[data-slideshow]');
  if (!box) return;
  const slides = [...box.querySelectorAll('img')];
  if (slides.length < 2) return;
  if (matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  let i = 0;
  setInterval(() => {
    slides[i].removeAttribute('data-active');
    i = (i + 1) % slides.length;
    slides[i].setAttribute('data-active', 'true');
  }, +box.dataset.interval || 6000);
})();

/* עמוד מוצר: שכבת מידות + מרחיב תיאור + סכום בכפתור */
(() => {
  const stage = document.querySelector('[data-dimbtn]');
  if (stage) {
    const dims = document.querySelector('[data-dims]');
    const shot = document.querySelector('[data-stage]');
    // קווי המידות נמדדו על צילום הסטודיו. אם הבמה מציגה תמונה אחרת,
    // הלחיצה מחזירה את צילום הסטודיו ואז מציירת עליו את הקווים.
    const dimSrc  = shot && shot.dataset.dimSrc;
    const heroSrc = shot && shot.dataset.heroSrc;
    if (dimSrc) { const pre = new Image(); pre.src = dimSrc; }

    stage.addEventListener('click', () => {
      const on = stage.getAttribute('aria-pressed') === 'true';
      stage.setAttribute('aria-pressed', String(!on));
      if (!on) {
        if (dimSrc) { shot.removeAttribute('width'); shot.removeAttribute('height'); shot.src = dimSrc; }
        dims.setAttribute('data-on', '');
      } else {
        dims.removeAttribute('data-on');
        if (heroSrc) shot.src = heroSrc;
      }
    });
  }

  const moreBtn = document.querySelector('[data-more]');
  if (moreBtn) {
    const rest = document.querySelector('[data-rest]');
    moreBtn.addEventListener('click', () => {
      const open = moreBtn.getAttribute('aria-expanded') === 'true';
      moreBtn.setAttribute('aria-expanded', String(!open));
      rest.hidden = open;
      moreBtn.firstElementChild.textContent = open ? 'עוד +' : 'פחות −';
    });
  }

  const cta = document.querySelector('[data-add]');
  if (cta) {
    const val = document.querySelector('.qty__val');
    const totalEl = cta.querySelector('[data-cta-total]');   // אופציונלי — הוסר מהעיצוב
    const labelEl = cta.querySelector('[data-cta-label]');
    const unit = +cta.dataset.price;
    const paint = () => {
      if (!totalEl) return;
      totalEl.textContent = '₪' + (unit * Math.max(1, +val.value || 1)).toLocaleString('en-US');
    };
    // הצעד עצמו מטופל בבלוק העגלה למעלה. כאן רק רענון התווית והסכום.
    document.querySelectorAll('.qty__btn').forEach(b =>
      b.addEventListener('click', () => {
        if (labelEl) labelEl.textContent = 'הוספה להזמנה';
        setTimeout(paint, 0);
      }));
    val.addEventListener('change', paint);
    cta.addEventListener('click', () => { if (labelEl) labelEl.textContent = 'נוסף להזמנה'; });
    paint();
  }

  /* ---------- model-viewer ---------- */
  /* loading="lazy" המובנה של model-viewer לא נדלק בחלק מהדפדפנים, והמודל
     פשוט לא נטען לעולם. מאומת בייצור. מחליפים ל-eager כשהבלוק מתקרב למסך —
     אותה התנהגות עצלה בדיוק, רק אמינה. */
  (() => {
    const mv = document.querySelector('model-viewer[loading="lazy"]');
    if (!mv) return;
    const go = () => mv.setAttribute('loading', 'eager');
    if (!('IntersectionObserver' in window)) return go();
    const io = new IntersectionObserver(es => {
      if (es.some(e => e.isIntersecting)) { go(); io.disconnect(); }
    }, { rootMargin: '800px 0px' });
    io.observe(mv);
  })();
})();

/* ---------- כלי נגישות ----------
   מצב המשתמש נשמר ב-localStorage של הדפדפן שלו בלבד.
   אין כאן שום קריאת רשת ושום מעקב. */
(function () {
  const root = document.querySelector('[data-a11y]');
  if (!root) return;

  const fab   = root.querySelector('.a11y__fab');
  const panel = root.querySelector('.a11y__panel');
  const close = root.querySelector('.a11y__x');
  const KEY   = 'atod_a11y_v1';
  const FLAGS = ['contrast', 'links', 'motion'];

  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } };
  const save = s => { try { localStorage.setItem(KEY, JSON.stringify(s)); } catch {} };

  let state = load();

  function apply() {
    const b = document.body;
    const z = +state.zoom || 1;
    if (z !== 1) { b.dataset.a11yZoom = String(z); b.style.setProperty('--a11y-zoom', z); }
    else { delete b.dataset.a11yZoom; b.style.removeProperty('--a11y-zoom'); }

    FLAGS.forEach(f => {
      const on = !!state[f];
      const attr = 'a11y' + f[0].toUpperCase() + f.slice(1);
      if (on) b.dataset[attr] = 'true'; else delete b.dataset[attr];
      const btn = root.querySelector(`[data-flag="${f}"]`);
      if (btn) btn.setAttribute('aria-pressed', String(on));
    });

    root.querySelectorAll('[data-zoom]').forEach(btn =>
      btn.setAttribute('aria-pressed', String(+btn.dataset.zoom === z)));

    // עצירת אנימציות עוצרת גם את מצגת הגיבור ואת סיבוב מודל התלת־מימד
    document.querySelectorAll('model-viewer[auto-rotate]').forEach(m => {
      if (state.motion) m.removeAttribute('auto-rotate'); });
    save(state);
  }

  function open()  { panel.hidden = false; fab.setAttribute('aria-expanded', 'true');  close.focus(); }
  function shut()  { panel.hidden = true;  fab.setAttribute('aria-expanded', 'false'); fab.focus(); }

  fab.addEventListener('click', () => (panel.hidden ? open() : shut()));
  close.addEventListener('click', shut);

  root.querySelectorAll('[data-zoom]').forEach(btn =>
    btn.addEventListener('click', () => { state.zoom = +btn.dataset.zoom; apply(); }));

  root.querySelectorAll('[data-flag]').forEach(btn =>
    btn.addEventListener('click', () => { const f = btn.dataset.flag; state[f] = !state[f]; apply(); }));

  root.querySelector('.a11y__reset').addEventListener('click', () => { state = {}; apply(); });

  document.addEventListener('keydown', e => { if (e.key === 'Escape' && !panel.hidden) shut(); });
  document.addEventListener('click', e => {
    if (!panel.hidden && !root.contains(e.target)) shut();
  });

  apply();
})();

/* ---------- מדידה + הסכמה לעוגיות ----------
   שני המזהים יושבים כאן, בקובץ אחד. להפעלה או לכיבוי — מעדכנים רק אותו.
   ריק = כלום לא נטען, ואין באנר.
   הסקריפטים נטענים אך ורק אחרי הסכמה מפורשת. */
(function () {
  const GA      = 'G-6R01MNSJWQ'; // Google Analytics 4  (Measurement ID · נכס studioatod, חשבון A-tod)
  const CLARITY = 'REPLACE';       // Microsoft Clarity   (Project ID)

  const has = v => v && !/REPLACE/.test(v);
  const ON0 = has(GA) || has(CLARITY);

  const KEY = 'atod_consent_v1';
  const get = () => { try { return localStorage.getItem(KEY); } catch { return null; } };
  const set = v => { try { localStorage.setItem(KEY, v); } catch {} };

  /* ביקורים של רועי עצמו לא אמורים להיספר.
     כניסה חד-פעמית ל-studioatod.com/?notrack=1 מסמנת את הדפדפן לצמיתות.
     ביטול: ?notrack=0 */
  const NT = 'atod_notrack';
  try {
    const q = new URLSearchParams(location.search).get('notrack');
    if (q === '1') localStorage.setItem(NT, '1');
    if (q === '0') localStorage.removeItem(NT);
  } catch {}
  let me = false;
  try { me = localStorage.getItem(NT) === '1'; } catch {}

  const ON = ON0 && !me;

  let loaded = false;
  const queue = [];

  /* ---- שכבת האירועים ---- */
  window.atodTrack = function (name, params) {
    if (!ON) return;
    if (!loaded) { queue.push([name, params]); return; }
    try { window.gtag && window.gtag('event', name, params || {}); } catch {}
    try { window.clarity && window.clarity('event', name); } catch {}
  };

  function loadScripts() {
    if (loaded || !ON) return;
    loaded = true;

    if (has(GA)) {
      const s = document.createElement('script');
      s.async = true;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA;
      document.head.appendChild(s);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      gtag('js', new Date());
      gtag('config', GA, { anonymize_ip: true });
    }

    if (has(CLARITY)) {
      (function (c, l, a, r, i, t, y) {
        c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
        t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
        y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
      })(window, document, 'clarity', 'script', CLARITY);
    }

    while (queue.length) { const [n, p] = queue.shift(); window.atodTrack(n, p); }
  }

  /* ---- הבאנר ---- */
  let banner = null;
  function buildBanner() {
    banner = document.createElement('div');
    banner.className = 'consent';
    banner.setAttribute('role', 'dialog');
    banner.setAttribute('aria-label', 'הסכמה לשימוש בעוגיות');
    banner.innerHTML =
      '<p class="consent__t">אנחנו רוצים להבין איך משתמשים באתר כדי לשפר אותו. ' +
      'לשם כך נשתמש בעוגיות של ' +
      (has(GA) && has(CLARITY) ? 'Google Analytics ושל Microsoft Clarity, שמקליט את המסך בזמן הגלישה'
        : has(CLARITY) ? 'Microsoft Clarity, שמקליט את המסך בזמן הגלישה'
        : 'Google Analytics') + '. ' +
      'בלי הסכמתכם לא ייטען דבר. פרטים ב<a href="privacy.html">מדיניות הפרטיות</a>.</p>' +
      '<div class="consent__btns">' +
      '<button type="button" class="consent__ok">אני מאשר</button>' +
      '<button type="button" class="consent__no">רק ההכרחי</button>' +
      '</div>';
    document.body.appendChild(banner);
    document.body.dataset.consentOpen = 'true';
    document.body.style.setProperty('--consent-h', banner.offsetHeight + 'px');

    banner.querySelector('.consent__ok').addEventListener('click', () => decide('granted'));
    banner.querySelector('.consent__no').addEventListener('click', () => decide('denied'));
  }

  function decide(v) {
    set(v);
    if (banner) { banner.remove(); banner = null; }
    delete document.body.dataset.consentOpen;
    if (v === 'granted') loadScripts();
  }

  /* כפתור בפוטר לשינוי ההחלטה בכל רגע */
  document.querySelectorAll('[data-consent-reopen]').forEach(b => {
    if (!ON) return;
    b.hidden = false;
    b.addEventListener('click', () => { if (!banner) buildBanner(); });
  });

  if (ON) {
    const c = get();
    if (c === 'granted') loadScripts();
    else if (c !== 'denied') buildBanner();
  }

  /* ---- מה נמדד ---- */
  const T = (n, p) => window.atodTrack(n, p);

  // צפייה במוצר
  const cta = document.querySelector('[data-add]');
  if (cta) T('view_item', {
    item_id: cta.dataset.add, item_name: cta.dataset.name,
    value: +cta.dataset.price, currency: 'ILS',
  });

  document.addEventListener('click', e => {
    const add = e.target.closest('[data-add]');
    if (add) {
      T('add_to_cart', {
        item_id: add.dataset.add, item_name: add.dataset.name,
        value: +add.dataset.price, currency: 'ILS',
      });
      return;
    }
    const rm = e.target.closest('[data-remove]');
    if (rm) { T('remove_from_cart', { item_id: rm.dataset.remove }); return; }

    // "להשלמת ההזמנה" — הצעד שאנחנו הכי רוצים למדוד
    const co = e.target.closest('.drawer__foot .btn-primary');
    if (co) {
      let sum = 0;
      try { sum = (JSON.parse(localStorage.getItem('atod_cart_v1')) || [])
        .reduce((s, l) => s + l.price * l.qty, 0); } catch {}
      T('begin_checkout', { value: sum, currency: 'ILS' });
      return;
    }
    if (e.target.closest('.m3d__ar'))        T('view_in_ar');
    if (e.target.closest('.masonry figure')) T('gallery_open');
  });

  // פתיחת העגלה
  const dr = document.querySelector('.drawer');
  if (dr) new MutationObserver(() => {
    if (dr.dataset.open === 'true') T('view_cart');
  }).observe(dr, { attributes: true, attributeFilter: ['data-open'] });

  // שליחת טופס צור קשר
  document.querySelector('#contact-form, .form')?.addEventListener('submit', () => T('contact_submit'));
  document.querySelector('#news-form')?.addEventListener('submit', () => T('newsletter_signup'));
})();

/* ---------- צ'ק-אאוט וסליקה (Grow דרך Make) ----------
   בלוק עצמאי: מפנה את כפתור העגלה לעמוד הצ'ק-אאוט, מרכיב שם את סיכום
   ההזמנה ושולח אותה ל-Make, שמייצר קישור תשלום ב-Grow ומפנה אליו.
   הסכום מחושב כאן; ב-Make יושבת רצפת מחיר שחוסמת סכום שהתעסקו בו. */
(() => {
  'use strict';
  const $  = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const ILS = n => '₪' + n.toLocaleString('he-IL', { minimumFractionDigits: 2 });
  const KEY = 'atod_cart_v1';
  const readCart = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return []; } };

  const ENDPOINT = 'https://hook.eu2.make.com/jgrgamto3vgdm7pbkxgs3jbihuwk0czd';

  /* כפתור ההזמנה בעגלה, בכל עמודי האתר */
  const foot = $('.drawer__foot');
  if (foot) {
    const btn = $('.btn-primary', foot);
    if (btn) btn.href = 'checkout.html';
    const note = $('.form-note', foot);
    if (note) note.textContent = 'תשלום מאובטח — אשראי, bit ו-Apple Pay.';
  }

  /* חזרה מתשלום מוצלח — מרוקנים את העגלה */
  if (/thank-you\.html$/.test(location.pathname)) {
    try { localStorage.removeItem(KEY); } catch {}
    $$('.cart__count').forEach(b => { b.textContent = '0'; b.dataset.empty = 'true'; });
  }

  const form = $('#checkout-form');
  if (!form) return;

  const cart = readCart();
  if (!cart.length) { location.replace('collection.html'); return; }

  form.action = ENDPOINT;

  const sub   = cart.reduce((s, l) => s + l.price * l.qty, 0);
  const units = cart.reduce((s, l) => s + l.qty, 0);
  const ship  = units >= 2 ? 0 : 50;

  $('#co-lines').innerHTML = cart.map(l =>
    '<div class="line"><img src="' + l.img + '" alt="" loading="lazy"><div>' +
    '<div class="line__n">' + l.name + '</div>' +
    '<div class="line__p">' + l.qty + ' × ' + ILS(l.price) + '</div>' +
    '</div></div>').join('');
  $('#co-sub').textContent   = ILS(sub);
  $('#co-ship').textContent  = ship ? ILS(ship) : 'חינם';
  $('#co-total').textContent = ILS(sub + ship);
  $('#co-hint').textContent  = units >= 2
    ? 'משלוח חינם — שני פריטים ומעלה'
    : 'הוספת פריט נוסף מזכה במשלוח חינם';

  /* Grow מסנן תווים מיוחדים מתיאור המוצר */
  $('#c-items').value  = cart.map(l => l.name + ' ' + l.qty + ' יח').join(', ')
                         + (ship ? ', משלוח 50' : '');
  $('#c-units').value  = units;
  $('#c-amount').value = (sub + ship).toFixed(2);

  if (new URLSearchParams(location.search).get('cancelled') === '1') {
    const n = $('#pay-cancelled'); if (n) n.hidden = false;
  }

  const err = $('#c-error');
  const mark = (field, bad) => { const f = field.closest('.field'); if (f) f.dataset.error = String(bad); return !bad; };
  const isPhone = v => /^0(5\d|[2-4]|7\d|8|9)\d{7}$/.test(v.replace(/[-\s]/g, ''));
  const isMail  = v => /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v);

  form.addEventListener('submit', e => {
    const f = form.elements;
    let ok = true;
    ok = mark(f.fullName, f.fullName.value.trim().split(/\s+/).length < 2) && ok;
    ok = mark(f.phone,   !isPhone(f.phone.value))                          && ok;
    ok = mark(f.email,   !isMail(f.email.value.trim()))                    && ok;
    ok = mark(f.address, !f.address.value.trim())                          && ok;
    ok = mark(f.city,    !f.city.value.trim())                             && ok;
    if (!ok) {
      e.preventDefault();
      if (err) { err.hidden = false; err.textContent = 'יש להשלים את הפרטים המסומנים.'; }
      form.querySelector('.field[data-error="true"] input')?.focus();
      return;
    }
    f.phone.value = f.phone.value.replace(/[-\s]/g, '');
    if (err) err.hidden = true;
    const btn = $('#c-submit');
    if (btn) { btn.disabled = true; btn.textContent = 'מעבירים לתשלום…'; }
  });
})();

/* ---------- זמינות מלאי ----------
   המצב של כל מוצר נקרא מ-/stock.json — קובץ אחד, 12 שורות.
   רועי עורך אותו ישירות ב-GitHub; האתר מתעדכן בלי בנייה מחדש.
   מוצר שלא מופיע בקובץ, או קובץ שלא נטען — מוצג כ"נוצק לפי הזמנה",
   שזו ברירת המחדל הנכונה לעבודת יד ולא מבטיחה דבר שאינו נכון. */
(() => {
  const DEFAULT = 'made';
  const STATE = {
    in:   'במלאי · מוכן למשלוח',
    made: 'נוצק לפי הזמנה · עד 10 ימי עסקים',
    out:  'אזל זמנית',
  };

  const css = `
.stock{display:flex;align-items:center;gap:8px;margin-top:12px;
  font-family:var(--f-he);font-weight:200;font-size:14px;line-height:1.4}
.stock::before{content:'';width:7px;height:7px;border-radius:50%;background:currentColor;flex:none}
.stock[data-k="in"]{color:#3F5D34}
.stock[data-k="made"]{color:rgba(46,37,31,.68)}
.stock[data-k="out"]{color:#7a2718}
.stock__ask{display:inline-block;margin-top:10px;font-family:var(--f-he);font-weight:200;
  font-size:14px;color:rgba(46,37,31,.68);border-bottom:1px solid rgba(46,37,31,.45);padding-bottom:2px}
.pdp__cta[disabled]{opacity:.4;cursor:not-allowed}
.card__out{position:absolute;top:10px;inset-inline-start:10px;z-index:2;
  background:rgba(255,255,255,.94);color:#7a2718;
  font-family:var(--f-he);font-weight:400;font-size:12px;letter-spacing:.05em;padding:5px 11px}
`;
  const s = document.createElement('style');
  s.textContent = css;
  document.head.appendChild(s);

  const slugOf = href => {
    const m = String(href || '').match(/product-([a-z0-9]+)\.html/i);
    return m ? m[1].toLowerCase() : null;
  };

  function paint(stock) {
    const key = sl => {
      const v = String(stock[sl] || '').toLowerCase().trim();
      return STATE[v] ? v : DEFAULT;
    };

    /* --- עמוד מוצר --- */
    const cta = document.querySelector('.pdp__cta[data-add]');
    const price = document.querySelector('.pdp__price');
    if (cta && price) {
      const sl = cta.dataset.add;
      const k = key(sl);

      const b = document.createElement('div');
      b.className = 'stock';
      b.dataset.k = k;
      b.setAttribute('role', 'status');
      b.textContent = STATE[k];
      price.insertAdjacentElement('afterend', b);

      if (k === 'out') {
        cta.disabled = true;
        cta.setAttribute('aria-disabled', 'true');
        const lab = cta.querySelector('[data-cta-label]') || cta;
        lab.textContent = 'אזל זמנית';

        const ask = document.createElement('a');
        ask.className = 'stock__ask';
        ask.href = 'contact.html';
        ask.textContent = 'רוצים שנעדכן כשיחזור? דברו איתנו';
        (cta.closest('.pdp__buy') || cta.parentElement).insertAdjacentElement('afterend', ask);
      }
    }

    /* --- כרטיסי מוצר בקטגוריות ובדף כל הדגמים --- */
    document.querySelectorAll('a.card[href]').forEach(card => {
      const sl = slugOf(card.getAttribute('href'));
      if (!sl || key(sl) !== 'out') return;
      const media = card.querySelector('.card__media');
      if (!media || media.querySelector('.card__out')) return;
      const tag = document.createElement('span');
      tag.className = 'card__out';
      tag.textContent = 'אזל זמנית';
      media.appendChild(tag);
    });
  }

  fetch('stock.json?t=' + Date.now(), { cache: 'no-store' })
    .then(r => (r.ok ? r.json() : {}))
    .catch(() => ({}))
    .then(data => paint(data && typeof data === 'object' ? data : {}));
})();
