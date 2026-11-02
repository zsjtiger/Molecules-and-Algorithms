import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_clinical_map():
    W, H = 1060, 470
    s = SVG(W, H)
    s.text(W / 2, 28, "AI 在临床开发中的应用图谱", 15.5, "middle", 700)
    cols = [("试验设计", ["终点与样本量", "入排标准优化", "方案可行性模拟"], OI["crimson"]),
            ("患者选择", ["生物标志物分层", "富集策略", "预后协变量调整"], OI["orange"]),
            ("招募与运营", ["中心选择", "患者匹配", "风险化监查"], OI["blue"]),
            ("数据与安全", ["数据清理", "不良事件信号", "影像终点读片"], OI["green"]),
            ("注册与文档", ["CSR 自动起草", "CTD 模块生成", "监管问询应答"], OI["purple"])]
    bw, gap = 188, 20
    for i, (title, items, c) in enumerate(cols):
        x = 20 + i * (bw + gap)
        s.box(x, 66, bw, 50, title, None, color=c, size=14, tint=0.18)
        for j, t in enumerate(items):
            s.box(x + 10, 132 + j * 56, bw - 20, 44, t, None, color=c, size=12, weight=400, tint=0.07)
    s.rect(20, 316, 1020, 46, OI["crimson"], tint=0.10, rx=6)
    s.text(530, 336, "影响 II/III 期成功率（价值极高，证据最少）", 12.5, "middle", 700, OI["crimson"])
    s.text(530, 355, "试验设计与患者选择", 11.5, "middle", 400, "#444")
    s.rect(20, 374, 1020, 46, OI["blue"], tint=0.10, rx=6)
    s.text(530, 394, "影响时间与成本（价值中高，已有效率数据）", 12.5, "middle", 700, OI["blue"])
    s.text(530, 413, "招募与运营、数据与安全、注册与文档", 11.5, "middle", 400, "#444")
    s.text(20, 452, "两类应用的证据成熟度差异巨大，混为一谈会高估 AI 对临床成功率的影响。", 12, "start", 400, "#444")
    return s.save(os.path.join(SV, "clinical_map.svg"))


def fig_digital_twin():
    W, H = 1040, 470
    s = SVG(W, H)
    s.text(W / 2, 28, "数字孪生的三种用法：区别至关重要", 15.5, "middle", 700)
    rows = [("预后协变量调整", "为每位真实受试者生成一个“若接受对照治疗会怎样”的预测，\n作为协变量纳入统计分析",
             "对照组仍是真实的，只是统计效率提高；EMA 已有资格认定先例", OI["green"], "监管接受度较高"),
            ("外部 / 合成对照臂", "用历史数据或真实世界数据构建对照组，替代部分或全部同期对照",
             "适用于罕见病、单臂试验；需论证可比性与偏倚控制", OI["orange"], "个案评估"),
            ("完全模拟对照组", "试验中没有任何真实对照受试者，对照结果全部由模型生成",
             "目前不是关键性试验的监管实践", OI["verm"], "不被接受")]
    for i, (a, b, c, col, badge) in enumerate(rows):
        y = 64 + i * 122
        s.box(20, y, 250, 104, a, None, color=col, size=14, tint=0.16)
        s.text(292, y + 32, b.split("\n")[0], 12, "start", 400)
        s.text(292, y + 54, b.split("\n")[1] if "\n" in b else "", 12, "start", 400)
        s.text(292, y + 82, c, 11.5, "start", 400, "#555")
        s.box(846, y + 28, 174, 48, badge, None, color=col, size=12.5, weight=600, tint=0.22)
    s.text(20, 456, "把三者混为一谈，是解读“数字孪生替代对照组”类新闻时最常见的错误。", 12, "start", 600, "#444")
    return s.save(os.path.join(SV, "digital_twin.svg"))


def fig_enrichment():
    plt = mpl_setup()
    import numpy as np
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.4), sharey=True)
    rng = np.random.default_rng(7)
    # unenriched: 30% responders
    for ax, frac, title in zip(axes, [0.30, 0.75], ["不富集：30% 应答者", "生物标志物富集：75% 应答者"]):
        n = 400
        resp = rng.random(n) < frac
        eff = np.where(resp, rng.normal(6.0, 1.6, n), rng.normal(0.3, 1.4, n))
        # 两幅图共用同一组分箱与坐标范围，否则读者无法直接比较两种入组策略
        ax.hist(eff, bins=np.linspace(-4, 11, 31), color=OI["sky"], edgecolor="white")
        ax.axvline(eff.mean(), color=OI["crimson"], lw=2.2)
        ax.set_xlim(-4, 11); ax.set_ylim(0, 60)
        ax.text(eff.mean() + 0.3, 53, f"平均效应 {eff.mean():.1f}",
                color=OI["crimson"], fontsize=11)
        ax.set_title(title, loc="left", fontsize=12)
        ax.set_xlabel("个体治疗效应")
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(False)
    axes[0].set_ylabel("患者数")
    fig.suptitle("富集策略：同一个药，入组谁决定了试验是成功还是失败",
                 x=0.01, y=1.04, ha="left", fontsize=12.5)
    fig.subplots_adjust(top=0.80)
    return save_chart(fig, os.path.join(SV, "enrichment.svg"))


def fig_evidence_gap():
    plt = mpl_setup()
    import numpy as np
    apps = ["文档与注册写作", "风险化监查", "中心选择与招募", "影像终点读片",
            "预后协变量调整", "外部对照臂", "生物标志物分层", "试验结局预测"]
    maturity = [3.6, 3.4, 3.2, 3.0, 2.6, 2.2, 2.0, 1.4]
    value = [2.0, 2.2, 2.6, 2.4, 3.2, 3.4, 4.4, 4.2]
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.axvspan(0.8, 2.5, ymin=0.52, ymax=1.0, color=OI["verm"], alpha=0.07)
    for a, m, v in zip(apps, maturity, value):
        c = OI["verm"] if (m < 2.5 and v > 3.0) else OI["blue"]
        ax.plot(m, v, "o", color=c, ms=9)
        ha = "right" if m > 3.0 else "left"
        dx = -0.09 if ha == "right" else 0.09
        ax.text(m + dx, v + 0.04, a, fontsize=10.5, ha=ha)
    ax.set_xlim(0.8, 4.2); ax.set_ylim(1.4, 5.0)
    ax.set_xticks([1.5, 2.5, 3.5]); ax.set_xticklabels(["低", "中", "高"])
    ax.set_yticks([2.0, 3.0, 4.0]); ax.set_yticklabels(["中", "高", "极高"])
    ax.set_xlabel("证据成熟度（2026）"); ax.set_ylabel("潜在价值")
    ax.axvline(2.5, color="#bbb", lw=0.8, ls="--"); ax.axhline(3.0, color="#bbb", lw=0.8, ls="--")
    ax.text(0.86, 4.82, "高价值 · 低证据", fontsize=10.5, color=OI["verm"], va="top")
    ax.set_title("临床 AI 内部的分化：效率类已有数据，决策类仍待验证", loc="left", fontsize=11.5)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "clinical_evidence_gap.svg"))


if __name__ == "__main__":
    print(fig_clinical_map(), fig_digital_twin())
    print(fig_enrichment())
    print(fig_evidence_gap())
