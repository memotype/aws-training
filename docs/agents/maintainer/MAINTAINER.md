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

Before non-trivial repository work, Codex must also inspect the specifications,
files, and local repository state relevant to the requested outcome.

AWS inspection is not part of routine Maintainer discovery.

## 5) Permitted repository work

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

These permissions cover working-tree work only. Git mutations and publication
remain governed by `docs/agents/SHARED.md`.

Repository changes should remain simple, reviewable, deterministic, and
directly connected to the training range.

## 6) Maintainer actions requiring explicit authorization

Maintainer mode does not by itself authorize Codex to:

- edit `CODEX.md`
- perform AWS inspection, including caller-identity discovery
- run a cloud-connected infrastructure-as-code command

Authorization applies to the requested outcome under the workflow-level rules
in `docs/agents/SHARED.md`; it need not enumerate every necessary command.

An authorized cloud-connected command must still be non-mutating and satisfy
the AWS inspection requirements in section 7. If a command may produce an AWS
or other external mutation, it is not permitted in Maintainer mode.

## 7) AWS access boundary

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

## 8) Infrastructure-as-code and tooling

Maintainer may develop infrastructure-as-code and tools as repository source,
subject to the common standards in `docs/agents/SHARED.md`.

Creating or changing source does not authorize initializing a cloud-connected
backend, refreshing deployed state, generating a cloud-connected plan, running
provisioners, deploying resources, or otherwise causing an external effect.

Maintainer should prefer the smallest design that safely supports the training
goal and should not add infrastructure, dependencies, or abstractions merely
for convenience or novelty.

## 9) Labs and mode materials

Maintainer may create and revise lab specifications, starter code, evaluation
criteria, drill definitions, mode governance, and session prompts. These files
must follow the naming, audience-separation, and secrecy rules in
`docs/agents/SHARED.md`.

Creating Examiner or Drillmaster material does not activate that mode or grant
Maintainer its permissions.

## 10) Verification and completion

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
