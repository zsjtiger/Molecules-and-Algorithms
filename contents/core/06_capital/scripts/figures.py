import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")

def fig_deal():
    plt = mpl_setup()
    import numpy as np
    # illustrative split of $2.75B headline (breakdown not disclosed)
    parts = [("首付款", 115, 1.00), ("研发里程碑", 300, 0.35), ("监管里程碑", 500, 0.08), ("商业化里程碑", 1835, 0.05)]
    head = sum(p[1] for p in parts)
    ra = [p[1] * p[2] for p in parts]
    cols = [OI["crimson"], OI["orange"], OI["sky"], OI["lgray"]]
    fig, ax = plt.subplots(figsize=(7.8, 3.0))
    left = 0
    for (n, v, pr), c in zip(parts, cols):
        ax.barh(1, v, left=left, color=c, height=0.5, label=f"{n}（{v}，假设成功概率 {int(pr*100)}%）")
        left += v
    left = 0
    for (n, v, pr), c, r in zip(parts, cols, ra):
        ax.barh(0, r, left=left, color=c, height=0.5)
        left += r
    ax.text(head + 30, 1, f"标题金额 {head:,}", va="center", fontsize=10.5)
    ax.text(sum(ra) + 30, 0, f"风险调整后约 {sum(ra):,.0f}（约 {sum(ra)/head*100:.0f}%）", va="center", fontsize=10.5, color=OI["crimson"])
    ax.set_yticks([1, 0]); ax.set_yticklabels(["新闻标题口径", "按阶段概率折算"])
    ax.set_xlim(0, 3700); ax.set_xlabel("百万美元（未折现）")
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.32), ncol=2, fontsize=9.5)
    ax.set_title("“最高 27.5 亿美元”的合作，按成功概率折算后只剩一小部分", loc="left")
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "deal_haircut.svg"))

def fig_partnerships():
    plt = mpl_setup()
    cats = ["靶点与生物学\n（含虚拟细胞、基因组）", "分子发现与设计", "临床开发", "生物标志物与精准医疗", "影像与诊断", "算力与数据协作基础设施"]
    n = [8, 7, 5, 2, 2, 2]
    fig, ax = plt.subplots(figsize=(7.0, 3.4))
    y = list(range(len(n)))[::-1]
    cols = [OI["crimson"]] + [OI["blue"]] * 5
    ax.barh(y, n, color=cols, height=0.6)
    for yi, v in zip(y, n): ax.text(v + 0.15, yi, str(v), va="center", fontsize=10.5)
    ax.set_yticks(y); ax.set_yticklabels(cats)
    ax.set_xlim(0, 9.5); ax.set_xlabel("合作数量（共 26 项）")
    ax.set_title("2026 年一季度药企–AI 合作：靶点与生物学类最多", loc="left")
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "q1_partnerships.svg"))

def fig_flows():
    W, H = 1060, 470
    s = SVG(W, H)
    s.text(W / 2, 28, "AI 制药的资本来源、载体与退出", 15.5, "middle", 700)
    src = [("风险投资与成长基金", "Thrive、红杉、高瓴、GV"), ("产业资本 / 战略投资", "礼来、赛诺菲、医药集团"),
           ("科技公司", "Alphabet、字节、腾讯、英伟达"), ("主权与政府基金", "淡马锡、MGX、地方产业基金")]
    mid = [("AI 原生药物研发公司", OI["crimson"]), ("AI for Science 平台", OI["blue"]), ("大厂孵化 / 分拆实体", OI["purple"])]
    out = [("合作首付款与里程碑", "现金流 + 价值确认"), ("公开市场上市", "纳斯达克；港股 18A / 18C"),
           ("并购", "如 Recursion–Exscientia；大药企收购"), ("资产出售 / 授权", "单个分子或项目打包")]
    for i, (a, b) in enumerate(src):
        s.box(30, 64 + i * 92, 250, 70, a, b, color=OI["gray"], size=13, subsize=11)
    for i, (a, c) in enumerate(mid):
        s.box(405, 110 + i * 100, 250, 64, a, None, color=c, size=13.5, tint=0.14)
    for i, (a, b) in enumerate(out):
        s.box(780, 64 + i * 92, 250, 70, a, b, color=OI["green"], size=13, subsize=11)
    # grouped connectors: bracket on each side + one thick arrow
    s.line(292, 99, 292, 375, OI["gray"], 2, head=None)
    for i in range(4):
        s.line(280, 64 + i * 92 + 35, 292, 64 + i * 92 + 35, OI["gray"], 2, head=None)
    s.line(292, 237, 380, 237, OI["gray"], 3, head=None)
    s.line(380, 142, 380, 342, OI["gray"], 2, head=None)
    for j in range(3):
        s.line(380, 110 + j * 100 + 32, 405, 110 + j * 100 + 32, OI["gray"], 2)
    s.line(668, 142, 668, 342, OI["green"], 2, head=None)
    for j in range(3):
        s.line(655, 110 + j * 100 + 32, 668, 110 + j * 100 + 32, OI["green"], 2, head=None)
    s.line(668, 237, 768, 237, OI["green"], 3, head=None)
    s.line(768, 99, 768, 375, OI["green"], 2, head=None)
    for i in range(4):
        s.line(768, 64 + i * 92 + 35, 780, 64 + i * 92 + 35, OI["green"], 2)
    s.text(342, 448, "资金流入", 12, "middle", 600, "#555")
    s.text(717, 448, "价值实现", 12, "middle", 600, OI["green"])
    return s.save(os.path.join(SV, "capital_flows.svg"))

def fig_bd():
    plt = mpl_setup()
    fig, ax = plt.subplots(figsize=(6.6, 2.4))
    ax.barh([1], [997], color=OI["lgray"], height=0.5)
    ax.barh([0], [50], color=OI["crimson"], height=0.5)
    ax.text(997 + 10, 1, "交易总额约 997 亿美元", va="center", fontsize=10.5)
    ax.text(50 + 10, 0, "首付款约 50 亿美元（约 5%）", va="center", fontsize=10.5, color=OI["crimson"])
    ax.set_yticks([1, 0]); ax.set_yticklabels(["总额", "首付款"])
    ax.set_xlim(0, 1450); ax.set_xlabel("亿美元")
    ax.set_title("2026 年上半年中国创新药对外 BD：首付款只占二十分之一", loc="left")
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "china_bd.svg"))

if __name__ == "__main__":
    print(fig_deal(), fig_partnerships(), fig_flows(), fig_bd())
