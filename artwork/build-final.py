"""Build the print files.

Horizontal: the acrylic sign holder is 8 x 2 in, so the insert is 8 x 2 —
edge to edge, no white margin showing inside the holder. Element sizes are the
original ones; only the card grew.

Vertical: 3 x 8 in, with the logos, the NFC rings and the centre type scaled up
moderately (see VERT_SPEC in enlarge.py).
"""
import sys, re
sys.path.insert(0, '.')
from enlarge import apply_spec, VERT_SPEC
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
            if m.start() < i:
                continue
            depth += 1 if m.group(1) == 'q' else -1
            if depth == 0:
                return m.end()
    return [d[s:end(s)] for s in starts]


def resize(block, bg_old, border_old, new_w, new_h, old_w, old_h, x, y, spec=None):
    """Redraw the card at a new trim and recentre its contents. No scaling."""
    if spec:
        block = apply_spec(block, spec)
    bg_new = 'n 0 0 %g %g re f*' % (new_w, new_h)
    border_new = 'n 6.12 6.12 %g %g re S' % (new_w - 12.24, new_h - 12.24)
    head, rest = block.split(border_old, 1)
    head = head.replace(bg_old, bg_new)
    head = re.sub(r'^q\n1 0 0 1 [\d.]+ [\d.]+ cm\n', 'q\n1 0 0 1 %g %g cm\n' % (x, y), head)
    body = rest.rstrip()
    assert body.endswith('Q')
    dx, dy = (new_w - old_w) / 2.0, (new_h - old_h) / 2.0
    return '%s%s\nq\n1 0 0 1 %g %g cm\n%s\nQ\nQ\n' % (
        head, border_new, dx, dy, body[:-1].rstrip('\n'))


def sheet(src_path, out_path, page, placements, resize_args, spec=None):
    src = PdfReader(src_path)
    w = PdfWriter()
    w.append(src)
    for pg in w.pages:
        d = recolour(pg.get_contents().get_data().decode('latin-1'))
        bs = blocks(d)
        out = ['1 0 0 1 0 0 cm  BT /F1 12 Tf 14.4 TL ET\n']
        for i, (x, y) in enumerate(placements):
            out.append(resize(bs[i % len(bs)], *resize_args, x=x, y=y, spec=spec))
        st = DecodedStreamObject()
        st.set_data(''.join(out).encode('latin-1'))
        pg[NameObject('/Contents')] = w._add_object(st)
        pg[NameObject('/MediaBox')] = ArrayObject(
            [FloatObject(0), FloatObject(0), FloatObject(page[0]), FloatObject(page[1])])
    with open(out_path, 'wb') as f:
        w.write(f)


# --- horizontal: 7.9 x 1.9  ->  8 x 2, three per landscape sheet -----------
sheet('source/HORIZONTAL-7.9x1.9.pdf', '/tmp/h-8x2.pdf',
      page=(792, 612), placements=[(108, 45), (108, 234), (108, 423)],
      resize_args=('n 0 0 568.8 136.8 re f*', 'n 6.12 6.12 556.56 124.56 re S',
                   576.0, 144.0, 568.8, 136.8))

# --- vertical: 2 x 8 -> 3 x 8, elements scaled moderately ------------------
V_ARGS = ('n 0 0 144 576 re f*', 'n 6.12 6.12 131.76 563.76 re S', 216.0, 576.0, 144.0, 576.0)
sheet('source/VERTICAL-2x8.pdf', '/tmp/v-3up.pdf', page=(792, 612),
      placements=[(36, 18), (288, 18), (540, 18)], resize_args=V_ARGS, spec=VERT_SPEC)
sheet('source/VERTICAL-2x8.pdf', '/tmp/v-2up.pdf', page=(612, 792),
      placements=[(60, 108), (336, 108)], resize_args=V_ARGS, spec=VERT_SPEC)
print('built')
