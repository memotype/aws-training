# Changelog

This file records curated material changes included in tagged project
milestones and the material changes currently being prepared for the next
milestone.

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
