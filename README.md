# Elements in Style

An interactive periodic table laid out as a spiral, with a pulsing electron-orbital viewer and a full set of statistics for all 118 elements.

**Live site:** https://hirosakuraba.github.io/Elements-in-Style/

## What it does

- **Spiral table.** Each turn of the spiral is one period, winding outward from hydrogen at the center. Elements in the same group sit on the same ray. The lanthanides and actinides branch off between groups 2 and 3 into two outer arcs, in the spirit of J. F. Hyde's 1975 chart *The chemical elements and their periodic relationships*.
- **Focus on click.** Click an element and the spiral zooms to it and dims everything outside its chemical family. You can scroll or pinch to zoom, drag to pan, use ← / → to step through atomic numbers, or pick from the element menu.
- **Orbital viewer, three ways:**
  - **2D density.** Textbook probability-density slices, |ψ|² in the xz-plane, labeled (n, l, m) — one square for each occupied orbital. **True size** puts all of an atom's orbitals on one scale, so the inner shells shrink to specks as nuclear charge grows. **Fit each** enlarges every orbital to fill its square. **Hydrogen n ≤ 4** shows the classic hydrogen atlas.
  - **3D.** A rotating point cloud of the real orbitals (px, dxy and so on), colored by subshell and by the sign of the wavefunction.
  - **Shells.** The classic Bohr-style count of electrons in shells K through Q.
  - All three views pulse. Pulsing can be switched off, and it stops automatically if your system asks for reduced motion.
- **Statistics drop-downs:**
  - Physical and thermal: melting and boiling point, density, heat capacity, conductivity, crystal structure.
  - Atomic: radii, electronegativity, electron affinity, oxidation states, and a chart of successive ionization energies.
  - Magnetism: unpaired electrons, ground-state term, spin-only and free-atom magnetic moments, bulk magnetic order, nuclear moments.
  - Isotopes: every known isotope with abundance, half-life, spin, magnetic moment and decay modes.
  - Electron configuration, with orbital box diagrams and per-subshell orbital energies and radii.


- **History panel.** A separate panel for each element gives:
  - when it was discovered, or first synthesized for man-made elements
  - who found it, where, and how
  - earlier and alternative names, such as glucinium, columbium, hahnium and the ununoctium-style placeholders
  - where its name comes from
  - a fun fact
  - a timeline placing it among all 118 elements

## How the orbitals are computed

The angular shape of an orbital (the clover of a d orbital, say) is the same in every atom, because it comes from the atom's spherical symmetry. The element changes the radial part: how large the orbital is, where its nodal rings fall, and how far it reaches toward the nucleus.

To get that radial part right for each element, `tools/lda_atoms.js` solves the atom self-consistently:

- It uses density-functional theory in the local-density approximation: Slater exchange plus Perdew–Zunger correlation, with Latter's tail correction.
- The radial Schrödinger equation is integrated with the Numerov method on a logarithmic grid.
- The starting potential is Thomas–Fermi.

The results reproduce the well-known features of real atoms. Iron's 3d orbital sits inside its 4s, and the 4f orbitals of the lanthanides pull in tight below the 5s and 5p shells. The resulting wavefunctions ship inside the page.

The calculation is non-relativistic, so values for the heaviest elements (roughly gold and beyond) are approximate.

## Data sources

- Element and isotope properties come from the [mendeleev](https://github.com/lmmentel/mendeleev) Python package, which compiles NIST, NUBASE, CRC and other references. Values for elements past fermium are mostly predictions.
- Ground-state term symbols and free-atom magnetic moments are estimated with Hund's rules. A few elements, such as cerium and thorium, are known exceptions.
- The spiral's layout is inspired by J. F. Hyde's 1975 chart, as reproduced by Jeremy Sachs (2016).

## Running it

The site is a single self-contained `index.html`, and the only thing it loads from outside is [three.js](https://threejs.org/) from cdnjs. Open the file in a browser, or serve the folder with any static server:

```sh
python3 -m http.server
```

## Rebuilding the data

```sh
cd tools
pip install mendeleev
python3 extract_elements.py   # element and isotope data -> elements.json
node lda_atoms.js             # self-consistent radial wavefunctions -> radial.json (about 30 s)
python3 history.py            # discovery history and fun facts -> history.json
python3 build.py              # template.html + data -> ../index.html
```

## Project layout

```
index.html              the whole site (HTML, CSS, JS and embedded data)
tools/template.html     page source before the data is embedded
tools/extract_elements.py
tools/lda_atoms.js
tools/history.py        discovery history, earlier names and fun facts for all 118 elements
tools/build.py
.nojekyll               tells GitHub Pages to serve files as-is
```

By Benjamin John Schulz. Released under the MIT License (see `LICENSE`).
