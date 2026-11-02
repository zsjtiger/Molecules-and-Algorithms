import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_models():
    W, H = 1060, 520
    s = SVG(W, H)
    s.text(W / 2, 28, "四种商业模式及其各自面临的质疑", 15.5, "middle", 700)
    rows = [("软件与平台授权", "把模型或平台卖给药企，按席位或项目收费",
             "单价低、替代品多，难以支撑高估值；客户倾向自建", OI["blue"]),
            ("服务与合作研发", "为药企承担特定研发环节，收取服务费与里程碑",
             "收入可见但不具复利；本质上是高端 CRO", OI["green"]),
            ("自研管线", "用自有平台推进自己的候选药物，靠授权或上市变现",
             "烧钱周期长，且最终要接受与传统药企同样的临床检验", OI["orange"]),
            ("混合模式", "服务收入养活自研管线，逐步提高自研比例",
             "两头都要做好，资源与注意力的分配是持续难题", OI["purple"])]
    for i, (a, b, c, col) in enumerate(rows):
        y = 62 + i * 104
        s.box(24, y, 220, 88, a, None, color=col, size=14, tint=0.17)
        s.text(268, y + 34, b, 12.5, "start", 400)
        s.text(268, y + 62, "主要质疑：" + c, 12, "start", 600, col)
    s.rect(24, 480, 1012, 34, OI["crimson"], tint=0.10, rx=5)
    s.text(530, 502, "共同的根本问题：平台的价值最终只能由管线成败来证明，而那需要十年",
           12.5, "middle", 700, OI["crimson"])
    return s.save(os.path.join(SV, "business_models.svg"))


def fig_talent():
    W, H = 1000, 440
    s = SVG(W, H)
    s.text(W / 2, 28, "人才结构的错配：三种人，两条断层", 15.5, "middle", 700)
    cols = [("计算背景", ["机器学习方法", "大规模工程", "评测与统计"], OI["blue"]),
            ("跨界（稀缺）", ["能把化学问题形式化", "能判断模型输出是否合理",
                           "能设计可验证的实验"], OI["crimson"]),
            ("实验背景", ["医药化学与合成", "细胞与动物药理", "项目与转化经验"], OI["green"])]
    for i, (title, items, c) in enumerate(cols):
        x = 30 + i * 320
        s.box(x, 70, 300, 46, title, None, color=c, size=14, tint=0.18)
        for j, t in enumerate(items):
            s.box(x + 10, 130 + j * 58, 280, 48, t, None, color=c, size=12,
                  weight=400, tint=0.08)
    rows = [("断层一：计算人不懂问题", "模型解决的是被错误形式化的问题，指标漂亮但不回答实际疑问"),
            ("断层二：实验人不懂边界", "把模型输出当作确定结论，或因一次失败全盘否定")]
    for i, (a, b) in enumerate(rows):
        y = 330 + i * 48
        s.box(30, y, 248, 38, a, None, color=OI["verm"], size=12, tint=0.14)
        s.text(298, y + 25, b, 12, "start", 400, "#444")
    return s.save(os.path.join(SV, "talent_gap.svg"))


def fig_repricing():
    plt = mpl_setup()
    import numpy as np
    phase = ["2015\n早期探索", "2018\n首批融资潮", "2021\n估值高点",
             "2023\n预期回调", "2026\n按证据定价"]
    hype = [1.5, 3.2, 4.8, 2.6, 2.4]
    evidence = [0.4, 0.9, 1.6, 2.3, 3.0]
    x = np.arange(len(phase))
    fig, ax = plt.subplots(figsize=(7.6, 3.8))
    ax.plot(x, hype, "-o", color=OI["orange"], lw=2.4, ms=8, label="市场预期")
    ax.plot(x, evidence, "-o", color=OI["green"], lw=2.4, ms=8, label="可验证的证据")
    ax.fill_between(x, hype, evidence, where=np.array(hype) > np.array(evidence),
                    color=OI["orange"], alpha=0.10)
    ax.set_xticks(x); ax.set_xticklabels(phase, fontsize=10)
    ax.set_yticks([1, 2, 3, 4, 5]); ax.set_yticklabels(["很低", "较低", "中", "较高", "很高"])
    ax.set_ylim(0, 5.4)
    ax.legend(frameon=False, loc="lower right", ncol=2, bbox_to_anchor=(1.0, 1.01), fontsize=10.5)
    ax.set_title("预期与证据的缺口正在收窄——两端同时向中间移动", loc="left", pad=22)
    ax.text(0.0, -0.32, "示意曲线，用于说明趋势形状，非量化指数。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.28)
    return save_chart(fig, os.path.join(SV, "repricing.svg"))


if __name__ == "__main__":
    print(fig_models(), fig_talent())
    print(fig_repricing())
