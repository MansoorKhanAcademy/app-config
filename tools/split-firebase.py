#!/usr/bin/env python3
"""Split a Firebase Realtime Database export (JSON) into per-app config files.

Usage:  python3 tools/split-firebase.py export.json prompt-book

Writes  <app>/prompts.json, ads.json, update.json, moreApps.json,
        banners.json, newCategories.json   (only the parts that exist).
Firebase export format: {"prompts": [...], "settings": {"ads": {...}, ...}}
"""
import json, os, sys

if len(sys.argv) != 3:
    sys.exit(__doc__)
src, app = sys.argv[1], sys.argv[2]
data = json.load(open(src, encoding="utf-8"))
os.makedirs(app, exist_ok=True)

def clean(v):
    # Firebase turns arrays with holes into objects/None; drop empty rows
    if isinstance(v, list):
        return [x for x in v if x]
    return v

def write(name, value):
    with open(os.path.join(app, name + ".json"), "w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote", os.path.join(app, name + ".json"))

if "prompts" in data:
    write("prompts", clean(data["prompts"]))
for k, v in (data.get("settings") or {}).items():
    write(k, v)
