#!/usr/bin/env python3
"""Robotics-themed pixel banner for Awesome Craft Robotics. Original scene, no brand marks."""
import random
from pathlib import Path

random.seed(7)
P = 8
W = 100
H = 34  # 800x272
out = []


def r(x, y, w, h, c, cls=None, extra=""):
    a = f' class="{cls}"' if cls else ""
    out.append(
        f'<rect x="{x*P}" y="{y*P}" width="{w*P}" height="{h*P}" fill="{c}"{a}{extra}/>'
    )


# 3x5 pixel font
F = {
    "A": ["010", "101", "111", "101", "101"],
    "B": ["110", "101", "110", "101", "110"],
    "C": ["011", "100", "100", "100", "011"],
    "F": ["111", "100", "110", "100", "100"],
    "I": ["111", "010", "010", "010", "111"],
    "O": ["010", "101", "101", "101", "010"],
    "R": ["110", "101", "110", "101", "101"],
    "S": ["011", "100", "010", "001", "110"],
    "T": ["111", "010", "010", "010", "010"],
    " ": ["000", "000", "000", "000", "000"],
}

style = """
<style>
.tw{animation:tw 2.4s steps(2) infinite}
.tw2{animation:tw 3.1s steps(2) infinite .8s}
.tw3{animation:tw 1.9s steps(2) infinite 1.4s}
@keyframes tw{0%,100%{opacity:1}50%{opacity:.15}}
.blink{animation:tw 1s steps(1) infinite}
.glow{animation:glow 1.4s steps(3) infinite}
@keyframes glow{0%,100%{opacity:.35}50%{opacity:1}}
.bob{animation:bob 1.2s steps(2) infinite}
.bob2{animation:bob 1.2s steps(2) infinite .3s}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.leg{animation:leg .6s steps(2) infinite}
.leg2{animation:leg .6s steps(2) infinite .3s}
@keyframes leg{0%,100%{opacity:1}50%{opacity:0}}
.arm{transform-box:fill-box;transform-origin:top center;animation:arm .8s steps(2) infinite}
.arm2{transform-box:fill-box;transform-origin:top center;animation:arm .8s steps(2) infinite .4s}
@keyframes arm{0%,100%{transform:rotate(-18deg)}50%{transform:rotate(18deg)}}
.pace{animation:pace 6s steps(12) infinite}
@keyframes pace{0%{transform:translateX(0)}50%{transform:translateX(48px)}100%{transform:translateX(0)}}
.waddle{animation:waddle 1.6s steps(4) infinite}
@keyframes waddle{0%,100%{transform:translateX(0)}25%{transform:translateX(8px)}75%{transform:translateX(-8px)}}
.led{animation:led 1.2s steps(2) infinite}
.led2{animation:led 1.6s steps(2) infinite .4s}
@keyframes led{0%,100%{opacity:1}50%{opacity:.2}}
</style>
"""

# Evening lab sky
sky = ["#071018", "#0a1620", "#0e1e2c", "#122536", "#162d40", "#1a3548", "#1e3d52"]
for i, c in enumerate(sky):
    r(0, i * 4, W, 4, c)

# Sparse stars, keep the title band clear
for i in range(24):
    while True:
        x = random.randrange(W)
        y = random.randrange(10)
        if not (18 <= x <= 82 and y <= 8):
            break
    r(x, y, 1, 1, random.choice(["#7dd3fc", "#fff7c2", "#86efac"]), random.choice(["tw", "tw2", "tw3"]))

# Soft moon, far right
r(91, 3, 5, 5, "#1e3a4c")
r(92, 4, 3, 3, "#cbd5e1")
r(93, 5, 1, 1, "#f8fafc")

# Title: CRAFT ROBOTICS
t = "CRAFT ROBOTICS"
tx = (W - len(t) * 4) // 2
ty = 2
for k, ch in enumerate(t):
    for yy, row in enumerate(F[ch]):
        for xx, b in enumerate(row):
            if b == "1":
                r(tx + k * 4 + xx + 0.25, ty + yy + 0.25, 1, 1, "#000", None, ' opacity=".55"')
                r(tx + k * 4 + xx, ty + yy, 1, 1, "#5eead4")

# Distant workbench / shelf on the left (no logos)
r(2, 18, 14, 1, "#334155")
r(3, 14, 12, 4, "#1e293b")
r(4, 15, 2, 2, "#fbbf24", "glow")  # toolbox lamp
r(8, 16, 3, 2, "#334155")
r(12, 15, 2, 3, "#475569")
r(6, 19, 2, 7, "#1f2937")  # legs
r(12, 19, 2, 7, "#1f2937")

# Floor
for x in range(W):
    r(x, 26, 1, 1, "#0ea5e9" if x % 5 == 0 else "#164e63")
    r(x, 27, 1, 1, "#0f172a" if x % 2 else "#1e293b")
    for y in range(28, H):
        r(x, y, 1, 1, "#0b1220" if (x + y) % 4 else "#111827")


# --- Small duck biped (left-centre), original design, no wordmarks ---
out.append('<g class="waddle">')
# body / hull
r(24, 18, 6, 5, "#f4d19a")
r(25, 19, 4, 3, "#f8e3bf")
# head
r(28, 14, 4, 4, "#f4d19a")
r(29, 15, 2, 2, "#f8e3bf")
r(31, 16, 1, 1, "#0f172a")  # eye
# beak
r(32, 16, 2, 1, "#f97316")
r(33, 17, 1, 1, "#ea580c")
# crest
r(29, 13, 2, 1, "#fb923c")
# feet (alternating)
r(25, 23, 2, 2, "#f97316", "leg")
r(28, 23, 2, 2, "#f97316", "leg2")
# hidden second pose for the step
r(25, 24, 2, 1, "#c2410c", "leg2")
r(28, 24, 2, 1, "#c2410c", "leg")
# tiny status LED on the chest
r(26, 20, 1, 1, "#22c55e", "led")
out.append("</g>")


# --- Quadruped dog (centre), original design ---
out.append('<g class="bob2">')
# torso
r(46, 18, 9, 4, "#94a3b8")
r(47, 19, 7, 2, "#cbd5e1")
# head
r(54, 16, 4, 4, "#94a3b8")
r(55, 17, 2, 2, "#e2e8f0")
r(57, 17, 1, 1, "#0f172a")  # eye
r(58, 18, 2, 1, "#64748b")  # snout
# ear
r(54, 15, 1, 2, "#64748b")
# tail
r(44, 18, 2, 1, "#64748b", "bob")
# legs (front/back alternating)
r(47, 22, 1, 3, "#64748b", "leg")
r(49, 22, 1, 3, "#475569", "leg2")
r(52, 22, 1, 3, "#64748b", "leg2")
r(54, 22, 1, 3, "#475569", "leg")
# back LED
r(50, 19, 1, 1, "#38bdf8", "led2")
out.append("</g>")


# --- Humanoid walking past (right) ---
out.append('<g class="pace">')
# head
r(72, 12, 3, 3, "#e2e8f0")
r(73, 13, 1, 1, "#0f172a")  # visor / eye
# torso
r(72, 15, 3, 5, "#64748b")
r(73, 16, 1, 3, "#94a3b8")
# backpack / compute
r(71, 16, 1, 3, "#334155")
# arms (swing)
r(70, 16, 2, 1, "#94a3b8", "arm")
r(70, 17, 1, 3, "#64748b", "arm")
r(75, 16, 2, 1, "#94a3b8", "arm2")
r(76, 17, 1, 3, "#64748b", "arm2")
# legs
r(72, 20, 1, 5, "#475569", "leg")
r(74, 20, 1, 5, "#334155", "leg2")
# chest LED
r(73, 17, 1, 1, "#22c55e", "led")
out.append("</g>")

# Floor marks under the walkers
r(24, 26, 12, 1, "#155e75")
r(46, 26, 14, 1, "#155e75")
r(68, 26, 16, 1, "#155e75")

# Status bar
out.append(
    f'<text x="{8}" y="{H*P-8}" font-family="monospace" font-size="12" fill="#5eead4">'
    f"&gt; open-source robots, ready to train"
    f'<tspan class="blink">_</tspan></text>'
)

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W*P} {H*P}" '
    f'width="{W*P}" height="{H*P}" shape-rendering="crispEdges">'
    + style
    + "".join(out)
    + "</svg>"
)

dest = Path(__file__).resolve().parent / "assets" / "craft-robotics.svg"
dest.write_text(svg)
print(f"wrote {dest} ({dest.stat().st_size} bytes)")
