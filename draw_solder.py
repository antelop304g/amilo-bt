from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1600, 2360
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def f(size, bold=False):
    return ImageFont.truetype(FONT, size, index=1 if bold else 0)


RED = (220, 40, 40)
BLUE = (30, 110, 220)
GRAY = (120, 120, 120)
DARK = (30, 30, 30)
GREEN = (20, 150, 70)
GOLD = (212, 170, 80)
BOARD = (22, 24, 28)
SILVER = (190, 195, 200)


def text(xy, s, size=26, fill=DARK, bold=False, anchor="la"):
    d.text(xy, s, font=f(size, bold), fill=fill, anchor=anchor)


def arrow(p1, p2, fill=DARK, width=4, head=16):
    d.line([p1, p2], fill=fill, width=width)
    ang = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    a1 = ang + math.radians(150)
    a2 = ang - math.radians(150)
    d.polygon([p2,
               (p2[0] + head * math.cos(a1), p2[1] + head * math.sin(a1)),
               (p2[0] + head * math.cos(a2), p2[1] + head * math.sin(a2))], fill=fill)


def panel(x0, y0, x1, y1, title):
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, outline=(200, 200, 200), width=3)
    text((x0 + 24, y0 + 18), title, 34, DARK, bold=True)


def cross(cx, cy, r, fill=RED, width=6):
    d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=fill, width=width)
    d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=fill, width=width)


def check(cx, cy, r, fill=GREEN, width=7):
    d.line([(cx - r, cy), (cx - r * 0.3, cy + r * 0.7), (cx + r, cy - r * 0.7)], fill=fill, width=width)


# ---------- 标题 ----------
text((W // 2, 40), "ESP32-S3 SuperMini 焊接示意", 52, DARK, bold=True, anchor="ma")
text((W // 2, 110), "只焊 5V、GND 两个孔 · 旧 USB 线的红、黑线直接焊进孔", 32, RED, bold=True, anchor="ma")

# ---------- ① 认孔 ----------
panel(40, 170, 800, 1010, "① 认孔（板子背面，Type-C 朝上）")
bx, by, bw, bh = 290, 330, 400, 520
pitch = 56
# Type-C
d.rounded_rectangle([bx + 120, by - 50, bx + 280, by + 30], radius=14, fill=SILVER, outline=(140, 140, 140), width=2)
text((bx + 200, by - 38), "Type-C", 22, DARK, anchor="ma")
d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=16, fill=BOARD)
left = ["5V", "GND", "3V3", "13", "12", "11", "10", "9", "8"]
right = ["TX", "RX", "1", "2", "3", "4", "5", "6", "7"]
for i in range(9):
    yy = by + 36 + i * pitch
    for side, labels in ((0, left), (1, right)):
        cx = bx + 30 if side == 0 else bx + bw - 30
        lab = labels[i]
        ring = GOLD
        if side == 0 and i == 0:
            ring = RED
        elif side == 0 and i == 1:
            ring = BLUE
        d.ellipse([cx - 20, yy - 20, cx + 20, yy + 20], fill=ring)
        d.ellipse([cx - 9, yy - 9, cx + 9, yy + 9], fill=(250, 250, 250))
        lx = cx + 34 if side == 0 else cx - 34
        text((lx, yy), lab, 22, (230, 230, 230), anchor="lm" if side == 0 else "rm")
text((bx + bw // 2, by + bh - 80), "Super Mini", 24, (200, 200, 200), anchor="ma")
text((bx + bw // 2, by + bh - 48), "ESP32-S3", 24, (200, 200, 200), anchor="ma")
text((bx + 200, by + 70), "B+  B-", 20, (170, 170, 170), anchor="ma")

# 高亮框和标注
y5, yg, y3 = by + 36, by + 36 + pitch, by + 36 + 2 * pitch
d.rounded_rectangle([bx + 4, y5 - 26, bx + 110, yg + 26], radius=10, outline=(255, 200, 0), width=5)
arrow((bx - 90, y5), (bx + 4, y5), RED, 5)
text((bx - 96, y5), "5V", 34, RED, bold=True, anchor="rm")
text((bx - 96, y5 + 34), "红线", 24, RED, anchor="rm")
arrow((bx - 90, yg + 22), (bx + 4, yg + 8), BLUE, 5)
text((bx - 96, yg + 28), "GND", 34, BLUE, bold=True, anchor="rm")
text((bx - 96, yg + 62), "黑线", 24, BLUE, anchor="rm")
cross(bx + 30, y3, 17, RED, 6)
text((bx - 96, y3 + 60), "3V3 别焊！", 26, RED, bold=True, anchor="rm")
text((bx - 96, y3 + 92), "接错会烧板", 22, RED, anchor="rm")
text((bx + 200, by + 100), "电池焊盘 不用管", 20, (170, 170, 170), anchor="ma")

text((70, 890), "· 5V 和 GND 挨在一起，就在 Type-C 旁边第 1、2 个孔", 24, DARK)
text((70, 930), "· 板子正面（芯片那面）同样位置也印着 5V / GND", 24, DARK)
text((70, 970), "· 右边 TX、RX 和其他数字孔全部不焊", 24, DARK)

# ---------- ② 掰 2 针 ----------
panel(820, 170, 1560, 560, "② 排针（直接焊线的话跳过②③）")
hx, hy = 880, 370
for i in range(9):
    px = hx + i * 70
    col = DARK if i < 2 else (150, 150, 150)
    d.rectangle([px, hy, px + 64, hy + 40], fill=col)
    d.rectangle([px + 27, hy - 70, px + 37, hy], fill=GOLD)
    d.rectangle([px + 27, hy + 40, px + 37, hy + 80], fill=GOLD)
cut = hx + 2 * 70 - 3
d.line([(cut, hy - 95), (cut, hy + 105)], fill=RED, width=4)
text((cut, hy - 128), "在这里掰断", 24, RED, bold=True, anchor="ma")
text((hx + 67, hy + 100), "要这 2 针", 24, DARK, bold=True, anchor="ma")
text((850, 510), "用尖嘴钳夹住，沿缝掰一下就断，剩下的留着备用", 24, DARK)

# ---------- ③ 插针方向 ----------
panel(820, 580, 1560, 1010, "③ 插针方向（侧面看，同上可跳过）")
sx, sy = 960, 730
# 板子
d.rectangle([sx, sy, sx + 460, sy + 24], fill=BOARD)
text((sx + 470, sy + 12), "板子", 24, DARK, anchor="lm")
text((sx + 230, sy - 80), "背面朝上（有 5V/GND 字的那面）", 22, GRAY, anchor="ma")
# 两根针
for k, px in enumerate([sx + 60, sx + 116]):
    d.rectangle([px - 5, sy - 22, px + 5, sy + 24], fill=GOLD)   # 短针露出
    d.rectangle([px - 5, sy + 24 + 30, px + 5, sy + 24 + 30 + 120], fill=GOLD)  # 长针
    # 焊点
    d.polygon([(px - 22, sy), (px + 22, sy), (px + 6, sy - 26), (px - 6, sy - 26)], fill=(185, 190, 195))
d.rectangle([sx + 30, sy + 24, sx + 146, sy + 54], fill=DARK)
text((sx + 170, sy - 10), "← 焊点在背面", 24, RED, bold=True, anchor="lm")
text((sx + 170, sy + 40), "← 黑色塑料贴住正面", 22, DARK, anchor="lm")
text((sx + 170, sy + 120), "← 长针朝正面，", 22, DARK, anchor="lm")
text((sx + 170, sy + 152), "   以后插杜邦线", 22, DARK, anchor="lm")
text((850, 930), "小技巧：长针插进泡沫/海绵立住，或用胶带固定，", 22, DARK)
text((850, 964), "保证针和板子垂直，再开始焊", 22, DARK)

# ---------- ④ 焊接动作 ----------
panel(40, 1030, 1560, 1470, "④ 焊接动作（每个孔 2～3 秒）")
steps = [
    ("1 烙铁头同时贴住", "焊盘和针，停 1～2 秒"),
    ("2 焊锡丝从另一侧", "碰焊盘，熔化一点就撤"),
    ("3 再撤烙铁", "静置 3 秒别动"),
]
for i, (a, b) in enumerate(steps):
    ox = 110 + i * 480
    oy = 1110
    # 板子剖面
    d.rectangle([ox, oy + 150, ox + 320, oy + 170], fill=BOARD)
    d.rectangle([ox + 140, oy + 150, ox + 180, oy + 170], fill=GOLD)
    d.rectangle([ox + 155, oy + 95, ox + 165, oy + 230], fill=GOLD)
    if i == 0 or i == 1:
        # 烙铁
        d.polygon([(ox + 10, oy + 20), (ox + 40, oy), (ox + 150, oy + 140), (ox + 138, oy + 152)], fill=(90, 90, 95))
        text((ox + 0, oy - 20), "烙铁", 22, GRAY)
    if i == 1:
        d.line([(ox + 300, oy + 10), (ox + 178, oy + 142)], fill=(200, 200, 205), width=8)
        text((ox + 250, oy - 20), "焊锡丝", 22, GRAY)
    if i == 2:
        d.polygon([(ox + 128, oy + 150), (ox + 192, oy + 150), (ox + 168, oy + 100), (ox + 152, oy + 100)], fill=(190, 195, 200))
        check(ox + 260, oy + 80, 26)
    text((ox + 160, oy + 250), a, 26, DARK, bold=True, anchor="ma")
    text((ox + 160, oy + 290), b, 24, DARK, anchor="ma")
    if i < 2:
        arrow((ox + 360, oy + 160), (ox + 440, oy + 160), GRAY, 5)
text((80, 1428), "烙铁温度 330～350℃ · 用 0.8mm 含松香焊锡丝 · 焊接时板子不要插任何线", 24, RED, bold=True)

# ---------- ⑤ 检查 ----------
panel(40, 1490, 1560, 1860, "⑤ 焊完检查")
checks = [
    ("好焊点", "亮、像小山包（圆锥）", True, "cone"),
    ("虚焊", "锡成球、没吃进焊盘 → 补焊", False, "ball"),
    ("连锡（最危险）", "5V 和 GND 连在一起 = 短路", False, "bridge"),
]
for i, (title, desc, ok, kind) in enumerate(checks):
    ox = 110 + i * 480
    oy = 1575
    d.rectangle([ox, oy + 90, ox + 320, oy + 110], fill=BOARD)
    pins = [ox + 110, ox + 210]
    for px in pins:
        d.rectangle([px - 16, oy + 90, px + 16, oy + 110], fill=GOLD)
        d.rectangle([px - 5, oy + 30, px + 5, oy + 90], fill=GOLD)
    if kind == "cone":
        for px in pins:
            d.polygon([(px - 18, oy + 90), (px + 18, oy + 90), (px + 6, oy + 55), (px - 6, oy + 55)], fill=(190, 195, 200))
    elif kind == "ball":
        for px in pins:
            d.ellipse([px - 16, oy + 42, px + 16, oy + 74], fill=(190, 195, 200))
    else:
        d.rounded_rectangle([pins[0] - 20, oy + 55, pins[1] + 20, oy + 90], radius=12, fill=(190, 195, 200))
    if ok:
        check(ox + 290, oy + 20, 24)
    else:
        cross(ox + 290, oy + 20, 18)
    text((ox + 160, oy + 140), title, 28, GREEN if ok else RED, bold=True, anchor="ma")
    text((ox + 160, oy + 182), desc, 24, DARK, anchor="ma")
text((80, 1812), "连锡了：烙铁加热，在两针之间划一下把锡带走；有吸锡带更方便", 24, DARK)

# ---------- ⑥ 最终接线 ----------
panel(40, 1880, 1560, 2320, "⑥ 接线（旧 USB-A 线剪开，红、黑线直接焊进孔）")
cy = 2080
# 充电器
d.rounded_rectangle([80, cy - 70, 230, cy + 70], radius=16, fill=(240, 240, 240), outline=DARK, width=3)
text((155, cy - 12), "手机", 24, DARK, anchor="ma")
text((155, cy + 20), "充电器", 24, DARK, anchor="ma")
d.rectangle([230, cy - 22, 280, cy + 22], fill=SILVER)
text((255, cy - 50), "USB-A 头", 20, GRAY, anchor="ma")
# 线
d.line([(280, cy - 8), (560, cy - 60)], fill=RED, width=8)
d.line([(280, cy + 8), (560, cy - 4)], fill=DARK, width=8)
d.line([(280, cy + 4), (420, cy + 70)], fill=(230, 230, 230), width=6)
d.line([(280, cy + 12), (420, cy + 90)], fill=GREEN, width=6)
text((290, cy + 118), "白、绿线/屏蔽层剪短包胶带", 22, GRAY, anchor="la")
text((420, cy - 105), "红→焊进 5V", 24, RED, bold=True, anchor="ma")
text((480, cy + 22), "黑→焊进 GND", 24, DARK, bold=True, anchor="ma")
# 板子
px0 = 560
d.rounded_rectangle([px0, cy - 110, px0 + 260, cy + 110], radius=12, fill=BOARD)
d.ellipse([px0 - 10, cy - 70, px0 + 14, cy - 46], fill=RED)
d.ellipse([px0 - 10, cy - 14, px0 + 14, cy + 10], fill=BLUE)
text((px0 + 30, cy - 58), "5V", 22, (230, 230, 230), anchor="lm")
text((px0 + 30, cy - 2), "GND", 22, (230, 230, 230), anchor="lm")
text((px0 + 130, cy + 60), "ESP32-S3", 24, (220, 220, 220), anchor="ma")
d.rounded_rectangle([px0 + 260, cy - 30, px0 + 300, cy + 30], radius=8, fill=SILVER)
text((px0 + 280, cy - 62), "Type-C", 20, GRAY, anchor="ma")
# OTG
d.rounded_rectangle([px0 + 300, cy - 36, px0 + 440, cy + 36], radius=10, fill=(90, 90, 95))
text((px0 + 370, cy - 14), "OTG", 22, (240, 240, 240), anchor="ma")
text((px0 + 370, cy + 50), "C 公 → USB-A 母", 20, GRAY, anchor="ma")
# 键盘线
d.line([(px0 + 440, cy), (px0 + 620, cy)], fill=DARK, width=8)
text((px0 + 530, cy - 40), "键盘原配线", 22, GRAY, anchor="ma")
d.rounded_rectangle([px0 + 620, cy - 80, px0 + 940, cy + 80], radius=16, fill=(245, 245, 245), outline=DARK, width=3)
for r in range(3):
    for c in range(8):
        kx = px0 + 640 + c * 36
        ky = cy - 60 + r * 40
        d.rounded_rectangle([kx, ky, kx + 30, ky + 32], radius=5, outline=GRAY, width=2)
text((px0 + 780, cy + 92), "熊猫 87 键盘", 24, DARK, anchor="ma")

text((80, 2240), "剥线：外皮剥 3cm，红黑线各剥 3mm 先上锡 · 颜色不是红黑先别接 · 线全接好再插充电器", 24, RED, bold=True)
text((80, 2276), "键盘灯亮 → 电脑蓝牙连 Amilo-BT → 打字测试", 24, DARK)

out = "/Volumes/M_SEC/develop/cs_no_repo/esp32/焊接示意.png"
img.save(out)
print(out)
