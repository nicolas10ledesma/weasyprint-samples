#!/usr/bin/env sh
# Recolour the dark card and outline the text, in one pass.
#
# The artwork is authored in CMYK. One token in the content stream is the
# brand's dark colour and one is the muted small-print line; swapping those
# two strings recolours the whole piece without touching geometry, logos or
# trim size.  See README.md for the palette.

python3 - <<'PY'
from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject

DARK, MUTED_DARK = '.82 .58 .68 .72', '.3 .14 .28 .3'      # what is in source/
NAVY, NAVY_MUTED = '.94 .78 .38 .52', '.38 .22 .10 .28'
MUTED_CREAM, NAVY_MUTED_CREAM = '.52 .34 .42 .28', '.58 .40 .20 .28'    # what we want

# Page 1 is the dark card, page 2 the cream one. Only page 1 is recoloured;
# the cream card keeps its original ink.
for stem in ['VERTICAL-2x8', 'HORIZONTAL-7.9x1.9']:
    w = PdfWriter()
    w.append(PdfReader('source/%s.pdf' % stem))
    pg = w.pages[0]
    d = pg.get_contents().get_data().decode('latin-1')
    d = d.replace(DARK, NAVY).replace(MUTED_DARK, NAVY_MUTED)
    st = DecodedStreamObject()
    st.set_data(d.encode('latin-1'))
    pg[NameObject('/Contents')] = w._add_object(st)
    with open('/tmp/%s-navy.pdf' % stem, 'wb') as f:
        w.write(f)
PY

for s in VERTICAL-2x8 HORIZONTAL-7.9x1.9; do
  gs -q -o "print/$s-NAVY-outlined.pdf" \
     -sDEVICE=pdfwrite -dNoOutputFonts -dPDFSETTINGS=/prepress -dAutoRotatePages=/None \
     "/tmp/$s-navy.pdf"
done
