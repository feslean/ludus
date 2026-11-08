---
doc_id: LUD-ADR-0005
title: "ADR-0005: Programming languages by assurance level"
revision: "1.0"
status: baselined
owner: Architecture lead
---

# ADR-0005: Programming languages by assurance level

## Status

Accepted

## Context

The SVP requires 100% MC/DC for LAL-1 code and 100% decision coverage for LAL-2 code. A
language can only be used at a level if those coverage measures can be produced with
available tools.

- **C.** GCC 14 added `-fcondition-coverage`, which measures masking MC/DC, reported by
  `gcov --conditions`. Clang also offers MC/DC instrumentation. The Linux kernel and eBPF
  programs are written in C.
- **Rust.** Rust improves memory safety and the kernel accepts Rust code. The experimental
  MC/DC instrumentation in `rustc` was removed in 2025, so MC/DC cannot currently be measured
  for Rust with the standard toolchain. Branch coverage support is also experimental.
- **Python.** coverage.py measures statement and branch coverage, which the SVP accepts as a
  decision coverage measure with the limitations in SVP section 7.2. No MC/DC tool is in
  common use.

## Decision

1. **LAL-1** code is written in C11 and compiled with GCC 14 or later for coverage
   measurement.
2. **LAL-2** code is written in C11, or in Rust once decision coverage for Rust has been
   demonstrated on a pilot component and accepted in a new decision record.
3. **LAL-3** code may use C11, Rust or Python 3.13.
4. **Process tools** are written in Python 3.13 and treated as LAL-2.
5. This record is revisited when MC/DC measurement for Rust becomes available in a stable
   toolchain.

## Alternatives considered

- **Rust at LAL-1.** Rejected until MC/DC can be measured; memory safety does not replace the
  structural coverage objective.
- **C++.** Not needed for any planned component; adds complexity to coding standard and
  coverage analysis.

## Consequences

- LAL-1 code needs the MISRA C discipline of the Coding Standard and careful review for memory
  errors, since C gives no memory safety.
- Fuzzing and sanitizers in test builds become important mitigations for C code at LAL-1.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
