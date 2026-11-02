import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_confidence():
    plt = mpl_setup()
    import numpy as np
    items = [("共结构–亲和力统一模型成为标配", 4.5, 2028),
             ("自驱动实验室在头部企业常规化", 4.0, 2029),
             ("抗体从头设计进入常规管线", 3.2, 2030),
             ("监管接受 AI 支撑的关键结论（首例）", 3.0, 2029),
             ("AI 来源药物完成 III 期获批（多例）", 2.8, 2031),
             ("可信的临床结局预测", 1.8, 2034),
             ("端到端自主发现（无人干预）", 1.2, 2035)]
    y = np.arange(len(items))[::-1]
    conf = [c for _, c, _ in items]
    names = [n for n, _, _ in items]
    yrs = [t for _, _, t in items]
    cols = [OI["green"] if c >= 3.5 else (OI["orange"] if c >= 2.5 else OI["verm"]) for c in conf]
    fig, ax = plt.subplots(figsize=(8.2, 3.9))
    ax.barh(y, conf, 0.56, color=cols)
    for yi, c, t in zip(y, conf, yrs):
        ax.text(c + 0.09, yi, f"约 {t} 年", va="center", fontsize=10.5, color="#555")
    ax.set_yticks(y); ax.set_yticklabels(names)
    ax.set_xticks([1, 2, 3, 4, 5]); ax.set_xticklabels(["很低", "低", "中", "较高", "高"])
    ax.set_xlim(0, 6.0)
    ax.set_xlabel("作者对该判断的信心")
    ax.set_title("2027–2035 的七项判断：按信心排序，而非按重要性", loc="left")
    ax.text(0.0, -0.32, "信心与时间均为作者的主观判断，列出是为了便于日后核对，而非预测。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.26, left=0.33)
    return save_chart(fig, os.path.join(SV, "trend_confidence.svg"))


def fig_drivers():
    W, H = 1040, 460
    s = SVG(W, H)
    s.text(W / 2, 28, "驱动与制约：决定速度的不是算法", 15.5, "middle", 700)
    s.box(24, 66, 490, 46, "加速因素", None, color=OI["green"], size=14, tint=0.18)
    s.box(526, 66, 490, 46, "制约因素", None, color=OI["verm"], size=14, tint=0.18)
    acc = [("实验自动化成本下降", "缩短飞轮周期，这是影响最大的一项"),
           ("统一模型替代拼接流程", "减少格式转换与无声失败"),
           ("监管路径逐步明确", "降低了采用新方法的不确定性"),
           ("评测标准开始建立", "使真实进展更容易与噪声区分")]
    con = [("临床数据的稀缺不会改变", "样本量受制于试验本身的成本与伦理"),
           ("疾病机制知识的增长缓慢", "这是知识问题，不随算力增长"),
           ("数据共享的激励不对称", "联盟难以维系，各自为政持续"),
           ("验证周期无法压缩", "临床试验的时长由生物学决定")]
    for i, (a, b) in enumerate(acc):
        y = 128 + i * 78
        s.text(30, y + 18, a, 12.5, "start", 700, OI["green"])
        s.text(30, y + 42, b, 11.5, "start", 400, "#444")
    for i, (a, b) in enumerate(con):
        y = 128 + i * 78
        s.text(532, y + 18, a, 12.5, "start", 700, OI["verm"])
        s.text(532, y + 42, b, 11.5, "start", 400, "#444")
    s.line(518, 66, 518, 426, OI["lgray"], 1.2, head=None)
    s.text(520, 450, "右栏多数是生物学与制度的约束，不随计算能力提升而放松",
           12.5, "middle", 700, "#444")
    return s.save(os.path.join(SV, "drivers.svg"))


def fig_scenarios():
    W, H = 1050, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "三种情景：区别在后端而非前端", 15.5, "middle", 700)
    cols = [("渐进情景（最可能）", OI["blue"],
             ["前端环节持续提效，周期与成本改善明确",
              "临床成功率小幅提升，统计上需十年才能确认",
              "行业结构：与传统药企深度融合，不再单列"]),
            ("加速情景", OI["green"],
             ["自动化与统一模型使飞轮周期缩短一个数量级",
              "在少数机制清晰的疾病领域出现成功率跃升",
              "行业结构：出现若干以平台为核心的新型大药企"]),
            ("停滞情景", OI["verm"],
             ["前端提效的收益被后端失败吞没",
              "资本退潮，自研管线被迫转为服务",
              "行业结构：AI 退回为常规工具，不再是叙事中心"])]
    bw, gap = 320, 22
    for i, (title, c, items) in enumerate(cols):
        x = 20 + i * (bw + gap)
        s.box(x, 66, bw, 46, title, None, color=c, size=13.5, tint=0.18)
        for j, t in enumerate(items):
            s.box(x + 8, 126 + j * 72, bw - 16, 62, t, None, color=c, size=11.5,
                  weight=400, tint=0.08)
    s.rect(20, 356, 980, 44, OI["purple"], tint=0.10, rx=6)
    s.text(510, 384, "三种情景在 2030 年前的前端表现相似，区分它们的是后端的临床数据",
           12.5, "middle", 700, OI["purple"])
    return s.save(os.path.join(SV, "scenarios.svg"))


if __name__ == "__main__":
    print(fig_drivers(), fig_scenarios())
    print(fig_confidence())
