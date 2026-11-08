---
doc_id: LUD-STD-002
title: Design Standard
revision: "1.0"
status: baselined
owner: Project lead
---

# Design Standard

## 1. Purpose

This standard defines the content and form of Ludus design data: the architecture
description, decision records, low-level requirements and interface descriptions. It is
applied in the design review ([SVP](../plans/svp.md), section 5.2).

## 2. Architecture description

The [Architecture Overview](../architecture/overview.md) and the per-component design
documents added in later phases describe:

1. the components, their LAL and their responsibilities;
2. the privilege level and process in which each component runs;
3. the data flow and control flow between components, including every interface that
   crosses a privilege or process boundary;
4. the failure modes of each component and how they are contained;
5. resource budgets (CPU time, memory, storage, latency) allocated to each component;
6. partitioning between components of different LAL ([PSAA](../plans/psaa.md),
   section 4.1, rule 4).

Diagrams are written as text (Mermaid in Markdown) so that they are versioned and
reviewable as diffs.

## 3. Decision records

Significant design decisions are recorded as Architecture Decision Records (ADRs) in
[`docs/architecture/adr/`](../architecture/adr/), using the
[template](../architecture/adr/0000-template.md).

1. A decision is significant if it constrains several components, is costly to reverse,
   affects an assurance level, or changes a plan or standard.
2. ADRs are numbered sequentially and never renumbered. Document identifiers are
   `LUD-ADR-NNNN` with the same number.
3. ADR status is one of `Proposed`, `Accepted`, `Deprecated` or `Superseded by ADR-NNNN`.
   This decision status is recorded in the body; the document status in the front matter
   follows the Documentation Standard.
4. An accepted ADR is not rewritten. A changed decision is a new ADR that supersedes the old
   one; the old one is updated only to point to its successor.

## 4. Low-level requirements

LLRs follow the [Requirements Standard](requirements-standard.md). For LAL-1 and LAL-2
components they specify, for each unit:

1. inputs, outputs and their valid ranges;
2. the algorithm or state machine, including all states and transitions;
3. behavior for every invalid input and every failure of a called function;
4. timing and resource limits where the HLR allocates them;
5. concurrency rules: which locks are held, which contexts may call the unit (for kernel
   code: process, softirq, hard interrupt, eBPF program context).

## 5. Interface descriptions

Every interface between components that crosses a privilege or process boundary, and every
persistent file format, has an interface description stating:

1. the data items, their types, units, ranges and byte order;
2. the version of the interface and the compatibility rule for later versions;
3. who validates each item and what happens on invalid data;
4. authentication and authorization of the caller, where applicable.

## 6. Design rules for privileged components

1. Privileged code does the minimum that requires privilege. Policy, parsing of complex
   formats and learning run unprivileged.
2. Data from unprivileged components is treated as untrusted by privileged components.
3. Every privileged operation that changes system state has a defined rollback.
4. eBPF programs are preferred to kernel modules where they can meet the requirement,
   because the kernel verifier bounds their behavior.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
