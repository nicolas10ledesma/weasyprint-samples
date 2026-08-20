# Pitch material — NFC review stands

Two printable pieces, rendered with WeasyPrint.

| File | Pages | What it is |
|---|---|---|
| `onepager.html` / `onepager.pdf` | 1 | The leave-behind. Hand it to a manager or supervisor after the demo. |
| `dossier.html` / `dossier.pdf` | 3 | The long version: specs, compliance detail, pricing tiers, how the first job runs. |

Both are US Letter, English, and print fine in black and white.

## Competitor prices

The comparison on page 3 of the dossier uses advertised single-unit prices for
one NFC review card, August 2026:

| Seller | Price |
|---|---|
| ReviewZaps (PVC card) | $24.95 |
| Taps Reviews (from) | $24.99 |
| TAPro Card ($24.90–$29.00, midpoint) | $26.95 |
| TAPiTAG (€24.99, converted) | ~$27.00 |
| OneTap Review (NFC + QR) | $28.05 |
| **Average** | **$26.39** |
| Cheapest listing found anywhere (Etsy) | $16.98 |
| Steel version (Tap On Reviews) | $39.95 |

Against $15 that is 43 % below the average of the five and 12 % below the
cheapest listing found anywhere.

No verified competitor price for an acrylic *stand* was found, so the documents
make no claim about stand pricing — don't add one without a source. Re-check
these before a reprint; they move.

## Rebuild

```sh
pip install weasyprint
weasyprint onepager.html onepager.pdf
weasyprint dossier.html dossier.pdf
```

## Things to edit before printing

- **Name.** Both files sign off as `Gus` — the brand name is still undecided, so nothing is
  branded. One string per file.
- **Prices.** Ready-made / with the customer's logo (+$3 a piece on singles):
  counter stand `$30`/`$33` · check-presenter card `$15`/`$18` · 2 stands `$50`/`$55` ·
  5 cards `$65`/`$80` · 1 stand + 5 cards `$85`/`$100` · 2 stands + 10 cards `$150`/`$175` ·
  4 stands + 20 cards `$280`/`$320`. They live in the price block of each file.
  **The printed price is final** — no sales tax, no fees, no setup charge. Don't add a tax line back in.
- **No free sample left behind, and no second visit.** The demo happens on the spot with the piece
  in hand; the ask is that they buy one that day. Both files close on "start with one stand, $30".
- **Both pieces carry two tap zones** — Google and the second platform. The check-presenter card is
  not Google-only.
- **The offer is product plus one visit** — hardware, configuration and, if paid for, design. No
  follow-up visits, no tap reports, no refund if a piece goes unused. Both files are written that
  way; don't let promises of ongoing service back in.
- **Phone and email** appear in the contact block of each file, plus the running footer of
  `dossier.css` (`@bottom-right`).
- **Logos.** No Google or Yelp logo is used anywhere — only the nominative wording
  "Review us on Google" and "Find us on Yelp", which needs no permission.
