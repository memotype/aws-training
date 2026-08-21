<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Maintainer Commit Instructions

Create a checkpoint commit of the currently reviewed Maintainer work.

Before staging:

- Confirm the current branch and applicable Git authority. Material Maintainer
  work is normally committed on the dedicated work branch established under
  section 6.1 of `MAINTAINER.md`. If work that requires the normal pull-request
  workflow is on the canonical branch, stop unless the operator has explicitly
  authorized another workflow permitted by governance.
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

Do not amend, push, tag, create a GitHub Release, mutate GitHub Issues, access
AWS, or perform other external mutations.

After committing, report:

- commit hash and subject
- files included
- any `SCRATCH.md` or `CHANGELOG.md` changes
- validation performed and results
- resulting working-tree and index status

Stop after the local commit.
