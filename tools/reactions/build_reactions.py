"""Package computed reaction paths into ../../reactions.html.

Input: h3_path.* from h3.py and fh2_path.* from fh2.py. Densities are stored per frame as bytes:
nz*nr bytes of log10 electron density (0-255), then nz*nr bytes of signed spin density (128 = none).
"""
import base64, json, os
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


rx = {'reactions': [h3()] + ([fh2()] if os.path.exists('fh2_path.json') else []) + [hoyle()]}
body = open('template.html').read().replace('__RX__', json.dumps(rx, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
head, rest = body.split('</style>', 1)
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head + '</style>\n</head>\n<body>\n' + rest + '\n</body>\n</html>\n')
open('../../reactions.html', 'w').write(doc)
print('wrote ../../reactions.html', len(doc), 'bytes')
