# -*- coding: utf-8 -*-
"""Replay transcript StrReplace/Write ops onto home.css / home.js / home-v2.css."""
import json
from pathlib import Path

ROOT = Path(r"c:\Users\hp\Desktop\yaw-studio-website (3)0\yaw-studio")
TRANS = Path(r"C:\Users\hp\.cursor\projects\c-Users-hp-Desktop-yaw-studio-website-3-0-yaw-studio\agent-transcripts\91301ce8-2820-4d42-a830-410d3df7fab8\91301ce8-2820-4d42-a830-410d3df7fab8.jsonl")

TARGETS = {
    str(ROOT / "assets" / "home.css").replace("\\", "/").lower(): ROOT / "assets" / "home.css",
    str(ROOT / "assets" / "home.js").replace("\\", "/").lower(): ROOT / "assets" / "home.js",
    str(ROOT / "assets" / "home-v2.css").replace("\\", "/").lower(): ROOT / "assets" / "home-v2.css",
    str(ROOT / "assets" / "home-v2.js").replace("\\", "/").lower(): ROOT / "assets" / "home-v2.js",
}

files = {p: (p.read_text(encoding="utf-8") if p.exists() else "") for p in set(TARGETS.values())}
# start home.css/js from current (reverted) copies
counts = {p: {"write": 0, "ok": 0, "miss": 0} for p in files}

def norm_path(p):
    return p.replace("\\", "/").lower()

ops = []
with TRANS.open(encoding="utf-8") as f:
    for line in f:
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        content = obj.get("message", {}).get("content")
        if not isinstance(content, list):
            continue
        for part in content:
            if not isinstance(part, dict) or part.get("type") != "tool_use":
                continue
            name = part.get("name")
            inp = part.get("input") or {}
            path = inp.get("path")
            if not path:
                continue
            key = norm_path(path)
            if key not in TARGETS:
                continue
            dest = TARGETS[key]
            if name == "Write":
                files[dest] = inp.get("contents", "")
                counts[dest]["write"] += 1
                ops.append(("WRITE", dest.name, len(files[dest])))
            elif name == "StrReplace":
                old = inp.get("old_string", "")
                new = inp.get("new_string", "")
                text = files[dest]
                n = text.count(old)
                if n == 0:
                    counts[dest]["miss"] += 1
                    ops.append(("MISS", dest.name, old[:60].replace("\n", " ")))
                else:
                    replace_all = bool(inp.get("replace_all"))
                    if replace_all:
                        files[dest] = text.replace(old, new)
                    else:
                        files[dest] = text.replace(old, new, 1)
                    counts[dest]["ok"] += 1
                    ops.append(("OK", dest.name, old[:40].replace("\n", " ")))

out_dir = ROOT / "_restored"
out_dir.mkdir(exist_ok=True)
for dest, text in files.items():
    (out_dir / dest.name).write_text(text, encoding="utf-8")
    print(dest.name, "bytes", len(text.encode("utf-8")), counts[dest])

print("--- last 20 ops ---")
for o in ops[-20:]:
    print(o)
print("total ops", len(ops))
print("reelrow in css", "reelrow" in files[ROOT / "assets" / "home.css"])
print("endcard-lux in css", "endcard-lux" in files[ROOT / "assets" / "home.css"])
print("credits-marq in css", "credits-marq" in files[ROOT / "assets" / "home.css"])
print("filmReel in js", "filmReel" in files[ROOT / "assets" / "home.js"])
