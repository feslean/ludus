---
doc_id: LUD-PLN-003
title: Software Verification Plan (SVP)
revision: "1.0"
status: baselined
owner: Project lead
---

# Software Verification Plan (SVP)

## 1. Purpose

This plan defines how Ludus shows that its software satisfies its requirements, that the
requirements are correct and complete enough to be verified, and that no unintended function
exists. It refines the [PSAA](psaa.md) (LUD-PLN-001) and applies to every component at every
Ludus Assurance Level (LAL).

## 2. Verification objectives by LAL

| Activity | LAL-1 | LAL-2 | LAL-3 |
|---|---|---|---|
| Requirements review (section 5.1) | Independent | Independent | Any maintainer |
| Design review (section 5.2) | Independent | Independent | Any maintainer |
| Code review (section 5.3) | Independent | Independent | Any maintainer |
| Review of verification cases (section 5.4) | Independent | Independent | Any maintainer |
| Requirements-based tests, normal range (section 6) | Required | Required | Required |
| Requirements-based tests, robustness (section 6) | Required | Required | Required |
| Statement coverage 100% (section 7) | Required | Required | Required |
| Decision coverage 100% (section 7) | Required | Required | Not required |
| MC/DC 100% (section 7) | Required | Not required | Not required |
| Data coupling and control coupling analysis (section 7.4) | Required | Required | Required |
| Source to object code correspondence | Not performed (deviation D-001) | Not required | Not required |

"Independent" means that the review or verification is performed by a person other than the
author of the item. While the project has one maintainer, this objective is not met
(deviation D-002 in the PSAA, section 7); every pull request then records the self-review
checklist instead, and LAL-1 code is not merged.

## 3. Verification methods

The verification methods allowed in requirements (LUD-STD-001, section 4) are:

| Method | Meaning | Evidence |
|---|---|---|
| `test` | Execution of the software with defined inputs and expected results | Test case with a `Verifies:` tag; CI result |
| `analysis` | Mathematical, statistical or tool-based examination | Analysis report under `docs/verification/` |
| `review` | Qualitative examination of an item against a checklist | Pull request review record |
| `inspection` | Examination of an item for the presence of required properties | Checker output or recorded inspection |

A requirement may list several methods. A requirement with `test` among its methods is not
`implemented` until at least one test case references it; the traceability checker enforces
this (requirement `HLR-TRC-010`).

## 4. Verification environment

- Automated verification runs in GitHub Actions on every pull request and on every push to
  `main`, using the workflow [`ci.yml`](../../.github/workflows/ci.yml).
- The same checks run locally with `make check`. A contributor must run them before
  requesting review.
- Tool versions are pinned in [`requirements-dev.txt`](../../requirements-dev.txt) and
  recorded in the SCI of each release.
- Hardware-dependent tests (from phase 1) run on reference machines whose configuration is
  recorded in the SCI. Results from machines that are not recorded are informative only.

## 5. Reviews

Each review is recorded in the pull request that introduces the item: the reviewer approves
the pull request and confirms the checklist in the pull request template. Findings are
resolved before merge or recorded as problem reports
([LUD-PRC-001](../process/problem-reporting.md)).

### 5.1 Requirements review checklist

1. The requirement conforms to the [Requirements Standard](../standards/requirements-standard.md).
2. The statement is unambiguous, verifiable and contains one obligation.
3. The requirement is consistent with its parents and with other requirements.
4. The verification method is feasible and appropriate.
5. Derived requirements have a rationale and have been considered for safety and security
   effects.
6. The assurance level is correct for the effect of a failure (PSAA, section 4).

### 5.2 Design review checklist

1. The design implements all allocated requirements and no unrequested behavior.
2. Privilege boundaries, data flows and failure modes are identified.
3. Partitioning between components of different LAL is shown or the higher LAL is applied.
4. The design conforms to the [Design Standard](../standards/design-standard.md).
5. Decisions with alternatives are recorded as decision records.

### 5.3 Code review checklist

1. The code implements its requirements and its `Implements:` tags are complete and correct.
2. The code conforms to the [Coding Standard](../standards/coding-standard.md), including any
   recorded deviations.
3. Error handling covers every failure of an external call.
4. No dead code is present; deactivated code is documented (section 7.3).
5. Untrusted input is validated before use.
6. Secrets, credentials and personal data are not logged or committed.

### 5.4 Verification case review checklist

1. Every requirement in scope has test cases or another recorded verification.
2. Test cases cover normal range and robustness (invalid, boundary and failure inputs).
3. Expected results are derived from the requirement, not from the code under test.
4. `Verifies:` tags are complete and correct.

## 6. Requirements-based testing

1. Test cases are derived from requirements. Every test function carries a `Verifies:` tag
   (LUD-STD-001, section 9) on the line immediately above the function or its first
   decorator.
2. For each requirement verified by test, the test set covers the normal range and the
   robustness range: invalid input, boundary values, missing or unreadable files and failing
   external calls.
3. Tests are deterministic. A test that depends on time, randomness or the environment
   controls that dependency explicitly (fixed seeds, temporary directories, isolated git
   configuration).
4. A test that fails intermittently is a problem report. It is not retried automatically and
   not disabled without an approved change request.

## 7. Structural coverage analysis

Structural coverage analysis shows that the requirements-based tests exercised the code
structure and finds code that no requirement asks for.

### 7.1 Measurement

| Language | Statement | Decision | MC/DC | Tool |
|---|---|---|---|---|
| Python | Yes | Branch coverage as an approximation of decision coverage (section 7.2) | Not available | coverage.py with `branch = true` |
| C | Yes | Yes | Masking MC/DC | GCC 14 or later with `--coverage -fcondition-coverage`, reported by `gcov --conditions` |

For kernel and eBPF code, which cannot be instrumented in place, coverage is measured by
building the same translation units in a user-space test harness with the instrumented host
compiler. The harness design is part of the phase 1 design review.

Coverage thresholds are enforced in CI: `fail_under = 100` in
[`pyproject.toml`](../../pyproject.toml) for the process tools.

### 7.2 Known measurement limitations

- coverage.py measures branches between lines. It does not measure Boolean expressions that
  are not branch points (for example a Boolean assignment or a conditional expression on one
  line). For LAL-2 Python code, the code review (section 5.3) confirms that each such
  expression is exercised with both outcomes by the requirements-based tests.
- Masking MC/DC as implemented by GCC is one accepted form of MC/DC. The form used is
  recorded in each coverage report.

### 7.3 Coverage gaps and exclusions

A coverage gap is resolved in one of these ways, recorded in the pull request:

1. **Missing test**: add a requirements-based test.
2. **Missing requirement**: the code implements something no requirement asks for. Write the
   requirement (often derived) or remove the code.
3. **Dead code**: remove it.
4. **Deactivated code**: code that is intentionally not executed in a configuration. It is
   documented in the design with the configurations in which it is active and verified in
   those configurations.

Exclusion markers (such as `# pragma: no cover`) are allowed only for the categories below.
Every other use is a coding standard violation.

| Category | Allowed form | Justification |
|---|---|---|
| E-1 | `if __name__ == "__main__":  # pragma: no cover` followed only by `sys.exit(main())` | The guarded statement only calls `main()`, which is fully covered by tests through its return value |

### 7.4 Data coupling and control coupling

Data and control coupling between components is analysed against the interface descriptions
of the design (LUD-STD-002). For each interface the analysis shows that integration tests
exercise every data item passed and every call path between the components. The process
tools in 0.1.0 have no inter-component interfaces other than the configuration file and the
command line, which are exercised by the tests of each tool.

## 8. Regression testing policy

1. **Every fixed problem report gets a regression test.** The test reproduces the failure,
   fails before the fix and passes after it. It carries a `Verifies:` tag for the requirement
   that the problem violated and names the problem report number in its docstring or comment.
   If the problem revealed a missing requirement, the requirement is written first.
2. **Location.** Regression tests for a component live next to the component's other tests.
   Cross-component and end-to-end regression tests live in
   [`tests/regression/`](../../tests/regression/README.md).
3. **Every change runs the full suite.** CI runs every test on every pull request and on
   every push to `main`. There is no reduced or selective suite for merging.
4. **Tests are not deleted silently.** Removing or weakening a test needs a change request
   that names the requirement the test verified and how that requirement remains verified.
5. **Security fixes.** A regression test for a vulnerability is added in the same pull
   request as the fix. If the test would disclose an unfixed vulnerability, it is added in the
   private fork used for the fix (LUD-SEC-001) and becomes public with the fix.
6. **Performance regressions** are measured with the reference benchmark procedure of
   section 9. A statistically significant increase in mean frame time attributable to Ludus is
   a problem report.

## 9. Reference benchmark procedure

This procedure defines the "reference benchmark sessions" named in performance requirements
such as `HLR-FRC-005`. It applies from phase 1.

1. **Benchmark set.** The reference benchmark set is listed in a controlled file
   `tests/performance/benchmarks.toml` (added in phase 1). It contains at least five
   workloads with deterministic built-in benchmark modes, covering: Direct3D 11 through DXVK,
   Direct3D 12 through vkd3d-proton, native Vulkan, one CPU-bound and one GPU-bound case.
2. **Machines.** Each run uses a reference machine recorded in the SCI, with the same kernel,
   drivers, firmware settings and power profile for both conditions.
3. **Conditions.** Condition A is the session without the component under test; condition B
   is the same session with it enabled. Nothing else differs.
4. **Runs.** One warm-up run per condition is discarded. Then at least 10 runs per condition
   are executed in alternating order (A, B, A, B, ...) to cancel thermal and background
   drift. The mean frame time of each run is computed from presentation timestamps.
5. **Statistic.** For each workload, the relative increase in mean frame time of B over A is
   computed per run pair. The acceptance statistic is the upper bound of the one-sided 95%
   confidence interval of the mean relative increase, from a paired t-interval, or from a
   bootstrap with 10,000 resamples where the paired differences are clearly not normal.
6. **Acceptance.** A budget of *p* percent (1.0 for `HLR-FRC-005`) is met when the acceptance
   statistic is at most *p* for every workload in the set.
7. **Records.** Raw frame times, the analysis script version and the result are stored as a
   verification record and summarized in the SAS of the release.

## 10. Verification records

| Record | Location |
|---|---|
| Review records | Pull request reviews and checklists |
| Test and coverage results | CI logs and coverage reports for the commit; summarized in the SAS |
| Trace data | [Traceability Matrix](../verification/traceability-matrix.md), regenerated for every change |
| Analyses | `docs/verification/` |
| Benchmark records | Attached to the release and summarized in the SAS |

## 11. Pass criteria for a change

A pull request may be merged when:

1. `make check` passes in CI (lint, type check, tests with 100% coverage, traceability,
   documents, licensing, release consistency);
2. the commit message check passes for every commit in the pull request;
3. the reviews required for the LAL of the changed items are recorded;
4. no review finding is open.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
