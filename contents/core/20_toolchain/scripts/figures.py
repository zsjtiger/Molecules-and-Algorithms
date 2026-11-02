import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_stack():
    W, H = 740, 540
    s = SVG(W, H)
    s.text(W / 2, 28, "AI 药物研发的开源技术栈", 15.5, "middle", 700)
    layers = [("应用层", "虚拟筛选流程、生成设计流程、ADMET 面板、科研智能体",
               "多为企业内部自建，开源项目少且碎片", OI["crimson"]),
              ("模型层", "AlphaFold / Boltz、RFdiffusion、ProteinMPNN、Chemprop、DiffDock",
               "开源程度最高，权重与代码多数可得", OI["orange"]),
              ("框架层", "PyTorch、PyTorch Geometric、DeepChem、JAX",
               "通用深度学习生态，成熟稳定", OI["green"]),
              ("领域库层", "RDKit、Open Babel、MDAnalysis、Biopython、OpenMM",
               "事实标准，几乎所有流程都依赖 RDKit", OI["blue"]),
              ("数据层", "ChEMBL / PubChem / PDB 的本地副本与 ETL 管道",
               "标识符对齐与版本管理是主要工作量", OI["purple"])]
    for i, (a, b, c, col) in enumerate(layers):
        y = 64 + i * 92
        s.box(24, y, 200, 76, a, None, color=col, size=14.5, tint=0.18)
        s.text(248, y + 30, b, 12.5, "start", 600)
        s.text(248, y + 56, c, 11.5, "start", 400, "#555")
    s.text(24, 532, "自下而上依赖关系明确；越往上开源覆盖越薄，企业自建比例越高。",
           12.5, "start", 700, "#444")
    return s.save(os.path.join(SV, "oss_stack.svg"))


def fig_fragmentation():
    W, H = 1044, 450
    s = SVG(W, H)
    s.text(W / 2, 28, "工具链碎片化：一个常规流程要跨越多少次格式转换", 15.5, "middle", 700)
    steps = [("ChEMBL 导出", "CSV + SMILES", OI["purple"]),
             ("RDKit 标准化", "Mol 对象", OI["blue"]),
             ("构象生成", "SDF（3D）", OI["blue"]),
             ("受体准备", "PDBQT / PDB", OI["green"]),
             ("对接", "程序专有格式", OI["green"]),
             ("MD / 重打分", "PRMTOP / GRO", OI["orange"]),
             ("汇总分析", "DataFrame", OI["crimson"])]
    bw, gap = 122, 26
    for i, (a, b, c) in enumerate(steps):
        x = 20 + i * (bw + gap)
        s.box(x, 76, bw, 84, a, b, color=c, size=11.5, subsize=10, tint=0.14)
        if i < 6:
            s.line(x + bw, 118, x + bw + gap, 118, OI["black"], 1.4)
            s.text(x + bw + gap / 2, 106, "转", 10, "middle", 700, OI["verm"])
    issues = [("单位不一致", "nM / μM / pIC50 混用，转换错误难以察觉"),
              ("坐标与质子化状态", "不同工具的默认质子化与互变异构处理不同"),
              ("标识符漂移", "同一分子在各步骤得到不同的内部 ID，结果难以回溯"),
              ("版本不可复现", "工具版本与参数未记录，几个月后无法重跑同一结果")]
    for i, (a, b) in enumerate(issues):
        y = 196 + i * 58
        s.box(20, y, 230, 46, a, None, color=OI["verm"], size=12, tint=0.13)
        s.text(272, y + 28, b, 12, "start", 400, "#444")
    s.text(20, 440, "每一次转换都是一个无声失败的机会：流程不会报错，只会给出错误的数字。",
           12.5, "start", 700, OI["crimson"])
    return s.save(os.path.join(SV, "fragmentation.svg"))


def fig_openness():
    plt = mpl_setup()
    import numpy as np
    names = ["RDKit", "Chemprop", "ProteinMPNN", "RFdiffusion", "ESMFold",
             "AlphaFold3", "Boltz-2", "商业对接软件", "企业内部平台"]
    code = [5, 5, 5, 5, 5, 3, 5, 1, 0]
    weights = [5, 5, 5, 5, 5, 2, 5, 1, 0]
    data = [5, 4, 3, 3, 3, 2, 3, 1, 0]
    y = np.arange(len(names))[::-1]; w = 0.26
    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    ax.barh(y + w, code, w, color=OI["blue"], label="代码可得")
    ax.barh(y, weights, w, color=OI["green"], label="权重可得")
    ax.barh(y - w, data, w, color=OI["orange"], label="训练数据可得")
    ax.set_yticks(y); ax.set_yticklabels(names, fontsize=10.5)
    ax.set_xticks([0, 1, 3, 5]); ax.set_xticklabels(["不可得", "受限", "部分", "完全"])
    ax.set_xlim(0, 5.6)
    ax.legend(frameon=False, loc="lower right", ncol=3, bbox_to_anchor=(1.0, 1.01), fontsize=10)
    ax.set_title("“开源”有三个层次，三者齐备的项目并不多", loc="left", pad=24)
    ax.text(0.0, -0.20, "评级依据各项目截至 2026 年的公开许可条款，商业条款可能随时间变化。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.18, left=0.20)
    return save_chart(fig, os.path.join(SV, "openness_levels.svg"))


if __name__ == "__main__":
    print(fig_stack(), fig_fragmentation())
    print(fig_openness())
