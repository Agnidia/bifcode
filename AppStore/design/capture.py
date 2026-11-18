#!/usr/bin/env python3
"""Capture Bifcode window PNGs for the App Store screenshots.

Usage: capture.py [shot numbers...]  (default: all)
Needs: a built Bifcode.app, Accessibility permission, and the click/winid helpers
compiled from click.swift / winid.swift (path in HELPERS).
"""
import json, os, subprocess, sys, time

D = "com.igrsoft.bifcode"
HELPERS = os.environ["HELPERS"]
OUT = os.environ["OUT"]
APP = os.environ["APP"]

SHOTS = {
 1: dict(lang="swift", theme="xcode-default", mode="dark", layout="vertical", pos="bottom-right", style="both",
         dont_icon="xmark", do_icon="checkmark", dont_label="Don'ts", do_label="Do's", dont_title="Don'ts", do_title="Do's",
         font=16, size=64, titles=True,
         bad='func name(_ u: User?) -> String {\n    return u!.name\n}',
         good='func name(_ u: User?) -> String {\n    guard let u else { return "" }\n    return u.name\n}'),
 2: dict(lang="python", theme="dracula", mode="dark", layout="horizontal", pos="top-right", style="both",
         dont_icon="xmark.circle", do_icon="checkmark.circle", dont_label="Don'ts", do_label="Do's", dont_title="Don'ts", do_title="Do's",
         font=16, size=56, titles=True,
         bad='squares = []\nfor n in numbers:\n    squares.append(n * n)',
         good='squares = [n * n for n in numbers]'),
 3: dict(lang="typescript", theme="github-light", mode="light", layout="horizontal", pos="bottom-right", style="icon",
         dont_icon="hand.thumbsdown", do_icon="hand.thumbsup", dont_label="Don'ts", do_label="Do's", dont_title="Don'ts", do_title="Do's",
         font=16, size=80, titles=True,
         bad='function parse(data: any) {\n  return data.items\n}',
         good='function parse(data: Response) {\n  return data.items\n}'),
 4: dict(lang="rust", theme="nord", mode="dark", layout="vertical", pos="bottom-right", style="text",
         dont_icon="xmark", do_icon="checkmark", dont_label="Bad", do_label="Good", dont_title="Bad", do_title="Good",
         font=16, size=64, titles=True,
         bad='let n = s.parse::<i32>().unwrap();',
         good='let n = s.parse::<i32>()?;'),
 5: dict(lang="go", theme="monokai", mode="dark", layout="horizontal", pos="bottom-right", style="both",
         dont_icon="exclamationmark.triangle", do_icon="star.fill", dont_label="Don'ts", do_label="Do's", dont_title="Don'ts", do_title="Do's",
         font=18, size=56, titles=True,
         bad='data, _ := os.ReadFile(path)',
         good='data, err := os.ReadFile(path)\nif err != nil {\n    return err\n}'),
 6: dict(lang="sql", theme="solarized-light", mode="light", layout="vertical", pos="bottom-right", style="icon",
         dont_icon="xmark.square", do_icon="checkmark.square", dont_label="Don'ts", do_label="Do's", dont_title="Don'ts", do_title="Do's",
         font=16, size=64, titles=True,
         bad='SELECT * FROM users;',
         good='SELECT id, name, email\nFROM users\nWHERE active = 1;'),
 7: dict(lang="kotlin", theme="atom-one-dark", mode="dark", layout="horizontal", pos="top-right", style="both",
         dont_icon="xmark", do_icon="checkmark", dont_label="No", do_label="Yes", dont_title="Don'ts", do_title="Do's",
         font=16, size=56, titles=False,
         bad='val len = name!!.length',
         good='val len = name?.length ?: 0'),
}

def sh(*a, **k):
    return subprocess.run(a, check=True, capture_output=True, text=True, **k).stdout.strip()

def osa(script):
    return sh("osascript", "-e", script)

def click(x, y):
    sh(f"{HELPERS}/click", str(x), str(y))

def paste(text):
    subprocess.run(["pbcopy"], input=text, text=True, check=True)
    time.sleep(0.2)
    osa('tell application "System Events" to keystroke "v" using command down')
    time.sleep(0.6)

def run(n):
    s = SHOTS[n]
    subprocess.run(["osascript", "-e", 'tell application "Bifcode" to quit'], capture_output=True)
    time.sleep(1.5)
    subprocess.run(["defaults", "delete", D], capture_output=True)
    w = lambda k, t, v: sh("defaults", "write", D, k, t, str(v))
    w("selectedLanguage", "-string", s["lang"]); w("selectedTheme", "-string", s["theme"]); w("themeMode", "-string", s["mode"])
    w("windowLayout", "-string", s["layout"]); w("indicatorPosition", "-string", s["pos"]); w("indicatorStyle", "-string", s["style"])
    w("doIndicatorIcon", "-string", s["do_icon"]); w("dontIndicatorIcon", "-string", s["dont_icon"])
    w("doIndicatorLabel", "-string", s["do_label"]); w("dontIndicatorLabel", "-string", s["dont_label"])
    w("doTitle", "-string", s["do_title"]); w("dontTitle", "-string", s["dont_title"])
    w("fontSize", "-float", s["font"]); w("indicatorSize", "-float", s["size"]); w("showTitle", "-bool", "YES" if s["titles"] else "NO")
    w("hasMadePurchase", "-bool", "NO")
    sh("open", APP); time.sleep(3.5)
    stacked = s["layout"] == "vertical"
    W, H = (900, 680) if stacked else (1000, 560)
    X, Y = 120, 40
    osa(f'tell application "System Events" to tell process "Bifcode"\nset frontmost to true\nset position of window 1 to {{{X}, {Y}}}\nset size of window 1 to {{{W}, {H}}}\nend tell')
    time.sleep(1.2)
    if stacked:
        pts = [(X + 360, Y + 380), (X + 360, Y + 560)]
    else:
        pts = [(X + 270, Y + 400), (X + 730, Y + 400)]
    for (x, y), code in zip(pts, [s["bad"], s["good"]]):
        click(x, y); time.sleep(0.4); paste(code)
    click(X + 165, Y + 55); time.sleep(0.8)
    wid = sh(f"{HELPERS}/winid")
    for k in range(6):
        sh("screencapture", "-x", "-o", "-l", wid, f"{OUT}/win{n}_{k}.png")
        time.sleep(0.27)
    print(n)

if __name__ == "__main__":
    for n in ([int(a) for a in sys.argv[1:]] or SHOTS):
        run(n)
    subprocess.run(["osascript", "-e", 'tell application "Bifcode" to quit'], capture_output=True)
