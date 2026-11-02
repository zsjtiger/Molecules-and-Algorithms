import sys, os, io
sys.path.insert(0, "/home/claude/aidd_book/tools")
from figkit import SVG, OI, mpl_setup, save_chart, mol_svg
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SV = os.path.join(HERE, "images", "svg")
from rdkit import Chem
from rdkit.Chem import AllChem, Draw, rdDepictor
from rdkit.Chem.Draw import rdMolDraw2D
import numpy as np

ASPIRIN = "CC(=O)Oc1ccccc1C(=O)O"

def rd_png(m, w=420, h=320, highlight=None, hcol=None, idx=False, legend=""):
    d = rdMolDraw2D.MolDraw2DCairo(w, h)
    o = d.drawOptions(); o.addAtomIndices = idx; o.bondLineWidth = 2; o.legendFontSize = 18
    o.annotationFontScale = 0.8
    if highlight:
        d.DrawMolecule(m, highlightAtoms=highlight, highlightAtomColors=hcol or {}, highlightBonds=[], legend=legend)
    else:
        d.DrawMolecule(m, legend=legend)
    d.FinishDrawing()
    from PIL import Image
    return Image.open(io.BytesIO(d.GetDrawingText()))

def fig_views():
    plt = mpl_setup()
    import selfies as sf
    m = Chem.MolFromSmiles(ASPIRIN); rdDepictor.Compute2DCoords(m)
    fig = plt.figure(figsize=(10.5, 6.2))
    gs = fig.add_gridspec(2, 3, wspace=0.25, hspace=0.38)
    # a: 2D structure with indices
    ax = fig.add_subplot(gs[0, 0]); ax.imshow(rd_png(m, idx=True)); ax.axis("off")
    ax.set_title("a  二维结构（原子编号）", loc="left", fontsize=11.5)
    # b: graph view
    ax = fig.add_subplot(gs[0, 1])
    conf = m.GetConformer()
    pos = np.array([[conf.GetAtomPosition(i).x, conf.GetAtomPosition(i).y] for i in range(m.GetNumAtoms())])
    for b in m.GetBonds():
        i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
        lw = {1.0: 1.2, 1.5: 2.0, 2.0: 2.8}.get(b.GetBondTypeAsDouble(), 1.2)
        ax.plot(*pos[[i, j]].T, color="#888", lw=lw, zorder=1)
    col = {"C": OI["gray"], "O": OI["verm"]}
    for a in m.GetAtoms():
        p = pos[a.GetIdx()]
        ax.scatter(*p, s=260, color=col.get(a.GetSymbol(), OI["blue"]), zorder=2, edgecolor="white", lw=1)
        ax.text(*p, a.GetSymbol(), ha="center", va="center", color="white", fontsize=9, zorder=3, fontweight="bold")
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("b  分子图：原子 = 节点，键 = 边", loc="left", fontsize=11.5)
    # c: 3D conformer projection
    mh = Chem.AddHs(m); AllChem.EmbedMolecule(mh, randomSeed=7); AllChem.MMFFOptimizeMolecule(mh)
    ax = fig.add_subplot(gs[0, 2], projection="3d")
    c3 = mh.GetConformer(); P = np.array([list(c3.GetAtomPosition(i)) for i in range(mh.GetNumAtoms())])
    for b in mh.GetBonds():
        i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
        ax.plot(*P[[i, j]].T, color="#999", lw=1.2)
    for a in mh.GetAtoms():
        c = {"C": OI["gray"], "O": OI["verm"], "H": "#dddddd"}.get(a.GetSymbol(), OI["blue"])
        ax.scatter(*P[a.GetIdx()], s=60 if a.GetSymbol() != "H" else 18, color=c, depthshade=False)
    ax.set_axis_off(); ax.view_init(elev=20, azim=35)
    ax.set_title("c  三维构象（MMFF 优化）", loc="left", fontsize=11.5)
    # d: strings
    ax = fig.add_subplot(gs[1, 0]); ax.axis("off")
    s_smi = ASPIRIN
    s_sf = sf.encoder(ASPIRIN)
    ax.text(0, 0.88, "SMILES", fontsize=11, fontweight="bold")
    ax.text(0, 0.72, s_smi, fontsize=11, family="DejaVu Sans Mono")
    ax.text(0, 0.50, "SELFIES（前 6 个符号）", fontsize=11, fontweight="bold")
    toks = list(sf.split_selfies(s_sf))
    ax.text(0, 0.34, "".join(toks[:6]) + " …", fontsize=10, family="DejaVu Sans Mono")
    ax.text(0, 0.14, f"共 {len(toks)} 个符号；任意符号序列都对应合法分子", fontsize=10, color="#555")
    ax.set_title("d  一维字符串", loc="left", fontsize=11.5)
    # e: ECFP4 bit vector
    ax = fig.add_subplot(gs[1, 1:])
    fp = AllChem.GetMorganFingerprintAsBitVect(m, 2, nBits=256)
    arr = np.array(list(fp)).reshape(8, 32)
    ax.imshow(arr, cmap="Greys", aspect="auto", vmin=0, vmax=1.4)
    ax.set_xticks([]); ax.set_yticks([])
    for s_ in ax.spines.values(): s_.set_visible(True); s_.set_color("#bbb")
    ax.set_title(f"e  ECFP4 指纹（256 位示意，{int(arr.sum())} 位为 1）", loc="left", fontsize=11.5)
    return save_chart(fig, os.path.join(SV, "aspirin_views.svg"))

def fig_ecfp():
    plt = mpl_setup()
    m = Chem.MolFromSmiles("CC(C)Cc1ccc(cc1)C(C)C(=O)O")  # ibuprofen
    rdDepictor.Compute2DCoords(m)
    center = 9  # aromatic carbon bearing propanoic acid
    fig, axes = plt.subplots(1, 3, figsize=(10.5, 3.2))
    for r, ax in zip([0, 1, 2], axes):
        if r == 0:
            atoms = {center}
        else:
            env = Chem.FindAtomEnvironmentOfRadiusN(m, r, center)
            atoms = {center}
            for bid in env:
                b = m.GetBondWithIdx(bid); atoms |= {b.GetBeginAtomIdx(), b.GetEndAtomIdx()}
        hc = {a: (0.90, 0.62, 0.0) if a != center else (0.65, 0.11, 0.19) for a in atoms}
        ax.imshow(rd_png(m, 420, 300, highlight=list(atoms), hcol=hc)); ax.axis("off")
        ax.set_title(f"半径 {r}：{len(atoms)} 个原子", loc="left", fontsize=11.5)
    fig.suptitle("ECFP 的迭代：以同一原子为中心，每轮把视野扩大一跳（布洛芬）", x=0.01, ha="left", fontsize=12.5)
    return save_chart(fig, os.path.join(SV, "ecfp_radius.svg"))

def fig_thalidomide():
    plt = mpl_setup()
    R = Chem.MolFromSmiles("O=C1CC[C@@H](N2C(=O)c3ccccc3C2=O)C(=O)N1")
    S = Chem.MolFromSmiles("O=C1CC[C@H](N2C(=O)c3ccccc3C2=O)C(=O)N1")
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    for ax, mm, t in zip(axes, [R, S], ["(R)-沙利度胺", "(S)-沙利度胺"]):
        rdDepictor.Compute2DCoords(mm)
        d = rdMolDraw2D.MolDraw2DCairo(460, 300); o = d.drawOptions(); o.addStereoAnnotation = True; o.bondLineWidth = 2
        d.DrawMolecule(mm); d.FinishDrawing()
        from PIL import Image
        ax.imshow(Image.open(io.BytesIO(d.GetDrawingText()))); ax.axis("off"); ax.set_title(t, fontsize=12)
    fig.suptitle("同一张二维连接图，两种空间排布：对映体需要立体信息才能区分", x=0.01, ha="left", fontsize=12.5)
    return save_chart(fig, os.path.join(SV, "thalidomide.svg"))

def fig_mpnn():
    W, H = 1060, 380
    s = SVG(W, H)
    s.text(W / 2, 28, "消息传递神经网络：每一层让原子“看到”更远一跳的邻居", 15.5, "middle", 700)
    # small graph panel 1
    def graph(ox, oy, hl, title):
        pts = {0: (0, 0), 1: (60, -35), 2: (120, 0), 3: (60, 45), 4: (180, -35), 5: (-60, -35)}
        edges = [(0, 1), (1, 2), (0, 3), (2, 3), (2, 4), (0, 5)]
        for i, j in edges:
            s.line(ox + pts[i][0], oy + pts[i][1], ox + pts[j][0], oy + pts[j][1], OI["lgray"], 2, head=None)
        for k, (x, y) in pts.items():
            c = OI["crimson"] if k == 0 else (OI["orange"] if k in hl else OI["gray"])
            s.circle(ox + x, oy + y, 13, c, tint=0.9 if (k == 0 or k in hl) else 0.25)
            s.text(ox + x, oy + y + 4.5, f"v{k}", 11, "middle", 700, "#ffffff" if (k == 0 or k in hl) else OI["black"])
        s.text(ox + 60, oy + 95, title, 12.5, "middle", 600)
    graph(120, 150, set(), "第 0 层：只有自身特征 h(0)")
    graph(470, 150, {1, 3, 5}, "第 1 层：聚合直接邻居的消息")
    graph(820, 150, {1, 3, 5, 2}, "第 2 层：信息来自两跳范围")
    s.line(330, 150, 400, 150, OI["black"], 1.5); s.line(680, 150, 750, 150, OI["black"], 1.5)
    s.text(365, 138, "M, U", 12, "middle", 600); s.text(715, 138, "M, U", 12, "middle", 600)
    # readout
    s.box(360, 290, 340, 50, "读出 R：汇总所有原子表示 → 分子性质预测值", None, color=OI["blue"], size=13, tint=0.12)
    s.text(530, 365, "M：消息函数；U：更新函数。T 层之后，每个原子表示编码半径为 T 的局部化学环境（与 ECFP 的迭代哈希同构）", 11, "middle", 400, "#555")
    return s.save(os.path.join(SV, "mpnn.svg"))

def fig_protein_reps():
    W, H = 1060, 290
    s = SVG(W, H)
    s.text(W / 2, 28, "蛋白质的五种表示：从序列到可被语言模型处理的结构词元", 15.5, "middle", 700)
    items = [("氨基酸序列", "MKTAYIAKQR…（20 种字母）", OI["gray"]),
             ("多序列比对 MSA", "同源序列对齐 → 共进化信号", OI["green"]),
             ("语言模型嵌入", "ESM 等：每个残基一个向量", OI["blue"]),
             ("三维结构", "骨架刚体框架 / 全原子坐标 / 残基对距离", OI["crimson"]),
             ("离散结构词元", "Foldseek 3Di、ESM3 结构词元", OI["purple"])]
    bw, gap, y = 184, 22, 90
    for i, (a, b, c) in enumerate(items):
        x = 22 + i * (bw + gap)
        s.box(x, y, bw, 100, a, b, color=c, size=13.5, subsize=11.5, tint=0.12)
        if i < 4: s.line(x + bw, y + 50, x + bw + gap, y + 50, OI["black"], 1.5)
    s.text(22, 235, "AlphaFold2 依赖 MSA；ESMFold 用语言模型嵌入替代 MSA；ESM3 把结构离散化为词元，与序列、功能一起生成。", 12, "start", 400, "#444")
    s.text(22, 262, "越往右，表示越接近“可直接用于设计”的形式，但也越依赖预训练模型的质量。", 12, "start", 400, "#444")
    return s.save(os.path.join(SV, "protein_reps.svg"))

if __name__ == "__main__":
    print(fig_views()); print(fig_ecfp()); print(fig_thalidomide()); print(fig_mpnn(), fig_protein_reps())
