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

  $('#contact-form')?.addEventListener('submit', e => {
    let bad = false;
    const name = $('#f-name'), mail = $('#f-mail'), tel = $('#f-tel');
    setErr(name.closest('.field'), name.value.trim() ? '' : (bad = true, 'נא למלא שם'));
    setErr(mail.closest('.field'), emailOk(mail.value.trim()) ? '' : (bad = true, 'נא למלא כתובת מייל תקינה'));
    if (tel.value.trim() && !/^[\d\-+() ]{7,}$/.test(tel.value.trim()))
      setErr(tel.closest('.field'), (bad = true, 'מספר טלפון לא תקין'));
    else setErr(tel.closest('.field'), '');
    e.preventDefault();
    if (bad) { $('[data-error="true"] input')?.focus(); return; }
    // אין שרת. פותחים הודעה מוכנה בתוכנת המייל של המשתמש.
    const to = e.currentTarget.dataset.mailto;
    const msg = $('#f-msg')?.value.trim() || '';
    const body = [`שם: ${name.value.trim()}`, `מייל: ${mail.value.trim()}`,
                  tel.value.trim() ? `טלפון: ${tel.value.trim()}` : null,
                  '', msg].filter(v => v !== null).join('\n');
    location.href = `mailto:${to}?subject=${encodeURIComponent('פנייה מהאתר')}&body=${encodeURIComponent(body)}`;
    const sent = document.querySelector('.form-sent');
    if (sent) sent.hidden = false;
  });

  $('#news-form')?.addEventListener('submit', e => {
    e.preventDefault();
    const i = $('#news-mail'), m = $('.news__msg');
    if (!emailOk(i.value.trim())) { m.textContent = 'נא להזין כתובת מייל תקינה'; m.style.color = '#7a2718'; return; }
    // אין רשימת תפוצה מחוברת. שולחים בקשת הרשמה במייל במקום להבטיח משהו שלא קורה.
    const to = e.currentTarget.dataset.mailto;
    location.href = `mailto:${to}?subject=${encodeURIComponent('הרשמה לרשימת התפוצה')}` +
                    `&body=${encodeURIComponent('אשמח להצטרף לרשימת התפוצה ולקבל את קוד ההנחה.\nכתובת המייל שלי: ' + i.value.trim())}`;
    m.textContent = 'פתחנו לכם הודעה מוכנה. שלחו אותה ונחזור אליכם עם הקוד.'; m.style.color = '';
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
    stage.addEventListener('click', () => {
      const on = stage.getAttribute('aria-pressed') === 'true';
      stage.setAttribute('aria-pressed', String(!on));
      if (!on) dims.setAttribute('data-on', ''); else dims.removeAttribute('data-on');
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
