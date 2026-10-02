# Repository Protection Baseline

This file records the required public-repository protection posture for Signalproof Intelligence.

## Enforced in repository content

- Apache-2.0 LICENSE
- NOTICE and THIRD-PARTY-NOTICES
- SECURITY.md
- PUBLIC-BOUNDARY.md
- CONTRIBUTING.md
- CODEOWNERS for owner review
- pull request checklist
- Community CLI cross-platform test workflow
- public sanitization workflow
- no model-weight/download authority in the Community CLI

## Required GitHub administrative ruleset

For `main`, enable a GitHub branch/ruleset with:

1. require pull requests before merge;
2. require at least one approving review;
3. require Code Owner review;
4. dismiss stale approvals when new commits are pushed;
5. require status checks:
   - Signalproof Community CLI test matrix;
   - Public Sanitization;
6. require conversation resolution;
7. block force pushes;
8. block branch deletion;
9. apply rules to administrators unless an emergency policy explicitly says otherwise.

## Current automation limitation

Repository files and CI can be created through the connected GitHub integration, but repository-admin ruleset mutation is not available through the current connection. Therefore content-level protections can be committed automatically, while the GitHub-hosted `main` ruleset must be enabled through repository settings by an administrator.

Do not describe `main` as administratively protected until GitHub reports an active rule/ruleset.
