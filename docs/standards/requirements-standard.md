---
doc_id: LUD-STD-001
title: Requirements Standard
revision: "1.0"
status: baselined
owner: Project lead
---

# Requirements Standard

## 1. Purpose

This standard defines how Ludus requirements are written, identified, stored and traced. It
applies to every requirement in [`requirements/`](../../requirements/). Rules marked
**(checked)** are enforced by the traceability checker (tool T-001,
[LUD-PRC-002](../process/tool-qualification.md)); the others are checked in the
requirements review ([SVP](../plans/svp.md), section 5.1).

## 2. Scope

The standard covers system requirements, software high-level requirements and software
low-level requirements, and the trace tags that link them to code and verification cases.

## 3. Requirement levels

| Level | Prefix | States | Parent level |
|---|---|---|---|
| System requirement | `SYS` | What Ludus as a whole, or the project process, must achieve | None |
| High-level requirement | `HLR` | What one software component must do, observable at its boundary | `SYS` |
| Low-level requirement | `LLR` | How a component is built, precisely enough to code and review against | `HLR` |

Rules:

1. A system requirement has no parents and cannot be derived. **(checked)**
2. Every HLR has at least one `SYS` parent, every LLR at least one `HLR` parent, unless the
   requirement is derived (section 8). **(checked)**
3. Parents must be at the level directly above. **(checked)**
4. Every `SYS` requirement in status `approved`, `implemented` or `verified` has at least one
   child requirement. **(checked)**

## 4. Attributes

Requirements are TOML tables in an array named `requirement`, one table per requirement:

| Attribute | Type | Mandatory | Content |
|---|---|---|---|
| `id` | string | Yes | Identifier (section 6) **(checked)** |
| `title` | string | Yes | Short name, at most about eight words |
| `statement` | string | Yes | The requirement itself (section 5) |
| `rationale` | string | Yes | Why the requirement exists; references to plans or decision records |
| `verification` | list of strings | Yes | One or more of `test`, `analysis`, `review`, `inspection` **(checked)** |
| `assurance` | string | Yes | `LAL-1`, `LAL-2` or `LAL-3` ([PSAA](../plans/psaa.md), section 4) **(checked)** |
| `status` | string | Yes | Section 7 **(checked)** |
| `parents` | list of strings | HLR and LLR | Parent identifiers **(checked)** |
| `derived` | boolean | No (default `false`) | `true` for a derived requirement (section 8) **(checked)** |
| `derived_rationale` | string | When `derived = true` | Why the requirement is needed although no parent asks for it **(checked)** |

All mandatory string attributes are non-empty **(checked)**. Other attributes are not used;
the checker ignores them, so reviewers reject them.

Example:

```toml
[[requirement]]
id = "HLR-FRC-009"
title = "Block integrity"
statement = "The flight recorder shall protect each written data block with a CRC-32C checksum."
rationale = "Corrupted telemetry must be detected rather than learned from."
verification = ["test"]
assurance = "LAL-2"
status = "draft"
parents = ["SYS-FRC-001"]
```

## 5. Statement rules

1. A statement contains the obligation keyword **shall** exactly once. Each statement
   therefore expresses one obligation. **(checked)** Requirements that would need two
   obligations are split.
2. The subject is the system, the component or the project ("Ludus shall", "The flight
   recorder shall", "The project shall").
3. The statement is verifiable: it names measurable quantities with units and limits, or
   observable behavior. Words such as "fast", "efficient", "user-friendly", "minimal",
   "as appropriate" and "etc." are not used.
4. Conditional behavior is written as "When (or If) *condition*, *subject* shall *behavior*".
5. Negative requirements ("shall not") are allowed when the prohibited behavior is
   observable.
6. A statement does not prescribe design unless the design is itself required (for example
   a file format for interoperability).
7. Defined terms are used as in the [Glossary](../project/glossary.md).
8. References to other documents use their document identifier and, where needed, a section
   number.

## 6. Identifiers

Identifiers have the form `LEVEL-AREA-NNN` **(checked)**:

- `LEVEL` is `SYS`, `HLR` or `LLR`;
- `AREA` is a three-letter code from the table below;
- `NNN` is a three-digit sequence number within the level and area.

| Area | Meaning |
|---|---|
| `PRC` | Project process (system level) |
| `TRC` | Traceability tooling |
| `DOC` | Document control tooling |
| `CMT` | Commit message tooling |
| `REL` | Release tooling |
| `FRC` | Flight recorder |
| `SAF` | Safety of the user's system: rollback, verification before applying changes |
| `SEC` | Security |

New area codes are added to this table by a change to this standard. Identifiers are unique
across all files **(checked)** and are never reused, including after deletion.

## 7. Status life cycle

| Status | Meaning | Entered when |
|---|---|---|
| `draft` | Written, not yet approved | The requirement is first committed |
| `approved` | Reviewed and accepted as a basis for design and code | The requirements review is recorded |
| `implemented` | Code that implements it is merged | Implementing code with `Implements:` tags (HLR, LLR) is merged, and tests with `Verifies:` tags exist if `test` is a verification method **(checked)** |
| `verified` | All verification methods are complete and recorded | The verification results are recorded for a release |
| `deleted` | No longer applies; kept for history | A change request removes the requirement |

Requirements in status `draft` or `approved` are not yet subject to the implementation and
test tag checks; those checks apply from status `implemented`. **(checked)**

A requirement in status `deleted` keeps its identifier and table. Parents and tags must not
reference deleted requirements **(checked)**.

## 8. Derived requirements

A derived requirement is one that is not directly traceable to a parent, usually because a
design decision introduced it. It is marked `derived = true` and has a `derived_rationale`
**(checked)**. Derived requirements are reported to the next gate review for assessment of
their effect on safety and security ([SDP](../plans/sdp.md), section 4.2).

## 9. Trace tags

Code and verification cases reference requirements with trace tags in comment lines:

```text
# Implements: HLR-TRC-001, HLR-TRC-002
# Verifies: HLR-TRC-001
// Implements: LLR-FRC-004
/* Verifies: LLR-FRC-004 */
```

1. A tag is a comment line that contains only the comment marker (`#`, `//`, `--`, `/*` or
   `*`), the keyword `Implements:` or `Verifies:` and one or more identifiers separated by
   commas or spaces. A trailing `*/` is allowed.
2. `Implements:` is placed on the line immediately above the function, method or module
   element that implements the requirement.
3. `Verifies:` is placed on the line immediately above the test function or its first
   decorator.
4. Tags name existing requirements that are not deleted. **(checked)** Malformed identifiers
   in tags are errors. **(checked)**
5. Tags are scanned in the directories and file types configured in `ludus-tools.toml`.
   Text that is not a comment line, such as this document, is never treated as a tag.

## 10. File organization

1. Requirements are stored in TOML files directly in `requirements/`, grouped by level and
   component: `system.toml`, `hlr-<component>.toml`, `llr-<component>.toml`.
2. Each file starts with SPDX headers and a comment stating its scope.
3. Files are UTF-8 encoded, valid TOML and contain at least one requirement table.
   **(checked)**

## 11. Changing requirements

1. A change to an `approved` or later requirement needs a change request and an impact
   analysis ([SCMP](../plans/scmp.md), section 4.3).
2. A changed statement returns the requirement to `approved` at most; downstream code and
   tests are reviewed again before it returns to `implemented`.
3. The traceability matrix is regenerated in the same pull request (`make matrix`).
   **(checked)**: CI fails when the committed matrix is out of date.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
