# Changelog

All notable changes to Ludus are documented in this file.

The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/), and the
project uses [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). The rules for
this file are in the [SCMP](docs/plans/scmp.md), section 7.

## [Unreleased]

## [0.1.0] - 2026-11-08

Planning baseline. This release contains no product code.

### Added

- Plan for Software Aspects of Assurance (PSAA) defining Ludus Assurance Levels LAL-1 to
  LAL-3, the life cycle data and the deviations D-001 to D-004 from the DO-178C process model.
- Software Development, Verification, Configuration Management and Quality Assurance Plans.
- Requirements, Design, Coding and Documentation Standards.
- Problem Reporting, Tool Qualification and Release processes.
- Vulnerability Management Process, draft Threat Model, advisory index and template.
- Architecture Overview (draft) and decision records ADR-0001 to ADR-0007.
- Roadmap with review gates G0 to G3, risk register, glossary and project pitch.
- Requirements baseline: 10 system requirements, 35 high-level requirements for the process
  tools and 12 draft high-level requirements for the flight recorder.
- Process tools: traceability checker and matrix generator (T-001), document checker (T-002),
  commit message checker (T-003) and release checker (T-004), with 171 tests at 100%
  statement and branch coverage.
- Generated requirements traceability matrix.
- Continuous integration running all checks on every pull request; security scanning with
  CodeQL and OSV-Scanner; Dependabot configuration.
- Issue templates for problem reports and change requests, pull request template, optional
  `commit-msg` hook.
- Software Configuration Index and Software Accomplishment Summary for 0.1.0.
