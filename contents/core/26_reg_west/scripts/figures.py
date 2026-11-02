import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_cou():
    W, H = 1000, 500
    s = SVG(W, H)
    s.text(W / 2, 28, "使用场景决定证据要求：同一个模型，不同的门槛", 15.5, "middle", 700)
    rows = [("内部排序与优先级", "决定先合成哪些分子、先测哪些化合物",
             "无监管要求，企业自行判断", OI["green"], "低"),
            ("支持性证据", "作为申报材料中的补充信息，不单独支撑结论",
             "需说明方法与局限，通常不需独立验证", OI["sky"], "中低"),
            ("替代部分实验", "用计算结果替代某项常规测定（如杂质致突变性评估）",
             "需符合既有指导原则并提供验证数据", OI["orange"], "中高"),
            ("支撑关键结论", "直接支持安全性或有效性的监管判定",
             "需完整的可信度评估：风险分级、验证、不确定性", OI["crimson"], "高")]
    for i, (a, b, c, col, lvl) in enumerate(rows):
        y = 62 + i * 100
        s.box(24, y, 210, 84, a, None, color=col, size=13.5, tint=0.17)
        s.text(258, y + 32, b, 12.5, "start", 400)
        s.text(258, y + 60, "证据要求：" + c, 12, "start", 600, col)
        s.box(876, y + 22, 100, 40, lvl, None, color=col, size=13, weight=700, tint=0.22)
    s.text(24, 484, "同一个模型可以同时用于四种场景，而每种场景的证据门槛完全不同。",
           12.5, "start", 700, "#444")
    return s.save(os.path.join(SV, "context_of_use.svg"))


def fig_credibility():
    W, H = 700, 430
    s = SVG(W, H)
    s.text(W / 2, 28, "FDA 可信度评估七步法：风险由使用场景决定", 15.5, "middle", 700)
    steps = [("1 定义关注的问题", "模型要回答的具体问题是什么"),
             ("2 界定使用场景（COU）", "模型输出在决策中的角色与范围，以及还有哪些证据并用"),
             ("3 评估模型风险", "由模型影响度与决策后果两个维度共同确定"),
             ("4 制定可信度评估计划", "风险越高，计划中要求的证据越强"),
             ("5 执行计划", "按计划完成验证与确认活动"),
             ("6 记录结果并沟通偏差", "与监管方讨论执行中与计划的任何偏离"),
             ("7 判定可信度是否充分", "结论是针对该使用场景的，换场景需重新评估")]
    for i, (a, b) in enumerate(steps):
        y = 64 + i * 48
        s.box(24, y, 250, 38, a, None, color=OI["blue"], size=12.5, tint=0.13)
        s.text(296, y + 25, b, 12, "start", 400, "#444")
    s.text(24, 422, "核心逻辑：证据的强度由风险决定，而风险由使用场景而非模型本身决定。",
           12.5, "start", 700, OI["crimson"])
    return s.save(os.path.join(SV, "credibility_steps.svg"))


def fig_regmap():
    W, H = 1060, 460
    s = SVG(W, H)
    s.text(W / 2, 28, "欧美与国际监管框架的分工", 15.5, "middle", 700)
    cols = [("FDA", OI["blue"],
             ["AI 在药物与生物制品监管决策中的\n应用指导（草案，2025）",
              "基于风险的可信度评估七步法",
              "模型辅助药物开发（MIDD）路径"]),
            ("EMA", OI["green"],
             ["AI 在药物生命周期中应用的\n反思文件（2024）",
              "数字孪生等方法的资格认定程序",
              "与 EU AI Act 的衔接"]),
            ("EU AI Act", OI["orange"],
             ["按风险分级的横向立法",
              "医疗相关多属高风险类别",
              "对透明度、数据治理、\n人类监督提出要求"]),
            ("ICH", OI["purple"],
             ["M7：杂质致突变性的\n计算毒理评估",
              "已被接受的“计算替代实验”先例",
              "后续指导原则正在讨论"])]
    bw, gap = 244, 20
    for i, (title, c, items) in enumerate(cols):
        x = 20 + i * (bw + gap)
        s.box(x, 66, bw, 44, title, None, color=c, size=14.5, tint=0.18)
        for j, t in enumerate(items):
            lines = t.split("\n")
            s.box(x + 6, 124 + j * 96, bw - 12, 84, lines[0],
                  lines[1] if len(lines) > 1 else None,
                  color=c, size=11.5, subsize=11, weight=400, tint=0.08)
    s.text(530, 440, "共同点：没有“AI 专用审评通道”，AI 被纳入既有的证据与质量体系来管理。",
           12.5, "middle", 700, "#444")
    return s.save(os.path.join(SV, "reg_map.svg"))


if __name__ == "__main__":
    print(fig_cou(), fig_credibility(), fig_regmap())
