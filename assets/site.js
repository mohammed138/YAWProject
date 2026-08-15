/* YAW STUDIO — small helpers. No framework, no tracking. */

/* 1. If an image file is missing, remove the broken icon.
      The gradient behind the slot keeps the layout looking designed. */
document.querySelectorAll('.ph img').forEach(function (img) {
  img.addEventListener('error', function () { img.remove(); });
  if (img.complete && img.naturalWidth === 0) img.remove();
});

/* 2. Filter chips — visual only in this static build.
      Wire these to your real query when the CMS is connected. */
document.querySelectorAll('[data-filter]').forEach(function (group) {
  group.addEventListener('click', function (e) {
    var b = e.target.closest('.chip');
    if (!b) return;
    b.setAttribute('aria-pressed', b.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
  });
});

/* 3. Forms are not connected yet.
      See README.md — add a Formspree / Netlify / Web3Forms action. */
document.querySelectorAll('[data-form]').forEach(function (f) {
  f.addEventListener('submit', function (e) {
    if (f.getAttribute('action')) return;      // real endpoint set — let it through
    e.preventDefault();
    var note = document.createElement('p');
    note.className = 'fine';
    note.style.color = 'var(--ask)';
    note.textContent = 'Form not connected yet. Add an action URL — see README.md.';
    f.appendChild(note);
  });
});

/* ============================================================
   CINEMA LAYER
   ============================================================ */
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- 1 · the entrance ------------------------------------ */
  var intro = document.querySelector('.intro');
  if (intro) {
    if (reduce) {
      intro.remove();
    } else {
      // measure each stroke so the draw-on finishes exactly, whatever the size
      intro.querySelectorAll('.mark path, .mark line').forEach(function (el) {
        var len = el.getTotalLength ? el.getTotalLength() : 1400;
        el.style.setProperty('--len', Math.ceil(len));
      });
      var closed = false;
      function open() {
        if (closed) return;
        closed = true;
        intro.classList.add('open');
        setTimeout(function () { intro.classList.add('out'); }, 700);
        setTimeout(function () { intro.remove(); }, 1800);
        document.body.style.overflow = '';
      }
      document.body.style.overflow = 'hidden';
      setTimeout(open, 3200);
      intro.addEventListener('click', open);
      window.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' || e.key === 'Enter' || e.key === ' ') open();
      });
      window.addEventListener('wheel', open, { passive: true, once: true });
      window.addEventListener('touchstart', open, { passive: true, once: true });
    }
  }

  /* --- 2 · the cinemascope hero ---------------------------- */
  var cine = document.querySelector('.cine');
  if (cine) {
    var shots = [].slice.call(cine.querySelectorAll('.shot'));
    var ticks = [].slice.call(cine.querySelectorAll('.hero-ticks button'));
    var cntEl = cine.querySelector('.hero-cnt');
    var i = 0, timer;

    function pad(n) { return String(n).padStart(2, '0'); }

    var cap = cine.querySelector('.cap');
    var capEyebrow = cap && cap.querySelector('.hero-eyebrow');
    var capTitle = cap && cap.querySelector('h1');
    var capRole = cap && cap.querySelector('.role');

    function decodeAttr(v) {
      if (!v) return '';
      var t = document.createElement('textarea');
      t.innerHTML = v;
      return t.value;
    }

    function syncCap(first) {
      if (!cap) return;
      var s = shots[i];
      var eyebrow = decodeAttr(s.getAttribute('data-eyebrow'));
      var title = decodeAttr(s.getAttribute('data-title'));
      var role = decodeAttr(s.getAttribute('data-role'));
      if (!title) return;

      function apply() {
        if (capEyebrow && eyebrow) capEyebrow.textContent = eyebrow;
        if (capTitle) capTitle.textContent = title;
        if (capRole && role) capRole.textContent = role;
        cap.classList.remove('is-swapping');
      }

      if (first || reduce) { apply(); return; }
      if (capTitle && capTitle.textContent === title) return;
      cap.classList.add('is-swapping');
      window.setTimeout(apply, 220);
    }

    // a shot may carry footage instead of a still — only the visible one runs,
    // and the still underneath stays put wherever autoplay is refused
    var clips = [].slice.call(cine.querySelectorAll('video.hero-clip'));
    clips.forEach(function (v) {
      var src = v.querySelector('source');
      if (src && src.getAttribute('data-src-mobile') && window.matchMedia('(max-width:700px)').matches) {
        src.setAttribute('src', src.getAttribute('data-src-mobile'));
        v.load();
      }
      v.addEventListener('playing', function () { v.classList.add('is-ready'); });
    });
    function syncClips() {
      clips.forEach(function (v) {
        var live = !reduce && v.closest('.shot') === shots[i];
        if (live) {
          var p = v.play();
          if (p && p.catch) p.catch(function () { v.classList.remove('is-ready'); });
        } else {
          v.pause();
        }
      });
    }

    function show(n, first) {
      i = (n + shots.length) % shots.length;
      shots.forEach(function (s, k) { s.classList.toggle('on', k === i); });
      syncClips();
      syncCap(!!first);
      ticks.forEach(function (t, k) {
        var on = k === i;
        t.classList.toggle('on', on);
        if (on) t.setAttribute('aria-current', 'true');
        else t.removeAttribute('aria-current');
      });
      if (cntEl) cntEl.textContent = pad(i + 1) + ' / ' + pad(shots.length);
      var ph = shots[i].querySelector('.ph');
      if (ph && !reduce) { ph.style.animation = 'none'; void ph.offsetWidth; ph.style.animation = ''; }
    }
    // a shot carrying footage holds longer than a still, so the clip gets watched
    function dwell() { return parseInt(shots[i].getAttribute('data-dwell'), 10) || 7000; }
    function play() {
      clearTimeout(timer);
      timer = setTimeout(function () { show(i + 1); play(); }, dwell());
    }

    ticks.forEach(function (t) {
      t.addEventListener('click', function () {
        var n = parseInt(t.getAttribute('data-shot'), 10);
        if (isNaN(n)) return;
        show(n);
        play();
      });
    });

    show(0, true);
    if (!reduce && shots.length > 1) play();
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (en) {
        en.forEach(function (e) {
          if (e.isIntersecting) { play(); syncClips(); }
          else { clearTimeout(timer); clips.forEach(function (v) { v.pause(); }); }
        });
      }, { threshold: 0.15 }).observe(cine);
    }
  }
})();

/* ============================================================
   THE MENU ROOM
   ============================================================ */
(function () {
  var btn = document.getElementById('menuBtn');
  var room = document.getElementById('menuRoom');
  if (!btn || !room) return;
  var closeBtn = document.getElementById('menuClose');
  var links = [].slice.call(room.querySelectorAll('.list a'));
  var lays = [].slice.call(room.querySelectorAll('.view .lay'));

  function open() {
    room.classList.add('open');
    room.setAttribute('aria-hidden', 'false');
    btn.setAttribute('aria-expanded', 'true');
    document.body.classList.add('locked');
    if (links[0]) links[0].focus();
  }
  function shut() {
    room.classList.remove('open');
    room.setAttribute('aria-hidden', 'true');
    btn.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('locked');
    btn.focus();
  }
  btn.addEventListener('click', open);
  if (closeBtn) closeBtn.addEventListener('click', shut);
  window.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && room.classList.contains('open')) shut();
  });
  /* the picture on the right follows whichever line you are on */
  links.forEach(function (a, i) {
    function pick() { lays.forEach(function (l, k) { l.classList.toggle('on', k === i); }); }
    a.addEventListener('mouseenter', pick);
    a.addEventListener('focus', pick);
  });
})();

/* ============================================================
   HELD PAGE — a page marked data-lock-links keeps the visitor.
   Routes to other documents are neutralised; anchors within this
   document still scroll, so the in-page navigation keeps working.
   ============================================================ */
(function () {
  var body = document.body;
  if (!body || !body.hasAttribute('data-lock-links')) return;
  var here = location.pathname.split('/').pop() || 'index.html';

  function leavesPage(a) {
    var href = a.getAttribute('href') || '';
    if (!href || href.charAt(0) === '#') return false;
    var doc = href.split('#')[0];
    return doc !== '' && doc !== here;
  }

  body.querySelectorAll('a[href]').forEach(function (a) {
    if (!leavesPage(a)) return;
    a.classList.add('is-locked');
    a.setAttribute('aria-disabled', 'true');
  });

  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a.is-locked') : null;
    if (!a) return;
    e.preventDefault();
    e.stopPropagation();
  }, true);
})();
