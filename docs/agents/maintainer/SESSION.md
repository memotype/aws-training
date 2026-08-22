<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Maintainer Session Initialization

Operate in **Maintainer** mode for this session.

Read each required governance file completely, one at a time, in the specified
order. If a read is truncated, continue that file to EOF before proceeding.

Before performing non-trivial work, read and follow these governance documents
in order:

1. `CODEX.md`
2. `docs/agents/SHARED.md`
3. `docs/agents/maintainer/MAINTAINER.md`

This prompt selects the mode but does not add to or override the permissions in
those documents.

After reading them, perform the governed read-only Maintainer orientation in
section 4 of `MAINTAINER.md`. Report the active mode, expected repository and
canonical default branch, current branch and checkout state, and current
Maintainer Issue queue summary or degraded-discovery status.

Then stop and ask whether the operator wants to continue a specific existing
Maintainer Issue or start a new unit of work. Do not select or mutate an Issue,
create or switch a branch, or edit repository content during initialization.
