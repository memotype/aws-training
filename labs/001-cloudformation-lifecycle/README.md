<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Lab 001: CloudFormation Lifecycle

## Purpose

Practice a complete, observable infrastructure lifecycle in the AWS training
account: establish the execution context, validate infrastructure source,
create a stack, inspect its real state, perform a controlled update, and
verify cleanup.

This is a guided foundational lab. The trainee/operator performs every AWS
operation. Codex in Maintainer mode may discuss repository source but must not
run these commands against AWS. Use Examiner mode and a separate examination
task if you want Codex to evaluate the completed exercise.

## Learning objectives

By completing this lab, you should be able to:

- distinguish local configuration and intended infrastructure from observed
  AWS state
- verify the caller account and select the Region explicitly before mutation
- follow CloudFormation stack events through create, update, and delete
- relate a template parameter update to the resource's physical identity and
  observed attributes
- collect evidence with enough identity, Region, target, and time context to
  support operational claims
- prove that temporary training resources were removed

## Scope and safety contract

This exercise scopes the human trainee/operator to create, inspect, update, and
delete exactly one CloudFormation stack in the configured training account and
primary Region. The stack owns exactly one standard Amazon SQS queue from
[`template.yaml`](template.yaml). The template omits `QueueName`, so
CloudFormation generates the physical name.

Derive the stack name as `<configured-resource-prefix>-lab-001-cfn-lifecycle`.
If a stack with that exact name already exists, stop. Treat it as unexpected
state and determine its ownership before continuing; do not adopt, update, or
delete it as part of a new attempt.

The queue uses SQS-managed server-side encryption, receives no messages during
the lab, and has no retention policy. Deleting the stack should delete the
queue. Do not add resources, send messages, change retention behavior, use a
different account or Region, or run the exercise against a production account.

Amazon SQS has request-based pricing and no minimum fee. The exercise makes a
small number of API requests, but a pricing allowance is not proof that an
individual account will incur no charge. Before deployment, confirm that the
current [Amazon SQS pricing](https://aws.amazon.com/sqs/pricing/) and the
account's current plan or credits comply with the cost policy in
`.aws-training.local.toml`. Stop if that cannot be established.

## Prerequisites

- The repository's root governance has been read and accepted.
- `.aws-training.local.toml` contains the intended non-secret account, Region,
  operator profile, tags, and cost policy.
- The AWS CLI profile uses temporary credentials where practical and has only
  the CloudFormation, SQS, and observation permissions needed for this lab.
- Python 3.11 or newer, AWS CLI v2, uv 0.12.2 or a later 0.12 patch release,
  and the repository's locked CloudFormation validation environment are
  available.
- No stack with the lab's derived name exists in the target account and Region.

Run commands from the repository root. Set these shell variables from the
validated local configuration; do not copy the example values blindly:

```sh
training_profile="your-configured-operator-profile"
training_account="your-expected-12-digit-account-id"
training_region="your-configured-primary-region"
training_prefix="your-configured-resource-prefix"
training_project_tag="your-configured-Project-tag"
training_environment_tag="your-configured-Environment-tag"
training_managed_by_tag="your-configured-ManagedBy-tag"
training_stack="${training_prefix}-lab-001-cfn-lifecycle"
training_template="labs/001-cloudformation-lifecycle/template.yaml"
```

## Phase 1: establish the execution context

Validate the local configuration offline:

```sh
python3 tools/aws_training_config.py \
  --config .aws-training.local.toml
```

Observe the caller identity using the configured operator profile:

```sh
aws sts get-caller-identity \
  --profile "$training_profile" \
  --output json
```

Compare the returned `Account` with `training_account`. Confirm that the ARN is
the intended training identity. A mismatch, expired session, unexpected
identity, or inability to verify the caller stops the exercise. STS identity
does not establish a Region, so use `training_region` explicitly on every
regional command below.

Check for a pre-existing stack:

```sh
aws cloudformation describe-stacks \
  --stack-name "$training_stack" \
  --profile "$training_profile" \
  --region "$training_region"
```

For a new attempt, AWS should report that the stack does not exist. Any
returned stack is unexpected state and stops the exercise.

Record the UTC observation time, profile name, Region, whether the account ID
matched, and a non-sensitive description of the principal. Do not record
credentials, session tokens, or unredacted account-specific output in the
repository.

## Phase 2: inspect and validate intended state

Read `template.yaml` and predict:

- which physical resource CloudFormation will create
- which properties and tags should be observable after creation
- whether changing `VisibilityTimeoutSeconds` should preserve or replace the
  queue
- what should happen to the queue when the stack is deleted

Validate the template without contacting AWS:

```sh
uv run --project tools/cloudformation --locked --isolated \
  cfn-lint "$training_template"
```

A passing local check is evidence about template source only. It does not
establish that the stack exists or that AWS will accept the deployment.

## Phase 3: create and observe the stack

Deploy the initial stack with a 30-second visibility timeout:

```sh
aws cloudformation deploy \
  --template-file "$training_template" \
  --stack-name "$training_stack" \
  --parameter-overrides \
    VisibilityTimeoutSeconds=30 \
    "ProjectTagValue=$training_project_tag" \
    "EnvironmentTagValue=$training_environment_tag" \
    "ManagedByTagValue=$training_managed_by_tag" \
  --tags \
    "Project=$training_project_tag" \
    "Environment=$training_environment_tag" \
    "ManagedBy=$training_managed_by_tag" \
    Lab=001-cloudformation-lifecycle \
  --profile "$training_profile" \
  --region "$training_region"
```

Inspect the stack, recent events, and outputs:

```sh
aws cloudformation describe-stacks \
  --stack-name "$training_stack" \
  --profile "$training_profile" \
  --region "$training_region"

aws cloudformation describe-stack-events \
  --stack-name "$training_stack" \
  --profile "$training_profile" \
  --region "$training_region" \
  --max-items 20

training_queue_url=$(aws cloudformation describe-stacks \
  --stack-name "$training_stack" \
  --profile "$training_profile" \
  --region "$training_region" \
  --query 'Stacks[0].Outputs[?OutputKey==`QueueUrl`].OutputValue' \
  --output text)
```

Use the output rather than reconstructing the queue URL. Inspect the deployed
queue directly:

```sh
aws sqs get-queue-attributes \
  --queue-url "$training_queue_url" \
  --attribute-names All \
  --profile "$training_profile" \
  --region "$training_region"

aws sqs list-queue-tags \
  --queue-url "$training_queue_url" \
  --profile "$training_profile" \
  --region "$training_region"
```

Before continuing, establish `CREATE_COMPLETE`, the queue's physical identity,
the 30-second `VisibilityTimeout`, SQS-managed encryption, and the expected
tags. If creation fails, preserve the relevant stack events and diagnose the
failure; do not broaden permissions or continue to the update phase blindly.

## Phase 4: update and compare

Change only `VisibilityTimeoutSeconds` from 30 to 60 by running the deployment
again with otherwise identical arguments:

```sh
aws cloudformation deploy \
  --template-file "$training_template" \
  --stack-name "$training_stack" \
  --parameter-overrides \
    VisibilityTimeoutSeconds=60 \
    "ProjectTagValue=$training_project_tag" \
    "EnvironmentTagValue=$training_environment_tag" \
    "ManagedByTagValue=$training_managed_by_tag" \
  --tags \
    "Project=$training_project_tag" \
    "Environment=$training_environment_tag" \
    "ManagedBy=$training_managed_by_tag" \
    Lab=001-cloudformation-lifecycle \
  --profile "$training_profile" \
  --region "$training_region"
```

Repeat the stack, event, and queue-attribute observations from phase 3. Compare
the result with your prediction. Establish `UPDATE_COMPLETE`, a 60-second
`VisibilityTimeout`, and whether the queue's physical identity changed.

## Phase 5: delete and verify cleanup

Capture the final evidence before deletion, then delete only the named stack:

```sh
aws cloudformation delete-stack \
  --stack-name "$training_stack" \
  --profile "$training_profile" \
  --region "$training_region"

aws cloudformation wait stack-delete-complete \
  --stack-name "$training_stack" \
  --profile "$training_profile" \
  --region "$training_region"
```

Verify both the control-plane and resource outcomes:

```sh
aws cloudformation describe-stacks \
  --stack-name "$training_stack" \
  --profile "$training_profile" \
  --region "$training_region"

aws sqs get-queue-attributes \
  --queue-url "$training_queue_url" \
  --attribute-names All \
  --profile "$training_profile" \
  --region "$training_region"
```

Both commands should report that their exact target no longer exists. An empty
or failed lookup is useful evidence only when the target, account, Region, and
observation time are known. If stack deletion fails or the queue remains,
cleanup is incomplete: retain the failure evidence and resolve the exact
resource deliberately rather than running broader deletion commands.

## Evidence submission

Provide a concise summary rather than a raw terminal transcript. Redact account
IDs and principal session details if the evidence will leave the local trusted
context. Include:

1. Preflight time, profile, selected Region, account-match result, and
   non-sensitive principal description.
2. The local template-validation result.
3. Initial stack status, relevant event sequence, queue identity, observed
   timeout, encryption setting, and tags.
4. Updated stack status, relevant event sequence, queue identity, and observed
   timeout, including whether replacement occurred.
5. Post-deletion observations for the exact stack and queue.
6. A short explanation of which claims came from source, live observation, or
   inference, plus anything unexpected.

## Evaluation criteria

Examiner should assess each criterion as **satisfied**, **not satisfied**, or
**not established** and explain the supporting evidence:

- Preflight established the intended identity, account, and Region before
  mutation.
- The trainee correctly distinguished local validation and intended state from
  deployed-state evidence.
- The created stack and queue matched the required scope, attributes, and tags.
- The update reached `UPDATE_COMPLETE`, produced the required timeout, and was
  compared accurately with the original physical identity.
- Cleanup evidence established absence of both the exact stack and queue in the
  intended account and Region.
- The submission included adequate provenance, identified unexpected results,
  and contained no secrets.

Missing evidence produces **not established**, not an assumed pass or failure.
Any out-of-scope resource, account, Region, or unresolved cleanup obligation is
a material finding.

## Completion boundary

The lab is complete only when the evidence requirements are met and cleanup is
verified. Completion does not prove that unrelated account resources are
absent, authorize another lab, or establish that cached observations remain
current.
