import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")

def fig_pipeline():
    W, H = 1080, 470
    s = SVG(W, H)
    s.text(W / 2, 28, "AI 靶点发现的证据整合流程", 15.5, "middle", 700)
    src = [("人类遗传学", "GWAS、功能缺失变异、孟德尔随机化", OI["crimson"]),
           ("组学", "转录组、蛋白质组、单细胞", OI["blue"]),
           ("功能基因组学", "CRISPR 筛选、Perturb-seq、表型成像", OI["green"]),
           ("文献与知识", "PubMed、专利、临床试验、知识图谱", OI["purple"])]
    for i, (a, b, c) in enumerate(src):
        s.box(24, 60 + i * 92, 230, 72, a, b, color=c, size=13.5, subsize=11, tint=0.12)
    dims = ["因果证据强度", "疾病组织表达", "通路与网络位置", "可成药性", "安全性信号", "新颖性与竞争"]
    s.rect(330, 60, 230, 348, OI["gray"], tint=0.06)
    s.text(445, 84, "多维打分", 13.5, "middle", 700)
    for i, d in enumerate(dims):
        s.box(350, 98 + i * 50, 190, 38, d, None, color=OI["gray"], size=12.5, weight=400, tint=0.05)
    # converge arrows
    s.line(254, 96, 268, 96, OI["black"], 1.5, head=None); s.line(254, 372, 268, 372, OI["black"], 1.5, head=None)
    s.line(268, 96, 268, 372, OI["black"], 1.5, head=None)
    for i in range(1, 3):
        s.line(254, 60 + i * 92 + 36, 268, 60 + i * 92 + 36, OI["black"], 1.5, head=None)
    s.line(268, 234, 330, 234, OI["black"], 1.5)
    steps = [("排序与证据档案", "每个候选附可追溯证据", OI["orange"]), ("专家审核", "生物学合理性、竞争格局", OI["gray"]),
             ("实验验证", "敲除/过表达、动物模型", OI["green"]), ("立项", "进入药物发现", OI["crimson"])]
    for i, (a, b, c) in enumerate(steps):
        y = 60 + i * 92
        s.box(640, y, 210, 72, a, b, color=c, size=13.5, subsize=11, tint=0.12)
        if i < 3: s.line(745, y + 72, 745, y + 92, OI["black"], 1.5)
    s.line(560, 234, 600, 234, OI["black"], 1.5, head=None); s.line(600, 234, 600, 96, OI["black"], 1.5, head=None)
    s.line(600, 96, 640, 96, OI["black"], 1.5)
    # feedback loop
    s.path("M 850 400 C 930 400, 930 70, 852 70", OI["verm"], 1.4, dash="2,2")
    s.text(1000, 226, "失败与阴性结果", 11.5, "middle", 600, OI["verm"])
    s.text(1000, 244, "回流更新模型", 11.5, "middle", 600, OI["verm"])
    s.legend(24, 448, [("line", OI["black"], "证据与决策流", None)], size=11)
    s.legend(260, 448, [("line", OI["verm"], "反馈信号", "2,2")], size=11)
    return s.save(os.path.join(SV, "target_pipeline.svg"))

def fig_genetic():
    plt = mpl_setup()
    fig, ax = plt.subplots(figsize=(6.4, 2.4))
    labs = ["Nelson 等 2015", "Minikel 等 2024"]
    v = [2.0, 2.6]
    ax.barh([1, 0], v, color=[OI["sky"], OI["blue"]], height=0.5)
    for y, x in zip([1, 0], v): ax.text(x + 0.05, y, f"约 {x}×", va="center", fontsize=11)
    ax.axvline(1, color="#888", ls="--", lw=1); ax.text(1.02, 1.42, "无遗传学支持 = 1×", fontsize=9.5, color="#666")
    ax.set_yticks([1, 0]); ax.set_yticklabels(labs); ax.set_xlim(0, 3.2); ax.set_ylim(-0.5, 1.7)
    ax.set_xlabel("有人类遗传学支持的药物机制，从临床到获批的相对成功率")
    ax.set_title("遗传学证据让临床成功率提高到两倍以上", loc="left")
    for s_ in ("top", "right"): ax.spines[s_].set_visible(False)
    return save_chart(fig, os.path.join(SV, "genetic_support.svg"))

def fig_mr():
    W, H = 900, 390
    s = SVG(W, H)
    s.text(W / 2, 28, "孟德尔随机化：用遗传变异作为工具变量推断因果", 15.5, "middle", 700)
    G = (90, 200, 170, 64); X = (360, 200, 180, 64); Y = (650, 200, 180, 64); U = (500, 70, 180, 56)
    s.box(*G, "遗传变异 G", "受孕时随机分配", color=OI["green"], size=13.5, subsize=11)
    s.box(*X, "暴露 X", "如某血浆蛋白水平", color=OI["blue"], size=13.5, subsize=11)
    s.box(*Y, "结局 Y", "疾病", color=OI["crimson"], size=13.5, subsize=11)
    s.box(*U, "混杂因素 U", "生活方式、环境…", color=OI["gray"], size=13, subsize=11, dashed=True)
    s.line(260, 232, 360, 232, OI["black"], 2); s.text(310, 222, "① 相关性", 11.5, "middle", 600)
    s.line(540, 232, 650, 232, OI["black"], 2); s.text(595, 222, "待估因果效应", 11.5, "middle", 600, OI["crimson"])
    s.line(560, 126, 470, 200, OI["gray"], 1.3, dash="4,3"); s.line(630, 126, 720, 200, OI["gray"], 1.3, dash="4,3")
    s.text(270, 120, "② 独立性：G 与 U 无关", 11.5, "middle", 600, OI["green"])
    s.path("M 175 264 C 260 330, 640 330, 740 266", OI["verm"], 1.4, dash="2,3")
    s.text(450, 370, "③ 排他性：G 不能绕过 X 直接影响 Y（水平多效性会破坏这一点）", 11.5, "middle", 600, OI["verm"])
    s.legend(30, 350 - 4, [("line", OI["black"], "假设的因果路径", None)], size=10.5) if False else None
    return s.save(os.path.join(SV, "mendelian_randomization.svg"))

def fig_kg():
    W, H = 900, 400
    s = SVG(W, H)
    s.text(W / 2, 28, "知识图谱上的链接预测：预测缺失的“基因—疾病”边", 15.5, "middle", 700)
    nodes = {"药物 A": (140, 120, OI["orange"]), "基因 1": (340, 110, OI["blue"]), "基因 2": (340, 260, OI["blue"]),
             "通路 P": (540, 185, OI["green"]), "疾病 D": (760, 120, OI["crimson"]), "表型 F": (760, 280, OI["purple"]),
             "基因 3": (140, 290, OI["blue"])}
    edges = [("药物 A", "基因 1", "抑制"), ("基因 1", "通路 P", "参与"), ("基因 2", "通路 P", "参与"),
             ("通路 P", "疾病 D", "相关"), ("疾病 D", "表型 F", "表现为"), ("基因 3", "基因 2", "相互作用"),
             ("基因 1", "疾病 D", "已知关联")]
    def edge_pts(a, b):
        (x1, y1, _), (x2, y2, _) = nodes[a], nodes[b]
        import math
        d = math.hypot(x2 - x1, y2 - y1); r = 34
        return x1 + (x2 - x1) * r / d, y1 + (y2 - y1) * r / d, x2 - (x2 - x1) * r / d, y2 - (y2 - y1) * r / d
    for a, b, lab in edges:
        x1, y1, x2, y2 = edge_pts(a, b)
        s.line(x1, y1, x2, y2, OI["gray"], 1.4)
        s.text((x1 + x2) / 2, (y1 + y2) / 2 - 6, lab, 10.5, "middle", 400, "#555")
    s.path("M 372 272 C 560 370, 690 300, 732 148", OI["crimson"], 2, dash="6,4")
    s.text(600, 352, "预测：基因 2 → 疾病 D ？", 12, "middle", 700, OI["crimson"])
    for n, (x, y, c) in nodes.items():
        s.circle(x, y, 34, c, tint=0.15)
        s.text(x, y + 5, n, 12.5, "middle", 700)
    s.text(30, H - 16, "风险：研究得多的基因边更多，模型容易偏向“已知热门靶点”，与发现新靶点的目标相悖。", 11.5, "start", 400, "#444")
    return s.save(os.path.join(SV, "kg_link_prediction.svg"))

def fig_ladder():
    W, H = 1000, 380
    s = SVG(W, H)
    s.text(W / 2, 28, "靶点证据的阶梯：越往上越可信，也越贵、越慢", 15.5, "middle", 700)
    rungs = [("计算预测与回顾性重现", "天 · 几乎零成本 · 易受泄漏影响", OI["lgray"]),
             ("体外功能实验", "周–月 · 敲除/过表达、细胞表型", OI["sky"]),
             ("动物模型", "月–年 · 物种转化风险", OI["blue"]),
             ("人类遗传学证据", "已有数据 · 自然实验，因果性较强", OI["green"]),
             ("临床概念验证（II 期）", "年 · 千万美元级 · 唯一的金标准", OI["crimson"])]
    for i, (a, b, c) in enumerate(rungs):
        y = 300 - i * 58
        w = 380 + i * 90
        x = (W - w) / 2
        s.box(x, y, w, 46, a + "：" + b, None, color=c, size=12.5, weight=600 if i == 4 else 400, tint=0.18)
    s.line(60, 340, 60, 70, OI["black"], 1.5); s.text(72, 66, "可信度 / 成本", 11.5, "start", 600)
    return s.save(os.path.join(SV, "evidence_ladder.svg"))

if __name__ == "__main__":
    print(fig_pipeline(), fig_genetic(), fig_mr(), fig_kg(), fig_ladder())
