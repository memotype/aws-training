<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# AWS DevOps Training Range

This repository is a hands-on AWS DevOps training and engineering-demonstration
project oriented toward the AWS Certified DevOps Engineer - Professional
(DOP-C02) exam. It also demonstrates how coding agents can support real
engineering work under explicit boundaries for authority, evidence, safety,
and reproducibility. The range is designed for building infrastructure,
practicing operational workflows, examining evidence, and eventually running
controlled failure-and-recovery exercises in a real, non-production AWS
account.

The AWS account used with this project is treated as a training range, not a
disposable sandbox. Work is governed by explicit operating modes so that
repository maintenance, evaluation, and AWS operations remain separate and
deliberate.

## Current Status

The project is in its initial infrastructure implementation phase.
Practical labs and
Drillmaster mode are **not implemented yet**. Repository source includes the
first shared infrastructure component, but no AWS deployment is established.

Maintainer and Examiner modes, operator-local configuration, local validation,
licensing checks, project-scoped AWS knowledge access, and native
CloudFormation source for a persistent Lambda artifact store are in place. The
`v0.2.0` milestone establishes the current human-facing governed training
framework. See the [changelog](CHANGELOG.md) for the milestone history and
current unreleased work.

Repository source and plans describe intended behavior only. They do not prove
that any AWS infrastructure is deployed or establish the current state of an
AWS account.

## How It Works

The human operator owns the repository, AWS account, credentials, and final
decisions. Codex works within an explicitly selected mode and a separately
provided task:

1. Open the repository with Codex CLI or a supported IDE integration.
2. Copy and submit the complete `SESSION.md` prompt for the desired mode.
3. Wait for Codex to read the governing documents, acknowledge the mode, and
   report the required orientation state.
4. For Maintainer work, choose a specific existing Issue to continue or start a
   new unit, then provide the scoped task. Submit an examination task directly
   after Examiner initialization.
5. Separately authorize later checkpoint, publication, merge, completion, or
   cleanup outcomes as applicable, and review the resulting changes and
   evidence.

The session prompts are deliberate, read-only entry points. Starting a session
does not itself select or create a work unit or authorize AWS changes, Git
mutations, repository edits, or GitHub mutations.

## Agent Modes

| Mode | Status | Purpose and entry point | AWS boundary |
| --- | --- | --- | --- |
| Maintainer | Implemented | Maintain repository assets and advise the trainee/operator. Start with the [Maintainer session prompt](docs/agents/maintainer/SESSION.md). | Normally no AWS access; never AWS mutation. |
| Examiner | Implemented | Observe and evaluate trainee work against exercise requirements. Start with the [Examiner session prompt](docs/agents/examiner/SESSION.md). | Strictly observational and only when the task authorizes inspection. |
| Drillmaster | Planned | Conduct controlled failure-and-recovery exercises without prematurely revealing the fault. | Not available until its governance is implemented. |

Routine AWS provisioning, deployment, operation, troubleshooting, repair,
exercise work, and cleanup are trainee/operator-owned because performing that
work is part of the training. Those human responsibilities do not require a
separate Codex AWS-operating mode.

The root [standing orders](CODEX.md), [shared governance](docs/agents/SHARED.md),
and selected mode governance define the authoritative boundaries. Modes are
never combined or switched implicitly.

## Getting Started

Clone the repository and restore its Markdown tooling:

```sh
git clone https://github.com/memotype/aws-training.git
cd aws-training
npm ci
```

For account-specific work, initialize the non-secret local configuration:

```sh
cp .aws-training.example.toml .aws-training.local.toml
```

You can use [Codex CLI](https://developers.openai.com/codex/cli) from the
repository root, or use the
[Codex IDE integration](https://developers.openai.com/codex/ide) available for
VS Code and compatible editors. The official documentation also describes
integrations provided through Xcode and JetBrains IDEs.

Before beginning governed work:

- Choose Maintainer or Examiner mode and submit its session prompt.
- Use an authenticated GitHub CLI (`gh`) for Maintainer initialization, which
  verifies the repository and reads the live Maintainer issue queue.
- Install uv 0.12.2 with Python 3.10 or newer. The repository uses uv for
  pinned licensing and CloudFormation validation and `uvx` to launch its
  project-scoped AWS knowledge integration.
- Use Python 3.11 or newer for the standard-library operator-configuration
  reader and its tests.
- Configure AWS credentials only when an exercise and active mode explicitly
  require authorized AWS access. Credentials are not a routine repository
  prerequisite.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `CODEX.md` | Root authority, training purpose, and AWS safety boundaries. |
| `docs/agents/` | Shared and mode-specific governance and session prompts. |
| `.aws-training.example.toml` | Safe tracked template for per-clone operator parameters. |
| `docs/standards/` | Canonical repository configuration and operational standards. |
| `infra/artifact-store/` | Native CloudFormation source for the shared Lambda artifact bucket. |
| `.codex/config.toml` | Project-scoped AWS knowledge integration for Codex. |
| `tools/aws_training_config.py` | Shared offline TOML reader and validator. |
| `tools/cloudformation/` | Pinned CloudFormation linting environment. |
| `tools/reuse/` | Pinned REUSE licensing-validation environment. |
| `package.json` | Markdown validation dependencies. |
| `CHANGELOG.md` | Curated changes for tagged and upcoming milestones. |
| `LICENSE.md` and `LICENSES/` | Licensing policy and canonical license texts. |

Governance reserves `infra/` for shared training-range infrastructure, `labs/`
for trainee exercises, and `docs/architecture/` for architecture material. The
artifact-store template is the first tracked shared-infrastructure source;
`labs/` and `docs/architecture/` do not yet contain tracked implementations.
The `docs/standards/` directory contains the operator-configuration contract.

## Local Configuration and Runtime State

The tracked `.aws-training.example.toml` documents safe placeholders. Its
gitignored copy, `.aws-training.local.toml`, is a schema-versioned interface for
non-secret account IDs, Regions, AWS CLI profile names, resource conventions,
and an explicit bounded cost policy for one clone. It must never contain
credentials.

AWS profiles remain managed through standard mechanisms outside the repository,
regardless of whether they use AWS login, STS, role assumption,
`credential_process`, or another provider. Configuration supplies parameters,
not permission to use them.

Runtime and audit state resolves outside the repository under
`${XDG_STATE_HOME:-~/.local/state}/aws-training/` by default. The planned
append-only `operations.jsonl` lets future mutation-capable Codex workflows
record their authorized out-of-band changes and restoration verification
without replacing infrastructure-as-code state or human audit history.

See the
[operator-configuration standard](docs/standards/OPERATOR_CONFIGURATION.md)
for the field contract, offline validator, state override, account and Region
safety assertions, and versioned ledger event model.

## Tooling and AWS Knowledge

Run the repository-wide Markdown check from the repository root:

```sh
npx markdownlint-cli2
```

Run the pinned REUSE licensing check with uv:

```sh
uv run --project tools/reuse --locked --isolated reuse --root . lint
```

Run the pinned CloudFormation check against the artifact-store template:

```sh
uv run --project tools/cloudformation --locked --isolated \
  cfn-lint infra/artifact-store/template.yaml
```

Validate the tracked example without creating local configuration or runtime
state:

```sh
python3 tools/aws_training_config.py \
  --config .aws-training.example.toml
```

The project-scoped [Codex configuration](.codex/config.toml) provides AWS
documentation search, AWS-authored skills, Region discovery, and service
availability information. It does not expose authenticated AWS API execution
tools. Knowledge access is not evidence of deployed AWS state and does not
grant authority to inspect or modify an account.

## Safety and Governance

Read [CODEX.md](CODEX.md) before relying on or changing this repository. Its
authority is followed by [shared governance](docs/agents/SHARED.md), the active
mode document, and then any applicable exercise or drill specification.

The central boundaries are:

- AWS actions have real security, availability, persistence, and cost effects.
- Possession of credentials is not authorization to use them.
- Infrastructure-as-code describes intended state, not necessarily deployed
  state.
- Maintainer mode never deploys or mutates AWS.
- Examiner mode never repairs or mutates AWS.
- Secrets and credentials must never be committed to the repository.
- Git, GitHub, and AWS changes are distinct authorization domains.

## Licensing

The project uses two licenses according to each file's primary purpose:

- Software, infrastructure configuration, automation, and other
  machine-oriented material use the MIT License.
- Governance, documentation, lab instructions, and other human-oriented
  material use the Creative Commons Attribution 4.0 International License.

See [LICENSE.md](LICENSE.md) for the complete boundary and validation policy.
