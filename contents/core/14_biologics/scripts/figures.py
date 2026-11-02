import sys, os, io
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_design_pipeline():
    W, H = 1086, 400
    s = SVG(W, H)
    s.text(W / 2, 28, "蛋白设计的标准流程：生成骨架 → 设计序列 → 结构验证", 15.5, "middle", 700)
    steps = [("靶点 + 表位", "指定要结合的位置\n（hotspot 残基）", OI["gray"]),
             ("RFdiffusion", "扩散生成蛋白骨架\n（只有主链坐标）", OI["purple"]),
             ("ProteinMPNN", "逆折叠：给骨架\n设计氨基酸序列", OI["blue"]),
             ("AlphaFold / ESMFold", "把序列折回去，\n看是否与目标骨架吻合", OI["green"]),
             ("湿实验", "表达、筛选、\n亲和力测定", OI["crimson"])]
    bw, gap = 190, 24
    for i, (a, b, c) in enumerate(steps):
        x = 20 + i * (bw + gap)
        s.box(x, 72, bw, 104, a, b.replace("\n", ""), color=c, size=13.5, subsize=11, tint=0.14)
        if i < 4:
            s.line(x + bw, 124, x + bw + gap, 124, OI["black"], 1.5)
    s.rect(234, 206, 614, 44, OI["green"], tint=0.08, rx=6)
    s.text(541, 233, "计算过滤：只有 RMSD 与 pLDDT 双双达标的设计才进入实验", 12.5, "middle", 600, OI["green"])
    s.path("M 1046 176 C 1046 300, 300 300, 300 250", OI["crimson"], 1.4, dash="3,3")
    s.text(620, 300, "实验结果回流：微调生成模型、更新筛选阈值", 12, "middle", 600, OI["crimson"])
    s.text(20, 352, "与小分子不同，蛋白设计不存在“可合成性”难题——任何序列都能用基因表达做出来。", 12, "start", 400, "#444")
    s.text(20, 378, "瓶颈因此从“能不能做出来”转移到“能不能成药”。", 12, "start", 600, "#444")
    return s.save(os.path.join(SV, "protein_design_pipeline.svg"))


def fig_antibody():
    W, H = 900, 440
    s = SVG(W, H)
    s.text(W / 2, 28, "抗体为什么特别难设计", 15.5, "middle", 700)
    # schematic Y-shaped antibody
    cx = 230
    s.line(cx, 300, cx, 230, OI["gray"], 14, head=None)
    s.line(cx, 232, cx - 85, 130, OI["gray"], 14, head=None)
    s.line(cx, 232, cx + 85, 130, OI["gray"], 14, head=None)
    for dx in (-85, 85):
        s.circle(cx + dx, 122, 22, OI["crimson"], tint=0.75)
    s.text(cx, 330, "抗体（示意）", 13, "middle", 600)
    s.text(cx, 92, "CDR 区", 12.5, "middle", 700, OI["crimson"])
    s.text(cx, 360, "重链 + 轻链各三个 CDR 环", 11.5, "middle", 400, "#555")
    reasons = [("CDR 环高度可变", "尤其 CDR-H3，长度和构象没有规律"),
               ("缺乏进化信息", "抗体多样性来自体细胞重组而非进化，MSA 方法失效"),
               ("靠柔性环而非规则二级结构", "普通结合蛋白设计依赖 α 螺旋 / β 折叠，原始 RFdiffusion 无法处理"),
               ("界面预测本身就难", "抗体–抗原复合物精度仍明显低于普通蛋白复合物")]
    for i, (a, b) in enumerate(reasons):
        s.box(430, 70 + i * 88, 450, 72, a, b, color=OI["blue"], size=13.5, subsize=11.5, tint=0.12)
    return s.save(os.path.join(SV, "antibody_difficulty.svg"))


def fig_developability():
    W, H = 1000, 460
    s = SVG(W, H)
    s.text(W / 2, 28, "从“能结合”到“能成药”：瓶颈的转移", 15.5, "middle", 700)
    s.box(60, 80, 300, 80, "能结合", "从头设计已取得突破：\nChai-2 迷你蛋白命中率 68%", color=OI["green"], size=15, subsize=11.5, tint=0.16)
    s.line(372, 120, 420, 120, OI["black"], 2)
    s.box(430, 80, 320, 80, "能成药", "可开发性与免疫原性\n仍是主要障碍", color=OI["crimson"], size=15, subsize=11.5, tint=0.16)
    items = [("亲和力与特异性", "是否结合脱靶蛋白"), ("热稳定性与化学稳定性", "储存与货架期"),
             ("聚集倾向", "高浓度下是否析出"), ("溶解度与黏度", "能否做成皮下注射剂"),
             ("表达量", "生产成本"), ("免疫原性", "是否引发抗药抗体"),
             ("药代动力学", "半衰期与给药频率"), ("易修饰位点", "氧化、脱酰胺影响一致性")]
    for i, (a, b) in enumerate(items):
        col = i % 4
        row = i // 4
        s.box(28 + col * 243, 210 + row * 96, 228, 78, a, b, color=OI["orange"], size=12.5, subsize=11, tint=0.12)
    s.text(500, 434, "AI 在这八项上的预测能力普遍弱于“能否结合”——这是生物药 AI 的下一个主战场", 12.5, "middle", 600, OI["crimson"])
    return s.save(os.path.join(SV, "developability.svg"))


def fig_modalities():
    plt = mpl_setup()
    import numpy as np
    mods = ["抗体", "迷你蛋白 /\n结合蛋白", "多肽", "siRNA / ASO", "ADC", "双特异性抗体"]
    design = [3.2, 4.3, 3.6, 2.4, 2.2, 2.6]
    develop = [2.6, 2.2, 2.4, 3.0, 1.9, 2.0]
    x = np.arange(len(mods)); w = 0.36
    fig, ax = plt.subplots(figsize=(8.2, 3.4))
    ax.bar(x - w / 2, design, w, color=OI["green"], label="AI 设计能力")
    ax.bar(x + w / 2, develop, w, color=OI["orange"], label="AI 可开发性 / 药代预测能力")
    ax.set_xticks(x); ax.set_xticklabels(mods, fontsize=10.5)
    ax.set_yticks([1, 2, 3, 4, 5]); ax.set_yticklabels(["很弱", "弱", "中", "较强", "强"])
    ax.set_ylim(0, 5.2)
    ax.set_title("各模态上 AI 能力的不均衡：设计能力普遍强于可开发性预测", loc="left")
    ax.legend(frameon=False, loc="upper right", fontsize=10)
    ax.text(0.0, -0.33, "纵轴为作者基于公开文献与报道的定性判断，非测量值。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.30)
    return save_chart(fig, os.path.join(SV, "modality_capability.svg"))


if __name__ == "__main__":
    print(fig_design_pipeline(), fig_antibody(), fig_developability())
    print(fig_modalities())
