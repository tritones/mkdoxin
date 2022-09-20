<!-- markdownlint-configure-file { "MD024": { "siblings_only": true } } -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

-   Add mypy to pre-commit (<https://github.com/tritones/mkdoxin/pull/24>)

### Changed

-   Updated base image of makedocs-material (<https://github.com/tritones/mkdoxin/pull/29>)

### Fixes

-   Improve logging to match(ish) McDocs (<https://github.com/tritones/mkdoxin/pull/24>)

## [0.1.2] - 2022-09-07

### Added

-   Docker compose! (<https://github.com/tritones/mkdoxin/pull/20>)

### Fixes

-   Avoid GitHub actions running twice (<https://github.com/tritones/mkdoxin/pull/21>)
-   Tweaks to importing environment variables (<https://github.com/tritones/mkdoxin/pull/20>)
-   Add guard in directory delete to ensure directory exists (<https://github.com/tritones/mkdoxin/pull/20>)

## [0.1.1] - 2022-09-06

### Added

-   Introduce semver and nightly docker builds (<https://github.com/tritones/mkdoxin/pull/16>)
-   Improves linting. adds markdownlint, and GH Actions for checks (<https://github.com/tritones/mkdoxin/pull/12>)
-   Implemented `pre-commits` (<https://github.com/tritones/mkdoxin/pull/10>)

## [0.1.0] - 2022-09-01

### Added

-   Initial functionality!
-   Configure Dependabot for Docker, pip, and GitHub Actions
-   Ability to "localize" the site_url
-   Add a simpler scheduler
-   Manual Docker Image build GitHub Action

<!-- Release Links -->

[unreleased]: https://github.com/tritones/mkdoxin/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/tritones/mkdoxin/releases/tag/v0.1.2
[0.1.1]: https://github.com/tritones/mkdoxin/releases/tag/v0.1.1
[0.1.0]: https://github.com/tritones/mkdoxin/releases/tag/v0.1.0
