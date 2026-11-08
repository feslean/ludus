# Regression tests

This directory holds cross-component and end-to-end regression tests. Regression tests for a
single component live next to that component's other tests. The policy is defined in the
[SVP](../../docs/plans/svp.md), section 8.

## Rules

1. Every fixed problem report gets a regression test that fails before the fix and passes
   after it.
2. The test carries a `Verifies:` tag for the requirement the problem violated, and names the
   problem report (for example `#42`) in its docstring.
3. File names start with the problem report number: `test_pr0042_<short_description>.py`.
4. Regression tests are never deleted or weakened without an approved change request.
5. Every test in this directory runs on every pull request.

## Index

| Problem report | Test | Requirement |
|---|---|---|
| None yet | | |

No problem reports have been fixed as of release 0.1.0.
