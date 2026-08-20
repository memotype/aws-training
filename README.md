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

The project is in its governance and structure phase. Practical labs, shared
AWS infrastructure, and Drillmaster mode are **not implemented yet**.

Maintainer and Examiner modes, local documentation checks, licensing
validation, and project-scoped AWS knowledge access are in place. The `v0.2.0`
milestone establishes the current human-facing governed training framework.
See the [changelog](CHANGELOG.md) for the milestone history.

Repository source and plans describe intended behavior only. They do not prove
that any AWS infrastructure is deployed or establish the current state of an
AWS account.

## How It Works

The human operator owns the repository, AWS account, credentials, and final
decisions. Codex works within an explicitly selected mode and a separately
provided task:

1. Open the repository with Codex CLI or a supported IDE integration.
2. Copy and submit the complete `SESSION.md` prompt for the desired mode.
3. Wait for Codex to read the governing documents and acknowledge the mode.
4. Submit the repository-maintenance or examination task separately.
5. Review the resulting changes, evidence, and any remaining actions.

The session prompts are deliberate entry points. Starting a session does not
itself authorize AWS changes, Git publication, or GitHub mutations.

## Agent Modes

| Mode | Status | Purpose and entry point | AWS boundary |
| --- | --- | --- | --- |
| Maintainer | Implemented | Maintain governance, documentation, tooling, and infrastructure-as-code source. Start with the [Maintainer session prompt](docs/agents/maintainer/SESSION.md). | Normally no AWS access; never AWS mutation. |
| Examiner | Implemented | Observe and evaluate trainee work against exercise requirements. Start with the [Examiner session prompt](docs/agents/examiner/SESSION.md). | Strictly observational and only when the task authorizes inspection. |
| Drillmaster | Planned | Conduct controlled failure-and-recovery exercises without prematurely revealing the fault. | Not available until its governance is implemented. |

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
  pinned licensing validation and `uvx` to launch its project-scoped AWS
  knowledge integration.
- Configure AWS credentials only when an exercise and active mode explicitly
  require authorized AWS access. Credentials are not a routine repository
  prerequisite.

## Repository Structure

| Path | Purpose |
| --- | --- |
| `CODEX.md` | Root authority, training purpose, and AWS safety boundaries. |
| `docs/agents/` | Shared and mode-specific governance and session prompts. |
| `.codex/config.toml` | Project-scoped AWS knowledge integration for Codex. |
| `tools/reuse/` | Pinned REUSE licensing-validation environment. |
| `package.json` | Markdown validation dependencies. |
| `CHANGELOG.md` | Curated changes for tagged and upcoming milestones. |
| `LICENSE.md` and `LICENSES/` | Licensing policy and canonical license texts. |

Governance reserves `infra/` for shared training-range infrastructure, `labs/`
for trainee exercises, and `docs/architecture/` and `docs/standards/` for
supporting design material. These areas do not yet contain tracked
implementations.

## Tooling and AWS Knowledge

Run the repository-wide Markdown check from the repository root:

```sh
npx markdownlint-cli2
```

Run the pinned REUSE licensing check with uv:

```sh
uv run --project tools/reuse --locked --isolated reuse --root . lint
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
