## Summary

<!-- What does this change do, and why? -->

## References

<!-- Issue numbers and requirement identifiers, for example: Refs: #42, HLR-FRC-009 -->

## Impact analysis

<!-- Required when requirements, design or controlled documents change
     (LUD-PLN-004, section 4.3): affected requirements, code, tests, documents, and the
     verification that must be repeated. -->

## Highest assurance level of the changed items

- [ ] LAL-1
- [ ] LAL-2
- [ ] LAL-3
- [ ] Not applicable (documentation or CI only)

## Author checklist

- [ ] `make check` passes locally.
- [ ] Commit messages follow the SCMP, section 6 (`feat`, `fix` and `perf` commits have a
      `Refs:` trailer), and the branch is rebased on `main` without merge commits.
- [ ] New or changed behavior has an `approved` requirement, and the code has `Implements:`
      tags.
- [ ] Tests cover normal and robustness cases and carry `Verifies:` tags; coverage is 100%.
- [ ] A fix for a problem report includes a regression test that fails without the fix.
- [ ] Changed controlled documents have a new revision and a revision history row.
- [ ] The traceability matrix is regenerated if requirements or tags changed (`make matrix`).
- [ ] `CHANGELOG.md` has an entry under `[Unreleased]` if users or contributors will notice
      the change.
- [ ] No secrets, credentials or personal data are included.

## AI assistance

- [ ] This contribution was prepared with AI assistance. I have reviewed and understand every
      line, and the commits record the assistance.
- [ ] No AI assistance was used.

## Reviewer checklist

<!-- The reviewer completes the checklists of the SVP, section 5, that apply to the changed
     items: requirements (5.1), design (5.2), code (5.3), verification cases (5.4). -->

- [ ] The applicable SVP review checklists are satisfied.
- [ ] The reviewer is not the author of the change.
