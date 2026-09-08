/* =========================================================================
   MindSpend site — น้องมายด์ interaction engine (shared, no dependencies)
   Voice rules (MINDSPEND_DESIGN_PRINCIPLES §4/§11): Itim only, observational,
   register high / valence zero — น้องมายด์ never tells the user what to do.
   ========================================================================= */
(function () {
  'use strict';
  var REDUCE = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var COARSE = window.matchMedia && matchMedia('(pointer: coarse)').matches;

  /* ---- theme toggle (dark home only; harmless elsewhere) --------------- */
  window.toggleTheme = function () {
    var h = document.documentElement;
    var n = h.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
    h.setAttribute('data-theme', n);
    try { localStorage.setItem('ms-theme', n); } catch (e) {}
  };

  /* ---- reveal on scroll ------------------------------------------------ */
  var els = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('visible'); });
  }

  /* ---- nav scrolled state + reading progress --------------------------- */
  var nav = document.querySelector('nav');
  var prog = document.querySelector('.ms-progress i');
  function onScroll() {
    if (nav) nav.classList.toggle('scrolled', scrollY > 30);
    if (prog) {
      var h = document.documentElement;
      var max = h.scrollHeight - innerHeight;
      prog.style.width = (max > 0 ? (Math.min(scrollY / max, 1) * 100) : 0) + '%';
    }
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  /* Supporting pages: make the full navigation available on small screens. */
  var links = nav && nav.querySelector('.nav-links');
  if (links) {
    var mobileMenu = document.createElement('details');
    mobileMenu.className = 'ms-mobile-menu';
    var menuSummary = document.createElement('summary');
    menuSummary.textContent = 'เมนู';
    var menuBody = document.createElement('div');
    links.querySelectorAll('a').forEach(function (a) { menuBody.appendChild(a.cloneNode(true)); });
    var themeControl = links.querySelector('.theme-toggle');
    if (themeControl) menuBody.appendChild(themeControl.cloneNode(true));
    mobileMenu.appendChild(menuSummary); mobileMenu.appendChild(menuBody);
    nav.appendChild(mobileMenu);
    menuBody.addEventListener('click', function (event) {
      if (event.target.closest('a')) mobileMenu.open = false;
    });
    mobileMenu.addEventListener('keydown', function (event) {
      if (event.key === 'Escape') { mobileMenu.open = false; menuSummary.focus(); }
    });
    nav.querySelectorAll('.nav-drop-trigger').forEach(function (trigger) {
      trigger.tabIndex = 0; trigger.setAttribute('role', 'button');
      trigger.setAttribute('aria-expanded', 'false');
      function toggleDrop() {
        var opened = trigger.parentElement.classList.toggle('open');
        trigger.setAttribute('aria-expanded', String(opened));
      }
      trigger.addEventListener('click', toggleDrop);
      trigger.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); toggleDrop(); }
        if (event.key === 'Escape') {
          trigger.parentElement.classList.remove('open'); trigger.setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  /* ---- น้องมายด์ speech bubbles ---------------------------------------- */
  var LINES = [
    'สวัสดีน้า เราชื่อน้องมายด์ 🌱',
    '“ตั้งใจซื้อหรือเปล่า?” — เราถามแค่นี้เองน้า',
    'ไม่มีถูกผิด มีแค่ได้เห็นตัวเองน้า',
    'วันนี้มีอะไรให้เราดูด้วยกันบ้างน้า',
    'เราอยู่ข้างเธอเสมอเลยน้า 💚',
    'เธอเลือกการซิงก์และการใช้ AI ได้ในตั้งค่าน้า',
    'มาดูเดือนนี้ด้วยกันมั้ย 👀'
  ];
  var li = 0, bubEl = null, bubTimer = null;

  function say(target, text) {
    if (bubEl) { bubEl.remove(); bubEl = null; clearTimeout(bubTimer); }
    var r = target.getBoundingClientRect();
    var b = document.createElement('div');
    b.className = 'ms-bub';
    b.setAttribute('role', 'status');
    b.textContent = text;
    document.body.appendChild(b);
    var x = Math.min(Math.max(r.left + r.width / 2 - b.offsetWidth / 2, 10), innerWidth - b.offsetWidth - 10);
    var y = r.top - b.offsetHeight - 12;
    if (y < 8) y = r.bottom + 12;
    b.style.left = x + 'px';
    b.style.top = y + 'px';
    requestAnimationFrame(function () { b.classList.add('show'); });
    bubEl = b;
    bubTimer = setTimeout(function () {
      b.classList.remove('show');
      setTimeout(function () { b.remove(); if (bubEl === b) bubEl = null; }, 260);
    }, 2600);
  }

  document.addEventListener('click', function (e) {
    var m = e.target.closest('[data-mind]');
    if (!m) return;
    m.classList.remove('boing'); void m.offsetWidth; m.classList.add('boing');
    setTimeout(function () { m.classList.remove('boing'); }, 700);
    say(m, m.getAttribute('data-say') || LINES[(li++) % LINES.length]);
  });

  /* sleeping mascot wake — swap art on first tap, then talk normally */
  document.addEventListener('click', function (e) {
    var w = e.target.closest('[data-wake]');
    if (!w || w.dataset.awake) return;
    w.dataset.awake = '1';
    var img = w.tagName === 'IMG' ? w : w.querySelector('img');
    if (img) img.src = w.getAttribute('data-wake');
    w.classList.add('awake');
    w.removeAttribute('data-say');
  });

  /* keyboard access for clickable mascots */
  document.querySelectorAll('[data-mind]').forEach(function (m) {
    if (!m.hasAttribute('tabindex')) m.setAttribute('tabindex', '0');
    if (!m.hasAttribute('role')) m.setAttribute('role', 'button');
    m.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); m.click(); }
    });
  });

  /* ---- count-up numbers [data-count] ----------------------------------- */
  function fmt(n) { return n.toLocaleString('en-US'); }
  function runCount(el) {
    var target = parseInt(el.getAttribute('data-count'), 10);
    var prefix = el.getAttribute('data-prefix') || '';
    if (!isFinite(target) || REDUCE) { el.textContent = prefix + fmt(target || 0); return; }
    var t0 = null, DUR = 1300;
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / DUR, 1);
      var ease = 1 - Math.pow(1 - p, 3);
      el.textContent = prefix + fmt(Math.round(target * ease));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counts = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window) {
    var co = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { runCount(e.target); co.unobserve(e.target); }
      });
    }, { threshold: 0.5 });
    counts.forEach(function (el) { co.observe(el); });
  } else {
    counts.forEach(runCount);
  }

  /* ---- hero mouse parallax [data-parallax] > [data-depth] --------------- */
  if (!REDUCE && !COARSE) {
    document.querySelectorAll('[data-parallax]').forEach(function (zone) {
      var kids = zone.querySelectorAll('[data-depth]');
      if (!kids.length) return;
      var raf = null, mx = 0, my = 0;
      function apply() {
        raf = null;
        kids.forEach(function (k) {
          var d = parseFloat(k.getAttribute('data-depth')) || 0;
          k.style.setProperty('--parx', (mx * d * 26).toFixed(1) + 'px');
          k.style.setProperty('--pary', (my * d * 18).toFixed(1) + 'px');
        });
      }
      zone.addEventListener('mousemove', function (e) {
        var r = zone.getBoundingClientRect();
        mx = (e.clientX - r.left) / r.width - 0.5;
        my = (e.clientY - r.top) / r.height - 0.5;
        if (!raf) raf = requestAnimationFrame(apply);
      });
      zone.addEventListener('mouseleave', function () {
        mx = my = 0;
        if (!raf) raf = requestAnimationFrame(apply);
      });
    });
  }

  /* ---- สติ+ tier picker (mirrors the in-app paywall behavior) ----------- */
  var tiles = document.querySelectorAll('.sp-tile[data-tier]');
  if (tiles.length) {
    var spCta = document.getElementById('sp-cta');
    var spTrial = document.getElementById('sp-trial');
    tiles.forEach(function (t) {
      t.addEventListener('click', function () {
        tiles.forEach(function (x) { x.classList.remove('on'); });
        t.classList.add('on');
        var life = t.getAttribute('data-tier') === 'lifetime';
        if (spCta) spCta.textContent = life ? 'เริ่มใช้ สติ+ ตลอดชีพ' : 'เริ่มฟรี 14 วัน';
        if (spTrial) spTrial.textContent = life ? 'จ่ายครั้งเดียว · เป็นเจ้าของถาวร' : 'ทดลอง 14 วันแรกฟรี · ยกเลิกได้ทุกเมื่อ';
      });
    });
  }

  /* ---- gentle 3D tilt [data-tilt] --------------------------------------- */
  if (!REDUCE && !COARSE) {
    document.querySelectorAll('[data-tilt]').forEach(function (c) {
      var r = null;
      c.addEventListener('mousemove', function (e) {
        r = r || c.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width - 0.5;
        var y = (e.clientY - r.top) / r.height - 0.5;
        c.style.setProperty('--ry', (x * 7).toFixed(2) + 'deg');
        c.style.setProperty('--rx', (-y * 7).toFixed(2) + 'deg');
      });
      c.addEventListener('mouseleave', function () {
        c.style.setProperty('--rx', '0deg');
        c.style.setProperty('--ry', '0deg');
        r = null;
      });
    });
  }
})();
