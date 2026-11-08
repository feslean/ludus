---
doc_id: LUD-ADR-0001
title: "ADR-0001: Record architecture decisions"
revision: "1.0"
status: baselined
owner: Architecture lead
---

# ADR-0001: Record architecture decisions

## Status

Accepted

## Context

Ludus is an open-source project that expects contributors to join and leave over time. The
assurance plans require that design decisions affecting requirements, assurance levels or
plans can be reviewed and traced. Decisions made in chat, issue threads or memory are lost or
cannot be found.

## Decision

We will record every significant design decision as an Architecture Decision Record in
`docs/architecture/adr/`, using the [template](0000-template.md) and the rules of the
[Design Standard](../../standards/design-standard.md), section 3. The format follows the
structure proposed by Michael Nygard (status, context, decision, consequences), with an
added section for alternatives.

## Alternatives considered

- **Design notes in the wiki.** Not versioned with the code and not reviewed in pull
  requests.
- **Decisions only in issue threads.** Hard to find, and the final decision is mixed with
  discussion.

## Consequences

- Decisions are reviewed in pull requests like any other controlled document.
- Superseded decisions remain readable, so the reasons for past designs are not lost.
- Writing a record takes effort, so the Design Standard limits records to significant
  decisions.

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
