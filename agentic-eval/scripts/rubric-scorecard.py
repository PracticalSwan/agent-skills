#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def compute_score(rubric: dict, scores: dict) -> dict:
    max_score = rubric.get("max_score", 5)
    dimensions = rubric["dimensions"]
    total = 0.0
    missing = []
    per_dimension = {}

    for name, config in dimensions.items():
        weight = float(config["weight"])
        if name not in scores:
            missing.append(name)
            continue
        raw_score = float(scores[name])
        normalized = raw_score / max_score
        weighted = normalized * weight
        total += weighted
        per_dimension[name] = {
            "raw_score": raw_score,
            "max_score": max_score,
            "weight": weight,
            "weighted_score": round(weighted, 4),
        }

    return {
        "overall_score": round(total, 4),
        "missing_dimensions": missing,
        "dimensions": per_dimension,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a candidate artifact against a weighted rubric.")
    parser.add_argument("--rubric", required=True, help="Path to a rubric JSON file.")
    parser.add_argument("--scores", required=True, help="Path to a scores JSON file.")
    parser.add_argument("--threshold", type=float, default=0.8, help="Passing threshold on a 0-1 scale.")
    args = parser.parse_args()

    rubric = load_json(Path(args.rubric))
    scores = load_json(Path(args.scores))
    result = compute_score(rubric, scores)
    result["threshold"] = args.threshold
    result["result"] = "PASS" if result["overall_score"] >= args.threshold and not result["missing_dimensions"] else "FAIL"

    print(json.dumps(result, indent=2))
    return 0 if result["result"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
