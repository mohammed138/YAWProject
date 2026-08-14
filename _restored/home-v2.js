/* YAW STUDIO — home v2 comparison helpers */
(function () {
  'use strict';
  if (!document.body.classList.contains('home-v2')) return;

  var coarse = window.matchMedia('(hover: none), (pointer: coarse)').matches;
  if (!coarse) return;

  var gallery = document.getElementById('cursorGallery');
  if (!gallery) return;
  gallery.classList.add('is-touch');
  gallery.querySelectorAll('.cursor-frame').forEach(function (f) {
    f.style.transform = '';
  });
})();
