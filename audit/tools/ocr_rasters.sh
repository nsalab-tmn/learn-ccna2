#!/bin/bash
# OCR every tracked raster (outside audit/): GIFs → first frame, images narrower than 1200 px upscaled ×2.
# Needs: ImageMagick (convert, identify), tesseract + tesseract-ocr-rus.
set -u
export OMP_THREAD_LIMIT=1
REPO="${AUDIT_REPO:-$(cd "$(dirname "$0")/../.." && pwd)}"
S="${AUDIT_WORK:-${TMPDIR:-/tmp}/vendor-audit}"
mkdir -p "$S/out" "$S/render/raster" "$S/ocr_raster"
cd "$REPO"
git ls-files | grep -iE '\.(png|jpe?g|gif)$' | grep -v '^audit/' > "$S/out/raster-list.txt"
doit() {
  f="$1"; S="$2"; name=$(echo "$f" | tr '/' '_')
  src="$f"
  case "${f,,}" in *.gif) convert "$f[0]" "$S/render/raster/$name.png" 2>/dev/null; src="$S/render/raster/$name.png";; esac
  w=$(identify -format '%w' "$src" 2>/dev/null | head -1)
  if [ -n "$w" ] && [ "$w" -lt 1200 ]; then convert "$src" -resize 200% "$S/render/raster/$name.ocr.png"; src="$S/render/raster/$name.ocr.png"; fi
  timeout 300 tesseract "$src" "$S/ocr_raster/$name" -l eng+rus --psm 11 >/dev/null 2>&1
}
export -f doit
xargs -P 3 -I{} bash -c 'doit "$@"' _ {} "$S" < "$S/out/raster-list.txt"
echo "ocr $(ls "$S/ocr_raster" | wc -l) / $(wc -l < "$S/out/raster-list.txt")"
