#!/usr/bin/env sh
# Convert every glyph in the artwork to vector outlines.
# The press RIP that printed the first batch substituted the subsetted
# Playfair Display and Jost fonts and dropped glyphs ("How did we do?" came
# out as "H□d□d □e d□?"). Outlined text carries no font at all, so there is
# nothing left to substitute.

for f in VERTICAL-2x8 HORIZONTAL-7.9x1.9; do
  gs -q -o "print/$f-outlined.pdf" \
     -sDEVICE=pdfwrite \
     -dNoOutputFonts \
     -dPDFSETTINGS=/prepress \
     -dAutoRotatePages=/None \
     "source/$f.pdf"
done

# Verify: this must print nothing but "NONE" for each file.
python3 - <<'PY'
from pypdf import PdfReader
import glob
for n in sorted(glob.glob('print/*-outlined.pdf')):
    fonts = set()
    for pg in PdfReader(n).pages:
        fo = pg.get('/Resources', {}).get('/Font')
        if fo:
            for k, v in fo.get_object().items():
                fonts.add(str(v.get_object().get('/BaseFont')))
    print(n, '->', fonts or 'NONE')
PY
