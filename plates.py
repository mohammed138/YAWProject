#!/usr/bin/env python3
"""
Placeholder plates for the YAW STUDIO build.

These are NOT photographs and they are NOT pictures of real places or
people. They are procedurally drawn atmospheric scenes — depth layers,
haze, directional light, grain — made only so the cinematic motion
(Ken Burns, dissolve, clip-path peel, grain, vignette) can be judged
with something that behaves like a photograph.

Replace every one of them with real work before publishing.
"""
import numpy as np
from PIL import Image, ImageFilter
import pathlib, math

OUT = pathlib.Path(__file__).parent / "yaw-studio" / "images"
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- helpers
def grad(h, w, top, bot, curve=1.0):
    t = (np.linspace(0, 1, h) ** curve)[:, None, None]
    g = np.array(top)[None, None, :] * (1 - t) + np.array(bot)[None, None, :] * t
    return np.broadcast_to(g, (h, w, 3)).astype(np.float64).copy()

def glow(h, w, cx, cy, r, strength, colour):
    y, x = np.mgrid[0:h, 0:w]
    d = np.sqrt(((x - cx) / r) ** 2 + ((y - cy) / (r * 0.85)) ** 2)
    g = np.clip(1 - d, 0, 1) ** 2.2
    return g[..., None] * np.array(colour)[None, None, :] * strength

def skyline(h, w, base, height, seed, blocks=14, jag=0.45):
    """a row of buildings as a boolean mask"""
    rng = np.random.default_rng(seed)
    mask = np.zeros((h, w), bool)
    x = -int(w * 0.05)
    while x < w:
        bw = int(rng.uniform(0.04, 0.13) * w)
        bh = int(height * rng.uniform(1 - jag, 1 + jag))
        top = max(0, base - bh)
        mask[top:base, max(0, x):min(w, x + bw)] = True
        # roof furniture — tanks, aerials
        if rng.random() < 0.55:
            tw = int(bw * rng.uniform(0.1, 0.26))
            th = int(bh * rng.uniform(0.05, 0.16))
            tx = x + int(bw * rng.uniform(0.1, 0.7))
            mask[max(0, top - th):top, max(0, tx):min(w, tx + tw)] = True
        x += bw + int(rng.uniform(0.002, 0.02) * w)
    return mask

def windows(h, w, mask, seed, density=0.34, val=0.55):
    rng = np.random.default_rng(seed + 99)
    lit = np.zeros((h, w), float)
    step_y, step_x = max(9, h // 90), max(7, w // 130)
    for yy in range(0, h - step_y, step_y * 2):
        for xx in range(0, w - step_x, step_x * 2):
            if mask[yy, xx] and rng.random() < density:
                lit[yy:yy + step_y, xx:xx + step_x] = rng.uniform(0.35, 1.0) * val
    return lit

def figure(h, w, cx, base, height, seed):
    """a simple standing silhouette"""
    rng = np.random.default_rng(seed)
    m = np.zeros((h, w), bool)
    hh = int(height)
    hw = max(2, int(hh * rng.uniform(0.17, 0.24)))
    head = int(hh * 0.16)
    top = base - hh
    y, x = np.mgrid[0:h, 0:w]
    m |= ((x - cx) ** 2 / (hw * 0.55) ** 2 + (y - (top + head * 0.5)) ** 2 / (head * 0.55) ** 2) < 1
    body = (np.abs(x - cx) < hw * 0.5) & (y > top + head) & (y < base)
    taper = (np.abs(x - cx) < hw * (0.5 + 0.35 * (y - top - head) / max(1, hh)))
    m |= body & taper
    return m

def finish(a, seed, grain=7.0, vig=0.62, warm=1.0):
    h, w = a.shape[:2]
    rng = np.random.default_rng(seed + 7)
    # grade
    a = a * np.array([warm, 1.0, 2.0 - warm])[None, None, :]
    # vignette
    y, x = np.mgrid[0:h, 0:w]
    d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    a = a * (1 - vig * np.clip(d - 0.35, 0, 1) ** 1.7)[..., None]
    # grain
    a = a + rng.normal(0, grain, (h, w, 1)) + rng.normal(0, grain * 0.4, (h, w, 3))
    a = np.clip(a, 0, 255).astype(np.uint8)
    im = Image.fromarray(a, "RGB")
    return im.filter(ImageFilter.GaussianBlur(0.4))

# ---------------------------------------------------------------- scenes
def _noise(h, w, seed, octaves=6):
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w))
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        n = max(2, int(4 * 2 ** o))
        small = rng.random((min(n, h), min(n, w)))
        up = np.asarray(Image.fromarray((small * 255).astype(np.uint8))
                        .resize((w, h), Image.BICUBIC)).astype(float) / 255.0
        out += up * amp; tot += amp; amp *= 0.52
    return out / tot

def scene_texture(w, h, seed):
    """a surface — wall, rubble, cloth — under raking light. Reads photographic."""
    rng = np.random.default_rng(seed)
    n = _noise(h, w, seed, 7)
    n = (n - n.min()) / (np.ptp(n) + 1e-6)
    # surface relief -> shading from a low light
    gy, gx = np.gradient(n)
    lx, ly = math.cos(rng.uniform(0, 6.28)), math.sin(rng.uniform(0, 6.28))
    shade = np.clip(0.5 + (gx * lx + gy * ly) * 26, 0, 1)
    base = 0.30 + 0.55 * n
    v = np.clip(base * (0.45 + 0.85 * shade), 0, 1)
    # broad light falloff across the frame
    yy, xx = np.mgrid[0:h, 0:w]
    fall = np.clip(1.25 - np.sqrt(((xx - w * rng.uniform(.2, .8)) / (w * .8)) ** 2 +
                                  ((yy - h * rng.uniform(.2, .8)) / (h * .8)) ** 2), .18, 1.2)
    v = np.clip(v * fall, 0, 1)
    warmv = np.array([1.0, 0.95, 0.86]) if seed % 2 else np.array([0.92, 0.95, 1.0])
    a = (v[..., None] * 235) * warmv[None, None, :]
    # a dark opening or object for depth
    if rng.random() < 0.8:
        ox, oy = w * rng.uniform(.12, .7), h * rng.uniform(.15, .58)
        ow, oh = w * rng.uniform(.14, .32), h * rng.uniform(.2, .48)
        sx = np.clip(1 - np.abs(xx - (ox + ow / 2)) / (ow / 2), 0, 1)
        sy = np.clip(1 - np.abs(yy - (oy + oh / 2)) / (oh / 2), 0, 1)
        soft = np.clip(np.minimum(sx, sy) * 9, 0, 1) ** 0.7
        a = a * (1 - soft[..., None] * 0.80)
    return finish(a, seed, grain=6.0, vig=0.58, warm=1.02)

def scene_street(w, h, seed, dawn=True):
    rng = np.random.default_rng(seed)
    if dawn:
        a = grad(h, w, (196, 176, 150), (86, 84, 92), 1.5)
        a += glow(h, w, w * rng.uniform(.38, .62), h * 0.46, w * 0.42, 1.0, (255, 226, 178))
        warm = 1.06
    else:
        a = grad(h, w, (150, 158, 172), (58, 62, 72), 1.4)
        a += glow(h, w, w * 0.5, h * 0.4, w * 0.5, 0.6, (210, 222, 236))
        warm = 0.98
    base = int(h * 0.78)
    for i, (hgt, tone, blur) in enumerate([(h*0.34, 0.55, 5), (h*0.44, 0.36, 2.5), (h*0.56, 0.14, 0)]):
        m = skyline(h, w, base + int(i * h * 0.03), hgt, seed + i * 13, blocks=12 - i * 2)
        lit = windows(h, w, m, seed + i * 21, density=0.30 - i * 0.08, val=0.8 - i * 0.2)
        layer = np.where(m[..., None], a * tone, a)
        layer = layer + lit[..., None] * np.array([255, 208, 150])[None, None, :] * 0.55
        if blur:
            layer = np.asarray(Image.fromarray(np.clip(layer,0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(blur))).astype(float)
        a = layer
    # ground
    gy = int(h * 0.82)
    a[gy:] = a[gy:] * 0.46
    rr = np.random.default_rng(seed + 3)
    for _ in range(int(w * 0.05)):
        bx = int(rr.uniform(0, w)); by = int(rr.uniform(gy, h))
        bw2 = int(rr.uniform(4, w * 0.02)); bh2 = int(rr.uniform(3, h * 0.012))
        a[by:by+bh2, bx:bx+bw2] *= rr.uniform(0.5, 1.35)
    # figures
    for k in range(rng.integers(1, 4)):
        m = figure(h, w, int(w * rng.uniform(0.12, 0.88)), int(h * rng.uniform(0.83, 0.92)),
                   h * rng.uniform(0.16, 0.30), seed + k * 31)
        a = np.where(m[..., None], a * 0.10, a)
    # haze
    a = a * 0.82 + grad(h, w, (44, 46, 54), (150, 146, 140), 0.8) * 0.18
    return finish(a, seed, warm=warm)

def scene_interior(w, h, seed):
    rng = np.random.default_rng(seed)
    a = grad(h, w, (44, 45, 50), (22, 23, 27), 0.8)
    # window light from one side
    cx = w * (0.22 if seed % 2 else 0.78)
    a += glow(h, w, cx, h * 0.34, w * 0.40, 0.62, (255, 236, 206))
    # window frame
    wx0, wx1 = int(cx - w*0.11), int(cx + w*0.11)
    wy0, wy1 = int(h*0.14), int(h*0.58)
    a[wy0:wy1, wx0:wx1] += 96
    for fx in np.linspace(wx0, wx1, 4).astype(int):
        a[wy0:wy1, max(0,fx-3):fx+3] *= 0.32
    a[int((wy0+wy1)/2)-3:int((wy0+wy1)/2)+3, wx0:wx1] *= 0.32
    # floor shaft of light
    y, x = np.mgrid[0:h, 0:w]
    shaft = np.clip(1 - np.abs(x - (cx + (w*0.16 if seed % 2 else -w*0.16))) / (w*0.22), 0, 1)
    shaft *= np.clip((y - h*0.5) / (h*0.45), 0, 1)
    a += shaft[..., None] * np.array([255, 232, 196])[None, None, :] * 24
    # figure against it
        # floor plane and a wall break, so it reads as a room not a poster
    fy = int(h * 0.74)
    a[fy:] = a[fy:] * 0.78
    a[fy-2:fy+2] *= 0.55
    m = figure(h, w, int(cx + (w*0.26 if seed % 2 else -w*0.26)), int(h*0.80), h*0.30, seed+5)
    a = np.where(m[..., None], a * 0.16, a)
    a = np.clip(a, 0, 245)
    return finish(a, seed, vig=0.66, warm=1.04)

def scene_horizon(w, h, seed):
    rng = np.random.default_rng(seed)
    a = grad(h, w, (206, 198, 186), (128, 134, 142), 2.1)
    a += glow(h, w, w * rng.uniform(.2, .8), h * 0.3, w * 0.55, 0.8, (255, 240, 214))
    base = int(h * 0.72)
    m = skyline(h, w, base, h * 0.16, seed, jag=0.7)
    a = np.where(m[..., None], a * 0.30, a)
    a[base:] = a[base:] * 0.55
    # dust band
    band = np.clip(1 - np.abs(np.arange(h) - base) / (h * 0.14), 0, 1)[:, None, None]
    a = a * (1 - band * 0.4) + np.array([214, 202, 182])[None, None, :] * band * 0.4
    for k in range(rng.integers(2, 6)):
        m2 = figure(h, w, int(w * rng.uniform(0.1, 0.9)), base + int(h*rng.uniform(0.02, 0.1)),
                    h * rng.uniform(0.07, 0.14), seed + k * 17)
        a = np.where(m2[..., None], a * 0.16, a)
    return finish(a, seed, vig=0.5, warm=1.04)

def scene_portrait(w, h, seed):
    a = grad(h, w, (58, 60, 66), (26, 27, 31), 1.0)
    a += glow(h, w, w * 0.30, h * 0.30, w * 0.60, 0.70, (255, 236, 206))
    m = figure(h, w, int(w * 0.52), int(h * 1.02), h * 0.72, seed)
    a = np.where(m[..., None], a * 0.13, a)
    return finish(a, seed, vig=0.75, warm=1.06)



# ================================================================
# THREE FAMILIES OF PLATE — one per act, so each act looks different
# ================================================================

def scene_wide(w, h, seed):
    """FILMS — anamorphic width, deep haze, a low sun, silhouettes at three
    distances. Meant to read as a frame pulled out of a film."""
    rng = np.random.default_rng(seed)
    sunx = w * rng.uniform(0.18, 0.82)
    a = grad(h, w, (188, 172, 152), (52, 56, 66), 1.7)
    a += glow(h, w, sunx, h * 0.52, w * 0.55, 1.15, (255, 214, 158))
    a += glow(h, w, sunx, h * 0.52, w * 0.12, 1.5, (255, 244, 222))
    yy, xx = np.mgrid[0:h, 0:w]
    streak = np.clip(1 - np.abs(yy - h * 0.52) / (h * 0.02), 0, 1) * \
             np.clip(1 - np.abs(xx - sunx) / (w * 0.45), 0, 1)
    a += streak[..., None] * np.array([120, 150, 210])[None, None, :] * 0.55
    base = int(h * 0.80)
    for i, (hgt, tone, blur) in enumerate([(h*0.30, 0.62, 6), (h*0.42, 0.40, 3), (h*0.58, 0.16, 0)]):
        m = skyline(h, w, base + int(i * h * 0.02), hgt, seed + i * 13)
        lay = np.where(m[..., None], a * tone, a)
        if blur:
            lay = np.asarray(Image.fromarray(np.clip(lay,0,255).astype(np.uint8))
                             .filter(ImageFilter.GaussianBlur(blur))).astype(float)
        a = lay
    a[base:] *= 0.5
    for k in range(rng.integers(2, 5)):
        sc = rng.uniform(0.10, 0.30)
        m = figure(h, w, int(w*rng.uniform(0.08,0.92)), base + int(h*rng.uniform(0.0,0.09)), h*sc, seed+k*29)
        a = np.where(m[..., None], a * 0.09, a)
    a = a * 0.86 + grad(h, w, (30, 34, 42), (168, 150, 126), 0.7) * 0.14
    return finish(a, seed, grain=8.0, vig=0.68, warm=1.07)


def scene_report(w, h, seed):
    """STORIES — a courtyard or a doorway: wall, opening, washing lines,
    people at different depths. Human scale, not epic."""
    rng = np.random.default_rng(seed)
    n = _noise(h, w, seed, 6)
    n = (n - n.min()) / (np.ptp(n) + 1e-6)
    a = (0.34 + 0.42 * n)[..., None] * np.array([232, 224, 210])[None, None, :]
    dx, dy = w * rng.uniform(.24, .62), h * rng.uniform(.14, .28)
    dw, dh = w * rng.uniform(.16, .26), h * rng.uniform(.46, .64)
    yy, xx = np.mgrid[0:h, 0:w]
    inside = (xx > dx) & (xx < dx + dw) & (yy > dy) & (yy < dy + dh)
    a = np.where(inside[..., None], a * 0.16, a)
    a += glow(h, w, dx + dw/2, dy + dh*0.75, dw*1.5, 0.55, (255, 236, 206))
    for k in range(int(rng.integers(2, 5))):
        ly = int(h * rng.uniform(0.10, 0.40))
        a[ly:ly+2, :] *= 0.55
        for c in range(int(rng.integers(3, 9))):
            cx = int(w * rng.uniform(0.02, 0.94)); cw = int(w * rng.uniform(.03, .08))
            ch = int(h * rng.uniform(.06, .16))
            a[ly:ly+ch, cx:cx+cw] *= rng.uniform(0.45, 0.95)
    gy = int(h * 0.84); a[gy:] *= 0.62
    m = figure(h, w, int(dx + dw*rng.uniform(.2,.8)), int(dy+dh), dh*0.72, seed+3)
    a = np.where(m[..., None], a * 0.22, a)
    for k in range(int(rng.integers(1, 4))):
        m2 = figure(h, w, int(w*rng.uniform(.05,.95)), int(h*rng.uniform(.80,.90)),
                    h*rng.uniform(.14,.34), seed+k*37)
        a = np.where(m2[..., None], a * 0.18, a)
    return finish(a, seed, grain=6.5, vig=0.52, warm=1.05)


def scene_still(w, h, seed):
    """FRAMES — one strong shape, one strong light, a lot of quiet wall."""
    rng = np.random.default_rng(seed)
    n = _noise(h, w, seed + 4, 7)
    n = (n - n.min()) / (np.ptp(n) + 1e-6)
    gy_, gx_ = np.gradient(n)
    ang = rng.uniform(0, 6.28)
    shade = np.clip(.5 + (gx_*math.cos(ang) + gy_*math.sin(ang)) * 22, 0, 1)
    v = np.clip((0.28 + 0.5*n) * (0.5 + 0.8*shade), 0, 1)
    yy, xx = np.mgrid[0:h, 0:w]
    lx, ly = w*rng.uniform(.1,.9), h*rng.uniform(.1,.6)
    fall = np.clip(1.3 - np.sqrt(((xx-lx)/(w*.75))**2 + ((yy-ly)/(h*.75))**2), .12, 1.25)
    v = np.clip(v * fall, 0, 1)
    tint = np.array([1.0, .96, .89]) if seed % 2 else np.array([.90, .94, 1.0])
    a = (v[..., None] * 240) * tint[None, None, :]
    kind = seed % 3
    if kind == 0:
        wx, wy = w*rng.uniform(.14,.58), h*rng.uniform(.12,.36)
        ww, wh = w*rng.uniform(.2,.32), h*rng.uniform(.26,.46)
        m = (xx>wx)&(xx<wx+ww)&(yy>wy)&(yy<wy+wh)
        a = np.where(m[..., None], np.minimum(a*2.4, 252), a)
        for fx in np.linspace(wx, wx+ww, 4):
            a[int(wy):int(wy+wh), int(fx)-2:int(fx)+2] *= .25
        a[int(wy+wh/2)-2:int(wy+wh/2)+2, int(wx):int(wx+ww)] *= .25
    elif kind == 1:
        m = figure(h, w, int(w*rng.uniform(.3,.7)), int(h*.94), h*rng.uniform(.5,.72), seed+9)
        a = np.where(m[..., None], a*0.13, a)
    else:
        ox, oy = w*rng.uniform(.1,.6), h*rng.uniform(.2,.48)
        ow, oh = w*rng.uniform(.22,.4), h*rng.uniform(.3,.5)
        sx = np.clip(1-np.abs(xx-(ox+ow/2))/(ow/2),0,1); sy = np.clip(1-np.abs(yy-(oy+oh/2))/(oh/2),0,1)
        soft = np.clip(np.minimum(sx,sy)*11,0,1) ** .8
        a = a * (1 - soft[..., None]*0.84)
    return finish(a, seed, grain=5.5, vig=0.6, warm=1.02)

# ---------------------------------------------------------------- build
JOBS = [
 ("hero.jpg",     2560, 1080, scene_wide,   11, {}),

 # FILMS — anamorphic, one per reel
 ("film-01.jpg",  2400, 1004, scene_wide,   61, {}),
 ("film-02.jpg",  2400, 1004, scene_wide,   62, {}),
 ("film-03.jpg",  2400, 1004, scene_wide,   63, {}),
 ("film-04.jpg",  2400, 1004, scene_wide,   64, {}),

 # STORIES — reportage
 ("story-01.jpg", 2000, 1330, scene_report, 71, {}),
 ("story-02.jpg", 2000, 1330, scene_report, 72, {}),
 ("story-03.jpg", 2000, 1330, scene_report, 73, {}),
 ("story-04.jpg", 1400,  930, scene_report, 74, {}),
 ("story-05.jpg", 1400,  930, scene_report, 75, {}),

 # FRAMES — single stills
 ("frame-01.jpg", 1800, 1350, scene_still,  81, {}),
 ("frame-02.jpg", 1800, 1350, scene_still,  82, {}),
 ("frame-03.jpg", 1800, 1350, scene_still,  83, {}),
 ("frame-04.jpg", 1800, 1350, scene_still,  84, {}),

 # the rest of the site
 ("w01.jpg",      1700, 1700, scene_still,  21, {}),
 ("w02.jpg",      1700, 1700, scene_report, 22, {}),
 ("w03.jpg",      1700, 1700, scene_wide,   23, {}),
 ("w04.jpg",      2000, 1200, scene_report, 24, {}),
 ("w05.jpg",      1700, 1700, scene_still,  25, {}),
 ("w06.jpg",      1700, 1700, scene_report, 26, {}),
 ("w07.jpg",      1400, 2100, scene_still,  27, {}),
 ("w08.jpg",      1700, 1700, scene_wide,   28, {}),
 ("w09.jpg",      1700, 1700, scene_report, 29, {}),
 ("w10.jpg",      2000, 1200, scene_wide,   30, {}),
 ("w11.jpg",      1700, 1700, scene_report, 31, {}),
 ("w12.jpg",      1700, 1700, scene_still,  32, {}),
 ("portrait.jpg", 1300, 1625, scene_report, 51, {}),
]

if __name__ == "__main__":
    for name, w, h, fn, seed, kw in JOBS:
        im = fn(w, h, seed, **kw)
        im.save(OUT / name, quality=84, optimize=True, progressive=True)
        print(name, im.size, (OUT / name).stat().st_size // 1024, "kb")
    print("\ndone —", len(JOBS), "plates")
