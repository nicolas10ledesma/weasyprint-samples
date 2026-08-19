# Artwork — NFC review pieces

## What went wrong on the first print run

The press printed `How did we do?` as `H□d□d □e d□?`. The tofu boxes are the
`.notdef` glyph: the RIP could not use the fonts the PDF carried.

The PDFs themselves are not corrupt — they render correctly in Chrome, Preview,
Acrobat and pdfium here. The embedded fonts are **subsets** of Playfair Display
and Jost that carry only a Mac Roman `(1,0)` cmap and generic `glyph000NN`
names. Plenty of RIPs want a Windows Unicode `(3,1)` cmap; when they don't find
one they substitute the font, and the substitute has no matching glyphs.

## The fix

`outline.sh` converts every glyph to vector paths. An outlined PDF carries no
font, so there is nothing left for a RIP to substitute — it draws shapes. This
is the standard prepress answer and any shop will take it.

The colours stay in **CMYK** (they were authored in CMYK; Ghostscript is run
with pdfwrite's default `LeaveColorUnchanged`), and the trim sizes are
untouched: 7.9 × 1.9 in horizontal, 2 × 8 in vertical, three up per US Letter
sheet, dark version on page 1 and cream on page 2.

## Files

| Path | What it is |
|---|---|
| `source/` | The two PDFs as they came out of the design tool. Do not send these to a printer. |
| `print/HORIZONTAL-7.9x1.9-outlined.pdf` | Counter piece, text outlined. **Send this one.** |
| `print/VERTICAL-2x8-outlined.pdf` | Check-presenter piece, text outlined. **Send this one.** |
| `print/HORIZONTAL-7.9x1.9-NAVY-outlined.pdf` | **Current counter piece.** Dark side in midnight navy, cream side untouched. |
| `print/VERTICAL-2x8-NAVY-outlined.pdf` | **Current check-presenter piece.** Same. |
| `print/COLOR-OPTIONS.pdf` | The four dark colourways at real size. Midnight navy was chosen. |
| `print/CREAM-INK-CHECK.pdf` | The cream card in green ink and in navy ink, side by side — open question. |

## Colours

| Role | CMYK |
|---|---|
| Midnight navy (chosen, dark side) | 94 · 78 · 38 · 52 |
| Muted line on navy | 38 · 22 · 10 · 28 |
| Dark green (original; still the ink on the cream side) | 82 · 58 · 68 · 72 |
| Gold | 16 · 32 · 95 · 5 |
| Cream | 2 · 3 · 10 · 0 |
| Muted line, on dark | 30 · 14 · 28 · 30 |
| Muted line, on cream | 52 · 34 · 42 · 28 |

`recolour.sh` does the swap and the outlining in one pass. The other candidates
from the options sheet, background then the muted line that goes with it:

| Name | Background | Muted line |
|---|---|---|
| Midnight navy | 94 · 78 · 38 · 52 | 38 · 22 · 10 · 28 |
| Graphite black | 66 · 56 · 52 · 84 | 26 · 20 · 20 · 34 |
| Oxblood | 40 · 94 · 68 · 55 | 20 · 38 · 30 · 30 |
| Espresso | 48 · 70 · 82 · 68 | 26 · 32 · 42 · 30 |

The dark colour is also the ink colour on the cream version (page 2), so
changing it changes both sides of the set.

## Reprint checklist

- Scale **100 %**, never "fit to page". Measure the first sheet: the horizontal
  must come out 7.9 in wide.
- Cardstock 14 pt (~250 g/m²) or heavier, so the NFC inlay doesn't telegraph
  through the paper.
- Ask for a **proof on the actual stock** before the full run. Dark backgrounds
  shift a lot between screen and paper.
