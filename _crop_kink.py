# -*- coding: utf-8 -*-
"""Crop and magnify the circled kink region from the user screenshot."""
from pathlib import Path
from PIL import Image, ImageDraw

src = Path(
    r"C:\Users\hp\.cursor\projects\c-Users-hp-Desktop-yaw-studio-website-3-0-yaw-studio"
    r"\assets\c__Users_hp_AppData_Roaming_Cursor_User_workspaceStorage_"
    r"9b809459abfd88f3bd065e71e6ab3b98_images_image-33fc6b01-837b-4725-8e76-126bcb7e7891.png"
)
im = Image.open(src).convert("RGBA")
print("shot", im.size)
# Red circle is on bottom-right of W — find red annotation pixels
w, h = im.size
reds = []
for y in range(h):
    for x in range(w):
        r, g, b, a = im.getpixel((x, y))
        if a > 200 and r > 180 and g < 80 and b < 80:
            # exclude logo's own red (center) — annotation is on far right
            if x > w * 0.65:
                reds.append((x, y))
if not reds:
    print("no red found on right")
else:
    xs = [p[0] for p in reds]
    ys = [p[1] for p in reds]
    print("red bbox", min(xs), min(ys), max(xs), max(ys), "count", len(reds))
    # crop around annotation with padding
    pad = 40
    box = (
        max(0, min(xs) - pad),
        max(0, min(ys) - pad),
        min(w, max(xs) + pad),
        min(h, max(ys) + pad),
    )
    crop = im.crop(box)
    # also a tighter crop of the W stroke itself (left of the circle center)
    cx = sum(xs) / len(xs)
    cy = sum(ys) / len(ys)
    print("center", cx, cy)
    tight = im.crop((int(cx - 120), int(cy - 100), int(cx + 40), int(cy + 100)))
    out = Path(r"_tmp_logo")
    out.mkdir(exist_ok=True)
    crop.resize((crop.width * 3, crop.height * 3), Image.NEAREST).save(out / "kink_region.png")
    tight.resize((tight.width * 4, tight.height * 4), Image.NEAREST).save(out / "kink_tight.png")
    print("saved crops")
