#!/usr/bin/env python3
"""
WCAG Color Contrast Ratio Checker

Check color contrast ratios between two hex colors and report AA/AAA
compliance for normal text, large text, and UI components.

Usage:
    python contrast-checker.py #1a1a2e #e0e0e0
    python contrast-checker.py "#333" "#fff" --verbose
    python contrast-checker.py --batch palette.css
    python contrast-checker.py --batch tailwind.config.js

Stdlib only (uses colorsys from stdlib).
"""

import argparse
import json
import os
import re
import sys
from typing import Optional


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert a hex color string to an (R, G, B) tuple (0–255 each)."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = h[0] * 2 + h[1] * 2 + h[2] * 2
    if len(h) != 6:
        raise ValueError(f"Invalid hex color: '{hex_color}'")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def relative_luminance(r: int, g: int, b: int) -> float:
    """
    Calculate relative luminance per WCAG 2.x specification.
    https://www.w3.org/TR/WCAG21/#dfn-relative-luminance
    """
    def linearize(channel: int) -> float:
        s = channel / 255.0
        return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4

    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(color1: str, color2: str) -> float:
    """
    Calculate the WCAG contrast ratio between two hex colors.
    Returns a value between 1.0 and 21.0.
    """
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)
    l1 = relative_luminance(r1, g1, b1)
    l2 = relative_luminance(r2, g2, b2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def check_wcag(ratio: float) -> dict:
    """Evaluate a contrast ratio against WCAG 2.x thresholds."""
    return {
        "ratio": round(ratio, 2),
        "normal_text_aa": ratio >= 4.5,       # Level AA, normal text
        "normal_text_aaa": ratio >= 7.0,      # Level AAA, normal text
        "large_text_aa": ratio >= 3.0,        # Level AA, large text (>=18pt or >=14pt bold)
        "large_text_aaa": ratio >= 4.5,       # Level AAA, large text
        "ui_components_aa": ratio >= 3.0,     # Level AA, UI components and graphical objects
    }


def format_result(fg: str, bg: str, result: dict, verbose: bool = False) -> str:
    """Format a single contrast check result as human-readable text."""
    lines = []

    def status(passed: bool) -> str:
        return "PASS" if passed else "FAIL"

    lines.append(f"  Foreground: {fg}  |  Background: {bg}")
    lines.append(f"  Contrast Ratio: {result['ratio']}:1")
    lines.append("")
    lines.append(f"  {'Check':<28} {'Result':<6} {'Required'}")
    lines.append(f"  {'─' * 28} {'─' * 6} {'─' * 10}")
    lines.append(f"  {'Normal Text (AA)':<28} {status(result['normal_text_aa']):<6} >= 4.5:1")
    lines.append(f"  {'Normal Text (AAA)':<28} {status(result['normal_text_aaa']):<6} >= 7.0:1")
    lines.append(f"  {'Large Text (AA)':<28} {status(result['large_text_aa']):<6} >= 3.0:1")
    lines.append(f"  {'Large Text (AAA)':<28} {status(result['large_text_aaa']):<6} >= 4.5:1")
    lines.append(f"  {'UI Components (AA)':<28} {status(result['ui_components_aa']):<6} >= 3.0:1")

    if verbose:
        r1, g1, b1 = hex_to_rgb(fg)
        r2, g2, b2 = hex_to_rgb(bg)
        l1 = relative_luminance(r1, g1, b1)
        l2 = relative_luminance(r2, g2, b2)
        lines.append("")
        lines.append(f"  Foreground RGB: ({r1}, {g1}, {b1})  Luminance: {l1:.4f}")
        lines.append(f"  Background RGB: ({r2}, {g2}, {b2})  Luminance: {l2:.4f}")

    return "\n".join(lines)


HEX_COLOR_PATTERN = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b")


def extract_colors_from_file(file_path: str) -> list[str]:
    """Extract all hex color values from a CSS, JS, or JSON file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        with open(file_path, "r", encoding="latin-1") as f:
            content = f.read()

    return list(set(HEX_COLOR_PATTERN.findall(content)))


def normalize_hex(color: str) -> str:
    """Normalize a hex color to 6-digit lowercase."""
    h = color.lstrip("#")
    if len(h) == 3:
        h = h[0] * 2 + h[1] * 2 + h[2] * 2
    return f"#{h.lower()}"


def batch_check(file_path: str, verbose: bool = False) -> list[dict]:
    """
    Extract colors from a file and check all pair combinations.
    Returns a list of result dicts sorted by contrast ratio (ascending).
    """
    colors = extract_colors_from_file(file_path)
    if len(colors) < 2:
        print(f"  Found {len(colors)} color(s) in '{file_path}'. Need at least 2 for comparison.",
              file=sys.stderr)
        return []

    colors = sorted(set(normalize_hex(c) for c in colors))
    print(f"  Found {len(colors)} unique colors in '{file_path}'.")
    print(f"  Checking {len(colors) * (len(colors) - 1) // 2} color pairs...\n")

    results = []
    for i, c1 in enumerate(colors):
        for c2 in colors[i + 1:]:
            ratio = contrast_ratio(c1, c2)
            wcag = check_wcag(ratio)
            results.append({
                "fg": c1,
                "bg": c2,
                "ratio": wcag["ratio"],
                "normal_aa": wcag["normal_text_aa"],
                "normal_aaa": wcag["normal_text_aaa"],
                "large_aa": wcag["large_text_aa"],
                "ui_aa": wcag["ui_components_aa"],
            })

    results.sort(key=lambda r: r["ratio"])
    return results


def format_batch_results(results: list[dict]) -> str:
    """Format batch results as a table."""
    lines = []

    lines.append(f"  {'Foreground':<12} {'Background':<12} {'Ratio':<8} "
                 f"{'Norm AA':<9} {'Norm AAA':<10} {'Large AA':<10} {'UI AA'}")
    lines.append(f"  {'─' * 12} {'─' * 12} {'─' * 8} {'─' * 9} {'─' * 10} {'─' * 10} {'─' * 6}")

    for r in results:
        def s(v: bool) -> str:
            return "PASS" if v else "FAIL"

        lines.append(
            f"  {r['fg']:<12} {r['bg']:<12} {r['ratio']:<8} "
            f"{s(r['normal_aa']):<9} {s(r['normal_aaa']):<10} "
            f"{s(r['large_aa']):<10} {s(r['ui_aa'])}"
        )

    failing = [r for r in results if not r["normal_aa"]]
    passing = [r for r in results if r["normal_aa"]]
    lines.append("")
    lines.append(f"  Summary: {len(passing)} pairs pass Normal AA, "
                 f"{len(failing)} pairs fail Normal AA.")

    if failing:
        lines.append("")
        lines.append("  Failing pairs (Normal Text AA):")
        for r in failing:
            lines.append(f"    {r['fg']} / {r['bg']} — {r['ratio']}:1 (need 4.5:1)")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="WCAG color contrast ratio checker.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "#1a1a2e" "#e0e0e0"
  %(prog)s "#333" "#fff" --verbose
  %(prog)s --batch styles.css
  %(prog)s --batch tailwind.config.js --json
        """,
    )
    parser.add_argument("colors", nargs="*",
                        help="Two hex colors to compare (e.g., '#333' '#fff').")
    parser.add_argument("--batch", metavar="FILE",
                        help="Extract colors from a file and check all pairs.")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show additional details (RGB values, luminance).")
    parser.add_argument("--json", action="store_true",
                        help="Output results as JSON.")
    args = parser.parse_args()

    if args.batch:
        if not os.path.isfile(args.batch):
            print(f"Error: File not found: '{args.batch}'", file=sys.stderr)
            sys.exit(1)

        results = batch_check(args.batch, args.verbose)

        if args.json:
            print(json.dumps(results, indent=2))
        elif results:
            print(format_batch_results(results))
        sys.exit(0)

    if len(args.colors) != 2:
        parser.error("Provide exactly two hex colors (e.g., '#333' '#fff'), or use --batch.")

    fg, bg = args.colors
    try:
        ratio = contrast_ratio(fg, bg)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    result = check_wcag(ratio)

    if args.json:
        output = {
            "foreground": normalize_hex(fg),
            "background": normalize_hex(bg),
            **result,
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n{'=' * 50}")
        print(f"  WCAG Contrast Check")
        print(f"{'=' * 50}\n")
        print(format_result(fg, bg, result, args.verbose))
        print(f"\n{'=' * 50}\n")

    if not result["normal_text_aa"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
