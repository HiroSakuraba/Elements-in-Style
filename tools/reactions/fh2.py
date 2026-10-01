"""Reaction 2 for the Reactions page: F + H2 -> HF + H (collinear).

Energies: UCCSD(T); densities: UCCSD. Basis aug-cc-pVTZ on F, cc-pVTZ on H (PySCF).
The fluorine 2p hole is held along the axis (the reactive 2-Sigma state) by fixing the
pi occupations in C-inf-v symmetry. For each asymmetric stretch s = r2 - r1 the
sum u = r1 + r2 is relaxed with a parabola fit, which traces the minimum-energy path.
Atoms: F at -r1, Ha at the origin, Hb at +r2.
"""
import json, os, time
import numpy as np
from pyscf import gto, scf, cc, lib
from pyscf.dft import numint

lib.num_threads(2)
BASIS = {'F': 'aug-cc-pvtz', 'H': 'cc-pvtz'}
HARTREE_EV = 27.211386
t0 = time.time()
_last = {}


def solve(r1, r2):
    mol = gto.M(atom=f'F 0 0 {-r1}; H 0 0 0; H 0 0 {r2}', basis=BASIS, spin=1, symmetry='Coov', unit='Angstrom', verbose=0)
    mf = scf.UHF(mol); mf.irrep_nelec = {'E1x': (1, 1), 'E1y': (1, 1)}; mf.conv_tol = 1e-10; mf.max_cycle = 200
    mf.kernel()
    if not mf.converged: mf = mf.newton(); mf.kernel()
    mycc = cc.UCCSD(mf); mycc.conv_tol = 1e-8; mycc.kernel()
    E = mycc.e_tot + mycc.ccsd_t()
    _last.update(mol=mol, mf=mf, cc=mycc, r=(r1, r2))
    return E


def golden(f, a, b, tol):
    g = (np.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a); fc, fd = f(c), f(d)
    while b - a > tol:
        if fc < fd: b, d, fd = d, c, fc; c = b - g * (b - a); fc = f(c)
        else: a, c, fc = c, d, fd; d = a + g * (b - a); fd = f(d)
    x = (a + b) / 2; return x, f(x)


# asymptotes (supermolecule with the third atom 15 A away, so basis and method are consistent)
FAR = 15.0
CK = 'fh2_ckpt'; os.makedirs(CK, exist_ok=True)   # checkpoints, so an interrupted run resumes where it stopped
if os.path.exists(f'{CK}/asym.json'):
    r_h2, E_inf, r_hf, E_prod = json.load(open(f'{CK}/asym.json'))
else:
    r_h2, E_inf = golden(lambda r: solve(FAR, r), 0.70, 0.79, 2e-3)
    r_hf, E_prod = golden(lambda r: solve(r, FAR), 0.88, 0.96, 2e-3)
    json.dump([r_h2, E_inf, r_hf, E_prod], open(f'{CK}/asym.json', 'w'))
print(f'H2 r_eq {r_h2:.4f}  HF r_eq {r_hf:.4f}  reaction energy {(E_prod - E_inf) * HARTREE_EV:.4f} eV  ({time.time() - t0:.0f}s)', flush=True)

NZ, NR = 176, 48
zs = np.linspace(-5.5, 5.5, NZ); rs = np.linspace(0.0, 3.0, NR)
Zg, Rg = np.meshgrid(zs, rs, indexing='ij')
pts = np.stack([Rg.ravel(), np.zeros(Rg.size), Zg.ravel()], axis=1) / 0.529177210903


def snapshot():
    mol, mf, mycc = _last['mol'], _last['mf'], _last['cc']
    da, db = mycc.make_rdm1(); ca, cb = mf.mo_coeff
    Da, Db = ca @ da @ ca.T, cb @ db @ cb.T
    ao = numint.eval_ao(mol, pts)
    ra, rb = numint.eval_rho(mol, ao, Da), numint.eval_rho(mol, ao, Db)
    Sm = mol.intor('int1e_ovlp'); Pa, Pb = mf.make_rdm1()
    labs = np.array([int(l.split()[0]) for l in mol.ao_labels()])
    PSa, PSb = Pa @ Sm, Pb @ Sm
    def mayer(A, B):
        ia, ib = labs == A, labs == B
        return 2 * (np.sum(PSa[np.ix_(ia, ib)] * PSa[np.ix_(ib, ia)].T) + np.sum(PSb[np.ix_(ia, ib)] * PSb[np.ix_(ib, ia)].T))
    return (ra + rb).reshape(NZ, NR).astype(np.float32), (ra - rb).reshape(NZ, NR).astype(np.float32), mayer(0, 1), mayer(1, 2)


S = np.round(np.concatenate([np.arange(-2.8, -1.39, 0.2), np.arange(-1.3, 0.31, 0.1), np.arange(0.4, 2.61, 0.2)]), 3)
frames, us = [], []
for k, s in enumerate(S):
    ck = f'{CK}/frame_{k:02d}.npz'
    if os.path.exists(ck):
        z = np.load(ck); meta = json.loads(str(z['meta'])); us.append(meta.pop('u'))
        frames.append({**meta, 'rho': z['rho'], 'spin': z['spin']}); continue
    E_of = lambda u: solve((u - s) / 2, (u + s) / 2)   # r1 = (u - s)/2, r2 = (u + s)/2
    if len(us) >= 2: ug = us[-1] + (us[-1] - us[-2]) / (S[len(us) - 1] - S[len(us) - 2]) * (s - S[len(us) - 1])
    elif us: ug = us[-1]
    else: ug = abs(s) + 2 * min(r_h2, r_hf)
    lo = abs(s) + 1.2
    ug = max(ug, lo + 0.1)
    h = 0.08
    for _ in range(6):   # parabola through three points; shift the bracket if the minimum is outside it
        e0, e1, e2 = E_of(ug - h), E_of(ug), E_of(ug + h)
        den = e0 - 2 * e1 + e2
        step = h * (e0 - e2) / (2 * den) if den > 0 else (h if e2 < e0 else -h)
        if abs(step) <= h: break
        ug = max(ug + np.clip(step, -2 * h, 2 * h), lo + h)
    u = ug + step
    E = E_of(u)
    if E > e1: u, E = ug, E_of(ug)
    us.append(u)
    rho, spin, bo1, bo2 = snapshot()
    r1, r2 = (u - s) / 2, (u + s) / 2
    frames.append({'s': float(s), 'r1': round(r1, 4), 'r2': round(r2, 4), 'dE': round((E - E_inf) * HARTREE_EV, 5),
                   'bo1': round(float(bo1), 3), 'bo2': round(float(bo2), 3), 'rho': rho, 'spin': spin})
    np.savez(ck, rho=rho, spin=spin, meta=json.dumps({**{k2: v for k2, v in frames[-1].items() if k2 not in ('rho', 'spin')}, 'u': float(u)}))
    print(f's={s:+.2f} r1={r1:.3f} r2={r2:.3f} dE={(E - E_inf) * HARTREE_EV:+.4f} eV bo={bo1:.2f}/{bo2:.2f}  ({time.time() - t0:.0f}s)', flush=True)

np.savez_compressed('fh2_path.npz', zs=zs, rs=rs, s=[f['s'] for f in frames], rho=np.stack([f['rho'] for f in frames]), spin=np.stack([f['spin'] for f in frames]))
json.dump({'reaction': 'F + H2 -> HF + H', 'method': 'UCCSD(T) energies, UCCSD densities; aug-cc-pVTZ (F), cc-pVTZ (H); PySCF; collinear minimum-energy path',
           'r_eq_H2': round(r_h2, 4), 'r_eq_HF': round(r_hf, 4), 'dE_reaction': round((E_prod - E_inf) * HARTREE_EV, 5),
           'frames': [{k: v for k, v in f.items() if k not in ('rho', 'spin')} for f in frames]}, open('fh2_path.json', 'w'), indent=1)
top = max(frames, key=lambda f: f['dE'])
print('barrier (eV):', top['dE'], 'at s', top['s'], ' total', round(time.time() - t0), 's')
