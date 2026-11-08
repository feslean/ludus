---
doc_id: LUD-STD-004
title: Documentation Standard
revision: "1.0"
status: baselined
owner: Project lead
---

# Documentation Standard

## 1. Purpose

This standard defines how Ludus controlled documents are identified, revised, registered and
linked. Rules marked **(checked)** are enforced by the document checker (tool T-002,
[LUD-PRC-002](../process/tool-qualification.md)) on every pull request.

## 2. Scope

1. Every Markdown file under `docs/` is a **controlled document**. **(checked)**
2. Files outside `docs/` (for example `README.md`, `CONTRIBUTING.md`, `SECURITY.md`) are
   project files under configuration control but not controlled documents; they do not
   carry front matter. Their relative links are still checked. **(checked)**
3. A controlled document that is the authoritative source of a rule must not be contradicted
   by a project file. Where they differ, the controlled document applies and the project file
   is corrected.

## 3. Identifiers

Document identifiers have the form `LUD-XXX-NNN` or, for decision records, `LUD-ADR-NNNN`
**(checked)**. Identifiers are unique **(checked)** and never reused.

| Category | Code | Examples |
|---|---|---|
| Project management, register, pitch | `PRJ` | Register, roadmap, risks, glossary, pitch |
| Plans | `PLN` | PSAA, SDP, SVP, SCMP, SQAP |
| Standards | `STD` | Requirements, design, coding, documentation |
| Processes | `PRC` | Problem reporting, tool qualification, release |
| Security | `SEC` | Vulnerability management, threat model, advisories |
| Architecture | `ARC` | Architecture overview |
| Decision records | `ADR` | ADR-0001 is `LUD-ADR-0001` |
| Verification | `VER` | Traceability matrix, analyses |
| Release records | `REL` | SCI, SAS |

## 4. Front matter

Every controlled document starts with a front matter block **(checked)**:

```yaml
---
doc_id: LUD-STD-004
title: Documentation Standard
revision: "1.0"
status: baselined
owner: Project lead
---
```

1. The block starts on the first line with `---` and ends with a line `---`. **(checked)**
2. The keys `doc_id`, `title`, `revision`, `status` and `owner` are present and not empty.
   **(checked)** Each key is on one line as `key: value`.
3. `owner` names a role, not a person, so that ownership survives changes of maintainers.

## 5. Revisions and status

1. Revisions are written `MAJOR.MINOR` and quoted. A change that alters a rule, an obligation
   or a decision increases `MAJOR` once per baseline cycle and resets `MINOR`; editorial
   changes increase `MINOR`. Documents in `draft` use revisions below `1.0`.
2. Generated documents and release records use the release version as revision (for example
   `"0.1.0"`).
3. Document status is one of **(checked)**:

   | Status | Meaning |
   |---|---|
   | `draft` | Work in progress; not yet a basis for other work |
   | `in-review` | Proposed for baselining in an open pull request |
   | `baselined` | Approved and in force |
   | `superseded` | Replaced; the revision history names the successor |

## 6. Revision history

Every controlled document ends with a section `## Revision history` containing a table with
the columns `Revision`, `Date` and `Description` **(checked: the section and at least one
entry exist)**. The last row is the current revision and must equal the front matter
revision **(checked)**. Rows are never deleted. The Git history remains the complete record
of changes; the table records the revisions that matter to readers.

## 7. Document register

The [Document Register](../README.md) (LUD-PRJ-000) lists every controlled document with its
identifier, title and path **(checked: every identifier appears in the register)**. Adding,
renaming or superseding a document updates the register in the same pull request.

## 8. Links

1. Links between files in the repository are relative Markdown links. Absolute paths
   starting with `/` are not used. **(checked)**
2. Every relative link resolves to an existing file or directory. **(checked)** Links in
   fenced code blocks and code spans are not checked.
3. External links use `https://` and point to stable locations (specification versions,
   permanent documentation pages).

## 9. Writing rules

1. Write in English, in short, direct sentences. Use the terms of the
   [Glossary](../project/glossary.md).
2. "Shall" is reserved for requirements in `requirements/`. Plans and standards use "must",
   "is" or the imperative.
3. Do not reproduce copyrighted standards. Refer to them by title, edition and section topic.
4. State limitations and open items plainly. A document must not claim compliance,
   certification, performance or adoption that has not been demonstrated.
5. Numbers about third-party products cite their source.

## 10. Generated documents

Generated documents (currently the [Traceability Matrix](../verification/traceability-matrix.md))
are produced by a tool, committed, and checked in CI against a fresh generation. They are
never edited by hand.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
