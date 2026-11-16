#!/usr/bin/env python3
"""Regression tests for preserving licensing notices during skill refreshes."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


PROMOTER_PATH = Path(__file__).with_name("promote-child-skills.py")
SPEC = importlib.util.spec_from_file_location("promote_child_skills", PROMOTER_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load promotion module at {PROMOTER_PATH}")
PROMOTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROMOTER)


class LicensePreservationTests(unittest.TestCase):
    def test_preserves_existing_license_and_notice_missing_upstream(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            destination = root / "destination"
            source.mkdir()
            destination.mkdir()
            (source / "SKILL.md").write_text("---\nname: example\n---\nCurrent skill.\n", encoding="utf-8")
            (destination / "SKILL.md").write_text("Old skill.\n", encoding="utf-8")
            (destination / "CHANGELOG.md").write_text("## Existing\n", encoding="utf-8")
            (destination / "LICENSE-APACHE-2.0.txt").write_text("Third-party license.\n", encoding="utf-8")
            (destination / "NOTICE.txt").write_text("Third-party notice.\n", encoding="utf-8")

            self.assertEqual(PROMOTER.replace_skill(source, destination, preserve_skill=False), "refreshed")

            self.assertEqual((destination / "LICENSE-APACHE-2.0.txt").read_text(encoding="utf-8"), "Third-party license.\n")
            self.assertEqual((destination / "NOTICE.txt").read_text(encoding="utf-8"), "Third-party notice.\n")
            self.assertEqual((destination / "CHANGELOG.md").read_text(encoding="utf-8"), "## Existing\n")
            self.assertIn("Current skill.", (destination / "SKILL.md").read_text(encoding="utf-8"))

    def test_prefers_current_upstream_license_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source"
            destination = root / "destination"
            source.mkdir()
            destination.mkdir()
            (source / "SKILL.md").write_text("---\nname: example\n---\nCurrent skill.\n", encoding="utf-8")
            (source / "LICENSE.txt").write_text("Current upstream license.\n", encoding="utf-8")
            (destination / "SKILL.md").write_text("Old skill.\n", encoding="utf-8")
            (destination / "LICENSE-APACHE-2.0.txt").write_text("Stale license.\n", encoding="utf-8")

            PROMOTER.replace_skill(source, destination, preserve_skill=False)

            self.assertEqual((destination / "LICENSE.txt").read_text(encoding="utf-8"), "Current upstream license.\n")
            self.assertFalse((destination / "LICENSE-APACHE-2.0.txt").exists())


if __name__ == "__main__":
    unittest.main()
