# Gemeinsame Bausteine für Entwurf G (Usability, Lenkung und Punkte)
import math

INK = '#1D1B3A'
FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&amp;family=Atkinson+Hyperlegible:wght@400;700&amp;display=swap">'

BASE_CSS = r"""
body{margin:0}
*{box-sizing:border-box}
button{font:inherit;color:inherit;cursor:pointer;border:0;background:none;padding:0;text-align:left}
button:disabled{cursor:default}
button:focus-visible,a:focus-visible{outline:3px solid #2F6BFF;outline-offset:3px}
a{color:#2B3FA8}a:hover{color:#1D1B3A}
.h{font-family:'Baloo 2','Trebuchet MS',sans-serif;font-weight:800;margin:0;line-height:1.08}
.cap{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.scr{position:absolute;left:0;top:0;width:768px;height:1024px;display:flex;flex-direction:column}
.card{background:#FFFBF2;border:3px solid #1D1B3A;border-radius:22px;box-shadow:0 5px 0 #1D1B3A}
.btn{display:flex;align-items:center;justify-content:center;gap:10px;min-height:60px;padding:0 26px;border:3px solid #1D1B3A;border-radius:18px;background:#FFC83D;box-shadow:0 5px 0 #1D1B3A;font-family:'Baloo 2',sans-serif;font-weight:800;font-size:21px;text-align:center;text-decoration:none;color:#1D1B3A}
.btn:active{transform:translateY(3px);box-shadow:0 2px 0 #1D1B3A}
.btn2{display:flex;align-items:center;justify-content:center;gap:8px;min-height:56px;padding:0 20px;border:3px solid #1D1B3A;border-radius:16px;background:#FFFFFF;box-shadow:0 4px 0 #1D1B3A;font-weight:700;font-size:17px;text-align:center;text-decoration:none;color:#1D1B3A}
.btn2:active{transform:translateY(2px);box-shadow:0 2px 0 #1D1B3A}
.btn:disabled,.btn2:disabled{background:#E4E2EC;color:#5E5B78;border-color:#8F8BA8;box-shadow:0 4px 0 #8F8BA8}
.chip{display:inline-flex;align-items:center;gap:6px;padding:4px 11px;border-radius:999px;border:2px solid #1D1B3A;background:#FFFFFF;font-size:14px;font-weight:700;line-height:1.2;white-space:nowrap}
.bubble{position:relative;background:#FFFFFF;border:3px solid #1D1B3A;border-radius:20px 20px 20px 6px;padding:12px 16px;font-size:17px;font-weight:700;line-height:1.35;box-shadow:0 4px 0 #1D1B3A}
.muted{color:#4F4C6E}
@keyframes wipp{0%,100%{transform:rotate(0)}50%{transform:rotate(-5deg)}}
.kr{animation:wipp 5s ease-in-out infinite;transform-origin:50% 90%}
@keyframes flug{0%{transform:translate(-160px,40px)}60%{transform:translate(900px,-60px)}100%{transform:translate(900px,-60px)}}
.komet{animation:flug 11s linear infinite}
@keyframes funk{0%,100%{opacity:.25}50%{opacity:1}}
.fu{animation:funk 3.2s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){.kr,.komet,.fu{animation:none}}
"""

def head(title):
    return ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n<title>%s</title>\n'
            '<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n%s\n<style>%s</style>\n</helmet>\n') % (title, FONT, BASE_CSS + '%s')

ICON = {
 'home': 'M4 11l8-7 8 7v9H4Z M10 20v-5h4v5',
 'grid': 'M4 4h7v7H4Z M13 4h7v7h-7Z M4 13h7v7H4Z M13 13h7v7h-7Z',
 'people': 'M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z M3.5 19a5.5 5.5 0 0 1 11 0 M16 11a2.5 2.5 0 1 0 0-5 M17 14.5a4.5 4.5 0 0 1 3.5 4.5',
 'user': 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z M4.5 20a7.5 7.5 0 0 1 15 0',
 'close': 'M6 6l12 12 M18 6L6 18',
 'back': 'M15 5l-7 7 7 7',
 'eye': 'M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6S2 12 2 12Z M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z',
 'pencil': 'M4 20l4.5-1L19 8.5 15.5 5 5 15.5 4 20Z M13.5 7l3.5 3.5',
 'loop': 'M19.5 12a7.5 7.5 0 1 1-2.2-5.3 M19.5 4v4h-4',
 'star': 'M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9Z',
 'clock': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z M12 7v5l3.5 2',
 'check': 'M5 12.5l4.5 4.5L19 7.5',
 'book': 'M4 5.5C4 4.7 4.7 4 5.5 4H11v15H5.5C4.7 19 4 19.7 4 20.5Z M20 5.5c0-.8-.7-1.5-1.5-1.5H13v15h5.5c.8 0 1.5.7 1.5 1.5Z',
 'geo': 'M3 20h18L3 4Z M3 15h3 M3 10.5h2 M8 20v-3 M12.5 20v-2',
 'tap': 'M9 11V5.5a2 2 0 0 1 4 0V11 M13 10a2 2 0 0 1 4 0v3 M9 11a2 2 0 0 0-4 0v2c0 4.4 3.1 8 7 8h1c3 0 5-2.7 5-6v-2',
 'bolt': 'M13 2L4.5 14H11l-1 8 8.5-12H12Z',
 'mix': 'M3 7h3.5L16 17h4 M3 17h3.5l3-3 M14 10l2-3h4 M18 4.5l2.5 2.5L18 9.5 M18 14.5l2.5 2.5-2.5 2.5',
 'trophy': 'M8 4h8v5a4 4 0 0 1-8 0Z M8 6H5a3 3 0 0 0 3 4 M16 6h3a3 3 0 0 1-3 4 M12 13v4 M8 20h8',
 'compass': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z M15.5 8.5l-2 5-5 2 2-5Z',
 'target': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z M12 16a4 4 0 1 0 0-8 4 4 0 0 0 0 8Z M12 12h.01',
 'draw': 'M4 19L19 5 M4 19h16 M14 19a10 10 0 0 0-3.5-7.5',
 'sliders': 'M4 7h9 M17 7h3 M4 17h3 M11 17h9 M15 9.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z M9 19.5a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z',
 'del': 'M9 5h11v14H9l-6-7Z M12.5 9.5l5 5 M17.5 9.5l-5 5',
 'info': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z M12 11v5 M12 7.5h.01',
 'pause': 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z M10 9v6 M14 9v6',
 'arrow': 'M5 12h14 M13 6l6 6-6 6',
 'lightbulb': 'M9 18h6 M10 21h4 M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3Z',
}

def ic(name, size=22, sw=2.4, color='currentColor', style=''):
    st = ' style="flex:none;%s"' % style
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" aria-hidden="true"%s><path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
            % (size, size, st, ICON[name], color, sw))

def ich(hole, size=22, sw=2.4):
    """Symbol, dessen Pfad aus einem Loch kommt"""
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" aria-hidden="true" style="flex:none"><path d="{{%s}}" fill="none" stroke="currentColor" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
            % (size, size, hole, sw))

def krabbi(w, label=None, extra=''):
    """Krabbi als Astronaut mit Sternen-Antennen (Themenhaut Weltraum)"""
    h = round(w * 144 / 120)
    acc = 'role="img" aria-label="%s"' % label if label else 'aria-hidden="true"'
    return ('<svg width="%d" height="%d" viewBox="0 -24 120 144" %s style="flex:none;overflow:visible%s">' % (w, h, acc, extra)
     + '<path d="M54 50L44 2M66 50l10-48" stroke="#1D1B3A" stroke-width="3" stroke-linecap="round" fill="none"></path>'
     + '<path d="M44 -12l2.6 5.3 5.8.8-4.2 4.1 1 5.8L44 1.2l-5.2 2.8 1-5.8-4.2-4.1 5.8-.8Z" fill="#FFC83D" stroke="#1D1B3A" stroke-width="2" stroke-linejoin="round"></path>'
     + '<path d="M76 -12l2.6 5.3 5.8.8-4.2 4.1 1 5.8L76 1.2l-5.2 2.8 1-5.8-4.2-4.1 5.8-.8Z" fill="#FFC83D" stroke="#1D1B3A" stroke-width="2" stroke-linejoin="round"></path>'
     + '<path d="M30 88l-11 8M27 79l-13 4M90 88l11 8M93 79l13 4" stroke="#C75A12" stroke-width="5" stroke-linecap="round" fill="none"></path>'
     + '<path d="M33 68C22 63 17 56 17 46M87 68c11-5 16-12 16-22" stroke="#F47B20" stroke-width="7" stroke-linecap="round" fill="none"></path>'
     + '<circle cx="17" cy="38" r="12" fill="#F47B20" stroke="#1D1B3A" stroke-width="2.5"></circle><path d="M17 40L9 25h14Z" fill="#C75A12"></path>'
     + '<circle cx="103" cy="38" r="12" fill="#F47B20" stroke="#1D1B3A" stroke-width="2.5"></circle><path d="M103 40l8-15H97Z" fill="#C75A12"></path>'
     + '<path d="M50 54L46 32M70 54l4-22" stroke="#F47B20" stroke-width="6" stroke-linecap="round" fill="none"></path>'
     + '<ellipse cx="60" cy="74" rx="34" ry="26" fill="#F47B20" stroke="#1D1B3A" stroke-width="3"></ellipse><ellipse cx="60" cy="83" rx="21" ry="11" fill="#FFA24D"></ellipse>'
     + '<circle cx="46" cy="27" r="10" fill="#FFFFFF" stroke="#1D1B3A" stroke-width="2.5"></circle><circle cx="74" cy="27" r="10" fill="#FFFFFF" stroke="#1D1B3A" stroke-width="2.5"></circle>'
     + '<circle cx="48" cy="28" r="4.5" fill="#1D1B3A"></circle><circle cx="76" cy="28" r="4.5" fill="#1D1B3A"></circle>'
     + '<path d="M52 73q8 7 16 0" stroke="#1D1B3A" stroke-width="3" stroke-linecap="round" fill="none"></path>'
     + '<circle cx="41" cy="72" r="4" fill="#FF8F6B"></circle><circle cx="79" cy="72" r="4" fill="#FF8F6B"></circle>'
     + '</svg>')

def burst():
    pts = []
    for i in range(20):
        r = 17 if i % 2 == 0 else 9
        a = math.pi * i / 10 - math.pi / 2
        pts.append('%.1f,%.1f' % (20 + r * math.cos(a), 20 + r * math.sin(a)))
    return ' '.join(pts)

# Rang-Symbole (niedlich: kleine Gesichter)
FACE = '<circle cx="{x1}" cy="{y}" r="1.6" fill="#1D1B3A"></circle><circle cx="{x2}" cy="{y}" r="1.6" fill="#1D1B3A"></circle><path d="M{m1} {my}q{q} 2.6 {q2} 0" stroke="#1D1B3A" stroke-width="1.5" fill="none" stroke-linecap="round"></path>'
def face(cx, cy):
    return FACE.format(x1=cx-3.2, x2=cx+3.2, y=cy-1, m1=cx-2.6, my=cy+2.2, q=2.6, q2=5.2)

RANK_SVG = {
 'staub': '<circle cx="11" cy="27" r="3" fill="#FFC83D" stroke="#1D1B3A" stroke-width="1.5"></circle><circle cx="30" cy="12" r="2.5" fill="#FFC83D" stroke="#1D1B3A" stroke-width="1.5"></circle><circle cx="21" cy="21" r="9" fill="#FFC83D" stroke="#1D1B3A" stroke-width="2"></circle>' + face(21, 21),
 'meteor': '<path d="M5 7l11 9M4 16l8 6M13 4l9 8" stroke="#1D1B3A" stroke-width="2.5" stroke-linecap="round" fill="none"></path><circle cx="26" cy="25" r="10" fill="#FFC83D" stroke="#1D1B3A" stroke-width="2"></circle>' + face(26, 25),
 'komet': '<path d="M3 4l23 12-10 10Z" fill="#FFE9A8" stroke="#1D1B3A" stroke-width="2" stroke-linejoin="round"></path><circle cx="26" cy="26" r="10" fill="#FFC83D" stroke="#1D1B3A" stroke-width="2"></circle>' + face(26, 26),
 'planet': '<circle cx="20" cy="20" r="11" fill="#FFC83D" stroke="#1D1B3A" stroke-width="2"></circle><path d="M3 26c3 3 14 0 23-6s12-11 10-13" stroke="#1D1B3A" stroke-width="2.5" fill="none" stroke-linecap="round"></path>' + face(20, 19),
 'pulsar': '<circle cx="20" cy="20" r="15" fill="none" stroke="#1D1B3A" stroke-width="2" stroke-dasharray="3 4"></circle><circle cx="20" cy="20" r="9" fill="#FFC83D" stroke="#1D1B3A" stroke-width="2"></circle>' + face(20, 20),
 'supernova': '<polygon points="%s" fill="#FFC83D" stroke="#1D1B3A" stroke-width="2" stroke-linejoin="round"></polygon>' % burst() + face(20, 21),
 'galaxis': '<path d="M20 20c0-8 8-11 13-6 5 4 4 12-1 16M20 20c0 8-8 11-13 6-5-4-4-12 1-16" stroke="#1D1B3A" stroke-width="3" stroke-linecap="round" fill="none"></path><circle cx="20" cy="20" r="7" fill="#FFC83D" stroke="#1D1B3A" stroke-width="2"></circle>' + face(20, 20),
}
def rank(name, size=36):
    return '<svg width="%d" height="%d" viewBox="0 0 40 40" aria-hidden="true" style="flex:none">%s</svg>' % (size, size, RANK_SVG[name])

def arcs(cx=32, cy=32, r=27):
    out = []
    for i in range(3):
        a0 = math.radians(-90 + i * 120 + 7)
        a1 = math.radians(-90 + i * 120 + 113)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        out.append('M%.2f %.2fA%d %d 0 0 1 %.2f %.2f' % (x0, y0, r, r, x1, y1))
    return out
ARC = arcs()

def token(var, size=64, numsize=20):
    """Paketmarke: Planet mit Nummer und Haken-Ring aus drei Teilen"""
    return ('<svg width="%d" height="%d" viewBox="0 0 64 64" aria-hidden="true" style="flex:none;display:block">' % (size, size)
     + ''.join('<path d="%s" fill="none" stroke="{{%s.c%d}}" stroke-width="{{%s.w%d}}" stroke-dasharray="{{%s.d%d}}" stroke-linecap="round"></path>' % (ARC[i], var, i, var, i, var, i) for i in range(3))
     + '<circle cx="32" cy="32" r="19" fill="{{%s.col}}" stroke="#1D1B3A" stroke-width="2.5"></circle>' % var
     + '<circle cx="25" cy="25" r="3.2" fill="#FFFFFF" opacity=".35"></circle><circle cx="39" cy="40" r="2.2" fill="#FFFFFF" opacity=".3"></circle>'
     + '<text x="32" y="39" text-anchor="middle" font-family="Baloo 2, sans-serif" font-weight="800" font-size="%d" fill="#FFFFFF" stroke="#1D1B3A" stroke-width="0.8">{{%s.nr}}</text>' % (numsize, var)
     + '</svg>')

def stars_bg(w, h, n, seed=3, color='#FFFFFF', op=0.9, blink=True):
    import random
    rnd = random.Random(seed)
    s = []
    for i in range(n):
        x, y = rnd.uniform(6, w - 6), rnd.uniform(6, h - 6)
        r = rnd.choice([1, 1.3, 1.6, 2.2])
        cls = ' class="fu" style="animation-delay:%.1fs"' % rnd.uniform(0, 3) if blink and i % 4 == 0 else ''
        s.append('<circle cx="%.0f" cy="%.0f" r="%s" fill="%s" opacity="%s"%s></circle>' % (x, y, r, color, op, cls))
    return ''.join(s)
