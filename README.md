# Elements in Style

An interactive periodic table laid out as a spiral, with a pulsing electron-orbital viewer and a full set of statistics for all 118 elements.

**Live site:** https://hirosakuraba.github.io/Elements-in-Style/

## What it does

- **Spiral table.** Each turn of the spiral is one period, winding outward from hydrogen at the center. Elements in the same group sit on the same ray. The lanthanides and actinides branch off between groups 2 and 3 into two outer arcs, in the spirit of J. F. Hyde's 1975 chart *The chemical elements and their periodic relationships*.
- **Focus on click.** Click an element and the spiral zooms to it and dims everything outside its chemical family. You can scroll or pinch to zoom, drag to pan, use ← / → to step through atomic numbers, or pick from the element menu.
- **Place in the table.** Each element shows its group and period, with buttons to light up its whole group (one ray of the spiral) or trace its period (one turn). A strip compares the outer electrons of every group member, so the repeating pattern is visible at a glance.
- **Color by family or by cosmic origin.** In Cosmic origin mode, each tile of the spiral is split in proportion to where the Solar System's supply of that element was made: the Big Bang, cosmic-ray fission, dying low-mass stars, exploding massive stars, exploding white dwarfs, merging neutron stars, radioactive decay on Earth, or people. The categories follow Jennifer Johnson's *Origin of the Elements* table (Ohio State) and NASA Goddard's version of it.
- **Orbital and nucleus viewer, five ways:**
  - **2D density.** Textbook probability-density slices, |ψ|² in the xz-plane, labeled (n, l, m) — one square for each occupied orbital. **True size** puts all of an atom's orbitals on one scale, so the inner shells shrink to specks as nuclear charge grows. **Fit each** enlarges every orbital to fill its square. **Hydrogen n ≤ 4** shows the classic hydrogen atlas.
  - **3D.** Solid, lit orbital shapes: the surface holding 90% of the electron's probability, in two colors for the two signs of the wavefunction. A subshell's orbitals are shown side by side, or one at a time with axes. **Whole atom** shows every shell as a nested layer, cut open, with the shells evenly spaced; a partly filled subshell pushes its shell into real bulges.
  - **Elektronium.** The idea comes from the Karlsruhe Physics Course: all of the atom's electrons are drawn as one continuous glowing fluid whose density is the quantum probability density. The fluid is ray-marched on the GPU and can be cut open. **Layers** shows how much fluid sits at each distance, so the shells glow as separate layers.
    **Excite** follows the outermost electron as it absorbs light, jumps to a higher orbital, and falls back. While the electron is between the two states, its Elektronium sloshes back and forth at the light's frequency, slowed down roughly 10¹⁴–10¹⁵ times; once it settles in either state, it holds still. The panel shows the transition (for example sodium 3s → 3p), the model's wavelength, and the measured wavelength of that spectral line where it is well known, with a swatch of the light's color.
  - **Shells.** No point electrons. Each shell is a tinted layer of Elektronium, and a radial density graph shows one hump per shell (area = electron count). **Replay filling** pours the electrons in, in the order subshells fill.
  - **Nucleus.** Every proton (red) and neutron (blue-grey) packed at true relative size, from hydrogen's lone proton to about 300 nucleons. **Cut open** shows the inside. Below it: the neutron-to-proton ratio, the nuclear radius and how many times smaller it is than the atom, the binding energy per nucleon from measured masses, and a strip of every isotope to switch between.
  - All views pulse. Pulsing can be switched off, and it stops automatically if your system asks for reduced motion.
- **Honest numbers.** Values are measured unless tagged **calc** (worked out on the page), **est** (estimate) or **pred** (predicted for superheavy elements). Elements with several solid forms get a switch, so carbon shows graphite and diamond separately, and phosphorus, sulfur, selenium and tin show their forms too. Arsenic's sublimation and helium's refusal to freeze are explained instead of shown as contradictory numbers.
- **Statistics drop-downs:**
  - Physical and thermal: melting and boiling point, density, heat capacity, conductivity, crystal structure.
  - Atomic: radii, electronegativity, electron affinity, oxidation states, and a chart of successive ionization energies.
  - Magnetism: unpaired electrons, ground-state term, spin-only and free-atom magnetic moments, bulk magnetic order, nuclear moments.
  - Isotopes: every known isotope with abundance, half-life, spin, magnetic moment, decay modes and quark counts.
  - Quarks and nucleons: up, down and total quark counts for any isotope you pick, and the share of the atom's mass that comes from the quarks' own rest mass (about 1%).
  - Electron configuration, with orbital box diagrams and per-subshell orbital energies and radii.


- **Cosmic origin panel.** For each element: a bar of its origin shares, what each process is, where Earth's supply differs (most helium and argon on Earth come from radioactive decay in rocks), and a short note.
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

The results reproduce the well-known features of real atoms. Iron's 3d orbital sits inside its 4s, and the 4f orbitals of the lanthanides pull in tight below the 5s and 5p shells. The same potential also gives each atom's lowest allowed excited orbital for the Excite view. Wavelengths computed from these single-electron energies are approximate: hydrogen is exact and lithium is within about 2%, but heavier atoms drift, so the page shows the measured wavelength alongside. The resulting wavefunctions ship inside the page.

The calculation is non-relativistic, so values for the heaviest elements (roughly gold and beyond) are approximate.

## Data sources

- Element and isotope properties come from the [mendeleev](https://github.com/lmmentel/mendeleev) Python package, which compiles NIST, NUBASE, CRC and other references. Values for elements past fermium are mostly predictions.
- Ground-state term symbols and free-atom magnetic moments are estimated with Hund's rules. A few elements, such as cerium and thorium, are known exceptions.
- The spiral's layout is inspired by J. F. Hyde's 1975 chart, as reproduced by Jeremy Sachs (2016).

## Where the origin shares come from

Johnson's chart was assembled by hand from the nucleosynthesis literature, and no numeric table was published with it. `tools/origin.py` assembles the shares in the same way: light elements from Big Bang, cosmic-ray and stellar yields; the iron peak split between core-collapse and white-dwarf supernovae; and for elements beyond iron, the Solar System's slow-neutron-capture shares (after Bisterzo et al. 2014 and Prantzos et al. 2020) credited to dying low-mass stars (or massive stars for the weak s-process), with the rapid-neutron-capture remainder credited to merging neutron stars, as Johnson does. The numbers are approximate, and the page says so.

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
python3 origin.py             # cosmic origin shares -> origin.json
python3 allotropes.py         # phase fixes and allotropes -> allotropes.json
python3 build.py              # template.html + data -> ../index.html
```

## Project layout

```
index.html              the whole site (HTML, CSS, JS and embedded data)
tools/template.html     page source before the data is embedded
tools/extract_elements.py
tools/lda_atoms.js
tools/history.py        discovery history, earlier names and fun facts for all 118 elements
tools/origin.py         cosmic-origin shares, reaction text and notes for all 118 elements
tools/allotropes.py     phase fixes and allotropes (graphite/diamond, white/red/black phosphorus, …)
tools/build.py
.nojekyll               tells GitHub Pages to serve files as-is
```

By Benjamin John Schulz. Released under the MIT License (see `LICENSE`).
