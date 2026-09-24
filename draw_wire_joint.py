from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1600, 1560
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)
FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"

RED = (220, 40, 40)
WHITE_WIRE = (235, 235, 235)
GRAY = (120, 120, 120)
DARK = (30, 30, 30)
GREEN = (20, 150, 70)
GOLD = (212, 170, 80)
COPPER = (205, 120, 60)
SOLDER = (185, 190, 196)
BOARD = (22, 24, 28)
SILVER = (190, 195, 200)
TAPE = (250, 220, 120)


def f(size, bold=False):
    return ImageFont.truetype(FONT, size, index=1 if bold else 0)


def text(xy, s, size=26, fill=DARK, bold=False, anchor="la"):
    d.text(xy, s, font=f(size, bold), fill=fill, anchor=anchor)


def panel(x0, y0, x1, y1, title, color=DARK):
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, outline=(200, 200, 200), width=3)
    text((x0 + 24, y0 + 18), title, 34, color, bold=True)


def check(cx, cy, r, fill=GREEN, width=7):
    d.line([(cx - r, cy), (cx - r * 0.3, cy + r * 0.7), (cx + r, cy - r * 0.7)], fill=fill, width=width)


def cross(cx, cy, r, fill=RED, width=7):
    d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=fill, width=width)
    d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=fill, width=width)


def wire_outline(points, fill, width):
    d.line(points, fill=(150, 150, 150), width=width + 4, joint="curve")
    d.line(points, fill=fill, width=width, joint="curve")


text((W // 2, 36), "线怎么焊到板子上 · 焊好后的样子", 50, DARK, bold=True, anchor="ma")
text((W // 2, 104), "推荐：不用排针，线头直接穿孔焊住", 32, GREEN, bold=True, anchor="ma")

# ---------- ① 侧面看 ----------
panel(40, 160, 800, 820, "① 侧面看（推荐做法）", GREEN)
bx0, bx1, by = 110, 730, 360
d.rectangle([bx0, by, bx1, by + 30], fill=BOARD)
text((bx1 - 10, by - 36), "背面（有字那面）朝上", 22, GRAY, anchor="ra")
text((bx1 - 10, by + 44), "正面（芯片那面）", 22, GRAY, anchor="ra")
for cx, col, name in ((300, RED, "红线"), (420, WHITE_WIRE, "白线")):
    d.rectangle([cx - 14, by, cx + 14, by + 30], fill=GOLD)
    # 铜丝穿过孔，从背面露出 1mm
    d.rectangle([cx - 5, by - 18, cx + 5, by + 60], fill=COPPER)
    # 焊点
    d.polygon([(cx - 26, by), (cx + 26, by), (cx + 8, by - 34), (cx - 8, by - 34)], fill=SOLDER)
    # 绝缘皮从正面下方引出
    wire_outline([(cx, by + 60), (cx, by + 170), (cx - 30, by + 240)], col, 16)
    text((cx - 30, by + 256), name, 24, RED if col == RED else DARK, bold=True, anchor="ma")
d.line([(300, by - 60), (300, by - 40)], fill=DARK, width=3)
text((300, by - 100), "焊点：亮、小山包", 24, GREEN, bold=True, anchor="ma")
text((560, by + 110), "← 绝缘皮贴近板子", 22, DARK, anchor="la")
text((560, by + 142), "   只露 1～2mm 铜丝", 22, DARK, anchor="la")
text((90, 700), "· 线从正面穿进孔，铜丝头从背面冒出一点", 24, DARK)
text((90, 740), "· 在背面上锡，锡把铜丝和金色焊盘包住", 24, DARK)
text((90, 780), "· 冒出来太长的铜丝，焊完用剪刀剪掉", 24, DARK)

# ---------- ② 背面看 ----------
panel(820, 160, 1560, 820, "② 背面看（焊好后）", GREEN)
ox, oy, ow, oh = 1010, 300, 360, 440
d.rounded_rectangle([ox + 110, oy - 44, ox + 250, oy + 20], radius=12, fill=SILVER)
text((ox + 180, oy - 34), "Type-C", 20, DARK, anchor="ma")
d.rounded_rectangle([ox, oy, ox + ow, oy + oh], radius=14, fill=BOARD)
pitch = 48
labels_l = ["5V", "GND", "3V3", "13", "12", "11", "10", "9"]
labels_r = ["TX", "RX", "1", "2", "3", "4", "5", "6"]
for i in range(8):
    yy = oy + 34 + i * pitch
    for side in (0, 1):
        cx = ox + 28 if side == 0 else ox + ow - 28
        d.ellipse([cx - 16, yy - 16, cx + 16, yy + 16], fill=GOLD)
        if not (side == 0 and i < 2):
            d.ellipse([cx - 7, yy - 7, cx + 7, yy + 7], fill=(250, 250, 250))
        lab = labels_l[i] if side == 0 else labels_r[i]
        text((cx + 26, yy) if side == 0 else (cx - 26, yy), lab, 20, (220, 220, 220),
             anchor="lm" if side == 0 else "rm")
for i in range(2):
    yy = oy + 34 + i * pitch
    cx = ox + 28
    d.ellipse([cx - 18, yy - 18, cx + 18, yy + 18], fill=SOLDER)
    d.ellipse([cx - 6, yy - 6, cx + 6, yy + 6], fill=(225, 228, 232))
# 线从板子下方引出（虚线表示在背面看不见）
for i, (col, xt, name) in enumerate(((RED, ox - 100, "红→5V"), (WHITE_WIRE, ox - 50, "白→GND"))):
    yy = oy + 34 + i * pitch
    wire_outline([(ox, yy), (xt, yy), (xt, oy + oh - 20)], col, 14)
    text((ox - 116, oy + 280 + i * 36), name, 24, RED if col == RED else DARK, bold=True, anchor="rm")
text((850, 758), "两个孔变成银色小圆包 · 中间不能连锡", 24, DARK, bold=True)
text((850, 792), "线从正面引出（背面看被板子挡住）· 用胶带固定在板边", 20, GRAY)

# ---------- ③ 也可以 ----------
panel(40, 840, 800, 1500, "③ 也可以：先焊排针，线再焊在针上")
by2 = 1010
d.rectangle([110, by2, 730, by2 + 30], fill=BOARD)
for cx, col in ((300, RED), (440, WHITE_WIRE)):
    d.rectangle([cx - 5, by2 - 16, cx + 5, by2 + 30], fill=GOLD)
    d.polygon([(cx - 24, by2), (cx + 24, by2), (cx + 7, by2 - 30), (cx - 7, by2 - 30)], fill=SOLDER)
    d.rectangle([cx - 30, by2 + 30, cx + 30, by2 + 60], fill=DARK)
    d.rectangle([cx - 5, by2 + 60, cx + 5, by2 + 190], fill=GOLD)
    for k in range(4):
        yy = by2 + 110 + k * 16
        d.arc([cx - 14, yy - 8, cx + 14, yy + 8], 0, 360, fill=COPPER, width=4)
    d.rounded_rectangle([cx - 12, by2 + 100, cx + 12, by2 + 180], radius=8, fill=SOLDER)
    wire_outline([(cx + 12, by2 + 170), (cx + 80, by2 + 230), (cx + 120, by2 + 290)], col, 14)
text((500, by2 + 100), "铜丝绕针 2～3 圈", 22, DARK, anchor="la")
text((500, by2 + 132), "再上锡焊牢", 22, DARK, anchor="la")
text((500, by2 + 164), "外面套热缩管/胶布", 22, DARK, anchor="la")
text((90, 1450), "步骤多、占地方；以后想换线方便些", 24, GRAY)

# ---------- ④ 不行 ----------
panel(820, 840, 1560, 1500, "④ 不行的做法", RED)
items = [
    ("只拧、只绑不上锡", "接触不稳，键盘时断时连"),
    ("铜丝露太长", "红白两根碰到 = 短路"),
    ("红白两个焊点连锡", "直接短路，充电器保护或烧板"),
    ("线焊到 3V3 孔", "5V 进 3.3V 会烧芯片"),
]
for i, (a, b) in enumerate(items):
    yy = 950 + i * 130
    cross(890, yy + 26, 20)
    text((930, yy), a, 28, RED, bold=True)
    text((930, yy + 42), b, 24, DARK)

out = "/Volumes/M_SEC/develop/cs_no_repo/esp32/线焊接示意.png"
img.save(out)
print(out)
