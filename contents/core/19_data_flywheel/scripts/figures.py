import sys, os, math
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart, box_edge
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_flywheel():
    W, H = 1000, 520
    s = SVG(W, H)
    s.text(W / 2, 28, "数据飞轮：四个环节，三处最容易断", 15.5, "middle", 700)
    cx, cy, r = 340, 280, 150
    nodes = [("模型预测", -90, OI["blue"]), ("实验验证", 0, OI["green"]),
             ("数据入库", 90, OI["sky"]), ("模型更新", 180, OI["purple"])]
    pos = {}
    for name, ang, c in nodes:
        a = math.radians(ang)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        pos[name] = (x, y)
        s.box(x - 86, y - 28, 172, 56, name, None, color=c, size=14, tint=0.17)
    # 顺时针连弧：起点取上游框的切向出口，终点取下游框的切向入口，
    # 两端都落在框的边界上，箭头头部正好抵住方框，不留悬空。
    for i in range(4):
        a0, a1 = nodes[i][1], nodes[(i + 1) % 4][1]
        p0 = box_edge(*pos[nodes[i][0]], 86, 28, a0 + 90)
        p1 = box_edge(*pos[nodes[(i + 1) % 4][0]], 86, 28, a1 - 90)
        s.arc_arrow(p0, p1, 0.22, OI["black"], 1.6)
        # 前三段弧上各标一个断点编号，与右侧说明一一对应
        if i < 3:
            am = math.radians(a0 + 45)
            mx, my = cx + (r + 46) * math.cos(am), cy + (r + 46) * math.sin(am)
            s.circle(mx, my, 13, OI["verm"], fill="#ffffff", sw=1.6)
            s.text(mx, my + 4.5, "①②③"[i], 12, "middle", 700, OI["verm"])
    s.text(cx, cy - 8, "一次迭代", 13.5, "middle", 700, "#444")
    s.text(cx, cy + 14, "周数到月数", 11.5, "middle", 400, "#666")
    breaks = [("① 验证通量不足", "模型每周能排出上千个候选，实验每周只能测几十个。",
               "飞轮的转速由最慢的那一环决定。"),
              ("② 阴性结果未入库", "验证失败的分子常常不被记录，而它们恰是模型最缺的信息；",
               "数据只进不出，偏差只增不减。"),
              ("③ 模型不真正更新", "许多流程里模型只在项目启动时训练一次，",
               "新数据堆在库里，从未回到训练集。")]
    for i, (a, b1, b2) in enumerate(breaks):
        y = 72 + i * 142
        s.rect(600, y, 384, 112, OI["verm"], tint=0.08, rx=8)
        s.rect(600, y, 384, 34, OI["verm"], tint=0.20, rx=8)
        s.text(618, y + 23, a, 13, "start", 700, OI["verm"])
        s.text(618, y + 62, b1, 11.5, "start", 400, "#444")
        s.text(618, y + 86, b2, 11.5, "start", 400, "#444")
    return s.save(os.path.join(SV, "data_flywheel.svg"))


def fig_cycle_time():
    plt = mpl_setup()
    import numpy as np
    cycles = np.arange(0, 9)
    fast = 1.0 - 0.72 * np.exp(-0.42 * cycles)
    slow = 1.0 - 0.72 * np.exp(-0.42 * cycles * 0.28)
    fig, ax = plt.subplots(figsize=(8.4, 3.8))
    ax.plot(cycles, fast, "-o", color=OI["green"], lw=2.2, ms=6, label="两周一轮（高通量验证）")
    ax.plot(cycles, slow, "-o", color=OI["orange"], lw=2.2, ms=6, label="半年一轮（外包验证）")
    ax.set_xlabel("迭代轮次"); ax.set_ylabel("模型在本项目上的相对能力")
    ax.set_ylim(0.2, 1.05)
    ax.set_yticks([0.3, 0.5, 0.7, 0.9]); ax.set_yticklabels(["低", "中", "较高", "高"])
    ax.legend(frameon=False, fontsize=10.5, loc="lower right", ncol=1, handletextpad=0.5)
    ax.set_title("决定飞轮价值的是迭代周期，不是单轮数据量", loc="left", pad=12)
    ax.text(0.0, -0.28, "示意曲线，用于说明周期长短对累计效果的影响，非实测数据。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.26, left=0.14)
    return save_chart(fig, os.path.join(SV, "cycle_time.svg"))


def fig_federated():
    W, H = 1040, 470
    s = SVG(W, H)
    s.text(W / 2, 28, "联邦学习：模型动，数据不动", 15.5, "middle", 700)
    for i, nm in enumerate(["药企 A", "药企 B", "药企 C"]):
        x = 60 + i * 320
        s.box(x, 70, 260, 88, nm, "本地数据不出防火墙", color=OI["blue"], size=14, subsize=11, tint=0.13)
        s.line(x + 130, 158, x + 130, 206, OI["black"], 1.4)
        s.text(x + 140, 186, "只上传模型更新", 11, "start", 400, "#555")
    s.rect(60, 212, 920, 56, OI["purple"], tint=0.14, rx=6)
    s.text(520, 236, "聚合服务器：合并各方的模型更新，不接触任何原始数据", 13.5, "middle", 700, OI["purple"])
    s.text(520, 256, "回传合并后的全局模型", 11.5, "middle", 400, "#555")
    rows = [("解决了什么", "在数据不能出域的前提下，让多方共同训练出比各自单独训练更好的模型", OI["green"]),
            ("没解决什么", "参与方的数据口径、测定方法与化学空间差异仍然存在，合并不会自动对齐", OI["orange"]),
            ("真正的障碍", "通常不是技术，而是激励：数据多的一方从共享中获益最少", OI["verm"])]
    for i, (a, b, c) in enumerate(rows):
        y = 300 + i * 54
        s.box(60, y, 180, 44, a, None, color=c, size=12.5, tint=0.16)
        s.text(262, y + 28, b, 12, "start", 400, "#444")
    return s.save(os.path.join(SV, "federated.svg"))


if __name__ == "__main__":
    print(fig_flywheel(), fig_federated())
    print(fig_cycle_time())
