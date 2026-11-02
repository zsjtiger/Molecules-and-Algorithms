import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_landscape():
    W, H = 1060, 584
    s = SVG(W, H)
    s.text(W / 2, 28, "药物研发数据资源全景：按数据类型与可及性", 15.5, "middle", 700)
    cols = [("化学与活性", OI["blue"],
             ["ChEMBL：文献提取的活性数据", "PubChem：聚合型化合物库",
              "BindingDB：结合亲和力", "ZINC / Enamine REAL：可购买库"]),
            ("结构", OI["green"],
             ["PDB：实验解析的三维结构", "AlphaFold DB：预测结构",
              "PDBbind：复合物与亲和力", "EMDB：冷冻电镜图谱"]),
            ("生物与组学", OI["purple"],
             ["UniProt：蛋白序列与注释", "GEO / ArrayExpress：表达数据",
              "DepMap：细胞系基因依赖", "Open Targets：靶点证据聚合"]),
            ("临床与真实世界", OI["orange"],
             ["ClinicalTrials.gov：试验登记", "FAERS：不良事件自发报告",
              "电子病历与理赔数据（商业）", "专病队列（受限）"])]
    bw, gap = 242, 18
    for i, (title, c, items) in enumerate(cols):
        x = 20 + i * (bw + gap)
        s.box(x, 64, bw, 44, title, None, color=c, size=14, tint=0.18)
        for j, t in enumerate(items):
            s.box(x + 6, 122 + j * 66, bw - 12, 56, t, None,
                  color=c, size=11.5, weight=400, tint=0.08)
    y = 404
    bands = [("完全开放", "可自由下载与再分发，是绝大多数公开模型的训练来源", OI["green"]),
             ("开放但有限制", "可访问但限制商业用途或再分发，常见于学术数据库", OI["orange"]),
             ("商业与专有", "付费或企业内部，规模与质量通常更高，但无法被外部验证", OI["verm"])]
    for i, (a, b, c) in enumerate(bands):
        s.rect(20, y + i * 46, 1020, 38, c, tint=0.10, rx=5)
        s.text(36, y + i * 46 + 24, a + "：", 12.5, "start", 700, c)
        s.text(152, y + i * 46 + 24, b, 12, "start", 400, "#444")
    s.text(20, 574, "公开数据决定了学术界的研究上限；专有数据决定了企业之间的差距。", 12, "start", 600, "#444")
    return s.save(os.path.join(SV, "data_landscape.svg"))


def fig_scale_gap():
    plt = mpl_setup()
    import numpy as np
    items = ["可购买分子\n(Enamine REAL)", "蛋白序列\n(UniProt)", "化合物记录\n(PubChem)",
             "活性数据点\n(ChEMBL)", "实验结构\n(PDB)", "复合物+亲和力\n(PDBbind)",
             "获批小分子药"]
    vals = [4.8e10, 2.5e8, 1.2e8, 2.4e7, 2.3e5, 2.3e4, 1.5e3]
    cols = [OI["blue"], OI["purple"], OI["blue"], OI["sky"], OI["green"], OI["green"], OI["crimson"]]
    x = np.arange(len(items))
    fig, ax = plt.subplots(figsize=(8.6, 3.9))
    ax.bar(x, vals, 0.58, color=cols)
    ax.set_yscale("log")
    ax.set_ylim(1e2, 2e11)
    ax.set_xticks(x); ax.set_xticklabels(items, fontsize=9.5)
    ax.set_ylabel("记录数（对数轴）")
    def lab(v):
        e = int(np.floor(np.log10(v)))
        m = v / 10 ** e
        return f"{m:.0f}×10^{e}"
    for xi, v in zip(x, vals):
        ax.text(xi, v * 1.9, lab(v), ha="center", fontsize=9.5, color="#555")
    ax.set_title("能枚举的很多，被测量过的很少，有临床结论的极少（跨越七个数量级）", loc="left")
    ax.text(0.0, -0.40, "数量为 2026 年前后的量级估计，各库统计口径不同，仅用于比较数量级。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.34)
    return save_chart(fig, os.path.join(SV, "data_scale_gap.svg"))


def fig_provenance():
    W, H = 1020, 430
    s = SVG(W, H)
    s.text(W / 2, 28, "一个活性数据点的来龙去脉：每一步都可能引入误差", 15.5, "middle", 700)
    steps = [("实验测定", "不同实验室的\n缓冲液、温度、\n酶浓度各不相同", OI["gray"]),
             ("论文发表", "阳性结果发表率\n远高于阴性结果", OI["orange"]),
             ("人工提取", "从表格与正文中\n抽取数值与单位", OI["blue"]),
             ("数据库收录", "标准化为统一字段，\n但原始条件已丢失", OI["sky"]),
             ("建模使用", "常被当作同质数据\n直接混合训练", OI["crimson"])]
    bw, gap = 180, 24
    for i, (a, b, c) in enumerate(steps):
        x = 24 + i * (bw + gap)
        s.box(x, 70, bw, 110, a, b.replace("\n", ""), color=c, size=13.5, subsize=10.5, tint=0.14)
        if i < 4:
            s.line(x + bw, 125, x + bw + gap, 125, OI["black"], 1.5)
    s.rect(24, 212, 972, 52, OI["crimson"], tint=0.10, rx=6)
    s.text(510, 234, "同一个分子对同一个靶点的 IC50，不同文献之间相差 10 倍并不罕见",
           13, "middle", 700, OI["crimson"])
    s.text(510, 254, "这不是数据录入错误，而是实验条件差异的真实反映", 11.5, "middle", 400, "#555")
    notes = [("对建模的含义", "训练标签本身带有约 0.5 个对数单位的固有噪声，模型精度不可能超过这个下限"),
             ("对评测的含义", "测试集误差低于标签噪声，通常意味着数据泄漏而非模型优秀"),
             ("对实践的含义", "跨来源混合数据时，应保留来源字段并检查同一分子的多次测定是否一致")]
    for i, (a, b) in enumerate(notes):
        y = 286 + i * 46
        s.text(24, y + 20, a + "：", 12.5, "start", 700, OI["purple"])
        s.text(150, y + 20, b, 12, "start", 400, "#444")
    return s.save(os.path.join(SV, "data_provenance.svg"))


if __name__ == "__main__":
    print(fig_landscape(), fig_provenance())
    print(fig_scale_gap())
