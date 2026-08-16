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

## 5) Git and external repository state

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

Working-tree state, Git repository state, and remote service state are distinct
authorization domains. Creating, editing, labeling, commenting on, reopening,
or closing a GitHub Issue changes durable remote state even though it does not
stage files or alter local Git history. Requests for local file or Git outcomes
do not implicitly authorize those remote mutations, and requests for remote
outcomes do not implicitly authorize working-tree or Git mutations.

The active mode or an explicit governed workflow may grant narrowly scoped
read-only remote discovery. Possession of authentication or the ability to run
a remote command is not authority to query other data or mutate remote state.
Any authorized remote mutation must follow the end-state authorization rule in
section 2 and remain limited to the requested outcome and targets.

### 5.1) GitHub Issue resolution and closure

Closing an implementation-backed GitHub Issue represents durable resolution in
the canonical published repository, not completion in a working tree or an
unpublished local commit. For repository changes, canonical published state is
the state of the expected GitHub repository's default branch unless an
authorized governed workflow explicitly designates another canonical branch.
In a direct workflow, the resolving commit must be pushed to that branch; in a
branch or pull-request workflow, the resolving changes must be merged into it.
An ordinary issue closure does not require a version tag or GitHub Release.

Implementation, committing, publication or merge, and issue closure are
separately authorized outcomes under section 2. Authority for one does not
imply authority for another, and the existence of an issue does not create an
automatic branch, commit, push, merge, or closure workflow.

Immediately before closing a repository-backed issue, Codex must verify through
GitHub that the resolving state is present on the expected canonical branch in
the expected repository. A matching local commit or a previous push or merge
attempt is not evidence of publication. Codex must not arrange automatic issue
closure through a commit or pull request because that would bypass this
verification step. Until publication and verification occur, a fully
implemented and validated issue remains open and must be handed off as **ready
to close after publication**. This handoff does not require a new label or
custom issue state.

An issue may close without a repository change when the authorized outcome is
a non-implementation disposition whose durable resolution is fully represented
by the issue itself, such as not planned, duplicate, invalid or superseded
work, or an issue-contained decision. If resolving a decision also requires
governance, documentation, or other repository changes, the repository-backed
lifecycle applies.

### 5.2) Version tags and releases

Version tags name intentional project milestones and must use the form
`vMAJOR.MINOR.PATCH`.

The Git tag is the canonical version marker. A GitHub Release is optional
publication metadata for that exact tag and does not replace or create a
different version identity.

Before `v1.0.0`, version numbers have these repository-specific meanings:

- `v0.MINOR.0` identifies a meaningful development milestone while the
  training range is still being designed or built.
- `v0.MINOR.PATCH` may identify a correction to an already tagged development
  milestone when a separate patch milestone is useful.
- `v1.0.0` identifies the first version the operator considers a coherent,
  usable AWS training range.

After `v1.0.0`, use ordinary semantic-versioning judgment where practical:
increment the major version for materially incompatible structural or workflow
changes, the minor version for substantial backward-compatible capabilities,
and the patch version for corrections.

Tags are intentional, never automatic. Creating, moving, deleting, or pushing
a tag, and creating, editing, or deleting a GitHub Release, each requires an
explicit operator-authorized outcome. Preparing a release or editing
`CHANGELOG.md` does not by itself authorize any of those mutations. A request
to create a local tag does not implicitly authorize pushing it or creating a
GitHub Release.

A release tag must point to the exact reviewed commit containing the matching
changelog entry. Before creating a tag, Codex must verify the intended target,
confirm that the index and working tree are clean, and inspect existing local
and remote tags to avoid collision or reuse. Published version tags must not be
moved or reused as a correction mechanism; a new version should normally be
created instead.

### 5.3) Changelog

`CHANGELOG.md` is the curated, user-facing record of material project changes.
It is not a commit log, issue tracker, working-memory handoff, or chronological
diary.

After material work begins following the newest version tag, the changelog must
contain one working entry headed `## Unreleased` above all released entries.
Before the first version tag, that entry summarizes the material project state
being built toward the first milestone. Immediately after a release, the file
may contain only released entries until the next material change begins.

The working entry must be tended as material work continues. It should read as
a concise overview for a repository user asking what has changed since the
newest tag, as though the current state were being released today. Related
changes should be consolidated into durable outcomes rather than accumulated as
individual edits. Minor wording, formatting, lint-only, and other
non-material implementation changes should normally be omitted.

The `Unreleased` entry and released entries must:

- appear in reverse chronological order
- summarize resulting project behavior, design, or capability rather than the
  sequence of commits used to produce it
- use only the relevant `Added`, `Changed`, `Fixed`, `Removed`, or `Security`
  subsections
- remain simple and accessible to a reader who does not know the implementation
  history

Issue references may be included when they materially improve the record, but
the changelog must not reproduce issue histories or handoff state.

When preparing a release, Maintainer must compare the working entry with the
material repository changes since the previous tag, then consolidate, prune,
and reword it into the overall release summary. The finalized entry must:

- replace `## Unreleased` with `## vMAJOR.MINOR.PATCH - YYYY-MM-DD`
- correspond exactly to the version tag being prepared
- use the date on which the finalized release changes are committed
- summarize all and only the material changes included in that milestone

If the release commit will occur on a different date, the entry must be updated
and finalized again before staging. Codex must finalize and review the
changelog entry before staging release changes. Staging, committing, creating a
tag, pushing it, and creating a GitHub Release occur only afterward and remain
separately authorized outcomes.

Once a release is tagged, its changelog entry is historical and must not be
rewritten for subsequent project changes. A task may authorize a genuine
documentation correction to a released entry; all other changes belong in a
later `Unreleased` entry. Finalizing a release must not add an empty replacement
`Unreleased` entry.

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

## 11) SPDX and REUSE licensing compliance

The repository uses SPDX short-form license expressions and adopts the
[REUSE Specification 3.3](https://reuse.software/spec-3.3/) as its operational
profile for file-level copyright and licensing information. `LICENSE.md`
defines which project material is licensed under `MIT` and which is licensed
under `CC-BY-4.0`.

Every file covered by REUSE 3.3 must have complete and accurate licensing
information associated with it:

- at least one `SPDX-FileCopyrightText` notice identifying the actual copyright
  holder and applicable publication year or years
- at least one `SPDX-License-Identifier` tag containing a valid SPDX license
  expression that accurately describes the file

Existing copyright and licensing notices must be preserved. Codex must not
attribute third-party work to the operator, replace a third party's license, or
claim rights that the operator does not hold.

Commentable files must carry their licensing information in a comment header as
near the beginning as the file format safely permits. The header must not
precede or invalidate a required shebang, encoding declaration, document type,
or other format-sensitive prefix. An uncommentable file must use an adjacent
`.license` file. `REUSE.toml` may be used only when individual headers or
sidecars are impractical, and each mapping must be explicit and reviewable.

The license expression must follow the material boundary in `LICENSE.md`:

- use `MIT` for code, infrastructure configuration, automation, and other
  machine-oriented technical material
- use `CC-BY-4.0` for governance, documentation, and other human-oriented
  material
- select one license for a normal project file according to its primary purpose
- treat small or illustrative code, commands, configuration fragments, and
  other technical examples in a human-oriented document as part of that
  `CC-BY-4.0` document; do not create mid-document license changes or SPDX
  snippet tags for ordinary embedded examples
- when embedded technical material becomes substantial enough to be
  independently reusable, prefer moving it into a separate `MIT`-licensed file
  and referencing it from the documentation

Primary purpose and reasonable engineering judgment control this boundary; no
numerical size threshold applies. SPDX snippet metadata is exceptional, not a
normal project workflow. It may be used when necessary to represent genuinely
different licensing that cannot be cleanly separated, such as incorporated
third-party material. Existing third-party copyrights and licenses must remain
intact, and material the project lacks authority to relicense must not be
silently absorbed under a containing file's project license.

License texts must be plain-text files named
`LICENSES/<SPDX-License-Identifier>.txt`. The directory must contain a license
text for every license referenced by covered files and no unused or unrelated
files. Each license text must be an unmodified copy of the applicable
authoritative license text. Copyright holders and years, SPDX metadata,
explanations, and other project-specific content must not be substituted into
or added to canonical license texts. Project copyright ownership belongs in
file-level metadata; REUSE excludes the license texts themselves from covered
files.

For original project files authored by the operator, file-level copyright
metadata must identify `Isaac Freeman <memotype@gmail.com>` as the copyright
holder and use the actual applicable year or years. For current original
material created in 2026, the normal form is:

```text
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: MIT
```

The license identifier must instead be `CC-BY-4.0` when that is the file's
license. This convention must not be assigned mechanically to third-party
material or work whose copyright ownership has not been established.

Every repository change must preserve accurate licensing information for each
file it adds, modifies, moves, or incorporates. Before completing repository
work and before creating a commit, Codex must run the repository's pinned REUSE
validator across the full repository and resolve every applicable failure.
Running the validator does not authorize a commit or any other Git mutation.

This section governs copyright and license metadata. It does not require an
SPDX software bill of materials unless the current task or a lower-authority
repository standard separately requires one.

## 12) Verification and handoff

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
