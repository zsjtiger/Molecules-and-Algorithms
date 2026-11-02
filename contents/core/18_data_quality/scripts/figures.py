import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_bias_taxonomy():
    W, H = 640, 524
    s = SVG(W, H)
    s.text(W / 2, 28, "药物研发数据中的六类系统性偏差", 15.5, "middle", 700)
    rows = [("研究热点偏差", "少数靶点占据绝大部分文献与数据",
             "模型在冷门靶点上几乎没有可学的信号", OI["crimson"]),
            ("发表偏差", "阳性结果发表率远高于阴性结果",
             "模型学到的是“什么有效”，而非“什么无效”", OI["orange"]),
            ("设计偏差", "医药化学以系列形式探索，骨架高度聚集",
             "随机划分会高估模型对新骨架的泛化能力", OI["blue"]),
            ("活性阈值偏差", "弱活性与无活性常被记为“大于某值”",
             "回归模型把截断值当作真实测量值", OI["sky"]),
            ("人群偏差", "临床与组学数据以欧洲血统人群为主",
             "遗传学证据在其他人群中的可迁移性未知", OI["purple"]),
            ("时间偏差", "方法与标准随年代变化，老数据口径不同",
             "跨年代混合训练会引入不可见的分布漂移", OI["green"])]
    for i, (a, b, c, col) in enumerate(rows):
        y = 60 + i * 74
        s.box(24, y, 194, 62, a, None, color=col, size=13.5, tint=0.17)
        s.text(238, y + 26, b, 12.5, "start", 400)
        s.text(238, y + 48, "后果：" + c, 12, "start", 600, col)
    s.text(24, 512, "六类偏差的共同点：它们都不是随机噪声，因此无法靠增大数据量抵消。",
           12.5, "start", 700, "#444")
    return s.save(os.path.join(SV, "bias_taxonomy.svg"))


def fig_longtail():
    plt = mpl_setup()
    import numpy as np
    rng = np.random.default_rng(3)
    n = 4000
    rank = np.arange(1, n + 1)
    counts = 9.0e4 * rank ** (-1.15)
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 3.6))
    ax = axes[0]
    ax.loglog(rank, counts, color=OI["blue"], lw=2)
    ax.set_xlabel("靶点按数据量排名"); ax.set_ylabel("活性数据点数")
    ax.set_title("数据量按靶点排名呈幂律分布", loc="left", fontsize=12)
    ax.axvline(100, color=OI["crimson"], lw=1.2, ls="--")
    ax.text(120, 2e4, "前 100 个靶点", fontsize=10, color=OI["crimson"])
    ax = axes[1]
    cum = np.cumsum(counts) / counts.sum() * 100
    frac = rank / n * 100
    ax.plot(frac, cum, color=OI["crimson"], lw=2.2)
    ax.plot([0, 100], [0, 100], color="#bbb", lw=1.0, ls="--")
    i5 = np.searchsorted(frac, 5.0)
    ax.plot([5, 5], [0, cum[i5]], color=OI["gray"], lw=1.0)
    ax.plot([0, 5], [cum[i5], cum[i5]], color=OI["gray"], lw=1.0)
    ax.text(13, cum[i5] - 10, f"前 5% 的靶点\n占全部数据的 {cum[i5]:.0f}%",
            fontsize=10.5, color=OI["crimson"])
    ax.set_xlabel("靶点比例（%）"); ax.set_ylabel("累计数据占比（%）")
    ax.set_title("少数靶点占据绝大部分数据", loc="left", fontsize=12)
    ax.set_xlim(0, 100); ax.set_ylim(0, 102)
    for a in axes:
        for s_ in ("top", "right"):
            a.spines[s_].set_visible(False)
    fig.suptitle("研究热点偏差：活性数据在靶点之间极度不均（示意分布）",
                 x=0.01, y=1.04, ha="left", fontsize=12.5)
    fig.subplots_adjust(top=0.78, wspace=0.32, bottom=0.18)
    return save_chart(fig, os.path.join(SV, "target_longtail.svg"))


def fig_split():
    plt = mpl_setup()
    import numpy as np
    methods = ["随机划分", "骨架划分", "时间划分"]
    r2 = [0.82, 0.54, 0.46]
    x = np.arange(3)
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    ax.bar(x, r2, 0.5, color=[OI["sky"], OI["orange"], OI["verm"]])
    for xi, v in zip(x, r2):
        ax.text(xi, v + 0.025, f"{v:.2f}", ha="center", fontsize=11.5, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(methods)
    ax.set_ylabel("测试集 R²"); ax.set_ylim(0, 1.0)
    ax.set_title("同一模型、同一数据，划分方式决定报告出的性能", loc="left")
    ax.text(0.0, -0.26, "数值为文献中常见的量级，用于说明趋势，非特定模型的测量结果。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.26)
    return save_chart(fig, os.path.join(SV, "split_effect.svg"))


def fig_mitigation():
    W, H = 1020, 400
    s = SVG(W, H)
    s.text(W / 2, 28, "偏差缓解：能做什么，不能做什么", 15.5, "middle", 700)
    s.box(30, 66, 460, 44, "可以缓解", None, color=OI["green"], size=14, tint=0.18)
    s.box(530, 66, 460, 44, "无法消除", None, color=OI["verm"], size=14, tint=0.18)
    can = ["按骨架或时间划分评测，诚实报告泛化能力",
           "保留并使用原始实验条件字段",
           "对同一分子的多次测定做一致性检查",
           "用删失回归正确处理“大于某值”的记录",
           "在报告中明确标注训练数据覆盖的化学与生物空间"]
    cannot = ["凭算法补出从未被测量过的数据",
              "让模型在训练分布之外可靠外推",
              "通过加权让冷门靶点获得真实信号",
              "用公开数据验证只有专有数据能回答的问题",
              "靠增大数据量抵消系统性偏差"]
    for i, t in enumerate(can):
        s.box(30, 124 + i * 52, 460, 42, t, None, color=OI["green"], size=11.5, weight=400, tint=0.08)
    for i, t in enumerate(cannot):
        s.box(530, 124 + i * 52, 460, 42, t, None, color=OI["verm"], size=11.5, weight=400, tint=0.08)
    s.text(510, 392, "务实的目标不是消除偏差，而是知道偏差在哪里、朝哪个方向、有多大。",
           12.5, "middle", 700, "#444")
    return s.save(os.path.join(SV, "bias_mitigation.svg"))


if __name__ == "__main__":
    print(fig_bias_taxonomy(), fig_mitigation())
    print(fig_longtail())
    print(fig_split())
