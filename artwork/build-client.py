"""Build a 5 x 7 counter sign carrying a client's own logo and palette.

The client logo is embedded as a 1-bit PDF image mask, so it paints in the
sign's ink colour and the file stays entirely CMYK — no RGB image sneaks in.

Palette here is sampled from Trailfolk's printed menu: warm cream stock, a
warm near-black ink and the brick red they use for the tagline.
"""
import sys, re, zlib
sys.path.insert(0, '.')
from enlarge import apply_spec
from pypdf import PdfReader, PdfWriter
from pypdf.generic import (DecodedStreamObject, EncodedStreamObject, NameObject,
                           ArrayObject, FloatObject, NumberObject, BooleanObject,
                           DictionaryObject)

# ---- Trailfolk palette, sampled from the menu photo -----------------------
CREAM_OLD, INK_OLD, MUTED_OLD, GOLD_OLD = (
    '.02 .03 .1 0', '.82 .58 .68 .72', '.52 .34 .42 .28', '.16 .32 .95 .05')
CREAM_NEW, INK_NEW, MUTED_NEW, RED_NEW = (
    '.05 .09 .16 0', '.55 .62 .70 .78', '.42 .44 .50 .30', '.32 .78 .75 .25')

# ---- layout with the client logo at the top ------------------------------
LOGO_SPEC = [
    ('img',  8,        dict(k=1.70, dy=-126.85)),                  # Google logo
    ('path', (11, 37), dict(cx=72, cy=461.4, k=1.50, dy=-138.40)), # Google ring
    ('text', 37,       dict(size=10.5, tc=2.47, dy=-149.40)),      # TAP TO REVIEW
    ('img',  39,       dict(k=1.70, dy=-24.65)),                   # Yelp logo
    ('path', (42, 68), dict(cx=72, cy=108.6, k=1.50, dy=-36.20)),  # Yelp ring
    ('text', 68,       dict(size=10.5, tc=2.47, dy=-47.20)),       # FIND US ON YELP
    ('path', (69, 84), dict(cx=72, cy=322.4, k=1.60, dy=-71.80)),  # stars
    ('text', 84,       dict(size=28, tc=0.28, dy=-75.40)),         # How did
    ('text', 85,       dict(size=28, tc=0.28, dy=-84.40)),         # we do?
    ('text', 86,       dict(size=9.5, tc=2.73, dy=-83.20)),        # ONE TAP
    ('text', 87,       dict(size=9.5, tc=2.73, dy=-85.00)),        # NO APP, NO TYPING
]

W, H, INSET, OLD_W = 360.0, 504.0, 9.0, 144.0
SHIFT = (W - OLD_W) / 2
BG_OLD, BORDER_OLD = 'n 0 0 144 576 re f*', 'n 6.12 6.12 131.76 563.76 re S'
BG_NEW = 'n 0 0 %g %g re f*' % (W, H)
BORDER_NEW = 'n %g %g %g %g re S' % (INSET, INSET, W - 2 * INSET, H - 2 * INSET)
LOGO_H, LOGO_TOP = 76.0, 480.6          # in block coordinates, centred on x = 72


def blocks(d):
    starts = [m.start() for m in re.finditer(r'q\n1 0 0 1 [\d.]+ [\d.]+ cm\n', d)]

    def end(i):
        depth = 0
        for m in re.finditer(r'(?m)^(q|Q)$', d):
            if m.start() < i:
                continue
            depth += 1 if m.group(1) == 'q' else -1
            if depth == 0:
                return m.end()
    return [d[s:end(s)] for s in starts]


def sign(block, x, y, logo_w, logo_h):
    block = apply_spec(block, LOGO_SPEC)
    head, rest = block.split(BORDER_OLD, 1)
    head = head.replace(BG_OLD, BG_NEW)
    head = re.sub(r'^q\n1 0 0 1 [\d.]+ [\d.]+ cm\n', 'q\n1 0 0 1 %g %g cm\n' % (x, y), head)
    body = rest.rstrip()[:-1].rstrip('\n')
    logo = ('%s k\nq %.3f 0 0 %.3f %.3f %.3f cm\n/ClientLogo Do\nQ\n'
            % (INK_NEW, logo_w, logo_h, 72 - logo_w / 2, LOGO_TOP - logo_h))
    return '%s%s\nq\n1 0 0 1 %g 0 cm\n%s\n%s\nQ\nQ\n' % (head, BORDER_NEW, SHIFT, body, logo)


px_w, px_h = (int(v) for v in open('clients/trailfolk-logo.dims').read().split())
logo_h = LOGO_H
logo_w = logo_h * px_w / px_h

src = PdfReader('source/VERTICAL-2x8.pdf')
w = PdfWriter()
w.append(src, pages=(1, 2))                       # the cream page
pg = w.pages[0]

mask = EncodedStreamObject()
mask._data = open('clients/trailfolk-logo.mask', 'rb').read()
mask[NameObject('/Type')] = NameObject('/XObject')
mask[NameObject('/Subtype')] = NameObject('/Image')
mask[NameObject('/Width')] = NumberObject(px_w)
mask[NameObject('/Height')] = NumberObject(px_h)
mask[NameObject('/ImageMask')] = BooleanObject(True)
mask[NameObject('/BitsPerComponent')] = NumberObject(1)
mask[NameObject('/Decode')] = ArrayObject([NumberObject(0), NumberObject(1)])
mask[NameObject('/Filter')] = NameObject('/FlateDecode')
ref = w._add_object(mask)
res = pg[NameObject('/Resources')]
xo = res.get('/XObject')
if xo is None:
    xo = DictionaryObject()
    res[NameObject('/XObject')] = xo
xo = xo.get_object()
xo[NameObject('/ClientLogo')] = ref

d = pg.get_contents().get_data().decode('latin-1')
d = (d.replace(INK_OLD, INK_NEW).replace(MUTED_OLD, MUTED_NEW)
      .replace(GOLD_OLD, RED_NEW).replace(CREAM_OLD, CREAM_NEW))
out = ['1 0 0 1 0 0 cm  BT /F1 12 Tf 14.4 TL ET\n']
for i, (x, y) in enumerate([(24, 54), (408, 54)]):
    out.append(sign(blocks(d)[i % len(blocks(d))], x, y, logo_w, logo_h))
st = DecodedStreamObject()
st.set_data(''.join(out).encode('latin-1'))
pg[NameObject('/Contents')] = w._add_object(st)
pg[NameObject('/MediaBox')] = ArrayObject(
    [FloatObject(0), FloatObject(0), FloatObject(792), FloatObject(612)])
with open('/tmp/trailfolk.pdf', 'wb') as f:
    w.write(f)
print('built  logo %.1f x %.1f pt (%.2f x %.2f in)' % (logo_w, logo_h, logo_w/72, logo_h/72))
