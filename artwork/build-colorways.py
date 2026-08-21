"""Build the 5 x 7 counter sign in one light and four dark colourways."""
import sys, re
sys.path.insert(0, '.')
from enlarge import apply_spec, SIGN_5x7_SPEC
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, ArrayObject, FloatObject

DARK, MUTED_DARK, MUTED_CREAM = '.82 .58 .68 .72', '.3 .14 .28 .3', '.52 .34 .42 .28'

# background (or ink, on the light one) and the muted "ONE TAP" line that goes with it
COLOURWAYS = {
    'NAVY':      ('.94 .78 .38 .52', '.38 .22 .10 .28'),
    'BURGUNDY':  ('.40 .94 .68 .55', '.22 .40 .30 .28'),
    'OAK':       ('.42 .60 .78 .55', '.28 .34 .44 .28'),
    'GRAPHITE':  ('.66 .56 .52 .84', '.26 .20 .20 .34'),
}
CREAM_INK = ('.94 .78 .38 .52', '.58 .40 .20 .28')   # navy ink on the cream card

W, H, INSET, OLD_W = 360.0, 504.0, 9.0, 144.0
SHIFT = (W - OLD_W) / 2
BG_OLD, BORDER_OLD = 'n 0 0 144 576 re f*', 'n 6.12 6.12 131.76 563.76 re S'
BG_NEW = 'n 0 0 %g %g re f*' % (W, H)
BORDER_NEW = 'n %g %g %g %g re S' % (INSET, INSET, W - 2 * INSET, H - 2 * INSET)
PLACE = [(24, 54), (408, 54)]


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


def sign(block, x, y):
    block = apply_spec(block, SIGN_5x7_SPEC)
    head, rest = block.split(BORDER_OLD, 1)
    head = head.replace(BG_OLD, BG_NEW)
    head = re.sub(r'^q\n1 0 0 1 [\d.]+ [\d.]+ cm\n', 'q\n1 0 0 1 %g %g cm\n' % (x, y), head)
    body = rest.rstrip()
    assert body.endswith('Q')
    return '%s%s\nq\n1 0 0 1 %g 0 cm\n%s\nQ\nQ\n' % (head, BORDER_NEW, SHIFT, body[:-1].rstrip('\n'))


def build(out, page_index, colour, muted, old_muted):
    src = PdfReader('source/VERTICAL-2x8.pdf')
    w = PdfWriter()
    w.append(src, pages=(page_index, page_index + 1))
    pg = w.pages[0]
    d = pg.get_contents().get_data().decode('latin-1')
    d = d.replace(DARK, colour).replace(old_muted, muted)
    out_ops = ['1 0 0 1 0 0 cm  BT /F1 12 Tf 14.4 TL ET\n']
    for i, (x, y) in enumerate(PLACE):
        out_ops.append(sign(blocks(d)[i % len(blocks(d))], x, y))
    st = DecodedStreamObject()
    st.set_data(''.join(out_ops).encode('latin-1'))
    pg[NameObject('/Contents')] = w._add_object(st)
    pg[NameObject('/MediaBox')] = ArrayObject(
        [FloatObject(0), FloatObject(0), FloatObject(792), FloatObject(612)])
    with open(out, 'wb') as f:
        w.write(f)


for name, (colour, muted) in COLOURWAYS.items():
    build('/tmp/sign-%s.pdf' % name, 0, colour, muted, MUTED_DARK)
    print('dark  ', name)
build('/tmp/sign-CREAM.pdf', 1, CREAM_INK[0], CREAM_INK[1], MUTED_CREAM)
print('light  CREAM')
