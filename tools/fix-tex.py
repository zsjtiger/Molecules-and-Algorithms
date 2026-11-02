#!/usr/bin/env python3
"""Localize chapter/section crossrefs in the generated LaTeX.

Quarto emits  第~\ref{sec-x}  for both chapters and sections; Chinese needs
第 N 章 / 第 N.M 节.  We decide the suffix from the label's heading level.
"""
import re, sys

path = sys.argv[1]
src = open(path, encoding="utf-8").read()

# label -> heading level
level = {}
for m in re.finditer(r'\\(chapter|section|subsection|subsubsection)\*?'
                     r'(?:\[[^\]]*\])?\{(?:[^{}]|\{[^{}]*\})*\}'
                     r'\\label\{(sec-[A-Za-z0-9_-]+)\}', src):
    level[m.group(2)] = m.group(1)

def suffix(label):
    return "章" if level.get(label) == "chapter" else "节"

n = [0, 0]
def repl(m):
    lbl = m.group(1)
    s = suffix(lbl)
    n[0 if s == "章" else 1] += 1
    return "第~\\ref{%s}~%s" % (lbl, s)

out = re.sub(r'第~\\ref\{(sec-[A-Za-z0-9_-]+)\}', repl, src)

# 附录 A/B/C are referenced the same way
out = re.sub(r'附录~\\ref\{(sec-[A-Za-z0-9_-]+)\}~?章?', r'附录~\\ref{\1}', out)

if out != src:
    open(path, "w", encoding="utf-8").write(out)
print(f"fix-tex: 章 {n[0]} 处, 节 {n[1]} 处, 已知标签 {len(level)} 个")
