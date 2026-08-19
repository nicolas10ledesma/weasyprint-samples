# Pitch material — NFC review stands

Two printable pieces, rendered with WeasyPrint.

| File | Pages | What it is |
|---|---|---|
| `onepager.html` / `onepager.pdf` | 1 | The leave-behind. Hand it to a manager or supervisor after the demo. |
| `dossier.html` / `dossier.pdf` | 3 | The long version: specs, compliance detail, pricing tiers, how the first job runs. |

Both are US Letter, English, and print fine in black and white.

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
- **The offer is product plus one visit** — hardware, configuration and, if paid for, design. No
  follow-up visits, no tap reports, no refund if a piece goes unused. Both files are written that
  way; don't let promises of ongoing service back in.
- **Phone and email** appear in the contact block of each file, plus the running footer of
  `dossier.css` (`@bottom-right`).
- **Logos.** No Google or Yelp logo is used anywhere — only the nominative wording
  "Review us on Google" and "Find us on Yelp", which needs no permission.
