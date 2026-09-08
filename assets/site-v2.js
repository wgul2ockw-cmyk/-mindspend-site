/* Progressive enhancement only: all product copy and navigation live in HTML. */
(() => {
  'use strict';
  const root = document.documentElement;
  const english = root.lang === 'en';
  const text = (th, en) => english ? en : th;
  const menu = document.querySelector('.menu-button');
  const navigation = document.getElementById('navigation');
  const closeMenu = () => {
    navigation.dataset.open = 'false';
    menu.setAttribute('aria-expanded', 'false');
    menu.setAttribute('aria-label', text('เปิดเมนู', 'Open menu'));
  };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    navigation.dataset.open = String(open);
    menu.setAttribute('aria-expanded', String(open));
    menu.setAttribute('aria-label', open ? text('ปิดเมนู', 'Close menu') : text('เปิดเมนู', 'Open menu'));
  });
  navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      closeMenu(); menu.focus();
    }
  });
  matchMedia('(min-width: 901px)').addEventListener('change', closeMenu);

  const themeButton = document.querySelector('.theme-button');
  const syncThemeButton = () => themeButton.setAttribute('aria-pressed', String(root.dataset.theme === 'dark'));
  syncThemeButton();
  themeButton.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('ms-theme', root.dataset.theme); } catch (_) { /* Storage is optional. */ }
    syncThemeButton();
  });

  const tabs = [...document.querySelectorAll('.tour-tab')];
  function selectTab(tab, focus = false) {
    tabs.forEach(item => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
    });
    if (focus) tab.focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => selectTab(tab));
    tab.addEventListener('keydown', event => {
      let next = index;
      if (['ArrowRight', 'ArrowDown'].includes(event.key)) next = (index + 1) % tabs.length;
      else if (['ArrowLeft', 'ArrowUp'].includes(event.key)) next = (index + tabs.length - 1) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault(); selectTab(tabs[next], true);
    });
  });
  selectTab(tabs[0]);
  root.classList.add('enhanced');

  document.querySelectorAll('[data-tag]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('[data-tag]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    const planned = button.dataset.tag === 'planned';
    document.querySelector('[data-tag-status]').textContent = planned
      ? text('ตัวอย่างนี้เลือก “วางแผน” — ตั้งใจไว้ก่อนจ่าย', 'This example is planned — intended before paying.')
      : text('ตัวอย่างนี้เลือก “ฉับพลัน” — ตัดสินใจในจังหวะนั้น', 'This example is impulse — decided in the moment.');
  }));

  let building = false;
  const initialNote = document.getElementById('score-note').textContent;
  document.querySelectorAll('[data-score-state]').forEach(button => button.addEventListener('click', () => {
    building = button.dataset.scoreState === 'building';
    document.querySelectorAll('[data-score-state]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    document.getElementById('field-center').classList.toggle('field-building', building);
    document.getElementById('field-value').textContent = building ? '12 / 30' : '76';
    document.getElementById('field-label').textContent = building ? text('วันของข้อมูลตัวอย่าง', 'days of sample history') : text('สัปดาห์ตัวอย่าง', 'Sample week');
    document.querySelectorAll('[data-pillar]').forEach(item => { item.textContent = building ? '—' : item.dataset.pillar; });
    document.getElementById('score-note').textContent = building
      ? text('กำลังเก็บข้อมูล: ตัวอย่างนี้มีช่วงข้อมูล 12 วันจากขั้นต่ำ 30 วัน จึงยังไม่แสดงคะแนน และไม่นับข้อมูลที่ขาดเป็นศูนย์', 'Building data: this example has 12 of the minimum 30 days of history. No score is shown; missing information is not treated as zero.')
      : initialNote;
    drawFrame(performance.now());
  }));

  // Inward-facing dashes echo the native Concentric Field. Sample artwork only.
  const canvas = document.getElementById('mind-field');
  const ctx = canvas.getContext('2d');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let inView = false, frame = 0;
  let palette = [];
  const refreshPalette = () => {
    const css = getComputedStyle(root);
    palette = ['--sage', '--clay', '--gold', '--mint', '--violet', '--muted'].map(token => css.getPropertyValue(token).trim());
    drawFrame(performance.now());
  };
  let seed = 42;
  const random = () => { seed = Math.imul(1664525, seed) + 1013904223 | 0; return (seed >>> 0) / 4294967296; };
  const dashes = Array.from({length:1080}, () => ({a:random()*Math.PI*2, r:random(), l:2+random()*6, c:Math.floor(random()*5)}));
  function drawFrame(now) {
    if (!ctx) return;
    ctx.clearRect(0,0,720,720);
    const phase = motion.matches ? 0 : now / 18000;
    dashes.forEach(d => {
      const position = (d.r + phase) % 1;
      const r = 320 - position * 225;
      const angle = d.a + Math.sin(position*Math.PI)*.04;
      ctx.globalAlpha = (.15 + Math.sin(position*Math.PI)*.48) * (building ? .55 : 1);
      ctx.strokeStyle = palette[building ? 5 : d.c];
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(360+Math.cos(angle)*r,360+Math.sin(angle)*r);
      ctx.lineTo(360+Math.cos(angle)*(r+d.l),360+Math.sin(angle)*(r+d.l));
      ctx.stroke();
    });
    ctx.globalAlpha = 1;
  }
  function tick(now) {
    drawFrame(now);
    frame = requestAnimationFrame(tick);
  }
  function reconcileAnimation() {
    cancelAnimationFrame(frame); frame = 0;
    if (inView && !document.hidden && !motion.matches && ctx) frame = requestAnimationFrame(tick);
    else drawFrame(performance.now());
  }
  refreshPalette();
  new MutationObserver(refreshPalette).observe(root,{attributes:true,attributeFilter:['data-theme']});
  if ('IntersectionObserver' in window) new IntersectionObserver(entries => {
    inView = entries[0].isIntersecting; reconcileAnimation();
  }).observe(canvas);
  else { inView = true; reconcileAnimation(); }
  motion.addEventListener('change', reconcileAnimation);
  document.addEventListener('visibilitychange', reconcileAnimation);
})();
