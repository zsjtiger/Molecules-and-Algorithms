"""figkit — shared figure helpers for the book.

Schematic diagrams follow the academic-diagram skill (Style B: Okabe–Ito accent,
semantic arrows, legend when >=2 arrow styles, SVG built as a list of lines,
validated, exported to PDF + 3x PNG). Data charts follow AcademicForge
figure-style (apply_figure_style). Molecules are drawn with RDKit.
"""
import os, subprocess, sys, math, html

# ---------------------------------------------------------------- palette
OI = {
    "black": "#1a1a1a", "orange": "#E69F00", "sky": "#56B4E9",
    "green": "#009E73", "yellow": "#F0E442", "blue": "#0072B2",
    "verm": "#D55E00", "purple": "#CC79A7", "gray": "#7a7a7a",
    "lgray": "#bdbdbd", "crimson": "#A51C30",
}
FONT = "'Noto Sans CJK SC','Noto Sans SC','PingFang SC','Microsoft YaHei',Helvetica,Arial,sans-serif"
SKILL_DIR = "/root/.claude/skills/synced/0b074efa-f0b9-4610-8894-9d558887faf3_b59618eb-219f-4a14-9faf-89720dc544af/academic-diagram"


def text_width(s, size):
    """Rough rendered width: CJK ~1.0em, ASCII ~0.56em."""
    w = 0.0
    for ch in s:
        w += size * (1.0 if ord(ch) > 0x2E80 else 0.56)
    return w


def wrap(s, size, maxw):
    """Greedy wrap that respects CJK (char-level) and ASCII words."""
    lines, cur = [], ""
    tokens, buf = [], ""
    for ch in s:
        if ord(ch) > 0x2E80 or ch == " ":
            if buf:
                tokens.append(buf); buf = ""
            tokens.append(ch)
        else:
            buf += ch
    if buf:
        tokens.append(buf)
    NOSTART = set("，。；：、）》」』！？,.;:)%")
    for t in tokens:
        if text_width(cur + t, size) <= maxw or not cur or (t and t[0] in NOSTART):
            cur += t
        else:
            lines.append(cur.strip()); cur = t.lstrip()
    if cur.strip():
        lines.append(cur.strip())
    return lines


class SVG:
    def __init__(self, w, h, bg="#ffffff"):
        self.w, self.h = w, h
        self.L = []
        self.L.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">')
        self.L.append(f'  <style>text {{ font-family: {FONT}; }}</style>')
        self.L.append('  <defs>')
        for name, col in OI.items():
            self.L.append(f'    <marker id="ar-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{col}"/></marker>')
            self.L.append(f'    <marker id="ah-{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#ffffff" stroke="{col}" stroke-width="1.3"/></marker>')
        self.L.append('  </defs>')
        self.L.append(f'  <rect width="{w}" height="{h}" fill="{bg}"/>')

    # ---- primitives
    def text(self, x, y, s, size=13, anchor="middle", weight=400, color=OI["black"], italic=False):
        st = ' font-style="italic"' if italic else ''
        self.L.append(f'  <text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{color}"{st}>{html.escape(s)}</text>')

    def mtext(self, x, y, lines, size=13, anchor="middle", weight=400, color=OI["black"], lh=1.3):
        """Multi-line text block vertically centred on y."""
        n = len(lines)
        y0 = y - (n - 1) * size * lh / 2 + size * 0.35
        for i, s in enumerate(lines):
            self.text(x, y0 + i * size * lh, s, size, anchor, weight, color)

    def rect(self, x, y, w, h, color=OI["black"], fill=None, rx=6, dashed=False, sw=1.5, tint=0.10):
        fo = ''
        if fill is None:
            fill, fo = color, f' fill-opacity="{tint}"'
        d = ' stroke-dasharray="5,3"' if dashed else ''
        self.L.append(f'  <rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" ry="{rx}" fill="{fill}"{fo} stroke="{color}" stroke-width="{sw}"{d}/>')

    def box(self, x, y, w, h, label, sub=None, color=OI["black"], size=13, subsize=10.5,
            weight=600, dashed=False, fill=None, rx=6, tint=0.10, pad=8):
        """Rounded node with wrapped label (+ optional wrapped sub-label)."""
        self.rect(x, y, w, h, color, fill, rx, dashed, tint=tint)
        ll = wrap(label, size, w - 2 * pad)
        sl = wrap(sub, subsize, w - 2 * pad) if sub else []
        tot = len(ll) * size * 1.3 + (len(sl) * subsize * 1.3 + 3 if sl else 0)
        ytop = y + h / 2 - tot / 2
        for i, s in enumerate(ll):
            self.text(x + w / 2, ytop + size * 0.95 + i * size * 1.3, s, size, "middle", weight)
        yb = ytop + len(ll) * size * 1.3 + 3
        for i, s in enumerate(sl):
            self.text(x + w / 2, yb + subsize * 0.95 + i * subsize * 1.3, s, subsize, "middle", 400, "#444444")
        return (x, y, w, h)

    def line(self, x1, y1, x2, y2, color=OI["black"], sw=1.5, dash=None, head="ar", tail=False, opacity=1.0):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        cname = [k for k, v in OI.items() if v == color]
        cname = cname[0] if cname else "black"
        me = f' marker-end="url(#{head}-{cname})"' if head else ''
        ms = f' marker-start="url(#{head}-{cname})"' if (tail and head) else ''
        op = f' opacity="{opacity}"' if opacity < 1 else ''
        self.L.append(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{color}" stroke-width="{sw}"{d}{me}{ms}{op}/>')

    def path(self, d, color=OI["black"], sw=1.5, dash=None, head="ar", fill="none"):
        dd = f' stroke-dasharray="{dash}"' if dash else ''
        cname = [k for k, v in OI.items() if v == color]
        cname = cname[0] if cname else "black"
        me = f' marker-end="url(#{head}-{cname})"' if head else ''
        self.L.append(f'  <path d="{d}" fill="{fill}" stroke="{color}" stroke-width="{sw}"{dd}{me}/>')

    def arc_arrow(self, a, b, bulge=0.26, color=OI["black"], sw=1.6, head="ar"):
        """从 a 点到 b 点画一段圆弧箭头。

        bulge 为弧高与弦长之比：正值向顺时针一侧外凸，负值反向。
        调用方负责把 a、b 放在方框边界上，这样箭头头部正好抵住方框。
        """
        (x0, y0), (x1, y1) = a, b
        L = math.hypot(x1 - x0, y1 - y0) or 1.0
        h = abs(bulge) * L
        r = (L * L / 4 + h * h) / (2 * h)  # 由弦长与弧高反推半径
        sweep = 1 if bulge > 0 else 0
        self.path(f"M {x0:.1f} {y0:.1f} A {r:.1f} {r:.1f} 0 0 {sweep} {x1:.1f} {y1:.1f}",
                  color, sw, head=head)

    def poly(self, pts, color=OI["black"], fill=None, sw=1.5, tint=0.10):
        fo = ''
        if fill is None:
            fill, fo = color, f' fill-opacity="{tint}"'
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.L.append(f'  <polygon points="{p}" fill="{fill}"{fo} stroke="{color}" stroke-width="{sw}"/>')

    def circle(self, cx, cy, r, color=OI["black"], fill=None, sw=1.5, tint=0.12):
        fo = ''
        if fill is None:
            fill, fo = color, f' fill-opacity="{tint}"'
        self.L.append(f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}"{fo} stroke="{color}" stroke-width="{sw}"/>')

    def legend(self, x, y, items, size=11, title=None):
        """items: list of (kind, color, label, dash) kind in {'line','box','hollow'}"""
        yy = y
        if title:
            self.text(x, yy, title, size, "start", 600); yy += size * 1.5
        for kind, col, lab, dash in items:
            if kind == "box":
                self.rect(x, yy - size * 0.8, 18, size, col, rx=2, tint=0.3)
            elif kind == "hollow":
                self.line(x, yy - size * 0.35, x + 26, yy - size * 0.35, col, 1.5, dash, head="ah")
            else:
                self.line(x, yy - size * 0.35, x + 26, yy - size * 0.35, col, 1.5, dash)
            self.text(x + 34, yy, lab, size, "start")
            yy += size * 1.6

    # ---- output
    def save(self, path, export=True):
        self.L.append('</svg>')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.L))
        v = subprocess.run(["bash", f"{SKILL_DIR}/scripts/validate-svg.sh", path], capture_output=True, text=True)
        ok = v.returncode == 0
        if not ok:
            print(v.stdout[-800:], v.stderr[-800:], file=sys.stderr)
        if export:
            export_svg(path)
        return ok


def export_svg(svg_path):
    """SVG -> PDF (vector) + 3x PNG in ../png/ next to svg dir."""
    import cairosvg
    d = os.path.dirname(svg_path)
    base = os.path.splitext(os.path.basename(svg_path))[0]
    pdir = os.path.join(os.path.dirname(d), "png")
    os.makedirs(pdir, exist_ok=True)
    cairosvg.svg2png(url=svg_path, write_to=os.path.join(pdir, base + ".png"), scale=2.0)
    cairosvg.svg2pdf(url=svg_path, write_to=os.path.join(pdir, base + ".pdf"))


# ---------------------------------------------------------------- data charts
def mpl_setup():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    sys.path.insert(0, "/tmp/claude-0/-home-claude/e00e5222-2a10-57a6-b6db-4934a605f6db/scratchpad/AcademicForge/skills/claude-science/figure-style")
    try:
        from kernel import apply_figure_style
        apply_figure_style(sizes=(12.5, 11.5, 10.5))
    except Exception as e:  # fall back silently
        print("figure-style not applied:", e, file=sys.stderr)
    for p in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]:
        if os.path.exists(p):
            font_manager.fontManager.addfont(p)
    plt.rcParams["font.family"] = ["Noto Sans CJK SC", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["svg.fonttype"] = "path"
    return plt


def save_chart(fig, svg_path):
    os.makedirs(os.path.dirname(svg_path), exist_ok=True)
    fig.savefig(svg_path, bbox_inches="tight")
    pdir = os.path.join(os.path.dirname(os.path.dirname(svg_path)), "png")
    os.makedirs(pdir, exist_ok=True)
    base = os.path.splitext(os.path.basename(svg_path))[0]
    fig.savefig(os.path.join(pdir, base + ".png"), dpi=220, bbox_inches="tight")
    fig.savefig(os.path.join(pdir, base + ".pdf"), bbox_inches="tight")
    # figure-style §9.1 overlap check
    import matplotlib as mpl
    r = fig.canvas.get_renderer()
    texts = [(t, t.get_window_extent(r)) for t in fig.findobj(mpl.text.Text)
             if t.get_text().strip() and t.get_visible()]
    ov = [(a.get_text(), b.get_text()) for i, (a, ba) in enumerate(texts)
          for b, bb in texts[i + 1:] if ba.overlaps(bb)]
    if ov:
        print("TEXT OVERLAPS:", ov[:8], file=sys.stderr)
    return ov


# ---------------------------------------------------------------- molecules
def mol_svg(smiles, path, w=360, h=260, legend="", highlight=None, atom_index=False):
    from rdkit import Chem
    from rdkit.Chem.Draw import rdMolDraw2D
    from rdkit.Chem import rdDepictor
    m = Chem.MolFromSmiles(smiles)
    rdDepictor.Compute2DCoords(m)
    d = rdMolDraw2D.MolDraw2DSVG(w, h)
    o = d.drawOptions()
    o.addAtomIndices = atom_index
    o.legendFontSize = 16
    o.bondLineWidth = 2
    o.clearBackground = True
    if highlight:
        d.DrawMolecule(m, highlightAtoms=highlight, legend=legend)
    else:
        d.DrawMolecule(m, legend=legend)
    d.FinishDrawing()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(d.GetDrawingText())
    export_svg(path)


def box_edge(cx, cy, hw, hh, deg):
    """方框中心 (cx,cy)、半宽 hw、半高 hh，在 deg 方向上的边界交点。"""
    a = math.radians(deg)
    ca, sa = math.cos(a), math.sin(a)
    t = min(hw / abs(ca) if abs(ca) > 1e-9 else 1e9,
            hh / abs(sa) if abs(sa) > 1e-9 else 1e9)
    return (cx + t * ca, cy + t * sa)
