/* YAW STUDIO — home v2 comparison helpers */
(function () {
  'use strict';
  if (!document.body.classList.contains('home-v2')) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var coarse = window.matchMedia('(hover: none), (pointer: coarse)').matches;

  /* ---- navbar: hide on scroll down, show on scroll up ---- */
  /* Primary handler lives in home.js; keep a light fallback here. */
  var hdr = document.querySelector('.hdr');
  var overlay = document.getElementById('menuRoom');
  if (hdr && !hdr.dataset.hideBound) {
    hdr.dataset.hideBound = '1';
    var lastY = window.scrollY || 0;
    var ticking = false;
    function onScroll() {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () {
        ticking = false;
        if (overlay && overlay.classList.contains('open')) {
          hdr.classList.remove('is-away');
          lastY = window.scrollY || 0;
          return;
        }
        var y = window.scrollY || 0;
        if (y < 48) hdr.classList.remove('is-away');
        else if (y > lastY + 4) hdr.classList.add('is-away');
        else if (y < lastY - 2) hdr.classList.remove('is-away');
        lastY = y;
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---- per-section image reveals ---- */
  var revealIo = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        revealIo.unobserve(entry.target);
      }
    });
  }, { threshold: 0.22, rootMargin: '0px 0px -8% 0px' });

  document.querySelectorAll('.home-v2 .cursor-frame, .home-v2 .final-visual, .home-v2 .end-brand').forEach(function (el) {
    if (reduce) el.classList.add('in-view');
    else revealIo.observe(el);
  });

  /* ---- film MP4s: play active / hovered / in-view plate ---- */
  var films = [].slice.call(document.querySelectorAll('.films-act .film'));
  function syncFilmClips() {
    films.forEach(function (film) {
      var vid = film.querySelector('video.film-clip');
      if (!vid) return;
      var shouldPlay = !reduce && (
        film.classList.contains('on') ||
        film.classList.contains('in-view') ||
        film.matches(':hover')
      );
      if (shouldPlay) {
        var play = vid.play();
        if (play && play.catch) play.catch(function () {});
      } else {
        vid.pause();
      }
    });
  }

  films.forEach(function (film) {
    var vid = film.querySelector('video.film-clip');
    if (!vid) return;
    vid.muted = true;
    vid.setAttribute('playsinline', '');
    vid.addEventListener('playing', function () { film.classList.add('is-playing'); });
    vid.addEventListener('pause', function () {
      if (!film.classList.contains('on') && !film.matches(':hover')) {
        film.classList.remove('is-playing');
      }
    });
    film.addEventListener('mouseenter', syncFilmClips);
    film.addEventListener('mouseleave', syncFilmClips);
  });

  if (films.length) {
    var classWatch = new MutationObserver(syncFilmClips);
    films.forEach(function (film) {
      classWatch.observe(film, { attributes: true, attributeFilter: ['class'] });
    });

    var filmIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        entry.target.classList.toggle('in-view', entry.isIntersecting);
      });
      syncFilmClips();
    }, { threshold: 0.55 });
    films.forEach(function (film) { filmIo.observe(film); });
    syncFilmClips();
  }

  /* ---- voices slider ---- */
  (function initVoices() {
    var root = document.getElementById('voicesSlider');
    if (!root) return;
    var shots = [].slice.call(root.querySelectorAll('.voices-shot'));
    var quotes = [].slice.call(root.querySelectorAll('.voices-quote'));
    var tabs = [].slice.call(root.querySelectorAll('.voices-index button'));
    var nowEl = document.getElementById('voicesNow');
    var rail = root.querySelector('.voices-rail i');
    var peekPrev = root.querySelector('.voices-peek.is-prev img');
    var peekNext = root.querySelector('.voices-peek.is-next img');
    var srcs = shots.map(function (s) {
      var img = s.querySelector('img');
      return img ? img.getAttribute('src') : '';
    });
    var n = quotes.length || shots.length;
    var i = 0;
    var lock = false;
    var hover = false;
    var vis = true;
    var timer = null;

    function pad(v) { return (v < 10 ? '0' : '') + v; }

    function dwell() {
      return quotes[i] && quotes[i].classList.contains('is-long') ? 6500 : 4000;
    }

    function canAuto() {
      return !reduce && n > 1 && vis && !hover && !document.hidden;
    }

    function stopAuto() {
      if (timer) {
        window.clearTimeout(timer);
        timer = null;
      }
      if (rail) {
        rail.style.transition = 'none';
        rail.style.width = '0%';
      }
    }

    function armAuto() {
      stopAuto();
      if (!canAuto()) return;
      var ms = dwell();
      if (rail) {
        void rail.offsetWidth;
        rail.style.transition = 'width ' + ms + 'ms linear';
        rail.style.width = '100%';
      }
      timer = window.setTimeout(function () {
        apply(i + 1, 'next');
      }, ms);
    }

    function apply(next, dir) {
      if ((next + n) % n === i || lock) return;
      stopAuto();
      lock = true;
      root.classList.toggle('is-prev', dir === 'prev');
      var prev = i;
      i = (next + n) % n;

      if (shots[prev]) {
        shots[prev].classList.add('is-leave');
        shots[prev].classList.remove('on');
      }
      if (shots[i]) shots[i].classList.add('on');

      if (quotes[prev]) {
        quotes[prev].classList.add('is-leave');
        quotes[prev].classList.remove('on');
        quotes[prev].setAttribute('aria-hidden', 'true');
      }
      if (quotes[i]) {
        quotes[i].classList.add('on');
        quotes[i].removeAttribute('aria-hidden');
      }

      tabs.forEach(function (btn, idx) {
        var on = idx === i;
        btn.classList.toggle('on', on);
        if (on) btn.setAttribute('aria-current', 'true');
        else btn.removeAttribute('aria-current');
      });
      if (nowEl) nowEl.textContent = pad(i + 1);
      if (peekPrev && srcs.length) peekPrev.src = srcs[(i - 1 + n) % n];
      if (peekNext && srcs.length) peekNext.src = srcs[(i + 1) % n];

      window.setTimeout(function () {
        if (shots[prev]) shots[prev].classList.remove('is-leave');
        if (quotes[prev]) quotes[prev].classList.remove('is-leave');
        lock = false;
        armAuto();
      }, reduce ? 80 : 700);
    }

    if (rail) rail.style.width = '0%';
    if (peekPrev && srcs.length) peekPrev.src = srcs[n - 1];
    if (peekNext && srcs.length) peekNext.src = srcs[1];

    tabs.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var next = parseInt(btn.getAttribute('data-i'), 10);
        if (isNaN(next)) return;
        apply(next, next < i ? 'prev' : 'next');
      });
    });
    root.querySelectorAll('.voices-arrows button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var dir = btn.getAttribute('data-dir');
        apply(dir === 'prev' ? i - 1 : i + 1, dir);
      });
    });

    root.setAttribute('tabindex', '0');
    root.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); apply(i + 1, 'next'); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); apply(i - 1, 'prev'); }
    });

    var x0 = 0;
    root.addEventListener('touchstart', function (e) {
      x0 = e.changedTouches[0].clientX;
    }, { passive: true });
    root.addEventListener('touchend', function (e) {
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) < 48) return;
      if (dx < 0) apply(i + 1, 'next');
      else apply(i - 1, 'prev');
    }, { passive: true });

    if (!coarse) {
      root.addEventListener('mouseenter', function () { hover = true; stopAuto(); });
      root.addEventListener('mouseleave', function () { hover = false; armAuto(); });
    }
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) stopAuto();
      else armAuto();
    });

    var io = new IntersectionObserver(function (entries) {
      vis = !!(entries[0] && entries[0].isIntersecting);
      if (vis) armAuto();
      else stopAuto();
    }, { threshold: 0.12 });
    io.observe(root);
    armAuto();
  })();

  /* ---- touch frames gallery ---- */
  if (!coarse) return;
  var gallery = document.getElementById('cursorGallery');
  if (!gallery) return;
  gallery.classList.add('is-touch');
  gallery.querySelectorAll('.cursor-frame').forEach(function (f) {
    f.style.transform = '';
  });
})();
