#!/usr/bin/env bash
# 生成 PDF：Quarto 出 .tex -> 本地化交叉引用 -> XeLaTeX 三遍
set -euo pipefail
cd "$(dirname "$0")/.."
# 本仓库自带两个空壳宏包（lmodern / fontawesome5），避免依赖 CTAN
export TEXMFHOME="${TEXMFHOME:-$PWD/tex/texmf}"

echo "[1/3] Quarto -> LaTeX（会重建 _build）"
quarto render --to latex >/dev/null

TEXDIR=_build/book-latex
TEX=$(ls "$TEXDIR"/*.tex | head -1)

echo "[2/3] 本地化交叉引用 + 放置封面图"
python3 tools/fix-tex.py "$TEX"
cp -f assets/images/cover-a4.jpg "$TEXDIR/"

echo "[3/3] XeLaTeX x3"
cd "$TEXDIR"
for i in 1 2 3; do
  xelatex -interaction=batchmode -halt-on-error "$(basename "$TEX")" >/dev/null 2>&1 \
    || { echo "xelatex 第 $i 遍失败，见 $(basename "${TEX%.tex}").log"; exit 1; }
done
PDF="$(basename "${TEX%.tex}").pdf"
cd ../..
mv -f "$TEXDIR/$PDF" "./$PDF"
echo "完成: ./$PDF"
echo
echo "注意：--to latex 会重建 _build，HTML 站点需要再跑一次 quarto render"
