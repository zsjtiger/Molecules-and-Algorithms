import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")

# ---------------------------------------------------------- Fig 1-1 pipeline
def fig_pipeline():
    W, H = 1040, 430
    s = SVG(W, H)
    stages = [("靶点发现与验证", "1–3 年"), ("苗头发现", "0.5–1 年"), ("苗头到先导", "0.5–1 年"),
              ("先导优化", "1–2 年"), ("临床前研究", "1–2 年"), ("临床 I–III 期", "5–8 年"),
              ("审评与上市后", "1 年 + 长期")]
    # evidence maturity of AI per stage: 0 low,1 mid,2 high
    ev = [0, 2, 2, 1, 1, 0, 1]
    evc = {0: OI["verm"], 1: OI["orange"], 2: OI["green"]}
    evl = {0: "低", 1: "中", 2: "高"}
    x0, y0, bw, bh, gap = 20, 120, 120, 70, 28
    xs = [x0 + i * (bw + gap) for i in range(7)]
    # phase brackets
    def bracket(xa, xb, label, col):
        y = 82
        s.line(xa, y, xb, y, col, 1.5, head=None)
        s.line(xa, y, xa, y + 10, col, 1.5, head=None)
        s.line(xb, y, xb, y + 10, col, 1.5, head=None)
        s.text((xa + xb) / 2, y - 10, label, 14, "middle", 700, col)
    bracket(xs[0], xs[3] + bw, "药物发现（drug discovery）", OI["blue"])
    bracket(xs[4], xs[6] + bw, "药物开发（drug development）", OI["crimson"])
    s.text(W / 2, 30, "从靶点到上市：12–15 年，资本化成本约 10 亿–26 亿美元", 15, "middle", 700)
    for i, (n, t) in enumerate(stages):
        col = OI["blue"] if i < 4 else OI["crimson"]
        s.box(xs[i], y0, bw, bh, n, t, color=col, size=13, subsize=11)
        if i < 6:
            # decision gate diamond between stages
            cx = xs[i] + bw + gap / 2
            cy = y0 + bh / 2
            r = 8
            s.poly([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], OI["black"], fill="#ffffff", sw=1.2)
            s.line(xs[i] + bw, cy, cx - r, cy, OI["black"], 1.5, head=None)
            s.line(cx + r, cy, xs[i + 1], cy, OI["black"], 1.5)
    # AI evidence band
    yb = 240
    s.text(x0, yb - 12, "AI 在该环节的证据成熟度（2026）", 12.5, "start", 600)
    for i in range(7):
        s.box(xs[i], yb, bw, 34, evl[ev[i]], None, color=evc[ev[i]], size=13, tint=0.22)
    # value band
    val = [2, 1, 1, 1, 1, 2, 1]
    vl = {1: "中", 2: "极高"}
    yv = 312
    s.text(x0, yv - 12, "AI 若奏效的潜在经济价值", 12.5, "start", 600)
    for i in range(7):
        s.box(xs[i], yv, bw, 34, vl[val[i]], None, color=OI["purple"] if val[i] == 2 else OI["gray"], size=13, tint=0.18 if val[i] == 2 else 0.08)
    # legend
    s.legend(x0, 384, [("line", OI["black"], "阶段流转（菱形 = 继续/终止决策点）", None)], size=11)
    s.legend(430, 384, [("box", OI["green"], "高", None)], size=11)
    s.legend(490, 384, [("box", OI["orange"], "中", None)], size=11)
    s.legend(550, 384, [("box", OI["verm"], "低（证据成熟度）", None)], size=11)
    s.text(W - 20, 420, "注：成熟度与价值为作者基于第 1.7 节的综合判断", 10.5, "end", 400, "#666")
    return s.save(os.path.join(SV, "rd_pipeline.svg"))

# ---------------------------------------------------------- Fig 1-2 attrition
def fig_attrition():
    plt = mpl_setup()
    import numpy as np
    steps = ["进入 I 期", "进入 II 期", "进入 III 期", "提交上市申请", "获批"]
    rates = [1, 0.52, 0.289, 0.578, 0.906]
    vals = np.cumprod(rates) * 100
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    cols = [OI["blue"]] * 4 + [OI["crimson"]]
    ax.barh(range(5)[::-1], vals, color=[c + "cc" for c in cols], height=0.62)
    for i, v in enumerate(vals):
        ax.text(v + 1.5, 4 - i, f"{v:.1f}", va="center", fontsize=10)
    labs = [steps[0]] + [f"{steps[i]}（{rates[i]*100:.0f}%）" for i in range(1, 5)]
    ax.set_yticks(range(5)[::-1]); ax.set_yticklabels(labs)
    ax.set_xlim(0, 112)
    ax.set_xlabel("每 100 个进入 I 期的项目中仍存活的数量")
    ax.set_title("100 个进入 I 期的项目，约 8 个最终获批", loc="left")
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "attrition.svg"))

# ---------------------------------------------------------- Fig 1-3 failure reasons
def fig_failure():
    plt = mpl_setup()
    labs = ["缺乏疗效", "安全性", "战略或商业原因", "其他（药代、操作等）"]
    v = [52, 24, 15, 9]
    fig, ax = plt.subplots(figsize=(6.6, 2.7))
    y = list(range(len(v)))[::-1]
    cols = [OI["verm"], OI["orange"], OI["gray"], OI["lgray"]]
    for yi, vi, c in zip(y, v, cols):
        ax.hlines(yi, 0, vi, color=c, lw=2)
        ax.plot(vi, yi, "o", color=c, ms=9)
        ax.text(vi + 2, yi, f"{vi}%", va="center", fontsize=10)
    ax.set_yticks(y); ax.set_yticklabels(labs)
    ax.set_xlim(0, 62); ax.set_xlabel("占 II/III 期失败的比例（%）")
    ax.set_title("一半以上的后期失败源于“药物没有疗效”", loc="left")
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "failure_reasons.svg"))

# ---------------------------------------------------------- Fig 1-4 Eroom
def fig_eroom():
    plt = mpl_setup()
    import numpy as np
    t = np.linspace(1950, 2010, 200)
    y = 2 ** (-(t - 1950) / 9) * 100
    fig, ax = plt.subplots(figsize=(6.8, 3.4))
    ax.plot(t, y, color=OI["crimson"], lw=2)
    ax.set_yscale("log")
    ax.set_yticks([100, 10, 1, 0.1]); ax.set_yticklabels(["100", "10", "1", "0.1"])
    ax.set_xlabel("年份")
    ax.set_ylabel("每 10 亿美元研发投入\n获批新药数（1950 = 100）")
    ax.set_title("Eroom 定律：研发效率约每 9 年减半（趋势示意）", loc="left")
    ax.annotate("组合化学、高通量筛选、\n基因组学同期大幅进步", xy=(1990, 2 ** (-40 / 9) * 100), xytext=(1958, 0.35),
                fontsize=9.5, arrowprops=dict(arrowstyle="->", color="#555", lw=1))
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    ax.margins(x=0.02)
    return save_chart(fig, os.path.join(SV, "eroom.svg"))

# ---------------------------------------------------------- Fig 1-5 rNPV scenarios
def fig_rnpv():
    plt = mpl_setup()
    import numpy as np
    # 依 @tbl-rnpv-assumptions 的假设实算，不写死数字
    R = 0.10  # 折现率

    def rnpv(rev, disc_years=4.0, disc_cost=30.0, p1=0.52, p2=0.29):
        """阶段：(时长, 成本, 该阶段结束时的成功率)；成本在阶段中点发生。"""
        stages = [(disc_years, disc_cost, 0.70),   # 药物发现到 IND
                  (1.0, 15.0, 1.00),               # 临床前
                  (1.5, 25.0, p1),                 # I 期
                  (2.5, 60.0, p2),                 # II 期
                  (3.0, 250.0, 0.58),              # III 期
                  (1.0, 5.0, 0.91)]                # 审评
        t, p, v = 0.0, 1.0, 0.0
        for dur, cost, ps in stages:
            v -= p * cost / (1 + R) ** (t + dur / 2)   # 成本按进入该阶段的概率加权
            t += dur
            p *= ps
        for k in range(10):                             # 上市后 10 年净收入
            v += p * rev / (1 + R) ** (t + k + 0.5)
        return v

    base400, base1000 = rnpv(400), rnpv(1000)
    # A1 发现期缩短 1.5 年；A2 发现成本减半；B/C 为成功率提升
    sc = [("A1 仅缩短发现时间", dict(disc_years=2.5)),
          ("A2 仅减半发现成本", dict(disc_cost=15.0)),
          ("A  A1+A2", dict(disc_years=2.5, disc_cost=15.0)),
          ("B  I 期成功率 52→80%", dict(p1=0.80)),
          ("C  II 期成功率 29→40%", dict(p2=0.40)),
          ("D  B+C", dict(p1=0.80, p2=0.40)),
          ("E  A+B+C", dict(disc_years=2.5, disc_cost=15.0, p1=0.80, p2=0.40))]
    lab = [a for a, _ in sc]
    d400 = [rnpv(400, **kw) - base400 for _, kw in sc]
    d1000 = [rnpv(1000, **kw) - base1000 for _, kw in sc]
    print(f"  rNPV 基准：4 亿 {base400:+.0f}，10 亿 {base1000:+.0f}（百万美元）")
    y = np.arange(len(lab))[::-1]
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    h = 0.36
    ax.barh(y + h / 2, d400, h, color=OI["sky"], label="上市后年净收入 4 亿美元")
    ax.barh(y - h / 2, d1000, h, color=OI["blue"], label="上市后年净收入 10 亿美元")
    for yi, a, b in zip(y, d400, d1000):
        # 保留一位小数：4 亿情景下 A2/B/C 的数值非常接近，取整会误显示为完全相同
        ax.text(max(a, 0) + 2, yi + h / 2, f"{a:+.1f}", va="center", fontsize=9)
        ax.text(b + 2, yi - h / 2, f"{b:+.1f}", va="center", fontsize=9)
    ax.axvline(0, color="#333", lw=0.8)
    ax.set_yticks(y); ax.set_yticklabels(lab)
    ax.set_xlabel("相对基准的 rNPV 变化（百万美元）")
    ax.set_xlim(-10, 170)
    ax.set_title("成功率的价值随市场规模放大，成本节省则不会", loc="left")
    ax.legend(frameon=False, loc="upper right")
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "rnpv_scenarios.svg"))

# ---------------------------------------------------------- Fig 1-6 value map
def fig_valuemap():
    plt = mpl_setup()
    # 末三项为标签偏移与对齐方式，手工指定以避免密集区标签互相遮挡
    pts = [("靶点发现与验证", 0.6, 2.85, 0.07, 0.07, "left"),
           ("苗头发现", 2.75, 1.45, -0.08, 0.07, "right"),
           ("先导优化", 2.3, 1.7, -0.08, 0.07, "right"),
           ("ADMET 预测", 1.95, 1.3, 0.08, 0.02, "left"),
           ("生物药设计", 1.62, 2.05, -0.09, -0.03, "right"),
           ("临床设计与患者分层", 0.9, 2.65, 0.07, 0.07, "left"),
           ("临床运营", 1.78, 2.22, 0.09, -0.03, "left"),
           ("注册与医学写作", 1.65, 1.5, -0.09, -0.03, "right"),
           ("商业化与医学事务", 1.95, 1.93, 0.09, -0.03, "left")]
    fig, ax = plt.subplots(figsize=(6.6, 4.6))
    ax.axvspan(0, 1.5, ymin=0.5, ymax=1, color=OI["verm"], alpha=0.07)
    ax.text(0.07, 2.12, "高价值 · 低证据\n（2026 年的核心矛盾）", fontsize=9.5, color=OI["verm"], va="bottom")
    for n, x, y, dx, dy, ha in pts:
        c = OI["verm"] if (x < 1.5 and y > 2) else OI["blue"]
        ax.plot(x, y, "o", color=c, ms=8)
        ax.text(x + dx, y + dy, n, fontsize=9.5, ha=ha, va="center")
    ax.set_xlim(0, 3.1); ax.set_ylim(1, 3)
    ax.set_xticks([0.5, 1.5, 2.5]); ax.set_xticklabels(["低", "中", "高"])
    ax.set_yticks([1.25, 2.0, 2.75]); ax.set_yticklabels(["中", "高", "极高"])
    ax.set_xlabel("AI 有效性的证据成熟度（2026）")
    ax.set_ylabel("AI 若奏效的潜在经济价值")
    ax.set_title("证据最充分的环节价值中等，价值最高的环节证据最少", loc="left", fontsize=11)
    ax.axvline(1.5, color="#bbb", lw=0.8, ls="--"); ax.axhline(2.0, color="#bbb", lw=0.8, ls="--")
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "value_map.svg"))

if __name__ == "__main__":
    print("pipeline", fig_pipeline())
    print("attrition", fig_attrition())
    print("failure", fig_failure())
    print("eroom", fig_eroom())
    print("rnpv", fig_rnpv())
    print("valuemap", fig_valuemap())
