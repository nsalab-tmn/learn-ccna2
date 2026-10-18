#!/bin/bash
# Render every tracked SVG (outside audit/) to PNG on white and OCR it (eng+rus).
# Needs: rsvg-convert (librsvg2-bin), tesseract + tesseract-ocr-rus.
set -u
export OMP_THREAD_LIMIT=1   # tesseract is ~100x slower when its OpenMP threads compete under xargs -P
REPO="${AUDIT_REPO:-$(cd "$(dirname "$0")/../.." && pwd)}"
S="${AUDIT_WORK:-${TMPDIR:-/tmp}/vendor-audit}"
mkdir -p "$S/out" "$S/render/svg" "$S/ocr"
cd "$REPO"
git ls-files '*.svg' | grep -v '^audit/' > "$S/out/svg-list.txt"
render() {
  f="$1"; S="$2"
  name=$(echo "$f" | tr '/' '_')
  out="$S/render/svg/$name.png"
  [ -s "$out" ] || timeout 300 rsvg-convert -b white -w 1600 "$f" -o "$out" 2>>"$S/out/render-errors.log" || echo "FAIL $f" >> "$S/out/render-errors.log"
  [ -s "$S/ocr/svg__$name.txt" ] || timeout 300 tesseract "$out" "$S/ocr/svg__$name" -l eng+rus --psm 11 >/dev/null 2>&1
}
export -f render
xargs -P 3 -I{} bash -c 'render "$@"' _ {} "$S" < "$S/out/svg-list.txt"
echo "rendered $(ls "$S/render/svg" | wc -l) / $(wc -l < "$S/out/svg-list.txt")"
