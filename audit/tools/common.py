# Shared paths for the vendor-mention audit pipeline.
#   REPO  — course repository root (two levels above this file, or $AUDIT_REPO)
#   WORK  — scratch directory for renders, OCR and intermediate JSON ($AUDIT_WORK, default $TMPDIR/vendor-audit)
#   OUT   — WORK/out (intermediate JSON); AUD — WORK/audit (final CSV/MD before they are copied to REPO/audit)
import os, subprocess

REPO = os.environ.get("AUDIT_REPO") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
WORK = os.environ.get("AUDIT_WORK") or os.path.join(os.environ.get("TMPDIR", "/tmp"), "vendor-audit")
OUT = os.path.join(WORK, "out")
AUD = os.path.join(WORK, "audit")
for d in (OUT, AUD):
    os.makedirs(d, exist_ok=True)


def tracked_files():
    """git ls-files of the course, without audit/ (the audit's own outputs and tools are not course content)."""
    return [f for f in subprocess.check_output(["git", "-C", REPO, "ls-files"]).decode().splitlines()
            if not f.startswith("audit/")]
