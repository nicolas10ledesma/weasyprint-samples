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
| `print/HORIZONTAL-8x2-NAVY-outlined.pdf` | **Counter insert, 8 × 2 in** — full size for the acrylic holder. Three per landscape sheet. |
| `print/VERTICAL-3x8-NAVY-3up-outlined.pdf` | **Check-presenter card, 3 × 8 in.** Three per landscape sheet. |
| `print/VERTICAL-3x8-NAVY-2up-outlined.pdf` | Same card, two per portrait sheet, for a printer that clips the 3up. |
| `print/COUNTER-SIGN-5x7-NAVY-outlined.pdf` | **Counter sign, 5 × 7 in** — the single upright piece for a business with only one spot. Two per landscape sheet. |
| `archive/` | The original green files. Kept for reference, not for printing. |

## Element sizes

**Horizontal.** The acrylic holder is 8 × 2 in, so the insert is 8 × 2 and fills
it edge to edge instead of leaving a white margin inside the holder. Only the
card grew — every element keeps its original size.

**Vertical.** The art was drawn for a 2-inch-wide card and did not grow when the
card went to 3 inches, so the logos and the centre type read small. `enlarge.py`
scales each element about its own centre; text is re-centred from the real
advance widths of the fonts embedded in the source PDF, not by eye. A first pass
went much further and crowded the card — it is kept in `enlarge.py` as
`_FIRST_TRY_TOO_BIG` so the same mistake isn't repeated.

| Vertical | Was | Now |
|---|---|---|
| Google logo | 13.6 mm | 18.4 mm |
| Yelp logo | 12.2 mm | 16.6 mm |
| NFC ring | 14.8 mm | 17.0 mm |
| "TAP TO REVIEW" | 6.8 pt | 8.0 pt |
| "ONE TAP / NO APP" | 6.6 pt | 7.6 pt |
| "How did we do?" | 20 pt | 23 pt |

The logos went up a second time, from 17.0 to 18.4 mm, on their own — the ring
and the type were already right, so only the two `img` scales moved.

Tap-zone positions are untouched and both sheets still yield three cards.

## The 5 × 7 counter sign

For a café or an ice cream shop that will only ever put one piece beside the
register, the 8 × 2 strip reads as an afterthought. `build-sign.py` lays the same
artwork out upright at 5 × 7 in — the standard photo-frame size, so slant-back
acrylic holders for it are everywhere and cheap in six-packs.

A4 was considered and rejected: on a small counter a full page reads as
advertising and managers push back on the footprint. 5 × 7 keeps the presence
without taking the counter over. 5.5 × 8.5 (half letter) is the step up if more
presence is ever wanted — it also cuts two per sheet with no waste.

The two tap zones end up **4.6 in apart**, centre to centre. An NTAG213 reads at
about 4 cm, so anything past roughly 3 in makes it impossible for a phone held to
one zone to pick up the other. There is a lot of margin here.

Type on this piece: headline 35 pt, "TAP TO REVIEW" 11.5 pt, the muted line
10.3 pt, logos 23 mm, NFC ring 22 mm.

## Colours

| Role | CMYK |
|---|---|
| Midnight navy — background on the dark card, ink on the cream one | 94 · 78 · 38 · 52 |
| Muted line, on the navy card | 38 · 22 · 10 · 28 |
| Muted line, on the cream card | 58 · 40 · 20 · 28 |
| Dark green (original, retired) | 82 · 58 · 68 · 72 |
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

## Checking the files

`verify.py` renders every file in `print/` at 300 dpi and measures the sheet,
the trim size of each card, the margins and the guillotine gaps, and confirms
no font survived outlining and no colour fell out of CMYK. Measured today:

| File | Trim | Per sheet | Tightest margin | Gap to cut in |
|---|---|---|---|---|
| `HORIZONTAL-8x2-NAVY` | 8.003 × 2.000 in | 3 | 0.623 in | 0.627 in |
| `VERTICAL-3x8-NAVY-3up` | 3.003 × 8.000 in | 3 | 0.250 in | 0.497 in |
| `VERTICAL-3x8-NAVY-2up` | 3.000 × 8.003 in | 2 | 0.833 in | 0.833 in |

Both pages of each file measure identically, so a dark piece and a cream piece
from the same set trim to the same size.

Contrast, both cards (WCAG ratio against their own background): headline
**15.4 : 1**, muted "ONE TAP" line **4.9 : 1**, gold **7.0 : 1** on navy and
**2.2 : 1** on cream. The gold is decorative on the cream card, not something a
guest has to read at arm's length; everything that carries meaning clears 4.5.

Ink coverage peaks at **262 %** on the navy, down from 280 % on the green it
replaced — comfortably inside what a digital press or a laser will hold.

**There is no bleed.** The colour stops exactly on the trim line, so a cut that
drifts outward leaves a white sliver along a dark card. Cutting half a
millimetre *inside* the card avoids it and nobody can tell. A bleed-and-crop-marks
version is only worth making for a commercial shop that trims for you.

## Reprint checklist

- Scale **100 %**, never "fit to page". Measure the first sheet: the horizontal
  must come out 7.9 in wide.
- Cardstock 14 pt (~250 g/m²) or heavier, so the NFC inlay doesn't telegraph
  through the paper.
- The 3up vertical sheet leaves only 0.25 in above and below the cards. Print one
  sheet and check nothing is clipped before running the batch; if it is, use the
  2up file instead.
- Ask for a **proof on the actual stock** before the full run. Dark backgrounds
  shift a lot between screen and paper.
