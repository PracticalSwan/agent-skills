#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
registry_path = repo_root / "scripts" / "skill-registry.json"
data = json.loads(registry_path.read_text(encoding="utf-8"))
config = data["codex_local_only_skill_sets"]["blender_skills"]
checkout = Path(config["checkout"])
source_root = checkout / Path(config["source_subdir"])

skill_names = sorted(
    path.name
    for path in source_root.iterdir()
    if path.is_dir() and (path / "SKILL.md").is_file()
)
commit = subprocess.check_output(
    ["git", "-C", str(checkout), "rev-parse", "HEAD"],
    text=True,
).strip()

extra_names = sorted(set(config.get("extra_protected_skill_names", [])))
protected_names = sorted(set(skill_names) | set(extra_names))
data["codex_local_only_skill_names"] = protected_names
data["source_commits"]["blender_skills"] = {
    "repo": "https://github.com/arjun988/blender-skills",
    "commit": commit,
}
registry_path.write_text(
    json.dumps(data, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)
print(json.dumps({"commit": commit, "skill_count": len(skill_names)}))
