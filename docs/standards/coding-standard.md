---
doc_id: LUD-STD-003
title: Coding Standard
revision: "1.0"
status: baselined
owner: Project lead
---

# Coding Standard

## 1. Purpose

This standard defines the rules for Ludus source code. It is applied in the code review
([SVP](../plans/svp.md), section 5.3) and, where possible, by automated checks in CI.

## 2. Rules for all languages

1. Every source file starts with SPDX headers:

   <!-- REUSE-IgnoreStart -->

   ```text
   SPDX-FileCopyrightText: <year> <copyright holder>
   SPDX-License-Identifier: <license>
   ```

   <!-- REUSE-IgnoreEnd -->

   written as comments in the language of the file. Files that cannot carry comments are
   covered by `REUSE.toml`.
2. Every function or module element that implements a requirement carries an `Implements:`
   trace tag (LUD-STD-001, section 9).
3. Compiler and linter warnings are errors. A warning may be suppressed only on the line
   concerned, with a comment that gives the reason.
4. No dead code. Commented-out code is not committed.
5. Every failure of an external call (system call, library call, subprocess, file access) is
   handled explicitly.
6. Input from files, the network, other processes and less privileged components is
   validated before use.
7. Secrets and personal data are never logged or committed.
8. Coverage exclusion markers are used only in the categories listed in the SVP,
   section 7.3.

## 3. C

### 3.1 Base rules

1. Language: C11. GNU extensions are allowed only where the Linux kernel or the eBPF
   toolchain requires them.
2. Kernel and eBPF code follows the
   [Linux kernel coding style](https://docs.kernel.org/process/coding-style.html). Where that
   style conflicts with a rule of section 3.2, the kernel style takes precedence for
   formatting and the conflict is recorded as a deviation for rules of substance.
3. User-space C code is formatted with `clang-format` using the configuration committed with
   the first C component.

### 3.2 MISRA C

1. LAL-1 and LAL-2 C code follows **MISRA C:2012** (with its published amendments), applied
   by reference. The guideline text is copyrighted and is not reproduced in this repository.
2. Compliance is managed with the **MISRA Compliance:2020** process: a guideline
   re-categorization plan, a guideline enforcement plan naming the analysis tool for each
   guideline, recorded deviations with rationale, and a guideline compliance summary in the
   SAS of each release that contains C code.
3. Mandatory guidelines are never deviated. Required guidelines may be deviated only through
   a recorded deviation approved in review. Advisory guidelines may be disapplied in the
   re-categorization plan.
4. The analysis tool and the enforcement plan are selected before gate G1 and recorded in a
   decision record. Until then no LAL-1 or LAL-2 C code is merged.

### 3.3 Additional rules for LAL-1

1. No dynamic memory allocation after initialization, except where the kernel interface
   requires it, in which case every allocation failure path is tested.
2. No recursion.
3. Every loop has a statically determinable upper bound.
4. Every function has a single, documented error convention.
5. Concurrency: shared data is accessed only under the locking rules stated in the LLR.

## 4. Rust

Rust is allowed only as described in [ADR-0005](../architecture/adr/0005-language-policy.md).
When allowed:

1. `cargo fmt` and `cargo clippy` with warnings as errors.
2. `unsafe` blocks carry a `SAFETY:` comment that states the invariants relied on, and are
   listed in the design of the component.
3. `panic!`, `unwrap` and `expect` are not used on paths reachable from external input.

## 5. Python

Python is used for process tools and LAL-3 components.

1. Python 3.13. Formatting and linting with `ruff`, type checking with `mypy --strict`, as
   configured in [`pyproject.toml`](../../pyproject.toml).
2. Line length 100.
3. No `type: ignore` comments; use `typing.cast` with a narrowed value where needed.
4. Lint suppressions (`noqa`) name the rule and the reason on the same line.
5. Subprocesses are run with a fixed argument list, never through a shell.
6. Files are read with an explicit encoding (UTF-8).

## 6. Shell

1. POSIX `sh` for hooks and small scripts. Scripts that need more than about 30 lines are
   written in Python.
2. Variables are quoted. Scripts start with `set -eu` where the logic allows it.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
