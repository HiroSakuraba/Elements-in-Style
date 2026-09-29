// Self-consistent LDA (exchange + Perdew–Zunger correlation), spherical, non-relativistic atom solver.
// Produces radial functions u_nl(r) = r R_nl(r) for every occupied subshell of every element.
const fs = require('fs');

function makeGrid(Z) {
  const h = 0.0125, x0 = Math.log(1e-7), rmax = 80, N = Math.ceil((Math.log(rmax) - x0) / h) + 1;
  const r = new Float64Array(N); for (let i = 0; i < N; i++) r[i] = Math.exp(x0 + i * h);
  return { h, N, r };
}

function solve(g, V, n, l, Eguess) {
  const { h, N, r } = g, L2 = (l + 0.5) * (l + 0.5), h12 = h * h / 12;
  const w = new Float64Array(N);
  let end = N;
  const integ = E => {
    let nodes = 0; end = N;
    w[0] = Math.pow(r[0], l + 0.5); w[1] = Math.pow(r[1], l + 0.5);
    let fm = L2 + 2 * r[0] * r[0] * (V[0] - E), f0 = L2 + 2 * r[1] * r[1] * (V[1] - E);
    for (let i = 1; i < N - 1; i++) {
      const fp = L2 + 2 * r[i + 1] * r[i + 1] * (V[i + 1] - E);
      if (h12 * fp > 0.3 && fp > f0) { end = i + 1; break; }
      w[i + 1] = (2 * w[i] * (1 + 5 * h12 * f0) - w[i - 1] * (1 - h12 * fm)) / (1 - h12 * fp);
      if (w[i + 1] * w[i] < 0) nodes++;
      if (Math.abs(w[i + 1]) > 1e200) { for (let k = 0; k <= i + 1; k++) w[k] *= 1e-200; }
      fm = f0; f0 = fp;
    }
    return nodes;
  };
  const target = n - l - 1;
  let lo = Math.min(...V.slice(0, 50)) * 0 - 0.6 * (-V[0] * r[0]) ** 2 - 5, hi = 0;
  for (let it = 0; it < 90; it++) {
    const mid = (lo + hi) / 2;
    if (integ(mid) > target) hi = mid; else lo = mid;
    if (hi - lo < 1e-11 * Math.max(1, Math.abs(lo))) break;
  }
  const E = lo; integ(E);
  const u = new Float64Array(N);
  for (let i = 0; i < end; i++) u[i] = Math.sqrt(r[i]) * w[i];
  // trim divergent tail beyond the last true node
  let last = 0, seen = 0;
  for (let i = 1; i < end; i++) if (u[i] * u[i - 1] < 0) { seen++; if (seen === target) last = i; }
  let peak = last;
  for (let i = last; i < end; i++) { if (Math.abs(u[i]) >= Math.abs(u[peak])) peak = i; else break; }
  let cut = end;
  for (let i = peak + 1; i < end - 1; i++) if (Math.abs(u[i + 1]) > Math.abs(u[i])) { cut = i; break; }
  for (let i = cut; i < N; i++) u[i] = 0;
  let norm = 0; for (let i = 0; i < N; i++) norm += u[i] * u[i] * r[i] * h;
  const s = 1 / Math.sqrt(norm); for (let i = 0; i < N; i++) u[i] *= s;
  if (u[peak] < 0) for (let i = 0; i < N; i++) u[i] = -u[i];
  return { E, u };
}

function pzCorr(rs) { // Perdew–Zunger 1981 unpolarized correlation potential
  if (rs >= 1) {
    const g = -0.1423, b1 = 1.0529, b2 = 0.3334, sq = Math.sqrt(rs), den = 1 + b1 * sq + b2 * rs;
    const ec = g / den;
    return ec * (1 + 7 / 6 * b1 * sq + 4 / 3 * b2 * rs) / den;
  }
  const A = 0.0311, B = -0.048, C = 0.0020, D = -0.0116, lr = Math.log(rs);
  return A * lr + (B - A / 3) + 2 / 3 * C * rs * lr + (2 * D - C) / 3 * rs;
}

function atom(Z, occ) {
  const g = makeGrid(Z), { h, N, r } = g;
  const b = 0.8853 * Math.pow(Z, -1 / 3);
  let V = new Float64Array(N);
  for (let i = 0; i < N; i++) { const x = r[i] / b, phi = 1 / ((1 + 0.53625 * x) ** 2); V[i] = -Math.max(Z * phi, 1) / r[i]; }
  let orbs, dV = 1, it = 0;
  for (it = 0; it < 150; it++) {
    orbs = occ.map(o => ({ ...o, ...solve(g, V, o.n, o.l) }));
    // density: 4 pi r^2 rho = sum occ u^2
    const P = new Float64Array(N);
    orbs.forEach(o => { for (let i = 0; i < N; i++) P[i] += o.c * o.u[i] * o.u[i]; });
    const q = new Float64Array(N); // enclosed charge
    for (let i = 1; i < N; i++) q[i] = q[i - 1] + 0.5 * h * (P[i] * r[i] + P[i - 1] * r[i - 1]);
    const outer = new Float64Array(N); // int_r^inf P/r' dr'
    for (let i = N - 2; i >= 0; i--) outer[i] = outer[i + 1] + 0.5 * h * (P[i] + P[i + 1]);
    const Vn = new Float64Array(N);
    for (let i = 0; i < N; i++) {
      const rho = P[i] / (4 * Math.PI * r[i] * r[i]);
      let vxc = 0;
      if (rho > 1e-30) { const rs = Math.cbrt(3 / (4 * Math.PI * rho)); vxc = -Math.cbrt(3 * rho / Math.PI) + pzCorr(rs); }
      let v = -Z / r[i] + q[i] / r[i] + outer[i] + vxc;
      if (v > -1 / r[i]) v = -1 / r[i]; // Latter tail
      Vn[i] = v;
    }
    dV = 0; for (let i = 0; i < N; i++) dV = Math.max(dV, Math.abs((Vn[i] - V[i]) * r[i]));
    const mix = it < 5 ? 0.2 : 0.35;
    for (let i = 0; i < N; i++) V[i] = (1 - mix) * V[i] + mix * Vn[i];
    if (dV < 2e-6) break;
  }
  return { orbs, it, dV, g };
}

const EL = JSON.parse(fs.readFileSync('elements.json', 'utf8'));
const LN = { s: 0, p: 1, d: 2, f: 3 };
const only = process.argv[2] ? process.argv[2].split(',').map(Number) : null;
const out = {};
const NG = 200, XA = Math.log(1e-4), XB = Math.log(40), DX = (XB - XA) / (NG - 1);
for (const e of EL) {
  if (only && !only.includes(e.Z)) continue;
  const occ = e.order.map(s => { const m = s.match(/(\d)([spdf])(\d+)/); return { n: +m[1], l: LN[m[2]], c: +m[3], key: m[1] + m[2] }; });
  const t0 = Date.now();
  const { orbs, it, dV, g } = atom(e.Z, occ);
  const rec = {};
  for (const o of orbs) {
    // resample u(r) on a shared log grid
    const vals = new Array(NG);
    let rbar = 0, norm = 0;
    for (let i = 0; i < g.N; i++) { const d = o.u[i] * o.u[i] * g.r[i] * g.h; norm += d; rbar += d * g.r[i]; }
    for (let k = 0; k < NG; k++) {
      const x = XA + k * DX, fi = (x - Math.log(g.r[0])) / g.h, i = Math.floor(fi), f = fi - i;
      vals[k] = (i < 0 || i >= g.N - 1) ? 0 : o.u[i] * (1 - f) + o.u[i + 1] * f;
    }
    const mx = Math.max(...vals.map(Math.abs)) || 1;
    rec[o.key] = { E: +(o.E * 27.211386).toFixed(3), rbar: +(rbar / norm).toFixed(4), s: mx, q: vals.map(v => Math.round(v / mx * 32767)) };
  }
  out[e.Z] = rec;
  if (only) console.log(e.sym, 'iters', it, 'dV', dV.toExponential(1), Date.now() - t0 + 'ms', Object.entries(rec).map(([k, v]) => `${k} ${(v.E / 27.211386).toFixed(3)}Ha <r>${v.rbar}`).join(' | '));
  else process.stderr.write(`${e.sym}(${it}) `);
}
if (!only) fs.writeFileSync('radial.json', JSON.stringify({ XA, DX, NG, atoms: out }));
