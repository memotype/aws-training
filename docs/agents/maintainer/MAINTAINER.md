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
   - If the query succeeds, identify each Issue by number, title, and priority,
     and include counts for each priority and for unprioritized issues in the
     confirmation message.
   - If the query cannot be completed, check
     `https://www.githubstatus.com/` for a reported GitHub Issues outage,
     summarize the reported status, and continue under the degraded-discovery
     procedure below. Do not treat the status page as evidence of the current
     issue queue.
3. Read `docs/agents/maintainer/SCRATCH.md`.
4. Inspect the current branch, `HEAD` attachment, index, and working tree
   without changing them.

The repository check must compare the repository returned by GitHub with the
configured checkout remote and the available operator context before returned
issue state is treated as authoritative. The narrow discovery authority in
this section covers only the read-only local Git inspection and `gh` repository
and issue queries needed to identify the expected repository, inspect its
Maintainer issue queue, and report checkout state. If the issue query cannot be
completed, it also covers one read-only request to
`https://www.githubstatus.com/`. It does not authorize other remote discovery,
general network activity, working-tree edits, Git mutations, or any GitHub
mutation.

If authentication, network access, or repository resolution prevents the
query, Codex must enter a degraded discovery state and report, before
acknowledging Maintainer mode, that the current durable issue queue could not be
established. Codex may still initialize Maintainer mode, but it must not claim
knowledge of the current queue or substitute `SCRATCH.md`, remembered issue
state, or a prior query for current GitHub state.

Codex must either inspect the current queue successfully or disclose the
degraded discovery state, and it must read `SCRATCH.md`, before acknowledging
that Maintainer mode is active. The initialization report must identify the
expected repository and canonical default branch, summarize the current branch,
index, and working-tree state, and include the required issue counts or degraded
discovery disclosure. Successfully returned issue state and `SCRATCH.md`
provide working context but do not select a mode, grant authority, or override
governance. If either conflicts with a governing document, the governing
document controls.

Initialization is an orientation boundary, not the beginning of a maintenance
unit. After reporting, Codex must stop and ask whether the operator wants to
continue a specific existing Maintainer Issue or start a new unit of work. It
must not select, create, label, edit, or comment on an Issue; create or switch a
branch; or edit repository content during initialization. A fresh session does
not imply a fresh Issue, branch, or task.

Before non-trivial repository work, Codex must also inspect the specifications,
files, and local repository state relevant to the requested outcome.

AWS inspection is not part of routine Maintainer discovery.

## 5) Maintainer working state

Maintainer uses GitHub Issues and `SCRATCH.md` for different kinds of
cross-session state. Both are subordinate to `CODEX.md`,
`docs/agents/SHARED.md`, this document, and the current task.

### 5.1) Durable work units and issue handoff

GitHub Issues in the expected repository carrying the `maintainer` label are
the authoritative durable register of discrete repository-maintenance defects,
risks, ambiguities, design decisions, and deferred work. GitHub's issue number
is the canonical identifier, open or closed state represents lifecycle, and
comments and issue history record discussion and progress.

A substantive Maintainer task is one durable unit of work represented by one
open Maintainer Issue and one dedicated Issue work branch. Maintainer sessions
are ephemeral execution contexts for that unit: a unit may span many sessions,
and starting a fresh session neither replaces the Issue nor creates another
one. Before new substantive implementation begins, the operator must choose an
existing Issue to continue or identify the requested outcome as a new unit so
the governed setup in section 6.1 can create its Issue.

Substantive work includes new project capabilities, governance changes,
tooling or dependency changes, infrastructure or lab changes, durable design
decisions, and coherent multi-file changes that warrant their own review and
history. Materiality follows engineering judgment, not line count. A tiny diff
may be substantive, while a truly incidental correction need not become a
durable unit merely for ceremony.

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

Issue comments may provide concise durable handoff state for a work unit when
the current task authorizes that mutation. Appropriate comment content includes
material decisions, findings, blockers, validation state, completed milestones,
remaining work, and relevant branch or commit identity. Comments must not
become command transcripts, reasoning diaries, session logs, or duplicates of
governance, Git or pull-request history, `CHANGELOG.md`, or repository-wide
evergreen context in `SCRATCH.md`. Stale conclusions should be corrected in a
later concise comment rather than silently treated as current.

Discovering or working on an Issue does not by itself authorize commenting,
branching, staging, committing, pushing, opening a pull request, or any
unrelated Issue mutation. Those remain separate outcomes except where the
operator invokes the bounded setup or publication workflows in section 6.

Maintainer must apply the GitHub Issue resolution and closure lifecycle in
section 5.2 of `docs/agents/SHARED.md`. When repository work is fully
implemented and validated but not yet published, Maintainer must leave the
issue open, report it as **ready to close after publication**, and identify the
separately authorized Git and GitHub outcomes still required. This handoff does
not create a label or custom issue state.

### 5.2) Maintainer working memory

`docs/agents/maintainer/SCRATCH.md` is Maintainer's freeform, repository-wide
working-memory and handoff file. It describes evergreen repository-development
context for a future Maintainer session. It may record:

- current repository-development state relevant to planned work
- decisions and completed work that affect future maintenance
- open questions, dependencies, constraints, and intended next work
- references to GitHub Issues by their canonical `#NN` identifiers

`SCRATCH.md` must use present-tense, evergreen framing. It must describe the
state of work as it now stands rather than accumulate a chronological diary of
session activity. When facts, decisions, or plans change, stale statements
should be revised or removed instead of being preserved merely as history.

`SCRATCH.md` must not duplicate the issue queue, replace Issue-specific handoff
comments, or be treated as evidence of current GitHub state. Maintainer should
update it when the current task permits the edit and its work materially changes
repository-wide plans or context needed across work units. It should not
duplicate canonical policy except for concise context needed to understand
current work, and it may not be used as evidence of deployed AWS state.

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

### 6.1) Issue-backed working-tree workflow

Substantive Maintainer work must be established on its dedicated Issue work
branch before new implementation begins. Normal substantive work must not be
performed or committed directly on the canonical default branch. The branch is
durable for the Issue rather than for one session and must be resumed across
sessions instead of replaced with a session-specific branch.

After initialization, an operator instruction to start a specified new
substantive Maintainer unit invokes this bounded setup workflow, including the
read-only repository and Issue discovery and relevant remote-ref refresh needed
for its safety checks. For new work, it authorizes creating exactly one
meaningful GitHub Issue, applying the appropriate existing `maintainer` and
priority labels, and creating and switching to exactly one dedicated Issue
branch. An instruction to continue a specified existing Issue authorizes the
branch creation or switch directly necessary to establish or resume that
Issue's one work branch. These setup operations require no command-by-command
approval, but they do not authorize editing or commenting on an existing Issue,
creating labels, working-tree changes beyond the requested task, staging,
committing, pushing, opening or changing a pull request, merging, Issue closure,
or branch cleanup.

The setup sequence is:

1. Resolve and verify the expected GitHub repository, configured matching
   remote, current canonical default branch, and exact current canonical
   upstream default-branch tip.
2. For existing work, verify the open `maintainer` Issue, read its body and
   relevant durable handoff comments, and confirm that the task continues its
   scope. For new work, create the Issue and apply appropriate existing labels
   before implementation.
3. Derive the branch name as `issue-<number>-<concise-slug>`, using the Issue
   number and a short stable description. One Issue uses one work branch.
4. Inspect `HEAD`, the current branch, index, working tree, local and applicable
   remote Issue-branch refs, and the relationship between the intended base and
   current canonical branch.
5. For new work, create the Issue branch at the exact verified current
   canonical upstream default-branch tip. For existing work, resume its verified
   Issue branch. Then verify the expected branch, base relationship, index, and
   working tree before implementation begins or resumes.

For new work, the Issue branch's starting commit identity must equal the exact
verified current canonical upstream default-branch tip. Maintainer may safely
fast-forward the local default branch first or branch directly from the
verified remote default ref; the resulting commit identity controls, not the
particular command. If that exact base cannot be established safely, stop
rather than begin from stale canonical state. The canonical checkout must also
contain no unrelated or already in-flight work that could be absorbed into the
new Issue branch.

For existing work, Maintainer must preserve all in-scope state and must not
silently absorb unrelated operator changes. If the Issue branch exists locally
or remotely, Maintainer must verify and resume it rather than create a competing
branch. If local and remote Issue-branch state diverges, the canonical base
changed unexpectedly, or reconciliation would require a pull, merge, rebase,
reset, stash, force operation, destructive restoration, or history rewrite,
stop and report the discrepancy.

An in-flight substantive change found on the canonical default branch is a
workflow violation, not permission to move it automatically. Maintainer must
stop unless the operator explicitly authorizes a bounded recovery onto the
Issue branch. Such recovery must inventory and fingerprint the working tree and
index before the transition, preserve them without stashing or rewriting, and
verify the same state afterward before work continues.

A truly incidental, non-substantive correction may omit an Issue only when the
operator selects an explicitly lighter workflow. That exception must not be
used to avoid the Issue lifecycle for a small but substantive change, does not
authorize a normal checkpoint through `COMMIT.md`, and does not imply direct
publication to the canonical branch.

### 6.2) Checkpoint commits

A checkpoint commit is a separately authorized outcome. Before staging,
Maintainer must verify that the specified open Maintainer Issue, current work
branch, and intended cumulative changes belong to the same work unit. `HEAD`
must be attached to the exact dedicated Issue branch, and that branch must not
be the canonical default branch. Failure of this invariant stops the commit;
commit authorization does not normally create, choose, or switch branches.

The operational `COMMIT.md` prompt invokes this governed checkpoint procedure.
It may require tending current handoff and changelog content, reviewing the
complete cumulative diff, and running required validation before staging only
in-scope changes. It does not authorize Issue comments, publication, or any
later lifecycle outcome.

### 6.3) Pull-request publication

Publication and pull-request creation are separately authorized from Issue
setup, working-tree implementation, and checkpoint commits. When the operator
explicitly authorizes the scoped Maintainer pull-request workflow, section 5.1
of `docs/agents/SHARED.md` governs the directly implied Git and GitHub
operations. The pull request must use the Issue branch as its head and the
canonical default branch as its base.

A Maintainer-created pull request should concisely state the resulting change,
relevant validation, important limitations or deferred work, and the associated
Issue using neutral linkage that does not arrange automatic closure. Once
implementation and validation are complete, it should normally be opened ready
for review. Draft pull requests are reserved for intentionally incomplete work
or explicit operator direction. Maintainer must verify the pull request's base,
head, state, and expected commit relationship, then stop for operator review
unless a later outcome is separately authorized. Agent self-approval,
self-merge, Issue closure, and branch cleanup are not part of publication.

### 6.4) Completion and post-merge cleanup

Merge, Issue closure, and post-merge branch cleanup are separate outcomes.
Issue closure follows section 5.2 of `docs/agents/SHARED.md` and requires
immediate verification that the resolving state is present on the canonical
branch. Branch cleanup must not begin until GitHub reports the pull request as
merged, the related Issue is closed as completed, and the resolving state is
present on the current canonical default branch.

The operational `POST_MERGE.md` prompt may explicitly authorize the distinct
Issue-completion and branch-cleanup outcomes together as one ordered workflow
for one exact repository, pull request, Issue, and Issue branch. This bounded
authorization does not make either outcome implicit in merge or authorize any
other Issue or ref mutation. The procedure supports only the repository's
merge-commit workflow; squash- or rebase-merged work requires a different
explicitly governed procedure.

The workflow must be safely resumable. At each stage, Maintainer must inspect
authoritative local and GitHub state and either perform the expected outcome or
verify that it is already satisfied. An Issue already closed as completed, or
a named local or remote Issue branch already absent at the beginning of the
workflow, is a satisfied outcome when all remaining identity, publication, and
safety evidence is consistent. Maintainer must not reopen an Issue or recreate
a branch merely to replay an outcome. An Issue closed for another reason, a ref
or Issue state that changes unexpectedly after it is observed, or any other
contradictory state stops the workflow.

The workflow must resolve the expected repository, unique matching remote, and
canonical default branch; require a clean index and working tree; verify
through GitHub that the named pull request was merge-committed into that branch
and that the resolving state is present there; and verify that the named Issue
is the related Maintainer work unit. The checkout must begin attached either to
the exact named Issue branch or to the canonical default branch. Starting on
the default branch permits resumption after an earlier invocation switched to
it, whether or not the local Issue branch deletion was already completed. A
detached `HEAD` or any other starting branch stops the workflow.

If the Issue lacks an adequate completion update, Maintainer may add one
concise comment recording the pull request, merge commit, and verified
canonical publication without duplicating existing handoff state. Immediately
before closing an open Issue, Maintainer must repeat the canonical-publication
verification, close that exact Issue as completed, and verify its resulting
state. If the Issue is already closed as completed, Maintainer must verify that
state and may add a missing completion update without reopening it. No branch
cleanup may proceed until Issue completion is verified.

Before any branch deletion, Maintainer must refresh the relevant refs, record
which named local and remote Issue refs exist and their exact tips, and prove
that every existing tip is an ancestor of the canonical remote default branch.
A ref already absent at this initial observation must be recorded as such and
must not be recreated. After switching to the default branch when necessary
and updating it by fast-forward only, Maintainer must repeat every applicable
ancestry proof while the Issue refs still exist. Git's normal safe local
deletion is an additional check, not a substitute for explicit canonical
containment evidence.

Only after every applicable check succeeds may Maintainer safely delete the
local Issue branch if it exists and delete the exact remote Issue branch if it
exists and its tip is unchanged. A ref that is already absent satisfies its
deletion outcome. Maintainer must then verify that the Issue remains closed as
completed, the default branch is synchronized, the checkout is clean, and both
Issue refs are absent. Any unexpected state, unpublished work, changed ref,
failed ancestry proof, or need for merge, rebase, reset, stash, force, broad
pruning, or destructive restoration stops the workflow without further
mutation or reconciliation.

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
