import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")

def fig_af2():
    W, H = 1080, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "AlphaFold2 的整体架构", 15.5, "middle", 700)
    s.poly([(30, 90), (200, 90), (180, 150), (10, 150)], OI["gray"], tint=0.08)
    s.text(105, 125, "目标序列", 13, "middle", 600)
    s.box(20, 170, 180, 60, "MSA 搜索", "同源序列 → 共进化", color=OI["green"], size=13, subsize=11)
    s.box(20, 250, 180, 60, "模板搜索（可选）", "已知同源结构", color=OI["gray"], size=13, subsize=11, dashed=True)
    # embeddings
    s.box(250, 110, 170, 70, "MSA 表示", "N_seq × L × c_m", color=OI["green"], size=13, subsize=11)
    s.box(250, 230, 170, 70, "对表示", "L × L × c_z", color=OI["blue"], size=13, subsize=11)
    for y in (125, 155):
        pass
    s.line(200, 200, 250, 145, OI["black"], 1.5); s.line(200, 280, 250, 265, OI["black"], 1.5)
    s.line(105, 150, 105, 170, OI["black"], 1.5)
    # evoformer
    s.rect(470, 80, 260, 250, OI["purple"], tint=0.07)
    s.text(600, 104, "Evoformer × 48", 14, "middle", 700, OI["purple"])
    ops = ["MSA 行注意力（对表示作偏置）", "MSA 列注意力", "外积均值：MSA → 对表示", "三角乘法更新", "三角注意力"]
    for i, o in enumerate(ops):
        s.box(488, 118 + i * 41, 224, 33, o, None, color=OI["purple"], size=12, weight=400, tint=0.05)
    s.line(420, 145, 470, 145, OI["black"], 1.5); s.line(420, 265, 470, 265, OI["black"], 1.5)
    # structure module
    s.box(770, 140, 170, 120, "结构模块 × 8", "不变点注意力（IPA）；每残基一个刚体框架", color=OI["crimson"], size=13.5, subsize=11, tint=0.12)
    s.line(730, 200, 770, 200, OI["black"], 1.5)
    s.box(965, 120, 105, 60, "全原子坐标", None, color=OI["black"], size=12, tint=0.05)
    s.box(965, 210, 105, 70, "置信度", "pLDDT · PAE · pTM", color=OI["orange"], size=12, subsize=10.5, tint=0.12)
    s.line(940, 175, 965, 150, OI["black"], 1.5); s.line(940, 230, 965, 245, OI["black"], 1.5)
    # recycling
    s.path("M 870 260 C 870 380, 335 380, 335 300", OI["gray"], 1.4, dash="5,3")
    s.text(600, 372, "循环（recycling）：输出重新作为输入，迭代 3 次左右", 11.5, "middle", 600, "#555")
    s.text(600, 405, "训练损失：框架对齐点误差（FAPE），不受全局旋转平移影响", 11.5, "middle", 400, "#555")
    return s.save(os.path.join(SV, "af2_arch.svg"))

def fig_af3():
    W, H = 1080, 360
    s = SVG(W, H)
    s.text(W / 2, 28, "AlphaFold3 的三处根本变化", 15.5, "middle", 700)
    inp = ["蛋白质链", "DNA / RNA", "小分子配体", "离子、修饰残基"]
    for i, t in enumerate(inp):
        s.box(24, 64 + i * 62, 170, 48, t, None, color=OI["green"] if i < 2 else OI["orange"], size=13, tint=0.12)
    s.text(109, 330, "① 输入扩展到一切生物分子", 12, "middle", 700, OI["green"])
    s.line(194, 88, 226, 88, OI["black"], 1.5, head=None); s.line(194, 274, 226, 274, OI["black"], 1.5, head=None)
    s.line(194, 150, 226, 150, OI["black"], 1.5, head=None); s.line(194, 212, 226, 212, OI["black"], 1.5, head=None)
    s.line(226, 88, 226, 274, OI["black"], 1.5, head=None); s.line(226, 180, 260, 180, OI["black"], 1.5)
    s.box(260, 120, 150, 120, "小型 MSA 模块", "对 MSA 的依赖大幅降低", color=OI["gray"], size=13, subsize=11)
    s.line(410, 180, 450, 180, OI["black"], 1.5)
    s.box(450, 100, 220, 160, "Pairformer × 48", "只维护单一表示与对表示，保留三角更新操作", color=OI["purple"], size=14, subsize=11.5, tint=0.10)
    s.text(560, 330, "② 用 Pairformer 替代 Evoformer", 12, "middle", 700, OI["purple"])
    s.line(670, 180, 710, 180, OI["black"], 1.5)
    s.box(710, 100, 220, 160, "扩散模块", "从噪声出发逐步去噪，直接生成全原子坐标；无需残基框架参数化", color=OI["crimson"], size=14, subsize=11.5, tint=0.12)
    s.text(820, 330, "③ 用扩散生成替代坐标回归", 12, "middle", 700, OI["crimson"])
    s.line(930, 180, 960, 180, OI["black"], 1.5)
    s.box(960, 130, 100, 100, "复合物结构 + 置信度", None, color=OI["black"], size=12.5, tint=0.05)
    return s.save(os.path.join(SV, "af3_changes.svg"))

def fig_frontier():
    W, H = 900, 470
    s = SVG(W, H)
    s.text(W / 2, 28, "亲和力预测的精度–成本前沿（示意）", 15.5, "middle", 700)
    L, R, T, B = 110, 860, 60, 400
    s.line(L, B, R, B, OI["black"], 1.3); s.line(L, B, L, T, OI["black"], 1.3)
    s.text((L + R) / 2, B + 40, "每个分子的计算成本（对数尺度）：毫秒 → 秒 → 分钟 → 小时 → 天", 12.5, "middle", 600)
    s.L.append(f'  <text x="{L-56}" y="{(T+B)/2}" font-size="12.5" font-weight="600" text-anchor="middle" transform="rotate(-90 {L-56} {(T+B)/2})">对同系列化合物的排序精度</text>')
    # regions as ellipses (qualitative)
    def blob(cx, cy, rx, ry, c, lab, sub):
        s.L.append(f'  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{c}" fill-opacity="0.18" stroke="{c}" stroke-width="1.5"/>')
        s.text(cx, cy - 2, lab, 13, "middle", 700)
        s.text(cx, cy + 16, sub, 11, "middle", 400, "#444")
    blob(200, 330, 80, 42, OI["gray"], "对接打分", "极快 · 精度低")
    blob(440, 280, 95, 42, OI["sky"], "MM/GBSA", "中等成本 · 中低精度")
    blob(720, 140, 115, 50, OI["blue"], "FEP / RBFE", "数小时 GPU · 约 1 kcal/mol")
    blob(330, 150, 110, 50, OI["crimson"], "Boltz-2 等 AI 模型", "FEP+ 基准 r ≈ 0.62，快 1000× 以上")
    s.path("M 610 140 C 520 120, 470 120, 445 140", OI["crimson"], 1.5, dash="4,3")
    s.text(530, 112, "目标：以低成本逼近物理方法精度", 11.5, "middle", 600, OI["crimson"])
    s.text(R, H - 12, "注：位置为定性示意；仅 Boltz-2 的数值来自原始报告 [Passaro 等 2025]", 10.5, "end", 400, "#666")
    return s.save(os.path.join(SV, "affinity_frontier.svg"))

def fig_landscape():
    plt = mpl_setup()
    import numpy as np
    x = np.linspace(0, 10, 500)
    y = 2.2 * np.exp(-((x - 2.5) ** 2) / 0.9) * -1 + -1.6 * np.exp(-((x - 7.0) ** 2) / 1.1) + 0.05 * (x - 5) ** 2 + 2.5
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    ax.plot(x, y, color=OI["blue"], lw=2.2)
    i1 = np.argmin(np.where(x < 5, y, 99)); i2 = np.argmin(np.where(x > 5, y, 99))
    ax.plot(x[i1], y[i1], "o", color=OI["gray"], ms=9); ax.plot(x[i2], y[i2], "o", color=OI["crimson"], ms=9)
    ax.annotate("apo 构象（无配体）\n口袋关闭——AF 常预测这里", (x[i1], y[i1]), xytext=(3.25, 0.12), fontsize=10.5,
                arrowprops=dict(arrowstyle="->", color="#555"))
    ax.annotate("holo 构象（配体结合）\n隐蔽口袋打开", (x[i2], y[i2]), xytext=(7.55, 0.12), fontsize=10.5, color=OI["crimson"],
                arrowprops=dict(arrowstyle="->", color=OI["crimson"]))
    ax.annotate("构象转变能垒", (4.9, y[np.argmin(abs(x-4.9))]), xytext=(4.0, 3.6), fontsize=10.5, arrowprops=dict(arrowstyle="->", color="#555"))
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel("构象坐标（如口袋开合程度）"); ax.set_ylabel("自由能")
    ax.set_title("蛋白不是一张照片：药物常结合在非基态构象上", loc="left")
    ax.set_ylim(-0.2, 4.3)
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "conformational_landscape.svg"))

def fig_workflow():
    W, H = 1080, 300
    s = SVG(W, H)
    s.text(W / 2, 28, "结构预测在药物研发中的实用流程与检查点", 15.5, "middle", 700)
    steps = [("获取靶点结构", "实验结构优先；否则 AF/Boltz 预测", OI["gray"]),
             ("口袋识别", "检查口袋区域 pLDDT", OI["blue"]),
             ("复合物预测", "多模型交叉（AF3、Boltz、Chai）", OI["purple"]),
             ("物理合理性检查", "PoseBusters；能量最小化", OI["orange"]),
             ("亲和力估计", "AI 模型初筛，FEP 精排", OI["crimson"]),
             ("实验验证", "晶体 / 冷冻电镜 + 活性", OI["green"])]
    bw, gap = 160, 16
    for i, (a, b, c) in enumerate(steps):
        x = 24 + i * (bw + gap)
        s.box(x, 80, bw, 96, a, b, color=c, size=13.5, subsize=11, tint=0.12)
        if i < 5: s.line(x + bw, 128, x + bw + gap, 128, OI["black"], 1.5)
    s.path("M 1000 176 C 1000 260, 104 260, 104 176", OI["green"], 1.4, dash="2,2")
    s.text(552, 262, "新的实验结构与亲和力数据回流，用于微调或校准模型", 11.5, "middle", 600, OI["green"])
    return s.save(os.path.join(SV, "structure_workflow.svg"))

if __name__ == "__main__":
    print(fig_af2(), fig_af3(), fig_frontier(), fig_landscape(), fig_workflow())
