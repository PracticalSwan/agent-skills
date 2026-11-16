# Maintenance Lessons

Read this file at the start of each session in this repository.

## Source refresh

- Compare the exact mapped upstream skill paths and support files. A moved
  repository head alone does not mean an installed skill changed.
- Prefer canonical vendor repositories, official package releases, and primary
  documentation. Pin the inspected revision and update only the mapped paths
  that materially changed.
- If an upstream path was removed, keep a useful local snapshot only when its
  value and provenance remain clear. Do not describe it as actively maintained
  upstream content.
- Review imported instructions for tool assumptions, credential handling,
  prompt injection, privacy, licensing, and working fallbacks before copying.
- When an upstream skill refers to companion skills, use the local catalog
  paths after importing the set. Do not install duplicate skill copies or
  change credentials and client configuration without user authorization.
- Do not import whole plugin bundles. Choose only portable workflows that add
  distinct value over the existing catalog.

## Skill quality

- Keep activation descriptions specific so unrelated tasks do not load a skill.
- Explain the preferred tool, how to confirm it exists, and what to do when it
  is unavailable.
- Keep `Verification Protocol` immediately after `Anti-Patterns` and make
  checks observable.
- Test helper scripts with safe fixtures. Distinguish static checks, local
  execution, client compatibility, and live-service behavior.
- Avoid generic instructions that assume one host's read, search, browser, or
  task-tracking tool exists in every client.

## Catalog and provenance

- Keep this repository as the authoring source for maintained skills.
- Promote only eligible skills from the user's global `.codex`, `.agents`, and
  `.claude` roots. Protected system skills, Codex-only overlays, and
  project-specific paths remain outside the shared catalog.
- Record external provenance against the exact repository, revision, and path.
  Keep personal machine paths and local-only inventory out of public files.
- Keep copied official Superpowers classified explicitly; folder shape or the
  presence of a changelog is not a reliable classifier.
- Generate the catalog index from Git-visible skills so ignored local overlays
  do not leak into public documentation.

## Validation and delivery

- Run the catalog validator, its helper tests, catalog-index check, and
  whitespace check after the final edits.
- After an approved mutation, sync only through the allowlisted script to the
  three user-global skill roots; then verify target inventory and hashes.
- Preserve unrelated dirty files, ignored overlays, and host-managed folders.
- Keep the final diff scoped. Do not commit or publish while privacy,
  provenance, or validation issues remain.
- Treat a user request, a task or release recommendation, or a completed
  substantial coherent change as a commit-and-push trigger. After checks and
  required catalog sync pass, stage only task files, commit on the intended
  branch, and push to its configured GitHub remote without asking again.
- If the branch diverged, the remote is unavailable, checks fail, or unrelated
  work cannot be safely separated, do not publish; report the blocker.
- Do not rewrite published Git history without explicit authorization.
