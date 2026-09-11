"""Validate projects/*.json and write projects.json for the wall.

Run by the GitHub Action on every push; run it locally with `python scripts/build.py` to check
your entry before pushing. Exits non-zero with a plain message naming the file and the field.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["title", "student", "github", "project", "blurb", "live_url", "site_url", "repo_url", "image", "updated"]
OPTIONAL = ["video_url"]
PROJECTS = {"1", "2", "3", "3a", "3b", "extra"}  # "3a"/"3b" accepted for old entries; use "3"
NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*--[a-z0-9][a-z0-9-]*\.json$")
URL_RE = re.compile(r"^https?://\S+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

errors, entries = [], []
for f in sorted((ROOT / "projects").glob("*.json")):
    if f.name == "README.md":
        continue
    if not NAME_RE.match(f.name):
        errors.append(f"{f.name}: file name must be <github-username>--<slug>.json, lowercase, hyphens only")
        continue
    try:
        d = json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"{f.name}: not valid JSON ({e.msg} at line {e.lineno})")
        continue
    if not isinstance(d, dict):
        errors.append(f"{f.name}: must be one JSON object")
        continue
    for k in REQUIRED:
        if k not in d:
            errors.append(f"{f.name}: missing field '{k}'")
    unknown = set(d) - set(REQUIRED) - set(OPTIONAL)
    if unknown:
        errors.append(f"{f.name}: unknown field(s) {sorted(unknown)}")
    if any(k not in d for k in REQUIRED):
        continue
    if f.name.split("--")[0] != str(d["github"]).lower():
        errors.append(f"{f.name}: file name must start with the github username '{d['github']}'")
    if str(d["project"]) not in PROJECTS:
        errors.append(f"{f.name}: 'project' must be one of {sorted(PROJECTS)}")
    for k in ("live_url", "site_url", "repo_url", "video_url"):
        v = d.get(k, "")
        if v and not URL_RE.match(v):
            errors.append(f"{f.name}: '{k}' must be a full http(s) URL or empty")
    if not d["site_url"] or not d["repo_url"]:
        errors.append(f"{f.name}: 'site_url' and 'repo_url' are required (the project website and the repository)")
    if not DATE_RE.match(str(d["updated"])):
        errors.append(f"{f.name}: 'updated' must be YYYY-MM-DD")
    if not (1 <= len(str(d["blurb"])) <= 400):
        errors.append(f"{f.name}: 'blurb' must be 1–400 characters")
    img = str(d["image"])
    if img:
        if not re.match(r"^images/[\w.\-]+\.(png|jpe?g|gif|webp|mp4|webm)$", img):
            errors.append(f"{f.name}: 'image' must be images/<name>.(png|jpg|gif|webp|mp4|webm)")
        elif not (ROOT / img).exists():
            errors.append(f"{f.name}: image file '{img}' is not in the repository — commit it too")
        elif (ROOT / img).stat().st_size > 8 * 1024 * 1024:
            errors.append(f"{f.name}: image '{img}' is over 8 MB — shrink it")
    d["project"] = str(d["project"])
    d.setdefault("video_url", "")
    entries.append(d)

if errors:
    print("projects.json NOT built — fix these:\n  " + "\n  ".join(errors))
    sys.exit(1)

entries.sort(key=lambda d: (d["updated"], d["title"]), reverse=True)
(ROOT / "projects.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"projects.json: {len(entries)} entries")
