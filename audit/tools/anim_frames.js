// Capture frames of each animated SVG (SMIL) at 12/32/52/72/92 % of its timeline for visual review.
// Usage: node anim_frames.js [outDir]   (default: $AUDIT_WORK/render/anim)
// Needs the `playwright` npm package; set CHROMIUM_PATH to use a preinstalled Chromium.
const path = require('path');
const fs = require('fs');
let chromium;
try { ({ chromium } = require('playwright')); }
catch (e) { ({ chromium } = require(process.env.PLAYWRIGHT_MODULE || '/opt/node-tools/node_modules/playwright')); }
const REPO = process.env.AUDIT_REPO || path.resolve(__dirname, '..', '..');
const WORK = process.env.AUDIT_WORK || path.join(process.env.TMPDIR || '/tmp', 'vendor-audit');
const OUT = process.argv[2] || path.join(WORK, 'render', 'anim');
fs.mkdirSync(OUT, { recursive: true });
const manifest = JSON.parse(fs.readFileSync(path.join(REPO, 'figma-assets.json'), 'utf8'));
(async () => {
  const opts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
  const browser = await chromium.launch(opts);
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  for (const a of manifest.assets.filter(x => x.kind === 'animation')) {
    const spec = JSON.parse(fs.readFileSync(path.join(REPO, 'animations', a.id, 'spec.json'), 'utf8'));
    const dur = spec.duration || 30;
    await page.goto('file://' + path.join(REPO, a.out.path));
    await page.waitForTimeout(500);
    for (const f of [0.12, 0.32, 0.52, 0.72, 0.92]) {
      const t = f * dur * 1000;
      await page.evaluate((t) => { const r = document.documentElement; r.pauseAnimations(); r.setCurrentTime(t / 1000); }, t);
      await page.waitForTimeout(150);
      await page.screenshot({ path: path.join(OUT, `${a.display.key}__${String(Math.round(f * 100)).padStart(2, '0')}.png`) });
    }
    console.log(a.display.key, dur, await page.evaluate(() => document.querySelectorAll('animate,animateTransform,animateMotion,set').length));
  }
  await browser.close();
})();
