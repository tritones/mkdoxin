# mkdoxin

<p align="center">
  <a href="https://github.com/tritones/mkdoxin">
    <img src="https://raw.githubusercontent.com/tritones/mkdoxin/main/.github/assets/mkdoxin-logo.svg"
      width="250" alt="mkdoxin!">
  </a>
</p>

> _When life gives you docs, make dachshund!_

[![MIT license][license image]][license link]
[![Build Status][build image]][build link]
[![GitHub release][github image]][github link]

mkdoxin takes external documentation repositories and builds them using mkdocs and mkdocs-material.

## Environment

The only required environment variable is `GIT_REPO`, the URL to the remote
repository.

Other, optional, environment variables are:

-   `MAX_REPO_SIZE` (integer) - value in KB, defaults to 1GB (1,000,000 KB)
-   `SCHEDULED_UPDATES` (boolean) - whether to automatically pull updates on a schedule. Defaults
    to `TRUE`.
-   `UPDATE_INTERVAL` (integer) - Only applicable if `SCHEDULED_UPDATES` is `TRUE`. Must be
    greater than `1`, defaults to `1`.
-   `UPDATE_CADENCE` (integer) - Only applicable if `SCHEDULED_UPDATES` is `TRUE`. Valid options
    are: `second`, `seconds`, `minute`, `minutes`, `hour`, `hours`, `day`, `days`, `week`, `weeks`,
    `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, `saturday`, `sunday`. Defaults to
    `day`.
-   `LOCALIZE_SITE_URL` (boolean) - whether to automatically "localize" the `site_url` from
    mkdocs.yml for any redirects. Converts to localhost for self-contained documents. Defaults to
    `TRUE`.\*

_\*Certain docs utilize the plugin [`mkdocs-redirects`][mkdocs-redirects link] and occasionally use
the hardcoded value from `site_url` in various redirect locations to support anchor references
(`#`), which `mkdocs-redirects` does not currently support._

[license image]: https://img.shields.io/badge/License-MIT-blue.svg
[license link]: https://github.com/tritones/mkdoxin/blob/main/LICENSE
[build image]: https://github.com/tritones/mkdoxin/actions/workflows/build-release.yaml/badge.svg?branch=main
[build link]: https://github.com/tritones/mkdoxin/actions/workflows/build-release.yaml
[github image]: https://img.shields.io/github/release/tritones/mkdoxin.svg
[github link]: https://github.com/tritones/mkdoxin/releases
[mkdocs-redirects link]: https://github.com/mkdocs/mkdocs-redirects
