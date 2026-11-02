import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_entry_points():
    plt = mpl_setup()
    import numpy as np
    items = [("文献与证据提取", 4.5, 1.2), ("ADMET 性质预测面板", 4.0, 1.8),
             ("化合物库设计与采购", 3.6, 2.05), ("虚拟筛选流程", 3.4, 3.35),
             ("逆合成路线建议", 2.8, 2.75), ("生成式分子设计", 2.4, 3.6),
             ("靶点发现与验证", 1.8, 4.3), ("临床结局预测", 1.5, 4.8)]
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    for name, ease, risk in items:
        c = OI["green"] if ease > 3.2 else (OI["orange"] if ease > 2.2 else OI["verm"])
        ax.plot(ease, risk, "o", color=c, ms=10)
        ha = "right" if ease > 3.2 else "left"
        dx = -0.11 if ha == "right" else 0.11
        ax.text(ease + dx, risk, name, fontsize=10.5, ha=ha, va="center")
    ax.axvspan(3.2, 5.0, color=OI["green"], alpha=0.06)
    ax.set_xlim(0.9, 5.0); ax.set_ylim(1.0, 5.2)
    ax.set_xticks([1.5, 2.5, 3.5, 4.5]); ax.set_xticklabels(["很难", "较难", "较易", "很易"])
    ax.set_yticks([1.5, 2.5, 3.5, 4.5]); ax.set_yticklabels(["很低", "较低", "较高", "很高"])
    ax.set_xlabel("落地难度（越右越容易见效）"); ax.set_ylabel("失败后的代价与争议")
    ax.text(3.3, 5.05, "建议的切入区", fontsize=11, color=OI["green"], va="top", fontweight="bold")
    ax.set_title("从哪里切入：先选容易见效、失败代价低的场景", loc="left")
    ax.text(0.0, -0.26, "评级为作者基于行业实践的定性判断，具体企业的排序会因现有能力而异。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.24, left=0.14)
    return save_chart(fig, os.path.join(SV, "entry_points.svg"))


def fig_team():
    W, H = 1040, 440
    s = SVG(W, H)
    s.text(W / 2, 28, "跨职能团队：四种角色，三个接口", 15.5, "middle", 700)
    roles = [("药物化学家 / 生物学家", "定义问题、判断结果是否合理、\n决定下一轮做什么", OI["crimson"]),
             ("计算与建模", "选择方法、训练与评估模型、\n给出带不确定性的预测", OI["blue"]),
             ("数据与平台工程", "数据管道、服务可靠性、\n可复现性与审计", OI["green"]),
             ("项目与转化负责人", "设定成功标准、协调优先级、\n对接管线决策", OI["purple"])]
    for i, (a, b, c) in enumerate(roles):
        x = 20 + i * 254
        s.box(x, 70, 238, 108, a, b.replace("\n", ""), color=c, size=12.5, subsize=10.5, tint=0.14)
    ifaces = [("化学 ↔ 建模", "问题是否被正确地形式化？预测的单位与口径是否一致？"),
              ("建模 ↔ 平台", "模型如何版本化、如何上线、失效时谁负责？"),
              ("团队 ↔ 管线", "这个预测会改变哪个具体决策？不采纳的理由是什么？")]
    for i, (a, b) in enumerate(ifaces):
        y = 218 + i * 62
        s.box(20, y, 212, 50, a, None, color=OI["orange"], size=12.5, tint=0.15)
        s.text(254, y + 30, b, 12, "start", 400, "#444")
    s.text(20, 420, "多数落地失败发生在接口处，而不是任何一个角色内部。", 12.5, "start", 700, "#444")
    return s.save(os.path.join(SV, "team_interfaces.svg"))


def fig_metrics():
    W, H = 1020, 460
    s = SVG(W, H)
    s.text(W / 2, 28, "度量投资回报：三类指标，可信度递减", 15.5, "middle", 700)
    tiers = [("过程指标", "预测通量、周期时长、数据入库延迟、模型再训练频率",
              "可直接观测，但与价值的关系最弱", OI["blue"], "可信度高 / 价值关联弱"),
             ("决策指标", "进入下一阶段的候选数、被终止项目的平均用时、\n化学家采纳预测的比例",
              "最有意义的一层，需要事先约定记录方式", OI["green"], "可信度中 / 价值关联强"),
             ("结果指标", "先导优化轮次、候选化合物提名时间、临床成功率",
              "周期长、混杂因素多，单个项目无法归因", OI["orange"], "可信度低 / 价值关联最强")]
    for i, (a, b, c, col, badge) in enumerate(tiers):
        y = 66 + i * 116
        s.box(20, y, 212, 98, a, None, color=col, size=14, tint=0.17)
        lines = b.split("\n")
        for j, ln in enumerate(lines):
            s.text(254, y + 32 + j * 22, ln, 12, "start", 400)
        s.text(254, y + 78, c, 11.5, "start", 400, "#555")
        s.box(790, y + 24, 210, 50, badge, None, color=col, size=11.5, weight=600, tint=0.20)
    s.rect(20, 420, 980, 32, OI["crimson"], tint=0.10, rx=5)
    s.text(510, 441, "“AI 节省了 N 个月”这类说法几乎总是结果指标的单项目归因——不可验证",
           12, "middle", 700, OI["crimson"])
    return s.save(os.path.join(SV, "roi_metrics.svg"))


if __name__ == "__main__":
    print(fig_team(), fig_metrics())
    print(fig_entry_points())
