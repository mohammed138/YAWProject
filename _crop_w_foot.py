# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw

# User screenshot
src = Path(
    r"C:\Users\hp\.cursor\projects\c-Users-hp-Desktop-yaw-studio-website-3-0-yaw-studio"
    r"\assets\c__Users_hp_AppData_Roaming_Cursor_User_workspaceStorage_"
    r"9b809459abfd88f3bd065e71e6ab3b98_images_image-33fc6b01-837b-4725-8e76-126bcb7e7891.png"
)
im = Image.open(src).convert("RGBA")
w, h = im.size
# Far-right bottom of logo — W foot. Based on layout, W right edge is near right side.
# Crop right 28% width, bottom 55% 
box = (int(w * 0.72), int(h * 0.35), int(w * 0.98), int(h * 0.78))
crop = im.crop(box)
crop.resize((crop.width * 4, crop.height * 4), Image.NEAREST).save(
    Path("_tmp_logo/w_right_foot.png")
)
print("box", box, "saved")

# Also from our clean SVG render
an = Image.open("_tmp_logo/analyze.png").convert("RGB")
# svg (900,420)-(1080,520) -> px
# scale 2, offset 60,20
box2 = (int((900 - 60) * 2), int((420 - 20) * 2), int((1080 - 60) * 2), int((520 - 20) * 2))
c2 = an.crop(box2)
c2.resize((c2.width * 3, c2.height * 3), Image.NEAREST).save("_tmp_logo/w_right_svg.png")
print("svg box", box2)
