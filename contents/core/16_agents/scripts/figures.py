import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_agent_arch():
    W, H = 1060, 470
    s = SVG(W, H)
    s.text(W / 2, 28, "科研智能体的典型架构", 15.5, "middle", 700)
    s.poly([(40, 72), (300, 72), (278, 128), (18, 128)], OI["gray"], tint=0.10)
    s.text(158, 106, "研究者的任务描述", 13.5, "middle", 600)
    s.poly([(410, 150), (560, 110), (710, 150), (560, 190)], OI["crimson"], tint=0.16)
    s.text(560, 155, "规划器（LLM）", 13.5, "middle", 700)
    s.line(158, 128, 460, 148, OI["black"], 1.5)
    s.box(790, 72, 250, 110, "记忆与中间结果", "工作笔记、已验证事实、失败尝试", color=OI["sky"], size=13.5, subsize=11, tint=0.12)
    s.line(710, 150, 790, 130, OI["black"], 1.5, tail=True)
    # single trunk down to a horizontal bus, then short stubs into each tool
    s.line(560, 190, 560, 236, OI["black"], 1.6, head=None)
    s.line(72, 236, 1048, 236, OI["black"], 1.4, head=None)
    tools = [("文献与专利检索", OI["blue"]), ("数据库查询", OI["blue"]),
             ("计算化学工具", OI["green"]), ("结构预测与对接", OI["green"]),
             ("统计与因果分析", OI["purple"]), ("自动化实验设备", OI["orange"])]
    bw, gap = 150, 12
    for i, (t, c) in enumerate(tools):
        x = 20 + i * (bw + gap)
        cx = x + bw / 2
        s.line(cx, 236, cx, 272, OI["black"], 1.3)
        s.box(x, 274, bw, 70, t, None, color=c, size=12, weight=400, tint=0.13)
    s.text(530, 376, "工具的返回值是事实来源；LLM 只负责决定调用什么、如何串联", 12, "middle", 400, "#444")
    s.rect(60, 398, 980, 46, OI["crimson"], tint=0.10, rx=6)
    s.text(550, 426, "人类审核关卡：任何进入决策或实验的结论都必须可追溯到原始证据", 13, "middle", 700, OI["crimson"])
    return s.save(os.path.join(SV, "agent_architecture.svg"))


def fig_task_suitability():
    plt = mpl_setup()
    tasks = ["文献综述与证据提取", "代码与数据分析脚本", "实验方案起草", "工具调用与流程编排",
             "知识图谱抽取", "假设生成", "数值预测（活性、ADMET）", "因果判断"]
    fit = [4.4, 4.2, 3.6, 3.8, 3.4, 2.6, 1.5, 1.3]
    risk = [2.2, 1.8, 2.6, 2.4, 2.8, 3.6, 4.4, 4.6]
    import numpy as np
    y = np.arange(len(tasks))[::-1]
    fig, ax = plt.subplots(figsize=(7.8, 3.8))
    w = 0.36
    ax.barh(y + w / 2, fit, w, color=OI["green"], label="适合程度")
    ax.barh(y - w / 2, risk, w, color=OI["verm"], label="误用风险")
    ax.set_yticks(y); ax.set_yticklabels(tasks)
    ax.set_xticks([1, 2, 3, 4, 5]); ax.set_xticklabels(["很低", "低", "中", "高", "很高"])
    ax.set_xlim(0, 5.4)
    ax.set_title("大语言模型在药物研发中的任务适配：越靠近数值与因果，风险越高",
                 loc="left", pad=22)
    ax.legend(frameon=False, loc="lower right", fontsize=10, ncol=2,
              bbox_to_anchor=(1.0, 1.01))
    ax.text(0.0, -0.30, "评级为作者基于公开报道与实践的定性判断。",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s_ in ("top", "right"):
        ax.spines[s_].set_visible(False)
    fig.subplots_adjust(bottom=0.26, left=0.26)
    return save_chart(fig, os.path.join(SV, "task_suitability.svg"))


def fig_hallucination():
    W, H = 820, 400
    s = SVG(W, H)
    s.text(W / 2, 28, "科研智能体的四类失效模式与对应防护", 15.5, "middle", 700)
    rows = [("幻觉引用", "编造不存在的文献、专利或实验结果", "强制检索增强：每条结论附可点击的原始链接", OI["verm"]),
            ("偏向主流", "复述文献中说得最多的观点，强化已知偏差", "显式要求列出反面证据与争议", OI["orange"]),
            ("工具误用", "调用了正确的工具但参数或解读错误", "工具输出做单位、量纲与范围的自动校验", OI["blue"]),
            ("级联错误", "多步推理中早期错误被后续步骤放大", "每步设置可验证的中间检查点", OI["purple"])]
    for i, (a, b, c, col) in enumerate(rows):
        y = 62 + i * 80
        s.box(24, y, 180, 62, a, None, color=col, size=13.5, tint=0.18)
        s.text(224, y + 26, b, 12.5, "start", 400)
        s.text(224, y + 48, "防护：" + c, 12, "start", 600, col)
    s.text(24, 388, "共同原则：智能体的输出是“待核查的线索”，不是“已验证的结论”。", 12.5, "start", 600, "#444")
    return s.save(os.path.join(SV, "failure_modes.svg"))


if __name__ == "__main__":
    print(fig_agent_arch(), fig_hallucination())
    print(fig_task_suitability())
