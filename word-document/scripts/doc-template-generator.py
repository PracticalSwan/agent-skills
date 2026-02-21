"""
Word Document Template Generator

This script generates Microsoft Word document templates
for common business documents like reports, letters, and memos.

Usage: python scripts/doc-template-generator.py
"""

from typing import Dict, List, Any, Optional
import json


class DocumentTemplate:
    """Base class for document templates."""

    def __init__(self, filename: str):
        self.filename = filename
        self.content = []

    def add_paragraph(self, text: str, style: str = "Normal") -> Dict:
        """Add a paragraph to the document."""
        return {
            "type": "paragraph",
            "text": text,
            "style": style
        }

    def add_heading(self, text: str, level: int = 1) -> Dict:
        """Add a heading to the document."""
        return {
            "type": "heading",
            "text": text,
            "level": level
        }

    def add_table(self, headers: List[str], rows: List[List[str]]) -> Dict:
        """Add a table to the document."""
        return {
            "type": "table",
            "headers": headers,
            "rows": rows
        }

    def add_list(self, items: List[str], ordered: bool = False) -> Dict:
        """Add a list to the document."""
        return {
            "type": "list",
            "items": items,
            "ordered": ordered
        }


class ReportTemplate(DocumentTemplate):
    """Template for formal business reports."""

    def create_cover_page(self, title: str, subtitle: str, author: str, date: str) -> List[Dict]:
        """Create a cover page for the report."""
        return [
            self.add_heading(title, level=1),
            self.add_paragraph(subtitle, "Subtitle"),
            self.add_paragraph(f"Prepared by: {author}", "Author"),
            self.add_paragraph(f"Date: {date}", "Date"),
            self.add_paragraph("", "Normal")  # Empty paragraph for spacing
        ]

    def create_executive_summary(self, summary: str) -> List[Dict]:
        """Create an executive summary section."""
        return [
            self.add_heading("Executive Summary", level=2),
            self.add_paragraph(summary)
        ]

    def create_table_of_contents(self) -> Dict:
        """Create a table of contents placeholder."""
        return {
            "type": "table_of_contents"
        }

    def create_section(self, title: str, content: List[str]) -> List[Dict]:
        """Create a report section."""
        section = [self.add_heading(title, level=2)]
        for paragraph in content:
            section.append(self.add_paragraph(paragraph))
        return section

    def create_findings_section(self, findings: List[Dict[str, str]]) -> List[Dict]:
        """Create a findings section with key findings."""
        section = [self.add_heading("Key Findings", level=2)]
        for finding in findings:
            section.append(self.add_heading(finding.get("title", ""), level=3))
            section.append(self.add_paragraph(finding.get("description", "")))
        return section


class MemoTemplate(DocumentTemplate):
    """Template for internal memos."""

    def create_memo_header(self, to: str, from_: str, date: str, subject: str) -> List[Dict]:
        """Create memo header."""
        return [
            self.add_paragraph("MEMORANDUM", "MemoTitle"),
            self.add_paragraph(f"To: {to}", "MemoField"),
            self.add_paragraph(f"From: {from_}", "MemoField"),
            self.add_paragraph(f"Date: {date}", "MemoField"),
            self.add_paragraph(f"Subject: {subject}", "MemoField"),
            self.add_paragraph("", "Normal")
        ]

    def create_memo_body(self, paragraphs: List[str]) -> List[Dict]:
        """Create memo body content."""
        return [self.add_paragraph(p) for p in paragraphs]


class LetterTemplate(DocumentTemplate):
    """Template for formal business letters."""

    def create_letter_header(self, sender_name: str, sender_address: List[str],
                            recipient_name: str, recipient_address: List[str],
                            date: str) -> List[Dict]:
        """Create letter header."""
        header = [
            self.add_paragraph(sender_name, "SenderName"),
            self.add_paragraph("\n".join(sender_address), "SenderAddress"),
            self.add_paragraph("", "Normal"),
            self.add_paragraph(date, "Date"),
            self.add_paragraph("", "Normal"),
            self.add_paragraph(recipient_name, "RecipientName"),
            self.add_paragraph("\n".join(recipient_address), "RecipientAddress"),
            self.add_paragraph("", "Normal")
        ]
        return header

    def create_salutation(self, recipient_name: str) -> Dict:
        """Create letter salutation."""
        return self.add_paragraph(f"Dear {recipient_name},")

    def create_letter_body(self, paragraphs: List[str]) -> List[Dict]:
        """Create letter body content."""
        return [self.add_paragraph(p) for p in paragraphs]

    def create_closing(self, sender_name: str, sender_title: str) -> List[Dict]:
        """Create letter closing."""
        return [
            self.add_paragraph("Sincerely,"),
            self.add_paragraph(sender_name),
            self.add_paragraph(sender_title, "Title")
        ]


def export_mcp_commands(content: List[Dict], filename: str) -> str:
    """Export document content as MCP commands."""
    commands = []
    commands.append("// Activate Word document tools")
    commands.append("activate_document_content_and_styling();")
    commands.append("")
    commands.append(f"// Create document: {filename}")
    commands.append(f'mcp_word_create_document({{ filename: "{filename}" }});')
    commands.append("")

    for item in content:
        if item["type"] == "heading":
            level = item.get("level", 1)
            commands.append(f'mcp_word_add_heading({{ text: "{item["text"]}", level: {level} }});')
        elif item["type"] == "paragraph":
            commands.append(f'mcp_word_add_paragraph({{ text: "{item["text"]}" }});')
        elif item["type"] == "table":
            headers = json.dumps(item["headers"])
            rows = json.dumps(item["rows"])
            commands.append(f'mcp_word_add_table({{ headers: {headers}, rows: {rows} }});')
        elif item["type"] == "list":
            items = json.dumps(item["items"])
            ordered = "true" if item.get("ordered") else "false"
            commands.append(f'mcp_word_add_list({{ items: {items}, ordered: {ordered} }});')
        elif item["type"] == "table_of_contents":
            commands.append('// Table of contents - add via Word UI or reference styles')

    commands.append("")
    commands.append(f"// Save document")
    commands.append(f'mcp_word_save_document({{ filename: "{filename}" }});')

    return "\n".join(commands)


# Example usage
def create_quarterly_report() -> str:
    """Example: Create a quarterly business report."""
    report = ReportTemplate("q3_business_report.docx")

    content = []
    content.extend(report.create_cover_page(
        title="Q3 2025 Business Report",
        subtitle="Finance Division",
        author="Finance Team",
        date="October 2025"
    ))

    content.append(report.create_table_of_contents())
    content.append(report.add_paragraph("", "Normal"))  # Page break

    content.extend(report.create_executive_summary(
        "Q3 showed strong performance with 20% revenue growth year-over-year, "
        "driven primarily by expansion in the APAC region. Operating margins improved "
        "to 33% through cost optimization initiatives."
    ))

    content.extend(report.create_section("Financial Highlights", [
        "Revenue reached $1.8M, representing a 20% increase compared to Q3 2024.",
        "Gross margin expanded to 45%, a 3 percentage point improvement.",
        "Operating income grew to $540K, up 25% year-over-year."
    ]))

    content.extend(report.create_section("Regional Performance", [
        "APAC region led growth with a 35% increase, driven by new market entries.",
        "Americas showed steady growth of 15% with strong performance in key accounts.",
        "EMEA exceeded targets with 12% growth despite challenging market conditions."
    ]))

    content.extend(report.create_findings_section([
        {
            "title": "Strong Revenue Growth",
            "description": "Revenue growth of 20% YoY exceeded expectations, driven by "
                         "successful product launches and market expansion."
        },
        {
            "title": "Margin Expansion",
            "description": "Gross margin improved by 3 percentage points through "
                         "strategic sourcing and operational efficiencies."
        },
        {
            "title": "Market Share Gains",
            "description": "Gained market share in key segments, particularly in "
                         "APAC where new product offerings resonated with customers."
        }
    ]))

    return export_mcp_commands(content, report.filename)


def create_internal_memo() -> str:
    """Example: Create an internal memo."""
    memo = MemoTemplate("all_hands_meeting.docx")

    content = []
    content.extend(memo.create_memo_header(
        to="All Staff",
        from_="Executive Team",
        date="October 15, 2025",
        subject="Q3 All-Hands Meeting"
    ))

    content.extend(memo.create_memo_body([
        "Please join us for our quarterly all-hands meeting on Friday, October 20th "
        "at 2:00 PM in the main conference room.",

        "Agenda items include:",
        "Q3 business review and financial results",
        "Product roadmap updates",
        "Employee recognition and awards",
        "Q&A session with leadership",

        "Light refreshments will be served. Please RSVP by Wednesday, October 18th.",

        "We look forward to seeing you there!"
    ]))

    return export_mcp_commands(content, memo.filename)


if __name__ == "__main__":
    print("=" * 80)
    print("Word Document Template Generator")
    print("=" * 80)
    print()

    print("Example 1: Quarterly Business Report")
    print("-" * 80)
    print(create_quarterly_report())
    print()

    print("=" * 80)
    print("Example 2: Internal Memo")
    print("-" * 80)
    print(create_internal_memo())
