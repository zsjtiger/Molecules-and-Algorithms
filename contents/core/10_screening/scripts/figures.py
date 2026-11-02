import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_funnel():
    W, H = 1060, 540
    s = SVG(W, H)
    s.text(W / 2, 28, "虚拟筛选级联：逐级收窄，逐级变贵", 15.5, "middle", 700)
    stages = [("化合物库", "100 万 – 100 亿", "枚举库或按需合成库", OI["gray"]),
              ("规则与药效团过滤", "10 万 – 1000 万", "理化性质、子结构、形状匹配", OI["blue"]),
              ("分子对接", "1000 – 10 万", "刚性受体打分，速度优先", OI["sky"]),
              ("重打分 / MM-GBSA", "100 – 1000", "引入溶剂化与柔性，中等精度", OI["green"]),
              ("自由能微扰（FEP）", "10 – 100", "物理最严格，算力最贵", OI["orange"]),
              ("实验测定", "5 – 50", "唯一的事实来源", OI["crimson"])]
    y0, h, gap = 60, 62, 10
    for i, (a, n, b, c) in enumerate(stages):
        y = y0 + i * (h + gap)
        wfrac = 1.0 - i * 0.11
        bw = int(620 * wfrac)
        x = 40 + (620 - bw) // 2
        s.box(x, y, bw, h, a, None, color=c, size=13.5, tint=0.16)
        s.text(690, y + 26, n + " 个分子", 12.5, "start", 700, c)
        s.text(690, y + 48, b, 11.5, "start", 400, "#555")
        if i < len(stages) - 1:
            s.line(350, y + h, 350, y + h + gap, OI["black"], 1.3)
    s.text(40, 522, "每一级的任务不是选出最好的分子，而是在不丢掉真阳性的前提下尽量减少进入下一级的数量。",
           12, "start", 600, "#444")
    return s.save(os.path.join(SV, "screening_funnel.svg"))


def fig_accuracy_cost():
    plt = mpl_setup()
    methods = [("药效团 / 形状匹配", 3.5e-4, 3.0, OI["blue"]),
               ("机器学习打分", 2e-3, 2.2, OI["sky"]),
               ("分子对接", 1e-2, 2.0, OI["sky"]),
               ("MM-GBSA 重打分", 2.0, 1.6, OI["green"]),
               ("绝对自由能计算", 200.0, 1.2, OI["orange"]),
               ("相对自由能微扰", 60.0, 1.0, OI["orange"]),
               ("实验测定（SPR/ITC）", 2000.0, 0.3, OI["crimson"])]
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    for name, cost, err, c in methods:
        ax.plot(cost, err, "o", color=c, ms=10)
        ax.annotate(name, (cost, err), textcoords="offset points",
                    xytext=(0, 13), ha="center", fontsize=10.5)
    ax.set_xscale("log")
    ax.set_xlabel("每个分子的大致算力 / 实验成本（相对单位，对数轴）")
    ax.set_ylabel("典型预测误差（kcal/mol）")
    ax.set_ylim(0, 3.6); ax.set_xlim(1e-4, 1e4)
    ax.axhline(1.4, color="#bbb", lw=0.9, ls="--")
    ax.text(1.3e-4, 1.48, "1.4 kcal/mol ≈ 10 倍亲和力差异", fontsize=10, color="#666")
    ax.set_title("精度与成本的权衡：没有既便宜又准确的方法", loc="left")
    ax.text(0.0, -0.26, "数值为公开文献报道的量级区间，具体体系差异很大，不应作为基准引用。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.24)
    return save_chart(fig, os.path.join(SV, "accuracy_cost.svg"))


def fig_docking_gap():
    W, H = 1000, 462
    s = SVG(W, H)
    s.text(W / 2, 28, "对接打分为什么与真实亲和力相关性不高", 15.5, "middle", 700)
    s.box(40, 70, 290, 64, "对接打分函数计算的", "受体与配体之间的相互作用能近似",
          color=OI["sky"], size=13.5, subsize=11, tint=0.14)
    s.box(660, 70, 300, 64, "真实结合自由能包含", "焓、熵、溶剂化与构象变化的总和",
          color=OI["crimson"], size=13.5, subsize=11, tint=0.14)
    s.text(500, 106, "≠", 24, "middle", 700, "#444")
    gaps = [("去溶剂化代价", "配体与口袋结合前都要脱去水合壳层，\n这部分能量往往与结合能同数量级"),
            ("熵损失", "配体固定在口袋中会损失平动、转动与构象自由度，\n打分函数通常只用经验项粗略近似"),
            ("受体柔性", "多数对接把受体视为刚性，忽略诱导契合与口袋开合"),
            ("打分函数的拟合来源", "参数拟合自已知复合物，外推到新骨架时系统性偏差明显")]
    for i, (a, b) in enumerate(gaps):
        y = 164 + i * 66
        s.box(40, y, 260, 54, a, None, color=OI["purple"], size=12.5, tint=0.13)
        lines = b.split("\n")
        s.text(320, y + (24 if len(lines) > 1 else 32), lines[0], 12, "start", 400)
        if len(lines) > 1:
            s.text(320, y + 44, lines[1], 12, "start", 400)
    s.text(40, 452, "实践结论：对接适合做富集排序，不适合做亲和力预测——两者是不同的任务。",
           12.5, "start", 700, OI["crimson"])
    return s.save(os.path.join(SV, "docking_gap.svg"))


def fig_ultralarge():
    W, H = 1020, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "超大库筛选：穷举对接与主动学习的两条路线", 15.5, "middle", 700)
    s.box(30, 66, 470, 46, "问题：按需合成库已达百亿量级，全部对接在算力上不可行", None,
          color=OI["gray"], size=12.5, tint=0.10)
    s.box(530, 66, 460, 46, "两条路线都不改变打分函数本身的精度上限", None,
          color=OI["gray"], size=12.5, tint=0.10)
    s.box(30, 140, 470, 110, "路线一：穷举式分布式对接",
          "把全库切片分发到大规模计算集群，逐个对接。优点是无偏；缺点是成本随库规模线性增长，且重复打分大量注定低分的分子。",
          color=OI["blue"], size=14, subsize=11.5, tint=0.13)
    s.box(530, 140, 460, 110, "路线二：主动学习加速",
          "先对接一个随机子集，用结果训练代理模型预测对接分，再只对接模型认为有希望的分子，迭代若干轮。通常可用全库 1% 以内的对接量找回大部分高分分子。",
          color=OI["green"], size=14, subsize=11.5, tint=0.13)
    s.rect(30, 276, 960, 54, OI["crimson"], tint=0.10, rx=6)
    s.text(510, 298, "两条路线共同的天花板：召回的是“对接分高的分子”，不是“真正有活性的分子”",
           13, "middle", 700, OI["crimson"])
    s.text(510, 320, "扩大库规模提高的是命中数量，而非命中率", 11.5, "middle", 400, "#555")
    s.text(30, 368, "因此超大库筛选的价值取决于两个前提：靶点口袋适合对接，且下游有足够的实验通量验证。",
           12, "start", 400, "#444")
    s.text(30, 398, "两者有一个不满足时，扩大库规模只会同比例放大假阳性。", 12, "start", 600, "#444")
    return s.save(os.path.join(SV, "ultra_large.svg"))


if __name__ == "__main__":
    print(fig_funnel(), fig_docking_gap(), fig_ultralarge())
    print(fig_accuracy_cost())
