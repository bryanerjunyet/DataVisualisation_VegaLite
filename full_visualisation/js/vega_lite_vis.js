(function () {
  const embedOptions = { actions: false };

  vegaEmbed('#choropleth_map', 'js/malaysia_crime_map.vg.json', embedOptions)
    .then(() => wireMapYearMirror())
    .catch(console.error);

  vegaEmbed('#crime_stack', 'js/malaysia_crime_stacked.vg.json', embedOptions)
    .then(() => {})
    .catch(console.error);

  vegaEmbed('#crime_sunburst', 'js/malaysia_crime_sunburst.vg.json', embedOptions)
    .then()
    .catch(console.error);

  vegaEmbed('#crime_area', 'js/malaysia_crime_area.vg.json', embedOptions)
    .then(() => {})
    .catch(console.error);

  vegaEmbed('#crime_scattered', 'js/malaysia_crime_scattered.vg.json', embedOptions)
    .then(() => {})
    .catch(console.error);

  vegaEmbed('#crime_box', 'js/malaysia_crime_box.vg.json', embedOptions)
    .then(() => {})
    .catch(console.error);

    


  // Mirror the current map year next to slider (map)
  function wireMapYearMirror() {
    const binding = document.querySelector('#bindings_map .vega-bindings');
    const mirror = document.getElementById('map_year_value');
    if (!binding || !mirror) return;
    const input = binding.querySelector('input[type="range"], select');
    const update = () => { mirror.textContent = input ? input.value : '—'; };
    if (input) {
      update();
      input.addEventListener('input', update);
      input.addEventListener('change', update);
    }
  }

  /* ----------------------- DRAG & DROP -----------------------
   * Drag ONLY from the handle (button.drag-handle).
   * Finds insertion point using distance to card centers → reliable both ways.
   */
  const grid = document.getElementById('dashboard');
  let draggingCard = null;

  grid.addEventListener('dragstart', (e) => {
    if (!e.target.classList.contains('drag-handle')) { e.preventDefault(); return; }
    draggingCard = e.target.closest('.card');
    if (!draggingCard) { e.preventDefault(); return; }
    draggingCard.classList.add('dragging');
    e.dataTransfer.setData('text/plain', '');
    e.dataTransfer.effectAllowed = 'move';
  });

  grid.addEventListener('dragend', () => {
    if (draggingCard) draggingCard.classList.remove('dragging');
    draggingCard = null;
  });

  grid.addEventListener('dragover', (e) => {
    e.preventDefault();
    if (!draggingCard) return;
    const after = findInsertionPoint(grid, e.clientX, e.clientY);
    if (!after) grid.appendChild(draggingCard);
    else grid.insertBefore(draggingCard, after);
  });

  function findInsertionPoint(container, x, y) {
    const cards = [...container.querySelectorAll('.card:not(.dragging)')];
    if (cards.length === 0) return null;

    let closest = { dist: Infinity, el: null };
    for (const el of cards) {
      const r = el.getBoundingClientRect();
      const cx = r.left + r.width / 2;
      const cy = r.top + r.height / 2;
      const d = Math.hypot(x - cx, y - cy);
      if (d < closest.dist) closest = { dist: d, el };
    }
    if (!closest.el) return null;

    const rect = closest.el.getBoundingClientRect();
    const aboveCenter = y < rect.top + rect.height / 2;
    return aboveCenter ? closest.el : closest.el.nextElementSibling;
  }
})();