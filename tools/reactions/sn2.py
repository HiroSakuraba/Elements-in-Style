"""Reaction 3 for the Reactions page: Cl- + CH3Cl -> ClCH3 + Cl- (SN2, backside attack, C3v).

Path: for each value of x = r2 - r1 (r1 = C...Cl_a incoming, r2 = C-Cl_b leaving) the rest of the
geometry (r1 + r2, C-H length, umbrella angle) is relaxed with MP2 gradients. At each relaxed
geometry: CCSD(T) energy, CCSD electron density on a 3D grid, the density of the highest
axial (a1) electron pair (the "curly arrow" pair), Mayer C-Cl bond orders, and Becke charges.
Basis aug-cc-pVDZ (PySCF). The reaction is symmetric, so only the first half (x <= 0) is
computed; build_reactions.py mirrors it. Atoms: Cl_a at -z, C at the origin, Cl_b at +z,
H1 in the xz plane (y = 0 is a mirror plane, so only y >= 0 is stored).
"""
import json, os, time
import numpy as np
from scipy.optimize import minimize
from pyscf import gto, scf, mp, cc, lib, dft
from pyscf.dft import numint

lib.num_threads(2)
BASIS, FROZEN, EV, BOHR = os.environ.get('SN2_BASIS', 'aug-cc-pvdz'), 11, 27.211386, 0.529177210903
CK = os.environ.get('SN2_CK', 'sn2_ckpt'); os.makedirs(CK, exist_ok=True)
t0 = time.time()
log = lambda *a: print(*a, f'({time.time() - t0:.0f}s)', flush=True)


def build(r1, r2, rch, th, with_a=True):
    xyz = ([[0, 0, -r1]] if with_a else []) + [[0, 0, 0], [0, 0, r2]]
    for k in range(3):
        p = 2 * np.pi * k / 3
        xyz.append([rch * np.sin(th) * np.cos(p), rch * np.sin(th) * np.sin(p), rch * np.cos(th)])
    return np.array(xyz, float)


def mol_of(xyz, with_a=True):
    sym = (['Cl'] if with_a else []) + ['C', 'Cl', 'H', 'H', 'H']
    return gto.M(atom=[[s, tuple(c)] for s, c in zip(sym, xyz)], basis=BASIS, charge=-1 if with_a else 0, unit='Angstrom', verbose=0)


_dm = {}
def rhf(mol, key):
    mf = scf.RHF(mol); mf.conv_tol = 1e-9; mf.max_cycle = 150
    dm0 = _dm.get(key); mf.kernel(dm0=dm0 if dm0 is not None and dm0.shape[0] == mol.nao else None)
    if not mf.converged: mf = mf.newton(); mf.kernel()
    _dm[key] = mf.make_rdm1(); return mf


def mp2_eg(xyz, with_a=True):
    mf = rhf(mol_of(xyz, with_a), with_a)
    pt = mp.MP2(mf).set(frozen=FROZEN if with_a else FROZEN - 5); pt.kernel()
    return pt.e_tot, pt.nuc_grad_method().kernel() / BOHR      # Hartree, Hartree per Angstrom


def relax(fx, v0, scale):
    """Minimise the MP2 energy over internal variables v (geometry fx(v)); returns v, E."""
    cache = {}
    def fg(w):
        v = w / scale; k = tuple(np.round(v, 10))
        if k not in cache:
            xyz = fx(v); E, g = mp2_eg(xyz, fx.with_a)
            J = np.stack([(fx(v + dv) - fx(v - dv)) / 2e-5 for dv in np.eye(len(v)) * 1e-5], -1)   # d xyz / d v
            cache[k] = (E, np.einsum('ac,acv->v', g, J) / scale)
        return cache[k]
    res = minimize(fg, v0 * scale, jac=True, method='BFGS', options={'gtol': 1.5e-4, 'maxiter': 40})
    v = res.x / scale; return v, fg(res.x)[0]


def ccsd_t(mol, frozen, key):
    mf = rhf(mol, key)
    mycc = cc.CCSD(mf).set(frozen=frozen); mycc.conv_tol = 1e-8; mycc.kernel()
    return mf, mycc, mycc.e_tot + mycc.ccsd_t()


# --- separated reactants: CH3Cl (MP2-relaxed) + Cl- ---
if os.path.exists(f'{CK}/asym.json'):
    asym = json.load(open(f'{CK}/asym.json'))
else:
    f_m = lambda v: build(0, v[0], v[1], v[2], with_a=False); f_m.with_a = False
    vm, _ = relax(f_m, np.array([1.78, 1.087, np.radians(108.5)]), np.array([1.2, 1.8, 1.0]))
    _, _, E_m = ccsd_t(mol_of(f_m(vm), False), FROZEN - 5, False)
    E_cl = ccsd_t(gto.M(atom='Cl 0 0 0', basis=BASIS, charge=-1, verbose=0), 5, 'cl')[2]
    asym = {'r_CCl': vm[0], 'r_CH': vm[1], 'th': float(np.degrees(vm[2])), 'E_inf': E_m + E_cl}
    json.dump(asym, open(f'{CK}/asym.json', 'w'))
E_inf = asym['E_inf']
log(f"CH3Cl: C-Cl {asym['r_CCl']:.4f} A, C-H {asym['r_CH']:.4f} A, H-C-Cl {asym['th']:.2f} deg")

# --- 3D grid (y >= 0 half) ---
NZ, NX, NY = 105, 41, 21
zs, xs, ys = np.linspace(-7.8, 7.8, NZ), np.linspace(-3.0, 3.0, NX), np.linspace(0.0, 3.0, NY)
Z3, Y3, X3 = np.meshgrid(zs, ys, xs, indexing='ij')                     # arrays are [z, y, x]
pts = np.stack([X3.ravel(), Y3.ravel(), Z3.ravel()], 1) / BOHR
rng = np.random.default_rng(1)
P = rng.normal(size=(200, 3)) * 1.5; c3 = np.array([[np.cos(2 * np.pi / 3), -np.sin(2 * np.pi / 3), 0], [np.sin(2 * np.pi / 3), np.cos(2 * np.pi / 3), 0], [0, 0, 1]])


def analyse(mol, mf, mycc):
    da = mycc.make_rdm1(ao_repr=True)
    rho = np.zeros(len(pts)); orb = np.zeros(len(pts))
    nocc = int((mf.mo_occ > 0).sum()); C = mf.mo_coeff[:, :nocc]
    a0 = numint.eval_ao(mol, P / BOHR); a1 = numint.eval_ao(mol, (P @ c3.T) / BOHR)
    v0, v1 = a0 @ C, a1 @ C
    a1sym = np.einsum('pi,pi->i', v0, v1) / np.einsum('pi,pi->i', v0, v0) > 0.9      # unchanged by a 120-degree turn
    i_sig = max(np.where(a1sym)[0], key=lambda i: mf.mo_energy[i])
    for s in range(0, len(pts), 20000):
        ao = numint.eval_ao(mol, pts[s:s + 20000])
        rho[s:s + 20000] = numint.eval_rho(mol, ao, da)
        orb[s:s + 20000] = 2 * (ao @ C[:, i_sig]) ** 2
    Sm = mol.intor('int1e_ovlp'); PS = mf.make_rdm1() @ Sm
    labs = np.array([int(l.split()[0]) for l in mol.ao_labels()])
    mayer = lambda A, B: float(np.sum(PS[np.ix_(labs == A, labs == B)] * PS[np.ix_(labs == B, labs == A)].T))
    # Becke charges from the CCSD density
    try:
        g = dft.gen_grid.Grids(mol); g.level = 3
        tab = g.gen_atomic_grids(mol, g.atom_grid, g.radi_method, g.level, g.prune)
        cl, wl = dft.gen_grid.get_partition(mol, tab, g.radii_adjust, g.atomic_radii, g.becke_scheme, concat=False)
        q = []
        for ia, (cg, wg) in enumerate(zip(cl, wl)):
            r_ = sum(numint.eval_rho(mol, numint.eval_ao(mol, cg[s:s + 20000]), da) @ wg[s:s + 20000] for s in range(0, len(wg), 20000))
            q.append(mol.atom_charge(ia) - r_)
    except Exception as e:
        log('charges failed:', e); q = [np.nan] * mol.natm
    return rho.reshape(NZ, NY, NX).astype(np.float32), orb.reshape(NZ, NY, NX).astype(np.float32), mayer(0, 1), mayer(1, 2), q, float(mf.mo_energy[i_sig])


XS = [-4.2, -3.8, -3.4, -3.0, -2.6, -2.3, -2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0]
if os.environ.get('SN2_TEST'): XS = [-1.4, 0.0]
scale = np.array([0.45, 1.8, 1.0])          # ~sqrt(force constants), so BFGS starts with a sensible step
v_prev = np.array([asym['r_CCl'] + asym['r_CCl'] + 4.2, asym['r_CH'], np.radians(asym['th'])]); us = []
frames = []
for k, x in enumerate(XS):
    ck = f'{CK}/frame_{k:02d}.npz'
    if os.path.exists(ck):
        z = np.load(ck); meta = json.loads(str(z['meta'])); v_prev = np.array(meta.pop('v'))
        frames.append({**meta, 'rho': z['rho'], 'orb': z['orb']}); us.append(v_prev[0]); continue
    fx = lambda v, x=x: build((v[0] - x) / 2, (v[0] + x) / 2, v[1], v[2]); fx.with_a = True
    v0 = v_prev.copy()
    if len(us) >= 2: v0[0] = us[-1] + (us[-1] - us[-2]) / (XS[k - 1] - XS[k - 2]) * (x - XS[k - 1])
    if x == 0.0: v0[2] = np.pi / 2
    v, E_mp2 = relax(fx, v0, scale)
    mol = mol_of(fx(v)); mf, mycc, E = ccsd_t(mol, FROZEN, True)
    rho, orb, bo1, bo2, q, eps = analyse(mol, mf, mycc)
    r1, r2 = (v[0] - x) / 2, (v[0] + x) / 2
    fr = {'s': x, 'r1': round(r1, 4), 'r2': round(r2, 4), 'rch': round(float(v[1]), 4), 'th': round(float(np.degrees(v[2])), 3),
          'dE': round((E - E_inf) * EV, 5), 'bo1': round(bo1, 3), 'bo2': round(bo2, 3), 'qa': round(float(q[0]), 3), 'qb': round(float(q[2]), 3), 'eps': round(eps, 4)}
    np.savez(ck, rho=rho, orb=orb, meta=json.dumps({**fr, 'v': [float(t) for t in v]}))
    frames.append({**fr, 'rho': rho, 'orb': orb}); us.append(v[0]); v_prev = v
    log(f"x={x:+.2f} r1={r1:.3f} r2={r2:.3f} CH={v[1]:.3f} th={np.degrees(v[2]):.1f} dE={fr['dE']:+.4f} eV bo={bo1:.2f}/{bo2:.2f} q={q[0]:+.2f}/{q[2]:+.2f}")

OUT = 'sn2_test' if os.environ.get('SN2_TEST') else 'sn2'
np.savez_compressed(f'{OUT}_path.npz', zs=zs, xs=xs, ys=ys, rho=np.stack([f['rho'] for f in frames]), orb=np.stack([f['orb'] for f in frames]))
json.dump({'reaction': 'Cl- + CH3Cl -> ClCH3 + Cl-', 'method': 'CCSD(T)/aug-cc-pVDZ energies and CCSD densities at MP2/aug-cc-pVDZ relaxed geometries (PySCF)',
           'asym': asym, 'frames': [{k2: v2 for k2, v2 in f.items() if k2 not in ('rho', 'orb')} for f in frames]}, open(f'{OUT}_path.json', 'w'), indent=1)
log('done; complex', min(f['dE'] for f in frames), 'barrier', frames[-1]['dE'])
