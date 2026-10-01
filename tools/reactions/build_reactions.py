"""Package computed reaction paths into ../../reactions.html.

Input: h3_path.npz + h3_path.json from h3.py. Densities are stored per frame as bytes:
nz*nr bytes of log10 electron density (0-255), then nz*nr bytes of signed spin density (128 = none).
"""
import base64, json
import numpy as np

HARTREE_EV = 27.211386


def pack(npz):
    rho, spin = npz['rho'], npz['spin']               # [nf, nz, nr], atomic units (e/bohr^3)
    lo, hi = -3.6, float(np.log10(rho.max()))
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
        'name': 'H + H₂',
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


rx = {'reactions': [h3()]}
body = open('template.html').read().replace('__RX__', json.dumps(rx, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
head, rest = body.split('</style>', 1)
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head + '</style>\n</head>\n<body>\n' + rest + '\n</body>\n</html>\n')
open('../../reactions.html', 'w').write(doc)
print('wrote ../../reactions.html', len(doc), 'bytes')
