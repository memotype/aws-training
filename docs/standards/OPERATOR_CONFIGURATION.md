<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Operator-Local Configuration and Runtime State

## Purpose and boundaries

Each clone may use non-secret, account-specific parameters without making the
public repository specific to one operator. The tracked
`.aws-training.example.toml` defines the supported TOML shape. The normal local
file is `.aws-training.local.toml`, which Git ignores.

Initialize it from the repository root:

```sh
cp .aws-training.example.toml .aws-training.local.toml
```

The local file supplies parameters, never authority. A configured profile,
identity, account, Region, resource name, tag, or state path does not authorize
Codex or a tool to use it. Active governance and the current task still control
every operation.

AWS credentials do not belong in either TOML file. Named AWS CLI profiles are
the repository's authentication abstraction; standard external mechanisms such
as AWS login, role assumption, STS credentials, `credential_process`, and
other AWS credential providers remain responsible for credential material.
Repository tooling must not read AWS credential files directly.

## TOML contract

The local TOML file is a small public configuration interface. Its required
top-level `schema_version` lets readers detect a future incompatible contract
instead of ambiguously interpreting fields under the wrong rules. The current
reader accepts exactly integer version `1`; it provides no migrations,
compatibility layers, or schema framework.

The reader rejects unsupported fields so misspellings fail visibly. Strings
described as non-empty are trimmed during normalization.

| Field | Requirement | Meaning |
| --- | --- | --- |
| `schema_version` | Required integer `1` | Version of this TOML configuration contract. |
| `aws.expected_account_id` | Required 12-digit string | Safety assertion for the account reported by STS `GetCallerIdentity`. |
| `aws.account_label` | Optional non-empty string | Human-readable label with no identity or authorization effect. |
| `aws.primary_region` | Required non-empty string | Expected Region for future preflight checks. |
| `aws.profiles.operator` | Required non-empty string | AWS CLI profile for separately authorized human-operator workflows. |
| `aws.profiles.maintainer_recovery` | Optional non-empty string | Dedicated profile required for explicitly invoked Maintainer recovery. |
| `aws.profiles.examiner` | Optional non-empty string | Future read-only Examiner profile. |
| `aws.profiles.drillmaster` | Optional non-empty string | Future Drillmaster profile. |
| `resources.prefix` | Required non-empty string | Prefix for training-range resources. |
| `resources.tags` | Required non-empty string table | Standard tags future tooling applies within its authority. |
| `cost.require_free_plan` | Required boolean | Whether this range must remain on the AWS Free plan. |
| `cost.max_out_of_pocket_usd` | Required finite non-negative number | Explicit out-of-pocket cost ceiling. |
| `state.directory` | Optional non-empty path string | Override for external runtime state. |

The Maintainer recovery profile remains optional for ordinary repository use,
but an invoked recovery workflow requires it. Maintainer must use that exact
profile for recovery diagnosis and mutation and must never fall back to the
human operator profile, another configured profile, or ambient credentials. An
absent, unusable, mismatched, or insufficiently authorized recovery profile
stops the workflow. The recovery identity should ultimately be scoped to the
training range and plausible recovery operations rather than broad
administration.

Examiner and Drillmaster profile names remain optional until those identities
and workflows are provisioned. The configuration does not prescribe whether a
profile ultimately represents a user, role, federated session, or another
standard AWS credential-provider chain.

Every configured range has an explicit cost policy, and no workflow may assume
unrestricted spending. When `cost.require_free_plan` is `true`,
`cost.max_out_of_pocket_usd` must be zero. When it is `false`, the ceiling may
be any finite number greater than or equal to zero. A ceiling constrains an
already-authorized workflow; it is never spending authority.

The tracked example retains the safest Free-plan and zero-out-of-pocket
posture. Free Tier credits remain a finite training budget rather than
permission for arbitrary consumption. Balances, expiration dates, and other
current plan facts must be obtained from AWS only during a separately
authorized runtime observation and must not be hard-coded into configuration.

## Shared reader and validation

`tools/aws_training_config.py` is the shared reader for future repository
tooling. It uses Python 3.11's standard-library `tomllib`, performs no credential
loading, and makes no network or AWS calls. Other Python tools can import
`load_config()` and consume the returned immutable data classes.

By default, the reader finds the Git working-tree root and requires
`.aws-training.local.toml`. `AWS_TRAINING_CONFIG` may name another file; a
relative value is resolved from the repository root. Callers may also pass an
explicit path to `load_config()` or the command-line validator:

```sh
python3 tools/aws_training_config.py \
  --config .aws-training.example.toml
```

Successful command-line validation prints normalized, non-secret JSON. A
missing local file reports the copy command needed to initialize it. Validation
checks schema version, required fields, types, account-ID format, cost-policy
invariants, non-empty Region and profile names, and the runtime-state boundary.
An unsupported schema version produces a distinct error from malformed TOML or
ordinary field validation. Offline validation does not establish the current
AWS identity, account, Region, Free-plan status, credit balance, deployed
resources, or authorization.

## Future authorized AWS preflight

Active governance and the current task must authorize an AWS workflow before
any AWS query occurs. Required preflight observations may be the first queries
of that already-authorized workflow; they do not depend on a caller-identity
check having happened earlier.

The general intended sequence is:

```text
load local configuration
        |
select configured profile
        |
authorized preflight begins
        |
STS GetCallerIdentity
        |
expected account matches?
        |
resolve/select expected Region
        |
other required account/plan/scope checks
        |
authorized AWS work may proceed
```

STS `GetCallerIdentity` verifies the active AWS principal and account for the
selected profile; it does not verify an ambient "caller" independently of that
credential selection. Maintainer recovery must select only
`aws.profiles.maintainer_recovery`. Failure to load or use it, an account or
principal mismatch, or insufficient permission for a necessary recovery
operation stops recovery rather than triggering profile substitution or
privilege escalation.

Preflight determines whether subsequent operations already within that
workflow's authority may proceed. Failure, inability to verify, or mismatch
must stop the workflow rather than expand its scope or trigger remediation.
Success verifies safety conditions; it does not grant new or broader authority.

Region handling is deliberate selection, not a caller-identity-style query for
an ambient effective Region. `aws.primary_region` is the normal expected
Region. Regional AWS calls must explicitly use that Region or another Region
explicitly permitted by the active exercise instead of silently trusting a
profile or environment default. An unexpected or unpermitted Region stops the
workflow.

No live preflight call is implemented by the offline configuration reader.

## External runtime state

Runtime and audit files live outside the Git working tree. The default state
directory is:

```text
${XDG_STATE_HOME:-~/.local/state}/aws-training/
```

`XDG_STATE_HOME`, when set, must resolve to an absolute path. The optional
`state.directory` value takes precedence; `~` is expanded, and a relative
override is resolved from the configuration file's directory. The reader
rejects every state directory that resolves to the repository root or beneath
it. Resolving a path does not create the directory.

Runtime state is local operational evidence. It must not be committed, treated
as authority, or treated as proof of current AWS state after its observation
context has become stale.

## Operations and cleanup ledger

Authorized mutation-capable Codex workflows use `operations.jsonl` beneath the
resolved state directory to automatically record mutations they perform under
an authorized active mode and task. Maintainer recovery is an authorized
producer when it performs AWS mutations. The ledger is append-only and uses
contract version `1`. Each line is one complete UTF-8 JSON object. Writers must
durably append new events without rewriting, removing, or reordering earlier
lines.

The ledger records operational intent, out-of-band mutations, and restoration
obligations for agent-generated training mutations. It supplements CloudTrail
and infrastructure-as-code state; it is not a complete audit history of every
human or system action and is not a generic rollback or workflow engine.
CloudFormation or another selected infrastructure-as-code system remains
responsible for the lifecycle and rollback of resources it owns.

Ordinary human/operator AWS work does not need manual ledger entries. The
operator must not be expected to hand-edit or append JSONL records for that
activity. Ledger-writing automation remains the responsibility of each
authorized mutation-capable Codex workflow.

Version 1 defines exactly two event types:

- `operation` records one mutation against one resource. It contains
  `schema_version`, `event_type`, a unique `event_id`, UTC RFC 3339
  `occurred_at`, initiating `mode`, `action`, `reason`, `aws`, `resource`,
  `pre_change`, and `restoration`.
- `restoration_verified` records later verification. It contains
  `schema_version`, `event_type`, a unique `event_id`, UTC RFC 3339
  `verified_at`, verifying `mode`, `operation_event_id`, `aws`, and
  `verification`. `operation_event_id` must reference the original operation;
  the original line remains unchanged.

The `mode` value is the lowercase canonical name of the active governed mode.
It must identify the mode that actually performed the authorized mutation.
Recording a mode never grants that mode mutation authority; an operation event
may be written only for a Codex mutation already authorized under the active
governance and task.

The `aws` object contains non-empty `profile`, observed `principal_arn`,
12-digit `account_id`, and `region` strings. The `resource` object contains a
non-empty `type` and stable `identifier`. `pre_change` and `verification` each
contain a concise `summary` and may contain an `evidence_ref` pointing to
separately retained, non-secret evidence. `restoration` contains boolean
`required` and a non-empty `obligation` when restoration is required.

One operation event should target one resource so cleanup obligations remain
unambiguous. A mutation affecting several resources should append one operation
event per resource, linked by a shared value in the human-readable reason when
useful. Absence of a matching `restoration_verified` event means a required
restoration remains unverified; it does not prove that restoration failed.

Example operation and subsequent verification events are shown as separate
JSONL lines:

```json
{"schema_version":1,"event_type":"operation","event_id":"6ed7676f-50f4-4729-ad13-136209aba02d","occurred_at":"2026-08-21T14:30:00Z","mode":"drillmaster","action":"ec2:StopInstances","reason":"authorized instance-recovery drill","aws":{"profile":"aws-training-drillmaster","principal_arn":"arn:aws:sts::123456789012:assumed-role/aws-training-drillmaster/example-session","account_id":"123456789012","region":"us-east-1"},"resource":{"type":"ec2:instance","identifier":"i-0123456789abcdef0"},"pre_change":{"summary":"instance state was running","evidence_ref":"observations/6ed7676f-before.json"},"restoration":{"required":true,"obligation":"verify that the instance returns to running and passes status checks"}}
{"schema_version":1,"event_type":"restoration_verified","event_id":"d8f9da96-5248-4d76-b072-5d8903429260","verified_at":"2026-08-21T14:45:00Z","mode":"drillmaster","operation_event_id":"6ed7676f-50f4-4729-ad13-136209aba02d","aws":{"profile":"aws-training-drillmaster","principal_arn":"arn:aws:sts::123456789012:assumed-role/aws-training-drillmaster/example-session","account_id":"123456789012","region":"us-east-1"},"verification":{"summary":"instance returned to running and both status checks passed","evidence_ref":"observations/6ed7676f-restored.json"}}
```

No ledger writer, AWS preflight implementation, or recovery IAM identity exists
yet. Maintainer recovery governance requires a compatible validated writer
before mutation and therefore stops before mutation while that dependency is
absent. This contract authorizes neither tooling implementation nor AWS use by
itself; those outcomes still require the active governance and current task.
