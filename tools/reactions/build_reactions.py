"""Package computed reaction paths into ../../reactions.html.

Input: h3_path.* from h3.py and fh2_path.* from fh2.py. Densities are stored per frame as bytes:
nz*nr bytes of log10 electron density (0-255), then nz*nr bytes of signed spin density (128 = none).
"""
import base64, gzip, json, os
import numpy as np

HARTREE_EV = 27.211386


def pack(npz, cap=None):
    rho, spin = npz['rho'], npz['spin']               # [nf, nz, nr], atomic units (e/bohr^3)
    lo, hi = -3.6, float(np.log10(min(rho.max(), cap or 1e9)))   # cap: let a heavy atom's core saturate
    rb = np.clip((np.log10(np.maximum(rho, 1e-12)) - lo) / (hi - lo), 0, 1)
    # spin: signed log scale so the small opposite-spin patch on the middle atom still shows
    smax = float(np.abs(spin).max()); sfloor = -2.7
    mag = np.clip((np.log10(np.maximum(np.abs(spin), 1e-12)) - sfloor) / (np.log10(smax) - sfloor), 0, 1)
    sb = 128 + np.sign(spin) * mag * 127
    nf = rho.shape[0]; out = bytearray()
    for f in range(nf):
        out += np.round(rb[f] * 255).astype(np.uint8).tobytes()
        out += np.clip(np.round(sb[f]), 1, 255).astype(np.uint8).tobytes()
    zs, rs = npz['zs'], npz['rs']
    return {'b64': base64.b64encode(bytes(out)).decode(), 'nz': len(zs), 'nr': len(rs), 'nf': nf,
            'z0': float(zs[0]), 'z1': float(zs[-1]), 'r1': float(rs[-1])}


def h3():
    npz = np.load('h3_path.npz'); meta = json.load(open('h3_path.json'))
    fr = meta['frames']
    ts = max(fr, key=lambda f: f['dE'])
    bar = ts['dE']
    frames = [{'x': f['s'], 'dE': f['dE'], 'r1': f['r1'], 'r2': f['r2'], 'bo1': f['bo1'], 'bo2': f['bo2']} for f in fr]
    return {
        'name': 'H + H₂', 'id': 'h-h2', 'group': 'Chemical',
        'equationHTML': 'H<sub>a</sub>–H<sub>b</sub> + H<sub>c</sub> → H<sub>a</sub> + H<sub>b</sub>–H<sub>c</sub>',
        'summary': 'The simplest chemical reaction there is: a hydrogen atom swaps partners with a hydrogen molecule. Three protons and three electrons, so it can be computed almost exactly.',
        'grid': pack(npz), 'frames': frames,
        'atoms': [{'label': 'H', 'sub': 'a', 'zKey': 'r1', 'sign': -1}, {'label': 'H', 'sub': 'b'}, {'label': 'H', 'sub': 'c', 'zKey': 'r2', 'sign': 1}],
        'bonds': [{'key': 'bo1', 'a': 0, 'b': 1, 'label': 'H<sub>a</sub>–H<sub>b</sub>', 'dist': 'r1'}, {'key': 'bo2', 'a': 1, 'b': 2, 'label': 'H<sub>b</sub>–H<sub>c</sub>', 'dist': 'r2'}],
        'ends': ['H₂ + H', 'H + H₂'],
        'xLabel': 'reaction progress →',
        'phases': [
            {'from': -99, 'jump': -2.6, 'title': 'A lone atom approaches',
             'text': 'On the left, H<sub>a</sub> and H<sub>b</sub> share a pair of electrons: that pair is the bond. On the right, H<sub>c</sub> arrives with a single unpaired electron, shown in green. Far apart, they barely notice each other.'},
            {'from': -1.05, 'jump': -0.8, 'title': 'The clouds push back',
             'text': 'Once the clouds overlap, the energy climbs. The molecule already holds a full pair, and a third electron can\'t join it (the Pauli exclusion principle), so the atom has to pry the old bond loose. The H<sub>a</sub>–H<sub>b</sub> bond starts to stretch.'},
            {'from': -0.25, 'jump': 0.0, 'title': 'Transition state',
             'text': f'The top of the hill, {bar:.2f} eV up. All three atoms sit in a line, {ts["r1"]:.2f} Å apart, and each link is about half a bond. The unpaired electron is now shared between the two end atoms, and the middle atom even picks up a faint opposite spin (pink).'},
            {'from': 0.25, 'jump': 0.8, 'title': 'Rolling downhill',
             'text': 'Past the top, the new H<sub>b</sub>–H<sub>c</sub> bond takes over and the old one gives way. The energy that went into climbing comes back as H<sub>a</sub> is pushed off, and now H<sub>a</sub> carries the unpaired electron.'},
            {'from': 1.05, 'jump': 2.6, 'title': 'Partners swapped',
             'text': 'A new molecule and a free atom, with exactly the starting energy, because the products are the same kind of thing as the reactants. Chemists tell them apart with deuterium (heavy hydrogen): D + H₂ → HD + H.'},
        ],
        'numbers': [
            ['Barrier (this calculation)', f'{bar:.3f} eV'],
            ['Barrier, best published surface', '0.417 eV <span class="vt">ref</span>'],
            ['Same barrier in kJ/mol', f'{bar * 96.485:.0f} kJ/mol'],
            ['H–H spacing at the top', f'{ts["r1"]:.3f} Å'],
            ['H₂ bond length (calc.)', f'{meta["r_eq_H2"]:.3f} Å'],
            ['H₂ bond length (measured)', '0.741 Å'],
            ['Energy released overall', '0 eV (same products)'],
            ['Frames computed', str(len(frames))],
        ],
        'method': ('<b>How this was computed.</b> Coupled-cluster theory (UCCSD) with the cc-pVTZ basis set, run in PySCF. '
                   'At each step the old and new bond lengths were set, then the atoms were allowed to settle into the lowest-energy '
                   'spacing, which traces the minimum-energy path. The densities are the real coupled-cluster electron densities. '
                   f'The barrier lands {abs(bar - 0.417) * 1000:.0f} meV above the best published value (Mielke, Garrett and Peterson, 2002); '
                   'most of the gap comes from the finite basis set. This reaction also has history: London, Eyring and Polanyi built '
                   'the first potential-energy surface for it in 1931, the start of the field of reaction dynamics.'),
    }


def fh2():
    npz = np.load('fh2_path.npz'); meta = json.load(open('fh2_path.json'))
    fr = meta['frames']; ts = max(fr, key=lambda f: f['dE']); bar = ts['dE']; dEr = fr[-1]['dE']
    frames = [{'x': f['s'], 'dE': f['dE'], 'r1': f['r1'], 'r2': f['r2'], 'bo1': f['bo1'], 'bo2': f['bo2']} for f in fr]
    x_ts = ts['s']
    x_hand = next(f['s'] for f in fr if f['bo1'] > f['bo2'])          # first frame where the new bond is the stronger one
    x_out = next(f['s'] for f in fr if f['dE'] < 0.75 * dEr)           # most of the energy already released
    return {
        'name': 'F + H₂', 'id': 'f-h2', 'group': 'Chemical',
        'equationHTML': 'F + H<sub>a</sub>–H<sub>b</sub> → F–H<sub>a</sub> + H<sub>b</sub>',
        'summary': 'Fluorine, the most reactive element, strips a hydrogen atom off a hydrogen molecule. A tiny barrier and a big payoff: the new H–F bond is far stronger than the H–H bond it replaces.',
        'grid': pack(npz, cap=2.0), 'frames': frames,
        'atoms': [{'label': 'F', 'zKey': 'r1', 'sign': -1, 'dot': 6}, {'label': 'H', 'sub': 'a'}, {'label': 'H', 'sub': 'b', 'zKey': 'r2', 'sign': 1}],
        'bonds': [{'key': 'bo1', 'a': 0, 'b': 1, 'label': 'F–H<sub>a</sub>', 'dist': 'r1'}, {'key': 'bo2', 'a': 1, 'b': 2, 'label': 'H<sub>a</sub>–H<sub>b</sub>', 'dist': 'r2'}],
        'ends': ['F + H₂', 'HF + H'],
        'xLabel': 'reaction progress →',
        'phases': [
            {'from': -99, 'jump': fr[0]['s'], 'title': 'Fluorine closes in',
             'text': 'Fluorine has nine electrons, one short of a full outer shell. The gap sits in a p orbital pointing straight at the molecule, so the unpaired electron (green) shows up as a lobe along the axis. The H<sub>a</sub>–H<sub>b</sub> pair on the right is a normal, full bond.'},
            {'from': round(x_ts - 0.35, 3), 'jump': x_ts, 'title': 'An early, tiny barrier',
             'text': f'The top of the hill comes early and is low: just {bar:.2f} eV. Fluorine is still {ts["r1"]:.2f} Å away, and the H–H bond has barely stretched ({ts["r2"]:.2f} Å, against 0.74 Å at rest). Fluorine pulls so hard that the reaction is almost downhill from the start.'},
            {'from': round(x_hand - 0.05, 3), 'jump': x_hand, 'title': 'The electron hand-off',
             'text': 'Now the H–H pair comes apart. One of its electrons pairs up with fluorine\'s missing one to make the new F–H bond, and the other stays behind on H<sub>b</sub>, which becomes the new unpaired electron (green moves to the right).'},
            {'from': round(x_out, 3), 'jump': fr[-1]['s'], 'title': 'Energy released',
             'text': f'Hydrogen fluoride and a free hydrogen atom, {abs(dEr):.2f} eV lower than where we started. Because the barrier came early, most of that energy ends up as vibration in the new H–F bond. That vibrating HF is what powers the hydrogen-fluoride chemical laser.'},
        ],
        'numbers': [
            ['Barrier (this calculation)', f'{bar:.3f} eV'],
            ['Collinear barrier, best published', '0.072 eV <span class="vt">ref</span>'],
            ['Energy released (calc.)', f'{abs(meta["dE_reaction"]):.3f} eV'],
            ['From measured bond energies', '1.37 eV <span class="vt">ref</span>'],
            ['F–H distance at the top', f'{ts["r1"]:.2f} Å <span class="vt">ref 1.57</span>'],
            ['H–H distance at the top', f'{ts["r2"]:.3f} Å <span class="vt">ref 0.763</span>'],
            ['HF bond length (calc.)', f'{meta["r_eq_HF"]:.3f} Å'],
            ['HF bond length (measured)', '0.917 Å'],
        ],
        'method': ('<b>How this was computed.</b> Energies from coupled-cluster theory with perturbative triples, UCCSD(T); densities from UCCSD. '
                   'Basis sets: aug-cc-pVTZ on fluorine, cc-pVTZ on hydrogen (PySCF). The fluorine p-hole is held along the axis, which is the state that reacts. '
                   'Each frame relaxes the atoms to the lowest-energy spacing, tracing the minimum-energy path. '
                   'The reference barrier is the collinear value of Cardoen, Simons and Gdanitz (2006); the true lowest path is slightly bent and about 0.015 eV lower, '
                   'and fluorine\'s spin-orbit coupling adds back roughly the same amount. '
                   'This was the showcase reaction of the crossed-molecular-beam experiments that shared the 1986 Nobel Prize in Chemistry (Herschbach, Lee and Polanyi).'),
    }


def hoyle():
    """Triple-alpha process through the Hoyle state. Nothing is computed here: energies, lifetimes and
    branching are measured values (ENSDF / TUNL evaluations); the animation timeline is a sketch."""
    keys = [(0, 7.275), (0.08, 7.275), (0.10, 7.367), (0.16, 7.367), (0.20, 7.275), (0.27, 7.275), (0.30, 7.367), (0.34, 7.367),
            (0.42, 7.654), (0.59, 7.654), (0.61, 4.439), (0.78, 4.439), (0.80, 0.0), (1.0, 0.0)]
    xs = np.linspace(0, 1, 201)
    frames = [{'x': round(float(x), 4), 'dE': round(float(np.interp(x, *zip(*keys))), 4)} for x in xs]
    he = '2 protons + 2 neutrons'
    return {
        'name': '3 ⁴He → ¹²C', 'id': 'hoyle', 'group': 'Nuclear', 'kind': 'nuclear', 'dur': 22,
        'equationHTML': '3 <sup>4</sup>He → <sup>12</sup>C* → <sup>12</sup>C + 2<span style="font-family:var(--f-body)">γ</span>',
        'summary': 'How stars make carbon: three helium nuclei fuse in a red giant\'s core. It only works because carbon-12 has an energy level, the Hoyle state, in just the right place.',
        'frames': frames, 'phases': [
            {'from': 0, 'jump': 0.05, 'title': 'Two helium nuclei meet',
             'text': 'Deep in a red giant, at about 100 million kelvin, helium nuclei (two protons and two neutrons each, also called alpha particles) slam into each other all the time. Two of them can stick together as beryllium-8.'},
            {'from': 0.15, 'jump': 0.19, 'title': 'Beryllium-8 falls apart',
             'text': 'Beryllium-8 is slightly heavier than two helium nuclei, by 92 keV, so it splits again in about 10<sup>−16</sup> s. Because pairs keep forming and splitting, there is always a tiny amount around: roughly one beryllium-8 for every billion helium nuclei.'},
            {'from': 0.3, 'jump': 0.36, 'title': 'A third one arrives in time',
             'text': 'Once in a while a third helium nucleus hits a beryllium-8 before it breaks. Together they carry 7.367 MeV more energy than ordinary carbon-12. That is 287 keV short of the Hoyle state, so it takes a fast collision from the star\'s heat to land right on it. When it does, the three lock into resonance, and the reaction runs vastly faster than it would without that energy level.'},
            {'from': 0.42, 'jump': 0.5, 'title': 'The Hoyle state',
             'text': 'An excited carbon-12: three helium clusters held loosely together, more like a bent chain than a tight triangle. It is fragile. About 9,996 times in 10,000 it simply falls back into three helium nuclei (the faint outlines).'},
            {'from': 0.58, 'jump': 0.62, 'title': 'Two gamma rays',
             'text': 'The rare exception: it sheds 3.21 MeV as a gamma ray and drops to a compact, spinning carbon-12 (the 2⁺ state, 4.44 MeV). Then a second gamma ray of 4.44 MeV carries off the spin and the rest of the energy.'},
            {'from': 0.8, 'jump': 0.9, 'title': 'Carbon-12',
             'text': 'Ordinary, stable carbon-12. Most of the carbon in the universe, including the carbon in you, was made this way. A second piece of luck helps it survive: oxygen-16 has an energy level just below the carbon-12 + helium-4 energy (7.12 against 7.16 MeV), so carbon is not quickly burned on into oxygen.'},
        ],
        'states': [
            {'from': 0, 'name': 'Helium-4 nuclei', 'rows': [['Energy above carbon-12', '7.275 MeV (three together)'], ['Each is made of', he], ['Lifetime', 'stable']]},
            {'from': 0.09, 'name': 'Beryllium-8', 'rows': [['Energy above carbon-12', '7.367 MeV (with one ⁴He)'], ['Made of', '4 protons + 4 neutrons'], ['Lifetime', '≈ 10⁻¹⁶ s']]},
            {'from': 0.17, 'name': 'Helium-4 nuclei', 'rows': [['Energy above carbon-12', '7.275 MeV (three together)'], ['Each is made of', he], ['Lifetime', 'stable']]},
            {'from': 0.285, 'name': 'Beryllium-8', 'rows': [['Energy above carbon-12', '7.367 MeV (with one ⁴He)'], ['Made of', '4 protons + 4 neutrons'], ['Lifetime', '≈ 10⁻¹⁶ s']]},
            {'from': 0.4, 'name': 'Carbon-12, Hoyle state', 'rows': [['Energy above carbon-12', '7.654 MeV'], ['Spin and parity', '0⁺'], ['Lifetime', '≈ 7 × 10⁻¹⁷ s'], ['Becomes stable carbon', 'about 4 in 10,000']]},
            {'from': 0.6, 'name': 'Carbon-12, first excited state', 'rows': [['Energy above carbon-12', '4.439 MeV'], ['Spin and parity', '2⁺ (spinning)'], ['Lifetime', '≈ 6 × 10⁻¹⁴ s']]},
            {'from': 0.79, 'name': 'Carbon-12', 'rows': [['Energy', '0 (ground state)'], ['Spin and parity', '0⁺'], ['Made of', '6 protons + 6 neutrons'], ['Lifetime', 'stable']]},
        ],
        'numbers': [
            ['Hoyle state energy', '7.654 MeV'],
            ['Hoyle\'s 1953 prediction', '7.68 MeV'],
            ['Above three ⁴He', '379 keV'],
            ['Above ⁸Be + ⁴He', '287 keV'],
            ['⁸Be above two ⁴He', '92 keV'],
            ['Chance it becomes carbon', '≈ 4 in 10,000'],
            ['Gamma rays given off', '3.21 + 4.44 MeV'],
            ['Typical red-giant core', '≈ 100 million K'],
        ],
        'method': ('<b>What is measured and what is sketched.</b> Every energy, lifetime and probability here is a measured value from the nuclear-data evaluations '
                   '(the chance of becoming carbon, about 4 in 10,000, is still being refined; one 2020 experiment found about 6). The temperature panel uses the '
                   'standard narrow-resonance rate, which scales as T<sup>−3</sup> e<sup>−4.40/T₉</sup> (T₉ in billions of kelvin). The nuclei themselves are a sketch: '
                   'helium clusters, with the Hoyle state drawn as the loose "bent arm" found by the first calculation of it from the forces between protons and neutrons '
                   '(Epelbaum, Krebs, Lee and Meißner, 2011–2012, on a supercomputer). Timing is not to scale: each step really takes about 10<sup>−16</sup> s. '
                   '<b>History.</b> Öpik and Salpeter worked out the two-step path through beryllium-8 in 1951–52. In 1953 Fred Hoyle argued that it would still be far too slow '
                   'to make the carbon we see unless carbon-12 had an energy level near 7.68 MeV. Ward Whaling\'s group at Caltech found it that same year, and in 1957 '
                   'Cook, Fowler and the Lauritsens showed it could be made from three helium nuclei. William Fowler shared the 1983 Nobel Prize in Physics for this line of work; Hoyle did not.'),
    }


def pack3d(npz, cap=2.0):
    """3D grid [frame, z, y>=0, x]: log density bytes, then log pair-density bytes of the reacting orbital (128 = none). Gzipped."""
    rho, orb = npz['rho'].astype(np.float32), npz['orb'].astype(np.float32)
    lo, hi = -3.6, float(np.log10(min(rho.max(), cap)))
    rb = np.clip((np.log10(np.maximum(rho, 1e-12)) - lo) / (hi - lo), 0, 1)
    top = float(np.log10(orb.max())); floor = top - 2.4
    ob = 128 + np.clip((np.log10(np.maximum(orb, 1e-12)) - floor) / (top - floor), 0, 1) * 127
    out = bytearray()
    for f in range(rho.shape[0]):
        out += np.round(rb[f] * 255).astype(np.uint8).tobytes(); out += np.round(ob[f]).astype(np.uint8).tobytes()
    zs, xs, ys = npz['zs'], npz['xs'], npz['ys']
    return {'b64': base64.b64encode(gzip.compress(bytes(out), 9)).decode(), 'nz': len(zs), 'ny': len(ys), 'nx': len(xs), 'nh': rho.shape[0],
            'z0': float(zs[0]), 'z1': float(zs[-1]), 'x0': float(xs[0]), 'x1': float(xs[-1])}


def sn2(prefix='sn2'):
    npz = np.load(f'{prefix}_path.npz'); meta = json.load(open(f'{prefix}_path.json'))
    half = meta['frames']; nh = len(half)
    mirror = lambda f: {'x': -f['s'], 'dE': f['dE'], 'r1': f['r2'], 'r2': f['r1'], 'rch': f['rch'], 'th': round(180 - f['th'], 3),
                        'bo1': f['bo2'], 'bo2': f['bo1'], 'qa': f['qb'], 'qb': f['qa']}
    first = [{'x': f['s'], 'dE': f['dE'], 'r1': f['r1'], 'r2': f['r2'], 'rch': f['rch'], 'th': f['th'], 'bo1': f['bo1'], 'bo2': f['bo2'], 'qa': f['qa'], 'qb': f['qb']} for f in half]
    frames = first + [mirror(half[k]) for k in range(nh - 2, -1, -1)]
    ts = half[-1]; cx = min(half, key=lambda f: f['dE']); A = meta['asym']
    return {
        'name': 'Cl⁻ + CH₃Cl', 'id': 'sn2', 'group': 'Chemical',
        'equationHTML': 'Cl<sub>a</sub><sup>−</sup> + CH<sub>3</sub>–Cl<sub>b</sub> → Cl<sub>a</sub>–CH<sub>3</sub> + Cl<sub>b</sub><sup>−</sup>',
        'summary': 'The textbook SN2 reaction: a chloride ion attacks carbon from the back, the old chlorine leaves from the front, and the three hydrogens flip over like an umbrella in the wind.',
        'grid3': pack3d(npz), 'frames': frames, 'tsAt': 0.0, 'release': False, 'barrierText': 'central barrier {} eV',
        'marks': [{'x': cx['s'], 'dE': cx['dE'], 'label': 'complex'}, {'x': -cx['s'], 'dE': cx['dE'], 'label': 'complex'}],
        'overlay': {'btn': 'Reacting pair', 'legend': 'the electron pair that moves (highest σ orbital)'},
        'atoms': [{'label': 'Cl', 'sub': 'a', 'zKey': 'r1', 'sign': -1, 'dot': 6}, {'label': 'C', 'dot': 5}, {'label': 'Cl', 'sub': 'b', 'zKey': 'r2', 'sign': 1, 'dot': 6},
                  {'label': 'H', 'h': 0, 'dot': 3}, {'label': 'H', 'h': 1, 'dot': 3}, {'label': 'H', 'h': 2, 'dot': 3}],
        'bonds': [{'key': 'bo1', 'a': 1, 'b': 0, 'label': 'C–Cl<sub>a</sub>', 'dist': 'r1'}, {'key': 'bo2', 'a': 1, 'b': 2, 'label': 'C–Cl<sub>b</sub>', 'dist': 'r2'},
                  {'fixed': 1, 'a': 1, 'b': 3}, {'fixed': 1, 'a': 1, 'b': 4}, {'fixed': 1, 'a': 1, 'b': 5}],
        'charges': [{'key': 'qa', 'label': 'Cl<sub>a</sub>'}, {'key': 'qb', 'label': 'Cl<sub>b</sub>'}],
        'ends': ['Cl⁻ + CH₃Cl', 'ClCH₃ + Cl⁻'], 'xLabel': 'reaction progress →',
        'phases': [
            {'from': -99, 'jump': frames[0]['x'], 'title': 'Chloride homes in',
             'text': 'Cl<sub>a</sub><sup>−</sup> carries an extra electron. Chloromethane is lopsided too: its chlorine pulls electrons away from the carbon, leaving the carbon\'s back side, between the hydrogens, slightly positive. The ion is drawn straight at it.'},
            {'from': -2.2, 'jump': cx['s'], 'title': 'A loose embrace',
             'text': f'Before any bond changes, the ion settles against the back of the molecule: the ion–dipole complex, {abs(cx["dE"]):.2f} eV lower than where it started. In a gas, where nothing else gets in the way, this complex is real and has been measured.'},
            {'from': -0.75, 'jump': 0.0, 'title': 'Backside attack',
             'text': f'The top of the central barrier. Cl–C–Cl stands in a straight line with both C–Cl bonds stretched to {ts["r1"]:.2f} Å, each about half a bond, and the negative charge is shared equally between the two chlorines. The three hydrogens lie flat. The green pair (the reacting σ orbital) now spans both chlorines with a gap at the carbon.'},
            {'from': 0.15, 'jump': 0.6, 'title': 'The umbrella flips',
             'text': 'Past the top, the hydrogens keep going and fold the other way, like an umbrella turned inside out by the wind. This Walden inversion is why an SN2 reaction flips the handedness of a carbon that has four different groups on it.'},
            {'from': 1.0, 'jump': frames[-1]['x'], 'title': 'Chloride leaves',
             'text': 'Cl<sub>b</sub> drifts off as the new chloride ion, carrying the negative charge, through the mirror-image complex and back to the starting energy. Same molecules, swapped places, and the carbon is now inside out.'},
        ],
        'numbers': [
            ['Complex (this calculation)', f'{cx["dE"]:+.3f} eV'],
            ['Complex, best published', '−0.458 eV <span class="vt">ref</span>'],
            ['Central barrier (calc.)', f'{ts["dE"]:+.3f} eV'],
            ['Central barrier, best published', '+0.090 eV <span class="vt">ref</span>'],
            ['Climb from the complex (calc.)', f'{ts["dE"] - cx["dE"]:.3f} eV'],
            ['Climb from the complex, best published', '0.548 eV <span class="vt">ref</span>'],
            ['C–Cl at the top (calc.)', f'{ts["r1"]:.3f} Å <span class="vt">ref 2.302</span>'],
            ['C–Cl in CH₃Cl (calc.)', f'{A["r_CCl"]:.3f} Å'],
            ['C–Cl in CH₃Cl (measured)', '1.78 Å'],
            ['Same reaction in water', '≈ 1.15 eV barrier'],
        ],
        'method': ('<b>How this was computed.</b> At each step the C–Cl difference was fixed and everything else (the C–Cl sum, the C–H length and the umbrella angle) '
                   'was relaxed with MP2. Then the energy was computed with coupled-cluster theory, CCSD(T), and the density with CCSD, all in the aug-cc-pVDZ basis (PySCF). '
                   'The density is real 3D data, shown on the plane through both chlorines, the carbon and one hydrogen (the other two hydrogens are faded because they sit out of that plane). '
                   'The reaction is its own mirror image, so the second half is the first half reflected. Charges come from dividing the CCSD density among the atoms (Becke partitioning). '
                   'References: focal-point values of Gonzales and co-workers (2005). aug-cc-pVDZ is a small basis set, so the complex comes out a little too deep and the central barrier a little too low; the climb from the complex to the top, where those errors largely cancel, is within 0.04 eV. '
                   '<b>Why water matters.</b> In water the same reaction has a barrier of about 1.15 eV (26 kcal/mol), because water molecules cling to the small chloride ion '
                   'and must be partly stripped away first. The gas-phase double well and the solvent effect were a landmark of computational chemistry (Chandrasekhar, Smith and Jorgensen, 1985).'),
    }


rx = {'reactions': [h3()] + ([fh2()] if os.path.exists('fh2_path.json') else []) + ([sn2(os.environ.get('SN2_PREFIX', 'sn2'))] if os.path.exists(os.environ.get('SN2_PREFIX', 'sn2') + '_path.json') else []) + [hoyle()]}
body = open('template.html').read().replace('__RX__', json.dumps(rx, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
head, rest = body.split('</style>', 1)
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head + '</style>\n</head>\n<body>\n' + rest + '\n</body>\n</html>\n')
open('../../reactions.html', 'w').write(doc)
print('wrote ../../reactions.html', len(doc), 'bytes')
