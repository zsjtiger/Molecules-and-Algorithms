import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_architecture():
    W, H = 1060, 620
    s = SVG(W, H)
    s.text(W / 2, 28, "企业级 AI 药物研发平台的参考架构", 15.5, "middle", 700)
    tiers = [
        ("交付层", OI["crimson"], ["项目工作台", "候选分子看板", "决策记录与审计"]),
        ("服务层", OI["orange"], ["预测服务 API", "流程编排引擎", "主动学习调度"]),
        ("模型层", OI["green"], ["模型注册表", "训练与再训练管道", "适用域与不确定性"]),
        ("数据层", OI["blue"], ["实体解析与主数据", "实验结果入库", "版本化数据集"]),
        ("基础设施层", OI["purple"], ["计算调度（CPU/GPU）", "对象存储", "环境与镜像管理"]),
    ]
    for i, (name, c, items) in enumerate(tiers):
        y = 64 + i * 96
        s.box(24, y, 186, 80, name, None, color=c, size=14, tint=0.18)
        for j, t in enumerate(items):
            s.box(234 + j * 262, y + 8, 246, 64, t, None, color=c, size=12.5,
                  weight=400, tint=0.09)
    s.rect(24, 552, 1012, 46, OI["crimson"], tint=0.10, rx=6)
    s.text(530, 580, "横向贯穿：标识符治理、权限与审计、可复现性记录——这三项做不好，上面各层都不可信",
           12.5, "middle", 700, OI["crimson"])
    s.text(24, 614, "决定平台成败的通常不是模型层，而是数据层的实体解析与服务层的编排可靠性。",
           12, "start", 600, "#444")
    return s.save(os.path.join(SV, "platform_arch.svg"))


def fig_build_buy():
    W, H = 1048, 450
    s = SVG(W, H)
    s.text(W / 2, 28, "自建、采购还是混合：按组件而非按平台决策", 15.5, "middle", 700)
    cols = [("优先采购 / 用开源", OI["green"],
             ["通用深度学习框架", "标准化领域库（RDKit 等）", "公开模型权重",
              "计算调度与存储"]),
            ("优先自建", OI["crimson"],
             ["实体解析与主数据治理", "实验结果入库管道", "与本企业实验流程的对接",
              "决策记录与审计"]),
            ("视情况而定", OI["orange"],
             ["预测服务与 API 层", "流程编排引擎", "可视化工作台",
              "模型注册与监控"])]
    bw, gap = 320, 24
    for i, (title, c, items) in enumerate(cols):
        x = 20 + i * (bw + gap)
        s.box(x, 66, bw, 46, title, None, color=c, size=13.5, tint=0.18)
        for j, t in enumerate(items):
            s.box(x + 8, 126 + j * 62, bw - 16, 52, t, None, color=c, size=12,
                  weight=400, tint=0.08)
    s.rect(20, 382, 1000, 44, OI["purple"], tint=0.10, rx=6)
    s.text(520, 410, "判据：这个组件体现了本企业的独特性吗？不独特的部分买或用开源，独特的部分自建",
           12.5, "middle", 700, OI["purple"])
    return s.save(os.path.join(SV, "build_buy.svg"))


def fig_failure_reasons():
    plt = mpl_setup()
    import numpy as np
    reasons = ["标识符与主数据未治理", "实验与建模团队脱节", "没有明确的使用场景",
               "模型未接入日常决策流程", "可复现性缺失", "算力或模型性能不足"]
    weight = [4.6, 4.4, 4.2, 4.0, 3.2, 1.4]
    cols = [OI["verm"]] * 5 + [OI["blue"]]
    y = np.arange(len(reasons))[::-1]
    fig, ax = plt.subplots(figsize=(7.8, 3.6))
    ax.barh(y, weight, 0.56, color=cols)
    ax.set_yticks(y); ax.set_yticklabels(reasons)
    ax.set_xticks([1, 2, 3, 4, 5]); ax.set_xticklabels(["很少", "偶尔", "常见", "很常见", "最常见"])
    ax.set_xlim(0, 5.3)
    ax.set_title("平台建设失败的原因：几乎都不是技术问题", loc="left")
    ax.text(0.0, -0.28, "依据公开报道与行业访谈的定性归纳，非统计调查结果。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.24, left=0.30)
    return save_chart(fig, os.path.join(SV, "platform_failures.svg"))


if __name__ == "__main__":
    print(fig_architecture(), fig_build_buy())
    print(fig_failure_reasons())
