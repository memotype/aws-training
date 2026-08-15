# Maintainer Working State

This file is Maintainer's working memory for repository-development handoffs.
It supplies current context and plans but does not select a mode, grant
authority, or override governance. A fresh session reads it after the canonical
governance documents and `ISSUES.md`, then acknowledges Maintainer mode and
waits for the operator's task.

## Current phase

The repository is in its governance and structure phase before practical AWS
training begins. Its planned responsibilities are:

- shared training-range infrastructure under `infra/`
- trainee exercise infrastructure under `labs/`
- governance, architecture, standards, and training documentation under
  `docs/`
- small repository-maintenance and validation utilities under `tools/`

Maintainer governance and its session prompt are present. Examiner and
Drillmaster governance and session prompts remain planned. No infrastructure as
code tool, shared infrastructure design, or lab contract is selected yet.

## Working governance state

Maintainer sessions use two non-governing working records:

- `ISSUES.md` holds stable, prioritized maintenance findings.
- `SCRATCH.md` holds this evergreen handoff state and future plans.

The issue register contains M-001 through M-012. M-002 is resolved: root
governance now separates absolute AWS prohibitions from actions that a mode and
task may conditionally authorize. M-001 and M-004 are medium-priority open
design decisions, while M-003 is low priority. M-012 records the replacement
of the stale handoff snapshot with this working state.

The Maintainer initialization prompt intentionally requires Codex to
acknowledge the active mode and wait for a separate operator task. M-011 tracks
that accepted usability tradeoff.

Shared governance requires Markdown files in a changeset to be linted. It also
requires a repository-wide Markdown lint before a commit unless the operator
expressly overrides the check.

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

## AWS state boundary

Repository source describes governance and intended future design only. It
does not establish current deployed AWS state. No live AWS evidence is recorded
for this maintenance phase, and Maintainer performs no AWS mutation or
deployment.

## Planned maintenance

The next planned design task is to draft Examiner governance and its session
prompt. M-001, concerning governance activation, does not block drafting but
should be resolved before newly written mode governance is activated. M-004,
concerning ownership of routine AWS deployment and cleanup, should be decided
while the overall mode set is designed. M-003 is lower-priority wording
cleanup.

Later repository work includes:

- drafting Drillmaster governance and its session prompt
- defining standards for AWS scope, credentials, naming, tagging, and cost
- defining architecture and the boundary between shared and lab infrastructure
- writing repository, `infra/`, and `labs/` documentation
- designing the lab template contract
- selecting an infrastructure-as-code tool and reproducible local conventions

There is no pre-authorized next implementation step. A fresh Maintainer session
waits for the operator to choose and authorize the next repository outcome.
