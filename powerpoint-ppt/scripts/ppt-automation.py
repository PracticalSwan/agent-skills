"""
PowerPoint Presentation Automation Script

This script automates common PowerPoint presentation tasks:
- Creating presentations from templates
- Populating slide content from data
- Generating slides from structured data
- Exporting presentation metadata

Usage: python scripts/ppt-automation.py
"""

from typing import Dict, List, Any, Optional
import json


class PresentationBuilder:
    """Builder for creating PowerPoint presentations programmatically."""

    def __init__(self, filename: str):
        self.filename = filename
        self.slides = []

    def add_title_slide(self, title: str, subtitle: str = "") -> Dict:
        """Add a title slide."""
        return {
            "type": "title",
            "title": title,
            "subtitle": subtitle
        }

    def add_content_slide(self, title: str, bullets: List[str]) -> Dict:
        """Add a content slide with bullet points."""
        return {
            "type": "content",
            "title": title,
            "bullets": bullets
        }

    def add_chart_slide(self, title: str, chart_path: str, bullets: List[str] = None) -> Dict:
        """Add a slide with a chart image."""
        return {
            "type": "chart",
            "title": title,
            "chart_path": chart_path,
            "bullets": bullets or []
        }

    def add_two_column_slide(self, title: str, left_bullets: List[str], right_bullets: List[str]) -> Dict:
        """Add a two-column content slide."""
        return {
            "type": "two_column",
            "title": title,
            "left": left_bullets,
            "right": right_bullets
        }

    def build_slides(self, data: List[Dict]) -> None:
        """Build slides from structured data."""
        for item in data:
            if item["type"] == "title":
                self.slides.append(self.add_title_slide(item["title"], item.get("subtitle", "")))
            elif item["type"] == "content":
                self.slides.append(self.add_content_slide(item["title"], item["bullets"]))
            elif item["type"] == "chart":
                self.slides.append(self.add_chart_slide(item["title"], item["chart_path"], item.get("bullets")))
            elif item["type"] == "two_column":
                self.slides.append(self.add_two_column_slide(item["title"], item["left"], item["right"]))

    def export_mcp_commands(self) -> str:
        """Export slides as MCP commands."""
        commands = []
        commands.append("// Activate required tools")
        commands.append("activate_presentation_creation_and_management();")
        commands.append("activate_text_placeholder_management();")
        commands.append("activate_content_management_tools();")
        commands.append("")
        commands.append(f'// Create presentation: {self.filename}')
        commands.append(f'mcp_ppt_create_presentation({{ filename: "{self.filename}", title: "Presentation" }});')
        commands.append("")

        slide_index = 0
        for slide in self.slides:
            if slide["type"] == "title":
                commands.append(f"// Slide {slide_index}: Title slide")
                commands.append(f'mcp_ppt_populate_placeholder({{ slide_index: {slide_index}, placeholder_index: 0, text: "{slide["title"]}" }});')
                if slide.get("subtitle"):
                    commands.append(f'mcp_ppt_populate_placeholder({{ slide_index: {slide_index}, placeholder_index: 1, text: "{slide["subtitle"]}" }});')
                commands.append("")

            elif slide["type"] == "content":
                commands.append(f"// Slide {slide_index}: {slide['title']}")
                commands.append(f'mcp_ppt_add_slide({{ filename: "{self.filename}", layout_index: 2 }});')
                commands.append(f'mcp_ppt_populate_placeholder({{ slide_index: {slide_index}, placeholder_index: 0, text: "{slide["title"]}" }});')
                if slide["bullets"]:
                    bullets_json = json.dumps(slide["bullets"])
                    commands.append(f'mcp_ppt_add_bullet_points_to_placeholder({{ slide_index: {slide_index}, placeholder_index: 1, bullet_points: {bullets_json} }});')
                commands.append("")

            elif slide["type"] == "chart":
                commands.append(f"// Slide {slide_index}: {slide['title']}")
                commands.append(f'mcp_ppt_add_slide({{ filename: "{self.filename}", layout_index: 2 }});')
                commands.append(f'mcp_ppt_populate_placeholder({{ slide_index: {slide_index}, placeholder_index: 0, text: "{slide["title"]}" }});')
                commands.append(f'mcp_ppt_manage_image({{ slide_index: {slide_index}, operation: "add", image_path: "{slide["chart_path"]}", left: 1.0, top: 1.5, width: 8.0, height: 4.5 }});')
                if slide.get("bullets"):
                    bullets_json = json.dumps(slide["bullets"])
                    commands.append(f'mcp_ppt_add_bullet_points_to_placeholder({{ slide_index: {slide_index}, placeholder_index: 1, bullet_points: {bullets_json} }});')
                commands.append("")

            slide_index += 1

        commands.append(f"// Save presentation")
        commands.append(f'mcp_ppt_save_presentation({{ filename: "{self.filename}" }});')

        return "\n".join(commands)


def create_business_review_presentation() -> str:
    """Example: Create a quarterly business review presentation."""
    builder = PresentationBuilder("q3_business_review.pptx")

    data = [
        {
            "type": "title",
            "title": "Q3 2025 Business Review",
            "subtitle": "Finance Division · October 2025"
        },
        {
            "type": "content",
            "title": "Agenda",
            "bullets": [
                "Financial Performance Overview",
                "Key Metrics and KPIs",
                "Regional Analysis",
                "Strategic Initiatives",
                "Q4 Outlook"
            ]
        },
        {
            "type": "chart",
            "title": "Revenue by Region",
            "chart_path": "./charts/revenue_by_region.png",
            "bullets": [
                "APAC led growth at +35%",
                "Americas +15%",
                "EMEA +12%"
            ]
        },
        {
            "type": "two_column",
            "title": "Operational Highlights",
            "left": [
                "Launched new product line",
                "Expanded to 3 new markets",
                "Hired 50 new employees"
            ],
            "right": [
                "Improved customer satisfaction",
                "Reduced operational costs",
                "Increased profit margins"
            ]
        },
        {
            "type": "content",
            "title": "Q4 Outlook",
            "bullets": [
                "Continue growth momentum",
                "Focus on customer retention",
                "Invest in product innovation",
                "Expand market presence"
            ]
        }
    ]

    builder.build_slides(data)
    return builder.export_mcp_commands()


def create_metrics_dashboard_presentation() -> str:
    """Example: Create a metrics dashboard presentation."""
    builder = PresentationBuilder("kpi_dashboard.pptx")

    data = [
        {
            "type": "title",
            "title": "Monthly KPI Dashboard",
            "subtitle": "Performance Overview"
        },
        {
            "type": "chart",
            "title": "Revenue Trend",
            "chart_path": "./charts/revenue_trend.png"
        },
        {
            "type": "chart",
            "title": "Customer Acquisition",
            "chart_path": "./charts/customer_acquisition.png"
        },
        {
            "type": "content",
            "title": "Key Metrics Summary",
            "bullets": [
                "Revenue: $1.8M (+20% YoY)",
                "Gross Margin: 45% (+3pp)",
                "Customer Count: 12,500 (+15%)",
                "NPS Score: 72 (+5 points)"
            ]
        }
    ]

    builder.build_slides(data)
    return builder.export_mcp_commands()


if __name__ == "__main__":
    print("=" * 80)
    print("PowerPoint Presentation Automation")
    print("=" * 80)
    print()

    print("Example 1: Business Review Presentation")
    print("-" * 80)
    print(create_business_review_presentation())
    print()

    print("=" * 80)
    print("Example 2: KPI Dashboard Presentation")
    print("-" * 80)
    print(create_metrics_dashboard_presentation())
