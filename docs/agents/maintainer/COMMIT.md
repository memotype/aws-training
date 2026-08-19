<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Maintainer Commit Instructions

Create a checkpoint commit of the currently reviewed Maintainer changes.

Inspect the complete working tree and index, preserve unrelated operator
changes, run all validation required by current governance, stage only the
in-scope reviewed changes, and create one concise commit describing the
resulting repository state.

Do not push or perform any other Git, GitHub, AWS, or external mutation not
directly required for the commit.

After committing, report the commit hash, subject, files included, validation
performed, and resulting working-tree/index status.
