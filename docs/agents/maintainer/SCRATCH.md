<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Maintainer Working State

This file is Maintainer's working memory for repository-development handoffs.
It supplies current context and plans but does not select a mode, grant
authority, or override governance. A fresh session reads it during the governed
read-only Maintainer orientation, reports repository and Issue-queue state, and
then asks the operator to continue an existing Issue or start a new work unit.

## Current phase

The repository is in its governance and structure phase before practical AWS
training begins. Its planned responsibilities are:

- shared training-range infrastructure under `infra/`
- trainee exercise infrastructure under `labs/`
- governance, architecture, standards, and training documentation under
  `docs/`
- small repository-maintenance and validation utilities under `tools/`

Maintainer governance, its operational prompts, the GitHub Issue-backed work
lifecycle, the changelog and milestone model, and the MIT / CC BY 4.0 licensing
design are implemented. Substantive Maintainer work uses one durable Issue and
dedicated branch across ephemeral sessions; checkpoint, publication, Issue
completion, and branch cleanup remain distinct outcomes, while one explicit
post-merge invocation may authorize the last two together as an ordered,
resumable workflow. A root README provides the human-facing project entry
point, current status, governed startup workflow, repository map, and local
validation commands. A tracked safe example, gitignored per-clone TOML file,
shared offline Python reader, and external XDG runtime-state contract provide
non-secret operator-local parameters without coupling the public repository to
one AWS account. Initial Examiner governance and its session prompt are also
implemented without mode-specific persistent working memory; examination
context is reconstructed from canonical exercise material, trainee evidence,
and authorized current observations. Native CloudFormation source defines the
first shared infrastructure component, a persistent S3 store for packaged
Lambda artifacts, with an isolated uv-locked `cfn-lint` environment for local
validation. Drillmaster governance and its session prompt are not yet
implemented. No repository-wide infrastructure-as-code choice, broader
shared-infrastructure design, lab framework, or lab contract is selected yet.

## Handoff boundary

GitHub Issues carrying the `maintainer` label are the durable source for
discrete work, decisions, priority, lifecycle, and concise work-unit handoff.
A fresh query establishes their current state. This file retains only broader
context needed across work units and must not be treated as a snapshot of the
issue queue or a replacement for Issue-specific handoff.

The Maintainer session uses a read-only initialization handshake: complete
discovery, acknowledge the mode, report orientation state, and stop for the
operator to select an existing Issue or a new work unit.

## Repository tooling

The repository uses locally installed `markdownlint-cli2` with configuration in
`.markdownlint-cli2.jsonc`. A targeted check uses `--no-globs`, while the
repository-wide check runs:

```sh
npx markdownlint-cli2
```

The isolated virtual project in `tools/cloudformation/` pins `cfn-lint` 1.55.1
and requires uv 0.12.2. Its canonical artifact-store validation is:

```sh
uv run --project tools/cloudformation --locked --isolated \
  cfn-lint infra/artifact-store/template.yaml
```

This local repository-source check makes no AWS API call and does not establish
deployment state. The native CloudFormation template does not add a deployment
wrapper or select an IaC system for future labs.

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
logs, Vim swap files, Python bytecode caches, and uv virtual environments.
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
access, and provisioned mode-specific AWS identities remain deferred pending
separate design, governance, implementation, and validation.

## Operator-local configuration and state

`.aws-training.example.toml` defines the tracked, non-secret configuration
shape, while `.aws-training.local.toml` is the explicitly ignored per-clone
file. AWS CLI profile names abstract external credential providers; the
operator profile is required, Examiner and Drillmaster profiles remain
optional, and Maintainer has no AWS profile. The Python 3.11 standard-library
reader in `tools/aws_training_config.py` requires TOML contract version 1 and
validates and normalizes the shared contract without contacting AWS or loading
credentials. Each clone declares a bounded cost policy; the safe example
requires the Free plan and zero out-of-pocket cost, while the public contract
also supports non-Free-plan accounts with a finite non-negative ceiling.

Expected account and primary Region values are future preflight safety
assertions, not current observations or authority. In an already-authorized AWS
workflow, caller identity is an initial preflight query and regional calls must
select the configured or exercise-permitted Region explicitly. Runtime state
defaults to the external XDG state location and may be overridden only to
another path outside the Git working tree. The version 1 append-only
`operations.jsonl` contract is only for future mutation-capable Codex workflows
to record per-resource operation events and later `restoration_verified` events
that reference the originals; it does not require human-authored entries. No
writer, AWS preflight, mutation workflow, or external runtime directory exists
yet.

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
`v0.2.0` is the current project milestone. Later material work begins a new
`Unreleased` entry that presents the user-facing delta without duplicating
commits, GitHub Issues, or this handoff.

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
- defining full AWS scope, identity provisioning, naming, tagging, and cost
  enforcement standards beyond the local parameter contract
- defining broader architecture and the boundary between shared and lab
  infrastructure
- writing broader `infra/` and `labs/` documentation
- designing the lab template contract
- selecting infrastructure-as-code conventions for future shared components
  and labs
