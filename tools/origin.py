# Cosmic origin of the elements for Elements in Style.
#
# Categories follow Jennifer Johnson's "Origin of the Elements" periodic table (Ohio State / SDSS, 2017;
# updated 2019) and the NASA Goddard version of it. Johnson did not publish a numeric table, so the
# fractions here are approximate and were assembled from the standard picture:
#   * light elements: Big Bang nucleosynthesis, cosmic-ray spallation, stellar burning;
#   * iron peak: split between core-collapse supernovae and Type Ia (white-dwarf) supernovae;
#   * beyond iron: solar s-process shares (slow neutron capture, mostly in dying low-mass AGB stars;
#     the "weak" s-process for Ga–Zr in massive stars) after Bisterzo et al. 2014 and Prantzos et al. 2020,
#     with the remaining r-process share credited to merging neutron stars, as Johnson does, and small
#     p-process shares to massive stars.
# Fractions are for the Solar System's supply. Earth-specific notes cover elements that on Earth come
# mainly from radioactive decay or from people.
import json

BB, CR, LM, MS, WD, NS, RD, HM = 'bb', 'cr', 'lm', 'ms', 'wd', 'ns', 'rd', 'hm'
F = {
 1: {BB: 1}, 2: {BB: .9, LM: .05, MS: .05}, 3: {BB: .25, CR: .15, LM: .6}, 4: {CR: 1}, 5: {CR: .7, MS: .3},
 6: {LM: .5, MS: .5}, 7: {LM: .6, MS: .4}, 8: {MS: 1}, 9: {LM: .5, MS: .5}, 10: {MS: 1},
 11: {MS: .85, LM: .15}, 12: {MS: 1}, 13: {MS: .95, LM: .05}, 14: {MS: .85, WD: .15}, 15: {MS: 1},
 16: {MS: .8, WD: .2}, 17: {MS: .8, WD: .2}, 18: {MS: .75, WD: .25}, 19: {MS: .9, WD: .1}, 20: {MS: .75, WD: .25},
 21: {MS: 1}, 22: {MS: .75, WD: .25}, 23: {MS: .55, WD: .45}, 24: {WD: .6, MS: .4}, 25: {WD: .75, MS: .25},
 26: {WD: .6, MS: .4}, 27: {MS: .55, WD: .45}, 28: {WD: .55, MS: .45}, 29: {MS: .8, LM: .2}, 30: {MS: .8, LM: .15, NS: .05},
 31: {MS: .6, LM: .3, NS: .1}, 32: {MS: .5, LM: .35, NS: .15}, 33: {MS: .45, LM: .2, NS: .35}, 34: {MS: .45, LM: .15, NS: .4},
 35: {MS: .4, LM: .15, NS: .45}, 36: {MS: .45, LM: .25, NS: .3}, 37: {LM: .3, MS: .2, NS: .5}, 38: {LM: .6, MS: .2, NS: .2},
 39: {LM: .65, MS: .1, NS: .25}, 40: {LM: .6, MS: .05, NS: .35}, 41: {LM: .55, NS: .45}, 42: {LM: .4, MS: .2, NS: .4},
 43: {HM: 1}, 44: {LM: .3, MS: .07, NS: .63}, 45: {LM: .15, NS: .85}, 46: {LM: .45, NS: .55}, 47: {LM: .2, NS: .8},
 48: {LM: .6, NS: .4}, 49: {LM: .35, NS: .65}, 50: {LM: .6, NS: .35, MS: .05}, 51: {LM: .25, NS: .75}, 52: {LM: .2, NS: .8},
 53: {LM: .05, NS: .95}, 54: {LM: .2, NS: .8}, 55: {LM: .15, NS: .85}, 56: {LM: .85, NS: .15}, 57: {LM: .7, NS: .3},
 58: {LM: .8, NS: .2}, 59: {LM: .5, NS: .5}, 60: {LM: .55, NS: .45}, 61: {HM: 1}, 62: {LM: .3, NS: .67, MS: .03},
 63: {LM: .06, NS: .94}, 64: {LM: .15, NS: .85}, 65: {LM: .07, NS: .93}, 66: {LM: .13, NS: .87}, 67: {LM: .08, NS: .92},
 68: {LM: .15, NS: .85}, 69: {LM: .13, NS: .87}, 70: {LM: .32, NS: .68}, 71: {LM: .2, NS: .8}, 72: {LM: .55, NS: .45},
 73: {LM: .4, NS: .6}, 74: {LM: .6, NS: .4}, 75: {LM: .09, NS: .91}, 76: {LM: .09, NS: .91}, 77: {LM: .02, NS: .98},
 78: {LM: .05, NS: .95}, 79: {LM: .06, NS: .94}, 80: {LM: .6, NS: .4}, 81: {LM: .75, NS: .25}, 82: {LM: .8, NS: .2},
 83: {LM: .3, NS: .7}, 84: {RD: 1}, 85: {RD: 1}, 86: {RD: 1}, 87: {RD: 1}, 88: {RD: 1}, 89: {RD: 1},
 90: {NS: 1}, 91: {RD: 1}, 92: {NS: 1},
}
for z in range(93, 119):
    F[z] = {HM: 1}

NOTES = {
 1: 'Every hydrogen atom in your body is about 13.8 billion years old.',
 2: 'Most helium in the universe is from the Big Bang, but the helium in party balloons comes from rocks: alpha particles from decaying uranium and thorium, trapped underground with natural gas.',
 3: 'Lithium is the odd one out: the Big Bang made some, cosmic rays a little, and dying stars most of the rest, yet stars also destroy it, so there is far less than models first predicted.',
 4: 'Stars destroy beryllium rather than make it. Nearly all of it comes from cosmic rays smashing carbon, nitrogen and oxygen nuclei in space.',
 5: 'Most boron is chipped off heavier nuclei by cosmic rays; some boron-11 is made by the neutrino blast of exploding stars.',
 6: 'About half of your carbon was puffed out by dying Sun-like stars, half by massive stars.',
 8: 'The oxygen you breathe was forged inside massive stars and blasted out when they exploded.',
 18: 'On Earth, 99.6% of argon is argon-40, made in rocks by the radioactive decay of potassium-40. That is why our air holds so much of it.',
 26: 'Iron comes from two kinds of supernova: exploding white dwarfs make a little more than half, collapsing massive stars the rest.',
 43: 'Technetium has no stable isotope. Any it was born with decayed long ago; tiny traces form in uranium ores, but almost all of it on Earth is made in nuclear reactors.',
 47: 'Silver is mostly from the rapid neutron capture of merging neutron stars, the same violent process that made gold.',
 56: 'Barium is a classic slow neutron-capture element, built a neutron at a time inside dying red giant stars over thousands of years.',
 61: 'Promethium has no stable isotope. A few hundred grams exist in Earth’s crust at any moment, from uranium fission; what people use is made in reactors.',
 63: 'Europium is the textbook tracer of the rapid neutron-capture process, so astronomers use it to track neutron-star mergers through cosmic history.',
 79: 'Most of the gold in your jewellery was made when two neutron stars collided, before the Sun was born.',
 82: 'Most lead was built slowly in dying red giants, and some on Earth is the end point of uranium and thorium decay.',
 84: 'On Earth, polonium only exists because uranium keeps decaying in rocks. Marie Curie found it in that decay chain.',
 86: 'Radon seeps out of the ground because uranium in rocks is always decaying into it.',
 90: 'Thorium and uranium were made by merging neutron stars before the Solar System formed. Their slow decay still heats Earth’s interior today.',
 92: 'Uranium was made by merging neutron stars billions of years ago, and it is still decaying. Earth’s uranium is a cosmic clock.',
}
EARTH = {
 2: 'On Earth, the helium people extract is mostly from radioactive decay in rocks.',
 18: 'On Earth, argon is almost all from the radioactive decay of potassium-40.',
 43: 'On Earth: human-made in reactors; natural traces form from uranium fission.',
 61: 'On Earth: human-made in reactors; natural traces form from uranium fission.',
 84: 'On Earth: produced continuously by the decay of uranium and thorium, which came from merging neutron stars.',
 85: 'On Earth: produced continuously by the decay of uranium and thorium.',
 86: 'On Earth: produced continuously by the decay of uranium and thorium.',
 87: 'On Earth: produced continuously by the decay of uranium (about 30 g exists in the crust at any moment).',
 88: 'On Earth: produced continuously by the decay of uranium and thorium.',
 89: 'On Earth: produced continuously by the decay of uranium and thorium.',
 91: 'On Earth: produced continuously by the decay of uranium.',
 93: 'Traces form naturally in uranium ores, but almost all neptunium is made in reactors.',
 94: 'Traces form naturally in uranium ores, but almost all plutonium is made in reactors.',
}
out = {}
for z, f in F.items():
    s = sum(f.values())
    assert abs(s - 1) < 1e-9, (z, s)
    out[z] = {'f': f}
    if z in NOTES: out[z]['note'] = NOTES[z]
    if z in EARTH: out[z]['earth'] = EARTH[z]
assert sorted(out) == list(range(1, 119))
json.dump(out, open('origin.json', 'w'), ensure_ascii=False, separators=(',', ':'))
print('ok', len(out))
