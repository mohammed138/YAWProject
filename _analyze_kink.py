# -*- coding: utf-8 -*-
"""Render SVG and detect kink on W right outer edge."""
from pathlib import Path
import subprocess
import tempfile
import re
from PIL import Image

ROOT = Path(r"c:\Users\hp\Desktop\yaw-studio-website (3)0\yaw-studio")
LOGO = ROOT / "assets" / "logo"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
OUT = ROOT / "_tmp_logo"
OUT.mkdir(exist_ok=True)

svg = (LOGO / "yaw-logo-vector-clear.svg").read_text(encoding="utf-8")
# render just the YAW mark (navy) on white for analysis
# bump size for precision
w, h = 2160, 1120
page = Path(tempfile.gettempdir()) / "yaw-kink-analyze.html"
page.write_text(
    f"""<!doctype html><html><head><style>
html,body{{margin:0;width:{w}px;height:{h}px;background:#fff;overflow:hidden}}
img{{width:{w}px;height:{h}px;display:block}}
</style></head><body>
<img src="{(LOGO / 'yaw-logo-vector-clear.svg').as_uri()}">
</body></html>""",
    encoding="utf-8",
)
shot = OUT / "analyze.png"
subprocess.run(
    [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        f"--window-size={w},{h}",
        f"--screenshot={shot}",
        page.as_uri(),
    ],
    check=True,
    capture_output=True,
)

im = Image.open(shot).convert("RGB")
print("rendered", im.size)

# viewBox 60 20 1080 560 mapped to 2160x1120
# scale = 2160/1080 = 2, 1120/560 = 2
# svg x -> (x-60)*2, svg y -> (y-20)*2

def to_px(sx, sy):
    return int(round((sx - 60) * 2)), int(round((sy - 20) * 2))


# Trace outer right edge: for each y from bottom to top near expected x, find rightmost navy pixel
# Navy approx #1F3288
def is_navy(p):
    r, g, b = p
    return abs(r - 31) < 40 and abs(g - 50) < 40 and abs(b - 136) < 50 and b > r + 40


# Scan y from 500..46 in svg = px
y0 = to_px(0, 500)[1]
y1 = to_px(0, 46)[1]
print("y px range", y0, y1)

edge = []
for py in range(y0, y1 - 1, -1):
    # search x from right
    found = None
    for px in range(im.width - 1, im.width // 2, -1):
        if is_navy(im.getpixel((px, py))):
            found = px
            break
    if found is not None:
        # convert back to svg-ish
        sx = found / 2 + 60
        sy = py / 2 + 20
        edge.append((py, found, sx, sy))

# Look for slope changes
print("edge samples", len(edge))
# compute local dx/dy over windows
prev = None
kinks = []
for i in range(5, len(edge) - 5):
    y_a, x_a, _, _ = edge[i - 5]
    y_b, x_b, _, _ = edge[i]
    y_c, x_c, _, _ = edge[i + 5]
    # slopes in px (x change per y step up, y decreases)
    s1 = (x_b - x_a) / (y_a - y_b + 1e-9)  # as y decreases (going up)
    s2 = (x_c - x_b) / (y_b - y_c + 1e-9)
    if abs(s1 - s2) > 0.35:
        kinks.append((edge[i], s1, s2, abs(s1 - s2)))

print("potential kinks (top 10 by delta):")
kinks.sort(key=lambda k: -k[3])
for k in kinks[:10]:
    (py, px, sx, sy), s1, s2, d = k
    print(f"  svg≈({sx:.1f},{sy:.1f}) px=({px},{py}) s1={s1:.3f} s2={s2:.3f} d={d:.3f}")

# Also print edge near bottom (first 40 samples going up from bottom)
print("\nbottom of right edge (first 40):")
for row in edge[:40]:
    py, px, sx, sy = row
    print(f"  svg({sx:.2f},{sy:.2f}) px({px},{py})")
