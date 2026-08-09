# -*- coding: utf-8 -*-
import io, json, glob, collections

fields = collections.Counter()
per_lib = {}
allkeys = set()
for f in glob.glob(r'extract\generated_assets\*.json'):
    try:
        d = json.load(io.open(f, encoding='utf-8'))
    except Exception as e:
        print('SKIP', f, e)
        continue
    chs = d.get('chapters', []) if isinstance(d, dict) else []
    ks = collections.Counter()
    for ch in chs:
        for a in ch.get('assets', []):
            for k in a:
                ks[k] += 1
                fields[k] += 1
                allkeys.add(k)
    name = f.split('\\')[-1]
    per_lib[name] = dict(ks)

print('TOTAL field usage across all assets:')
for k, v in fields.most_common():
    print('  %-28s %d' % (k, v))
