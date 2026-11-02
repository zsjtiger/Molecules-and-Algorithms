import sys, os
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")


def fig_leakage():
    W, H = 700, 470
    s = SVG(W, H)
    s.text(W / 2, 28, "数据泄漏的五条路径：为什么基准分数会虚高", 15.5, "middle", 700)
    rows = [("系列泄漏", "同一篇论文的同系列类似物被随机分到训练集与测试集两边",
             "按骨架或来源文献划分", OI["crimson"]),
            ("时间泄漏", "用后来才有的数据训练，去预测更早的结果",
             "按时间划分，模拟真实的前瞻场景", OI["orange"]),
            ("结构泄漏", "测试集的蛋白与训练集高度同源（序列相似度 > 30%）",
             "按序列相似度或家族聚类划分", OI["blue"]),
            ("预处理泄漏", "标准化、特征选择或归一化在划分之前对全量数据做",
             "所有预处理只在训练折内拟合", OI["purple"]),
            ("调参泄漏", "用测试集反复调超参，测试集实际上变成了验证集",
             "划出独立的、只用一次的保留集", OI["green"])]
    for i, (a, b, c, col) in enumerate(rows):
        y = 62 + i * 76
        s.box(24, y, 170, 64, a, None, color=col, size=13.5, tint=0.17)
        s.text(216, y + 26, b, 12.5, "start", 400)
        s.text(216, y + 50, "对策：" + c, 12, "start", 600, col)
    s.text(24, 462, "五条路径的共同后果：报告的性能描述的是记忆能力，而不是泛化能力。",
           12.5, "start", 700, "#444")
    return s.save(os.path.join(SV, "leakage_paths.svg"))


def fig_metric_mismatch():
    plt = mpl_setup()
    import numpy as np
    rng = np.random.default_rng(11)
    n = 300
    truth = rng.normal(6.5, 1.2, n)
    # model A: good R2 globally, poor at the top
    predA = truth + rng.normal(0, 0.55, n)
    # model B: worse globally, but ranks the top correctly
    predB = truth + rng.normal(0, 1.0, n)
    predB[truth > 8.0] = truth[truth > 8.0] + rng.normal(0, 0.25, (truth > 8.0).sum())
    predA[truth > 8.0] = truth[truth > 8.0] + rng.normal(0, 1.3, (truth > 8.0).sum())
    fig, axes = plt.subplots(1, 2, figsize=(9.0, 3.7), sharex=True, sharey=True)
    for ax, pred, nm, c in zip(axes, [predA, predB], ["模型 A", "模型 B"], [OI["blue"], OI["green"]]):
        r2 = 1 - ((truth - pred) ** 2).sum() / ((truth - truth.mean()) ** 2).sum()
        hi = truth > 8.0
        ax.plot(truth[~hi], pred[~hi], "o", color=c, ms=4, alpha=0.45)
        ax.plot(truth[hi], pred[hi], "o", color=OI["crimson"], ms=6)
        ax.plot([3, 11], [3, 11], color="#bbb", lw=1.0, ls="--")
        ax.set_title(f"{nm}：全局 R² = {r2:.2f}", loc="left", fontsize=12)
        ax.set_xlabel("实测 pIC50")
        for s_ in ("top", "right"):
            ax.spines[s_].set_visible(False)
    axes[0].set_ylabel("预测 pIC50")
    axes[0].set_xlim(3, 11); axes[0].set_ylim(3, 11)
    axes[1].text(3.4, 10.2, "红点 = 高活性分子\n（项目真正关心的部分）",
                 fontsize=10.5, color=OI["crimson"], va="top")
    fig.suptitle("全局 R² 更高的模型，在真正关心的高活性区间可能更差",
                 x=0.01, y=1.04, ha="left", fontsize=12.5)
    fig.subplots_adjust(top=0.80, bottom=0.17, wspace=0.12)
    return save_chart(fig, os.path.join(SV, "metric_mismatch.svg"))


def fig_eval_checklist():
    W, H = 1020, 420
    s = SVG(W, H)
    s.text(W / 2, 28, "读到一个性能数字时该问的七个问题", 15.5, "middle", 700)
    qs = [("划分方式是什么？", "随机、骨架、时间——三者评价的是不同能力"),
          ("基线是什么？", "与随机森林或最近邻比过吗，还是只与其他深度模型比"),
          ("指标是否匹配用途？", "排序任务用富集指标，不是全局相关系数"),
          ("标签噪声是多少？", "测试误差低于标签噪声就要怀疑泄漏"),
          ("适用域覆盖了什么？", "测试集与真实使用场景的分布是否一致"),
          ("重复了几次？", "单次运行的差异可能大于方法之间的差异"),
          ("消融做了吗？", "去掉关键输入后性能是否下降，若不降则模型学的是别的")]
    for i, (a, b) in enumerate(qs):
        y = 62 + i * 48
        s.box(24, y, 212, 38, a, None, color=OI["blue"], size=12.5, tint=0.13)
        s.text(258, y + 25, b, 12, "start", 400, "#444")
    s.text(24, 410, "七问中任何一问没有答案，这个数字就不足以支撑决策。", 12.5, "start", 700, OI["crimson"])
    return s.save(os.path.join(SV, "eval_checklist.svg"))


if __name__ == "__main__":
    print(fig_leakage(), fig_eval_checklist())
    print(fig_metric_mismatch())
