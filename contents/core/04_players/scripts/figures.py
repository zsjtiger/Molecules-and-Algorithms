import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")

def fig_map():
    W, H = 900, 600
    s = SVG(W, H)
    s.text(W / 2, 28, "五条路线的定位：数据来自哪里，AI 覆盖多宽", 15.5, "middle", 700)
    L, R, T, B = 110, 860, 70, 520
    s.line(L, B, R, B, OI["black"], 1.3); s.line(L, B, L, T, OI["black"], 1.3)
    s.text((L + R) / 2, B + 40, "核心数据来源：公开数据为主  →  专有实验数据为主", 13, "middle", 600)
    s.L.append(f'  <text x="{L-60}" y="{(T+B)/2}" font-size="13" font-weight="600" text-anchor="middle" transform="rotate(-90 {L-60} {(T+B)/2})">AI 覆盖的研发环节：单一环节  →  全流程</text>')
    # quadrant guides
    s.line((L + R) / 2, T, (L + R) / 2, B, OI["lgray"], 1, dash="4,4", head=None)
    s.line(L, (T + B) / 2, R, (T + B) / 2, OI["lgray"], 1, dash="4,4", head=None)
    # ref=True 的两项不属于本章的"五条路线"，画成空心点以示区别
    pts = [("英矽智能", "端到端", 0.45, 0.90, OI["crimson"], False),
           ("Recursion", "表型驱动", 0.86, 0.74, OI["green"], False),
           ("Isomorphic Labs", "结构优先", 0.38, 0.38, OI["blue"], False),
           ("晶泰科技", "AI + 机器人", 0.88, 0.52, OI["orange"], False),
           ("Chai / Xaira", "生物药设计", 0.52, 0.14, OI["purple"], False),
           ("薛定谔", "物理计算（参照）", 0.16, 0.22, OI["gray"], True),
           ("大药企自建", "礼来、诺华等（参照）", 0.70, 0.64, OI["black"], True)]
    for name, route, x, y, c, ref in pts:
        px = L + x * (R - L); py = B - y * (B - T)
        s.circle(px, py, 9, c, fill=("#ffffff" if ref else None), tint=0.85, sw=2.0)
        anchor = "end" if x > 0.8 else "start"
        dx = -16 if anchor == "end" else 16
        s.text(px + dx, py - 2, name, 13, anchor, 700)
        s.text(px + dx, py + 15, route, 11.5, anchor, 400, "#555")
    s.circle(L + 14, T + 10, 7, OI["gray"], fill="#ffffff", sw=2.0)
    s.text(L + 28, T + 14, "空心点为参照项，不属于本章的五条路线", 11, "start", 400, "#666")
    s.text(R - 4, H - 14, "注：位置为作者基于公开信息的定性判断，非测量值", 10.5, "end", 400, "#666")
    return s.save(os.path.join(SV, "players_map.svg"))

def fig_triangle():
    W, H = 860, 600
    s = SVG(W, H)
    s.text(W / 2, 28, "三种商业模式的权衡", 15.5, "middle", 700)
    A = (430, 140); Bp = (110, 470); C = (750, 470)
    s.poly([A, Bp, C], OI["gray"], tint=0.05, sw=1.3)
    def corner(p, title, sub, anchor, dy):
        s.text(p[0], p[1] + dy, title, 14, anchor, 700)
        s.text(p[0], p[1] + dy + 20, sub, 11.5, anchor, 400, "#444")
    corner(A, "自研管线", "上限最高 · 资本需求最大 · 承担全部临床风险", "middle", -48)
    corner(Bp, "技术服务（CRO 式）", "现金流稳 · 天花板低 · 易被药企自建替代", "start", 34)
    corner(C, "平台合作（里程碑 + 分成）", "分享成功收益 · 价值依赖合作方决策", "end", 34)
    # 重心坐标 (自研, 技术服务, 平台合作)，三者之和为 1
    co = [("英矽智能", 0.55, 0.30, 0.15, OI["crimson"]), ("Recursion", 0.58, 0.08, 0.34, OI["green"]),
          ("晶泰科技", 0.20, 0.45, 0.35, OI["orange"]), ("Isomorphic", 0.33, 0.05, 0.62, OI["blue"]),
          ("薛定谔", 0.25, 0.55, 0.20, OI["gray"]), ("Chai", 0.15, 0.20, 0.65, OI["purple"])]
    for name, a, b, c, col in co:
        x = a * A[0] + b * Bp[0] + c * C[0]; y = a * A[1] + b * Bp[1] + c * C[1]
        s.circle(x, y, 8, col, tint=0.85)
        # 统一放在点的右侧；靠近右边界的点改放左侧，避免标签出界
        if x > 0.66 * W:
            s.text(x - 13, y + 4, name, 12.5, "end", 600)
        else:
            s.text(x + 13, y + 4, name, 12.5, "start", 600)
    s.text(W - 20, H - 14, "注：点的位置表示收入结构的大致侧重，为作者定性判断", 10.5, "end", 400, "#666")
    return s.save(os.path.join(SV, "business_triangle.svg"))

def fig_moat():
    W, H = 980, 430
    s = SVG(W, H)
    s.text(W / 2, 28, "护城河在迁移：基础模型能力商品化之后，差异化落在哪里", 15.5, "middle", 700)
    # left column: commoditizing
    s.text(230, 70, "正在商品化（开源可得）", 13.5, "middle", 700, OI["gray"])
    left = ["结构预测（Boltz、Chai-1、OpenFold3）", "初步亲和力预测（Boltz-2）", "蛋白设计（RFdiffusion、ProteinMPNN）",
            "分子性质预测（Chemprop 等）", "通用大语言模型与智能体框架"]
    for i, t in enumerate(left):
        s.box(40, 88 + i * 58, 380, 44, t, None, color=OI["gray"], size=12.5, weight=400, tint=0.08)
    # right column: differentiation
    s.text(750, 70, "差异化来源（难以复制）", 13.5, "middle", 700, OI["crimson"])
    right = [("专有数据", "自动化实验、表型成像、含阴性样本"), ("闭环速度", "设计–合成–测试–学习一轮几天还是几周"),
             ("临床资产", "被人体数据验证过的分子"), ("领域深度", "特定疾病或模态的长期积累"),
             ("合作网络与渠道", "大药企选择权、数据合作")]
    for i, (a, b) in enumerate(right):
        s.box(560, 88 + i * 58, 380, 44, a + "：" + b, None, color=OI["crimson"], size=12.5, weight=400, tint=0.10)
    # arrow
    s.line(430, 230, 548, 230, OI["black"], 2)
    s.text(489, 220, "竞争焦点转移", 12, "middle", 600)
    s.text(W - 20, H - 14, "注：左右两栏并非一一对应", 10.5, "end", 400, "#666")
    return s.save(os.path.join(SV, "moat_shift.svg"))

if __name__ == "__main__":
    print(fig_map(), fig_triangle(), fig_moat())
