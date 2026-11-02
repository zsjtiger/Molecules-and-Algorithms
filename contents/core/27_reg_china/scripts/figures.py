import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_two_tracks():
    W, H = 1040, 440
    s = SVG(W, H)
    s.text(W / 2, 28, "两条不同的轨道：AI 用于监管，与 AI 用于申报", 15.5, "middle", 700)
    s.box(24, 66, 490, 50, "轨道一：AI 用于监管工作本身", None, color=OI["blue"], size=14, tint=0.18)
    s.box(526, 66, 490, 50, "轨道二：AI 用于申报材料与研发", None, color=OI["green"], size=14, tint=0.18)
    left = [("《关于「人工智能+药品监管」的实施意见》", "2026 年 4 月发布，国药监综〔2026〕6 号"),
            ("七类应用场景", "人机协同审评、全链条智慧监管、风险监测、\n检查执法、协同监管、政务服务、产业数字化协同"),
            ("两个时间节点", "2030 年初步建成体系，2035 年智慧治理"),
            ("定位", "AI 辅助人的决策，不替代人的决策")]
    right = [("尚无 AI 专项技术指导原则", "目前按既有的证据与质量体系管理"),
             ("模型引导的研发已有先例", "《模型引导的罕见疾病药物研发技术指导原则》（2025）"),
             ("与国际接轨", "ICH 成员国，M7 等指导原则同样适用"),
             ("实际门槛", "与欧美一致：由使用场景而非技术决定")]
    for i, (a, b) in enumerate(left):
        y = 132 + i * 74
        lines = b.split("\n")
        s.text(30, y + 18, a, 12.5, "start", 700, OI["blue"])
        for j, ln in enumerate(lines):
            s.text(30, y + 40 + j * 20, ln, 11.5, "start", 400, "#444")
    for i, (a, b) in enumerate(right):
        y = 132 + i * 74
        s.text(532, y + 18, a, 12.5, "start", 700, OI["green"])
        s.text(532, y + 40, b, 11.5, "start", 400, "#444")
    s.line(518, 66, 518, 424, OI["lgray"], 1.2, head=None)
    return s.save(os.path.join(SV, "china_two_tracks.svg"))


def fig_hgr():
    W, H = 880, 500
    s = SVG(W, H)
    s.text(W / 2, 28, "人类遗传资源：什么情形需要许可，什么情形只需备案", 15.5, "middle", 700)
    rows = [("采集（特定种类或数量）", "行政许可", "已属国际合作许可范围的，并入该申请", OI["crimson"]),
            ("保藏", "行政许可", "独立事项，需单独申请", OI["crimson"]),
            ("国际科研合作", "行政许可", "外方单位实质性参与即触发", OI["crimson"]),
            ("材料出境", "行政许可", "指实物样本的出境", OI["crimson"]),
            ("国际合作临床试验", "备案", "为药品上市注册目的开展的，走备案而非许可", OI["orange"]),
            ("信息对外提供或开放使用", "事先报告 + 备份", "已公开的信息不在此列", OI["purple"])]
    for i, (a, b, c, col) in enumerate(rows):
        y = 62 + i * 68
        s.box(24, y, 290, 56, a, None, color=col, size=12.5, tint=0.14)
        s.box(336, y + 8, 126, 40, b, None, color=col, size=12.5, weight=700, tint=0.22)
        s.text(488, y + 34, c, 12, "start", 400, "#444")
    s.text(24, 486, "判断起点是“外方单位是否实质性参与”，而非合作协议怎么写。",
           12.5, "start", 700, OI["crimson"])
    return s.save(os.path.join(SV, "hgr_matrix.svg"))


def fig_compliance_stack():
    W, H = 1000, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "中国数据合规的四层叠加：药企要同时满足", 15.5, "middle", 700)
    layers = [("《生物安全法》", "上位法，确立生物安全与遗传资源的基本制度", OI["crimson"]),
              ("《人类遗传资源管理条例》及实施细则", "采集、保藏、国际合作、出境与信息对外提供的具体规则", OI["orange"]),
              ("《数据安全法》与数据出境规则", "重要数据的识别、出境安全评估与标准合同", OI["blue"]),
              ("《个人信息保护法》", "患者个人信息的告知同意、最小必要与单独同意", OI["green"])]
    for i, (a, b, c) in enumerate(layers):
        y = 70 + i * 82
        s.box(24, y, 400, 66, a, None, color=c, size=13.5, tint=0.16)
        s.text(448, y + 40, b, 12, "start", 400, "#444")
    s.text(24, 410, "四层相互独立：满足其中一层不构成对其他层的豁免。", 12.5, "start", 700, "#444")
    return s.save(os.path.join(SV, "compliance_stack.svg"))


if __name__ == "__main__":
    print(fig_two_tracks(), fig_hgr(), fig_compliance_stack())
