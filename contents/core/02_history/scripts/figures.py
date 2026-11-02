import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")

def fig_timeline():
    W, H = 1100, 470
    s = SVG(W, H)
    x0, x1 = 60, 1040
    y = 250
    y_from, y_to = 1960, 2027
    def X(yr):
        segs = [(1960, 2011.5, 60, 430), (2011.5, 2019.5, 430, 620), (2019.5, 2027, 620, 1040)]
        for a, b, xa, xb in segs:
            if yr <= b: return xa + (yr - a) / (b - a) * (xb - xa)
        return xb
    s.text(W / 2, 30, "计算药物设计的三次浪潮（1960–2026）", 16, "middle", 700)
    # eras
    eras = [(1960, 2011, "第一次浪潮：计算化学与物理方法", OI["gray"]),
            (2012, 2019.9, "第二次：深度学习进入化学", OI["blue"]),
            (2020, 2026.9, "第三次：结构预测与生成式基础模型", OI["crimson"])]
    for a, b, lab, c in eras:
        s.rect(X(a), y - 18, X(b) - X(a), 36, c, tint=0.16, rx=4)
    s.text((X(1960) + X(2011)) / 2, y + 5, eras[0][2], 12.5, "middle", 600, OI["black"])
    s.text((X(2012) + X(2020)) / 2, y + 5, "深度学习", 12.5, "middle", 600, OI["blue"])
    s.text((X(2020) + X(2027)) / 2, y + 5, "基础模型", 12.5, "middle", 600, OI["crimson"])
    # axis ticks
    for yr in [1960, 1970, 1980, 1990, 2000, 2010, 2015]:
        s.line(X(yr), y + 18, X(yr), y + 26, OI["black"], 1, head=None)
        s.text(X(yr), y + 42, str(yr), 11, "middle", 400, "#444")
    s.text(W - 20, H - 12, "注：横轴为分段刻度，2012 年后的区间被放大", 10.5, "end", 400, "#666")
    # milestones: (year, label, up/down level)
    up = [(1964, "Hansch–藤田：QSAR", 4), (1982, "DOCK 分子对接", 3), (1988, "CoMFA 三维 QSAR", 2),
          (1995, "HIV 蛋白酶抑制剂", 1), (2010, "ECFP 指纹 / FEP 走向实用", 4), (2012, "默克 Kaggle 竞赛", 3),
          (2017, "MPNN 框架", 2), (2019, "Chemprop；GENTRL", 1)]
    for yr, lab, lv in up:
        yy = y - 30 - lv * 34
        s.line(X(yr), y - 18, X(yr), yy + 4, OI["gray"], 1, head=None)
        s.circle(X(yr), y - 18, 3.5, OI["black"], fill=OI["black"])
        s.text(X(yr) - 4, yy, lab, 11.5, "start", 400)
    dn = [(2020, "AlphaFold2 在 CASP14 达到近实验精度"), (2021, "AlphaFold 结构数据库；Isomorphic Labs 成立"),
          (2022, "ProteinMPNN；ESMFold"), (2023, "RFdiffusion"),
          (2024, "AlphaFold3；Boltz-1；诺贝尔化学奖"), (2025, "Boltz-2 开源；rentosertib IIa 结果发表"),
          (2026, "首个端到端 AI 药物进入 III 期")]
    nums = "①②③④⑤⑥⑦"
    for i, (yr, lab) in enumerate(dn):
        cx = X(yr)
        s.line(cx, y + 18, cx, y + 54, OI["crimson"], 1, head=None)
        s.circle(cx, y + 64, 10, OI["crimson"], fill="#ffffff", sw=1.3)
        s.text(cx, y + 68.5, str(i + 1), 11, "middle", 700, OI["crimson"])
    # key in two columns
    kx = [560, 800]; ky = y + 100
    for i, (yr, lab) in enumerate(dn):
        col = 0 if i < 4 else 1
        row = i if i < 4 else i - 4
        s.text(kx[col] - 180 * (1 - col), ky + row * 22, f"{nums[i]} {yr}  {lab}", 11.5, "start", 400)
    return s.save(os.path.join(SV, "history_timeline.svg"))

def fig_lineages():
    W, H = 1060, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "两条技术谱系的汇合：物理方法与数据驱动方法", 16, "middle", 700)
    bw, bh = 168, 62
    ys_phys, ys_data = 90, 290
    xs = [30, 230, 430, 630]
    phys = [("分子力学与对接", "DOCK、AutoDock、Glide", OI["gray"]), ("自由能微扰 FEP", "高精度、慢、贵", OI["gray"]),
            ("增强采样 + GPU", "FEP+、OpenFE", OI["gray"]), ("机器学习力场", "NequIP、MACE", OI["gray"])]
    data = [("QSAR 与描述符", "线性回归、少量特征", OI["blue"]), ("指纹 + 随机森林", "ECFP、梯度提升树", OI["blue"]),
            ("图神经网络", "MPNN、Chemprop", OI["blue"]), ("预训练与语言模型", "Uni-Mol、ESM", OI["blue"])]
    s.text(30, ys_phys - 14, "物理谱系：从第一性原理出发，需要少量数据、大量算力", 12.5, "start", 600, "#555")
    s.text(30, ys_data - 14, "数据谱系：从实验数据中学习，依赖数据规模与质量", 12.5, "start", 600, OI["blue"])
    for i, (a, b, c) in enumerate(phys):
        s.box(xs[i], ys_phys, bw, bh, a, b, color=c)
        if i < 3: s.line(xs[i] + bw, ys_phys + bh / 2, xs[i + 1], ys_phys + bh / 2, c)
    for i, (a, b, c) in enumerate(data):
        s.box(xs[i], ys_data, bw, bh, a, b, color=c)
        if i < 3: s.line(xs[i] + bw, ys_data + bh / 2, xs[i + 1], ys_data + bh / 2, c)
    # convergence node
    cx, cy, cw, ch = 850, 175, 190, 92
    s.box(cx, cy, cw, ch, "共折叠 + 亲和力基础模型", "AlphaFold3、Boltz-2、IsoDDE：扩散生成结构，数据驱动估计亲和力", color=OI["crimson"], tint=0.14)
    # curved arrows into convergence (control points outside boxes)
    s.path(f"M {xs[3]+bw} {ys_phys+bh/2} C {cx-40} {ys_phys+bh/2}, {cx-40} {cy+20}, {cx} {cy+24}", OI["gray"])
    s.path(f"M {xs[3]+bw} {ys_data+bh/2} C {cx-40} {ys_data+bh/2}, {cx-40} {cy+ch-20}, {cx} {cy+ch-24}", OI["blue"])
    # AlphaFold injection from structure-biology (PDB)
    s.box(430, 192, 300, 50, "PDB 实验结构（>20 万）+ 共进化信息", None, color=OI["green"], size=12.5, tint=0.12)
    s.line(730, 217, cx, 220, OI["green"], 1.5, dash="5,3")
    s.legend(30, 392, [("line", OI["gray"], "物理方法演进", None)], size=11)
    s.legend(230, 392, [("line", OI["blue"], "数据驱动方法演进", None)], size=11)
    s.legend(470, 392, [("line", OI["green"], "结构数据作为训练信号", "5,3")], size=11)
    return s.save(os.path.join(SV, "two_lineages.svg"))

if __name__ == "__main__":
    print(fig_timeline(), fig_lineages())
