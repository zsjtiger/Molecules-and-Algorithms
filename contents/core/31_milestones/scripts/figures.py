import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_milestones():
    W, H = 980, 606
    s = SVG(W, H)
    s.text(W / 2, 28, "十二项可核对的里程碑：按可观测的时间排序", 15.5, "middle", 700)
    rows = [("2027", "FDA 可信度评估指导文件定稿", "是否由草案转为正式稿", OI["blue"]),
            ("2027", "一个主流评测基准按时间划分重做并公开", "是否有产业界主导的新基准发布", OI["blue"]),
            ("2028", "统一的结构–亲和力模型进入商业流程", "主要平台是否以单模型替代拼接", OI["green"]),
            ("2028", "AI 来源候选药物累计进入 III 期超过 20 个", "登记库中可统计", OI["green"]),
            ("2029", "首例 AI 输出支撑关键监管结论获接受", "审评报告中是否出现", OI["orange"]),
            ("2029", "头部企业公开报告飞轮周期缩短的量化数据", "是否出现带基线的周期数据", OI["orange"]),
            ("2030", "AI 来源药物 II 期通过率可与历史基线比较", "样本量是否足以做统计检验", OI["crimson"]),
            ("2030", "抗体从头设计产物进入临床", "是否有完全从头设计的抗体 IND", OI["crimson"]),
            ("2031", "多个 AI 来源药物获批上市", "获批数量与适应症分布", OI["purple"]),
            ("2032", "阴性结果数据库形成行业惯例", "是否有跨企业的阴性数据共享机制", OI["purple"]),
            ("2033", "被忽视疾病领域出现 AI 驱动的候选药物", "管线中是否出现相关项目", OI["sky"]),
            ("2035", "AI 对临床成功率的影响可被统计确认", "是否有同行评议的队列比较研究", OI["sky"])]
    s.text(112, 48, "里程碑", 11.5, "start", 700, "#888")
    s.text(548, 48, "核对方式", 11.5, "start", 700, "#888")
    for i, (yr, a, b, col) in enumerate(rows):
        y = 64 + i * 44
        s.box(24, y, 70, 34, yr, None, color=col, size=12.5, weight=700, tint=0.20)
        s.text(112, y + 23, a, 12.5, "start", 600)
        s.text(548, y + 23, b, 11.5, "start", 400, "#555")
    s.text(24, 598, "每一项都写成可以回答“是或否”的形式——这是与宏大叙事的区别所在。",
           12.5, "start", 700, OI["crimson"])
    return s.save(os.path.join(SV, "milestones.svg"))


def fig_falsify():
    W, H = 920, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "本书的核心判断及其否证条件", 15.5, "middle", 700)
    rows = [("前端提效是真实的", "若到 2029 年仍无企业能给出带基线的周期缩短数据，此判断应被怀疑",
             OI["green"]),
            ("后端瓶颈不随算力放松", "若某个疾病领域在 2030 年前出现成功率的数量级跃升，此判断需修正",
             OI["orange"]),
            ("评测缺口是核心障碍", "若按时间划分的产业基准建立后，方法间差距仍如现在的报告所示，此判断不成立",
             OI["blue"]),
            ("数据的方向性偏差难以消除", "若出现能在长尾靶点上稳定有效的方法，此判断应被修正",
             OI["purple"])]
    for i, (a, b, col) in enumerate(rows):
        y = 66 + i * 82
        s.box(24, y, 270, 66, a, None, color=col, size=13.5, tint=0.17)
        s.text(318, y + 40, b, 12, "start", 400, "#444")
    s.text(24, 406, "一个不能被否证的判断不是判断，是立场。", 12.5, "start", 700, OI["crimson"])
    return s.save(os.path.join(SV, "falsification.svg"))


if __name__ == "__main__":
    print(fig_milestones(), fig_falsify())
