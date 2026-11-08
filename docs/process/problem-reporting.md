---
doc_id: LUD-PRC-001
title: Problem Reporting and Corrective Action Process
revision: "1.0"
status: baselined
owner: Project lead
---

# Problem Reporting and Corrective Action Process

## 1. Purpose

This process records, assesses, fixes and closes every deviation of Ludus software, its
requirements or its life cycle data from what the plans and standards require. It is part of
configuration management ([SCMP](../plans/scmp.md), section 4.1).

Suspected **security vulnerabilities are not reported through this process.** They are
reported privately under [LUD-SEC-001](../security/vulnerability-management.md), and enter
this process only when the advisory is published.

## 2. What is a problem report

A problem report is a GitHub issue opened with the *Problem report* template and labelled
`problem-report`. It is raised for:

- software behavior that differs from a requirement;
- a requirement that is wrong, ambiguous, incomplete or not verifiable;
- a deviation from a plan or standard (including findings of reviews and of quality
  assurance, label `qa-finding`);
- a defect in a tool listed in the [Tool Qualification Plan](tool-qualification.md);
- an intermittent test failure.

## 3. Content

| Field | Content |
|---|---|
| Summary | One sentence |
| Affected version | Release or commit |
| Affected items | Requirements, code, documents, tests |
| Observed behavior | What happened, with logs or reproduction steps |
| Expected behavior | What should have happened, with the requirement or rule |
| Classification | Section 4 (set during triage) |
| Assurance level | Highest LAL of the affected items |

## 4. Classification

| Class | Definition | Response |
|---|---|---|
| PR-1 Safety | Can cause data loss, system instability, security exposure or loss of rollback, or affects LAL-1 code | Fix before the next release; a release containing a known PR-1 problem is not made |
| PR-2 Functional | Software does not meet a requirement, without PR-1 effects | Fix or justify in the SAS of the next release |
| PR-3 Process | Life cycle data or process deviation without a software defect | Fix or justify in the SAS of the next release |
| PR-4 Editorial | Wording, typography, formatting | Fix when convenient |

## 5. Workflow

```text
 open --> triaged --> in-progress --> fixed --> verified --> closed
             |                                       |
             +--> rejected (with reason)             +--> reopened
```

1. **Open.** Anyone opens a problem report.
2. **Triaged.** A maintainer confirms it, sets the class and the affected items, and links
   duplicates. Rejected reports record the reason.
3. **In progress.** A fix is developed on a topic branch.
4. **Fixed.** The fix is merged. The pull request contains:
   - the change, with a `fix` commit whose `Refs:` trailer names the issue;
   - a regression test ([SVP](../plans/svp.md), section 8);
   - corrected requirements or documents where the problem was in them;
   - a `Fixed` entry in the `[Unreleased]` section of the changelog when users can see the
     problem.
5. **Verified.** A maintainer other than the author of the fix confirms that the regression
   test fails without the fix and passes with it (while deviation D-002 is open, the author
   records this check).
6. **Closed.** The issue is closed with a link to the fixing commit.

## 6. Open problem reports at release

Every PR-1 and PR-2 problem report open at a release is listed in the SAS of the release
with its justification. No release is made with an open PR-1 report.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
