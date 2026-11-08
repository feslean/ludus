# Governance

This document describes the roles in the Ludus project and how decisions are made.

## Roles

| Role | Responsibilities | Held by |
|---|---|---|
| Contributor | Proposes changes through issues and pull requests | Anyone |
| Maintainer | Reviews and merges pull requests, triages issues, is a code owner | See [MAINTAINERS.md](MAINTAINERS.md) |
| Project lead | Owns the plans and standards, approves changes to them, breaks ties | See [MAINTAINERS.md](MAINTAINERS.md) |
| Security lead | Runs the [vulnerability management process](docs/security/vulnerability-management.md) | See [MAINTAINERS.md](MAINTAINERS.md) |
| Quality assurance | Audits process conformance at gates and releases ([SQAP](docs/plans/sqap.md)) | A maintainer other than the author of the item |
| Release manager | Prepares and tags releases ([Release Process](docs/process/release-process.md)) | A maintainer |

Document owners named in front matter (for example "Architecture lead") are roles. While a
role has not been assigned, it is held by the project lead.

## Decision making

1. **Everyday changes** are decided in pull requests. A pull request is merged when it meets
   the pass criteria of the [SVP](docs/plans/svp.md), section 11.
2. **Significant design decisions** are recorded as decision records
   ([Design Standard](docs/standards/design-standard.md), section 3) and accepted by lazy
   consensus among maintainers: a proposal open for at least seven days without a sustained
   objection is accepted.
3. **Changes to plans and standards** need the approval of the project lead.
4. **Disagreements** that consensus cannot resolve are decided by the project lead, who
   records the reasoning in the pull request or decision record.

## Independence

The plans require that reviews of LAL-1 and LAL-2 items be performed by someone other than
the author. A maintainer never approves their own pull request. While the project has only
one maintainer, this requirement cannot be met; the deviation (D-002) is recorded in the
[PSAA](docs/plans/psaa.md), and LAL-1 code is not merged until a second maintainer can review
it.

## Becoming a maintainer

A contributor with a record of high-quality contributions and reviews may be nominated by a
maintainer. The nomination is accepted by lazy consensus among maintainers and recorded in
[MAINTAINERS.md](MAINTAINERS.md) by pull request.

## Changes to this document

Changes to this document need the approval of the project lead and are announced in the
changelog.
