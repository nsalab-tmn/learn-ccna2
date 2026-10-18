# Build labelled contact sheets for the manual visual review (logos, device faces, vendor GUI, icon style).
# In: WORK/render/svg (render_svgs.sh), tracked rasters, WORK/render/anim (anim_frames.js). Out: WORK/sheets/*.png
# Needs ImageMagick `montage`.
import glob, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import REPO, WORK, tracked_files

SHEETS = os.path.join(WORK, "sheets")
os.makedirs(SHEETS, exist_ok=True)


def montage(items, out, tile, geometry, pointsize):
    args = ["montage"]
    for label, path in items:
        args += ["-label", label, path]
    args += (["-tile", tile] if tile else []) + ["-geometry", geometry, "-pointsize", str(pointsize), "-background", "#c8c8c8", out]
    subprocess.run(args, check=True)


svg = sorted(glob.glob(os.path.join(WORK, "render", "svg", "*.png")))
for i in range(0, len(svg), 12):
    items = [(p.split("_assets_")[-1].replace(".svg.png", ""), p) for p in svg[i:i + 12]]
    montage(items, os.path.join(SHEETS, f"svg-{i // 12 + 1:02d}.png"), "4x3", "560x320+6+6", 20)
rasters = [f for f in tracked_files() if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
for i in range(0, len(rasters), 12):
    items = [(f[-46:], os.path.join(REPO, f) + "[0]") for f in rasters[i:i + 12]]
    montage(items, os.path.join(SHEETS, f"raster-{i // 12 + 1:02d}.png"), "4x3", "560x340+6+6", 17)
frames = sorted(glob.glob(os.path.join(WORK, "render", "anim", "*.png")))
keys = sorted({os.path.basename(p).split("__")[0] for p in frames}, key=lambda k: [int(x) if x.isdigit() else x for x in k.replace("-", ".").split(".")])
for i in range(0, len(keys), 3):
    items = [(os.path.basename(p)[:-4], p) for k in keys[i:i + 3] for p in sorted(glob.glob(os.path.join(WORK, "render", "anim", f"{k}__*.png")))]
    montage(items, os.path.join(SHEETS, f"anim-{i // 3 + 1:02d}.png"), "5x3", "400x225+4+4", 14)
emb = sorted(glob.glob(os.path.join(WORK, "render", "embedded", "*")))
if emb:
    montage([(os.path.basename(p), p) for p in emb], os.path.join(SHEETS, "embedded.png"), "", "500x500+8+8", 14)
print(len(os.listdir(SHEETS)), "sheets in", SHEETS)
