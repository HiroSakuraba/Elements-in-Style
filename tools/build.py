"""Assemble index.html from template.html plus the two generated data files.

Run from this folder, in order:
    python3 extract_elements.py   # -> elements.json  (needs: pip install mendeleev)
    node lda_atoms.js             # -> radial.json    (self-consistent atom solver, ~30 s)
    python3 history.py            # -> history.json   (discovery history and fun facts)
    python3 build.py              # -> ../index.html
"""
import base64, json, struct

elements = json.load(open('elements.json'))
radial = json.load(open('radial.json'))
history = json.load(open('history.json'))

atoms = {}
for z, rec in radial['atoms'].items():
    atoms[z] = {k: {'E': v['E'], 'rbar': v['rbar'], 's': v['s'],
                    'b': base64.b64encode(struct.pack('<%dh' % len(v['q']), *v['q'])).decode()}
                for k, v in rec.items()}
rad = json.dumps({'XA': radial['XA'], 'DX': radial['DX'], 'NG': radial['NG'], 'atoms': atoms}, separators=(',', ':'))
data = json.dumps(elements, separators=(',', ':'), ensure_ascii=False).replace('</', '<\\/')

body = open('template.html').read().replace('__DATA__', data).replace('__RAD__', rad).replace('__HIST__', json.dumps(history, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))
body = body.replace('<title>Periodic Spiral</title>', '<title>Elements in Style</title>', 1)
body = body.replace('<h1>Periodic Spiral</h1>', '<h1>Elements in Style</h1>', 1)
head, rest = body.split('</style>', 1)
doc = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
       '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
       + head + '</style>\n</head>\n<body>\n' + rest + '\n</body>\n</html>\n')
open('../index.html', 'w').write(doc)
print('wrote ../index.html', len(doc), 'bytes')
