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
design are present in the current working tree. Canonical license texts and the
human-readable license boundary are present, but repository-wide file-level
SPDX metadata and validation are not yet implemented. Examiner and Drillmaster
governance and session prompts are not yet implemented. No infrastructure-as-
code tool, shared infrastructure design, lab framework, or lab contract is
selected yet.

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
licensing profile. The existing files are not yet annotated, and no REUSE
validator is selected, installed, or pinned. The licensing and governance
baseline is present in repository source. Its current Git and publication state
must be established from Git and GitHub rather than inferred from this handoff.

The npm manifest and lock file preserve the Markdown lint dependencies.
`.gitignore` excludes local editor configuration, `node_modules`, npm debug
logs, and Vim swap files. Infrastructure-as-code ignore rules remain deferred
until the tool and runtime artifact conventions are selected.

## Staged SPDX adoption plan

The stages below are the current plan for completing repository-wide SPDX and
REUSE adoption. A fresh Maintainer session must verify the working tree and
current governance before relying on this handoff. Completing one stage does
not authorize a later stage, a Git mutation, publication, or an external
effect.

### Stage 1: Establish the governed baseline

- Confirm that the operator accepts the licensing and shared-governance design
  currently present in the working tree.
- Reinitialize or reaffirm Maintainer mode under the accepted governance before
  relying on its SPDX requirements.
- Obtain explicit operator authorization before editing `CODEX.md` to add
  file-level metadata.
- Obtain explicit operator authorization before installing or adding a REUSE
  validator dependency.
- Preserve unrelated working-tree changes and keep committing and publication
  as separately authorized outcomes.

### Stage 2: Inventory and classify covered files

- Enumerate the files covered by REUSE 3.3 from the actual working tree rather
  than from this handoff.
- Confirm copyright ownership and preserve all existing third-party notices;
  do not mechanically attribute uncertain or third-party material to the
  operator.
- Apply `CC-BY-4.0` to human-oriented governance and documentation files and
  `MIT` to machine-oriented code, configuration, automation, manifests, and
  lock files according to `LICENSE.md`.
- Treat ordinary technical examples inside human-oriented documents as part of
  the containing document. Do not plan mid-document license changes or SPDX
  snippet metadata for those examples.
- Record REUSE exemptions, including the root `LICENSE.md` overview and the
  canonical texts under `LICENSES/`, and confirm the selected validator applies
  those exclusions as expected.

The anticipated classification of the current small file set is:

- `CC-BY-4.0`: `CODEX.md`, `CHANGELOG.md`, and Markdown governance under
  `docs/`
- `MIT`: `.gitignore`, `.markdownlint-cli2.jsonc`, `package.json`, and
  `package-lock.json`
- licensing files: `LICENSE.md` is `CC-BY-4.0` under the project policy but is
  REUSE-exempt as the root licensing overview; canonical texts under
  `LICENSES/` remain unmodified and unannotated

This list is an implementation aid, not a substitute for a fresh inventory or
the authoritative boundary in `LICENSE.md`.

### Stage 3: Select reproducible validation tooling

- Select one supported REUSE validator release and a reproducible distribution
  method appropriate to the repository.
- Pin the validator and its material dependencies through a lock file,
  immutable container digest, or comparably deterministic mechanism.
- Provide one documented local command that runs full-repository `reuse lint`
  without modifying repository or external state.
- Run the validator against the unannotated baseline and use its findings to
  confirm the Stage 2 inventory before changing file metadata.

### Stage 4: Add file-level metadata

- Add `SPDX-FileCopyrightText` and `SPDX-License-Identifier` headers near the
  start of every commentable covered file, using syntax safe for its format.
- Use `2026 Isaac Freeman <memotype@gmail.com>` for current original material
  only after ownership is established, and use actual applicable years for any
  material created outside 2026.
- Use adjacent `.license` sidecars for uncommentable strict formats such as the
  current JSON manifests.
- Use an explicit, reviewable `REUSE.toml` mapping only when individual headers
  or sidecars are genuinely impractical, not merely because a mapping would be
  shorter, tidier, or more convenient.
- Keep `LICENSES/MIT.txt` and `LICENSES/CC-BY-4.0.txt` byte-for-byte canonical;
  never add project copyright or SPDX metadata to those texts.
- Add or reconcile ecosystem-native license metadata, such as the npm package
  license field, without treating it as a replacement for REUSE metadata.

### Stage 5: Validate and review the retrofit

- Run full-repository `reuse lint` and resolve every applicable finding.
- Run targeted Markdown lint for changed Markdown files and the complete
  repository-wide Markdown lint.
- Validate every changed strict-format file with its native parser or existing
  repository check.
- Compare both canonical license files with their authoritative sources.
- Review the complete cumulative diff, including sidecars and other untracked
  files, and confirm that no third-party attribution or license was lost.

### Stage 6: Add continuous enforcement

- Add a deterministic CI check that runs the same pinned REUSE validation used
  locally.
- Pin external CI actions and validator artifacts immutably where practical.
- Ensure new CI configuration carries the correct `MIT` metadata and does not
  create a hidden dependency on mutable global tooling.
- Validate the workflow locally or statically to the extent possible before
  any separately authorized publication.

### Stage 7: Curate and hand off the completed adoption

- Update `CHANGELOG.md` at the outcome level and reduce this section to the
  remaining current state rather than preserving completed steps as history.
- Report validation evidence, exemptions, third-party findings, and any files
  that require operator judgment.
- Obtain separate authorization for staging, committing, pushing, or any other
  Git or GitHub outcome.
- After the operator accepts any resulting governance-file changes, apply the
  governance activation procedure before relying on them in another session.

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

## Undeveloped areas

The live Maintainer issue queue provides the authoritative discrete work and
priorities. Broader areas not yet developed include:

- Examiner and Drillmaster governance and session prompts
- defining standards for AWS scope, credentials, naming, tagging, and cost
- defining architecture and the boundary between shared and lab infrastructure
- writing repository, `infra/`, and `labs/` documentation
- designing the lab template contract
- selecting an infrastructure-as-code tool and reproducible local conventions
