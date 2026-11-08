---
doc_id: LUD-SEC-004
title: Security Advisory Template
revision: "1.0"
status: baselined
owner: Security lead
---

# Security Advisory Template

Copy this file to `YYYY-NNN-short-title.md`, replace the front matter with the advisory's own
values (`doc_id` from `LUD-SEC-1001` upward, `revision: "1.0"`, `status: baselined`), replace
every placeholder in angle brackets, add the advisory to the [index](README.md) and to the
[document register](../../README.md), and delete this paragraph.

## Summary

<One paragraph: what the vulnerability is and what an attacker can achieve.>

## Identifiers

| Item | Value |
|---|---|
| GHSA | `GHSA-xxxx-xxxx-xxxx` |
| CVE | `CVE-YYYY-NNNNN` |
| Severity | <Critical, High, Medium or Low> |
| CVSS 4.0 vector | `CVSS:4.0/...` |
| Affected component and LAL | <component>, <LAL> |
| Affected versions | <range> |
| Fixed in | <version> |
| Weakness | <CWE identifier and name> |

## Impact

<Who is affected, under which configuration, and with what consequence.>

## Preconditions

<What an attacker needs: access, configuration, user interaction.>

## Remediation

<Upgrade instructions. Workarounds for users who cannot upgrade.>

## Fix

<Commit identifiers of the fix and of the regression test.>

## Timeline

| Date | Event |
|---|---|
| YYYY-MM-DD | Report received |
| YYYY-MM-DD | Report acknowledged |
| YYYY-MM-DD | Assessment completed |
| YYYY-MM-DD | Fix released and advisory published |

## Credit

<Reporter name or handle, if they wish to be credited.>

## Revision history

| Revision | Date | Description |
|---|---|---|
| 1.0 | 2026-11-08 | Initial baseline for release 0.1.0. |
