import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_chain():
    W, H = 1060, 566
    s = SVG(W, H)
    s.text(W / 2, 28, "从分子到患者：四道推断鸿沟", 15.5, "middle", 700)
    steps = ["分子结合靶点", "细胞中产生效应", "动物模型中改善表型",
             "人体中改变生物标志物", "患者的临床结局改善"]
    gaps = [("体外到细胞", "化合物进不去细胞、被外排、\n在胞内浓度远低于体外"),
            ("细胞到动物", "药代动力学、代谢、\n组织分布与毒性", ),
            ("动物到人", "模型生物与人类的\n通路差异和疾病建模不足"),
            ("标志物到结局", "替代终点未必预测\n真实的临床获益")]
    bw = 190
    for i, t in enumerate(steps):
        y = 64 + i * 92
        s.box(24, y, bw, 64, t, None, color=OI["blue"], size=13, tint=0.14)
        if i < 4:
            s.line(118, y + 64, 118, y + 92, OI["black"], 1.5)
            a, b = gaps[i][0], gaps[i][1]
            # 引线把每道鸿沟与它所对应的那一段箭头明确连起来
            s.line(118, y + 78, 254, y + 72, OI["verm"], 1.0, dash="4,3", head=None)
            s.box(254, y + 42, 220, 60, a, None, color=OI["verm"], size=12.5, tint=0.16)
            lines = b.split("\n")
            for j, ln in enumerate(lines):
                s.text(498, y + 62 + j * 22, ln, 11.5, "start", 400, "#444")
    s.rect(24, 512, 1012, 40, OI["crimson"], tint=0.10, rx=6)
    s.text(530, 537, "AI 在第一道鸿沟上帮助最大，而决定成败的是后三道", 13, "middle", 700, OI["crimson"])
    return s.save(os.path.join(SV, "inference_chain.svg"))


def fig_translation():
    plt = mpl_setup()
    import numpy as np
    stages = ["体外结合", "细胞活性", "动物药效", "I 期安全", "II 期疗效", "III 期确证"]
    surv = [100, 62, 34, 20, 12, 7]
    x = np.arange(len(stages))
    fig, ax = plt.subplots(figsize=(7.8, 3.6))
    ax.plot(x, surv, "-o", color=OI["crimson"], lw=2.4, ms=8)
    for xi, v in zip(x, surv):
        ax.text(xi, v + 5, f"{v}", ha="center", fontsize=11, color=OI["crimson"], fontweight="bold")
    ax.fill_between(x, surv, color=OI["crimson"], alpha=0.08)
    ax.set_xticks(x); ax.set_xticklabels(stages, fontsize=10.5)
    ax.set_ylabel("相对存活比例"); ax.set_ylim(0, 115)
    ax.set_title("每一道鸿沟都筛掉一批：问题不在任何单一环节", loc="left")
    ax.text(0.0, -0.30, "示意比例，用于说明衰减形状，非特定数据集的统计值。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.26)
    return save_chart(fig, os.path.join(SV, "translation_attrition.svg"))


def fig_what_ai_cannot():
    W, H = 1020, 430
    s = SVG(W, H)
    s.text(W / 2, 28, "科学瓶颈：哪些是数据问题，哪些不是", 15.5, "middle", 700)
    s.box(24, 66, 470, 44, "更多数据可以缓解", None, color=OI["green"], size=14, tint=0.18)
    s.box(526, 66, 470, 44, "更多数据无法解决", None, color=OI["verm"], size=14, tint=0.18)
    left = ["分子性质与 ADMET 的预测精度",
            "已知靶点家族内的结合预测",
            "已有通路的组学特征识别",
            "文献与专利的证据汇总"]
    right = ["疾病机制本身尚未被理解",
             "模型生物与人类的生物学差异",
             "替代终点与临床结局的因果关系",
             "人体内复杂系统的涌现行为"]
    for i, t in enumerate(left):
        s.box(24, 124 + i * 62, 470, 52, t, None, color=OI["green"], size=12, weight=400, tint=0.08)
    for i, t in enumerate(right):
        s.box(526, 124 + i * 62, 470, 52, t, None, color=OI["verm"], size=12, weight=400, tint=0.08)
    s.text(510, 400, "右栏的问题不是算力或样本量不足，而是人类尚未掌握相应的因果知识。",
           12.5, "middle", 700, "#444")
    s.text(510, 422, "AI 可以加速对这些问题的研究，但不能跳过研究本身。", 12, "middle", 400, "#555")
    return s.save(os.path.join(SV, "data_vs_science.svg"))


if __name__ == "__main__":
    print(fig_chain(), fig_what_ai_cannot())
    print(fig_translation())
