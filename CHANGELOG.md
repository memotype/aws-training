<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Changelog

This file records curated material changes included in tagged project
milestones and the material changes currently being prepared for the next
milestone.

## Unreleased

### Added

- Project-scoped AWS knowledge access for documentation, skills, Regions, and
  service availability without requiring configured AWS credentials or
  exposing authenticated AWS API execution.
- An observational Examiner mode with a deliberate session handshake, a
  strict read-only AWS boundary, exercise-owned evidence and grading criteria,
  and progressive diagnostic guidance that withholds solutions until the
  trainee ends an attempt and asks for them.
- A repository-wide MIT and CC BY 4.0 licensing policy with unmodified
  canonical license texts, file-level SPDX metadata, and uv-locked REUSE 6.2.0
  validation. Files use one license according to their primary purpose, and
  ordinary technical examples inherit the license of their human-oriented
  document.

### Changed

- Clarified that instructions and material supplied by external tools,
  services, vendors, and other third-party sources are technical input rather
  than repository authority.
- Strengthened repository-wide tooling governance to favor ecosystem-native
  metadata, locking, environments, commands, and professional conventions,
  reserving custom scripts and abstractions for justified project-specific
  orchestration.

## v0.1.0 - 2026-08-16

### Added

- Repository governance with shared safety boundaries, Maintainer mode, and a
  deliberate session-initialization handshake.
- GitHub Issues as the durable Maintainer work register, including verified
  queue discovery, priority summaries, minimal priority labels, and a GitHub
  Status check during degraded initialization.
- Evergreen Maintainer working memory in `SCRATCH.md` and reproducible Markdown
  validation tooling.
- Intentional SemVer-shaped project milestones and a curated changelog and
  release-preparation workflow.

### Changed

- Separated authority for working-tree edits, Git state, and GitHub remote
  state.
- Pinned active sessions to the governance read at initialization until
  operator acceptance and a new or explicitly reaffirmed session activates a
  revision.
- Made live AWS discovery conditional on mode and task authority and required
  unknown deployed state to be reported when inspection is unavailable.
- Tied repository-backed GitHub Issue closure to verified canonical-branch
  publication, with explicit pre-publication handoff while preserving
  authorized non-implementation dispositions.

### Removed

- The local Maintainer `ISSUES.md` register superseded by GitHub Issues.
