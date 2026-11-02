import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")

def fig_ecosystem():
    W, H = 1060, 560
    s = SVG(W, H)
    s.text(W / 2, 28, "中国 AI 制药生态的分层结构（2026）", 15.5, "middle", 700)
    layers = [
        ("政策与监管", "国务院“人工智能+”行动；国家药监局“人工智能+药品监管”实施意见；数据与遗传资源合规", OI["gray"]),
        ("资本", "2026 前三季度 57 笔融资、近 158 亿元；红杉、高瓴等集中押注头部；港股 18C 通道", OI["purple"]),
        ("大厂与 AI for Science 平台", "字节（Anew Labs）· 百度系（百图生科）· 腾讯 · 华为 · 深势科技", OI["blue"]),
        ("AI 原生药物研发公司", "英矽智能 · 晶泰科技 · 剂泰科技 · 德睿智药 · 深度智耀 · 元思生肽 等", OI["crimson"]),
        ("创新药企与 Biotech", "东阳光药 · 翰思艾泰 等通过合作、合资引入 AI 能力", OI["orange"]),
        ("CXO 与自动化实验室", "合成与筛选产能；“计算设计—实验验证—数据反馈”闭环（如赛默飞 × 金斯瑞）", OI["green"]),
        ("医院、临床与数据", "临床试验招募快、成本低；真实世界数据规模大但分散", OI["sky"]),
    ]
    y0, h, gap = 56, 58, 8
    for i, (name, desc, c) in enumerate(layers):
        y = y0 + i * (h + gap)
        s.rect(30, y, 1000, h, c, tint=0.10, rx=6)
        s.L.append(f'  <rect x="30" y="{y}" width="200" height="{h}" rx="6" fill="{c}" fill-opacity="0.85"/>')
        s.text(130, y + h / 2 + 5, name, 13.5, "middle", 700, "#ffffff")
        s.text(248, y + h / 2 + 5, desc, 12.5, "start", 400)
    # outflow arrow
    s.text(30, H - 20, "出海通道：对外授权（license-out）、合资、海外临床；2026 年上半年中国创新药 BD 交易总额约 997 亿美元。", 11.5, "start", 400, "#444")
    return s.save(os.path.join(SV, "china_ecosystem.svg"))

def fig_swot():
    W, H = 1040, 470
    s = SVG(W, H)
    s.text(W / 2, 28, "中国 AI 制药：结构性优势与约束", 15.5, "middle", 700)
    adv = [("临床速度与成本", "患者招募快，单患者成本低"), ("化学合成与工程产能", "CXO 体系成熟，DMTA 闭环可快速搭建"),
           ("工程与算法人才", "大厂 AI 团队转入 AI4S"), ("出海交易通道", "跨国药企大规模采购中国资产"),
           ("政策方向明确", "“人工智能+”与药监数智化")]
    con = [("原始创新与新靶点", "First-in-class 比例仍低"), ("数据合规", "人类遗传资源、个人信息、数据出境"),
           ("高端算力", "先进 GPU 出口管制"), ("资本集中与估值", "资金向头部集中，长尾融资难"),
           ("地缘政治", "海外对中国生物技术企业的立法与审查动向")]
    s.text(270, 66, "结构性优势", 14, "middle", 700, OI["green"])
    s.text(770, 66, "结构性约束", 14, "middle", 700, OI["verm"])
    for i, (a, b) in enumerate(adv):
        s.box(30, 82 + i * 70, 480, 58, a, b, color=OI["green"], size=13.5, subsize=11.5, tint=0.10)
    for i, (a, b) in enumerate(con):
        s.box(530, 82 + i * 70, 480, 58, a, b, color=OI["verm"], size=13.5, subsize=11.5, tint=0.10)
    return s.save(os.path.join(SV, "china_swot.svg"))

if __name__ == "__main__":
    print(fig_ecosystem(), fig_swot())
