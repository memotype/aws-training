<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Maintainer Post-Merge Completion Instructions

Complete the post-merge lifecycle for the following already-merged work:

- Repository: `<owner>/<repository>`
- Pull request: `#<pull-request-number>`
- Related Issue: `#<issue-number>`
- Issue branch: `<issue-branch>`

Replace every placeholder with the exact intended value before using this
prompt.

This task explicitly authorizes the distinct Issue-completion and branch-cleanup
outcomes defined in section 6.4 of `MAINTAINER.md` together as one ordered
workflow for only the named repository, pull request, Issue, and Issue branch.
It authorizes the required read-only GitHub discovery and relevant ref refresh;
one concise completion comment if no adequate completion update is already
present; closure of the named Issue as completed when it is still open;
switching the checkout to the canonical default branch; updating that branch by
fast-forward only; and safe deletion of only the named Issue branch locally and
remotely when each ref exists. It does not authorize repository-content
changes, merging, reopening an Issue, mutation of any other Issue, or cleanup
of any other ref.

The workflow is resumable. For each expected outcome, inspect current
authoritative state and either perform the outcome or verify that it is already
satisfied before continuing. Verify and do not duplicate an adequate completion
update that is already present. If none exists, add one whether the Issue is
open or already closed as completed; do not reopen a closed Issue to add it. Do
not recreate an Issue branch that is already absent. Treat the named Issue
already closed as completed as an already-satisfied closure outcome, and treat
an initially absent local or remote Issue branch as an already-satisfied
deletion outcome, when the remaining state is consistent.

Invoke section 6.4 completely. Resolve the expected repository, unique matching
remote, and current canonical default branch rather than assuming their names.
Verify every publication, Issue-completion, clean-checkout, ref-identity, and
ancestry precondition before deletion. Stop without further mutation if the
pull request was not merge-committed, the Issue is closed for a reason other
than completed, state is unexpected or contradictory, work is unpublished, an
observed ref changed, or any check fails.

Do not use force deletion, force-push, reset, rebase, stash, history rewriting,
destructive restoration, or broad pruning. Do not create commits; modify
repository files, pull requests, tags, or releases; mutate the named Issue
beyond its bounded completion update and close-as-completed outcome; access
AWS; or perform any unrelated mutation.

After completion and cleanup, report:

- starting branch and repository status
- resolved remote and expected GitHub repository identity
- pull-request, Issue, and canonical-publication evidence
- whether the completion update and Issue closure were performed or already
  satisfied
- local and applicable remote Issue-tip ancestry results
- canonical default-branch commit and synchronization result
- whether each local and remote Issue-branch deletion was performed or already
  satisfied
- final branch and repository status
- final Issue state
- verification that the old Issue branch is absent locally and remotely

Stop after completion, cleanup, and verification.
