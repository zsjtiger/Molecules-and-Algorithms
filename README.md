# 分子与算法：AI 药物研发全景（2026）

Quarto 书稿，同一份源码生成 **HTML 网站**与 **PDF 电子书**
- 正文 31 章 + 3 个附录，约 16.3 万汉字
- 110 张自绘插图，每张同时产出 SVG / PNG / PDF 三种格式（PDF 供 LaTeX 使用，矢量）
- 269 条参考文献，GB/T 7714-2015 数字顺序格式

## 目录结构

```
_quarto.yml              书籍配置（html / pdf / latex 三个 format）
index.qmd                序言
references.bib           参考文献
requirements.txt         插图生成的 Python 依赖（渲染书稿不需要）
contents/
  parts/p1..p7.qmd       七个篇首页（各含 2–3 条贯穿全篇的 principle）
  core/NN_name/
    NN_name.qmd          章节正文
    scripts/figures.py   该章插图的生成脚本
    images/svg/*.svg     网页用
    images/png/*.png     预览用
    images/png/*.pdf     LaTeX 用（矢量）
  backmatter/            附录 A 术语表 / B 资源清单 / C 资料来源
filters/
  callouts.lua           MLSysBook 风格 callout → Quarto callout + 中文标题
  latex-figs.lua         仅 latex：SVG 路径改 PDF；自定义 div → tcolorbox
tools/
  figkit.py              绘图公共库（Okabe–Ito 配色、CJK 换行、重叠检测）
  zhquotes.py            ASCII 引号 → 中文弯引号
  postrender.py          HTML 交叉引用标签本地化
  fix-tex.py             LaTeX 交叉引用本地化（第 N 章 / 第 N.M 节）
  audit-arrows.py        插图静态检查（箭头穿框 / 悬空 / 元素出界）
  build-pdf.sh           PDF 构建流水线
tex/
  preamble.tex           LaTeX 导言区（中文排版、配色、盒子、标题样式、整页封面）
  texmf/                 两个空壳宏包，见下
assets/
  styles/style.scss      HTML 主题
  images/cover.jpg       封面原图（HTML 用）
  images/cover-a4.jpg    按 A4 比例居中裁切（PDF 整页封面用）
```

## 构建

### HTML

```bash
quarto render
# 输出：_build/index.html
```

### PDF

```bash
bash tools/build-pdf.sh
# 输出：./分子与算法.pdf
```

> `--to latex` 会重建 `_build/`，把 HTML 站点覆盖掉。
> 两种格式都要时，**先出 PDF 再出 HTML**：
> `bash tools/build-pdf.sh && quarto render`

PDF 不走 `quarto render --to pdf`，而是三段式：

1. `quarto render --to latex` 生成 `.tex`
2. `tools/fix-tex.py` 本地化交叉引用
3. XeLaTeX 跑三遍

**第 2 步是必需的**：Quarto 对章节引用只输出「第 18」，中文需要「第 18 章」。
脚本按标签的标题层级判断该补「章」还是「节」。HTML 侧由 `postrender.py` 做等价处理。

## 环境配置

成稿环境为 Ubuntu 24.04，实测版本如下。只渲染书稿不需要 Python 那一组——
仓库里已经带了全部 110 张插图的 SVG / PNG / PDF，改插图时才需要。

| 组件 | 本书实测版本 | 用途 | 渲染书稿必需 |
|---|---|---|:---:|
| Quarto | 1.6.42 | 书籍渲染 | 是 |
| XeTeX / TeX Live | 2023 | PDF 排版（必须是 XeLaTeX，不能用 pdfLaTeX） | 仅 PDF |
| Noto CJK 字体 | — | Serif / Sans / Sans Mono CJK SC 三套 | 仅 PDF |
| Python | 3.13 | 后处理脚本 + 插图生成 | 是 |
| matplotlib | 3.11.2 | 数据图 | 改插图时 |
| numpy | 2.5.3 | 同上 | 改插图时 |
| cairosvg | 2.9.1 | SVG → PNG / PDF | 改插图时 |
| rdkit | 2026.9.1 | 分子结构图（第 7、12 章） | 改插图时 |
| selfies | 2.2.0 | SELFIES 字符串（第 7 章） | 改插图时 |
| pillow | 12.3.0 | 封面裁切 | 改封面时 |

`tools/` 下的 `postrender.py`、`fix-tex.py`、`zhquotes.py`、`audit-arrows.py`
只用标准库，所以**渲染链本身对 Python 的要求仅是 3.9+，无第三方依赖**。

### Ubuntu / Debian

```bash
# 1. Quarto（apt 源里的版本偏旧，从官网取 deb）
wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.6.42/quarto-1.6.42-linux-amd64.deb
sudo dpkg -i quarto-1.6.42-linux-amd64.deb

# 2. XeLaTeX 与所需宏包
sudo apt install -y \
  texlive-xetex texlive-latex-recommended texlive-latex-extra \
  texlive-fonts-recommended texlive-pictures
# 提供：tcolorbox titlesec fancyhdr caption geometry microtype eso-pic xcolor

# 3. 中文字体
sudo apt install -y fonts-noto-cjk fonts-noto-cjk-extra

# 4. 插图依赖（可选）
sudo apt install -y libcairo2        # cairosvg 的系统依赖
pip install -r requirements.txt
```

### macOS

```bash
brew install --cask quarto mactex          # mactex 约 4 GB，basictex 装不全宏包
brew install cairo
brew tap homebrew/cask-fonts
brew install --cask font-noto-sans-cjk-sc font-noto-serif-cjk-sc
pip install -r requirements.txt
```

macOS 下 cairosvg 有时找不到 Homebrew 装的 libcairo，需要：

```bash
export DYLD_FALLBACK_LIBRARY_PATH="$(brew --prefix)/lib:$DYLD_FALLBACK_LIBRARY_PATH"
```

### 校验

```bash
quarto --version                           # 期望 1.6.x
xelatex --version | head -1                # 期望含 XeTeX
fc-list : family | grep -c "Noto Serif CJK SC"   # 期望 > 0
kpsewhich tcolorbox.sty                    # 应打印路径
python3 -c "import matplotlib, cairosvg, rdkit; print('插图依赖 ok')"
```

四项里前三项有任何一项不过，PDF 构建会在 XeLaTeX 阶段中断，
报错写在 `_build/book-latex/*.log` 里（`build-pdf.sh` 用的是 `batchmode`，
终端上只会看到一行「xelatex 第 N 遍失败」）。

### 关于 tex/texmf/

Pandoc 的 LaTeX 模板会无条件 `\usepackage{lmodern}`，Quarto 的 callout 代码会引用
`fontawesome5`。本书字体全部由 fontspec 指定、callout 图标已关闭，这两个宏包都用不上，
但缺失会导致编译中断。`tex/texmf/` 下放了两个**空壳实现**满足依赖，
`build-pdf.sh` 会自动把 `TEXMFHOME` 指向这里。

若你的 TeX 发行版本身带这两个包，删掉 `tex/texmf/` 并取消 `build-pdf.sh` 里的
`TEXMFHOME` 设置即可。

### 关于中文断行

环境中没有 `xeCJK`（CTAN 不可达），改用 XeTeX 内建的 CJK 断行：

```latex
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 0.08em minus 0.04em
```

效果够用。若你的环境有 `xeCJK`，在 `tex/preamble.tex` 里换成
`\usepackage{xeCJK}` 会得到更好的标点压缩与中西文间距。

## 重新生成插图

```bash
python3 contents/core/23_evaluation/scripts/figures.py
```

每个脚本独立运行，输出写回同章的 `images/` 下，三种格式一次产出。
全部重跑：

```bash
for f in contents/core/*/scripts/figures.py; do python3 "$f"; done
```

两道自检：

- `tools/figkit.py` 的 `save_chart()` 在保存数据图时做文字重叠检测并打印告警。
  图例条目之间、坐标轴标签与刻度之间常有**误报**，以肉眼为准。
- `python3 tools/audit-arrows.py` 扫描全部 SVG，报告箭头穿框、箭头悬空、
  marker 未定义、方框或文字超出画布。这一项应当是干净的。

## 已知的格式差异

- **callout 编号**：HTML 按章编号（「原则 10.1」），PDF 全书连续（「原则 13」）。
  图表编号两边一致（「图 10.3」）。自定义 callout 类型在 LaTeX 下未走章节分级。
- **强调文本**：中文无真斜体，PDF 版把 `\emph` 映射为无衬线体以作区分。
