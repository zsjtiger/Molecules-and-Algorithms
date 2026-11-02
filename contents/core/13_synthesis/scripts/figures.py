import sys, os, io
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart, box_edge
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_retro_tree():
    W, H = 1040, 460
    s = SVG(W, H)
    s.text(W / 2, 28, "逆合成分析：从目标分子倒推到可购买砌块", 15.5, "middle", 700)
    s.box(420, 62, 200, 56, "目标分子", "待合成的候选药物", color=OI["crimson"], size=14, subsize=11)
    mid = [("中间体 A", 170), ("中间体 B", 450), ("中间体 C", 730)]
    for t, x in mid:
        s.box(x, 190, 180, 50, t, None, color=OI["blue"], size=13, tint=0.12)
    s.line(500, 118, 260, 190, OI["black"], 1.5)
    s.line(520, 118, 540, 190, OI["black"], 1.5)
    s.line(540, 118, 800, 190, OI["black"], 1.5)
    s.text(350, 150, "断键 ①", 11.5, "middle", 600, "#555")
    s.text(560, 160, "断键 ②", 11.5, "middle", 600, "#555")
    s.text(720, 150, "断键 ③", 11.5, "middle", 600, "#555")
    leaves = [("砌块 1", 40), ("砌块 2", 240), ("砌块 3", 440), ("砌块 4", 640), ("砌块 5", 840)]
    for t, x in leaves:
        s.box(x, 320, 160, 48, t, None, color=OI["green"], size=12.5, tint=0.14)
    s.line(230, 240, 120, 320, OI["black"], 1.4)
    s.line(290, 240, 320, 320, OI["black"], 1.4)
    s.line(520, 240, 520, 320, OI["black"], 1.4)
    s.line(790, 240, 720, 320, OI["black"], 1.4)
    s.line(820, 240, 920, 320, OI["black"], 1.4)
    s.text(20, 400, "每一次断键对应一个已知反应的逆过程；叶子节点必须是可购买的起始原料。", 12, "start", 400, "#444")
    s.text(20, 426, "搜索空间随深度指数增长，因此需要神经网络策略 + 蒙特卡洛树搜索等方法剪枝。", 12, "start", 400, "#444")
    return s.save(os.path.join(SV, "retro_tree.svg"))


def fig_dmta():
    W, H = 940, 660
    s = SVG(W, H)
    s.text(W / 2, 28, "设计–合成–测试–学习（DMTA）闭环", 15.5, "middle", 700)
    cx, cy, r = 440, 330, 205
    import math
    nodes = [("设计 Design", "生成模型 + 多参数评分", OI["blue"], -90),
             ("合成 Make", "机器人自动化合成", OI["orange"], 0),
             ("测试 Test", "纯度、结构、活性、ADMET", OI["green"], 90),
             ("学习 Learn", "数据回流，更新模型", OI["purple"], 180)]
    pts = []
    for t, sub, c, ang in nodes:
        a = math.radians(ang)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        pts.append((x, y))
        s.box(x - 112, y - 42, 224, 84, t, sub, color=c, size=14, subsize=11.5, tint=0.14)
    # 顺时针连弧：两端都落在方框边界上，箭头抵住下游框，不悬在半空
    for i, j in [(0, 1), (1, 2), (2, 3), (3, 0)]:
        p0 = box_edge(pts[i][0], pts[i][1], 112, 42, nodes[i][3] + 90)
        p1 = box_edge(pts[j][0], pts[j][1], 112, 42, nodes[j][3] - 90)
        s.arc_arrow(p0, p1, 0.20, OI["black"], 1.8)
    s.circle(cx, cy, 78, OI["crimson"], tint=0.10, sw=1.2)
    s.text(cx, cy - 12, "闭环周期", 14, "middle", 700, OI["crimson"])
    s.text(cx, cy + 10, "人工：数周", 11.5, "middle", 400)
    s.text(cx, cy + 30, "自动化：数天", 11.5, "middle", 600, OI["crimson"])
    s.text(20, 634, "价值不在单个环节更快，而在循环更快、且每轮都产生标准化、含失败记录的数据。", 12, "start", 400, "#444")
    return s.save(os.path.join(SV, "dmta_loop.svg"))


def fig_negative_data():
    plt = mpl_setup()
    import numpy as np
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.2))
    labels = ["成功反应", "失败反应"]
    lit = [95, 5]
    auto = [20, 80]
    for ax, v, t, note in zip(axes, [lit, auto], ["公开文献 / 专利反应库", "自动化实验室记录"],
                              ["发表偏差：失败极少被记录", "系统记录全部结果"]):
        cols = [OI["sky"], OI["verm"]]
        b = ax.bar(labels, v, color=cols, width=0.55)
        for rect, val in zip(b, v):
            ax.text(rect.get_x() + rect.get_width() / 2, val + 2, f"约 {val}%", ha="center", fontsize=11)
        ax.set_ylim(0, 104); ax.set_title(t, loc="left", fontsize=12)
        ax.text(0.5, -0.30, note, transform=ax.transAxes, ha="center", fontsize=10.5, color="#555")
        ax.set_ylabel("占记录的比例" if ax is axes[0] else "")
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(False)
    fig.suptitle("阴性数据的来源差异：模型要学会“什么做不出来”，就必须有失败记录",
                 x=0.01, y=1.10, ha="left", fontsize=12.5)
    fig.subplots_adjust(bottom=0.26, top=0.82)
    return save_chart(fig, os.path.join(SV, "negative_data.svg"))


def fig_automation_levels():
    W, H = 1020, 400
    s = SVG(W, H)
    s.text(W / 2, 28, "实验室自动化的四个层级", 15.5, "middle", 700)
    levels = [("L1 辅助", "人工操作 + 电子记录本", "数据可追溯", OI["lgray"]),
              ("L2 自动化单元", "自动加样、平行合成、自动纯化", "单步通量提升", OI["sky"]),
              ("L3 流程自动化", "合成—纯化—分析串联，人工调度", "标准化数据", OI["blue"]),
              ("L4 自驱动闭环", "AI 决定下一批实验，机器人执行", "真正的 DMTA 闭环", OI["crimson"])]
    bw, gap = 232, 18
    for i, (a, b, c, col) in enumerate(levels):
        x = 20 + i * (bw + gap)
        s.box(x, 70, bw, 110, a, b, color=col, size=14.5, subsize=11.5, tint=0.16)
        s.box(x + 20, 200, bw - 40, 44, c, None, color=col, size=12, weight=600, tint=0.08)
        if i < 3:
            s.line(x + bw, 125, x + bw + gap, 125, OI["black"], 1.5)
    s.text(20, 296, "2026 年的产业现实：多数企业处于 L2–L3；完全无人干预的 L4 闭环仍然罕见，", 12, "start", 400, "#444")
    s.text(20, 322, "瓶颈往往不在合成，而在分析与生物活性测试的自动化程度。", 12, "start", 400, "#444")
    s.text(20, 358, "晶泰科技公开称其实验室有 300 余台机器人、50 万条实验记录，其中约 80% 为阴性样本。", 11.5, "start", 400, "#666")
    return s.save(os.path.join(SV, "automation_levels.svg"))


if __name__ == "__main__":
    print(fig_retro_tree(), fig_dmta())
    print(fig_negative_data())
    print(fig_automation_levels())
