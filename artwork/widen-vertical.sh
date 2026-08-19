#!/usr/bin/env sh
# Rebuild the vertical piece 3 in wide instead of 2 in, then outline the text.
#
# The card is redrawn one inch wider and the whole artwork is translated half
# an inch to the right so it stays centred — nothing is scaled, so the tap
# zones keep their exact heights and the type keeps its exact size.
#
# Two impositions come out of it:
#   3up  landscape, three cards per Letter sheet, 0.25 in margin top and bottom
#   2up  portrait,  two cards per Letter sheet,  1.5 in margins (use this one
#        if your printer clips the 3up)

python3 recolour-widen.py
for t in 3up 2up; do
  gs -q -o "print/VERTICAL-3x8-NAVY-$t-outlined.pdf" \
     -sDEVICE=pdfwrite -dNoOutputFonts -dPDFSETTINGS=/prepress -dAutoRotatePages=/None \
     "/tmp/vert3x8-$t.pdf"
done
