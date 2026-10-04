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
  select(tabs[0]);
})();
