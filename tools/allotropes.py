# Physical-state corrections and allotropes for Elements in Style.
#
# The mendeleev database leaves melting point (and so phase) empty for elements with several solid forms,
# and for helium, and gives arsenic a "melting point" that only applies under pressure. This file supplies
# the corrected state at 25 °C / 1 atm, explanatory notes, and per-form properties for elements whose forms
# differ a lot. Values: CRC Handbook of Chemistry and Physics and the Royal Society of Chemistry periodic table.
import json

A = {
  2: {
    'phase': 'Gas',
    'mpNote': 'Never freezes at normal pressure, even at absolute zero. Solid helium needs about 25 atm (melting ≈ 0.95 K there).',
  },
  33: {
    'phase': 'Solid',
    'mpNote': 'Does not melt at normal pressure: grey arsenic sublimes (turns straight to gas) at 889 K (616 °C). It melts at 1090 K (817 °C) only under about 28 atm.',
    'bpLabel': 'Sublimation point',
  },
  6: {
    'phase': 'Solid',
    'why': 'Graphite’s atoms bond in flat sheets of hexagons, with some electrons free to roam along each sheet: it conducts electricity, and the sheets slide over each other, which is how a pencil writes. Diamond bonds every atom to four neighbours in one rigid 3D framework: no free electrons and nothing to slide, so it is an insulator and the hardest natural material. Same atoms, different arrangement.',
    'forms': [
      {'name': 'Graphite', 'note': 'The stable form at room conditions.',
       'mpNote': 'Does not melt at normal pressure; it melts only above about 100 atm (≈ 4,600 K).', 'bp': 4098.15, 'bpLabel': 'Sublimation point',
       'density': 2.27, 'structure': 'Stacked hexagonal sheets (hexagonal)', 'k': '≈ 120–170 W/(m·K) overall; far higher along the sheets',
       'extra': [['Electricity', 'Conducts (along the sheets)'], ['Hardness (Mohs)', '1–2, soft and slippery'], ['Looks', 'Black, opaque, greasy']]},
      {'name': 'Diamond', 'note': 'Formed deep in the Earth’s mantle; at room conditions it is metastable, turning to graphite only extremely slowly.',
       'mpNote': 'Does not melt at normal pressure; heated above about 1,800 K without air it turns into graphite, and in air it burns at around 1,000 K.', 'bp': None,
       'density': 3.515, 'structure': 'Diamond cubic (each atom bonded to 4 others)', 'k': '≈ 2,200 W/(m·K), among the highest of any bulk material',
       'extra': [['Electricity', 'Insulator'], ['Hardness (Mohs)', '10, the hardest natural material'], ['Looks', 'Colourless, transparent']]},
    ],
  },
  15: {
    'phase': 'Solid',
    'why': 'White phosphorus is made of separate P₄ molecules held under heavy strain, so it reacts violently and glows as it slowly burns in air. Red phosphorus links those units into long chains, and black phosphorus into graphite-like layers; each step ties the atoms together more firmly and makes the form more stable.',
    'forms': [
      {'name': 'White', 'note': 'Waxy and toxic; glows in the dark and can catch fire in air at about 30 °C, so it is stored under water.',
       'mp': 317.3, 'bp': 553.7, 'density': 1.823, 'structure': 'P₄ molecules (cubic crystal)',
       'extra': [['Electricity', 'Insulator'], ['Looks', 'White to yellow, waxy']]},
      {'name': 'Red', 'note': 'Stable in air; used on the striking strip of matchboxes.',
       'mpNote': 'Does not melt at normal pressure; it sublimes at about 690 K (416 °C).', 'bp': None,
       'density': 2.2, 'structure': 'Linked chains (mostly amorphous)',
       'extra': [['Electricity', 'Insulator'], ['Looks', 'Dark red powder']]},
      {'name': 'Black', 'note': 'The most stable form, made under high pressure; single layers are called phosphorene.',
       'mpNote': 'Turns into other forms before melting at normal pressure.', 'bp': None,
       'density': 2.69, 'structure': 'Puckered layers (orthorhombic)',
       'extra': [['Electricity', 'Semiconductor'], ['Looks', 'Black, flaky, like graphite']]},
    ],
  },
  16: {
    'phase': 'Solid',
    'why': 'Both forms are built from the same crown-shaped rings of eight sulfur atoms. They differ only in how the rings stack, and sulfur switches from rhombic to monoclinic when warmed above 95 °C.',
    'forms': [
      {'name': 'Rhombic (α)', 'note': 'The stable form at room temperature.',
       'mp': 388.36, 'bp': 717.76, 'density': 2.07, 'structure': 'S₈ rings (orthorhombic)', 'extra': [['Looks', 'Yellow crystals']]},
      {'name': 'Monoclinic (β)', 'note': 'Stable between 95 °C and its melting point; slowly reverts to rhombic when cooled.',
       'mp': 392.75, 'bp': 717.76, 'density': 1.96, 'structure': 'S₈ rings (monoclinic)', 'extra': [['Looks', 'Pale yellow needles']]},
    ],
  },
  34: {
    'phase': 'Solid',
    'why': 'Grey selenium is spiral chains of atoms, which let it conduct electricity when light hits it. Red selenium is separate rings of eight atoms and turns grey when heated.',
    'forms': [
      {'name': 'Grey', 'note': 'The stable form; its conductivity rises in light, which made it the heart of early photocopiers and light meters.',
       'mp': 494.0, 'bp': 958.15, 'density': 4.81, 'structure': 'Spiral chains (trigonal)', 'extra': [['Electricity', 'Semiconductor, photoconductor']]},
      {'name': 'Red', 'note': 'Made by precipitation from solution; changes to grey on heating.',
       'mpNote': 'Turns into grey selenium on heating, before melting.', 'bp': None,
       'density': 4.39, 'structure': 'Se₈ rings (monoclinic)', 'extra': [['Electricity', 'Insulator']]},
    ],
  },
  50: {
    'phase': 'Solid',
    'why': 'Below 13 °C, tin slowly switches to grey tin, which has the same crystal framework as diamond and silicon. Grey tin is much less dense, so the metal swells and crumbles into powder. This "tin pest" was blamed for crumbling organ pipes and buttons in cold winters.',
    'forms': [
      {'name': 'White (β)', 'note': 'The familiar shiny metal, stable above 13.2 °C.',
       'mp': 505.08, 'bp': 2875.0, 'density': 7.287, 'structure': 'Metallic (tetragonal)', 'extra': [['Electricity', 'Conducts (metal)']]},
      {'name': 'Grey (α)', 'note': 'Stable below 13.2 °C; forms slowly in the cold.',
       'mpNote': 'Turns back into white tin above 13.2 °C, long before melting.', 'bp': None,
       'density': 5.77, 'structure': 'Diamond cubic, like silicon', 'extra': [['Electricity', 'Semiconductor'], ['Looks', 'Dull grey, crumbly powder']]},
    ],
  },
}
json.dump(A, open('allotropes.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('ok', len(A))
