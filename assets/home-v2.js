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

  /* ---- touch frames gallery ---- */
  if (!coarse) return;
  var gallery = document.getElementById('cursorGallery');
  if (!gallery) return;
  gallery.classList.add('is-touch');
  gallery.querySelectorAll('.cursor-frame').forEach(function (f) {
    f.style.transform = '';
  });
})();
