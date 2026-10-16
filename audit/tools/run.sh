#!/bin/bash
# Run the whole vendor-mention audit for this course repository.
#   AUDIT_WORK=/path/to/scratch  — work dir (default $TMPDIR/vendor-audit); renders and OCR there are reused on re-runs
#   NO_INSTALL=1                 — leave results in $AUDIT_WORK/audit instead of copying them to audit/
#   SKIP_VISUAL=1                — skip rendering/OCR/frames/sheets (reuse what is already in $AUDIT_WORK)
set -euo pipefail
T="$(cd "$(dirname "$0")" && pwd)"
REPO="${AUDIT_REPO:-$(cd "$T/../.." && pwd)}"
export AUDIT_REPO="$REPO"
export AUDIT_WORK="${AUDIT_WORK:-${TMPDIR:-/tmp}/vendor-audit}"
mkdir -p "$AUDIT_WORK"
py() { python3 -I "$T/$1"; }
if [ -z "${SKIP_VISUAL:-}" ]; then
  echo "== 1/5 render + OCR SVG";        "$T/render_svgs.sh"
  echo "== 2/5 OCR rasters";             "$T/ocr_rasters.sh"
  echo "== 3/5 embedded rasters";        py extract_embedded.py
  echo "== 4/5 animation frames";        node "$T/anim_frames.js" || echo "   (skipped: playwright/chromium not available)"
  echo "== 5/5 contact sheets";          py contact_sheets.py || echo "   (skipped: montage not available)"
fi
echo "== docx/pdf text";                 py docs_scan.py
echo "== OCR dictionary pass";           py ocr_scan.py
echo "== text dictionary pass";          py scan.py
echo "== classify";                      py classify.py
echo "== visual/doc/course rows";        py visual_rows.py
echo "== assemble + ledger";             py assemble.py
echo "== report";                        py report.py
echo "== de-marketing tiers";            py plan_tiers.py
if [ -z "${NO_INSTALL:-}" ]; then
  cp "$AUDIT_WORK"/audit/{vendor-mentions.csv,vendor-mentions.md,dictionary-hits.csv,demarketing-tiers.csv} "$REPO/audit/"
  echo "results copied to $REPO/audit/"
else
  echo "results in $AUDIT_WORK/audit/"
fi
