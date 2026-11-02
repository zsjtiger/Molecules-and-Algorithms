#!/usr/bin/env python3
"""Post-render: localize cross-reference labels in generated HTML."""
import os, re, glob
OUT = os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_build")
LBL = {"Important": "原则", "Note": "定义", "Warning": "案例", "Tip": "检查点", "Caution": "标杆"}
pat = re.compile(r'(<a [^>]*class="quarto-xref"[^>]*>)(.*?)(</a>)', re.S)

def fix(m):
    a, inner, end = m.groups()
    href = re.search(r'href="([^"]*)"', a)
    href = href.group(1) if href else ""
    for en, zh in LBL.items():
        inner = inner.replace(en + "&nbsp;", zh + "&nbsp;")
    if "#sec-" in href or href.endswith(".html"):
        txt = re.sub(r"<[^>]+>", "", inner)
        mm = re.match(r"\s*第(?:&nbsp;|\s)*([0-9]+(?:\.[0-9]+)*)\s*$", txt)
        if mm:
            num = mm.group(1)
            inner = f"第&nbsp;{num}&nbsp;{'节' if '.' in num else '章'}"
    return a + inner + end

for f in glob.glob(os.path.join(OUT, "**", "*.html"), recursive=True):
    s = open(f, encoding="utf-8").read()
    t = pat.sub(fix, s)
    if t != s:
        open(f, "w", encoding="utf-8").write(t)
