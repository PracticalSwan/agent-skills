# Changelog

## [2026-04-04] - Initial Import and Catalog Upgrade

### Added

- Imported `agentic-eval` from the `awesome-copilot` reference catalog into the canonical maintained workspace
- Reframed the skill around repeatable rubric design, evidence-based evaluation, and stop conditions
- Added `references/rubric-template.json`, `references/example-scores.json`, and `scripts/rubric-scorecard.py` so the workflow can be exercised locally across clients

### Tested

- Ran `python agentic-eval/scripts/rubric-scorecard.py --rubric agentic-eval/references/rubric-template.json --scores agentic-eval/references/example-scores.json --threshold 0.8`
- Planned validation through `python scripts/validate-skills.py`
