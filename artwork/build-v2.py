"""Build the enlarged v2 artwork: navy, 3 x 8 vertical, scaled-up elements."""
import sys, re
sys.path.insert(0, '.')
from enlarge import apply_spec, VERT_SPEC, HORIZ_SPEC
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject, ArrayObject, FloatObject

DARK, MUTED_DARK, MUTED_CREAM = '.82 .58 .68 .72', '.3 .14 .28 .3', '.52 .34 .42 .28'
NAVY, N_MUTED_DARK, N_MUTED_CREAM = '.94 .78 .38 .52', '.38 .22 .10 .28', '.58 .40 .20 .28'

def recolour(d):
    return (d.replace(DARK, NAVY).replace(MUTED_DARK, N_MUTED_DARK)
             .replace(MUTED_CREAM, N_MUTED_CREAM))

def blocks(d):
    starts = [m.start() for m in re.finditer(r'q\n1 0 0 1 [\d.]+ [\d.]+ cm\n', d)]
    def end(i):
        depth = 0
        for m in re.finditer(r'(?m)^(q|Q)$', d):
            if m.start() < i: continue
            depth += 1 if m.group(1) == 'q' else -1
            if depth == 0: return m.end()
    return [d[s:end(s)] for s in starts]

def move(block, x, y):
    return re.sub(r'^q\n1 0 0 1 [\d.]+ [\d.]+ cm\n',
                  'q\n1 0 0 1 %g %g cm\n' % (x, y), block)

# ---------- horizontal: same 7.9 x 1.9 trim, three per landscape sheet ------
w = PdfWriter(); w.append(PdfReader('source/HORIZONTAL-7.9x1.9.pdf'))
for pg in w.pages:
    d = recolour(pg.get_contents().get_data().decode('latin-1'))
    bs = [apply_spec(b, HORIZ_SPEC) for b in blocks(d)]
    st = DecodedStreamObject()
    st.set_data(('1 0 0 1 0 0 cm  BT /F1 12 Tf 14.4 TL ET\n' + '\n'.join(bs)).encode('latin-1'))
    pg[NameObject('/Contents')] = w._add_object(st)
with open('/tmp/h-v2.pdf', 'wb') as f: w.write(f)

# ---------- vertical: widened to 3 x 8, then elements scaled ---------------
OLD_W, H, NEW_W = 144.0, 576.0, 216.0
SHIFT = (NEW_W - OLD_W) / 2
BG_OLD, BORDER_OLD = 'n 0 0 144 576 re f*', 'n 6.12 6.12 131.76 563.76 re S'
BG_NEW = 'n 0 0 %g %g re f*' % (NEW_W, H)
BORDER_NEW = 'n 6.12 6.12 %g %g re S' % (NEW_W - 12.24, H - 12.24)

def widen(b, x, y):
    b = apply_spec(b, VERT_SPEC)
    head, rest = b.split(BORDER_OLD, 1)
    head = head.replace(BG_OLD, BG_NEW)
    head = re.sub(r'^q\n1 0 0 1 [\d.]+ [\d.]+ cm\n', 'q\n1 0 0 1 %g %g cm\n' % (x, y), head)
    body = rest.rstrip()
    assert body.endswith('Q')
    return '%s%s\nq\n1 0 0 1 %g 0 cm\n%s\nQ\nQ\n' % (head, BORDER_NEW, SHIFT, body[:-1].rstrip('\n'))

LAY = {'3up': dict(page=(792, 612), xs=[36, 288, 540], y=18),
       '2up': dict(page=(612, 792), xs=[60, 336], y=108)}
src = PdfReader('source/VERTICAL-2x8.pdf')
for tag, l in LAY.items():
    w = PdfWriter(); w.append(src)
    for pg in w.pages:
        d = recolour(pg.get_contents().get_data().decode('latin-1'))
        bs = blocks(d)
        out = ['1 0 0 1 0 0 cm  BT /F1 12 Tf 14.4 TL ET\n']
        for i, x in enumerate(l['xs']):
            out.append(widen(bs[i % len(bs)], x, l['y']))
        st = DecodedStreamObject(); st.set_data(''.join(out).encode('latin-1'))
        pg[NameObject('/Contents')] = w._add_object(st)
        pg[NameObject('/MediaBox')] = ArrayObject(
            [FloatObject(0), FloatObject(0), FloatObject(l['page'][0]), FloatObject(l['page'][1])])
    with open('/tmp/v-v2-%s.pdf' % tag, 'wb') as f: w.write(f)
print('built')
