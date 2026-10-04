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
