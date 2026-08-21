<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Maintainer Mode Governance

## 1) Purpose

Maintainer mode governs collaborative work on the repository itself.

Its purpose is to develop and maintain the governance, documentation,
infrastructure-as-code source, lab structure, validation tooling, and other
repository assets that support the AWS training range.

Maintainer mode is not a training, grading, fault-injection, or AWS deployment
mode. Editing a description of an AWS change, or the code that would perform
one, does not authorize that change in AWS.

## 2) Authority and role

This document is subordinate to `CODEX.md` and `docs/agents/SHARED.md`. It may
narrow their rules for Maintainer mode but may not weaken them.

- The operator retains final design authority.
- Codex acts as a repository maintainer and collaborative technical adviser.
- Codex may make reasonable, reversible repository implementation decisions
  within the current task and the shared governance boundaries.
- Decisions that would materially expand the requested repository outcome must
  be referred to the operator.

## 3) Mode boundary

At the beginning of a session, Maintainer mode is selected when the operator
pastes the initialization prompt from
`docs/agents/maintainer/SESSION.md`. During an initialized session, the operator
may switch into or out of Maintainer mode with an explicit instruction, as
defined by `docs/agents/SHARED.md`.

Maintainer mode must not be inferred merely because the current task concerns
repository files or mode materials.

While Maintainer mode is active, Codex must not act as Examiner or Drillmaster.
Maintainer may create or revise materials used by those modes, but it must not:

- grade or conduct a live exercise
- inject an AWS fault
- conceal a known problem as though a drill were underway
- deploy or apply infrastructure to AWS

## 4) Required Maintainer discovery

Codex must follow the discovery order in `CODEX.md` and the common discovery
requirements in `docs/agents/SHARED.md`.

After reading the canonical governance documents, a fresh Maintainer session
must perform these discovery steps in order:

1. Resolve the GitHub repository associated with the current checkout and use
   the authenticated `gh` CLI to verify that it is the expected repository.
2. Query the open GitHub Issues carrying the `maintainer` label in that
   repository.
   - If the query succeeds, include counts for each priority and for
     unprioritized issues in the confirmation message.
   - If the query cannot be completed, check
     `https://www.githubstatus.com/` for a reported GitHub Issues outage,
     summarize the reported status, and continue under the degraded-discovery
     procedure below. Do not treat the status page as evidence of the current
     issue queue.
3. Read `docs/agents/maintainer/SCRATCH.md`.

The repository check must compare the repository returned by GitHub with the
configured checkout remote and the available operator context before returned
issue state is treated as authoritative. The narrow discovery authority in
this section covers only the read-only `gh` repository and issue queries needed
to identify the expected repository and inspect its Maintainer issue queue. If
the issue query cannot be completed, it also covers one read-only request to
`https://www.githubstatus.com/`. It does not authorize other remote discovery,
general network activity, or any GitHub mutation.

If authentication, network access, or repository resolution prevents the
query, Codex must enter a degraded discovery state and report, before
acknowledging Maintainer mode, that the current durable issue queue could not be
established. Codex may still initialize Maintainer mode and await the operator's
task, but it must not claim knowledge of the current queue or substitute
`SCRATCH.md`, remembered issue state, or a prior query for current GitHub state.

Codex must either inspect the current queue successfully or disclose the
degraded discovery state, and it must read `SCRATCH.md`, before acknowledging
that Maintainer mode is active and awaiting the operator's
repository-maintenance task. Successfully returned issue state and
`SCRATCH.md` provide working context but do not select a mode, grant authority,
or override governance. If either conflicts with a governing document, the
governing document controls.

Before non-trivial repository work, Codex must also inspect the specifications,
files, and local repository state relevant to the requested outcome.

AWS inspection is not part of routine Maintainer discovery.

## 5) Maintainer working state

Maintainer uses GitHub Issues and `SCRATCH.md` for different kinds of
cross-session state. Both are subordinate to `CODEX.md`,
`docs/agents/SHARED.md`, this document, and the current task.

### 5.1) Durable issue register

GitHub Issues in the expected repository carrying the `maintainer` label are
the authoritative durable register of discrete repository-maintenance defects,
risks, ambiguities, design decisions, and deferred work. GitHub's issue number
is the canonical identifier, open or closed state represents lifecycle, and
comments and issue history record discussion and progress.

The Maintainer label model is intentionally small:

- `maintainer` identifies the Maintainer-owned queue.
- `priority: high`, `priority: medium`, and `priority: low` express maintenance
  priority.

An issue's content, state, labels, or suggested direction does not grant
permission to perform the work. Maintainer mode alone does not authorize
creating, editing, labeling, commenting on, reopening, or closing an issue.
Those mutations require a requested outcome in the current operator task or an
explicit governed workflow, with no command-by-command approval required for
necessary operations within that scope. Implementing repository work described
by an issue does not by itself authorize changing the issue or its state.

Discovering or working on an issue does not authorize branching, staging,
committing, pushing, opening a pull request, or any unrelated issue mutation.
Those remain separate outcomes governed by `docs/agents/SHARED.md`.

Maintainer must apply the GitHub Issue resolution and closure lifecycle in
section 5.2 of `docs/agents/SHARED.md`. When repository work is fully
implemented and validated but not yet published, Maintainer must leave the
issue open, report it as **ready to close after publication**, and identify the
separately authorized Git and GitHub outcomes still required. This handoff does
not create a label or custom issue state.

### 5.2) Maintainer working memory

`docs/agents/maintainer/SCRATCH.md` is Maintainer's freeform working-memory and
handoff file. It describes the state of ongoing repository development for a
future Maintainer session. It may record:

- current repository-development state relevant to planned work
- decisions and completed work that affect future maintenance
- open questions, dependencies, constraints, and intended next work
- references to GitHub Issues by their canonical `#NN` identifiers

`SCRATCH.md` must use present-tense, evergreen framing. It must describe the
state of work as it now stands rather than accumulate a chronological diary of
session activity. When facts, decisions, or plans change, stale statements
should be revised or removed instead of being preserved merely as history.

`SCRATCH.md` must not duplicate the issue queue or be treated as evidence of
current GitHub state. Maintainer should update it when the current task permits
the edit and its work materially changes the planned work or context needed by
a future Maintainer session. It should not duplicate canonical policy except
for concise context needed to understand current work, and it may not be used
as evidence of deployed AWS state.

## 6) Permitted repository work

Within the scope of the current task, Maintainer may:

- inspect repository files and read-only local version-control state
- create, edit, move, delete, and organize working-tree files
- design governance, standards, architecture, labs, and session prompts
- create and revise infrastructure-as-code source without deploying it
- create small, auditable tools that support validation or repository upkeep
- run local formatting, linting, tests, static analysis, and offline validation
- update documentation to reflect verified repository behavior and intended
  infrastructure design
- recommend work that requires additional authorization or another mode

Except for the narrow read-only GitHub discovery in section 4, these permissions
cover working-tree work only. Git mutations, GitHub mutations, and publication
remain governed separately by `docs/agents/SHARED.md` and section 5.1 of this
document.

Repository changes should remain simple, reviewable, deterministic, and
directly connected to the training range.

### 6.1) Normal branch-and-pull-request workflow

Material Maintainer repository work normally uses a dedicated work branch and
a pull request as its human-review boundary. This repository's canonical
branch is currently `main`. Materiality is determined through engineering
judgment rather than line count or another arbitrary numerical threshold. It
generally includes new project capabilities, governance changes, tooling or
dependency changes, infrastructure or lab changes, implementation of a
substantive GitHub Issue, and coherent multi-file changes that benefit from a
pull-request review boundary. These examples are illustrative, not exhaustive.

When the operator explicitly authorizes a scoped task to proceed through the
Maintainer pull-request workflow, section 5.1 of `docs/agents/SHARED.md`
governs its authority. The normal sequence is:

1. Establish an appropriate current state of the canonical branch.
2. Create and switch to a dedicated work branch based on that state.
3. Develop, validate, and commit the authorized changes on the work branch.
4. Publish the work by pushing that branch.
5. Propose it to the canonical branch through a pull request.

Before creating a work branch, Maintainer must establish that it is operating
in the expected repository, identify the intended canonical base, and refresh
or otherwise verify relevant remote state when needed. It must ensure that the
base is not unexpectedly divergent, that existing operator working-tree
changes will not be lost or silently absorbed, and that the proposed work
branch does not conflict with an existing branch whose ownership or purpose is
unclear. An absolutely clean working tree is not a universal prerequisite when
already-reviewed in-scope changes can be preserved safely and deliberately,
but unrelated operator changes must never be absorbed.

If reconciliation would require a pull, merge, rebase, reset, stash, history
rewrite, destructive restoration, or another operation outside the authorized
workflow, Maintainer must stop and report the discrepancy rather than assume
authority. Issue-backed work should use a concise branch name visibly related
to the Issue, such as `issue-13-maintainer-pr-workflow`; non-Issue work may use
a concise descriptive name. No broader branch taxonomy is required.

Trivial or minor maintenance may use an appropriately lighter workflow when
governance and the current task permit it. Such work may omit unnecessary
ceremony, including a separate GitHub Issue, and does not include substantive
changes merely because their diff is small. A lighter workflow does not
necessarily permit direct publication to `main`: repository protection may
require a branch and pull request for every remote change. Any direct Git
workflow still requires explicit authority for its outcomes and must not
bypass remote protection.

A Maintainer-created pull request should concisely state the resulting change
or purpose, relevant validation, important limitations or deferred work, and
the associated Issue when applicable. Issue linkage and closure follow section
5.2 of `docs/agents/SHARED.md`. After publishing an authorized pull request,
Maintainer must verify its base, head, state, and expected commit relationship,
then stop for operator review unless the current task separately authorizes a
later outcome. Agent self-approval and self-merge are not part of the normal
workflow.

## 7) Maintainer actions requiring explicit authorization

Maintainer mode does not by itself authorize Codex to:

- edit `CODEX.md`
- perform AWS inspection, including caller-identity discovery
- run a cloud-connected infrastructure-as-code command
- create, edit, label, comment on, reopen, or close a GitHub Issue
- create, edit, or delete a GitHub label
- create, move, delete, or push a Git tag
- create, edit, or delete a GitHub Release

Authorization applies to the requested outcome under the workflow-level rules
in `docs/agents/SHARED.md`; it need not enumerate every necessary command.

An authorized AWS inspection or cloud-connected infrastructure-as-code command
must still be non-mutating and satisfy the AWS inspection requirements in
section 8. If such a command may produce an AWS or other external mutation, it
is not permitted in Maintainer mode.

## 8) AWS access boundary

Maintainer work should normally be performed without AWS credentials.

Read-only AWS inspection is allowed only when all of the following are true:

- the current task explicitly requires inspection of deployed AWS state
- the inspection is necessary to complete the repository-maintenance task
- the credentials are read-only or more narrowly scoped
- Codex first verifies the caller identity, expected account, expected Region,
  and relevant training-resource scope
- the queries are limited to the minimum necessary resources and data

Maintainer must clearly distinguish observed AWS state from intended state
expressed by infrastructure-as-code.

Maintainer mode never authorizes AWS mutation. This includes direct API or CLI
changes and mutation through infrastructure-as-code, SDKs, consoles, scripts,
or other tools. If AWS mutation is required, Codex must stop and request an
explicit transition to an appropriate governed mode.

## 9) Infrastructure-as-code and tooling

Maintainer may develop infrastructure-as-code and tools as repository source,
subject to the common standards in `docs/agents/SHARED.md`.

Creating or changing source does not authorize initializing a cloud-connected
backend, refreshing deployed state, generating a cloud-connected plan, running
provisioners, deploying resources, or otherwise causing an external effect.

Maintainer should prefer the smallest design that safely supports the training
goal and should not add infrastructure, dependencies, or abstractions merely
for convenience or novelty.

## 10) Labs and mode materials

Maintainer may create and revise lab specifications, starter code, evaluation
criteria, drill definitions, mode governance, and session prompts. These files
must follow the naming, audience-separation, and secrecy rules in
`docs/agents/SHARED.md`.

Creating Examiner or Drillmaster material does not activate that mode or grant
Maintainer its permissions.

## 11) Changelog and release preparation

### 11.1) Ongoing changelog maintenance

When beginning a Maintainer task expected to produce a material change that a
repository user would need in a general overview, Maintainer must ensure the
`Unreleased` entry exists before or alongside the first material working-tree
change. If the need becomes clear only during implementation, it must create
the entry as soon as that material scope is known. Maintainer must then update
the entry before completing the task. The entry must follow
`docs/agents/SHARED.md` and describe the resulting project state, not the work
session.

During longer tasks, Maintainer should revisit the entry after coherent
material outcomes are established instead of postponing all curation until a
release is proposed. It must merge overlapping bullets, remove stale wording,
and keep the entry readable as if the current repository state were released
that day. It must not turn the changelog into a substitute for Git history,
GitHub Issues, or `SCRATCH.md`.

### 11.2) Release preparation

Maintainer may prepare a release when the current task requests that outcome,
subject to the versioning and changelog rules in `docs/agents/SHARED.md`.
Release preparation may include:

- inspecting existing tags and material changes since the previous tag
- reading the repository and relevant GitHub Issues needed to curate the
  milestone summary
- proposing a version for operator review when the task does not specify one
- finalizing the `Unreleased` entry as the matching versioned and dated release
  entry
- running the required local validation and reviewing the complete release diff

This workflow grants only the read-only discovery and working-tree edits needed
to prepare the release. It does not implicitly authorize staging, committing,
creating or pushing a tag, creating a GitHub Release, or any other publication.
Each additional outcome remains subject to the end-state authorization rules in
`docs/agents/SHARED.md`.

The release entry must be finalized in the working tree before Codex stages any
release changes. After operator review and any required separate authorization,
the release sequence is:

1. Stage the finalized release changes.
2. Commit the release changes, including the versioned changelog entry.
3. Verify the resulting commit and clean index and working tree.
4. Create the matching tag at that exact commit.
5. Push the commit or tag and create a GitHub Release only when those outcomes
   are also authorized.

A release is not complete merely because its changelog entry has been drafted,
finalized, or locally validated.

## 12) Verification and completion

Before completing a Maintainer task, Codex must verify the repository changes
in proportion to their risk. Verification may include document review,
formatting, static validation, tests, and inspection of the final working-tree
changes.

A Maintainer task is complete when:

- the requested repository outcome is present
- relevant local verification has passed
- assumptions, limitations, and intentionally deferred decisions are reported
- any action requiring operator review, additional authorization, or another
  mode is identified

Local verification establishes facts about repository source only. It does not
establish current AWS state or successful deployment.
