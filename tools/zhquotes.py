#!/usr/bin/env python3
"""Convert ASCII double quotes in Chinese prose to “ ” (skips code, attributes, YAML, math)."""
import re, sys
def conv_segment(seg, state):
    out = []
    for ch in seg:
        if ch == '"':
            out.append('“' if state[0] else '”'); state[0] = not state[0]
        else:
            out.append(ch)
    return ''.join(out)
def convert(text):
    lines, out = text.split('\n'), []
    infence = False; inyaml = False
    for i, ln in enumerate(lines):
        st = ln.strip()
        if i == 0 and st == '---': inyaml = True; out.append(ln); continue
        if inyaml:
            if st == '---': inyaml = False
            out.append(ln); continue
        if st.startswith('```'): infence = not infence; out.append(ln); continue
        if infence or st.startswith(':::') or st.startswith('$$') or st.startswith('#|') or st.startswith('!['):
            out.append(ln); continue
        # protect {...} attribute blocks, inline code, inline math
        parts = re.split(r'(\{[^{}]*\}|`[^`]*`|\$[^$]+\$)', ln)
        state = [True]
        for j, p in enumerate(parts):
            if j % 2 == 0: parts[j] = conv_segment(p, state)
        out.append(''.join(parts))
    return '\n'.join(out)
import glob, os
targets = sys.argv[1:]
if not targets:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    targets = sorted(glob.glob(os.path.join(root, '**', '*.qmd'), recursive=True))
    targets = [t for t in targets if '/_build/' not in t]
n = 0
for f in targets:
    s = open(f, encoding='utf-8').read(); t = convert(s)
    if s != t:
        open(f, 'w', encoding='utf-8').write(t); n += 1
print(f'zhquotes: {n} file(s) converted, {len(targets)} scanned')
