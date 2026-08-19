"""Widen the vertical card from 2x8 to 3x8 and impose it two ways.

The card and everything in it live in one q/Q block whose coordinates are
relative to the card's own origin, so widening is: draw a wider background and
border, then translate the original contents right by half the added width.
Nothing is scaled — tap-zone heights and type sizes are untouched.
"""
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, ArrayObject, FloatObject
import re

SRC = 'source/VERTICAL-2x8.pdf'
OLD_W, H, NEW_W = 144.0, 576.0, 216.0
SHIFT = (NEW_W - OLD_W) / 2

DARK, MUTED_DARK = '.82 .58 .68 .72', '.3 .14 .28 .3'
NAVY, NAVY_MUTED = '.94 .78 .38 .52', '.38 .22 .10 .28'

BG_OLD, BORDER_OLD = 'n 0 0 144 576 re f*', 'n 6.12 6.12 131.76 563.76 re S'
BG_NEW = 'n 0 0 %g %g re f*' % (NEW_W, H)
BORDER_NEW = 'n 6.12 6.12 %g %g re S' % (NEW_W - 12.24, H - 12.24)


def blocks(data):
    starts = [m.start() for m in re.finditer(r'q\n1 0 0 1 [\d.]+ [\d.]+ cm\n', data)]

    def end(i):
        depth = 0
        for m in re.finditer(r'(?m)^(q|Q)$', data):
            if m.start() < i:
                continue
            depth += 1 if m.group(1) == 'q' else -1
            if depth == 0:
                return m.end()
    return [data[s:end(s)] for s in starts]


def widen(block, x, y):
    head, rest = block.split(BORDER_OLD, 1)
    head = head.replace(BG_OLD, BG_NEW)
    head = re.sub(r'^q\n1 0 0 1 [\d.]+ [\d.]+ cm\n', 'q\n1 0 0 1 %g %g cm\n' % (x, y), head)
    body = rest.rstrip()
    assert body.endswith('Q')
    return '%s%s\nq\n1 0 0 1 %g 0 cm\n%s\nQ\nQ\n' % (head, BORDER_NEW, SHIFT, body[:-1].rstrip('\n'))


LAYOUTS = {
    '3up': dict(page=(792, 612), xs=[36, 288, 540], y=18),
    '2up': dict(page=(612, 792), xs=[60, 336], y=108),
}

src = PdfReader(SRC)
for tag, lay in LAYOUTS.items():
    w = PdfWriter()
    w.append(src)
    for pno, pg in enumerate(w.pages):
        d = pg.get_contents().get_data().decode('latin-1')
        if pno == 0:                       # page 1 is the dark card
            d = d.replace(DARK, NAVY).replace(MUTED_DARK, NAVY_MUTED)
        bs = blocks(d)
        out = ['1 0 0 1 0 0 cm  BT /F1 12 Tf 14.4 TL ET\n']
        for i, x in enumerate(lay['xs']):
            out.append(widen(bs[i % len(bs)], x, lay['y']))
        st = DecodedStreamObject()
        st.set_data(''.join(out).encode('latin-1'))
        pg[NameObject('/Contents')] = w._add_object(st)
        pg[NameObject('/MediaBox')] = ArrayObject(
            [FloatObject(0), FloatObject(0), FloatObject(lay['page'][0]), FloatObject(lay['page'][1])])
    with open('/tmp/vert3x8-%s.pdf' % tag, 'wb') as f:
        w.write(f)
    print('built', tag, lay['page'], len(lay['xs']), 'per sheet')
