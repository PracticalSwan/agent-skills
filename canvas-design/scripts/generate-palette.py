"""
Color Palette Generator

Generates color palettes (complementary, analogous, triadic, split-complementary)
from a base hex color. Includes WCAG contrast ratio calculations for accessibility.

Usage:
    python generate-palette.py "#E53E3E"
    python generate-palette.py "#4299E1" --harmony all
    python generate-palette.py "#48BB78" --harmony triadic --format css
"""

import colorsys
import sys
import math
from typing import NamedTuple


class Color(NamedTuple):
    r: int
    g: int
    b: int

    @property
    def hex(self) -> str:
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

    @property
    def rgb_str(self) -> str:
        return f"rgb({self.r}, {self.g}, {self.b})"

    @property
    def hsl(self) -> tuple[float, float, float]:
        h, l, s = colorsys.rgb_to_hls(self.r / 255, self.g / 255, self.b / 255)
        return h * 360, s * 100, l * 100


WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)


def hex_to_color(hex_str: str) -> Color:
    hex_str = hex_str.lstrip("#")
    if len(hex_str) == 3:
        hex_str = "".join(c * 2 for c in hex_str)
    if len(hex_str) != 6:
        raise ValueError(f"Invalid hex color: #{hex_str}")
    return Color(
        int(hex_str[0:2], 16),
        int(hex_str[2:4], 16),
        int(hex_str[4:6], 16),
    )


def hsl_to_color(h: float, s: float, l: float) -> Color:
    h_norm = (h % 360) / 360
    s_norm = max(0, min(100, s)) / 100
    l_norm = max(0, min(100, l)) / 100
    r, g, b = colorsys.hls_to_rgb(h_norm, l_norm, s_norm)
    return Color(round(r * 255), round(g * 255), round(b * 255))


def relative_luminance(color: Color) -> float:
    """Calculate relative luminance per WCAG 2.1 definition."""
    def linearize(channel: int) -> float:
        c = channel / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r_lin = linearize(color.r)
    g_lin = linearize(color.g)
    b_lin = linearize(color.b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def contrast_ratio(color1: Color, color2: Color) -> float:
    """Calculate WCAG contrast ratio between two colors."""
    l1 = relative_luminance(color1)
    l2 = relative_luminance(color2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def wcag_grade(ratio: float) -> str:
    if ratio >= 7.0:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3.0:
        return "AA-large"
    return "FAIL"


def shift_hue(h: float, s: float, l: float, degrees: float) -> Color:
    return hsl_to_color(h + degrees, s, l)


def generate_lightness_variants(h: float, s: float) -> list[Color]:
    return [hsl_to_color(h, s, l) for l in [20, 35, 50, 65, 80, 92]]


def complementary(h: float, s: float, l: float) -> dict[str, list[Color]]:
    base = hsl_to_color(h, s, l)
    comp = shift_hue(h, s, l, 180)
    return {
        "name": "Complementary",
        "colors": [base, comp],
        "variants": generate_lightness_variants(h, s)
            + generate_lightness_variants((h + 180) % 360, s),
    }


def analogous(h: float, s: float, l: float) -> dict[str, list[Color]]:
    return {
        "name": "Analogous",
        "colors": [
            shift_hue(h, s, l, -30),
            hsl_to_color(h, s, l),
            shift_hue(h, s, l, 30),
        ],
        "variants": [],
    }


def triadic(h: float, s: float, l: float) -> dict[str, list[Color]]:
    return {
        "name": "Triadic",
        "colors": [
            hsl_to_color(h, s, l),
            shift_hue(h, s, l, 120),
            shift_hue(h, s, l, 240),
        ],
        "variants": [],
    }


def split_complementary(h: float, s: float, l: float) -> dict[str, list[Color]]:
    return {
        "name": "Split-Complementary",
        "colors": [
            hsl_to_color(h, s, l),
            shift_hue(h, s, l, 150),
            shift_hue(h, s, l, 210),
        ],
        "variants": [],
    }


HARMONY_MAP = {
    "complementary": complementary,
    "analogous": analogous,
    "triadic": triadic,
    "split-complementary": split_complementary,
}


def format_color_line(color: Color, label: str = "") -> str:
    ratio_w = contrast_ratio(color, WHITE)
    ratio_b = contrast_ratio(color, BLACK)
    grade_w = wcag_grade(ratio_w)
    grade_b = wcag_grade(ratio_b)
    prefix = f"  {label:<22}" if label else "  "
    return (
        f"{prefix}{color.hex}  "
        f"RGB({color.r:>3}, {color.g:>3}, {color.b:>3})  "
        f"vs white: {ratio_w:5.2f}:1 [{grade_w:<8}]  "
        f"vs black: {ratio_b:5.2f}:1 [{grade_b:<8}]"
    )


def format_css_variables(palette: dict, prefix: str = "color") -> str:
    lines = [f"/* {palette['name']} palette */"]
    for i, color in enumerate(palette["colors"]):
        lines.append(f"--{prefix}-{i + 1}: {color.hex};")
    if palette["variants"]:
        lines.append(f"\n/* Lightness variants */")
        for i, color in enumerate(palette["variants"]):
            lines.append(f"--{prefix}-variant-{i + 1}: {color.hex};")
    return "\n".join(lines)


def print_palette(palette: dict) -> None:
    labels = ["Base", "Second", "Third", "Fourth"]
    print(f"\n{'=' * 90}")
    print(f"  {palette['name']} Palette")
    print(f"{'=' * 90}")

    for i, color in enumerate(palette["colors"]):
        label = labels[i] if i < len(labels) else f"Color {i + 1}"
        print(format_color_line(color, label))

    if palette["variants"]:
        print(f"\n  Lightness Variants:")
        shade_labels = ["900 (darkest)", "700", "500 (base)", "300", "100", "50 (lightest)"]
        for i, color in enumerate(palette["variants"]):
            idx = i % 6
            hue_group = "Primary" if i < 6 else "Complement"
            label = f"{hue_group} {shade_labels[idx]}"
            print(format_color_line(color, label))


def print_accessibility_summary(base: Color) -> None:
    ratio_w = contrast_ratio(base, WHITE)
    ratio_b = contrast_ratio(base, BLACK)

    print(f"\n{'=' * 90}")
    print("  Accessibility Summary")
    print(f"{'=' * 90}")
    print(f"  Base color: {base.hex}  RGB({base.r}, {base.g}, {base.b})")
    print(f"  Relative luminance: {relative_luminance(base):.4f}")
    print()
    print(f"  Against white (#FFFFFF):")
    print(f"    Contrast ratio:    {ratio_w:.2f}:1")
    print(f"    Normal text:       {wcag_grade(ratio_w)}")
    print(f"    Large text:        {'PASS' if ratio_w >= 3.0 else 'FAIL'}")
    print(f"    UI components:     {'PASS' if ratio_w >= 3.0 else 'FAIL'}")
    print()
    print(f"  Against black (#000000):")
    print(f"    Contrast ratio:    {ratio_b:.2f}:1")
    print(f"    Normal text:       {wcag_grade(ratio_b)}")
    print(f"    Large text:        {'PASS' if ratio_b >= 3.0 else 'FAIL'}")
    print(f"    UI components:     {'PASS' if ratio_b >= 3.0 else 'FAIL'}")
    print()

    best_bg = "black" if ratio_b > ratio_w else "white"
    print(f"  Recommendation: Use on {best_bg} background for best readability.")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python generate-palette.py <hex_color> [--harmony <type|all>] [--format <text|css>]")
        print()
        print("Harmony types: complementary, analogous, triadic, split-complementary, all")
        print("Formats: text (default), css")
        print()
        print("Examples:")
        print('  python generate-palette.py "#E53E3E"')
        print('  python generate-palette.py "#4299E1" --harmony all')
        print('  python generate-palette.py "#48BB78" --harmony triadic --format css')
        sys.exit(1)

    hex_input = sys.argv[1].strip().strip('"').strip("'")
    harmony_type = "all"
    output_format = "text"

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--harmony" and i + 1 < len(sys.argv):
            harmony_type = sys.argv[i + 1].lower()
            i += 2
        elif sys.argv[i] == "--format" and i + 1 < len(sys.argv):
            output_format = sys.argv[i + 1].lower()
            i += 2
        else:
            i += 1

    try:
        base = hex_to_color(hex_input)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    h, s, l = base.hsl

    print(f"\n  Base Color: {base.hex}  RGB({base.r}, {base.g}, {base.b})")
    print(f"  HSL: {h:.1f}°, {s:.1f}%, {l:.1f}%")

    if harmony_type == "all":
        generators = list(HARMONY_MAP.values())
    elif harmony_type in HARMONY_MAP:
        generators = [HARMONY_MAP[harmony_type]]
    else:
        print(f"Error: Unknown harmony type '{harmony_type}'.")
        print(f"Available: {', '.join(HARMONY_MAP.keys())}, all")
        sys.exit(1)

    for gen in generators:
        palette = gen(h, s, l)
        if output_format == "css":
            print(f"\n{format_css_variables(palette)}")
        else:
            print_palette(palette)

    print_accessibility_summary(base)


if __name__ == "__main__":
    main()
