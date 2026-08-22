<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Maintainer Commit Instructions

Create a checkpoint commit for Maintainer Issue `#<issue-number>`.

Replace the placeholder with the exact existing Issue number before using this
prompt. This prompt authorizes the local checkpoint commit and the read-only
repository and Issue discovery needed to invoke section 6.2 of `MAINTAINER.md`.
It does not authorize creating, selecting, or switching a branch or mutating an
Issue.

Before staging or committing:

- Invoke the governed checkpoint procedure in section 6.2 of `MAINTAINER.md`.
  Verify the expected repository and current canonical default branch, the open
  `maintainer` Issue, and the exact dedicated Issue branch derived under section
  6.1. Read the Issue's relevant durable handoff context.
- Inspect `HEAD`, the current branch, index, working tree, and complete
  cumulative diff, including untracked in-scope files. If `HEAD` is detached,
  the checkout is on the canonical default branch, or the current branch is not
  the specified Issue's dedicated branch, stop and report the invariant failure
  without creating or switching a branch.
- Review `docs/agents/maintainer/SCRATCH.md` and update it only as needed so it
  reflects the current evergreen handoff state. Remove stale state; do not turn
  it into a task diary or duplicate governance, Issues, or changelog history.
- Review the root `CHANGELOG.md` and tend `Unreleased` so it accurately
  summarizes the material project state after this work. Consolidate related
  changes, remove stale wording, and omit implementation trivia. Do not prepare
  a numbered release unless explicitly requested.
- Review the complete working tree and cumulative diff, preserving unrelated
  operator changes.
- Run all validation required by the currently authoritative governance.
- Re-review the final diff after any handoff or validation edits.

Then stage only the reviewed in-scope files/hunks and create one concise commit
whose subject describes the resulting repository state.

Do not amend, create or switch a branch, push, tag, create a pull request,
create a GitHub Release, mutate GitHub Issues, access AWS, or perform other
external mutations.

After committing, report:

- commit hash and subject
- Issue and dedicated branch verified
- files included
- any `SCRATCH.md` or `CHANGELOG.md` changes
- validation performed and results
- resulting working-tree and index status

Stop after the local commit.
