#!/bin/sh
# Renders the sales material to PDF with WeasyPrint.
#   pip install weasyprint && ./build.sh
set -e
cd "$(dirname "$0")"
python3 -m weasyprint one-pager.html one-pager.pdf
python3 -m weasyprint presentation-3pages.html presentation-3pages.pdf
echo "one-pager.pdf and presentation-3pages.pdf written"
