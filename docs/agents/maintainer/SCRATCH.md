<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Maintainer Working State

This file is Maintainer's working memory for repository-development handoffs.
It supplies current context and plans but does not select a mode, grant
authority, or override governance. A fresh session reads it after the canonical
governance documents and the required Maintainer GitHub issue discovery
attempt, then acknowledges Maintainer mode and waits for the operator's task.

## Current phase

The repository is in its governance and structure phase before practical AWS
training begins. Its planned responsibilities are:

- shared training-range infrastructure under `infra/`
- trainee exercise infrastructure under `labs/`
- governance, architecture, standards, and training documentation under
  `docs/`
- small repository-maintenance and validation utilities under `tools/`

Maintainer governance, its session prompt, the GitHub issue-backed maintenance
workflow, the changelog and milestone model, and the MIT / CC BY 4.0 licensing
design are implemented. Initial Examiner governance and its session prompt are
also implemented without mode-specific persistent working memory; examination
context is reconstructed from canonical exercise material, trainee evidence,
and authorized current observations. Drillmaster governance and its session
prompt are not yet implemented. No
infrastructure-as-code tool, shared infrastructure design, lab framework, or
lab contract is selected yet.

## Handoff boundary

GitHub Issues carrying the `maintainer` label are the durable source for
discrete work, decisions, priority, and lifecycle. A fresh query establishes
their current state. This file retains only broader context needed across
Maintainer sessions and must not be treated as a snapshot of the issue queue.

The Maintainer session continues to use the deliberate initialization
handshake: complete discovery, acknowledge the mode, and wait for a separate
operator task.

## Repository tooling

The repository uses locally installed `markdownlint-cli2` with configuration in
`.markdownlint-cli2.jsonc`. A targeted check uses `--no-globs`, while the
repository-wide check runs:

```sh
npx markdownlint-cli2
```

Shared governance adopts REUSE 3.3 as the repository's file-level SPDX
licensing profile. The isolated virtual project in `tools/reuse/` declares
REUSE 6.2.0 in `pyproject.toml`, resolves its transitive dependencies in
`uv.lock`, and requires uv 0.12.2. The documented repository-wide check is:

```sh
uv run --project tools/reuse --locked --isolated reuse --root . lint
```

The command builds an isolated environment outside the repository working tree
from the committed lock before running `reuse lint`; `--locked` rejects stale
dependency metadata instead of updating it. A globally installed `reuse`
executable is not the repository's validator authority.

Covered commentable files carry inline metadata. The strict npm JSON files use
adjacent `.license` sidecars, and their ecosystem-native license fields point
to `LICENSE.md` without representing the repository as single-licensed. The
literal SPDX example in shared governance is enclosed by REUSE ignore markers
so it is not mistaken for operative file metadata. No `REUSE.toml` mapping is
needed.

`LICENSE.md` is covered by the project's `CC-BY-4.0` policy but is exempt from
REUSE metadata as the root licensing overview. The canonical license texts
under `LICENSES/` remain unannotated REUSE license files. Current Git and
publication state must be established from Git and GitHub rather than inferred
from this handoff.

The npm manifest and lock file preserve the Markdown lint dependencies.
`.gitignore` excludes local editor configuration, `node_modules`, npm debug
logs, Vim swap files, and uv virtual environments.
Infrastructure-as-code ignore rules remain deferred until the tool and runtime
artifact conventions are selected.

The project-scoped Codex configuration exposes AWS knowledge tools without
requiring configured AWS credentials through `mcp-proxy-for-aws` 1.6.4. It
uses the conventional exact-version `uvx` invocation with proxy read-only mode
and an explicit tool allowlist; no authenticated AWS API execution tools are
exposed, and a separate locked tool project is not justified for this
non-deterministic remote knowledge dependency. The proxy's `--skip-auth` mode
may still consult ambient AWS credentials for transport signing when they are
available. Hard ambient-credential isolation, authenticated Agent Toolkit
access, and mode-specific AWS profiles remain deferred pending separate design,
governance, implementation, and validation.

## Remaining SPDX work

Continuous enforcement remains a future, separately authorized stage:

- Add a deterministic CI check that runs the same pinned REUSE validation used
  locally.
- Pin external CI actions and validator artifacts immutably where practical.
- Ensure new CI configuration carries the correct `MIT` metadata and does not
  create a hidden dependency on mutable global tooling.
- Validate the workflow locally or statically to the extent possible before
  any separately authorized publication.

## Release model

Project milestones use intentional SemVer-shaped version tags. Release
preparation curates only material milestone changes into `CHANGELOG.md`.
`v0.1.0` is the existing project milestone. The current `Unreleased` entry is
being curated toward a later milestone whose version remains an operator
decision. The entry presents the user-facing delta without duplicating commits,
GitHub Issues, or this handoff.

## AWS state boundary

Repository source describes governance and intended future design only. It
does not establish current deployed AWS state. No live AWS evidence is recorded
for this maintenance phase, and Maintainer performs no AWS mutation or
deployment.

## Cross-mode authority

The lifetime of otherwise compatible task-specific authority across an
explicit mode switch remains a shared-governance question tracked by #5.
Examiner independently prohibits AWS mutation regardless of authority held by
an earlier mode or task, but that safety boundary does not resolve the broader
cross-mode authorization model.

## Undeveloped areas

The live Maintainer issue queue provides the authoritative discrete work and
priorities. Broader areas not yet developed include:

- Drillmaster governance and session prompts
- defining standards for AWS scope, credentials, naming, tagging, and cost
- defining architecture and the boundary between shared and lab infrastructure
- writing repository, `infra/`, and `labs/` documentation
- designing the lab template contract
- selecting an infrastructure-as-code tool and reproducible local conventions
