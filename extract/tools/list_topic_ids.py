# -*- coding: utf-8 -*-
import io, re, glob, os
for f in sorted(glob.glob(r'data\topics\topic-*.js')):
    s = io.open(f, encoding='utf-8').read()
    m = re.search(r'id: "([a-z0-9-]+)"', s)
    n = re.search(r'name: "([^"]+)"', s)
    print(os.path.basename(f), '->', m.group(1) if m else '?', '|', n.group(1) if n else '?')