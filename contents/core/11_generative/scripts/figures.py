import sys, os, io
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_paradigms():
    W, H = 1060, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "分子生成的五种范式", 15.5, "middle", 700)
    rows = [
        ("自回归语言模型", "逐符号生成 SMILES / SELFIES", "有效率高、多样性好；难控制几何",
         "MolGPT、ChemGPT", OI["blue"]),
        ("变分自编码器", "编码到连续隐空间再解码", "可在隐空间做优化；解码有效率有限",
         "ChemVAE、JT-VAE", OI["sky"]),
        ("强化学习", "以评分函数为奖励引导生成器", "可优化任意可计算目标；最易奖励作弊",
         "REINVENT、GENTRL", OI["crimson"]),
        ("扩散 / 流匹配", "从噪声逐步去噪，可在三维坐标上进行", "适合口袋条件生成；物理合理性待改进",
         "TargetDiff、DiffSBDD", OI["purple"]),
        ("基于反应的生成", "生成合成路线而非结构", "产物天然可合成；化学空间受反应库限制",
         "SynNet、按需合成库枚举", OI["green"]),
    ]
    s.text(262, 52, "做法与权衡", 12, "start", 700, "#777")
    s.text(760, 52, "代表方法", 12, "start", 700, "#777")
    for i, (a, b, c, rep, col) in enumerate(rows):
        y = 60 + i * 68
        s.box(24, y, 220, 54, a, None, color=col, size=13.5, tint=0.16)
        s.text(262, y + 23, b, 12.5, "start", 600)
        s.text(262, y + 43, c, 11.5, "start", 400, "#555")
        s.text(760, y + 33, rep, 11.5, "start", 400, col)
    s.text(24, 412, "实际平台往往是多种范式的组合，并由一组评分组件共同约束。", 11.5, "start", 400, "#444")
    return s.save(os.path.join(SV, "generation_paradigms.svg"))


def fig_rl_loop():
    W, H = 1030, 430
    s = SVG(W, H)
    s.text(W / 2, 28, "生成 + 强化学习 + 多参数评分的工业界范式", 15.5, "middle", 700)
    s.box(60, 150, 190, 90, "生成器", "先验模型 + 策略", color=OI["blue"], size=14, subsize=11.5)
    s.box(350, 150, 170, 90, "候选分子", "每轮数百到数千个", color=OI["gray"], size=14, subsize=11.5)
    s.line(250, 195, 350, 195, OI["black"], 1.5)
    comps = [("活性模型", OI["crimson"]), ("ADMET 模型", OI["orange"]), ("可合成性评分", OI["green"]),
             ("相似性 / 新颖性约束", OI["purple"]), ("多样性惩罚", OI["sky"])]
    for i, (t, c) in enumerate(comps):
        s.box(620, 62 + i * 64, 230, 50, t, None, color=c, size=12.5, weight=400, tint=0.14)
        s.line(520, 195, 620, 62 + i * 64 + 25, OI["lgray"], 1.2)
    s.box(620, 390, 230, 34, "综合奖励 R", None, color=OI["black"], size=13, tint=0.08)
    # 五个评分项是并列的，汇总线走右侧总线，不从方框中间穿过
    bus = 884
    for i in range(5):
        yy = 62 + i * 64 + 25
        s.line(850, yy, bus, yy, OI["lgray"], 1.2, head=None)
    s.line(bus, 62 + 25, bus, 407, OI["lgray"], 1.2, head=None)
    s.line(bus, 407, 850, 407, OI["black"], 1.5)
    s.path("M 620 407 C 400 407, 160 380, 155 240", OI["crimson"], 1.8)
    s.text(410, 374, "策略梯度更新（含 KL 正则）", 12, "middle", 600, OI["crimson"])
    s.text(60, 96, "关键：奖励的每一项都是真实目标的代理，", 11.5, "start", 400, "#444")
    s.text(60, 116, "优化压力越大，越可能钻代理的漏洞。", 11.5, "start", 400, "#444")
    return s.save(os.path.join(SV, "rl_scoring_loop.svg"))


def fig_overopt():
    plt = mpl_setup()
    import numpy as np
    kl = np.linspace(0, 10, 300)
    proxy = 1 - np.exp(-0.55 * kl)
    true = 1.25 * (1 - np.exp(-0.6 * kl)) - 0.085 * kl ** 1.45
    fig, ax = plt.subplots(figsize=(7.0, 3.5))
    ax.plot(kl, proxy, color=OI["sky"], lw=2.2, label="代理奖励（评分函数给出的分数）")
    ax.plot(kl, true, color=OI["crimson"], lw=2.2, label="真实目标（实验验证的质量）")
    k = kl[int(np.argmax(true))]
    ax.axvline(k, color="#888", ls="--", lw=1)
    ax.annotate("拐点：继续优化开始损害真实目标", (k, max(true)), xytext=(k + 0.4, 0.42),
                fontsize=10.5, color=OI["crimson"], arrowprops=dict(arrowstyle="->", color=OI["crimson"]))
    ax.set_xlabel("相对初始分布的 KL 散度（优化强度）")
    ax.set_ylabel("性能（归一化）")
    ax.set_title("代理模型过度优化：分数一路上涨，真实质量先升后降", loc="left")
    ax.set_xticks([]); ax.set_yticks([])
    ax.legend(frameon=False, loc="lower left", fontsize=10)
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "proxy_overoptimization.svg"))


def fig_constrained():
    plt = mpl_setup()
    from rdkit import Chem
    from rdkit.Chem import rdDepictor, AllChem
    from rdkit.Chem.Draw import rdMolDraw2D
    from PIL import Image
    core = Chem.MolFromSmarts("c1ccc2[nH]cnc2c1")
    smis = [("起始先导", "Cc1ccc2[nH]cnc2c1"),
            ("R 基团替换", "COc1ccc2[nH]cnc2c1"),
            ("片段生长", "O=C(N)c1ccc2[nH]cnc2c1"),
            ("骨架跃迁", "Cc1ccc2[nH]ccc2n1")]
    fig, axes = plt.subplots(1, 4, figsize=(11, 2.9))
    for ax, (t, smi) in zip(axes, smis):
        m = Chem.MolFromSmiles(smi)
        rdDepictor.Compute2DCoords(m)
        match = m.GetSubstructMatch(core)
        d = rdMolDraw2D.MolDraw2DCairo(420, 300)
        o = d.drawOptions(); o.bondLineWidth = 2
        hc = {a: (0.0, 0.62, 0.45) for a in match}
        d.DrawMolecule(m, highlightAtoms=list(match), highlightAtomColors=hc)
        d.FinishDrawing()
        ax.imshow(Image.open(io.BytesIO(d.GetDrawingText()))); ax.axis("off")
        ax.set_title(t, fontsize=12)
    fig.suptitle("有约束的生成：保留关键骨架（绿色），只改动外围——这才是工业界最常用的方式",
                 x=0.01, ha="left", fontsize=12.5)
    return save_chart(fig, os.path.join(SV, "constrained_generation.svg"))


def fig_synthesis_aware():
    plt = mpl_setup()
    from rdkit import Chem
    from rdkit.Chem import rdDepictor
    from rdkit.Chem.Draw import rdMolDraw2D
    from PIL import Image
    items = [("砌块 A", "OB(O)c1ccc(C)cc1"), ("砌块 B", "Brc1ccccc1C#N"), ("产物（Suzuki 偶联）", "Cc1ccc(-c2ccccc2C#N)cc1")]
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 2.8))
    for ax, (t, smi) in zip(axes, items):
        m = Chem.MolFromSmiles(smi)
        rdDepictor.Compute2DCoords(m)
        d = rdMolDraw2D.MolDraw2DCairo(430, 300)
        d.drawOptions().bondLineWidth = 2
        d.DrawMolecule(m); d.FinishDrawing()
        ax.imshow(Image.open(io.BytesIO(d.GetDrawingText()))); ax.axis("off")
        ax.set_title(t, fontsize=12)
    fig.suptitle("合成感知生成：模型输出的是“砌块 + 可靠反应”，产物天然可合成",
                 x=0.01, ha="left", fontsize=12.5)
    return save_chart(fig, os.path.join(SV, "synthesis_aware.svg"))


if __name__ == "__main__":
    print(fig_paradigms(), fig_rl_loop())
    print(fig_overopt())
    print(fig_constrained())
    print(fig_synthesis_aware())
