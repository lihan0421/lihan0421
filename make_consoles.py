# -*- coding: utf-8 -*-
"""Generate Arturia-themed terminal console SVGs for the GitHub profile."""
import json

D = json.load(open('console_data.json', encoding='utf-8'))
LANGS = D['langs']
TOTAL = D['total_bytes']
REPOS = D['top_repos']

INK = '#1a222b'
SLATE = '#5b6b7b'
ICE = '#4a7ba6'
ICE_SOFT = '#b8cfe3'
BORDER = '#dbe7f2'
BG = '#ffffff'
LANG_ORDER = ['Python', 'Jupyter Notebook', 'HTML', 'TypeScript', 'JavaScript']
LANG_SHORT = {'Jupyter Notebook': 'Jupyter'}

def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def frame(w, h, title):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <rect width="{w}" height="{h}" rx="12" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
  <rect x="1" y="1" width="{w-2}" height="34" rx="11" fill="#f2f7fc"/>
  <circle cx="20" cy="18" r="5" fill="#b8cfe3"/>
  <circle cx="38" cy="18" r="5" fill="#9abfda"/>
  <circle cx="56" cy="18" r="5" fill="#7ba6c9"/>
  <text x="{w/2}" y="24" text-anchor="middle" font-family="Consolas, Menlo, monospace" font-size="13" fill="{SLATE}">{esc(title)}</text>
'''

def row(y, label, value, vfill=INK, mono=True):
    lf = 'Consolas, Menlo, monospace' if mono else '"Microsoft YaHei", "PingFang SC", sans-serif'
    out = f'<text x="26" y="{y}" font-family="{lf}" font-size="15" fill="{SLATE}">{esc(label)}</text>'
    if mono:
        out += f'<text x="230" y="{y}" font-family="Consolas, Menlo, monospace" font-size="15" fill="{vfill}">{esc(value)}</text>'
    else:
        out += f'<text x="230" y="{y}" font-family="\"Microsoft YaHei\", \"PingFang SC\", sans-serif" font-size="15" fill="{vfill}">{esc(value)}</text>'
    return out

# ---------------- 1. contribution console ----------------
lines = [
    ('$ ', 'arturia --status', ICE, True),
    ('● operator', 'Li Han (李涵)', INK, False),
    ('● base', 'SJTU · LLMSE Lab', INK, False),
    ('● public repos', '19 · own 13', INK, True),
    ('● stars', '97 ★', INK, True),
    ('● followers', '7 · following 6', INK, True),
    ('● contributions', '52 (last 365d)', INK, True),
    ('● papers', "ICSE 2026 · TOSEM · ICSE 2027 (in review)", INK, True),
]
CW, CH = 900, 16 + 34 + len(lines) * 32
svg = [frame(CW, CH, 'arturia@github:~ — contribution console')]
y = 70
for label, val, fill, mono in lines:
    svg.append(row(y, label, val, fill, mono))
    y += 32
svg.append('</svg>')
open('assets/contribution-console.svg', 'w', encoding='utf-8').write('\n'.join(svg))
print('contribution-console.svg', CW, CH)

# ---------------- 2. language console ----------------
langs = []
for lang in LANG_ORDER:
    if lang in LANGS:
        langs.append((LANG_SHORT.get(lang, lang), LANGS[lang]))
tot = sum(n for _, n in langs)
BW, BH = 440, 16 + 34 + len(langs) * 42 + 56
svg = [frame(BW, BH, 'arturia@github:~ — languages')]
y = 84
for lang, n in langs:
    pct = 100 * n / tot
    bar_w = int(320 * pct / 100)
    svg.append(f'<rect x="26" y="{y-13}" width="{bar_w}" height="18" rx="9" fill="#cfe0ef"/>')
    svg.append(f'<text x="34" y="{y}" font-family="Consolas, Menlo, monospace" font-size="14" fill="{INK}">{esc(lang)}</text>')
    svg.append(f'<text x="414" y="{y}" text-anchor="end" font-family="Consolas, Menlo, monospace" font-size="14" fill="{ICE}">{pct:.0f}%</text>')
    y += 42
svg.append(f'<text x="26" y="{y+6}" font-family="Consolas, Menlo, monospace" font-size="13" fill="{SLATE}">bytes: {TOTAL:,} · non-fork repos</text>')
svg.append('</svg>')
open('assets/language-console.svg', 'w', encoding='utf-8').write('\n'.join(svg))
print('language-console.svg', BW, BH)

# ---------------- 3. repository console ----------------
RW, RH = 440, 16 + 34 + len(REPOS) * 32 + 24
svg = [frame(RW, RH, 'arturia@github:~ — repositories')]
y = 70
for r in REPOS:
    name = r['name']
    svg.append(f'<text x="26" y="{y}" font-family="Consolas, Menlo, monospace" font-size="15" fill="{INK}">{esc(name)}</text>')
    svg.append(f'<text x="414" y="{y}" text-anchor="end" font-family="Consolas, Menlo, monospace" font-size="15" fill="{ICE}">{r["stars"]} ★</text>')
    y += 32
svg.append(f'<text x="26" y="{y+4}" font-family="Consolas, Menlo, monospace" font-size="13" fill="{SLATE}">top-{len(REPOS)} by stars</text>')
svg.append('</svg>')
open('assets/repository-console.svg', 'w', encoding='utf-8').write('\n'.join(svg))
print('repository-console.svg', RW, RH)