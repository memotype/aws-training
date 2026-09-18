<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Practical Labs

Labs are trainee-operated exercises in the real AWS training account. Each lab
defines its own objectives, authorized resource scope, cost and persistence
boundaries, evidence requirements, success criteria, and cleanup checks.

Repository source describes intended infrastructure. It does not prove that a
lab is deployed or authorize Codex to operate AWS. The trainee/operator runs
the AWS commands, while Examiner may evaluate the resulting evidence under its
separately initialized governance and task.

## Available labs

| Lab | Purpose | AWS resources |
| --- | --- | --- |
| [001 - CloudFormation lifecycle](001-cloudformation-lifecycle/README.md) | Practice safe preflight, deployment, observation, update, and verified cleanup. | One temporary standard SQS queue in one CloudFormation stack. |
