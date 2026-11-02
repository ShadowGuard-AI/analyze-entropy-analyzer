#!/usr/bin/env python3
"""analyze-entropy-analyzer logo: cross section disc straight on, concentric rings canopy green to rain black,
one fire scar wedge of charred wood healed over, single frog lime line where new growth closed over it."""
import math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
V1 = "--v1" in sys.argv
W, H = 900, 520
GREEN = (44, 92, 52); BLACK = (14, 24, 16); LIME = (150, 210, 90); PALE = (238, 240, 226)
img = Image.new("RGB", (W, H), PALE); d = ImageDraw.Draw(img, "RGBA")
cx, cy, R = 450, 196, 158
# bark rim: rough broken circle
for a in range(0, 360, 6):
    r = R + (7 if a % 24 == 0 else 2)
    x, y = cx + math.cos(math.radians(a)) * r, cy + math.sin(math.radians(a)) * r
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(70, 48, 30))
d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(196, 164, 112))
# rings: canopy green shading to rain black toward the bark (outer darker bands interleaved with wood)
for r in range(R - 6, 8, -8):
    t = r / R
    col = (int(216 - 90 * t), int(188 - 70 * t), int(140 - 52 * t)) if (r // 8) % 2 == 0 else (int(120 + 40 * t), int(140 - 30 * t), int(80 - 20 * t))
    if (r // 8) % 5 == 4:
        col = (int(52 + 30 * t), int(84 - 20 * t), int(48 - 14 * t))  # canopy green ring
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col, outline=(140, 110, 70))
d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(110, 80, 48))
# fire scar wedge: dark triangular intrusion, later rings bend around it (drawn as wedge plus bent arcs)
if not V1:
    a0, a1 = math.radians(38), math.radians(66)
    pts = [(cx, cy)]
    for a in range(38, 67, 4):
        pts.append((cx + math.cos(math.radians(a)) * (R - 4), cy + math.sin(math.radians(a)) * (R - 4)))
    d.polygon(pts, fill=(16, 13, 10))
    for r in (62, 84, 106, 128):  # rings bending around the wound
        d.arc([cx - r, cy - r, cx + r, cy + r], 68, 36 + 360, fill=(168, 138, 92), width=4)
    # single frog lime line where new growth closed over the wound, along the outer scar edge
    lime_pts = [(cx + math.cos(math.radians(a)) * (R - 10), cy + math.sin(math.radians(a)) * (R - 10)) for a in range(40, 65, 3)]
    d.line(lime_pts, fill=LIME, width=5)
    # bark rim broken at scar side
    for a in range(40, 65, 6):
        x, y = cx + math.cos(math.radians(a)) * (R + 2), cy + math.sin(math.radians(a)) * (R + 2)
        d.rectangle([x - 8, y - 5, x + 8, y + 5], fill=PALE)
try:
    f = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/AutourOne.ttf", 38)
except Exception:
    f = ImageFont.load_default()
d.text((450, 438), "analyze-entropy-analyzer", font=f, fill=GREEN, anchor="mm")
img = img.filter(ImageFilter.GaussianBlur(0.3))
out = "scratch/logo-v1.png" if V1 else "logo.png"
img.save(__file__.rsplit("/", 1)[0] + "/" + out)
if not V1:
    img.resize((64, 37)).save(__file__.rsplit("/", 1)[0] + "/scratch/logo64-ship.png")
print("saved", out)
