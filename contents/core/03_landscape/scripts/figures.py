import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")

def fig_spectrum():
    W, H = 1060, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "“AI 药物”的定义光谱：AI 参与得越深，统计口径越窄", 15.5, "middle", 700)
    # gradient bar via steps
    x0, x1, y = 40, 1020, 70
    stages = ["靶点", "分子", "优化", "临床策略"]
    levels = [("L1 辅助", "局部环节用 AI：性质预测、虚拟筛选", [0, 0, 1, 0], OI["sky"]),
              ("L2 优化", "人定靶点与骨架，AI 主导先导优化", [0, 0, 2, 0], OI["blue"]),
              ("L3 生成", "靶点已知，分子主要由生成模型产生", [0, 2, 2, 0], OI["orange"]),
              ("L4 端到端", "靶点、分子、临床策略均有 AI 参与", [2, 2, 2, 1], OI["crimson"]),
              ("表型驱动", "不预设靶点，从细胞表型中发现", [2, 1, 1, 0], OI["green"])]
    colx = [470, 600, 730, 860]
    for i, st in enumerate(stages):
        s.text(colx[i] + 50, y + 8, st, 12.5, "middle", 600)
    for r, (name, desc, cov, col) in enumerate(levels):
        yy = y + 24 + r * 50
        s.box(40, yy, 120, 38, name, None, color=col, size=13, tint=0.18)
        s.text(175, yy + 24, desc, 12, "start", 400)
        for i, c in enumerate(cov):
            fill = {0: "#ffffff", 1: col, 2: col}[c]
            op = {0: 1.0, 1: 0.35, 2: 0.9}[c]
            s.L.append(f'  <rect x="{colx[i]+5}" y="{yy+4}" width="90" height="30" rx="4" fill="{fill}" fill-opacity="{op}" stroke="{col}" stroke-width="1.2"/>')
    s.text(1000, y + 8, "代表", 12.5, "middle", 600)
    reps = ["多数药企项目", "zasocitinib*", "多数初创项目", "rentosertib", "REC-4881"]
    for r, t in enumerate(reps):
        s.text(1000, y + 24 + r * 50 + 24, t, 11.5, "middle", 400)
    # 图例按"填充深浅"而非颜色说明：每行的颜色只用于区分层级，深浅才表示参与度
    lg = OI["crimson"]
    s.L.append(f'  <rect x="400" y="{H-68}" width="18" height="14" rx="3" fill="{lg}" fill-opacity="0.9" stroke="{lg}" stroke-width="1.2"/>')
    s.text(424, H - 57, "深色填充：AI 主导该环节", 11, "start")
    s.L.append(f'  <rect x="600" y="{H-68}" width="18" height="14" rx="3" fill="{lg}" fill-opacity="0.35" stroke="{lg}" stroke-width="1.2"/>')
    s.text(624, H - 57, "浅色填充：AI 参与但不主导", 11, "start")
    s.L.append(f'  <rect x="812" y="{H-68}" width="18" height="14" rx="3" fill="#ffffff" stroke="{lg}" stroke-width="1.2"/>')
    s.text(836, H - 57, "空白：无 AI 或未披露", 11, "start")
    s.text(40, H - 57, "（行内颜色仅区分层级）", 10.5, "start", 400, "#777")
    s.text(40, H - 14, "* zasocitinib 的发现主要依靠基于物理的计算（FEP 等），属于“计算驱动”而非生成式 AI。", 10.5, "start", 400, "#666")
    return s.save(os.path.join(SV, "ai_spectrum.svg"))

def fig_rentosertib():
    W, H = 1080, 330
    s = SVG(W, H)
    s.text(W / 2, 28, "rentosertib（TNIK 抑制剂，特发性肺纤维化）：端到端 AI 药物的研发路径", 15.5, "middle", 700)
    steps = [("靶点识别", "PandaOmics：多组学、网络、文献、衰老评分 → TNIK", OI["green"]),
             ("分子设计", "Chemistry42 生成式化学，约 18 个月到候选化合物", OI["blue"]),
             ("I 期", "健康受试者安全性与药代", OI["sky"]),
             ("IIa 期（2025）", "71 例 IPF 患者；12 周 FVC +98.4 mL vs 安慰剂 −20.3 mL", OI["orange"]),
             ("III 期（2026.7）", "320 例；52 周；主要终点 FVC 年下降率", OI["crimson"]),
             ("读出与申报", "公司规划约 2029 年读出", OI["gray"])]
    bw, bh, gap, x0, y0 = 158, 104, 20, 22, 92
    for i, (a, b, c) in enumerate(steps):
        x = x0 + i * (bw + gap)
        dashed = (i == 5)
        s.box(x, y0, bw, bh, a, b, color=c, dashed=dashed, size=13.5, subsize=11.5, tint=0.13)
        if i < 5:
            s.line(x + bw, y0 + bh / 2, x + bw + gap, y0 + bh / 2, OI["black"], 1.5)
    # AI involvement ribbon
    s.text(x0, 238, "AI 参与：", 12.5, "start", 600)
    s.rect(x0 + 70, 222, (bw + gap) * 2 - gap - 70, 22, OI["crimson"], tint=0.25, rx=3)
    s.text(x0 + 70 + ((bw + gap) * 2 - gap - 70) / 2, 238, "靶点 + 分子", 11.5, "middle", 600, OI["crimson"])
    s.rect(x0 + 3 * (bw + gap), 222, bw * 2 + gap, 22, OI["crimson"], tint=0.12, rx=3)
    s.text(x0 + 3 * (bw + gap) + (bw * 2 + gap) / 2, 238, "临床结局预测（inClinico）辅助设计", 11.5, "middle", 400, OI["crimson"])
    s.text(x0, 300, "虚线框为尚未发生的阶段。II a 期数据来自《自然·医学》2025 年 6 月；III 期信息来自公司公告与登记记录（NCT07687459）。", 10.5, "start", 400, "#666")
    return s.save(os.path.join(SV, "rentosertib_path.svg"))

def fig_phase_success():
    plt = mpl_setup()
    fig, ax = plt.subplots(figsize=(6.8, 2.6))
    # ci 为该行的 95% 置信区间（II 期按正文"10 个项目、4 个成功"估算），None 表示原文未给出
    rows = [("I 期成功率", (80, 90), 52, None),
            ("II 期成功率", (35, 45), 29, (12, 74))]
    for i, (lab, (lo, hi), hist, ci) in enumerate(rows):
        y = 1 - i
        if ci:
            ax.hlines(y, ci[0], ci[1], color=OI["crimson"], lw=16, alpha=0.16)
            ax.text(ci[1] + 2, y, f"95% 置信区间 {ci[0]}–{ci[1]}%（约 10 个项目）",
                    va="center", fontsize=10, color="#777")
        ax.hlines(y, lo, hi, color=OI["crimson"], lw=7, alpha=0.9)
        ax.plot(hist, y, "D", color=OI["gray"], ms=9)
        ax.text((lo + hi) / 2, y + 0.3, f"AI 发现分子 {lo}–{hi}%",
                va="center", ha="center", fontsize=10.5, color=OI["crimson"])
        ax.text(hist, y - 0.3, f"历史平均 {hist}%", va="center", ha="center", fontsize=10.5, color="#555")
    ax.set_yticks([1, 0]); ax.set_yticklabels([r[0] for r in rows])
    ax.set_xlim(0, 118); ax.set_ylim(-0.6, 1.6)
    ax.set_xlabel("阶段转换成功率（%）"); ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_title("AI 分子 I 期明显更好，II 期样本少、区间宽", loc="left")
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "ai_phase_success.svg"))

def fig_zaso():
    plt = mpl_setup()
    import numpy as np
    ends = ["sPGA 0/1", "PASI 75", "PASI 90", "PASI 100"]
    data = {"3001（n=693）": {"zasocitinib": [71, 76, 61, 33], "阿普米司特": [32, 37, 17, 3], "安慰剂": [11, 12, 5, 0.7]},
            "3002（n=1108）": {"zasocitinib": [69, 71, 52, 25], "阿普米司特": [30, 33, 16, 4], "安慰剂": [13, 12, 4, 1]}}
    cols = {"zasocitinib": OI["crimson"], "阿普米司特": OI["sky"], "安慰剂": OI["lgray"]}
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.5), sharey=True, gridspec_kw={"wspace": 0.06})
    for ax, (study, d) in zip(axes, data.items()):
        x = np.arange(4); w = 0.26
        for k, (arm, v) in enumerate(d.items()):
            ax.bar(x + (k - 1) * w, v, w, color=cols[arm], label=arm)
            if arm == "zasocitinib":
                for xi, vi in zip(x, v): ax.text(xi - w, vi + 1.5, f"{vi}", ha="center", fontsize=9.5)
        ax.set_xticks(x); ax.set_xticklabels(ends)
        ax.set_title(f"LATITUDE {study}", loc="left", fontsize=11.5)
        ax.set_ylim(0, 88)
        for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    axes[0].set_ylabel("第 16 周应答率（%）")
    axes[1].legend(frameon=False, loc="upper right", fontsize=10)
    return save_chart(fig, os.path.join(SV, "zasocitinib_ph3.svg"))

if __name__ == "__main__":
    print(fig_spectrum(), fig_rentosertib(), fig_phase_success(), fig_zaso())
