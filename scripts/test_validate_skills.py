#!/usr/bin/env python3
"""Regression tests for retired-client detection in the catalog validator."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


VALIDATOR_PATH = Path(__file__).with_name("validate-skills.py")
SPEC = importlib.util.spec_from_file_location("validate_skills", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load validator module at {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class RemovedClientDetectionTests(unittest.TestCase):
    def test_rejects_retired_client_surfaces(self) -> None:
        for text in (
            "Gemini CLI",
            "gemini cli",
            "Antigravity CLI",
            "Antigravity IDE",
            "Antigravity host integration",
        ):
            with self.subTest(text=text):
                self.assertIsNotNone(VALIDATOR.REMOVED_CLIENT_RE.search(text))

    def test_allows_official_gemini_api_managed_agent(self) -> None:
        for text in (
            "Use the Antigravity Agent through the Gemini API.",
            "antigravity-preview-09-2026",
            'agent_config={"type": "antigravity"}',
        ):
            with self.subTest(text=text):
                self.assertIsNone(VALIDATOR.REMOVED_CLIENT_RE.search(text))


if __name__ == "__main__":
    unittest.main()
