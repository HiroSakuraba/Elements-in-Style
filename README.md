# Elements in Style

An interactive periodic table laid out as a spiral, with a pulsing electron-orbital viewer and a full set of statistics for all 118 elements.

**Live site:** https://hirosakuraba.github.io/Elements-in-Style/

## What it does

- **Spiral table.** Each turn of the spiral is one period, winding outward from hydrogen at the center. Elements in the same group sit on the same ray. The lanthanides and actinides branch off between groups 2 and 3 into two outer arcs, in the spirit of J. F. Hyde's 1975 chart *The chemical elements and their periodic relationships*.
- **Spiral or table.** One switch animates the same 118 tiles between the spiral and the standard 18-column table, keeping colors, selection and highlights, so the spiral connects to the table people already know.
- **A three-line introduction for every element:** what stands out, why it sits where it does (worked out from its electron configuration), and where you meet it in everyday life.
- **Try this.** Six short discoveries that answer themselves visually: what repeats along a ray, carbon-12 vs carbon-14, why orbitals have dark rings, how a 2D slice relates to the 3D shape, which elements came from colliding neutron stars, and watching an electron make light.
- **Focus on click.** Click an element and the spiral zooms to it and dims everything outside its chemical family. You can scroll or pinch to zoom, drag to pan, use ← / → to step through atomic numbers, or pick from the element menu.
- **Place in the table.** Each element shows its group and period, with buttons to light up its whole group (one ray of the spiral) or trace its period (one turn). A strip compares the outer electrons of every group member, so the repeating pattern is visible at a glance.
- **Color by family or by cosmic origin.** In Cosmic origin mode, each tile of the spiral is split in proportion to where the Solar System's supply of that element was made: the Big Bang, cosmic-ray fission, dying low-mass stars, exploding massive stars, exploding white dwarfs, merging neutron stars, radioactive decay on Earth, or people. The categories follow Jennifer Johnson's *Origin of the Elements* table (Ohio State) and NASA Goddard's version of it.
- **Orbital and nucleus viewer, five ways:**
  - **2D density.** Textbook probability-density slices, |ψ|² in the xz-plane, one square for each occupied orbital, named (3dxz, 4s …) with its quantum numbers. **Compare actual sizes** puts all of an atom's orbitals on one scale, so the inner shells shrink to specks as nuclear charge grows; **Enlarge each shape** fits each orbital to its square. Tap a square to enlarge it with **labels** for the nucleus, the radial and angular nodes, and the most likely distance. **Hydrogen n ≤ 4** shows the classic hydrogen atlas.
  - **3D.** Solid, lit orbital shapes: the surface holding 90% of the electron's probability, in two colors for the two signs of the wavefunction. A subshell's orbitals are shown side by side, or one at a time with axes. With one orbital shown, **Slice plane** cuts through it with a movable plane (xy, xz or yz) and shows the cross-section live beside it; **Sweep** moves the plane back and forth. **Whole atom** shows every shell as a nested layer, cut open, with the shells evenly spaced; a partly filled subshell pushes its shell into real bulges.
  - **Elektronium.** The idea comes from the Karlsruhe Physics Course: all of the atom's electrons are drawn as one continuous glowing fluid whose density is the quantum probability density. The fluid is ray-marched on the GPU and can be cut open. **Layers** shows how much fluid sits at each distance, so the shells glow as separate layers.
    **Excite** follows the outermost electron as it absorbs light, jumps to a higher orbital, and falls back. While the electron is between the two states, its Elektronium sloshes back and forth at the light's frequency, slowed down roughly 10¹⁴–10¹⁵ times; once it settles in either state, it holds still. The panel shows the transition (for example sodium 3s → 3p), the model's wavelength, and the measured wavelength of that spectral line where it is well known, with a swatch of the light's color. The light itself is drawn as a wave packet in its real color (labelled not to scale: a 589 nm wave is about 1,600 times wider than a sodium atom). It flows in, its electric field drives the sloshing, and its energy passes into the atom. On the way back down, the atom radiates like a tiny antenna: wavefronts spread out brightest sideways and dark along the slosh axis. An energy ladder shows the gap the photon carries, and a spectrum strip shows the matching dark absorption line and bright emission line (or points off the end for ultraviolet and infrared lines).
  - **Shells.** No point electrons. Each shell is a tinted layer of Elektronium, and a radial density graph shows one hump per shell (area = electron count). **Replay filling** pours the electrons in, in the order subshells fill.
  - **Nucleus.** Every proton (red) and neutron (blue-grey) packed at true relative size, from hydrogen's lone proton to about 300 nucleons. **Cut open** shows the inside. Below it: the neutron-to-proton ratio, the nuclear radius and how many times smaller it is than the atom, the binding energy per nucleon from measured masses, and a strip of every isotope to switch between. For radioactive isotopes, **decay buttons** play out each of the isotope's real decay modes: alpha (a 2-proton, 2-neutron clump escapes), beta-minus and beta-plus (a neutron turns into a proton or the reverse as a quark changes, throwing out an electron or positron and a ghostly neutrino), electron capture (an inner electron is swallowed and the cloud refills the gap with an X-ray), spontaneous fission, neutron and proton emission, cluster decay, and gamma rays where they follow well-known decays (cobalt-60, caesium-137, technetium-99m and others). The remaining nucleons repack into the daughter nucleus. Each decay shows its equation, the energy released calculated from measured masses (Q value), the daughter with its half-life, and a button to jump to the daughter, so you can follow a decay chain by hand. **Slow motion** plays decays three times slower.
    **Follow the decay chain** traces the most likely decay from nucleus to nucleus until it reaches a stable one, for example uranium-238 → lead-206 in 14 decays (8 alpha, 6 beta) releasing about 51.7 MeV in total. **Play chain** animates every step in the nucleus view while a numbered path hops around the spiral (or table) to show where the element moves.
    **What a half-life means** runs 100 nuclei of the chosen isotope, each decaying at a random moment, with each half-life shown as 2 seconds. A live count is plotted against the expected halving curve, so you can see that single decays are unpredictable but the group halves every half-life.
  - **Expand** enlarges the viewer. All views can pulse; the pulse is a decorative glow (a settled atom's density does not change in time), it can be switched off, and it stops automatically if your system asks for reduced motion.
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

## Reactions

A second page, `reactions.html` (linked from the menu at the top of every page), shows chemical reactions computed with real quantum chemistry:

- **H + H₂ → H₂ + H**, the simplest reaction there is: a hydrogen atom swaps partners with a hydrogen molecule. The barrier is symmetric and the products are the same kind of thing as the reactants.
- **F + H₂ → HF + H**, where fluorine strips a hydrogen off the molecule. The barrier is tiny and early, and about 1.4 eV is released, mostly as vibration of the new HF (the basis of the HF chemical laser).

Each reaction has:

- **2D slice** of the electron density through the three atoms, with the unpaired electron shown in green and a faint opposite spin in pink.
- **Elektronium**: the same density as a glowing 3D cloud you can turn.
- An energy chart you can drag to move through the reaction, with the barrier marked.
- Bond strengths (bond orders) and bond lengths updating as one bond breaks and the other forms.
- Step-by-step narration, from the atom's approach through the transition state to the swapped partners.

Both paths come from coupled-cluster theory in [PySCF](https://pyscf.org/). At each step the atoms settle into their lowest-energy spacing, which traces the minimum-energy path.

- **H + H₂** (UCCSD/cc-pVTZ): the barrier is 0.446 eV, against 0.417 eV from the best published surface (Mielke, Garrett and Peterson, 2002). At the top, each bond is almost exactly half a bond (0.46), with the atoms 0.93 Å apart.
- **F + H₂** (UCCSD(T) energies and UCCSD densities, aug-cc-pVTZ on F and cc-pVTZ on H): the energy released is 1.365 eV, against 1.37 eV from measured bond energies. The barrier is 0.083 eV, against 0.072 eV for the collinear barrier of Cardoen, Simons and Gdanitz (2006), and it sits at their geometry: F–H 1.56 Å and H–H 0.764 Å, against 1.57 and 0.763 Å.

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

Each page is a single self-contained HTML file, and the only thing they load from outside is [three.js](https://threejs.org/) from cdnjs. Open the file in a browser, or serve the folder with any static server:

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
python3 intros.py             # element introductions -> intros.json
python3 build.py              # template.html + data -> ../index.html

cd reactions
pip install pyscf
python3 h3.py                 # H + H2 reaction path and densities (about 7 min on 2 cores)
python3 fh2.py                # F + H2 reaction path and densities (about 65 min on 2 cores; resumes if interrupted)
python3 build_reactions.py    # template.html + paths -> ../../reactions.html
```

## Project layout

```
index.html              the Elements page (HTML, CSS, JS and embedded data)
reactions.html          the Reactions page
tools/template.html     page source before the data is embedded
tools/extract_elements.py
tools/lda_atoms.js
tools/history.py        discovery history, earlier names and fun facts for all 118 elements
tools/origin.py         cosmic-origin shares, reaction text and notes for all 118 elements
tools/allotropes.py     phase fixes and allotropes (graphite/diamond, white/red/black phosphorus, …)
tools/intros.py         one-line introductions for all 118 elements
tools/build.py
tools/reactions/        reaction calculations (h3.py, fh2.py), page source and build_reactions.py
.nojekyll               tells GitHub Pages to serve files as-is
```

By Benjamin John Schulz. Released under the MIT License (see `LICENSE`).
