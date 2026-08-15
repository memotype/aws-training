# Changelog

This file records curated material changes included in tagged project
milestones and the material changes currently being prepared for the next
milestone.

## Unreleased

### Added

- Repository governance with shared safety boundaries, Maintainer mode, and a
  deliberate session-initialization handshake.
- GitHub Issues as the durable Maintainer work register, including verified
  queue discovery, minimal priority labels, and degraded initialization when
  GitHub is unavailable.
- Evergreen Maintainer working memory in `SCRATCH.md` and reproducible Markdown
  validation tooling.
- Intentional SemVer-shaped project milestones and a curated changelog and
  release-preparation workflow.

### Changed

- Separated authority for working-tree edits, Git state, and GitHub remote
  state.

### Removed

- The local Maintainer `ISSUES.md` register superseded by GitHub Issues.
