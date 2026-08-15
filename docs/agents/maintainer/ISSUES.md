# ISSUES

This is a Maintainer working register for unresolved repository-governance
findings. It records problems and possible resolutions, but it does not select
an operating mode, grant authority, or override `CODEX.md`,
`docs/agents/SHARED.md`, or a mode governance document.

## M-001 [MEDIUM] Governance changes lack an activation boundary

**Status:** Open

Maintainer may edit `SHARED.md` or its own mode document, but nothing says
whether those edits immediately become authoritative. An agent should never be
able to expand its own permissions and then rely on the new wording during the
same task.

The same ambiguity applies when the operator or another process changes a
governance file during an initialized session: the documents do not define
whether the session continues under the version originally read or immediately
adopts the working-tree version.

**Suggested resolution:** Define a governance activation procedure. A safe
default would treat governance edits as proposals for the current task and
prohibit them from granting new authority until the operator explicitly accepts
the changes and reinitializes or reaffirms the active mode. Also define whether
the authoritative version comes from the working tree, the current commit, or a
session initialization snapshot.

**Progress:** The resolution of M-002 establishes a narrow activation boundary
for any future relaxation of an absolute AWS prohibition. The activation rule
for other governance changes remains undecided.

## M-002 [HIGH] Absolute AWS prohibitions are conditionally worded

**Status:** Resolved

`CODEX.md` introduces its AWS safety list with "Unless specifically authorized
by governing documents and the current task." The list then includes actions
such as exposing root credentials, closing the account, weakening the IAM
controls that constrain Codex, and disabling cost or safety controls. Read
literally, the qualifier makes every item potentially authorizable by a
lower-level governance document and task.

This conflicts with the apparent intent that some account-level actions are
outside the training range under all ordinary modes.

**Suggested resolution:** Split the list into absolute prohibitions that lower
documents and ordinary tasks cannot authorize, and restricted high-risk actions
that require an appropriate mode plus explicit task authority. Define the
exception or governance-amendment process for any absolute rule that the
operator may legitimately need to change.

**Progress:** `CODEX.md` now separates absolute prohibitions from conditionally
authorizable AWS actions. Absolute prohibitions cover root-user and account
closure actions, unrestricted administration, evasion of Codex's IAM boundary,
account-level guardrails, destructive key deletion, indiscriminate destruction,
loss of the only recovery copy, out-of-scope resources, unjustified material
cost, and concealment of unexpected effects. Lower authorities cannot create
exceptions. Any future relaxation requires an explicitly authorized edit to
`CODEX.md`, operator acceptance, and a fresh or reaffirmed governance session;
the edit itself does not authorize the AWS action.

## M-003 [LOW] AWS discovery requirements conflict with Maintainer access limits

**Status:** Open

`CODEX.md` requires inspection of the actual AWS environment when current
deployed state matters and says not to assume AWS state when it can be queried.
`MAINTAINER.md` permits AWS inspection only when the current task explicitly
requires it and the other Maintainer safeguards are satisfied.

The safe interpretation is that the mode and task must authorize inspection
before the root discovery rule applies, but the root wording can also be read as
an independent mandate to query AWS.

**Suggested resolution:** Qualify the root discovery rule: when current state
matters *and* the active mode and task permit inspection, inspect it; otherwise,
report that current deployed state cannot be established. Apply the same
qualification to the instruction not to reconstruct queryable state from
memory.

**Progress:** Maintainer practice currently follows the restrictive
interpretation, but the text has not been reconciled.

## M-004 [MEDIUM] No mode owns ordinary AWS deployment and cleanup

**Status:** Open design decision

Maintainer cannot deploy or mutate AWS. Examiner is principally observational.
Drillmaster mutations are tied to controlled drills and their authorized fault
injection or restoration. No current mode clearly owns routine provisioning of
shared infrastructure, deployment of a trainee lab, ordinary repair, or lab
cleanup.

This is not a defect if all such work is intentionally reserved for the human
operator, but that responsibility is not currently explicit.

**Suggested resolution:** Decide whether Codex will ever perform routine AWS
changes. If not, state that deployment and cleanup are operator-only. If it
will, introduce a narrowly governed operational mode rather than stretching
Drillmaster into a general mutation role.

**Progress:** Operator responsibility versus an additional mode remains
undecided.

## M-005 [MEDIUM] Governance responsibilities are repeated across layers

**Status:** Open

Mode selection, evidence rules, repository permissions, AWS boundaries, and
verification appear in overlapping forms in `CODEX.md`, `SHARED.md`, and
`MAINTAINER.md`. Some repetition is useful defense in depth, but it increases
reading cost and creates drift risk as Examiner and Drillmaster governance are
added.

**Suggested resolution:** Apply a stricter factoring rule:

- `CODEX.md` contains the authority hierarchy, mode definitions, constitutional
  invariants, and hard prohibitions.
- `SHARED.md` contains common operational procedures and safeguards.
- Each mode document contains only that mode's capability grant, restrictions,
  and workflow.
- Each session prompt activates a mode and points to canonical governance.

Retain deliberate repetition only where the safety value is worth the drift
risk.

**Progress:** An initial shared-versus-mode refactor was completed, but the root
versus-shared boundary still needs review.

## M-006 [MEDIUM] Mode switches do not define task and authorization lifetime

**Status:** Open

The documents explain how to switch modes but do not explicitly say what
happens to an unfinished task, pending operation, or authorization granted
under the previous mode. They also do not define whether a new conversation,
context handoff, agent restart, or similar boundary creates a new governance
session.

**Suggested resolution:** Define "session" and state that switching modes
immediately suspends or terminates the prior mode's task authority. Permissions
and approvals from the prior mode should not carry into the new mode unless the
operator expressly restates them under the new mode.

**Progress:** Mode selection and switching are defined; lifecycle semantics are
not.

## M-007 [MEDIUM] Operative governance terms lack decision rules

**Status:** Open

Several subjective terms control permissions or stopping behavior, including
"non-trivial," "materially expand," "substantial repository content,"
"materially different cost," "approved mechanism," "external effect," and
"current task." Their intended meanings are understandable, but different
agents may draw different boundaries.

**Suggested resolution:** Add a small shared definitions section with practical
decision rules and examples. Numerical thresholds are not necessary for every
term, but uncertain cases should have a consistent conservative default and a
clear escalation path.

**Progress:** No common definitions section exists.

## M-008 [MEDIUM] AWS evidence lacks provenance requirements

**Status:** Open

The distinction between observed state, intended state, inference, and prior
notes is strong. However, a live AWS observation only establishes what was seen
at a particular time and within the account, Region, resources, API, and query
scope inspected. The current wording can be read as establishing the entire
current state without those qualifications.

**Suggested resolution:** Require material AWS findings to identify the
observation time, caller/account context, applicable Region, and relevant query
or resource scope. Describe observations as time- and scope-bounded evidence.

**Progress:** Identity, account, Region, and scope checks are required before
operations, but evidence handoffs do not yet require this metadata.

## M-009 [MEDIUM] Non-AWS external and host side effects are under-specified

**Status:** Open

Git mutations, dependency changes, and AWS actions receive detailed treatment,
but other side effects are less explicit. Examples include writing to non-AWS
services, downloading and executing remote scripts, starting containers,
changing host configuration, invoking repository hooks, or running a nominally
local test that contacts an external system.

**Suggested resolution:** Add a shared command-execution rule that classifies
all commands by actual and potential side effects, regardless of tool name or
service. Define the authorization required for outbound reads, external writes,
host mutations, and execution of unreviewed repository scripts.

**Progress:** The AWS section contains the right side-effect principle, but its
general applicability is unclear.

## M-010 [MEDIUM] Concealed drill material lacks a storage and visibility model

**Status:** Open design dependency

`SHARED.md` requires separation between trainee-facing material and concealed
Drillmaster details, while also warning that prompt instructions do not make
information secret. If the trainee can inspect the complete repository and its
history, drill answers stored there are only nominally concealed.

Security secrets and pedagogical spoilers also have different handling needs,
but the current text does not distinguish them.

**Suggested resolution:** Define the trainee's repository visibility model,
distinguish true secrets from exercise spoilers, and select an approved storage
mechanism for each category before Drillmaster material is added.

**Progress:** Deferred until the Drillmaster and repository-access design is
developed.

## M-011 [LOW] Session initialization requires an extra conversational round trip

**Status:** Accepted for review

The Maintainer session prompt requires Codex to acknowledge the mode and await a
separate maintenance task. This is a clear safety handshake, but it prevents an
operator from efficiently supplying initialization and a task together.

`SCRATCH.md` records that this behavior is intentional, so this is a usability
tradeoff rather than an accidental contradiction.

**Suggested resolution:** Keep the hard handshake if operator review between
initialization and work is desired. Otherwise, allow Codex to acknowledge the
mode before beginning a task included in the same message and wait only when no
task accompanies the prompt.

**Progress:** Current behavior is intentionally conservative.

## M-012 [MEDIUM] The temporary handoff note is stale and duplicates policy

**Status:** Resolved

`SCRATCH.md` says the repository has no commits and that its files are
untracked. The repository now has commit `12e6805` on `main`, tracking
`origin/main`, with a clean working tree before this issue register was added.
The note also repeats several canonical governance decisions, which increases
the chance that a low-authority working record will drift from the documents it
summarizes.

**Suggested resolution:** Update or retire stale handoff state. Keep temporary
handoffs focused on unresolved decisions and genuinely temporary context;
prefer deriving repository status from Git rather than recording volatile
snapshots in a committed document. Do not duplicate canonical policy unless the
text is clearly marked as a non-authoritative summary and has continuing value.

**Progress:** The file now lives at `docs/agents/maintainer/SCRATCH.md` and is an
evergreen Maintainer working-state document. Volatile Git snapshots, expired
authorization reminders, and duplicated policy detail have been removed. The
mode document defines its purpose and requires future Maintainer sessions to
read it during initialization.
