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
workflow, and the changelog and milestone model are present in repository
source. Examiner and Drillmaster governance and session prompts are not yet
implemented. No infrastructure-as-code tool, shared infrastructure design, lab
framework, or lab contract is selected yet.

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

The npm manifest and lock file preserve the Markdown lint dependencies.
`.gitignore` excludes local editor configuration, `node_modules`, npm debug
logs, and Vim swap files. Infrastructure-as-code ignore rules remain deferred
until the tool and runtime artifact conventions are selected.

## Release model

Project milestones use intentional SemVer-shaped version tags. Release
preparation curates only material milestone changes into `CHANGELOG.md`.
The current `Unreleased` entry is being curated toward the first intentional
milestone. Its version remains an operator decision. The entry presents the
user-facing delta without duplicating commits, GitHub Issues, or this handoff.

## AWS state boundary

Repository source describes governance and intended future design only. It
does not establish current deployed AWS state. No live AWS evidence is recorded
for this maintenance phase, and Maintainer performs no AWS mutation or
deployment.

## Undeveloped areas

The live Maintainer issue queue provides the authoritative discrete work and
priorities. Broader areas not yet developed include:

- Examiner and Drillmaster governance and session prompts
- defining standards for AWS scope, credentials, naming, tagging, and cost
- defining architecture and the boundary between shared and lab infrastructure
- writing repository, `infra/`, and `labs/` documentation
- designing the lab template contract
- selecting an infrastructure-as-code tool and reproducible local conventions
