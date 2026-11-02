import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_six_questions():
    W, H = 660, 548
    s = SVG(W, H)
    s.text(W / 2, 28, "AI 制药的六个伦理问题：各自的争议焦点", 15.5, "middle", 700)
    rows = [("可及性", "效率提升的收益流向哪里：更低的药价，还是更高的利润？",
             "技术本身不决定分配；定价与报销制度决定", OI["crimson"]),
            ("研究方向的公平", "AI 会优先改善数据多的领域，而数据多的领域本就是富裕市场的疾病",
             "被忽视疾病可能因偏差放大而进一步落后", OI["orange"]),
            ("数据主体的权益", "患者数据训练出的模型产生了商业价值，患者是否分享收益？",
             "知情同意的范围通常不覆盖后续的模型训练", OI["blue"]),
            ("责任归属", "当基于模型输出的决策造成损害，责任在开发者、使用者还是机构？",
             "现有法律框架以人的判断为前提，适配尚不完整", OI["purple"]),
            ("人群代表性", "训练数据以特定人群为主，模型在其他人群中的可靠性未知",
             "这是科学问题，也是分配正义问题", OI["green"]),
            ("人的位置", "当模型承担越来越多的判断，专业判断力会不会退化？",
             "长期风险：丧失独立评估模型输出的能力", OI["sky"])]
    for i, (a, b, c, col) in enumerate(rows):
        y = 62 + i * 78
        s.box(24, y, 176, 64, a, None, color=col, size=13.5, tint=0.17)
        s.text(222, y + 26, b, 12.5, "start", 400)
        s.text(222, y + 50, c, 12, "start", 600, col)
    s.text(24, 542, "六个问题的共同点：技术进步不会自动解决它们，反而常在技术最成功时最尖锐。",
           12.5, "start", 700, "#444")
    return s.save(os.path.join(SV, "six_questions.svg"))


def fig_neglected():
    plt = mpl_setup()
    import numpy as np
    cats = ["肿瘤", "免疫与炎症", "神经退行", "代谢", "罕见病", "被忽视的热带病"]
    data = [4.8, 4.0, 3.4, 3.6, 2.4, 0.9]
    burden = [3.2, 3.0, 3.4, 4.2, 1.8, 3.8]
    x = np.arange(len(cats)); w = 0.36
    fig, ax = plt.subplots(figsize=(8.2, 3.6))
    ax.bar(x - w / 2, data, w, color=OI["blue"], label="可用数据与研发投入")
    ax.bar(x + w / 2, burden, w, color=OI["orange"], label="全球疾病负担")
    ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=10.5)
    ax.set_yticks([1, 2, 3, 4, 5]); ax.set_yticklabels(["很低", "低", "中", "高", "很高"])
    ax.set_ylim(0, 5.8)
    ax.legend(frameon=False, loc="lower right", ncol=2, bbox_to_anchor=(1.0, 1.01), fontsize=10)
    ax.set_title("数据多的地方不是负担重的地方：AI 会放大这个错配", loc="left", pad=22)
    ax.text(0.0, -0.30, "定性示意，用于说明错配方向，非量化指标。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.26)
    return save_chart(fig, os.path.join(SV, "neglected_mismatch.svg"))


def fig_responsibility():
    W, H = 1020, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "责任链条：每一环都可以指向下一环", 15.5, "middle", 700)
    nodes = [("模型开发者", "我只提供工具，\n不对具体使用负责"),
             ("平台提供方", "我按合同交付，\n科学判断在客户"),
             ("使用的研究者", "我按流程使用，\n模型是机构批准的"),
             ("决策机构", "我依据专业人员的\n建议做出决定")]
    bw, gap = 220, 36
    for i, (a, b) in enumerate(nodes):
        x = 24 + i * (bw + gap)
        s.box(x, 74, bw, 100, a, b.replace("\n", ""), color=OI["purple"], size=13.5,
              subsize=11, tint=0.13)
        if i < 3:
            s.line(x + bw, 124, x + bw + gap, 124, OI["verm"], 1.6)
    s.rect(24, 206, 972, 44, OI["verm"], tint=0.12, rx=6)
    s.text(510, 234, "结果：责任在链条上流动，最终可能无人实际承担", 13, "middle", 700, OI["verm"])
    fixes = [("记录决策依据", "每个采纳或不采纳模型建议的决定都留下理由"),
             ("明确问责主体", "合同与内部制度事先指定每类决策的责任人"),
             ("保留人的否决权", "模型的建议永远是输入，决定权不下放给系统")]
    for i, (a, b) in enumerate(fixes):
        y = 268 + i * 48
        s.box(24, y, 200, 38, a, None, color=OI["green"], size=12.5, tint=0.14)
        s.text(246, y + 25, b, 12, "start", 400, "#444")
    return s.save(os.path.join(SV, "responsibility_chain.svg"))


if __name__ == "__main__":
    print(fig_six_questions(), fig_responsibility())
    print(fig_neglected())
