"""Prepress check for the print files.

Measures what actually comes out of the renderer rather than trusting the
source: sheet size, trim size of every card, margins, gaps for the guillotine,
whether any font survived outlining, and whether any colour slipped out of
CMYK. Run it after any change to the artwork.
"""
from pypdf import PdfReader
import pypdfium2 as pdfium
import numpy as np
import glob
import re

DPI = 300
RGB = re.compile(r'[\d.]+ [\d.]+ [\d.]+ (?:rg|RG)\b')
GRAY = re.compile(r'[\d.]+ (?:g|G)\b')
CMYK = re.compile(r'([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) [kK]')


def runs(v):
    out, s = [], None
    for i, on in enumerate(v):
        if on and s is None:
            s = i
        elif not on and s is not None:
            out.append((s, i - 1))
            s = None
    if s is not None:
        out.append((s, len(v) - 1))
    return out


for f in sorted(glob.glob('print/*outlined.pdf')):
    print('=' * 78)
    print(f)
    reader = PdfReader(f)
    pdf = pdfium.PdfDocument(f)
    for i, page in enumerate(reader.pages):
        d = page.get_contents().get_data().decode('latin-1')
        fonts = page.get('/Resources', {}).get('/Font')
        fonts = list(fonts.get_object().keys()) if fonts else []
        tac = max(((sum(float(x) for x in m.groups()) * 100) for m in CMYK.finditer(d)), default=0)

        im = pdf[i].render(scale=DPI / 72).to_pil().convert('RGB')
        a = np.asarray(im).astype(int)
        mask = a.sum(axis=2) < 730
        W, H = im.size
        cw, rh = runs(mask.any(axis=0)), runs(mask.any(axis=1))

        print('  page %d  sheet %.2f x %.2f in  fonts=%s  rgb=%d  gray=%d  max ink=%.0f%%'
              % (i + 1, W / DPI, H / DPI, fonts or 'NONE',
                 len(RGB.findall(d)), len(GRAY.findall(d)), tac))
        for x0, x1 in cw:
            for y0, y1 in rh:
                print('     card %.3f x %.3f in   margins L %.3f R %.3f T %.3f B %.3f'
                      % ((x1 - x0 + 1) / DPI, (y1 - y0 + 1) / DPI,
                         x0 / DPI, (W - 1 - x1) / DPI, y0 / DPI, (H - 1 - y1) / DPI))
        for axis, rr in (('across', cw), ('down', rh)):
            if len(rr) > 1:
                gaps = [(rr[j + 1][0] - rr[j][1] - 1) / DPI for j in range(len(rr) - 1)]
                print('     gaps %s: %s in' % (axis, ', '.join('%.3f' % g for g in gaps)))
