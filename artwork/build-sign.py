"""Build the 5 x 7 in counter sign: one upright piece, two per Letter sheet."""
import sys, re
sys.path.insert(0, '.')
from enlarge import apply_spec, SIGN_5x7_SPEC
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, ArrayObject, FloatObject

DARK, MUTED_DARK, MUTED_CREAM = '.82 .58 .68 .72', '.3 .14 .28 .3', '.52 .34 .42 .28'
NAVY, N_MUTED_DARK, N_MUTED_CREAM = '.94 .78 .38 .52', '.38 .22 .10 .28', '.58 .40 .20 .28'

W, H = 360.0, 504.0          # 5 x 7 in
INSET = 9.0
OLD_W = 144.0
SHIFT = (W - OLD_W) / 2      # the art is centred on x = 72 in the source block

BG_OLD, BORDER_OLD = 'n 0 0 144 576 re f*', 'n 6.12 6.12 131.76 563.76 re S'
BG_NEW = 'n 0 0 %g %g re f*' % (W, H)
BORDER_NEW = 'n %g %g %g %g re S' % (INSET, INSET, W - 2 * INSET, H - 2 * INSET)


def recolour(d):
    return (d.replace(DARK, NAVY).replace(MUTED_DARK, N_MUTED_DARK)
             .replace(MUTED_CREAM, N_MUTED_CREAM))


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


src = PdfReader('source/VERTICAL-2x8.pdf')
w = PdfWriter()
w.append(src)
PLACE = [(24, 54), (408, 54)]            # two up on Letter landscape
for pg in w.pages:
    d = recolour(pg.get_contents().get_data().decode('latin-1'))
    bs = blocks(d)
    out = ['1 0 0 1 0 0 cm  BT /F1 12 Tf 14.4 TL ET\n']
    for i, (x, y) in enumerate(PLACE):
        out.append(sign(bs[i % len(bs)], x, y))
    st = DecodedStreamObject()
    st.set_data(''.join(out).encode('latin-1'))
    pg[NameObject('/Contents')] = w._add_object(st)
    pg[NameObject('/MediaBox')] = ArrayObject(
        [FloatObject(0), FloatObject(0), FloatObject(792), FloatObject(612)])
with open('/tmp/sign5x7.pdf', 'wb') as f:
    w.write(f)
print('built')
