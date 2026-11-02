import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_inventorship():
    W, H = 1020, 470
    s = SVG(W, H)
    s.text(W / 2, 28, "AI 参与的发明：三个相互独立的问题", 15.5, "middle", 700)
    rows = [("谁是发明人？", "多数法域要求发明人必须是自然人；AI 不能被列为发明人",
             "判例已较为明确：DABUS 系列案在美、英、欧均被驳回", OI["blue"]),
            ("发明能否获得专利？", "AI 参与不影响可专利性，关键看人类是否做出了实质性贡献",
             "USPTO 2024 年指引：需识别出对权利要求有实质贡献的自然人", OI["green"]),
            ("权利归谁所有？", "由雇佣关系与合同约定决定，与 AI 是否参与无关",
             "实践要点：平台方与药企的合作协议须事先约定归属", OI["orange"])]
    for i, (a, b, c, col) in enumerate(rows):
        y = 66 + i * 118
        s.box(24, y, 230, 98, a, None, color=col, size=14, tint=0.17)
        s.text(278, y + 34, b, 12.5, "start", 400)
        s.text(278, y + 68, c, 12, "start", 600, col)
    s.rect(24, 424, 972, 36, OI["crimson"], tint=0.10, rx=5)
    s.text(510, 447, "混淆这三个问题，是 AI 制药合作谈判中最常见的法律误区",
           12.5, "middle", 700, OI["crimson"])
    return s.save(os.path.join(SV, "inventorship.svg"))


def fig_patent_challenges():
    W, H = 1020, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "AI 生成分子给专利制度带来的三个新难题", 15.5, "middle", 700)
    rows = [("充分公开", "生成模型的输出难以用传统方式描述“如何得到”",
             "若说明书无法使本领域技术人员重现，可能被认定公开不充分", OI["crimson"]),
            ("创造性（非显而易见性）", "当 AI 能枚举一个化学空间，该空间内的分子是否仍属“非显而易见”",
             "尚无定论；若标准收紧，大量生成式专利的有效性将受影响", OI["orange"]),
            ("在先技术的范围", "AI 大规模枚举并公开的分子，是否构成对后续申请的在先技术",
             "“专利丛林”式的防御性公开可能挤压后来者的空间", OI["purple"])]
    for i, (a, b, c, col) in enumerate(rows):
        y = 66 + i * 110
        s.box(24, y, 240, 92, a, None, color=col, size=13.5, tint=0.17)
        s.text(288, y + 32, b, 12.5, "start", 400)
        s.text(288, y + 64, c, 12, "start", 600, col)
    s.text(24, 410, "三者的共同根源：专利制度的许多概念以“人类的创造行为”为隐含前提。",
           12.5, "start", 700, "#444")
    return s.save(os.path.join(SV, "patent_challenges.svg"))


def fig_biosecurity():
    W, H = 740, 500
    s = SVG(W, H)
    s.text(W / 2, 28, "生物安全的多层防护：没有单点能解决问题", 15.5, "middle", 700)
    layers = [("模型层", "能力限制、拒绝有害请求、对高风险用途的访问控制",
               "可被绕过；开源权重后失效", OI["blue"]),
              ("数据层", "限制高危毒素与病原体数据的获取与再分发",
               "多数相关数据本就公开，限制效果有限", OI["sky"]),
              ("合成层", "DNA 合成服务商筛查订单序列，云实验室做客户尽职调查",
               "覆盖率取决于服务商的自愿参与程度", OI["green"]),
              ("设备与试剂层", "关键设备与前体物质的流通管理",
               "管制清单的更新滞后于新出现的风险", OI["orange"]),
              ("法律与规范层", "两用性研究的审查、从业者规范、国际公约",
               "滞后于技术发展，但提供最终的问责依据", OI["purple"])]
    for i, (a, b, c, col) in enumerate(layers):
        y = 64 + i * 80
        s.box(24, y, 170, 66, a, None, color=col, size=13.5, tint=0.17)
        s.text(216, y + 28, b, 12, "start", 400)
        s.text(216, y + 52, "局限：" + c, 11.5, "start", 600, col)
    s.rect(24, 468, 692, 24, OI["green"], tint=0.12, rx=4)
    s.text(370, 485, "最有效的一层往往不是最受关注的一层：合成筛查比模型限制更难绕过",
           12, "middle", 700, OI["green"])
    return s.save(os.path.join(SV, "biosecurity_layers.svg"))


if __name__ == "__main__":
    print(fig_inventorship(), fig_patent_challenges(), fig_biosecurity())
