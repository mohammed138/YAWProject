/* ============================================================
   YAW STUDIO — cinematic home interactions
   ============================================================ */
(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* header scroll state + hide on scroll down */
  var hdr = document.querySelector('.hdr');
  var menuRoom = document.getElementById('menuRoom');
  if (hdr && document.body.classList.contains('fs-cine')) {
    var lastY = window.scrollY || 0;
    var hdrTick = false;
    function updateHdr() {
      var y = window.scrollY || 0;
      hdr.classList.toggle('solid', y > 60);
      if (menuRoom && menuRoom.classList.contains('open')) {
        hdr.classList.remove('is-away');
        lastY = y;
        return;
      }
      if (y < 48) {
        hdr.classList.remove('is-away');
      } else if (y > lastY + 4) {
        hdr.classList.add('is-away');
      } else if (y < lastY - 2) {
        hdr.classList.remove('is-away');
      }
      lastY = y;
    }
    function onHdrScroll() {
      if (hdrTick) return;
      hdrTick = true;
      requestAnimationFrame(function () {
        hdrTick = false;
        updateHdr();
      });
    }
    updateHdr();
    window.addEventListener('scroll', onHdrScroll, { passive: true });
  }

  /* reveal on scroll */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) e.target.classList.add('seen');
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.story-editorial, .prod-visual').forEach(function (el) {
    if (reduce) el.classList.add('seen');
    else io.observe(el);
  });

  /* hero parallax */
  var cine = document.querySelector('.cine');
  if (cine && !reduce) {
    function activePh() {
      var s = cine.querySelector('.shot.on .ph');
      return s || cine.querySelector('.shot .ph');
    }
    window.addEventListener('scroll', function () {
      var ph = activePh();
      if (!ph) return;
      var r = cine.getBoundingClientRect();
      if (r.bottom < 0 || r.top > window.innerHeight) return;
      var p = Math.min(1, Math.max(0, -r.top / r.height));
      ph.style.transform = 'scale(' + (1.02 + p * 0.08).toFixed(3) + ') translate3d(0,' + (p * 40).toFixed(1) + 'px,0)';
    }, { passive: true });
  }

  /* film-strip reel */
  var reel = document.getElementById('filmReel');
  var reelNav = document.querySelector('.films-act .reel-nav');
  if (reel && reelNav) {
    var films = [].slice.call(reel.querySelectorAll('.film'));
    var cnt = reelNav.querySelector('.cnt');
    var bar = reelNav.querySelector('.bar i');
    var idx = 0;
    var lock = false;

    function paint(i) {
      if (!films.length) return;
      idx = (i + films.length) % films.length;
      films.forEach(function (f, n) { f.classList.toggle('on', n === idx); });
      if (cnt) cnt.textContent = String(idx + 1).padStart(2, '0') + ' / ' + String(films.length).padStart(2, '0');
      if (bar) bar.style.transform = 'scaleX(' + ((idx + 1) / films.length).toFixed(3) + ')';
    }

    function go(i) {
      paint(i);
      lock = true;
      films[idx].scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', inline: 'center', block: 'nearest' });
      setTimeout(function () { lock = false; }, reduce ? 50 : 450);
    }

    reelNav.querySelectorAll('[data-reel]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        go(idx + (btn.getAttribute('data-reel') === 'next' ? 1 : -1));
      });
    });

    var scrollT;
    reel.addEventListener('scroll', function () {
      if (lock) return;
      clearTimeout(scrollT);
      scrollT = setTimeout(function () {
        var mid = reel.scrollLeft + reel.clientWidth / 2;
        var best = 0, dist = Infinity;
        films.forEach(function (f, n) {
          var c = f.offsetLeft + f.offsetWidth / 2;
          var d = Math.abs(c - mid);
          if (d < dist) { dist = d; best = n; }
        });
        paint(best);
      }, 60);
    }, { passive: true });

    paint(0);

    /* drag / swipe the reel with mouse or touch */
    var drag = { active: false, moved: false, startX: 0, startLeft: 0, pid: null };
    function dragStart(e) {
      if (e.pointerType === 'mouse' && e.button !== 0) return;
      drag.active = true;
      drag.moved = false;
      drag.startX = e.clientX;
      drag.startLeft = reel.scrollLeft;
      drag.pid = e.pointerId;
      reel.classList.add('is-dragging');
      try { reel.setPointerCapture(e.pointerId); } catch (err) {}
    }
    function dragMove(e) {
      if (!drag.active) return;
      var dx = e.clientX - drag.startX;
      if (Math.abs(dx) > 4) drag.moved = true;
      reel.scrollLeft = drag.startLeft - dx;
    }
    function dragEnd(e) {
      if (!drag.active) return;
      drag.active = false;
      reel.classList.remove('is-dragging');
      try { if (drag.pid != null) reel.releasePointerCapture(drag.pid); } catch (err) {}
      drag.pid = null;
      if (drag.moved) {
        var mid = reel.scrollLeft + reel.clientWidth / 2;
        var best = 0, dist = Infinity;
        films.forEach(function (f, n) {
          var c = f.offsetLeft + f.offsetWidth / 2;
          var d = Math.abs(c - mid);
          if (d < dist) { dist = d; best = n; }
        });
        go(best);
      }
    }
    reel.addEventListener('pointerdown', dragStart);
    reel.addEventListener('pointermove', dragMove);
    reel.addEventListener('pointerup', dragEnd);
    reel.addEventListener('pointercancel', dragEnd);
    reel.addEventListener('click', function (e) {
      if (drag.moved) {
        e.preventDefault();
        e.stopPropagation();
        drag.moved = false;
      }
    }, true);

    if (!reduce && finePointer) {
      films.forEach(function (piece) {
        var plate = piece.querySelector('.plate');
        if (!plate) return;
        piece.addEventListener('mousemove', function (e) {
          if (drag.active) return;
          var r = plate.getBoundingClientRect();
          var px = (e.clientX - r.left) / r.width - 0.5;
          var py = (e.clientY - r.top) / r.height - 0.5;
          var ph = plate.querySelector('.ph');
          if (ph) ph.style.transform = 'scale(1.06) translate3d(' + (px * -14).toFixed(1) + 'px,' + (py * -10).toFixed(1) + 'px,0)';
        });
        piece.addEventListener('mouseleave', function () {
          var ph = plate.querySelector('.ph');
          if (ph) ph.style.transform = '';
        });
      });
    }
  }

  /* cursor gallery */
  var gallery = document.getElementById('cursorGallery');
  var label = document.getElementById('cursorLabel');
  if (gallery && !reduce && finePointer) {
    var frames = [].slice.call(gallery.querySelectorAll('.cursor-frame'));
    var stage = gallery.querySelector('.cursor-stage');
    var gx = 0, gy = 0, ax = 0, ay = 0, raf;

    gallery.addEventListener('mousemove', function (e) {
      var r = stage.getBoundingClientRect();
      gx = ((e.clientX - r.left) / r.width - 0.5) * 2;
      gy = ((e.clientY - r.top) / r.height - 0.5) * 2;
      if (!raf) raf = requestAnimationFrame(tick);
    }, { passive: true });

    function tick() {
      ax += (gx - ax) * 0.06;
      ay += (gy - ay) * 0.06;
      frames.forEach(function (f, i) {
        var depth = 1 + (i % 3) * 0.4;
        f.style.transform = 'translate3d(' + (ax * 14 * depth).toFixed(2) + 'px,' + (ay * 10 * depth).toFixed(2) + 'px,0)';
      });
      raf = (Math.abs(gx - ax) > 0.002 || Math.abs(gy - ay) > 0.002) ? requestAnimationFrame(tick) : null;
    }

    if (label) {
      window.addEventListener('mousemove', function (e) {
        if (!gallery.matches(':hover')) return;
        label.style.left = e.clientX + 'px';
        label.style.top = e.clientY + 'px';
      }, { passive: true });
      gallery.addEventListener('mouseenter', function () { label.classList.add('on'); gallery.classList.add('dim-others'); });
      gallery.addEventListener('mouseleave', function () {
        label.classList.remove('on');
        gallery.classList.remove('dim-others');
        frames.forEach(function (f) { f.classList.remove('active'); f.style.transform = ''; });
      });
      frames.forEach(function (f) {
        f.addEventListener('mouseenter', function () {
          frames.forEach(function (x) { x.classList.toggle('active', x === f); });
          label.textContent = 'View';
        });
      });
    }
  }

  /* publications marquee — pause on press / focus */
  var credits = document.getElementById('creditsField');
  if (credits) {
    credits.addEventListener('pointerdown', function () { credits.classList.add('is-paused'); });
    credits.addEventListener('pointerup', function () { credits.classList.remove('is-paused'); });
    credits.addEventListener('pointerleave', function () { credits.classList.remove('is-paused'); });
    credits.querySelectorAll('.credit-item').forEach(function (el) {
      el.setAttribute('tabindex', '0');
      el.addEventListener('focus', function () { credits.classList.add('is-paused'); });
      el.addEventListener('blur', function () { credits.classList.remove('is-paused'); });
    });
  }

  /* production reel capability switch */
  var prodVisual = document.querySelector('.prod-visual');
  var prodRows = [].slice.call(document.querySelectorAll('.prod-row'));
  var prodImgs = [].slice.call(document.querySelectorAll('.prod-img'));
  var prodCap = document.getElementById('prodCap');
  var prodLabel = document.getElementById('prodLabel');
  if (prodRows.length && prodImgs.length) {
    function activate(row) {
      var cap = row.getAttribute('data-cap');
      var label = row.getAttribute('data-label') || '';
      prodRows.forEach(function (r) { r.classList.toggle('active', r === row); });
      prodImgs.forEach(function (img) {
        var on = img.getAttribute('data-cap') === cap;
        img.classList.toggle('on', on);
        if (on) {
          var ph = img.querySelector('.ph img');
          if (ph && !reduce) {
            ph.style.animation = 'none';
            void ph.offsetWidth;
            ph.style.animation = '';
          }
        }
      });
      if (prodCap) prodCap.textContent = cap;
      if (prodLabel) prodLabel.textContent = label;
    }
    prodRows.forEach(function (row) {
      row.addEventListener('mouseenter', function () { activate(row); });
      row.addEventListener('focus', function () { activate(row); });
      row.addEventListener('click', function () { activate(row); });
    });
  }

  /* footer end-of-reel timecode */
  var endTc = document.getElementById('endTc');
  if (endTc && !reduce) {
    function pad2(n) { return String(n).padStart(2, '0'); }
    function tick() {
      var s = Math.floor(performance.now() / 1000) % 3600;
      var mm = Math.floor(s / 60);
      var ss = s % 60;
      endTc.textContent = '00:' + pad2(mm) + ':' + pad2(ss);
    }
    tick();
    setInterval(tick, 1000);
  }
})();
