"""Scale the artwork up inside the same trim size.

The art was drawn for a 2 x 8 in card and never grew when the card went to
3 x 8, so on the printed piece the logos and the small type read small and the
horizontal card carries a wide empty band top and bottom.

Every element in a card sits in its own run of the content stream and is
centred on the card's axis, so each one can be scaled about its own centre
without touching the others. Text is re-centred exactly: the advance widths
come from the fonts embedded in the source PDF, so the new x is computed, not
guessed.
"""
import re
from fontTools.ttLib import TTFont

JOST = TTFont('source/Jost-Regular.ttf')
PLAY = TTFont('source/PlayfairDisplay-Regular.ttf')
FONTS = {'F2+0': JOST, 'F3+0': PLAY}


def unescape(s):
    """PDF string literal -> text."""
    out, i = [], 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            nxt = s[i + 1]
            if nxt.isdigit():
                oct_digits = re.match(r'[0-7]{1,3}', s[i + 1:]).group(0)
                out.append(chr(int(oct_digits, 8)))
                i += 1 + len(oct_digits)
                continue
            out.append(nxt)
            i += 2
            continue
        out.append(s[i])
        i += 1
    return ''.join(out)


def text_width(font, text, size, tc):
    cmap = font['cmap'].tables[0].cmap
    hmtx, upem = font['hmtx'], font['head'].unitsPerEm
    total = 0.0
    for ch in text:
        gname = cmap.get(ord(ch))
        adv = hmtx[gname][0] if gname else 0
        total += adv / upem * size + tc
    return total


TEXT_RE = re.compile(
    r'^(BT 1 0 0 1 0 0 Tm [\d. ]+k )([\d.]+)( Tc 1 0 0 1 )([\d.]+) ([\d.]+)'
    r'( Tm /)(\S+)( )([\d.]+)( Tf )([\d.]+)( TL \()(.*)(\) Tj ET)$')

IMG_RE = re.compile(r'^([\d.]+) 0 0 ([\d.]+) ([\d.]+) ([\d.]+) cm$')


def scale_text(line, new_size, new_tc, dy):
    m = TEXT_RE.match(line)
    assert m, line[:80]
    tc_old = float(m.group(2))
    x, y = float(m.group(4)), float(m.group(5))
    fname, size_old = m.group(7), float(m.group(9))
    body = m.group(13)
    font = FONTS[fname]
    text = unescape(body)
    w_old = text_width(font, text, size_old, tc_old)
    w_new = text_width(font, text, new_size, new_tc)
    x_new = x - (w_new - w_old) / 2.0
    lead = new_size * 1.2
    return ('%s%g%s%.4f %.4f%s%s%s%g%s%g%s%s%s'
            % (m.group(1), new_tc, m.group(3), x_new, y + dy, m.group(6),
               fname, m.group(8), new_size, m.group(10), lead, m.group(12),
               body, m.group(14)))


def scale_img(line, k, dy):
    m = IMG_RE.match(line)
    assert m, line
    w, h, x, y = (float(m.group(i)) for i in range(1, 5))
    return ('%.5f 0 0 %.5f %.5f %.5f cm'
            % (w * k, h * k, x - w * (k - 1) / 2, y - h * (k - 1) / 2 + dy))


def wrap_paths(lines, cx, cy, k, dy):
    tx, ty = cx - k * cx, (cy + dy) - k * cy
    return ['q', '%g 0 0 %g %.4f %.4f cm' % (k, k, tx, ty)] + lines + ['Q']


# ---- what gets scaled, per card -------------------------------------------
# (kind, line index or range, parameters)
VERT_SPEC = [
    ('img',  8,            dict(k=1.45, dy=4)),          # Google logo
    ('path', (11, 37),     dict(cx=72, cy=461.4, k=1.30, dy=0)),
    ('text', 37,           dict(size=9.0, tc=2.1, dy=-3)),   # TAP TO REVIEW
    ('img',  39,           dict(k=1.45, dy=6)),          # Yelp logo
    ('path', (42, 68),     dict(cx=72, cy=108.6, k=1.30, dy=0)),
    ('text', 68,           dict(size=9.0, tc=2.1, dy=-3)),   # FIND US ON YELP
    ('path', (69, 84),     dict(cx=72, cy=322.4, k=1.40, dy=0)),  # stars
    ('text', 84,           dict(size=26, tc=0.26, dy=3)),   # How did
    ('text', 85,           dict(size=26, tc=0.26, dy=-3)),  # we do?
    ('text', 86,           dict(size=8.6, tc=2.5, dy=-2)),  # ONE TAP
    ('text', 87,           dict(size=8.6, tc=2.5, dy=-5)),  # NO APP, NO TYPING
]

HORIZ_SPEC = [
    ('img',  8,            dict(k=1.35, dy=3)),
    ('path', (11, 37),     dict(cx=95.04, cy=65.4, k=1.25, dy=0)),
    ('text', 37,           dict(size=8.4, tc=2.0, dy=-2)),
    ('img',  39,           dict(k=1.35, dy=3)),
    ('path', (42, 68),     dict(cx=473.76, cy=65.4, k=1.25, dy=0)),
    ('text', 68,           dict(size=8.4, tc=2.0, dy=-2)),
    ('path', (69, 84),     dict(cx=284.4, cy=100.85, k=1.35, dy=2)),
    ('text', 84,           dict(size=30, tc=0.24, dy=-2)),
    ('text', 85,           dict(size=8.8, tc=2.4, dy=-1)),
]


def apply_spec(block, spec):
    lines = block.split('\n')
    out = {}
    for kind, where, p in spec:
        if kind == 'img':
            out[where] = [scale_img(lines[where], p['k'], p['dy'])]
        elif kind == 'text':
            out[where] = [scale_text(lines[where], p['size'], p['tc'], p['dy'])]
        else:
            a, b = where
            out[a] = wrap_paths(lines[a:b], p['cx'], p['cy'], p['k'], p['dy'])
            for i in range(a + 1, b):
                out[i] = []
    return '\n'.join(
        '\n'.join(out[i]) if i in out and out[i] else
        ('' if i in out else lines[i])
        for i in range(len(lines))
        if not (i in out and not out[i])
    )
