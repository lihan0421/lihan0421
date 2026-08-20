# -*- coding: utf-8 -*-
"""Build the Arturia-themed GitHub profile banner (1920x640)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 640
OUT = 'assets'
INK = (26, 34, 43)          # near-black ink
SLATE = (91, 107, 123)      # secondary text
ICE = (74, 123, 166)        # ice blue accent
ICE_SOFT = (170, 198, 224)  # soft ice blue
BG_TOP = (255, 255, 255)
BG_BOT = (238, 244, 250)    # very light ice blue

def font(path, size):
    return ImageFont.truetype(path, size)

YAHEI_B = 'C:/Windows/Fonts/msyhbd.ttc'
YAHEI = 'C:/Windows/Fonts/msyh.ttc'
ARIAL_B = 'C:/Windows/Fonts/arialbd.ttf'
CONSOLA_B = 'C:/Windows/Fonts/consolab.ttf'

# ---------- 1. background: vertical gradient ----------
bg = Image.new('RGB', (W, H))
dr = ImageDraw.Draw(bg)
for y in range(H):
    t = y / (H - 1)
    c = tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3))
    dr.line([(0, y), (W, y)], fill=c)

# ---------- 2. art on the right (full height, blends into light bg) ----------
art = Image.open('arturia.png').convert('RGB')
art_h = H
art_w = round(art.width * art_h / art.height)   # 939
art = art.resize((art_w, art_h), Image.LANCZOS)
ax = W - art_w                                   # x start of art
bg.paste(art, (ax, 0))

# ---------- 3. text block on the left ----------
dr = ImageDraw.Draw(bg)
X = 84

def text_center_y(dr, y_center, txt, fnt, fill):
    bbox = dr.textbbox((0, 0), txt, font=fnt)
    dr.text((X, y_center - (bbox[3] - bbox[1]) / 2 - bbox[1]), txt, font=fnt, fill=fill)

# 3.0 music motif line
f_motif = font(YAHEI, 34)
dr.text((X, 96), '♪  ♫  Arturia Mode  ♬  ♪', font=f_motif, fill=ICE_SOFT)
motif_w = dr.textbbox((0, 0), '♪  ♫  Arturia Mode  ♬  ♪', font=f_motif)[2]

# 3.1 name: English + Chinese
f_name_en = font(ARIAL_B, 108)
f_name_cn = font(YAHEI_B, 96)
name_y = 240
text_center_y(dr, name_y, 'Li Han', f_name_en, INK)
en_w = dr.textbbox((0, 0), 'Li Han', font=f_name_en)[2]

# thin divider between EN and CN
div_x = X + en_w + 42
dr.rectangle([div_x, name_y - 58, div_x + 4, name_y + 58], fill=ICE)
cn_x = div_x + 46
cn_bbox = dr.textbbox((0, 0), '李涵', font=f_name_cn)
dr.text((cn_x, name_y - (cn_bbox[3] - cn_bbox[1]) / 2 - cn_bbox[1]), '李涵', font=f_name_cn, fill=INK)

# 3.2 tagline — kept short enough to stay left of the artwork (x < 940)
f_tag = font(YAHEI, 34)
text_center_y(dr, name_y + 128, 'LLM Agent Builder · Repository-level SE', f_tag, SLATE)

# 3.3 secondary line
f_sub = font(YAHEI, 26)
text_center_y(dr, name_y + 192, 'M.S. @ SJTU LLMSE · SWE-bench · Multi-Agent · ICSE 2026', f_sub, (124, 140, 155))

# attribution font defined before the guard below uses it
f_attr = font(YAHEI, 24)

# 3.4 text-safe guard: every text line must stay left of the artwork zone (x=981)
art_left = 981
line_checks = [
    ('motif', '♪  ♫  Arturia Mode  ♬  ♪', f_motif),
    ('name', 'Li Han', f_name_en),
    ('cn_name', '李涵', f_name_cn),
    ('tagline', 'LLM Agent Builder · Repository-level SE', f_tag),
    ('sub', 'M.S. @ SJTU LLMSE · SWE-bench · Multi-Agent · ICSE 2026', f_sub),
    ('attribution', '「献给世界的乐章」 — 明日方舟 · 阿尔图罗 (Arturia)', f_attr),
]
text_rights = []
for label, txt, fnt in line_checks:
    w = dr.textbbox((0, 0), txt, font=fnt)[2]
    text_rights.append(w)
    assert X + w <= art_left, f'text "{label}" would overlap artwork: right edge {X + w} >= {art_left}'
max_text_w = max(text_rights)

# 3.5 thin rule under text block (aligns with the widest line)
dr.rectangle([X, name_y + 232, X + max_text_w + 8, name_y + 234], fill=ICE_SOFT)

# 3.6 bottom-left attribution
dr.text((X, H - 52), '「献给世界的乐章」 — 明日方舟 · 阿尔图罗 (Arturia)', font=f_attr, fill=(150, 163, 176))

import os
os.makedirs(OUT, exist_ok=True)
bg.save(f'{OUT}/banner.png', optimize=True)
print('banner saved:', f'{OUT}/banner.png', bg.size)

# ---------- 4. footer art (full art, 40%) ----------
art_full = Image.open('arturia.png').convert('RGB')
w2 = 680
h2 = round(art_full.height * w2 / art_full.width)
art_full = art_full.resize((w2, h2), Image.LANCZOS)
# white card border (polaroid feel) — skip, plain is cleaner
art_full.save(f'{OUT}/arturia.png', optimize=True)
print('footer art saved:', f'{OUT}/arturia.png', art_full.size)