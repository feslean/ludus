# Security Policy

## Reporting a vulnerability

**Do not report security vulnerabilities through public issues, pull requests or
discussions.**

Report them privately through GitHub's private vulnerability reporting: open the
repository's **Security** tab and choose **Report a vulnerability**.

If private reporting is not available, open a public issue that asks for a private contact
**without any details** of the vulnerability.

Please include the affected version or commit, a description of the impact, and steps to
reproduce.

## What to expect

The project is maintained by volunteers. We aim to:

| Step | Target |
|---|---|
| Acknowledge your report | Within 7 days |
| Tell you whether we accept it and how severe it is | Within 14 days |
| Release a fix | 30 days (Critical), 60 days (High) or 90 days (Medium, Low) after assessment |
| Publish the advisory | With the fix, and by default no later than 90 days after your report |

We request a CVE identifier for every accepted vulnerability that affects a released version
and credit you in the advisory if you wish. We will not pursue legal action against good-faith
research reported under this policy.

The full process is the [Vulnerability Management Process](docs/security/vulnerability-management.md).
Published advisories are listed in the [advisory index](docs/security/advisories/README.md).

## Supported versions

While Ludus is at major version 0, only the latest minor release receives security fixes.

| Version | Supported |
|---|---|
| 0.1.x | Yes |

Release 0.1.0 contains process tools and documents only; it contains no product code that
runs on players' machines.
