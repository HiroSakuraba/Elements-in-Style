import json, math
from fractions import Fraction
from mendeleev import element

UNIT_S = {'asec':1e-18,'fsec':1e-15,'psec':1e-12,'nsec':1e-9,'usec':1e-6,'msec':1e-3,'sec':1,'s':1,
          'minute':60,'hour':3600,'day':86400,'year':3.15576e7,'kyear':3.15576e10,'Myear':3.15576e13,
          'Gyear':3.15576e16,'Tyear':3.15576e19,'Pyear':3.15576e22,'Eyear':3.15576e25,'Zyear':3.15576e28,'Yyear':3.15576e31}
UNIT_LABEL = {'asec':'as','fsec':'fs','psec':'ps','nsec':'ns','usec':'µs','msec':'ms','sec':'s','s':'s','minute':'min',
              'hour':'h','day':'d','year':'y','kyear':'ky','Myear':'My','Gyear':'Gy','Tyear':'Ty','Pyear':'Py',
              'Eyear':'Ey','Zyear':'Zy','Yyear':'Yy'}
LCH = 'SPDFGHIKLMNOQRTUVWXYZ'
LNUM = {'s':0,'p':1,'d':2,'f':3,'g':4}

MAG_NOTES = {
 'Fe':'Ferromagnetic (Curie point 1043 K)','Co':'Ferromagnetic (Curie point 1388 K)',
 'Ni':'Ferromagnetic (Curie point 627 K)','Gd':'Ferromagnetic (Curie point 293 K)',
 'Tb':'Ferromagnetic below 219 K','Dy':'Ferromagnetic below 85 K','Ho':'Ferromagnetic below 20 K',
 'Er':'Ferromagnetic below 19 K','Tm':'Ferromagnetic below 32 K','Cr':'Antiferromagnetic (Néel point 311 K)',
 'Mn':'Antiferromagnetic (α-Mn, Néel point ≈95 K)','Eu':'Antiferromagnetic below 91 K',
 'O':'O₂ is paramagnetic; liquid oxygen clings to a magnet'}

def half(x):
    return str(Fraction(x).limit_denominator(2))

def hund(conf):
    S = 0.0; L = 0; parity = 0; nopen = 0; cap = 0
    for (n, o), N in conf.items():
        l = LNUM[o]; parity += l * N
        k = 2*l + 1
        if N == 0 or N == 2*k: continue
        nopen += N; cap += 2*k
        mls = list(range(l, -l-1, -1))
        up = min(N, k); dn = N - up
        S += (up - dn) / 2
        L += sum(mls[:up]) + sum(mls[:dn])
    L = abs(L)
    if nopen == 0:
        J = 0.0
    elif nopen < cap/2:
        J = abs(L - S)
    else:
        J = L + S
    if J == 0:
        g = 0.0; mu = 0.0
    else:
        g = 1 + (J*(J+1) + S*(S+1) - L*(L+1)) / (2*J*(J+1))
        mu = g * math.sqrt(J*(J+1))
    unpaired = int(round(2*S))
    term = f"{int(round(2*S+1))}{LCH[L] if L < len(LCH) else 'L'+str(L)}{half(J)}"
    return dict(term=term, odd=parity % 2 == 1, S=S, L=L, J=J, gJ=round(g, 4), muJ=round(mu, 3),
                unpaired=unpaired, muS=round(math.sqrt(unpaired*(unpaired+2)), 3))

def fmt_hl(v, u):
    if v is None: return None
    lab = UNIT_LABEL.get(u, u)
    if v >= 1e4 or (v < 1e-2 and v > 0):
        s = f"{v:.3g}"
    else:
        s = f"{v:g}"
    return f"{s} {lab}"

def modes(iso):
    out = []
    dms = iso.decay_modes or []
    for idx, d in enumerate(dms):
        m = d.mode
        if m in ('IS',): continue
        cluster = m[:1].isdigit() and m not in ('2B-', '2B+', '2p', '2n', '3p')
        trace = (m == 'SF' and idx > 0) or cluster
        if trace or d.intensity is None:
            out.append(m + (' (trace)' if trace else ''))
        else:
            rel = {'=':'', '~':'≈', '<':'<', '>':'>'}.get((d.relation or '').strip(), '')
            out.append(f"{m} {rel}{d.intensity:g}%")
    return ', '.join(out)

data = []
for Z in range(1, 119):
    e = element(Z)
    conf = {(n, o): c for (n, o), c in e.ec.conf.items()}
    order = [f"{n}{o}{c}" for (n, o), c in e.ec.conf.items()]
    h = hund(conf)
    isos = []
    stable = 0; longest = None
    for i in sorted(e.isotopes, key=lambda i: i.mass_number):
        st = bool(i.is_stable) and i.abundance is not None
        hs = None
        if i.half_life is not None and i.half_life_unit in UNIT_S:
            hs = i.half_life * UNIT_S[i.half_life_unit]
        if st: stable += 1
        elif hs is not None and (longest is None or hs > longest[0]):
            longest = (hs, i.mass_number, fmt_hl(i.half_life, i.half_life_unit))
        mu = None
        if i.g_factor is not None and i.spin not in (None, '', '0'):
            try:
                I = float(Fraction(i.spin.strip('()')))
                if I > 0: mu = round(i.g_factor * I, 4)
            except Exception: pass
        isos.append([i.mass_number,
                     round(i.mass, 6) if i.mass else None,
                     i.abundance,
                     'stable' if st else fmt_hl(i.half_life, i.half_life_unit),
                     hs if not st else None,
                     (i.spin or '') + (i.parity or '') if i.spin else '',
                     mu,
                     '' if st else modes(i)])
    ie = e.ionenergies or {}
    mp, bp = e.melting_point, e.boiling_point
    if mp is None: phase = None
    elif 298.15 < mp: phase = 'Solid'
    elif bp is not None and 298.15 < bp: phase = 'Liquid'
    else: phase = 'Gas'
    zeff = {}
    for (n, o) in conf:
        try: zeff[f"{n}{o}"] = round(e.zeff(n=n, o=o), 3)
        except Exception: pass
    data.append(dict(
        Z=Z, sym=e.symbol, name=e.name, mass=e.atomic_weight, series=e.series, group=e.group_id,
        period=e.period, block=e.block, econf=e.econf, order=order, zeff=zeff,
        mp=mp, bp=bp, density=e.density, phase=phase,
        en=e.en_pauling, ie1=ie.get(1), ies=[round(ie[k], 3) for k in sorted(ie)][:8] if ie else [],
        ea=e.electron_affinity, radius=e.atomic_radius, cov=e.covalent_radius_pyykko, vdw=e.vdw_radius,
        ox=e.oxistates, cp=e.specific_heat_capacity, k=e.thermal_conductivity, fus=e.fusion_heat,
        vap=e.evaporation_heat, lattice=e.lattice_structure, lat_c=e.lattice_constant,
        disc_year=e.discovery_year, discoverers=e.discoverers, origin=e.name_origin,
        desc=e.description, uses=e.uses, crust=e.abundance_crust, radioactive=bool(e.is_radioactive),
        mag=h, magnote=MAG_NOTES.get(e.symbol), stable=stable,
        longest=[longest[1], longest[2]] if longest and not stable else None,
        isotopes=isos, cpk=e.cpk_color))

s = json.dumps(data, separators=(',', ':'), ensure_ascii=False)
open('elements.json', 'w').write(s)
print(len(s), sum(len(d['isotopes']) for d in data))
for sym in ['Fe', 'Gd', 'Ce', 'U', 'Cr', 'O', 'Pt']:
    d = next(x for x in data if x['sym'] == sym); print(sym, d['mag'], d['phase'], d['longest'], d['stable'])
print(data[91]['isotopes'][30:40])
