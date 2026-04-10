// main.js
(function () {
  const ruta = window.location.pathname;
  document.querySelectorAll('nav a').forEach(a => {
    if (a.getAttribute('href') === ruta) a.classList.add('activo');
  });
})();

function initSliders() {
  document.querySelectorAll('input[type="range"]').forEach(s => {
    const rv = s.closest('.rw')?.querySelector('.rv');
    if (!rv) return;
    const actualizar = () => {
      const v = parseFloat(s.value);
      rv.textContent = (s.dataset.pct === '1')
        ? (v * 100).toFixed(0) + '%'
        : v;
    };
    actualizar();
    s.addEventListener('input', actualizar);
  });
}

function toast(msg, tipo) {
  let wrap = document.querySelector('.toasts');
  if (!wrap) {
    wrap = document.createElement('div');
    wrap.className = 'toasts';
    document.body.appendChild(wrap);
  }
  const t = document.createElement('div');
  t.className = 'toast' + (tipo ? ' ' + tipo : '');
  t.textContent = msg;
  wrap.appendChild(t);
  setTimeout(() => {
    t.style.opacity = '0';
    t.style.transition = 'opacity .3s';
    setTimeout(() => t.remove(), 300);
  }, 3000);
}

const fmt      = (n, d) => parseFloat(n).toFixed(d !== undefined ? d : 2);
const pct      = (n)    => fmt(n, 1) + '%';
const horaFmt  = (h)    => { const hh = parseInt(h); return (hh % 12 || 12) + ':00 ' + (hh < 12 ? 'AM' : 'PM'); };
const colorApt = (v)    => v >= 0.75 ? 'var(--verde)' : v >= 0.45 ? 'var(--amarillo)' : 'var(--rojo)';

function exportCSV(tablaId, nombre) {
  const filas = Array.from(document.getElementById(tablaId)?.querySelectorAll('tr') || []);
  if (!filas.length) return;
  const csv = filas
    .map(f => Array.from(f.querySelectorAll('th,td')).map(c => '"' + c.innerText + '"').join(','))
    .join('\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' }));
  a.download = nombre;
  a.click();
  toast('CSV descargado');
}

document.addEventListener('DOMContentLoaded', initSliders);