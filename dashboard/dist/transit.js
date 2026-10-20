/* Illustration and descriptive plotting only; no scientific fits in the browser. */
(() => {
  const $ = id => document.getElementById(id);
  const canvas = $('transit-canvas'), ctx = canvas.getContext('2d');
  let catalog, tic = '80387959', playing = false, raf, previous = 0, offset = 0;
  const mint = '#8be2ca', gold = '#f0bf7a', muted = '#a0aec0';
  const text = (label, x, y, size = 12, color = muted, align = 'left') => {
    ctx.font = `${size}px ui-monospace, monospace`; ctx.fillStyle = color; ctx.textAlign = align; ctx.fillText(label, x, y);
  };
  function samples() {
    const d = catalog[tic], sector = $('transit-sector').value;
    return d.series.filter(s => sector === 'all' || String(s.sector) === sector).flatMap(s => s.points);
  }
  function draw() {
    if (!catalog) return;
    const d = catalog[tic], w = canvas.clientWidth, h = canvas.clientHeight, mobile = w < 650;
    const ratio = window.devicePixelRatio || 1;
    if (canvas.width !== Math.round(w*ratio) || canvas.height !== Math.round(h*ratio)) {canvas.width = Math.round(w*ratio); canvas.height = Math.round(h*ratio);}
    ctx.setTransform(ratio,0,0,ratio,0,0);ctx.clearRect(0,0,w,h);
    ctx.fillStyle = '#101823';ctx.fillRect(0,0,w,h);
    text(`TIC ${tic}`,24,25,13,mint);
    text('ILLUSTRATION · HOST UNRESOLVED', mobile?24:w-24,mobile?45:25,mobile?9:11,gold,mobile?'left':'right');
    const cx = w/2, cy = mobile?151:132, radius=70;
    // Appearance is illustrative; radius ratio assumes an undiluted uniform disk.
    const bodyRadius = radius*Math.sqrt(d.reference_depth_ppm/1e6);
    const glow = ctx.createRadialGradient(cx,cy,30,cx,cy,118);
    glow.addColorStop(0,'#ffb45355');glow.addColorStop(1,'#ffb45300');ctx.fillStyle=glow;ctx.fillRect(cx-120,cy-120,240,240);
    const surface=ctx.createRadialGradient(cx-18,cy-22,5,cx,cy,radius);
    surface.addColorStop(0,'#fff2c1');surface.addColorStop(.7,'#f7c56e');surface.addColorStop(1,'#c7883f');
    ctx.fillStyle=surface;ctx.beginPath();ctx.arc(cx,cy,radius,0,2*Math.PI);ctx.fill();
    ctx.save();ctx.beginPath();ctx.arc(cx,cy,radius,0,2*Math.PI);ctx.clip();
    for(let i=0;i<160;i++){const angle=i*2.399963,rr=radius*Math.sqrt(i/160);ctx.fillStyle=i%2?'#ffe9ae18':'#93622712';ctx.beginPath();ctx.arc(cx+Math.cos(angle)*rr,cy+Math.sin(angle)*rr,1.5+(i%4)*.35,0,7);ctx.fill();}ctx.restore();
    const bodyX=cx+offset*2*(radius+bodyRadius);
    ctx.setLineDash([3,6]);ctx.strokeStyle='#8be2ca40';ctx.beginPath();ctx.moveTo(Math.max(20,cx-170),cy);ctx.lineTo(Math.min(w-20,cx+170),cy);ctx.stroke();ctx.setLineDash([]);
    if(bodyX>12&&bodyX<w-12){ctx.fillStyle='#11151c';ctx.beginPath();ctx.arc(bodyX,cy,bodyRadius,0,7);ctx.fill();ctx.strokeStyle=mint;ctx.beginPath();ctx.arc(bodyX,cy,12,0,7);ctx.stroke();}
    text('Central crossing assumed · ring locates body',cx,mobile?248:229,mobile?9:11,muted,'center');
    text(`P ${d.period.toFixed(5)} d  ·  D ${d.duration_hours.toFixed(2)} h`,cx,mobile?267:248,mobile?10:12,mint,'center');
    // Full vertical range contains every displayed sample (no outlier clipping).
    const pts=samples(), span=d.duration_hours*2;
    const maxAbs=Math.max(1000,...pts.map(p=>Math.abs(p[1])))*1.12;
    const top=mobile?316:294,left=mobile?54:74,right=w-24,bottom=h-65;
    const px=x=>left+(x+span)/(2*span)*(right-left);
    const py=y=>top+(maxAbs-y)/(maxAbs*2)*(bottom-top);
    text('BASELINE-SUBTRACTED FLUX / ppm',left,top-18,mobile?9:11,muted);
    ctx.fillStyle='#8be2ca0b';ctx.fillRect(px(-d.duration_hours/2),top,px(d.duration_hours/2)-px(-d.duration_hours/2),bottom-top);
    for(const v of [-1,-.5,0,.5,1]){const y=v*maxAbs;ctx.strokeStyle=v===0?'#62716f':'#26313e';ctx.beginPath();ctx.moveTo(left,py(y));ctx.lineTo(right,py(y));ctx.stroke();text(Math.round(y).toLocaleString(),left-8,py(y)+4,mobile?9:11,muted,'right');}
    for(const v of [-2,-1,0,1,2]){const x=v*d.duration_hours;text(x.toFixed(1),px(x),bottom+20,mobile?10:11,muted,'center');}
    if($('transit-points').checked){ctx.fillStyle='#91aabe55';for(const [x,y] of pts){ctx.beginPath();ctx.arc(px(x),py(y),mobile?1.5:2,0,7);ctx.fill();}}
    const bins=Array.from({length:32},()=>[]);
    for(const p of pts){const i=Math.floor((p[0]+span)/(2*span)*32);if(i>=0&&i<32)bins[i].push(p);}
    for(const bin of bins){if(!bin.length)continue;const x=bin.reduce((s,p)=>s+p[0],0)/bin.length,y=bin.reduce((s,p)=>s+p[1],0)/bin.length;ctx.fillStyle=mint;ctx.beginPath();ctx.arc(px(x),py(y),3.5,0,7);ctx.fill();}
    const cursor=px(offset*d.duration_hours);ctx.strokeStyle=gold;ctx.setLineDash([4,4]);ctx.beginPath();ctx.moveTo(cursor,top);ctx.lineTo(cursor,bottom);ctx.stroke();ctx.setLineDash([]);
    text('Hours from saved dip center', (left+right)/2,bottom+42,mobile?10:12,muted,'center');
    text(`${$('transit-sector').value === 'all' ? 'All sectors' : 'S'+$('transit-sector').value} · ${pts.length.toLocaleString()} samples · 32 mean bins`,(left+right)/2,h-7,mobile?9:11,muted,'center');
    $('transit-time-label').textContent=`${(offset*d.duration_hours).toFixed(2)} h`;
  }
  function stop(){playing=false;cancelAnimationFrame(raf);previous=0;$('transit-play').textContent='Play animation';}
  function frame(time){if(!playing)return;if(previous)offset+=(time-previous)/1000/4;previous=time;if(offset>2)offset=-2;$('transit-time').value=offset;draw();raf=requestAnimationFrame(frame);}
  function choose(){if(!catalog)return;stop();offset=0;$('transit-time').value=0;const d=catalog[tic];$('transit-sector').replaceChildren(new Option('All saved sectors','all'),...d.series.map(s=>new Option(s.label,String(s.sector))));$('transit-source').textContent=d.method;$('transit-assumptions').textContent=`Illustration assumes a central crossing of one undiluted, uniform disk, with radius ratio √depth. Reference depth: ${d.reference_depth_ppm.toFixed(0)} ppm. ${d.reference} Surface texture, path and host are illustrative; no planet radius, orbit orientation or temperature is established.`;draw();}
  $('transit-play').onclick=()=>{if(!catalog)return;if(playing)stop();else{playing=true;$('transit-play').textContent='Pause animation';raf=requestAnimationFrame(frame);}};
  $('transit-time').oninput=()=>{stop();offset=Number($('transit-time').value);draw();};
  $('transit-sector').onchange=draw;$('transit-points').onchange=draw;
  $('transit-download').onclick=()=>{if(!catalog)return;draw();const a=document.createElement('a');a.download=`TIC-${tic}-illustration-and-measurements.png`;a.href=canvas.toDataURL('image/png');a.click();};
  window.addEventListener('candidatechange',e=>{tic=e.detail;choose();});
  new ResizeObserver(draw).observe(canvas);
  fetch('transits.json').then(r=>{if(!r.ok)throw Error('Transit data unavailable');return r.json();}).then(d=>{catalog=d;choose();}).catch(e=>{$('transit-source').textContent='Transit data could not be loaded. Reload to retry.';console.error(e);});
})();
