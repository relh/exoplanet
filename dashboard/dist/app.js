const info={
 '80387959':{i:0,priority:'Highest follow-up priority',period:'4.19217-day signal',description:'Dip depth by observing sector. Each point is a joint fit of the fixed transit window and local baselines.',strength:'Dips occur in all six tested sectors, including two recoveries at previously predicted times. No coherent odd/even depth difference or secondary eclipse at half phase was found.',limits:'Image fits give inconsistent source positions. Recent depths are shallower, but observing epoch and pipeline differences are confounded. The sector 100 depth is 582 ±133 ppm after adjustment (previous uncertainty: 99 ppm). An eclipse of 1.1–1.4% on TIC 80387965 could reproduce the dip under generous aperture-throughput assumptions; no such eclipse has been observed.',caption:'Points: fitted depth. Bars: approximate time-averaging noise-adjusted uncertainty; not calibrated confidence intervals. SPOC and QLP use different epochs here; this is not a controlled pipeline comparison.'},
 '402358350':{i:1,priority:'Recurring signal',period:'~11.76954-day signal',description:'Combined depth across twelve baseline variants. All twelve analyses use the same eight events.',strength:'All eight usable events remain positive under every tested baseline variant. Combined depths span 590–659 ppm, with approximate adjusted uncertainties of 41–93 ppm.',limits:'The predefined timing test failed. Source attribution and possible contamination from stellar pulsations remain unresolved. A 21–23% eclipse on TIC 1918682563 could reproduce the dip under generous aperture-throughput assumptions; no such eclipse has been observed.',caption:'Points: combined fitted depth. Bars: approximate time-averaging noise-adjusted uncertainty; not calibrated confidence intervals. D is the fixed 0.144-day duration. SAP = aperture flux; PDCSAP = corrected flux.'}
};

let data;
let selected = '80387959';
const el = id => document.getElementById(id);
const color = group => ['QLP', 'PDCSAP'].includes(group) ? '#f0bf7a' : '#8be2ca';

function drawChart(rows) {
  const width = Math.max(240, el('chart').clientWidth - (innerWidth <= 950 ? 36 : 52));
  const compact = width < 510;
  const rowHeight = compact ? 76 : 43;
  const top = compact ? 38 : 22;
  const height = top + rows.length * rowHeight + 40;
  const left = compact ? 10 : (selected === '80387959' ? 86 : 165);
  const right = width - (compact ? 16 : 105);
  const x = value => left + value / 1400 * (right - left);
  const parts = [`<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Dip depths with approximate noise-adjusted uncertainties. Exact values in the measurement table.">`];
  for (let value = 0; value <= 1400; value += 350) {
    parts.push(`<line x1="${x(value)}" y1="${top-8}" x2="${x(value)}" y2="${height-46}" stroke="#26313e" stroke-dasharray="${value ? '2 5' : '0'}"/><text x="${x(value)}" y="${height-25}" text-anchor="middle">${value.toLocaleString()}</text>`);
  }
  rows.forEach((r, i) => {
    const y = top + i * rowHeight + (compact ? 31 : 9);
    const c = color(r.group);
    const value = `${r.depth.toFixed(0)} ± ${r.error.toFixed(0)}`;
    if (compact) {
      parts.push(`<rect x="0" y="${y-43}" width="${width}" height="34" fill="#111925"/><text x="0" y="${y-26}">${r.label}</text><text x="${width}" y="${y-10}" text-anchor="end" style="fill:${c}">${value}</text>`);
    } else {
      parts.push(`<text x="${left-14}" y="${y+4}" text-anchor="end">${r.label}</text><text x="${width}" y="${y+4}" text-anchor="end" style="fill:${c}">${value}</text>`);
    }
    parts.push(`<g stroke="${c}" stroke-width="2"><line x1="${x(r.depth-r.error)}" y1="${y}" x2="${x(r.depth+r.error)}" y2="${y}"/><path d="M${x(r.depth-r.error)} ${y-5}v10 M${x(r.depth+r.error)} ${y-5}v10"/></g><circle cx="${x(r.depth)}" cy="${y}" r="8" fill="${c}" fill-opacity=".12"/><circle cx="${x(r.depth)}" cy="${y}" r="4" fill="${c}"><title>${r.label}: ${r.depth.toFixed(1)} ± ${r.error.toFixed(1)} ppm</title></circle>`);
  });
  parts.push(`<text x="${(left+right)/2}" y="${height-3}" text-anchor="middle">Dip depth / ppm</text></svg>`);
  el('chart').innerHTML = parts.join('');
}

function render(reset = false) {
  if (!data) return;
  const a = info[selected];
  for (const id of ['priority', 'description', 'strength', 'limits', 'caption']) el(id).textContent = a[id];
  el('title').textContent = selected === '80387959' ? 'Dip depth by observing sector' : 'Dip depth by baseline model';
  document.querySelectorAll('[data-id]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.id === selected)));
  const groups = [...new Set(data[selected].map(x => x.group))];
  if (reset) el('filter').replaceChildren(...['All', ...groups].map(v => new Option(v === 'All' ? 'All products' : v, v)));
  el('legend').innerHTML = groups.map(g => `<span><i class="swatch" style="background:${color(g)}"></i>${g}</span>`).join('');
  const rows = data[selected].filter(r => el('filter').value === 'All' || r.group === el('filter').value);
  drawChart(rows);
  el('measurements').innerHTML = rows.map(r => `<tr><td>${r.label}</td><td>${r.depth.toFixed(1)}</td><td>${r.error.toFixed(1)}</td></tr>`).join('');
  el('report').href = '#vetting';
  el('exofop').href = `https://exofop.ipac.caltech.edu/tess/target.php?id=${selected}`;
  el('figure').src = el('figurelink').href = `evidence-${a.i}.png`;
  el('figure').alt = `Archived scientific diagnostic for TIC ${selected}`;
}

fetch('data.json').then(r => {
  if (!r.ok) throw Error('Data request failed');
  return r.json();
}).then(d => {
  data = d;
  render(true);
}).catch(e => {
  el('title').textContent = 'Measurements unavailable';
  el('chart').textContent = 'Could not load measurements. Reload the page or inspect data.json.';
  console.error(e);
});
document.querySelectorAll('[data-id]').forEach(b => b.onclick = () => {
  selected = b.dataset.id;
  render(true);
  window.dispatchEvent(new CustomEvent('candidatechange', {detail: selected}));
});
el('filter').onchange = () => render();
new ResizeObserver(() => render()).observe(el('chart'));

// Summary links select the corresponding observations before scrolling to them.
document.querySelectorAll('[data-select]').forEach(link => link.addEventListener('click', () => {
  document.querySelector(`[data-id="${link.dataset.select}"]`).click();
}));
