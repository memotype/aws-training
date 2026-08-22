<!--
SPDX-FileCopyrightText: 2026 Isaac Freeman <memotype@gmail.com>
SPDX-License-Identifier: CC-BY-4.0
-->

# Maintainer Post-Merge Cleanup Instructions

Complete post-merge cleanup for the following already-completed work:

- Repository: `<owner>/<repository>`
- Pull request: `#<pull-request-number>`
- Related Issue: `#<issue-number>`
- Issue branch: `<issue-branch>`

Replace every placeholder with the exact intended value before using this
prompt.

This task separately authorizes the local Git and GitHub cleanup operations
defined in section 6.4 of `MAINTAINER.md` for only the named repository, pull
request, Issue, and Issue branch. It authorizes the read-only GitHub discovery
and relevant ref refresh required by that procedure, switching the checkout to
the canonical default branch, updating that branch by fast-forward only, and
safe deletion of only the named Issue branch locally and remotely. It does not
authorize repository-content changes, merging, Issue mutation, or cleanup of
any other ref.

Invoke section 6.4 completely. Resolve the expected repository, unique matching
remote, and current canonical default branch rather than assuming their names.
Verify every publication, Issue-completion, clean-checkout, ref-identity, and
ancestry precondition before deletion. Stop without cleanup if the pull request
was not merge-committed, state is unexpected, work is unpublished, a ref
changed, or any check fails.

Do not use force deletion, force-push, reset, rebase, stash, history rewriting,
destructive restoration, or broad pruning. Do not create commits; modify
repository files, pull requests, Issues, tags, or releases; access AWS; or
perform any unrelated mutation.

After cleanup, report:

- starting branch and repository status
- resolved remote and expected GitHub repository identity
- pull-request, Issue, and canonical-publication evidence
- local and applicable remote Issue-tip ancestry results
- canonical default-branch commit and synchronization result
- local and remote Issue-branch deletion results
- final branch and repository status
- verification that the old Issue branch is absent locally and remotely

Stop after cleanup and verification.
