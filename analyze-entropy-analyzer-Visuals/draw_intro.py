#!/usr/bin/env python3
"""analyze-entropy-analyzer intro: sequoia grove clearing, cut face with rings and fire scars, no readable mark.
Fern fronds lower corners, seed pods and leaf litter foreground, orchid blooms left, lime new growth at rim."""
import math, random, sys
from PIL import Image, ImageDraw, ImageFilter
random.seed(61)
V1 = "--v1" in sys.argv
W, H = 1200, 520
GREEN = (44, 92, 52); BLACK = (16, 26, 18); LIME = (150, 210, 90); MAGENTA = (206, 62, 150); WOOD = (216, 188, 140)
img = Image.new("RGB", (W, H), (24, 40, 26)); d = ImageDraw.Draw(img, "RGBA")
# canopy closing the top, gaps letting pale light down
d.rectangle([0, 0, W, 120], fill=(28, 54, 30))
for _ in range(160):
    x, y = random.uniform(0, W), random.uniform(0, 110); r = random.uniform(10, 34)
    d.ellipse([x - r, y - r * .6, x + r, y + r * .6], fill=random.choice([(36, 70, 38), (48, 88, 46), (58, 104, 52)]))
for gx in (300, 620, 920):
    d.polygon([(gx, 0), (gx + 54, 0), (gx + 96, 430), (gx - 30, 430)], fill=(244, 240, 200, 34))  # light columns
# standing trunks rising beyond the clearing
for (x, w) in [(60, 74), (190, 56), (1010, 66), (1120, 80), (880, 44)]:
    d.rectangle([x, 40, x + w, 430], fill=(92, 62, 40))
    for ly in range(50, 420, 26):
        d.line([(x + 6, ly), (x + w - 8, ly + 8)], fill=(70, 46, 30), width=3)
# far rim: thin bright band of new growth
d.rectangle([0, 402, W, 418], fill=LIME)
d.rectangle([0, 410, W, 430], fill=(70, 130, 60))
# clearing floor
d.rectangle([0, 418, W, H], fill=(96, 78, 52))
for _ in range(900):
    x, y = random.uniform(0, W), random.uniform(418, H); d.point((x, y), fill=random.choice([(120, 100, 66), (80, 64, 42), (140, 168, 84)]))
# fallen branch left with small distant orchid blooms
d.line([(0, 368), (210, 402)], fill=(84, 56, 34), width=16)
for i in range(6 if not V1 else 2):
    x, y = 30 + i * 30, 352 - math.sin(i) * 8
    d.ellipse([x - 7, y - 5, x + 7, y + 5], fill=MAGENTA); d.ellipse([x - 3, y - 2, x + 3, y + 2], fill=(240, 170, 210))
# THE cut face, midground centre: rings from an off centre heart, dark fire scar notches at uneven intervals
cx, cy = 590, 268
for r in range(168, 8, -9):
    col = WOOD if (r // 9) % 2 == 0 else (192, 158, 108)
    d.ellipse([cx - r, cy - r * .82, cx + r, cy + r * .82], fill=col, outline=(150, 118, 76))
d.ellipse([cx - 10, cy - 8, cx + 10, cy + 8], fill=(120, 88, 54))  # heart
# fire scars: dark wedges interrupting rings
for (ang, rr) in [(28, 128), (112, 96), (196, 142), (262, 82), (322, 112)]:
    a = math.radians(ang); x2, y2 = cx + math.cos(a) * rr, cy + math.sin(a) * rr * .82
    x1, y1 = cx + math.cos(a) * (rr - 52), cy + math.sin(a) * (rr - 52) * .82
    d.polygon([(x1, y1), (x2 - 11, y2 - 7), (x2 + 11, y2 + 7)], fill=(22, 18, 14))
    d.line([(x1, y1), (x2, y2)], fill=LIME, width=2)  # healed lime edge where growth closed over
# sawn edge of the fallen trunk entering lower right, cropped before pattern can be followed
d.rectangle([930, 440, W, H], fill=(104, 72, 44))
for r in range(70, 10, -12):
    d.arc([1120 - r, 500 - r, 1120 + r, 500 + r], 90, 300, fill=(188, 156, 106), width=4)
# fern fronds arching in from both lower corners
def fern(x, y, ang, ln):
    for i in range(15):
        t = i / 15; bx, by = x + math.cos(ang) * ln * t, y + math.sin(ang) * ln * t - 26 * math.sin(t * 3)
        s = 20 * (1 - t * .7)
        d.line([(bx, by), (bx - s, by - s * .5)], fill=(52, 118, 58), width=3)
        d.line([(bx, by), (bx + s * .4, by - s)], fill=(62, 132, 66), width=3)
fern(10, 516, -0.5, 250); fern(70, 520, -0.9, 200); fern(1190, 516, -2.6, 250); fern(1130, 520, -2.2, 190)
# seed pods scattered on the clearing floor
for _ in range(34):
    x, y = random.uniform(30, 1170), random.uniform(436, 508)
    d.ellipse([x, y, x + 13, y + 5], fill=(146, 112, 66), outline=(110, 84, 48))
# coins of canopy light on the ring face
for _ in range(26):
    x, y = random.uniform(cx - 150, cx + 150), random.uniform(cy - 120, cy + 120); r = random.uniform(6, 18)
    d.ellipse([x - r, y - r * .6, x + r, y + r * .6], fill=(250, 244, 190, 46))
img = img.filter(ImageFilter.GaussianBlur(0.4))
out = "scratch/intro-v1.png" if V1 else "intro-banner.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out); print("saved", out)
