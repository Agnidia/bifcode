#!/usr/bin/env python3
"""Compose the 7 App Store screenshots (2880x1800) from windows/winN.png.

Usage: python3 build.py   (needs Google Chrome and network for Google Fonts)
Output: ../screenshots/APP_DESKTOP/0N.png
"""
import os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "screenshots", "APP_DESKTOP")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SHOTS = [
 ("Show what to do.<br>And what not to.", "Turn two snippets into a clear Do and Don't image.", 0.82),
 ("19 languages. One tool.", "From Swift to YAML, with accurate syntax highlighting.", 1.08),
 ("11 themes, dark and light", "Match your docs, slides, or blog.", 1.08),
 ("Badges your way", "Icon, text, or both. Any size, any corner.", 0.9),
 ("Pick any icon", "Checkmarks, stars, thumbs, warnings. Your call.", 1.08),
 ("Side by side or stacked", "Choose the layout that fits your page.", 0.9),
 ("Private by design", "Everything stays on your Mac. Export crisp 2x PNG.", 1.08),
]

HTML = """<!doctype html><meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@500&family=JetBrains+Mono:wght@700&display=swap');
:root{--bg0:#0F172A;--bg1:#1B2336;--fg:#F8FAFC;--muted:#94A3B8;--do:#22C55E;--dont:#EF4444}
*{margin:0;box-sizing:border-box}
html,body{width:2880px;height:1800px;overflow:hidden;background:#0F172A}
body{background:linear-gradient(160deg,var(--bg0) 0%,var(--bg1) 100%);position:relative;font-family:'IBM Plex Sans',sans-serif}
.glow{position:absolute;width:1400px;height:1400px;border-radius:50%;filter:blur(160px);opacity:.22}
.g1{background:var(--dont);left:-500px;bottom:-800px}
.g2{background:var(--do);right:-500px;bottom:-800px}
h1{position:absolute;top:110px;left:0;right:0;text-align:center;font:700 112px/1.08 'JetBrains Mono',monospace;color:var(--fg);letter-spacing:-2px}
p{position:absolute;left:0;right:0;text-align:center;font:500 52px/1.2 'IBM Plex Sans',sans-serif;color:var(--muted)}
.win{position:absolute;left:50%;transform:translateX(-50%);filter:drop-shadow(0 50px 80px rgba(0,0,0,.55)) drop-shadow(0 0 2px rgba(255,255,255,.12))}
</style>
<div class="glow g1"></div><div class="glow g2"></div>
<h1>@@h@@</h1><p style="top:@@ptop@@px">@@p@@</p>
<img class="win" src="file://@@img@@" style="top:@@wtop@@px;width:@@w@@px">
"""

os.makedirs(OUT, exist_ok=True)
for i, (h, p, scale) in enumerate(SHOTS, 1):
    img = os.path.join(HERE, "windows", f"win{i}.png")
    from struct import unpack
    with open(img, "rb") as f:
        f.seek(16); w, ht = unpack(">II", f.read(8))
    w, ht = int(w * scale), int(ht * scale)
    lines = h.count("<br>") + 1
    ptop = 110 + int(112 * 1.08 * lines) + 30
    wtop = ptop + 52 + 70
    wtop = min(wtop, 1800 - ht - 70)
    html = HTML
    for k, v in dict(h=h, p=p, img=img, w=w, ptop=ptop, wtop=wtop).items():
        html = html.replace(f"@@{k}@@", str(v))
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as t:
        t.write(html)
    out = os.path.join(OUT, f"{i:02d}.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=2880,2000", "--virtual-time-budget=8000", f"--screenshot={out}", f"file://{t.name}"],
                   check=True, capture_output=True)
    from PIL import Image
    Image.open(out).crop((0, 0, 2880, 1800)).save(out)
    print(out)
