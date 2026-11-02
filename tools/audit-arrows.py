#!/usr/bin/env python3
"""静态审计 SVG 插图中的箭头质量问题。

检测三类缺陷：
  1. 箭头线段穿过与自身端点无关的矩形（"箭头穿框"）
  2. 带 marker-end 但引用了不存在的 marker 定义（渲染为无箭头或报错）
  3. 线段长度过短（< 8px），箭头头部会盖住整条线
"""
import glob
import os
import re
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"


def seg_rect_cross(p0, p1, rect, pad=2.0):
    """线段 p0->p1 是否穿过矩形内部（两端点都在矩形外时才算穿过）。"""
    x, y, w, h = rect
    x0, y0, x1, y1 = x - pad, y - pad, x + w + pad, y + h + pad

    def inside(p):
        return x0 <= p[0] <= x1 and y0 <= p[1] <= y1

    if inside(p0) or inside(p1):
        return False  # 端点贴在框上，属正常连接

    # Liang-Barsky 裁剪
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, p0[0] - x0), (dx, x1 - p0[0]), (-dy, p0[1] - y0), (dy, y1 - p0[1])):
        if p == 0:
            if q < 0:
                return False
        else:
            t = q / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True


def parse_path_points(d):
    """粗略提取 path 的折点（仅支持 M/L/H/V 绝对指令，figkit 只生成这些）。"""
    toks = re.findall(r"([MLHVAmlhvaCcQqZz])|(-?\d+\.?\d*)", d)
    cmds, pts, cur, mode = [], [], [0.0, 0.0], None
    nums = []
    for c, n in toks:
        if c:
            if mode and nums:
                pass
            mode = c
            nums = []
            cmds.append(c)
        else:
            nums.append(float(n))
            if mode in ("M", "L") and len(nums) == 2:
                cur = [nums[0], nums[1]]
                pts.append(tuple(cur))
                nums = []
            elif mode == "H" and len(nums) == 1:
                cur = [nums[0], cur[1]]
                pts.append(tuple(cur))
                nums = []
            elif mode == "V" and len(nums) == 1:
                cur = [cur[0], nums[0]]
                pts.append(tuple(cur))
                nums = []
            elif mode in ("C", "Q", "c", "q", "m", "l", "h", "v"):
                nums = []  # 曲线/相对指令不参与穿框判定
    return pts, set(cmds)


def audit_bounds(root):
    """元素是否超出画布：方框/圆被裁掉是最刺眼的排版缺陷。"""
    out = []
    try:
        W = float(root.get("width")); H = float(root.get("height"))
    except (TypeError, ValueError):
        return out
    for r in root.iter(NS + "rect"):
        try:
            x, y = float(r.get("x", 0)), float(r.get("y", 0))
            w, h = float(r.get("width", 0)), float(r.get("height", 0))
        except ValueError:
            continue
        if x < -0.5 or y < -0.5 or x + w > W + 0.5 or y + h > H + 0.5:
            out.append(f"方框出界: ({x:.0f},{y:.0f},{w:.0f}x{h:.0f}) 画布 {W:.0f}x{H:.0f}")
    for t in root.iter(NS + "text"):
        if t.get("transform"):
            continue  # 旋转文本（轴标签）另算
        try:
            x, y = float(t.get("x", 0)), float(t.get("y", 0))
            size = float(t.get("font-size", 12))
        except ValueError:
            continue
        txt = "".join(t.itertext())
        w = sum(size * (1.0 if ord(ch) > 0x2E80 else 0.56) for ch in txt)
        a = t.get("text-anchor", "start")
        x0 = x if a == "start" else (x - w / 2 if a == "middle" else x - w)
        if x0 < -2 or x0 + w > W + 2 or y > H + 2:
            out.append(f"文字出界: “{txt[:22]}” 右端 {x0 + w:.0f} / 画布宽 {W:.0f}")
    for c in root.iter(NS + "circle"):
        try:
            cx, cy, rr = float(c.get("cx")), float(c.get("cy")), float(c.get("r"))
        except (TypeError, ValueError):
            continue
        if cx - rr < -0.5 or cy - rr < -0.5 or cx + rr > W + 0.5 or cy + rr > H + 0.5:
            out.append(f"圆出界: ({cx:.0f},{cy:.0f},r={rr:.0f}) 画布 {W:.0f}x{H:.0f}")
    return out


def audit(path):
    issues = []
    tree = ET.parse(path)
    root = tree.getroot()
    issues += audit_bounds(root)
    markers = {m.get("id") for m in root.iter(NS + "marker")}

    rects = []
    for r in root.iter(NS + "rect"):
        try:
            rects.append(
                (
                    float(r.get("x", 0)),
                    float(r.get("y", 0)),
                    float(r.get("width", 0)),
                    float(r.get("height", 0)),
                )
            )
        except ValueError:
            pass
    # 背景底板（占满画布）不参与判定
    if rects:
        maxa = max(w * h for _, _, w, h in rects)
        rects = [r for r in rects if r[2] * r[3] < maxa * 0.6]

    segs = []  # (p0, p1, 标签)
    for ln in root.iter(NS + "line"):
        try:
            p0 = (float(ln.get("x1")), float(ln.get("y1")))
            p1 = (float(ln.get("x2")), float(ln.get("y2")))
        except (TypeError, ValueError):
            continue
        segs.append((p0, p1, ln, "line"))
    for pa in root.iter(NS + "path"):
        d = pa.get("d") or ""
        pts, cmds = parse_path_points(d)
        # 曲线、圆弧与相对指令不参与穿框判定：解析器只认绝对 M/L/H/V，
        # 把 A 的半径参数当成坐标会产生大量误报
        if cmds & set("CcQqAamlhv"):
            continue
        for a, b in zip(pts, pts[1:]):
            segs.append((a, b, pa, "path"))

    for p0, p1, el, kind in segs:
        mk = el.get("marker-end") or el.get("marker-start") or ""
        m = re.match(r"url\(#(.+)\)", mk)
        if m and m.group(1) not in markers:
            issues.append(f"marker 未定义: {m.group(1)}")
        L = ((p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2) ** 0.5
        # 阈值取 4px：短于箭头本身的线段会被头部完全盖住。
        # 5–8px 的短接头（如决策菱形两侧的小箭头）是正常画法，不报。
        if mk and L < 4:
            issues.append(f"箭头线段过短 ({L:.1f}px) @ {p0}")
        if not mk:
            continue
        for r in rects:
            if seg_rect_cross(p0, p1, r):
                issues.append(
                    f"箭头穿框: ({p0[0]:.0f},{p0[1]:.0f})->({p1[0]:.0f},{p1[1]:.0f}) "
                    f"穿过 rect({r[0]:.0f},{r[1]:.0f},{r[2]:.0f}x{r[3]:.0f})"
                )
    return issues


def main():
    files = sorted(glob.glob("contents/core/*/images/svg/*.svg"))
    bad = 0
    for f in files:
        try:
            iss = audit(f)
        except Exception as e:  # noqa: BLE001
            print(f"!! {f}: 解析失败 {e}")
            continue
        if iss:
            bad += 1
            short = f.replace("contents/core/", "").replace("/images/svg/", "/")
            print(f"\n== {short}")
            for i in iss[:12]:
                print(f"   - {i}")
            if len(iss) > 12:
                print(f"   ... 另有 {len(iss) - 12} 条")
    print(f"\n共 {len(files)} 张，{bad} 张存在疑似问题")


if __name__ == "__main__":
    main()
