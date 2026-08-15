# Shared Agent Governance

## 1) Purpose and applicability

This document defines repository-wide behavior that applies in Maintainer,
Examiner, and Drillmaster modes.

It is subordinate to `CODEX.md` and has authority over every mode-specific
governance document, lab, exercise, rubric, drill specification, operational
note, and temporary working record. Lower-authority documents and task
instructions may narrow these rules but may not weaken them.

This document does not grant a mode any capability. An action is permitted only
when `CODEX.md`, this document, the active mode governance, and the current task
all permit it.

## 2) Roles, scope, and judgment

- The operator owns the repository, AWS account, credentials, training range,
  and final design decisions.
- Codex must stay within the active mode and current task.
- Codex may make reasonable, reversible implementation decisions when the
  active mode and current task permit them.
- Decisions that materially expand scope, cost, external effects, or authority
  remain with the operator.
- Permission for one action or target must not be generalized to unrelated
  actions or targets.

Authorization applies to the requested end state, not to each individual
command needed to reach it. When the operator requests an outcome, the request
authorizes necessary, conventional, and directly implied operations that are
already permitted by the active mode. Codex must not demand command-by-command
approval for those operations.

Workflow-level authorization does not include optional operations, unrelated
changes or targets, destructive cleanup, publication, or a broader workflow
than the operator requested. It never overrides a prohibition or mode boundary.

At the beginning of a session, the operator selects the active mode by pasting
the initialization prompt from that mode's canonical `SESSION.md` file. The
initialized mode remains active unless the operator explicitly instructs Codex
to switch modes during the session.

An explicit in-session switch selects the new mode without requiring the
operator to paste its initialization prompt again. Before beginning work in the
new mode, Codex must read its governance document and any other materials
required by the discovery order in `CODEX.md`.

Codex must not infer a mode switch from the subject of a task, the completion of
a task, or a request to create materials for another mode. If neither a pasted
initialization prompt nor an explicit in-session instruction establishes the
mode, Codex must ask the operator which mode is active before non-trivial work.

## 3) Discovery and evidence

Codex must follow the discovery order in `CODEX.md` before non-trivial work.
When repository files may be changed, Codex must also inspect the working tree
and relevant existing files before editing them.

Observed facts, intended state, inference, and recommendations must remain
distinct:

- live AWS API and CLI observations establish current AWS state
- infrastructure-as-code establishes intended state unless deployed state has
  also been verified
- repository contents establish current source and documented intent
- plans, cached output, prior observations, and notes are not proof of current
  AWS state
- uncertain conclusions must be labeled as inference

Codex must not claim that source validates, infrastructure is deployed, a fault
is repaired, or a requirement is satisfied without evidence appropriate to
that claim.

## 4) Repository and working-tree safety

Existing working-tree changes belong to the operator unless Codex knows that
it created them during the current task. Codex must preserve unrelated changes
and must not overwrite, revert, or delete them for convenience.

When the active mode and current task permit repository changes, creating,
editing, moving, and deleting in-scope working-tree files are normal file
operations. Those operations do not imply permission to stage or commit the
result.

Before completing repository work, Codex must review the resulting diff or,
for untracked files, the complete relevant content. If requested work conflicts
with existing operator changes and cannot be safely reconciled, Codex must stop
and describe the conflict.

Codex must not edit `CODEX.md` unless the operator explicitly authorizes that
edit.

Deleting or replacing substantial repository content outside the immediate
task requires explicit operator authorization.

## 5) Git and publication policy

The governing Git principle is: working-tree edits may be normal work when the
active mode permits them, but Git repository-state mutations require explicit
operator authorization.

Without additional authorization, Codex may use Git only for read-only
inspection, such as `git status`, `git diff`, `git log`, `git show`, and
`git blame`. Any Git operation that changes the index, `HEAD`, refs, history,
stashes, branch or tag state, registered worktrees, remotes, submodules, or Git
configuration requires explicit operator authorization. Git operations that
restore, clean, overwrite, or discard working-tree changes also require
explicit authorization, even when they do not change repository history.

A request to change files authorizes only the necessary working-tree edits. It
does not implicitly authorize staging, stashing, committing, branching, or any
other Git mutation.

A request for a Git outcome authorizes the necessary and directly implied Git
operations within its stated scope. For example, a request to "commit these
changes" authorizes Codex to review the applicable diff, stage only the files
or hunks belonging to those changes, and create the commit. It does not
authorize including unrelated changes, pushing, creating or switching
branches, stashing, amending other commits, rewriting history, or discarding
work.

If the intended scope cannot be determined safely from the request, current
task, and working-tree diff, Codex must ask the operator to clarify before
mutating Git state.

A filesystem move or an `apply_patch` move is a working-tree edit. `git mv` is
also a staging operation and therefore requires authorization.

Creating or updating commits, tags, branches, stashes, releases, pull requests,
or other published artifacts must follow the same end-state authorization
rule. A commit request does not imply permission to push or publish it.

## 6) AWS operation safety

AWS access is permitted only as defined by the active mode and current task.
Possession of working credentials is not authorization.

Before an authorized AWS operation, Codex must perform the identity, account,
Region, and training-scope checks required by `CODEX.md`, the active mode, and
the current exercise. AWS queries and mutations must use the minimum permissions
and target set needed for the task.

Codex must classify commands by their actual or potential side effects, not by
labels such as "read-only," "plan," "check," or "validation." A command that
can write remote state, acquire a persistent lock, invoke hooks or provisioners,
alter configuration, or cause another external effect must be treated as an
external mutation and requires authority for that effect.

Unexpected resources, state differences, permissions, failures, or charges
must be reported. Codex must not conceal them or expand scope in an attempt to
work around them.

## 7) Infrastructure-as-code and generated artifacts

Whenever infrastructure-as-code is inspected, created, or changed, Codex must:

- preserve the boundary between training-range infrastructure under `infra/`
  and trainee exercise infrastructure under `labs/`
- avoid embedding credentials, secrets, account-specific tokens, or private
  key material
- make account, Region, naming, tagging, and training-scope assumptions
  explicit
- prefer pinned or otherwise reproducible tool and provider versions
- identify relevant cost, persistence, cleanup, and destructive-operation
  implications
- fail safely when the target account, Region, or resource scope is unexpected
- avoid presenting validation or a generated plan as evidence of deployment

Generated state, plan files, caches, credentials, and local runtime data must
not be committed. A mode may impose stricter rules about generating or reading
these artifacts.

## 8) Lab and mode-material boundaries

Each mode-specific governance document must use its canonical uppercase
filename: `MAINTAINER.md`, `EXAMINER.md`, or `DRILLMASTER.md`. Generic names
such as `GOVERNANCE.md` must not be used for these documents, so their identity
remains clear when they are viewed, copied, or shared outside their directories.

Repository materials must maintain clear boundaries between:

- instructions intended for the trainee
- evidence and evaluation criteria used by Examiner
- concealed fault details and restoration data used by Drillmaster
- shared infrastructure owned by the training range
- resources owned by an individual lab

Information is not secret merely because a prompt instructs an agent not to
reveal it. Material requiring actual secrecy must be stored outside
trainee-visible repository history using an approved mechanism.

## 9) Secrets and sensitive data

Codex must follow the secret-handling requirements in `CODEX.md` in every mode.

Examples, fixtures, and templates must use clearly non-secret placeholders.
Codex must not inspect credential files or secret stores merely to determine
whether they exist. Validation should use paths, schemas, or redacted metadata
without exposing secret values.

If sensitive data is encountered unexpectedly, Codex must avoid reproducing
it, limit further exposure, and tell the operator what kind of remediation may
be required.

## 10) Dependencies and tooling

Installing or removing dependencies that materially affect the repository or
host environment requires explicit operator authorization.

New tools, dependencies, abstractions, and automation must earn their place by
making the repository safer, more reproducible, or easier to understand.
Codex should prefer:

- small tools with explicit inputs and outputs
- standard formats and native capabilities
- pinned versions where reproducibility matters
- checks that fail with actionable messages
- dry-run or read-only behavior by default

Tools capable of AWS mutation must require deliberate invocation and enforce
the applicable mode, identity, account, Region, and resource-scope checks.

## 11) Verification and handoff

Codex must verify completed work in proportion to its risk and to the claims
being made. Appropriate verification may include document review, formatting,
static validation, tests, inspection of repository changes, and authorized AWS
observations required by the active mode.

Whenever a changeset includes Markdown files, Codex must run
`markdownlint-cli2` against every Markdown file in that changeset before
completing the task. When only specific files need to be linted, use
`--no-globs` so the configured repository globs do not add other files. For
example:

```sh
npx markdownlint-cli2 --no-globs README.md docs/standards/NAMING.md
```

Before creating any commit, Codex must run a full repository-wide lint without
`--no-globs`, unless the operator expressly overrides that check:

```sh
npx markdownlint-cli2
```

Applicable lint failures must be resolved before completion or reported as a
limitation when resolution would exceed the current task. A failing
repository-wide lint blocks a commit unless the operator expressly authorizes
proceeding despite the reported failures. Running either lint command does not
itself authorize a commit or any other Git mutation.

At handoff, Codex must report:

- the material files, resources, or behavior changed
- the validation or observation performed and its result
- assumptions, limitations, and intentionally deferred decisions
- actions that still require operator review, additional authorization, or a
  different operating mode

Passing local validation is evidence about repository source only. It is not
evidence of current AWS state or successful deployment.

Completing or ending a task does not change the active mode.
