import math
FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&display=swap">'
BODYFONT = "'Atkinson Hyperlegible', 'Verdana', sans-serif"
HEADFONT = "'Bricolage Grotesque', 'Trebuchet MS', sans-serif"

COSTUMES = {
 'none': '',
 'helm': '<circle cx="60" cy="38" r="40" fill="rgba(170,195,255,.18)" stroke="#BFD0FF" stroke-width="3"></circle><path d="M30 22a34 34 0 0 1 18-16" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round" fill="none" opacity=".85"></path>',
 'hut': '<path d="M62 -22L84 10Q60 17 36 10Z" fill="#6B3FD4"></path><ellipse cx="60" cy="11" rx="31" ry="6" fill="#4A2A9E"></ellipse><path d="M61 -8l1.800 3.800 4.200.500-3.100 2.900.800 4.100-3.700-2-3.700 2 .800-4.100-3.100-2.900 4.200-.500z" fill="#FFD75E"></path>'.replace('.800','.8').replace('.500','.5').replace('.100','.1').replace('.200','.2').replace('.700','.7'),
 'suedwester': '<path d="M38 10Q60 -20 82 10Z" fill="#FFC83D"></path><path d="M26 12Q60 2 94 12Q98 18 90 17Q60 9 30 17Q22 18 26 12Z" fill="#E0A100"></path>',
 'detektiv': '<path d="M34 11Q38 -10 62 -9Q86 -8 88 11Z" fill="#7A5A3A"></path><path d="M28 11h66a3 3 0 0 1 0 6H28a3 3 0 0 1 0-6Z" fill="#5C4129"></path><circle cx="104" cy="26" r="10" fill="rgba(255,255,255,.55)" stroke="#2B2118" stroke-width="3.5"></circle><path d="M104 36v8" stroke="#2B2118" stroke-width="4" stroke-linecap="round"></path>',
 'taucher': '<rect x="30" y="13" width="60" height="28" rx="13" fill="rgba(150,225,255,.35)" stroke="#0B6E8A" stroke-width="4"></rect><path d="M90 27h9v-34" stroke="#FF6B4A" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"></path>',
}

def krabbi(w, costume='helm', style='', label=None):
    h = round(w * 144 / 120)
    acc = 'role="img" aria-label="%s"' % label if label else 'aria-hidden="true"'
    st = (' style="%s"' % style) if style else ''
    return ('<svg width="%d" height="%d" viewBox="0 -24 120 144" %s%s>' % (w, h, acc, st)
     + '<path d="M30 88l-11 8M27 79l-13 4M90 88l11 8M93 79l13 4" stroke="#C75A12" stroke-width="5" stroke-linecap="round" fill="none"></path>'
     + '<path d="M33 68C22 63 17 56 17 46M87 68c11-5 16-12 16-22" stroke="#F47B20" stroke-width="7" stroke-linecap="round" fill="none"></path>'
     + '<circle cx="17" cy="38" r="12" fill="#F47B20"></circle><path d="M17 40L9 25h14Z" fill="#C75A12"></path>'
     + '<circle cx="103" cy="38" r="12" fill="#F47B20"></circle><path d="M103 40l8-15H97Z" fill="#C75A12"></path>'
     + '<path d="M50 54L46 32M70 54l4-22" stroke="#F47B20" stroke-width="6" stroke-linecap="round" fill="none"></path>'
     + '<ellipse cx="60" cy="74" rx="34" ry="26" fill="#F47B20"></ellipse><ellipse cx="60" cy="83" rx="21" ry="11" fill="#FFA24D"></ellipse>'
     + '<circle cx="46" cy="27" r="10" fill="#FFFFFF" stroke="#15173A" stroke-width="2"></circle><circle cx="74" cy="27" r="10" fill="#FFFFFF" stroke="#15173A" stroke-width="2"></circle>'
     + '<circle cx="48" cy="28" r="4.5" fill="#15173A"></circle><circle cx="76" cy="28" r="4.5" fill="#15173A"></circle>'
     + '<path d="M52 73q8 7 16 0" stroke="#15173A" stroke-width="3" stroke-linecap="round" fill="none"></path>'
     + '<circle cx="41" cy="72" r="4" fill="#FF8F6B"></circle><circle cx="79" cy="72" r="4" fill="#FF8F6B"></circle>'
     + COSTUMES[costume] + '</svg>')

def burst():
    pts = []
    for i in range(20):
        r = 17 if i % 2 == 0 else 9
        a = math.pi * i / 10 - math.pi / 2
        pts.append('%.1f,%.1f' % (20 + r * math.cos(a), 20 + r * math.sin(a)))
    return ' '.join(pts)

def rank(name, size=40, line='#15173A'):
    Y = '#FFC83D'
    b = {
     'staub': '<circle cx="12" cy="26" r="3.5" fill="{Y}" stroke="{L}" stroke-width="1.5"></circle><circle cx="21" cy="13" r="3" fill="{Y}" stroke="{L}" stroke-width="1.5"></circle><circle cx="28" cy="25" r="4.5" fill="{Y}" stroke="{L}" stroke-width="1.5"></circle><circle cx="18" cy="33" r="2" fill="{L}"></circle><circle cx="32" cy="12" r="2" fill="{L}"></circle>',
     'meteor': '<path d="M6 8l11 9M5 17l8 6M14 5l9 8" stroke="{L}" stroke-width="2.5" stroke-linecap="round" fill="none"></path><circle cx="27" cy="26" r="9" fill="{Y}" stroke="{L}" stroke-width="2"></circle><circle cx="24" cy="24" r="2" fill="{L}" opacity=".45"></circle><circle cx="30" cy="29" r="1.5" fill="{L}" opacity=".45"></circle>',
     'komet': '<path d="M4 5l22 12-9 9Z" fill="#FFE9A8" stroke="{L}" stroke-width="2" stroke-linejoin="round"></path><circle cx="26" cy="26" r="9" fill="{Y}" stroke="{L}" stroke-width="2"></circle>',
     'planet': '<circle cx="20" cy="20" r="10" fill="{Y}" stroke="{L}" stroke-width="2"></circle><ellipse cx="20" cy="20" rx="18" ry="5" transform="rotate(-20 20 20)" fill="none" stroke="{L}" stroke-width="2.5"></ellipse>',
     'pulsar': '<path d="M8 4l24 32" stroke="{L}" stroke-width="2.5" stroke-linecap="round" fill="none"></path><circle cx="20" cy="20" r="13" fill="none" stroke="{L}" stroke-width="2" stroke-dasharray="3 4"></circle><circle cx="20" cy="20" r="7" fill="{Y}" stroke="{L}" stroke-width="2"></circle>',
     'supernova': '<polygon points="%s" fill="{Y}" stroke="{L}" stroke-width="2" stroke-linejoin="round"></polygon><circle cx="20" cy="20" r="3" fill="{L}"></circle>' % burst(),
     'galaxis': '<path d="M20 20c0-7 7-10 12-6 5 4 4 12-1 16M20 20c0 7-7 10-12 6-5-4-4-12 1-16" stroke="{L}" stroke-width="3" stroke-linecap="round" fill="none"></path><circle cx="20" cy="20" r="5.5" fill="{Y}" stroke="{L}" stroke-width="2"></circle>',
    }[name].replace('{Y}', Y).replace('{L}', line)
    return '<svg width="%d" height="%d" viewBox="0 0 40 40" aria-hidden="true">%s</svg>' % (size, size, b)

ICON = {
 'wissen': 'M4 5.5C4 4.700 4.700 4 5.500 4H11v15H5.500C4.700 19 4 19.700 4 20.500V5.500ZM20 5.500C20 4.700 19.300 4 18.500 4H13v15h5.500c.800 0 1.500.700 1.500 1.500V5.500Z',
 'karten': 'M7 8h11a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H7a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1ZM8 4.500h9M10 13h5',
 'erkennen': 'M2.500 12S6 5.500 12 5.500 21.500 12 21.500 12 18 18.500 12 18.500 2.500 12 2.500 12ZM12 9.500a2.500 2.500 0 1 0 0 5 2.500 2.500 0 0 0 0-5Z',
 'zeichnen': 'M4 20l1-4.500L16.500 4a2.100 2.100 0 0 1 3 3L8 18.500 4 20ZM14.500 6l3 3',
 'messen': 'M3 19 12 5l9 14H3ZM12 19v-3M8 19v-2M16 19v-2',
 'schaetzen': 'M4 17a8 8 0 1 1 16 0M12 17l4-6M7.500 17h9',
 'zeit': 'M12 8a6.500 6.500 0 1 0 0 13 6.500 6.500 0 0 0 0-13ZM12 11v3.500l2 1.500M10 3.500h4M12 3.500V8',
 'test': 'M8 4h8v3H8V4ZM6 5.500H5a1 1 0 0 0-1 1V20a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V6.500a1 1 0 0 0-1-1h-1M8.500 14l2.500 2.500 4.500-5',
 'duell': 'M3 12h18M7 8l-4 4 4 4M17 8l4 4-4 4M12 9v6',
 'stern': 'M12 3l2.200 5.600 5.800.400-4.500 3.700 1.500 5.800L12 15.300 6.900 18.500l1.500-5.800L4 9l5.800-.400L12 3Z',
 'sortieren': 'M4 5h7v6H4V5ZM13 13h7v6h-7v-6ZM14 6h6M14 9h4M4 15h6M4 18h4',
 'schloss': 'M7 11V8a5 5 0 0 1 10 0v3M6 11h12a1 1 0 0 1 1 1v7a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1v-7a1 1 0 0 1 1-1Z',
 'check': 'M5 12.500l4.500 4.500L19 7.500',
 'x': 'M6 6l12 12M18 6L6 18',
 'pfeil': 'M5 12h14M13 6l6 6-6 6',
 'weg': 'M5 19.500a2 2 0 1 0 0-4 2 2 0 0 0 0 4ZM19 8.500a2 2 0 1 0 0-4 2 2 0 0 0 0 4ZM7 17.500h7a3 3 0 0 0 0-6h-4a3 3 0 0 1 0-6h7',
 'frei': 'M5 7h8M17 7h2M5 12h2M11 12h8M5 17h9M18 17h1M15 5v4M9 10v4M16 15v4',
 'gem': 'M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM3.500 19a5.500 5.500 0 0 1 11 0M16 11a2.500 2.500 0 1 0 0-5M17 14.500a4.500 4.500 0 0 1 3.500 4.500',
 'ich': 'M12 12a4 4 0 1 0 0-8 4 4 0 0 0 0 8ZM4.500 20a7.500 7.500 0 0 1 15 0',
 'fernrohr': 'M3 14l12-6 2.500 5-12 6L3 14ZM15 8l3-1.500 2.500 5-3 1.500M9 17l-2 4M11 16l3 5',
 'muenze': 'M12 4a8 8 0 1 0 0 16 8 8 0 0 0 0-16ZM12 8v8M9.500 10h3.500a1.500 1.500 0 0 1 0 3h-2a1.500 1.500 0 0 0 0 3H14',
 'seil': 'M2 12c3-3 5 3 8 0s5 3 8 0 3-1 4 0',
 'rad': 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18ZM12 3v18M3 12h18M5.600 5.600l12.800 12.800M18.400 5.600 5.600 18.400',
 'geist': 'M6 20V10a6 6 0 0 1 12 0v10l-3-2-3 2-3-2-3 2ZM10 10h.010M14 10h.010',
}
import re
for k in ICON:
    ICON[k] = re.sub(r'(\.\d)00', r'\1', ICON[k]).replace('.010', '.01')

def icon(name, size=24, color='currentColor', sw=2):
    return '<svg width="%d" height="%d" viewBox="0 0 24 24" aria-hidden="true"><path d="%s" fill="none" stroke="%s" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round"></path></svg>' % (size, size, ICON[name], color, sw)

def week(today):
    pts = [(20,48),(66,22),(112,40),(160,16),(208,44),(254,24),(300,50)]
    lit = [True, True, False, True, today, False, False]
    days = ['Mo','Di','Mi','Do','Fr','Sa','So']
    s = '<svg width="320" height="84" viewBox="0 0 320 84" role="img" aria-label="Sternbild der Woche">'
    s += '<path d="M' + ' L'.join('%d %d' % p for p in pts) + '" fill="none" stroke="#7C84D6" stroke-width="2" stroke-dasharray="2 6" stroke-linecap="round"></path>'
    for (x, y), l, d in zip(pts, lit, days):
        if l:
            s += '<circle cx="%d" cy="%d" r="9" fill="#FFC83D" stroke="#15173A" stroke-width="2"></circle>' % (x, y)
        else:
            s += '<circle cx="%d" cy="%d" r="8" fill="#FBF8F1" stroke="#5A5C78" stroke-width="2"></circle>' % (x, y)
        s += '<text x="%d" y="78" text-anchor="middle" font-size="13" font-weight="700" fill="#3D3F63">%s</text>' % (x, d)
    return s + '</svg>'

def page(title, helmet_css, body, script, props='{"$preview":{"width":768,"height":1024}}'):
    return ('<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n<title>%s</title>\n<script src="./support.js"></script>\n</head>\n<body>\n<x-dc>\n<helmet>\n%s\n<style>\n%s\n</style>\n</helmet>\n%s\n</x-dc>\n<script type="text/x-dc" data-dc-script data-props=\'%s\'>\n%s\n</script>\n</body>\n</html>\n' % (title, FONT, helmet_css, body, props, script))
