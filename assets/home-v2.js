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
    var n = shots.length;
    var i = 0;
    var lock = false;

    function pad(v) { return (v < 10 ? '0' : '') + v; }

    function apply(next, dir) {
      if (next === i || lock) return;
      lock = true;
      root.classList.toggle('is-prev', dir === 'prev');
      var prev = i;
      i = (next + n) % n;

      shots[prev].classList.add('is-leave');
      shots[prev].classList.remove('on');
      shots[i].classList.add('on');

      quotes[prev].classList.add('is-leave');
      quotes[prev].classList.remove('on');
      quotes[prev].setAttribute('aria-hidden', 'true');
      quotes[i].classList.add('on');
      quotes[i].removeAttribute('aria-hidden');

      tabs.forEach(function (btn, idx) {
        var on = idx === i;
        btn.classList.toggle('on', on);
        if (on) btn.setAttribute('aria-current', 'true');
        else btn.removeAttribute('aria-current');
      });
      if (nowEl) nowEl.textContent = pad(i + 1);
      if (rail) rail.style.width = (n < 2 ? 100 : (i / (n - 1)) * 100) + '%';
      if (peekPrev) peekPrev.src = srcs[(i - 1 + n) % n];
      if (peekNext) peekNext.src = srcs[(i + 1) % n];

      window.setTimeout(function () {
        shots[prev].classList.remove('is-leave');
        quotes[prev].classList.remove('is-leave');
        lock = false;
      }, reduce ? 80 : 820);
    }

    if (rail) rail.style.width = '0%';
    if (peekPrev) peekPrev.src = srcs[n - 1];
    if (peekNext) peekNext.src = srcs[1];

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
