# -*- coding: utf-8 -*-
from pathlib import Path
import re

svg = Path(r"assets/logo/yaw-logo-vector-clear.svg").read_text(encoding="utf-8")
m = re.search(r'<path d="([^"]+)" fill="#1F3288" fill-rule="evenodd"', svg)
d = m.group(1)
tokens = re.findall(r"[MLHZ]|-?[\d.]+", d)
cmd = None
pts = []
i = 0
while i < len(tokens):
    t = tokens[i]
    if t in "MLHZ":
        cmd = t
        i += 1
        if cmd == "Z":
            pts.append(("Z", None, None))
        continue
    if cmd in ("M", "L"):
        x = float(tokens[i])
        y = float(tokens[i + 1])
        i += 2
        pts.append((cmd, x, y))
    elif cmd == "H":
        x = float(tokens[i])
        i += 1
        pts.append(("H", x, None))
    elif cmd == "V":
        y = float(tokens[i])
        i += 1
        pts.append(("V", None, y))
    else:
        i += 1

print("=== first contour (outer) ===")
for n, (c, x, y) in enumerate(pts):
    if c == "Z" and n > 0:
        print(f"{n:3d} Z  ---- end outer ----")
        break
    print(f"{n:3d} {c} x={x} y={y}")

print("\n=== rightmost points x>=900 ===")
for n, (c, x, y) in enumerate(pts):
    if x is not None and x >= 900:
        print(f"{n:3d} {c} x={x} y={y}")

print("\n=== W hole (3rd subpath typically) ===")
z_idx = [n for n, (c, _, _) in enumerate(pts) if c == "Z"]
print("Z indices", z_idx)
# print each contour
start = 0
for zi in z_idx:
    contour = pts[start : zi + 1]
    xs = [x for _, x, _ in contour if x is not None]
    if xs and max(xs) > 800:
        print(f"\n-- contour {start}:{zi} maxx={max(xs):.1f} --")
        for n, (c, x, y) in enumerate(contour):
            abs_n = start + n
            print(f"{abs_n:3d} {c} x={x} y={y}")
    start = zi + 1
