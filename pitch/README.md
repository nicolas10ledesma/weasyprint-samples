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
- **Prices.** `$79` / `$149` / `$25` live in the price blocks. The research put the sustainable
  range at $49–79 for the counter piece and $129–179 for the set.
- **Phone and email** appear in the contact block of each file, plus the running footer of
  `dossier.css` (`@bottom-right`).
- **Logos.** No Google or Yelp logo is used anywhere — only the nominative wording
  "Review us on Google" and "Find us on Yelp", which needs no permission.
