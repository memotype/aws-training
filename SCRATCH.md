# Maintainer Handoff State

Updated: 2026-08-14

This is a temporary, low-authority working note. It does not select an
operating mode, grant permission, or override any governance document. A fresh
session must be initialized by the operator with the appropriate canonical
`SESSION.md` prompt before doing non-trivial work.

## Repository purpose

This repository is being built as a practical AWS training range for the AWS
Certified DevOps Engineer - Professional exam (DOP-C02). It will contain:

- governance and session prompts under `docs/`
- training-range IaC under `infra/`
- trainee lab IaC under `labs/`

The repository is still in its initial governance and structure phase. No IaC
tool has been chosen, no AWS infrastructure has been created through this work,
and no AWS inspection or mutation was performed in the prior session.

## Canonical governance files now present

- `CODEX.md` - root and highest-authority repository governance
- `docs/agents/SHARED.md` - rules that apply across every operating mode
- `docs/agents/maintainer/MAINTAINER.md` - Maintainer-specific permissions and
  boundaries
- `docs/agents/maintainer/SESSION.md` - thin Maintainer initialization prompt

The canonical planned files established by `CODEX.md` but not yet created are:

- `docs/agents/examiner/EXAMINER.md`
- `docs/agents/examiner/SESSION.md`
- `docs/agents/drillmaster/DRILLMASTER.md`
- `docs/agents/drillmaster/SESSION.md`

## Decisions established with the operator

### Modes

There are three modes:

- Maintainer manages repository design and source at the meta-level.
- Examiner inspects, evaluates, questions, and grades trainee work.
- Drillmaster conducts bounded, authorized fault-injection exercises.

At the start of a new session, the operator selects the mode by pasting the
associated canonical `SESSION.md` prompt. During that session, the operator may
switch modes with an explicit instruction. Task subject or task completion must
not be interpreted as a mode switch.

### Shared versus mode-specific governance

Use this test when factoring rules:

> Would the operator still want this rule to apply if Codex were currently
> Examiner or Drillmaster?

If yes, it probably belongs in `docs/agents/SHARED.md`. If it describes what
Maintainer is allowed to do, it belongs in `MAINTAINER.md`.

The first refactor using this test has been completed. Shared governance now
owns cross-mode rules for scope, workflow authorization, evidence, working-tree
safety, Git, AWS-operation safeguards, IaC hygiene, lab/material separation,
secrets, dependencies, tooling, verification, handoff, and mode transitions.
Maintainer governance retains its repository permissions and its stricter AWS
access boundary.

### Governance filenames

Mode governance documents are named after their modes so they remain
identifiable outside their directories:

- `MAINTAINER.md`
- `EXAMINER.md`
- `DRILLMASTER.md`

Do not use a generic filename such as `GOVERNANCE.md` for these files.

### Git policy

The intended principle is:

> Working-tree edits may be normal work when the active mode permits them, but
> Git repository-state mutations require explicit operator authorization.

Git is limited to read-only inspection unless the operator requests a Git end
state. Authorization is outcome-oriented rather than command-by-command. For
example, "commit these changes" authorizes reviewing and staging the applicable
changes and creating that commit; it does not authorize including unrelated
changes, pushing, switching branches, stashing, rewriting history, or
discarding work.

### Maintainer AWS boundary

Maintainer normally works without AWS credentials. Read-only AWS inspection
requires an explicit task need and the safeguards in `MAINTAINER.md`.
Maintainer never authorizes AWS mutation or deployment. Editing IaC source is
not authorization to apply it.

### Session prompts

Session prompts should remain thin. They select a mode and point to canonical
governance; they should not duplicate policy or create permissions that can
drift from governance.

The Maintainer prompt intentionally ends by requiring Codex to acknowledge the
active mode and await a separate repository-maintenance task. It does not say
to continue work, and it does not restate the authority hierarchy.

## Current repository state

The repository has no commits yet and is on `main`. Current files are untracked.
No files have been staged, stashed, committed, pushed, or otherwise published.

Directories currently present:

- `docs/agents/{maintainer,examiner,drillmaster}`
- `docs/architecture`
- `docs/standards`
- `infra`
- `labs/template`
- `tools`

Most directories are empty and therefore will not be retained by Git until
real files are added. Prefer useful documents over `.gitkeep` placeholders.

The current `.gitignore` contains only Vim swap-file patterns. It still needs
to be expanded after the IaC tool and local runtime-data conventions are
chosen. Do not broadly ignore files that should be reproducible and committed,
such as provider lock files.

## Work not yet done

- The operator has not completed review of the first drafts of `SHARED.md` and
  `MAINTAINER.md`; further discussion and refinement are expected.
- Examiner governance and its session prompt have not been drafted.
- Drillmaster governance and its session prompt have not been drafted.
- Standards for AWS scope, credentials, naming/tagging, cost controls, and lab
  contracts have not been written.
- Repository, `infra/`, and `labs/` README files have not been written.
- The lab template contract has not been designed.
- No IaC tool or `infra/` substructure has been selected.
- No AWS credentials or live AWS state have been inspected.

There is no pre-authorized next implementation step. After initialization, a
fresh Maintainer session should acknowledge the mode, read this note when the
operator directs it to do so, and await the operator's next task.

## Authorization reminder

The prior session received narrow authorization to edit `CODEX.md` to add
Maintainer mode and canonical governance paths. Those edits are complete. Do
not treat that prior authorization as continuing permission to edit
`CODEX.md`.

This handoff request authorized only the working-tree edit to `SCRATCH.md`. It
did not authorize staging, committing, branching, stashing, pushing, AWS
access, dependency installation, or any other external or repository-state
mutation.
