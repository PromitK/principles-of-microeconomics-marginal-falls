(() => {
  const controls = document.getElementById('course-controls');
  if (!controls) return;
  controls.hidden = false;
  const search = document.getElementById('module-search');
  const gamesOnly = document.getElementById('games-only');
  const buttons = [...document.querySelectorAll('[data-filter]')];
  const acts = [...document.querySelectorAll('[data-act]')];
  let active = 'all';
  function update() {
    const terms = search.value.toLowerCase().trim().split(/\s+/).filter(Boolean);
    let total = 0;
    for (const act of acts) {
      let count = 0;
      for (const row of act.querySelectorAll('[data-module]')) {
        const visible = (active === 'all' || act.dataset.act === active)
          && (!gamesOnly.checked || row.dataset.hasGames === 'true')
          && terms.every(term => row.dataset.search.includes(term));
        row.hidden = !visible;
        if (visible) count++;
      }
      act.hidden = count === 0;
      total += count;
    }
    document.getElementById('result-count').textContent = `${total} ${total === 1 ? 'module' : 'modules'}`;
    document.getElementById('no-results').hidden = total !== 0;
    for (const button of buttons) {
      const selected = button.dataset.filter === active;
      button.classList.toggle('active', selected);
      button.setAttribute('aria-pressed', String(selected));
    }
  }
  for (const button of buttons) button.addEventListener('click', () => { active = button.dataset.filter; update(); });
  search.addEventListener('input', update);
  gamesOnly.addEventListener('change', update);
  document.getElementById('reset-filters').addEventListener('click', () => {
    active = 'all'; search.value = ''; gamesOnly.checked = false; update(); search.focus();
  });
  document.querySelectorAll('.route-stop').forEach(link => link.addEventListener('click', () => {
    active = 'all'; search.value = ''; gamesOnly.checked = false; update();
  }));
})();


// Enhance module pages with accessible tabs; both panels remain readable without JavaScript.
(() => {
  const tablist = document.querySelector('.module-tabs');
  if (!tablist) return;
  const tabs = [...tablist.querySelectorAll('[role="tab"]')];
  function select(tab, focus = false) {
    for (const item of tabs) {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      document.getElementById(item.getAttribute('aria-controls')).hidden = !selected;
    }
    if (focus) tab.focus();
  }
  for (const [index, tab] of tabs.entries()) {
    tab.addEventListener('click', () => select(tab));
    tab.addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next !== undefined) { event.preventDefault(); select(tabs[next], true); }
    });
  }
  tablist.hidden = false;
  function selectFragment() {
    const tab = tabs.find(item => item.getAttribute('aria-controls') === `panel-${location.hash.slice(1)}`);
    if (tab) select(tab);
  }
  select(tabs[0]);
  selectFragment();
  window.addEventListener('hashchange', selectFragment);
  document.querySelectorAll('a[href="#slides"]').forEach(link => link.addEventListener('click', () => select(tabs.find(tab => tab.id === 'tab-slides'))));
})();


(() => {
  const viewer = document.querySelector('.slide-viewer');
  if (!viewer) return;
  const stage = viewer.querySelector('.slide-stage');
  const canvas = document.getElementById('slide-canvas');
  const ctx = canvas.getContext('2d');
  const count = Number(viewer.dataset.count);
  const width = Number(viewer.dataset.width), height = Number(viewer.dataset.height);
  const descriptions = JSON.parse(document.getElementById('slide-descriptions').textContent);
  const previous = document.getElementById('slide-prev'), next = document.getElementById('slide-next');
  const jump = document.getElementById('slide-page');
  const loading = document.getElementById('slide-loading'), error = document.getElementById('slide-error');
  let page = 0, generation = 0, cachedSource = '', cachedImage;
  async function show(index) {
    page = Math.max(0, Math.min(count - 1, index));
    const current = page, token = ++generation;
    previous.disabled = page === 0; next.disabled = page === count - 1; jump.value = String(page + 1);
    loading.hidden = false; error.hidden = true; stage.setAttribute('aria-busy', 'true');
    const source = `../slides/module-${viewer.dataset.module}-${String(Math.floor(page / 8) + 1).padStart(2, '0')}.webp`;
    try {
      let img = cachedImage;
      if (source !== cachedSource || !img) {
        img = new Image();
        await new Promise((resolve, reject) => { img.onload = resolve; img.onerror = reject; img.src = source; });
      }
      if (token !== generation) return;
      cachedImage = img; cachedSource = source;
      const slot = current % 8;
      ctx.clearRect(0, 0, width, height);
      ctx.drawImage(img, (slot % 2) * width, Math.floor(slot / 2) * height, width, height, 0, 0, width, height);
      canvas.setAttribute('aria-label', `Slide ${current + 1} of ${count}. ${descriptions[current] || ''}`);
      document.getElementById('slide-status').textContent = `Slide ${current + 1} of ${count}`;
      loading.hidden = true;
    } catch {
      if (token !== generation) return;
      loading.hidden = true; error.hidden = false;
    } finally { if (token === generation) stage.setAttribute('aria-busy', 'false'); }
  }
  previous.addEventListener('click', () => show(page - 1));
  next.addEventListener('click', () => show(page + 1));
  jump.addEventListener('change', () => { const value = Number(jump.value); show(Number.isFinite(value) ? Math.round(value) - 1 : page); });
  document.getElementById('slide-retry').addEventListener('click', () => { cachedSource = ''; show(page); });
  stage.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); show(page - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); show(page + 1); }
    if (event.key === 'Home') { event.preventDefault(); show(0); }
    if (event.key === 'End') { event.preventDefault(); show(count - 1); }
  });
  canvas.addEventListener('contextmenu', event => event.preventDefault());
  const full = document.getElementById('slide-fullscreen');
  function expand(active) {
    viewer.classList.toggle('is-expanded', active);
    document.body.classList.toggle('slides-expanded', active);
    full.textContent = active ? 'Exit full screen' : 'Full screen';
    full.setAttribute('aria-pressed', String(active));
    if (!active) full.focus();
  }
  full.hidden = false;
  full.addEventListener('click', () => expand(!viewer.classList.contains('is-expanded')));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && viewer.classList.contains('is-expanded')) expand(false);
  });
  show(0);
})();
