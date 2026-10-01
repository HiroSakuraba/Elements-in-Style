"""Compute reaction paths and electron densities for the Reactions page (Elements in Style).

Reaction 1: H + H2 -> H2 + H (collinear, the simplest chemical reaction).
Method: UHF reference + UCCSD correlation, cc-pVTZ basis (PySCF). For each value of the asymmetric
stretch s = r1 - r2 the symmetric stretch is relaxed, which traces the minimum-energy path.
Along the path we store total electron density and spin density (where the unpaired electron is)
on a cylindrical (z, rho) grid, plus Mayer bond orders from the UHF density.
"""
import json, sys, time
import numpy as np
from pyscf import gto, scf, cc, lib
from pyscf.dft import numint

lib.num_threads(2)
BASIS = 'cc-pvtz'
ANG = 1.0

def h3(r1, r2):
    # middle atom at the origin; H_a on the left (incoming), H_c on the right (leaving)
    return gto.M(atom=f'H 0 0 {-r1}; H 0 0 0; H 0 0 {r2}', basis=BASIS, spin=1, unit='Angstrom', verbose=0)

def solve(r1, r2, dm0=None):
    mol = h3(r1, r2)
    mf = scf.UHF(mol); mf.conv_tol = 1e-10
    mf.kernel(dm0=dm0)
    if not mf.converged: mf = mf.newton(); mf.kernel()
    mycc = cc.UCCSD(mf); mycc.conv_tol = 1e-8; mycc.kernel()
    return mol, mf, mycc

def energy(r1, r2):
    mol, mf, mycc = solve(r1, r2)
    return mycc.e_tot

def golden(f, a, b, tol=2e-3):
    g = (np.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a); fc, fd = f(c), f(d)
    while b - a > tol:
        if fc < fd: b, d, fd = d, c, fc; c = b - g * (b - a); fc = f(c)
        else: a, c, fc = c, d, fd; d = a + g * (b - a); fd = f(d)
    x = (a + b) / 2; return x, f(x)

t0 = time.time()
# reference: H + H2 far apart
mol_h2 = gto.M(atom='H 0 0 0; H 0 0 0.7414', basis=BASIS, verbose=0)
def e_h2(r):
    m = gto.M(atom=f'H 0 0 0; H 0 0 {r}', basis=BASIS, verbose=0)
    mf = scf.RHF(m).run(); return cc.CCSD(mf).run().e_tot
r_eq, E_h2 = golden(e_h2, 0.70, 0.78, 1e-4)
mfa = scf.UHF(gto.M(atom='H 0 0 0', basis=BASIS, spin=1, verbose=0)).run()
E_h = mfa.e_tot
E_inf = E_h2 + E_h
print(f'H2 r_eq = {r_eq:.4f} A, E(H2) = {E_h2:.6f}, E(H) = {E_h:.6f}', flush=True)

# minimum-energy path: for each asymmetric stretch s = r1 - r2, relax r1 + r2
S = np.concatenate([np.linspace(-2.6, -1.0, 9), np.linspace(-0.9, 0.9, 19), np.linspace(1.0, 2.6, 9)])
path = []
for s in S:
    # r1 = (u + s)/2, r2 = (u - s)/2, with both bonds >= 0.6 A
    lo = abs(s) + 1.2; hi = abs(s) + 2.4
    u, E = golden(lambda u: energy((u + s) / 2, (u - s) / 2), lo, hi, 4e-3)
    r1, r2 = (u + s) / 2, (u - s) / 2
    path.append((s, r1, r2, E))
    print(f's={s:+.2f} r1={r1:.3f} r2={r2:.3f} dE={(E - E_inf) * 27.2114:.4f} eV  ({time.time() - t0:.0f}s)', flush=True)

# densities on a cylindrical grid around the molecular axis
NZ, NR = 160, 48
zs = np.linspace(-5.0, 5.0, NZ); rs = np.linspace(0.0, 3.0, NR)
Zg, Rg = np.meshgrid(zs, rs, indexing='ij')
pts = np.stack([Rg.ravel(), np.zeros(Rg.size), Zg.ravel()], axis=1) / 0.529177210903  # Angstrom -> bohr

frames = []
for (s, r1, r2, E) in path:
    mol, mf, mycc = solve(r1, r2)
    da, db = mycc.make_rdm1()  # MO basis (alpha, beta)
    ca, cb = mf.mo_coeff
    Da = ca @ da @ ca.T; Db = cb @ db @ cb.T
    ao = numint.eval_ao(mol, pts)
    rho_a = numint.eval_rho(mol, ao, Da); rho_b = numint.eval_rho(mol, ao, Db)
    Sm = mol.intor('int1e_ovlp'); Pa, Pb = mf.make_rdm1()
    labs = np.array([int(l.split()[0]) for l in mol.ao_labels()])
    PSa, PSb = Pa @ Sm, Pb @ Sm
    def mayer(A, B):
        ia, ib = labs == A, labs == B
        return 2 * (np.sum(PSa[np.ix_(ia, ib)] * PSa[np.ix_(ib, ia)].T) + np.sum(PSb[np.ix_(ia, ib)] * PSb[np.ix_(ib, ia)].T))
    frames.append({'s': round(float(s), 4), 'r1': round(float(r1), 4), 'r2': round(float(r2), 4), 'dE': round(float((E - E_inf) * 27.211386), 5),
                   'bo1': round(float(mayer(0, 1)), 3), 'bo2': round(float(mayer(1, 2)), 3),
                   'rho': (rho_a + rho_b).reshape(NZ, NR).astype(np.float32), 'spin': (rho_a - rho_b).reshape(NZ, NR).astype(np.float32)})
    print(f'density s={s:+.2f} done ({time.time() - t0:.0f}s)', flush=True)

np.savez_compressed('h3_path.npz', zs=zs, rs=rs, s=[f['s'] for f in frames], rho=np.stack([f['rho'] for f in frames]), spin=np.stack([f['spin'] for f in frames]))
json.dump({'reaction': 'H + H2 -> H2 + H', 'method': f'UCCSD/{BASIS} (PySCF), minimum-energy path, collinear', 'r_eq_H2': round(r_eq, 4),
           'frames': [{k: v for k, v in f.items() if k not in ('rho', 'spin')} for f in frames]}, open('h3_path.json', 'w'), indent=1)
print('barrier (eV):', max(f['dE'] for f in frames), ' total time', round(time.time() - t0), 's')
