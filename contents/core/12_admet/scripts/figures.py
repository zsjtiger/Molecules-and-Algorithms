import sys, os, io
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_admet_map():
    W, H = 1064, 494
    s = SVG(W, H)
    s.text(W / 2, 28, "ADMET：药物在体内的旅程与对应的预测终点", 15.5, "middle", 700)
    # ADME 是串联的时间顺序；T（毒性）不是最后一环，另画成横跨全程的并行约束带
    stages = [("A 吸收", "口服给药 → 进入血液", ["溶解度", "渗透性（Caco-2）", "口服生物利用度 F"], OI["green"]),
              ("D 分布", "随血液到达组织", ["血浆蛋白结合率", "血脑屏障穿透", "分布容积 Vd"], OI["blue"]),
              ("M 代谢", "主要由肝脏 CYP450 处理", ["CYP 底物 / 抑制", "代谢稳定性", "代谢位点"], OI["purple"]),
              ("E 排泄", "经肾或经肝清除", ["清除率 CL", "半衰期 t½"], OI["sky"])]
    bw, gap = 236, 20
    for i, (a, b, items, c) in enumerate(stages):
        x = 20 + i * (bw + gap)
        s.box(x, 62, bw, 62, a, b, color=c, size=14, subsize=11, tint=0.16)
        if i < 3:
            s.line(x + bw, 93, x + bw + gap, 93, OI["black"], 1.5)
        for j, t in enumerate(items):
            s.box(x + 8, 148 + j * 50, bw - 16, 40, t, None, color=c, size=12, weight=400, tint=0.07)
    # 毒性带：横跨四个阶段，左右各一个箭头表示"全程适用"
    ty = 312
    s.rect(20, ty, 1024, 76, OI["crimson"], tint=0.10, rx=8)
    s.text(36, ty + 26, "T 毒性", 14, "start", 700, OI["crimson"])
    s.text(104, ty + 26, "不是最后一步，而是贯穿吸收、分布、代谢、排泄全过程的并行约束",
           12.5, "start", 400, OI["crimson"])
    for j, t in enumerate(["hERG 抑制", "肝毒性 DILI", "遗传毒性"]):
        s.box(36 + j * 180, ty + 38, 168, 28, t, None, color=OI["crimson"], size=11.5,
              weight=400, tint=0.16)
    s.text(1028, ty + 58, "任一阶段都可能触发", 11.5, "end", 400, OI["crimson"])
    s.text(20, 420, "历史教训：1991 年约 40% 的临床失败源于药代问题；到 2000 年这一比例降至约 10%。", 12, "start", 400, "#444")
    s.text(20, 444, "早期 ADMET 筛选已经把大部分药代问题挡在临床之前——这也意味着这一环节的边际改进空间", 12, "start", 400, "#444")
    s.text(20, 468, "不如靶点选择（见第 1 章 AI 价值地图）。", 12, "start", 400, "#444")
    return s.save(os.path.join(SV, "admet_map.svg"))


def fig_attrition_shift():
    plt = mpl_setup()
    import numpy as np
    cats = ["药代动力学 /\n生物利用度", "缺乏疗效", "安全性 /\n毒性", "商业与其他"]
    y1991 = [40, 29, 21, 10]
    y2000 = [10, 46, 30, 14]
    x = np.arange(len(cats)); w = 0.36
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.bar(x - w / 2, y1991, w, color=OI["gray"], label="约 1991 年")
    ax.bar(x + w / 2, y2000, w, color=OI["crimson"], label="约 2000 年")
    for xi, a, b in zip(x, y1991, y2000):
        ax.text(xi - w / 2, a + 1, f"{a}%", ha="center", fontsize=10)
        ax.text(xi + w / 2, b + 1, f"{b}%", ha="center", fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(cats)
    ax.set_ylabel("占临床失败的比例")
    ax.set_ylim(0, 56)
    ax.set_title("早期 ADMET 筛选把药代失败压了下去，疗效随之成为主因", loc="left")
    ax.legend(frameon=False, loc="upper right", fontsize=10)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "attrition_shift.svg"))


def fig_conformal():
    plt = mpl_setup()
    import numpy as np
    rng = np.random.default_rng(3)
    x = np.concatenate([rng.normal(0.3, 0.16, 90), rng.normal(0.82, 0.07, 26)])
    x = np.clip(x, 0.02, 0.98)
    y = 2.6 + 3.1 * x + rng.normal(0, 0.22, x.size)
    width = 0.42 + 2.6 * np.clip(x - 0.55, 0, None) ** 1.5 * 3
    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    o = np.argsort(x)
    ax.fill_between(x[o], (y - width)[o], (y + width)[o], color=OI["sky"], alpha=0.25, label="conformal 预测区间（90% 覆盖）")
    ax.plot(x[o], y[o], color=OI["blue"], lw=1.6, label="模型点预测")
    ax.axvspan(0.62, 1.0, color=OI["verm"], alpha=0.07)
    ax.text(0.64, 2.75, "训练化学空间之外\n区间自动变宽", fontsize=10.5, color=OI["verm"])
    ax.set_xlabel("与训练集的化学距离（示意）")
    ax.set_ylabel("预测的 logS（溶解度）")
    ax.set_title("conformal prediction：对不熟悉的分子，诚实地说“我不确定”", loc="left")
    ax.set_xticks([]); ax.legend(frameon=False, loc="upper left", fontsize=10)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "conformal_prediction.svg"))


def fig_herg():
    plt = mpl_setup()
    from rdkit import Chem
    from rdkit.Chem import rdDepictor
    from rdkit.Chem.Draw import rdMolDraw2D
    from PIL import Image
    mols = [("特非那定（因 hERG 撤市）", "CC(C)(C)c1ccc(cc1)C(O)CCCN1CCC(CC1)C(O)(c1ccccc1)c1ccccc1"),
            ("非索非那定（活性代谢物）", "CC(C)(C(O)=O)c1ccc(cc1)C(O)CCCN1CCC(CC1)C(O)(c1ccccc1)c1ccccc1")]
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 3.2))
    for ax, (t, smi) in zip(axes, mols):
        m = Chem.MolFromSmiles(smi)
        rdDepictor.Compute2DCoords(m)
        d = rdMolDraw2D.MolDraw2DCairo(560, 330)
        d.drawOptions().bondLineWidth = 2
        d.DrawMolecule(m); d.FinishDrawing()
        ax.imshow(Image.open(io.BytesIO(d.GetDrawingText()))); ax.axis("off")
        ax.set_title(t, fontsize=12)
    fig.suptitle("一个叔丁基被氧化成羧酸，心脏安全性就完全不同——这正是 ADMET 预测的难度",
                 x=0.01, ha="left", fontsize=12.5)
    return save_chart(fig, os.path.join(SV, "herg_example.svg"))


def fig_mpo():
    plt = mpl_setup()
    import numpy as np
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 2.7))
    x1 = np.linspace(0, 8, 200)
    d1 = np.clip(np.where(x1 < 3, x1 / 3, np.where(x1 < 5, 1, 1 - (x1 - 5) / 3)), 0, 1)
    axes[0].plot(x1, d1, color=OI["blue"], lw=2.2); axes[0].set_xlabel("logP")
    axes[0].set_title("梯形：有最优区间", loc="left", fontsize=11.5)
    x2 = np.linspace(0, 150, 200)
    d2 = 1 / (1 + np.exp((x2 - 90) / 12))
    axes[1].plot(x2, d2, color=OI["green"], lw=2.2); axes[1].set_xlabel("拓扑极性表面积 TPSA")
    axes[1].set_title("S 形：越小越好，有软阈值", loc="left", fontsize=11.5)
    x3 = np.linspace(0, 10, 200)
    d3 = np.clip(x3 / 6, 0, 1)
    axes[2].plot(x3, d3, color=OI["orange"], lw=2.2); axes[2].set_xlabel("代谢稳定性（小时）")
    axes[2].set_title("线性饱和：越大越好", loc="left", fontsize=11.5)
    for ax in axes:
        ax.set_ylim(-0.05, 1.08); ax.set_yticks([0, 1]); ax.set_ylabel("期望度 d")
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(False)
    fig.suptitle("多参数优化：把每项性质映射到 0–1 的期望度，再加权合成单一评分",
                 x=0.01, y=1.08, ha="left", fontsize=12.5)
    fig.subplots_adjust(top=0.80, wspace=0.42)
    return save_chart(fig, os.path.join(SV, "mpo_desirability.svg"))


if __name__ == "__main__":
    print(fig_admet_map())
    print(fig_attrition_shift())
    print(fig_conformal())
    print(fig_herg())
    print(fig_mpo())
