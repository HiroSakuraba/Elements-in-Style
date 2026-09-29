# History data for Elements in Style.
# Fields per element: year label, numeric year for the timeline, kind (known / discovered / synthesized),
# who, where, how, earlier names, fun fact.
import json

K, D, S = 'known', 'discovered', 'synthesized'
H = {}
def e(z, year, t, kind, who, where, how, names, fact):
    H[z] = dict(year=year, t=t, kind=kind, who=who, where=where, how=how, names=names, fact=fact)

e(1, '1766', 1766, D, 'Henry Cavendish', 'London, England',
  'Dissolved metals such as zinc and iron in acids and collected the gas given off. In 1781 he showed that it burns to make water.',
  '“Inflammable air” (Cavendish). Lavoisier renamed it hydrogène, “water-maker”, in 1783.',
  'Hydrogen makes up about three quarters of all the ordinary matter in the universe by mass.')
e(2, '1868 (Sun) · 1895 (Earth)', 1868, D, 'Pierre Janssen and Norman Lockyer; isolated by William Ramsay, and independently by Per Cleve and Nils Langlet', 'India and England; London and Uppsala',
  'Seen as an unexplained yellow line in the spectrum of the Sun during the eclipse of 18 August 1868. Ramsay first captured it on Earth in 1895, from gas released when the uranium mineral cleveite was treated with acid.',
  'Named “helium” by Lockyer and Edward Frankland, after helios, the Sun, before anyone had a sample.',
  'It was found in space before it was found on Earth, and at normal pressure liquid helium never freezes, even at absolute zero.')
e(3, '1817', 1817, D, 'Johan August Arfwedson', 'Stockholm, Sweden (in Berzelius’s laboratory)',
  'Found a new alkali while analyzing petalite ore from the island of Utö. William Brande first isolated the metal by electrolysis in 1821.',
  '“Lithion” or “lithina”, from Greek lithos, stone, because it was found in a mineral rather than in plants or animals.',
  'It is the lightest metal: a lump floats on water, and even on oil.')
e(4, '1798', 1798, D, 'Louis-Nicolas Vauquelin', 'Paris, France',
  'Found a new oxide in beryl and emerald. Friedrich Wöhler and Antoine Bussy independently isolated the metal in 1828 by reducing its chloride with potassium.',
  '“Glucinium” (symbol Gl), from Greek glykys, sweet, because its salts taste sweet. France used that name until 1957.',
  'The 18 hexagonal mirror segments of the James Webb Space Telescope are made of gold-coated beryllium.')
e(5, '1808', 1808, D, 'Joseph Louis Gay-Lussac and Louis Jacques Thénard; independently Humphry Davy', 'Paris, France and London, England',
  'Heated boric acid with potassium metal. The product was quite impure; truly pure boron was first made by Ezekiel Weintraub in 1909.',
  '“Boracium” (Davy) and “bore” (French), from borax, the mineral it came from.',
  'Borosilicate glass, the heat-proof glass in lab beakers and oven dishes, owes its toughness to boron.')
e(6, 'Prehistory', -3750, K, 'Unknown; used as charcoal and soot since prehistoric times', 'Worldwide',
  'Charcoal was made by burning wood in low air. Lavoisier listed carbon as an element in 1789, and in 1796 Smithson Tennant proved diamond is pure carbon by burning one and collecting only carbon dioxide.',
  'Latin carbo, charcoal. Graphite was long called “plumbago” or “black lead”.',
  'Pencil “lead” has never contained lead. It is graphite, a form of carbon.')
e(7, '1772', 1772, D, 'Daniel Rutherford (also Carl Scheele, Henry Cavendish and Joseph Priestley, independently)', 'Edinburgh, Scotland',
  'Burned material in a closed volume of air, then absorbed the carbon dioxide. The gas left over put out flames and suffocated mice.',
  '“Noxious air”, “mephitic air” and “phlogisticated air”. Lavoisier called it azote, “lifeless”, which is still its name in French. “Nitrogène”, “nitre-maker”, came from Jean-Antoine Chaptal in 1790.',
  'About 78% of every breath you take is nitrogen, and your body breathes it straight back out unused.')
e(8, '1771–1774', 1774, D, 'Carl Wilhelm Scheele (c. 1771, published 1777) and Joseph Priestley (1 August 1774)', 'Uppsala, Sweden and Calne, England',
  'Priestley focused sunlight through a large lens onto mercury(II) oxide and collected the gas it released. Scheele got the same gas by heating several compounds, including potassium nitrate and manganese dioxide.',
  '“Fire air” (Scheele) and “dephlogisticated air” (Priestley). Lavoisier named it oxygène in 1777.',
  'The name means “acid-former”. It comes from Lavoisier’s mistaken belief that every acid contains oxygen.')
e(9, '1886', 1886, D, 'Henri Moissan', 'Paris, France',
  'Electrolysed a solution of potassium hydrogen fluoride in liquid hydrogen fluoride, chilled well below freezing in a platinum–iridium apparatus.',
  'Ampère proposed “phthore” (“destructive”), which survives as ftor in Russian. “Fluorine” comes from fluorite, a mineral used as a flux (Latin fluere, to flow).',
  'Several chemists were injured or killed trying to isolate it over 70 years. Moissan succeeded and won the 1906 Nobel Prize.')
e(10, '1898', 1898, D, 'William Ramsay and Morris Travers', 'London, England',
  'Liquefied air and let it boil off slowly, catching the new gas in one of the fractions. Its spectrum blazed bright crimson.',
  'Ramsay’s 13-year-old son suggested “novum”, Latin for new. Ramsay preferred the Greek form, neon.',
  'Neon signs only glow red-orange when they really contain neon. The other colours come from other gases or coatings.')
e(11, '1807', 1807, D, 'Humphry Davy', 'Royal Institution, London, England',
  'Ran a current from a large voltaic battery through molten caustic soda (sodium hydroxide).',
  'Named after soda. The symbol Na comes from Latin natrium, from natron, the salt Egyptians used to dry out mummies.',
  'Davy isolated potassium only days before sodium, both with the same giant battery.')
e(12, '1755 (recognized) · 1808 (isolated)', 1808, D, 'Joseph Black recognized it; Humphry Davy isolated it', 'Edinburgh, Scotland; London, England',
  'Davy electrolysed a damp mixture of magnesia and mercury oxide, getting a magnesium amalgam, then boiled off the mercury.',
  'Davy first called it “magnium”. The name traces to Magnesia, a district of Thessaly in Greece.',
  'Burning magnesium keeps going even under water or carbon dioxide; it tears the oxygen out of both.')
e(13, '1825', 1825, D, 'Hans Christian Ørsted; purer metal by Friedrich Wöhler in 1827', 'Copenhagen, Denmark; Göttingen, Germany',
  'Reduced aluminium chloride with a potassium amalgam. Cheap aluminium came only in 1886, with the Hall–Héroult electrolysis process.',
  'Davy proposed “alumium”, then “aluminum”. Most of the world later settled on “aluminium”.',
  'In the 1850s aluminium cost more than gold. The capstone of the Washington Monument (1884) is a showpiece of aluminium.')
e(14, '1824', 1824, D, 'Jöns Jacob Berzelius', 'Stockholm, Sweden',
  'Heated potassium with potassium fluorosilicate and washed away the salts, leaving amorphous silicon. Gay-Lussac and Thénard had made an impure version in 1811.',
  '“Silicium” (Berzelius), still its name in many languages. Thomas Thomson suggested “silicon” in 1817 to match boron and carbon.',
  'Silicon is about 28% of Earth’s crust by mass, second only to oxygen.')
e(15, '1669', 1669, D, 'Hennig Brand', 'Hamburg, Germany',
  'An alchemist hunting for the philosopher’s stone, he boiled down large amounts of urine and heated the residue until a glowing white solid distilled over.',
  'Brand called it “cold fire”. Phosphorus is Greek for “light-bearer”, an old name for Venus as the morning star.',
  'It was the first element discovered by a known person using a chemical method.')
e(16, 'Antiquity', -2000, K, 'Unknown; found free near volcanoes and hot springs', 'Worldwide',
  'Picked up as yellow crystals around volcanic vents. Lavoisier showed in 1777 that it is an element, not a compound.',
  '“Brimstone”, “burning stone”. Latin sulpur.',
  'Jupiter’s moon Io has volcanoes that erupt sulfur and sulfur dioxide.')
e(17, '1774', 1774, D, 'Carl Wilhelm Scheele; shown to be an element by Humphry Davy in 1810', 'Uppsala, Sweden; London, England',
  'Reacted the mineral pyrolusite (manganese dioxide) with hydrochloric acid and got a choking yellow-green gas.',
  '“Dephlogisticated muriatic acid”, later “oxymuriatic acid”, because chemists assumed it contained oxygen. Davy named it chlorine, from Greek chloros, pale green.',
  'For 36 years chemists were sure it was a compound of oxygen, until Davy showed there was none in it.')
e(18, '1894', 1894, D, 'Lord Rayleigh and William Ramsay', 'London, England',
  'Rayleigh noticed nitrogen taken from air was about 0.5% denser than nitrogen made from chemicals. Removing all the nitrogen and oxygen from air left a small, stubborn residue: argon.',
  'Greek argos, “idle” or “lazy”, because it would not react with anything.',
  'Air is almost 1% argon, more than 20 times as much as carbon dioxide.')
e(19, '1807', 1807, D, 'Humphry Davy', 'Royal Institution, London, England',
  'Electrolysis of slightly damp molten potash (potassium hydroxide). It was the first metal ever isolated by electrolysis.',
  'Named after potash, “pot ashes”. The symbol K comes from Latin kalium, from Arabic al-qalī, plant ashes.',
  'Davy’s assistant recorded that he danced around the room with delight when the silvery globules burst into flame.')
e(20, '1808', 1808, D, 'Humphry Davy', 'London, England',
  'Electrolysed a mixture of lime and mercury oxide to get a calcium amalgam, then distilled off the mercury.',
  'From Latin calx, lime.',
  'An adult human carries about a kilogram of calcium, mostly in bones and teeth.')
e(21, '1879', 1879, D, 'Lars Fredrik Nilson', 'Uppsala, Sweden',
  'Found while separating rare earths from the minerals euxenite and gadolinite, and identified by its spectrum.',
  'Predicted in 1871 by Dmitri Mendeleev as “eka-boron”.',
  'Per Cleve pointed out that it matched Mendeleev’s predicted eka-boron, one of the first wins for the periodic table.')
e(22, '1791', 1791, D, 'William Gregor; independently Martin Heinrich Klaproth in 1795', 'Cornwall, England; Berlin, Germany',
  'Gregor, a clergyman, found a new metal in black sand from the Manaccan valley. Pure metal was first made in 1910 by Matthew Hunter, by heating its chloride with sodium.',
  '“Menachanite” (Gregor). Klaproth named it titanium after the Titans of Greek myth.',
  'Titanium is about as strong as many steels but around 45% lighter.')
e(23, '1801 · 1830', 1830, D, 'Andrés Manuel del Río; rediscovered by Nils Gabriel Sefström', 'Mexico City, Mexico; Falun, Sweden',
  'Del Río found it in a lead ore now called vanadinite, but was persuaded it was impure chromium and withdrew his claim. Sefström rediscovered it in Swedish iron ore. Henry Roscoe made the metal in 1867.',
  '“Panchromium” (“all colours”) and then “erythronium” (del Río). Sefström named it after Vanadís, a name of the Norse goddess Freyja.',
  'Some sea squirts pack vanadium into their blood cells at millions of times the concentration in seawater.')
e(24, '1797', 1797, D, 'Louis-Nicolas Vauquelin', 'Paris, France',
  'Analyzed crocoite, a bright orange-red lead mineral from Siberia, and in 1798 got the metal by heating its oxide with charcoal.',
  'From Greek chroma, colour, because its compounds come in so many.',
  'Traces of chromium give rubies their red and emeralds their green.')
e(25, '1774', 1774, D, 'Johan Gottlieb Gahn (isolated); recognized by Carl Scheele and Torbern Bergman', 'Stockholm, Sweden',
  'Gahn heated pyrolusite (manganese dioxide) with charcoal and oil to get the metal.',
  'Pyrolusite was called “black magnesia”, and the metal was briefly “manganesium”. It shares its roots with magnesium, which caused decades of confusion.',
  'Around 90% of all manganese mined goes into making steel.')
e(26, 'Prehistory', -3500, K, 'Unknown; used as meteoric iron, then smelted from about 1200 BC', 'Middle East and Anatolia',
  'The first iron came from meteorites. Smelting ore with charcoal at high temperature began the Iron Age.',
  'Latin ferrum. Old English īsern.',
  'Tutankhamun was buried with a dagger forged from meteoritic iron.')
e(27, 'c. 1735', 1735, D, 'Georg Brandt', 'Stockholm, Sweden',
  'Showed that the deep blue colour of certain glasses came from a new metal, not from bismuth as people assumed.',
  'From German Kobold, goblin. Miners blamed goblins for ores that looked valuable but gave off poisonous arsenic fumes when smelted.',
  'It was the first metal discovered by a known person since ancient times.')
e(28, '1751', 1751, D, 'Axel Fredrik Cronstedt', 'Stockholm, Sweden',
  'Extracted a new metal from niccolite, an ore that looked like copper ore but yielded no copper.',
  'Miners called the ore Kupfernickel, “copper-demon” or “Old Nick’s copper”.',
  'A US five-cent “nickel” is actually 75% copper and only 25% nickel.')
e(29, 'Prehistory', -9000, K, 'Unknown; native copper was worked around 9000 BC', 'Middle East',
  'First hammered from naturally occurring lumps of metal, then smelted from ore from about 5000 BC.',
  'Latin cyprium, “metal of Cyprus”, later cuprum.',
  'The Statue of Liberty is copper. Its green colour is a patina that formed over about 30 years.')
e(30, 'c. 1300 (India) · 1746 (Europe)', 1746, D, 'Metallurgists at Zawar, India; in Europe credited to Andreas Sigismund Marggraf', 'Rajasthan, India; Berlin, Germany',
  'Zinc boils at a lower temperature than it smelts, so it escapes as vapour. Indian smelters around the 14th century solved this with downward distillation. Marggraf heated calamine with charcoal in a closed vessel.',
  '“Spelter”. Paracelsus called it zincum, perhaps from German Zinke, prong, for the shape of its crystals.',
  'Since 1982 a US penny has been 97.5% zinc with a thin copper coat.')
e(31, '1875', 1875, D, 'Paul-Émile Lecoq de Boisbaudran', 'Paris, France',
  'Spotted two new violet lines in the spectrum of zinc blende ore, then isolated the metal by electrolysis.',
  'Predicted by Mendeleev as “eka-aluminium”.',
  'It melts at 29.8 °C, so a piece will melt in your hand.')
e(32, '1886', 1886, D, 'Clemens Winkler', 'Freiberg, Germany',
  'Analysed the mineral argyrodite, found about 7% of its mass unaccounted for, and tracked down the missing element.',
  'Predicted by Mendeleev as “eka-silicon”.',
  'Mendeleev predicted an atomic weight of about 72 and a density of 5.5 g/cm³. The measured values were 72.6 and 5.35.')
e(33, 'c. 1250', 1250, D, 'Traditionally credited to Albertus Magnus', 'Germany',
  'Heated its sulfide ores, orpiment and realgar (known since antiquity), with soap. Arsenic compounds were used much earlier.',
  'From Greek arsenikon, yellow orpiment, from Persian zarnikh, gold-coloured.',
  'It was a favourite poison, nicknamed “inheritance powder”, until the Marsh test of 1836 made it easy to detect.')
e(34, '1817', 1817, D, 'Jöns Jacob Berzelius and Johan Gottlieb Gahn', 'Stockholm, Sweden',
  'Found in a red sludge from the lead chambers of a sulfuric acid works. At first they thought it was tellurium.',
  'From Greek selene, the Moon, as a partner to tellurium, which was named after the Earth.',
  'Selenium conducts electricity better in light than in the dark, which made it the heart of early photocopiers.')
e(35, '1826', 1826, D, 'Antoine-Jérôme Balard; independently Carl Löwig', 'Montpellier, France; Heidelberg, Germany',
  'Balard bubbled chlorine through brine from salt marshes and extracted the red-brown liquid that formed.',
  'Balard proposed “muride”. It was named bromine from Greek bromos, stench.',
  'Justus von Liebig had been sent a sample earlier but labelled it “liquid iodine chloride”. He kept the bottle as a reminder never to jump to conclusions.')
e(36, '1898', 1898, D, 'William Ramsay and Morris Travers', 'London, England',
  'Found in what was left after nearly all of a sample of liquid air had boiled away.',
  'From Greek kryptos, hidden.',
  'From 1960 to 1983 the metre was defined by an orange-red spectral line of krypton-86.')
e(37, '1861', 1861, D, 'Robert Bunsen and Gustav Kirchhoff', 'Heidelberg, Germany',
  'Found two deep red lines in the spectrum of the mineral lepidolite using their new spectroscope.',
  'From Latin rubidus, deep red.',
  'It was the second element found with a spectroscope, a year after caesium. The metal melts at 39 °C.')
e(38, '1790 · 1808', 1790, D, 'Adair Crawford and William Cruickshank; isolated by Humphry Davy in 1808', 'Edinburgh and London',
  'Crawford saw that a mineral from Strontian, Scotland, behaved differently from barium minerals. Davy isolated the metal by electrolysis.',
  '“Strontites” and “strontia”, after the mineral strontianite.',
  'It is named after the Scottish village of Strontian, and it gives fireworks their bright red.')
e(39, '1794', 1794, D, 'Johan Gadolin', 'Turku, Finland',
  'Analysed a heavy black mineral found in 1787 at the Ytterby quarry near Stockholm and found a new oxide, “yttria”. Friedrich Wöhler isolated the metal in 1828.',
  'Yttria earth. The mineral was later named gadolinite, after Gadolin.',
  'The single village of Ytterby gave its name to four elements: yttrium, ytterbium, terbium and erbium.')
e(40, '1789', 1789, D, 'Martin Heinrich Klaproth', 'Berlin, Germany',
  'Found a new oxide, “zirconia”, in a zircon gem from Sri Lanka. Berzelius made an impure metal in 1824.',
  'Zircon comes from Persian zargun, gold-coloured.',
  'Zircon crystals from Western Australia are about 4.4 billion years old, the oldest known pieces of Earth.')
e(41, '1801', 1801, D, 'Charles Hatchett; confirmed distinct from tantalum by Heinrich Rose in 1844', 'London, England; Berlin, Germany',
  'Analysed a mineral sample from Connecticut kept in the British Museum. For 40 years it was confused with tantalum, until Rose separated them.',
  '“Columbium” (Cb), after Columbia, a name for America. The US used it until IUPAC chose niobium in 1949.',
  'Rose named it after Niobe, the daughter of Tantalus, because it is so similar to tantalum.')
e(42, '1778 · 1781', 1781, D, 'Carl Wilhelm Scheele (identified); Peter Jacob Hjelm (isolated)', 'Uppsala, Sweden',
  'Scheele showed that the mineral molybdenite was not graphite or lead ore. Hjelm reduced the oxide with carbon to get the metal.',
  'From Greek molybdos, lead. The soft grey mineral was long confused with lead ore and graphite.',
  'Its name means “lead-like”, though it has nothing to do with lead.')
e(43, '1937', 1937, S, 'Carlo Perrier and Emilio Segrè', 'Palermo, Italy',
  'Examined a molybdenum strip from Ernest Lawrence’s cyclotron at Berkeley that had been hit by deuterons, and found a new radioactive element in it.',
  'Predicted by Mendeleev as “eka-manganese”. Earlier false claims include “davyum”, “lucium”, “nipponium” and “masurium”.',
  'It was the first element made artificially, and its name comes from Greek technetos, artificial. Technetium-99m is used in tens of millions of medical scans a year.')
e(44, '1844', 1844, D, 'Karl Ernst Claus', 'Kazan, Russia',
  'Extracted it from the residues left after refining platinum ore from the Ural Mountains.',
  'Gottfried Osann had proposed “ruthenium”, along with “pluran” and “polinium”, in 1828, but his samples were impure. Claus kept the name.',
  'It is named after Ruthenia, Latin for Russia, the first element named after that country.')
e(45, '1804', 1804, D, 'William Hyde Wollaston', 'London, England',
  'Dissolved crude platinum ore in aqua regia and separated out a metal whose salts were rose-red.',
  'From Greek rhodon, rose.',
  'At times it has been the most expensive precious metal, well above gold and platinum.')
e(46, '1802', 1802, D, 'William Hyde Wollaston', 'London, England',
  'Found it in the same platinum-ore work that gave him rhodium.',
  'Named after the asteroid Pallas, discovered earlier that year.',
  'Wollaston first announced it anonymously, by selling it in a shop as “new silver”. One skeptic bought some and declared it a fake alloy.')
e(47, 'Antiquity', -5000, K, 'Unknown; mined from about 3000 BC in Anatolia', 'Anatolia and the Aegean',
  'Separated from lead ores by cupellation, oxidizing away the lead.',
  'Latin argentum, which gave Argentina its name.',
  'Silver conducts electricity and heat better than any other metal.')
e(48, '1817', 1817, D, 'Friedrich Stromeyer (also Karl Hermann, Karl Meissner and J. C. H. Roloff)', 'Göttingen, Germany',
  'Investigated why a zinc carbonate sample turned yellow on heating, even though it contained no iron, and found a new metal as the impurity.',
  'From Latin cadmia, calamine, the zinc ore it was found in.',
  'Cadmium pollution along a Japanese river caused “itai-itai” (“it hurts, it hurts”) disease in the 20th century.')
e(49, '1863', 1863, D, 'Ferdinand Reich and Hieronymus Theodor Richter', 'Freiberg, Germany',
  'Found a brilliant indigo line in the spectrum of zinc ore.',
  'From indigo, for that spectral line.',
  'Reich was colour-blind, so his assistant Richter had to do the looking.')
e(50, 'Antiquity', -3000, K, 'Unknown; used in bronze from about 3000 BC', 'Middle East and Europe',
  'Smelted from the ore cassiterite. Mixed with copper, it made bronze.',
  'Latin stannum.',
  'Bending a bar of tin makes a faint crackling sound, called the “tin cry”.')
e(51, 'Antiquity', -3000, K, 'Unknown; the metal was described by Vannoccio Biringuccio in 1540', 'Egypt and the Middle East',
  'Its sulfide, stibnite, was ground into powder. The metal was made by heating the ore with iron.',
  'Latin stibium. “Antimony” may come from Greek anti-monos, “not alone”, since it is rarely found pure.',
  'Ancient Egyptians used powdered stibnite as black eyeliner (kohl).')
e(52, '1782', 1782, D, 'Franz-Joseph Müller von Reichenstein; named by Klaproth in 1798', 'Sibiu, Transylvania',
  'Found an unknown metal while analysing a gold ore, and spent three years testing it.',
  '“Metallum problematicum” and “aurum paradoxum”, paradoxical gold.',
  'Named after the Earth (Latin tellus). Even small exposures give people garlic breath that lasts for weeks.')
e(53, '1811', 1811, D, 'Bernard Courtois', 'Paris, France',
  'Was extracting saltpetre from seaweed ash for Napoleon’s gunpowder. Adding sulfuric acid gave off a violet vapour that condensed into dark crystals.',
  '“Substance X”. Gay-Lussac named it iode, from Greek iodes, violet.',
  'It was found because France needed gunpowder during the Napoleonic Wars.')
e(54, '1898', 1898, D, 'William Ramsay and Morris Travers', 'London, England',
  'Found in the heaviest leftover fraction of krypton distilled from liquid air.',
  'From Greek xenos, stranger.',
  'In 1962 Neil Bartlett made xenon hexafluoroplatinate, the first compound of a noble gas.')
e(55, '1860', 1860, D, 'Robert Bunsen and Gustav Kirchhoff', 'Heidelberg, Germany',
  'Evaporated tens of thousands of litres of Dürkheim spring water and found two new blue lines in the spectrum of the residue. Carl Setterberg first made the metal in 1882.',
  'From Latin caesius, sky blue.',
  'The second is defined by caesium: exactly 9,192,631,770 cycles of the radiation from caesium-133.')
e(56, '1774 · 1808', 1774, D, 'Carl Wilhelm Scheele (baryta); isolated by Humphry Davy in 1808', 'Uppsala, Sweden; London, England',
  'Scheele distinguished its oxide, baryta, from lime. Davy isolated the metal by electrolysis.',
  '“Terra ponderosa” (heavy earth) and baryta, from Greek barys, heavy. Its mineral was the “Bologna stone”.',
  'The Bologna stone glowed in the dark after being heated, which fascinated 17th-century alchemists.')
e(57, '1839', 1839, D, 'Carl Gustaf Mosander', 'Stockholm, Sweden',
  'Partly decomposed cerium nitrate and extracted a new oxide hiding inside it.',
  'From Greek lanthanein, to lie hidden.',
  'Each nickel-metal-hydride battery in an early Toyota Prius held around 10 kg of lanthanum.')
e(58, '1803', 1803, D, 'Jöns Jacob Berzelius and Wilhelm Hisinger; independently Martin Heinrich Klaproth', 'Sweden; Germany',
  'Found a new oxide in the heavy mineral now called cerite.',
  'Klaproth called it “ochroite”. Berzelius named it after the dwarf planet Ceres, discovered two years earlier.',
  'The flint in a cigarette lighter is mostly cerium alloy, which throws sparks when scraped.')
e(59, '1885', 1885, D, 'Carl Auer von Welsbach', 'Vienna, Austria',
  'Split “didymium”, which had been accepted as an element since 1841, into two elements by fractional crystallization.',
  'Part of “didymium” (Greek didymos, twin). Its name means “green twin”.',
  'Didymium was thought to be a single element for 44 years. Didymium glass is still used in glassblowers’ goggles.')
e(60, '1885', 1885, D, 'Carl Auer von Welsbach', 'Vienna, Austria',
  'The other half of didymium, separated by fractional crystallization.',
  '“Neodidymium”, new twin.',
  'Neodymium–iron–boron magnets are the strongest permanent magnets there are, and they are in most earbuds and electric motors.')
e(61, '1945', 1945, S, 'Jacob Marinsky, Lawrence Glendenin and Charles Coryell', 'Oak Ridge, Tennessee, USA',
  'Separated it from uranium fission products made in the Oak Ridge graphite reactor, using ion-exchange chromatography.',
  'Earlier false claims were “illinium” (1926, Illinois) and “florentium” (Florence). Coryell’s wife Grace suggested promethium.',
  'It is the only lanthanide with no stable isotope, named after Prometheus, who stole fire from the gods.')
e(62, '1879', 1879, D, 'Paul-Émile Lecoq de Boisbaudran', 'Paris, France',
  'Identified by its spectrum in didymium extracted from the mineral samarskite.',
  'Named after samarskite, which was named after the Russian mining officer Vasili Samarsky-Bykhovets.',
  'Through its mineral, it was the first element named, indirectly, after a person.')
e(63, '1901', 1901, D, 'Eugène-Anatole Demarçay', 'Paris, France',
  'Painstakingly separated samarium samples and identified a new element by its spectrum.',
  'Named after Europe.',
  'Europium compounds made the red colour in older television screens.')
e(64, '1880', 1880, D, 'Jean Charles Galissard de Marignac', 'Geneva, Switzerland',
  'Detected it by spectroscopy in samarskite. Lecoq de Boisbaudran purified it and named it in 1886.',
  'Named after the mineral gadolinite, and so after the Finnish chemist Johan Gadolin.',
  'It is magnetic only below about 20 °C, so a piece loses its pull on a warm day.')
e(65, '1843', 1843, D, 'Carl Gustaf Mosander', 'Stockholm, Sweden',
  'Split yttria into three oxides: yttria, “erbia” and “terbia”.',
  'Mosander’s original names were later swapped: what he called “erbia” is now terbia, and vice versa.',
  'The name swap happened by confusion in the 1860s and 1870s, and it stuck.')
e(66, '1886', 1886, D, 'Paul-Émile Lecoq de Boisbaudran', 'Paris, France',
  'Separated it from holmium oxide after more than 30 tries, reportedly working on the marble slab of his fireplace.',
  'From Greek dysprositos, hard to get at.',
  'The pure metal was not made until the 1950s, when Frank Spedding developed ion-exchange separation.')
e(67, '1878', 1878, D, 'Marc Delafontaine and Jacques-Louis Soret (spectrum); Per Teodor Cleve (separation, 1879)', 'Geneva, Switzerland; Uppsala, Sweden',
  'Soret saw unexplained absorption lines. Cleve independently separated it from erbia.',
  'Soret called it “element X”. Cleve named it holmium after Holmia, Latin for Stockholm.',
  'Holmium has the largest magnetic moment of any naturally occurring element, which makes it useful in the strongest electromagnets.')
e(68, '1843', 1843, D, 'Carl Gustaf Mosander', 'Stockholm, Sweden',
  'One of three oxides Mosander separated from yttria.',
  'Mosander originally called this one “terbia”; the names were later swapped.',
  'Erbium-doped fibre amplifiers boost the light signals that carry the internet under the oceans.')
e(69, '1879', 1879, D, 'Per Teodor Cleve', 'Uppsala, Sweden',
  'Found in the leftovers after removing other rare earths from erbia.',
  'Named after Thule, a mythical land in the far north.',
  'It is one of the rarest lanthanides, yet still more common than gold.')
e(70, '1878', 1878, D, 'Jean Charles Galissard de Marignac', 'Geneva, Switzerland',
  'Heated erbium nitrate and separated a new oxide, “ytterbia”.',
  'In 1907 Georges Urbain split ytterbia into “neoytterbium” and “lutecium”. Auer von Welsbach called the two parts “aldebaranium” and “cassiopeium”.',
  'Ytterbium atomic clocks are among the most precise clocks ever built.')
e(71, '1907', 1907, D, 'Georges Urbain; independently Carl Auer von Welsbach and Charles James', 'Paris, France; Austria; New Hampshire, USA',
  'All three split Marignac’s ytterbia into two elements.',
  '“Lutecium” (Urbain, from Lutetia, Latin for Paris) and “cassiopeium” (Auer von Welsbach), which German chemists used until the 1950s.',
  'Lutetium-177 is now used in targeted cancer treatment.')
e(72, '1923', 1923, D, 'Dirk Coster and George de Hevesy', 'Copenhagen, Denmark (Niels Bohr’s institute)',
  'Bohr’s new atomic theory predicted element 72 should resemble zirconium, not the rare earths. They searched zirconium ores with X-ray spectroscopy and found it.',
  'Georges Urbain claimed it as “celtium” in 1911. Named after Hafnia, Latin for Copenhagen.',
  'Hafnium is so chemically similar to zirconium that it had hidden inside zirconium ores all along.')
e(73, '1802', 1802, D, 'Anders Gustaf Ekeberg', 'Uppsala, Sweden',
  'Found a new oxide in minerals from Finland and Sweden that would not dissolve in acids.',
  'Named after Tantalus, who in Greek myth could never drink the water around him, just as the oxide could not take up acid. Confused with niobium until 1866.',
  'Tantalum capacitors are in almost every mobile phone.')
e(74, '1783', 1783, D, 'Juan José and Fausto Elhuyar (isolated); tungstic acid identified by Scheele in 1781', 'Bergara, Spain',
  'The Elhuyar brothers got tungstic acid from wolframite and reduced it with charcoal to make the metal.',
  'Wolfram (symbol W), from German “wolf’s froth”, because the ore ate up tin during smelting like a wolf. Tungsten is Swedish for heavy stone.',
  'It has the highest melting point of any metal, 3,422 °C.')
e(75, '1925', 1925, D, 'Walter Noddack, Ida Tacke and Otto Berg', 'Berlin, Germany',
  'Found by X-ray spectroscopy in platinum ores and the mineral columbite.',
  'Masataka Ogawa may have found it in 1908 and called it “nipponium”, but he thought it was element 43.',
  'It was the last stable element to be discovered. It is named after the Rhine.')
e(76, '1803', 1803, D, 'Smithson Tennant', 'London, England',
  'Studied the black residue left when crude platinum is dissolved in aqua regia, and found two new metals in it: osmium and iridium.',
  'From Greek osme, smell, for the sharp odour of its volatile oxide.',
  'At 22.59 g/cm³ it is the densest naturally occurring element.')
e(77, '1803', 1803, D, 'Smithson Tennant', 'London, England',
  'The second new metal in the platinum residue.',
  'Named after Iris, the Greek goddess of the rainbow, for its colourful salts.',
  'A thin layer rich in iridium, found worldwide, is key evidence that an asteroid impact ended the age of dinosaurs.')
e(78, '1748 (in Europe)', 1748, D, 'Pre-Columbian South Americans; described by Antonio de Ulloa', 'Colombia; Spain',
  'Native peoples worked it with gold. Europeans studied grains from the Pinto River in Colombia.',
  '“Platina del Pinto”, little silver of the Pinto River. Also “white gold”.',
  'Spanish officials once dumped it in rivers, because it was being used to counterfeit gold.')
e(79, 'Prehistory', -6000, K, 'Unknown; gathered as nuggets and flakes', 'Worldwide',
  'Found pure in rivers and rocks; later panned and mined.',
  'Latin aurum, “shining dawn”.',
  'All the gold ever mined would fit in a cube about 22 metres on a side.')
e(80, 'Antiquity', -1500, K, 'Unknown; found in Egyptian tombs from about 1500 BC', 'Egypt, China and the Mediterranean',
  'Made by roasting the red ore cinnabar, which releases mercury vapour that condenses into liquid metal.',
  'Hydrargyrum (“water-silver”, symbol Hg) and quicksilver.',
  'It is the only metal liquid at room temperature. Hat-makers poisoned by the mercury used for felt inspired “mad as a hatter”.')
e(81, '1861', 1861, D, 'William Crookes; metal isolated by Claude-Auguste Lamy in 1862', 'London, England; Lille, France',
  'Saw a bright green line in the spectrum of residue from a sulfuric acid plant.',
  'From Greek thallos, a green shoot.',
  'Its tasteless, odourless salts earned it the nickname “poisoner’s poison”.')
e(82, 'Antiquity', -6500, K, 'Unknown; smelted from about 6500 BC', 'Anatolia',
  'Smelted from the ore galena, which melts and releases lead easily in a simple fire.',
  'Latin plumbum, which gives us “plumbing” and “plumber”.',
  'Roman water pipes were made of lead, which is why a plumber is named after it.')
e(83, 'c. 1500', 1500, D, 'Known to miners; shown to be a distinct element by Claude François Geoffroy in 1753', 'Germany; Paris, France',
  'Long confused with tin and lead. Geoffroy showed it is a separate metal.',
  '“Wismut” in German, and “tectum argenti”, roof of silver.',
  'It is very slightly radioactive, with a half-life about a billion times the age of the universe.')
e(84, '1898', 1898, D, 'Marie and Pierre Curie', 'Paris, France',
  'Chemically separated tonnes of pitchblende, using radioactivity to track which fraction held the new element.',
  '“Radium F”, as a product of radium decay. The Curies named it after Poland.',
  'Marie Curie named it after her homeland, which did not exist as an independent country at the time, to draw attention to its cause.')
e(85, '1940', 1940, S, 'Dale Corson, Kenneth MacKenzie and Emilio Segrè', 'Berkeley, California, USA',
  'Bombarded bismuth-209 with alpha particles in a cyclotron.',
  'Predicted as “eka-iodine”. False earlier claims include “alabamine”, “helvetium” and “dakin”.',
  'It is the rarest naturally occurring element: less than a gram is thought to exist in Earth’s crust at any moment.')
e(86, '1899 · 1900', 1900, D, 'Ernest Rutherford and Robert Owens (from thorium); Friedrich Ernst Dorn (from radium)', 'Montreal, Canada; Halle, Germany',
  'Noticed that thorium and radium gave off a radioactive gas.',
  '“Emanation”, “radium emanation”, “thoron”, “actinon” and “niton”. Radon was adopted in 1923.',
  'Radon seeping into basements is the second leading cause of lung cancer after smoking.')
e(87, '1939', 1939, D, 'Marguerite Perey', 'Institut Curie, Paris, France',
  'Purified actinium-227 and found a radioactivity that belonged to a new element produced when actinium decays.',
  'Predicted as “eka-caesium”. Perey called it “actinium K”. False earlier claims include “virginium”, “moldavium” and “russium”.',
  'It was the last element discovered in nature. Perey later became the first woman elected to the French Academy of Sciences.')
e(88, '1898', 1898, D, 'Marie and Pierre Curie (with Gustave Bémont)', 'Paris, France',
  'Traced a strong radioactivity through tonnes of pitchblende to a new element. Marie Curie and André-Louis Debierne isolated the metal in 1910.',
  'From Latin radius, ray.',
  'Workers who painted glow-in-the-dark watch dials with radium, the “Radium Girls”, suffered severe poisoning, which led to modern workplace safety laws.')
e(89, '1899', 1899, D, 'André-Louis Debierne; independently Friedrich Oskar Giesel in 1902', 'Paris, France; Braunschweig, Germany',
  'Separated it from pitchblende residues left after the Curies extracted radium.',
  'Giesel called it “emanium”.',
  'Actinium is so radioactive that it glows pale blue in the dark.')
e(90, '1829', 1829, D, 'Jöns Jacob Berzelius', 'Stockholm, Sweden',
  'Analysed a black mineral sent by Morten Thrane Esmark from Norway (now called thorite).',
  'Named after Thor, the Norse god of thunder.',
  'Berzelius had already used the name “thorium” in 1815 for a supposed element that turned out to be yttrium phosphate. He recycled it.')
e(91, '1913 · 1917', 1917, D, 'Kasimir Fajans and Oswald Göhring (1913); Otto Hahn and Lise Meitner (1917)', 'Karlsruhe, Germany; Berlin, Germany',
  'Fajans and Göhring found a short-lived isotope in the uranium decay chain. Hahn and Meitner found the long-lived isotope protactinium-231.',
  '“Brevium” (Fajans), for its short half-life. “Protoactinium” was shortened to protactinium in 1949. Predicted by Mendeleev as “eka-tantalum”.',
  'In 1961 Britain extracted about 125 g from 60 tonnes of nuclear waste. For decades that was almost the whole world’s supply.')
e(92, '1789', 1789, D, 'Martin Heinrich Klaproth', 'Berlin, Germany',
  'Dissolved pitchblende in nitric acid and obtained an oxide he took to be the new element. Eugène-Melchior Péligot isolated the metal in 1841.',
  'Named after the planet Uranus, discovered eight years earlier.',
  'Henri Becquerel discovered radioactivity in 1896 when uranium salts fogged a wrapped photographic plate.')
e(93, '1940', 1940, S, 'Edwin McMillan and Philip Abelson', 'Berkeley, California, USA',
  'Bombarded uranium with neutrons in the cyclotron. Uranium-239 decayed into the new element.',
  'Enrico Fermi thought he had made it in 1934 and named it “ausenium”. That claim was wrong.',
  'It was the first element heavier than uranium ever made, and was named after Neptune, the planet past Uranus.')
e(94, '1940–41', 1941, S, 'Glenn Seaborg, Edwin McMillan, Joseph Kennedy and Arthur Wahl', 'Berkeley, California, USA',
  'Bombarded uranium with deuterons in the 60-inch cyclotron. The discovery was kept secret until 1946.',
  'Code-named “49” during the Manhattan Project. Named after Pluto.',
  'Seaborg chose the symbol Pu, rather than Pl, as a joke on “pee-yoo”, and expected it to be rejected. It wasn’t.')
e(95, '1944', 1944, S, 'Glenn Seaborg, Ralph James, Leon Morgan and Albert Ghiorso', 'Metallurgical Laboratory, Chicago, USA',
  'Bombarded plutonium with neutrons in a nuclear reactor.',
  'Nicknamed “pandemonium” because it was so hard to separate. Named after the Americas, by analogy with europium.',
  'Seaborg revealed it on a children’s radio quiz show in November 1945, days before the official announcement.')
e(96, '1944', 1944, S, 'Glenn Seaborg, Ralph James and Albert Ghiorso', 'Berkeley and Chicago, USA',
  'Bombarded plutonium-239 with alpha particles in the Berkeley cyclotron.',
  'Nicknamed “delirium”. Named after Marie and Pierre Curie.',
  'Curium-244 sources powered the X-ray spectrometers that analysed rocks on several Mars rovers.')
e(97, '1949', 1949, S, 'Stanley Thompson, Albert Ghiorso and Glenn Seaborg', 'Berkeley, California, USA',
  'Bombarded americium-241 with alpha particles.',
  'Named after the city of Berkeley.',
  'For its first 13 years only invisible traces existed. The first visible speck, a berkelium compound, was made in 1962.')
e(98, '1950', 1950, S, 'Stanley Thompson, Kenneth Street Jr., Albert Ghiorso and Glenn Seaborg', 'Berkeley, California, USA',
  'Bombarded curium-242 with alpha particles.',
  'Named after the state and University of California.',
  'The New Yorker joked they should have named elements 97 and 98 “universitium” and “ofium”. The team replied they would save “newium” and “yorkium” for later.')
e(99, '1952', 1952, S, 'Albert Ghiorso and team (Berkeley, Argonne and Los Alamos)', 'Found in debris from the “Ivy Mike” test, Enewetak Atoll',
  'Identified in fallout from the first hydrogen bomb test. The discovery was kept secret until 1955.',
  'Named after Albert Einstein.',
  'It was first made in a thermonuclear explosion, not a laboratory.')
e(100, '1952', 1952, S, 'Albert Ghiorso and team (Berkeley, Argonne and Los Alamos)', 'Found in debris from the “Ivy Mike” test, Enewetak Atoll',
  'Identified in the same hydrogen-bomb fallout as einsteinium.',
  'Named after Enrico Fermi.',
  'It is the heaviest element that can be built up by adding neutrons; beyond it, the next isotopes fall apart too fast. This is called the fermium gap.')
e(101, '1955', 1955, S, 'Albert Ghiorso, Bernard Harvey, Gregory Choppin, Stanley Thompson and Glenn Seaborg', 'Berkeley, California, USA',
  'Bombarded a tiny einsteinium target with alpha particles, and detected just 17 atoms in total.',
  'Named after Dmitri Mendeleev.',
  'It was the first element made and detected one atom at a time. Naming it after a Russian scientist at the height of the Cold War needed US government sign-off.')
e(102, '1958–1966', 1966, S, 'Joint Institute for Nuclear Research (Georgy Flerov’s group), after disputed claims from Stockholm and Berkeley', 'Dubna, USSR',
  'Bombarded uranium-238 with neon-22 ions. The Dubna work was eventually credited as the reliable discovery.',
  'A Stockholm team claimed it in 1957 and named it “nobelium”. Dubna proposed “joliotium”.',
  'The Swedish claim was wrong, but the name nobelium stuck anyway.')
e(103, '1961', 1961, S, 'Albert Ghiorso, Torbjørn Sikkeland, Almon Larsh and Robert Latimer (credit shared with Dubna)', 'Berkeley, California, USA',
  'Bombarded californium with boron ions.',
  'Its first symbol was Lw. IUPAC changed it to Lr in 1963.',
  'Named after Ernest Lawrence, inventor of the cyclotron that made so many new elements possible.')
e(104, '1964 · 1969', 1969, S, 'Joint Institute for Nuclear Research (Dubna) and Berkeley (credit shared)', 'Dubna, USSR; Berkeley, USA',
  'Dubna bombarded plutonium with neon. Berkeley bombarded californium with carbon.',
  '“Kurchatovium” (Ku) in the Soviet bloc, and temporarily “unnilquadium”.',
  'Its name was fought over for 30 years in the “Transfermium Wars” and settled only in 1997.')
e(105, '1968 · 1970', 1970, S, 'Joint Institute for Nuclear Research (Dubna) and Berkeley (credit shared)', 'Dubna, USSR; Berkeley, USA',
  'Dubna bombarded americium with neon. Berkeley bombarded californium with nitrogen.',
  '“Nielsbohrium” (Ns) in the Soviet bloc, “hahnium” (Ha) in the US, and briefly “joliotium”.',
  'The 1975 spiral chart this site is based on labels element 105 “Ha, proposed”, the old American name.')
e(106, '1974', 1974, S, 'Albert Ghiorso and team', 'Berkeley, California, USA',
  'Bombarded californium-249 with oxygen-18 ions.',
  'Temporarily “unnilhexium”. Named after Glenn Seaborg.',
  'It was the first element named after a living person. Seaborg joked he could get mail addressed in elements: seaborgium, lawrencium, berkelium, californium, americium.')
e(107, '1981', 1981, S, 'Peter Armbruster and Gottfried Münzenberg', 'GSI, Darmstadt, West Germany',
  'Fused chromium-54 with bismuth-209 in the “cold fusion” method pioneered at Dubna.',
  'Proposed as “nielsbohrium”. IUPAC shortened it to bohrium, since no other element uses a first name.',
  'Named after Niels Bohr, whose atomic model predicted element 72 decades earlier.')
e(108, '1984', 1984, S, 'Peter Armbruster and Gottfried Münzenberg', 'GSI, Darmstadt, West Germany',
  'Fused iron-58 with lead-208.',
  'Temporarily “unniloctium”. Named after the German state of Hesse.',
  'Calculations suggest that, if enough could be made, it would be the densest substance of all, at over 27 g/cm³.')
e(109, '1982', 1982, S, 'Peter Armbruster and Gottfried Münzenberg', 'GSI, Darmstadt, West Germany',
  'Fused iron-58 with bismuth-209. The discovery rested on a single atom.',
  'Temporarily “unnilennium”. Named after Lise Meitner.',
  'Meitner helped explain nuclear fission but was left out of the Nobel Prize; this element was named in her honour.')
e(110, '1994', 1994, S, 'Sigurd Hofmann and team', 'GSI, Darmstadt, Germany',
  'Fused nickel-62 with lead-208.',
  'Temporarily “ununnilium”. Named after Darmstadt.',
  'The team considered calling it “wixhausium”, after the Darmstadt district where the lab sits.')
e(111, '1994', 1994, S, 'Sigurd Hofmann and team', 'GSI, Darmstadt, Germany',
  'Fused nickel-64 with bismuth-209.',
  'Temporarily “unununium” (Uuu). Named after Wilhelm Röntgen, discoverer of X-rays.',
  'It was discovered almost exactly 99 years after Röntgen found X-rays.')
e(112, '1996', 1996, S, 'Sigurd Hofmann and team', 'GSI, Darmstadt, Germany',
  'Fused zinc-70 with lead-208.',
  'Temporarily “ununbium”. Named after Nicolaus Copernicus.',
  'The name was made official on 19 February 2010, Copernicus’s birthday.')
e(113, '2004', 2004, S, 'Kōsuke Morita and team', 'RIKEN, Wakō, Japan',
  'Fused zinc-70 with bismuth-209. The team saw just three atoms in nine years.',
  'Temporarily “ununtrium”. Named after Nihon, Japan.',
  'It was the first element discovered in Asia.')
e(114, '1999', 1999, S, 'Yuri Oganessian and team (Dubna, with Lawrence Livermore)', 'Dubna, Russia',
  'Fused calcium-48 with plutonium-244.',
  'Temporarily “ununquadium”. Named after the Flerov Laboratory of Nuclear Reactions.',
  'Theory suggests it may behave almost like a noble gas, which would make it a very odd metal.')
e(115, '2003', 2003, S, 'Yuri Oganessian and team (Dubna, with Lawrence Livermore)', 'Dubna, Russia',
  'Fused calcium-48 with americium-243.',
  'Temporarily “ununpentium”. Named after the Moscow region.',
  'Its decay chain produced Dubna’s first atoms of element 113.')
e(116, '2000', 2000, S, 'Yuri Oganessian and team (Dubna, with Lawrence Livermore)', 'Dubna, Russia',
  'Fused calcium-48 with curium-248.',
  'Temporarily “ununhexium”. Named after Livermore, California.',
  'Its longest-lived known isotope survives for less than a tenth of a second.')
e(117, '2010', 2010, S, 'Yuri Oganessian and team (Dubna, Oak Ridge, Vanderbilt and Lawrence Livermore)', 'Dubna, Russia',
  'Fused calcium-48 with berkelium-249. The berkelium was made in a reactor at Oak Ridge and flown to Russia.',
  'Temporarily “ununseptium”. Named after Tennessee.',
  'It is the most recently discovered element. The rare berkelium target was delayed in customs on its way to Russia.')
e(118, '2002', 2002, S, 'Yuri Oganessian and team (Dubna, with Lawrence Livermore)', 'Dubna, Russia',
  'Fused calcium-48 with californium-249. Only a handful of atoms have ever been made.',
  'Temporarily “ununoctium”. A 1999 Berkeley claim was retracted.',
  'Named after Yuri Oganessian, it is only the second element named after a living person.')

assert len(H) == 118 and sorted(H) == list(range(1, 119)), sorted(set(range(1, 119)) - set(H))
json.dump(H, open('history.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('ok', sum(len(json.dumps(v)) for v in H.values()))
