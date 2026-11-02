#!/usr/bin/env python3
"""analyze-entropy-analyzer wordmark banner: sequoia grove at canopy filtered noon, fallen giant cut face centre,
fire scars at irregular intervals, title branded in Autour One in an arc along the outer bark edge only."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
random.seed(71)
V1 = "--v1" in sys.argv
W, H = 1200, 420
GREEN = (44, 92, 52); LIME = (150, 210, 90); MAGENTA = (206, 62, 150); WOOD = (216, 188, 140)
img = Image.new("RGB", (W, H), (26, 44, 28)); d = ImageDraw.Draw(img, "RGBA")
# standing trunks both sides rising out of the top
for (x, w) in [(10, 92), (130, 64), (1010, 78), (1120, 96), (930, 48)]:
    d.rectangle([x, 0, x + w, 360], fill=(94, 64, 40))
    for ly in range(8, 350, 24):
        d.line([(x + 7, ly), (x + w - 9, ly + 9)], fill=(72, 48, 30), width=3)
# canopy coins of light
for _ in range(120):
    x, y = random.uniform(0, W), random.uniform(0, 90); r = random.uniform(8, 26)
    d.ellipse([x - r, y - r * .6, x + r, y + r * .6], fill=random.choice([(40, 76, 40), (54, 96, 50)]))
# clearing floor with ferns and seed pods in foreground
d.rectangle([0, 330, W, H], fill=(98, 80, 52))
for _ in range(600):
    x, y = random.uniform(0, W), random.uniform(330, H); d.point((x, y), fill=random.choice([(124, 104, 68), (84, 68, 44)]))
for _ in range(26):
    x, y = random.uniform(20, 1180), random.uniform(352, 408)
    d.ellipse([x, y, x + 12, y + 5], fill=(146, 112, 66), outline=(110, 84, 48))
def fern(x, y, ang, ln):
    for i in range(13):
        t = i / 13; bx, by = x + math.cos(ang) * ln * t, y + math.sin(ang) * ln * t - 20 * math.sin(t * 3); s = 17 * (1 - t * .7)
        d.line([(bx, by), (bx - s, by - s * .5)], fill=(52, 118, 58), width=3); d.line([(bx, by), (bx + s * .4, by - s)], fill=(62, 132, 66), width=3)
fern(6, 416, -0.5, 210); fern(1194, 416, -2.6, 210); fern(300, 420, -0.8, 130)
# fallen giant: horizontal trunk body with the cut face dominating middle distance
d.rectangle([330, 236, 870, 330], fill=(96, 66, 40))
for ly in range(244, 324, 18):
    d.line([(340, ly), (860, ly + 6)], fill=(74, 50, 30), width=3)
cx, cy, R = 600, 208, 138
for r in range(R, 8, -8):
    col = WOOD if (r // 8) % 2 == 0 else (190, 156, 106)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(148, 116, 74))
d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(116, 84, 50))
for (ang, rr) in [(24, 108), (96, 78), (168, 122), (232, 88), (306, 100)]:
    a = math.radians(ang); x2, y2 = cx + math.cos(a) * rr, cy + math.sin(a) * rr; x1, y1 = cx + math.cos(a) * (rr - 44), cy + math.sin(a) * (rr - 44)
    d.polygon([(x1, y1), (x2 - 10, y2 - 6), (x2 + 10, y2 + 6)], fill=(20, 16, 12))
    d.line([(x1, y1), (x2, y2)], fill=LIME, width=2)
for _ in range(22):  # brightest coins on the ring face
    x, y = random.uniform(cx - 120, cx + 120), random.uniform(cy - 110, cy + 110); r = random.uniform(5, 15)
    d.ellipse([x - r, y - r * .6, x + r, y + r * .6], fill=(250, 244, 190, 52))
# orchid magenta blooms on a fallen branch at left edge, lime new growth picked up faintly
d.line([(0, 286), (180, 318)], fill=(84, 56, 34), width=13)
for i in range(7):
    x, y = 18 + i * 24, 276 - math.sin(i) * 7
    d.ellipse([x - 8, y - 6, x + 8, y + 6], fill=MAGENTA); d.ellipse([x - 3, y - 2, x + 3, y + 2], fill=(242, 176, 214))
d.rectangle([0, 326, W, 334], fill=(120, 180, 80))
# title branded letter by letter in an arc along the cut face outer bark edge
try:
    f = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/AutourOne.ttf", 16)
except Exception:
    f = ImageFont.load_default()
name = "analyze-entropy-analyzer"
if not V1:
    n = len(name); a_start, a_end = 200, 340
    for i, ch in enumerate(name):
        a = math.radians(a_start + (a_end - a_start) * (i / max(1, n - 1)))
        x, y = cx + math.cos(a) * (R - 13), cy + math.sin(a) * (R - 13)
        d.text((x, y), ch, font=f, fill=(52, 34, 18), anchor="mm")
else:
    d.text((600, 386), name, font=f, fill=(52, 34, 18), anchor="mm")  # v1 flaw: straight line on the floor, not the bark arc
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = "scratch/banner-v1.png" if V1 else "banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
