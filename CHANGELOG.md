# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
This change log follows the conventions of
[keep a CHANGELOG](http://keepachangelog.com/).

## [Unreleased][Unreleased]

## 0.2.5 / 2016-03-12

### Added

- Add twine and wheel as development dependencies.

## Changed

- Constrain lmfit version less than 0.9.0.

## 0.2.0 / 2014-03-25

### Added

- Added figure subpackage (still in development).

## 0.1.0 / 2014-03-11

- First stable release. No planned API breaking changes.

## 0.0.9 / 2014-02-25

### Changed

- Plot fit line over data points.

## 0.0.8 / 2014-02-23

### Changed

- The values of `min` and `max` (for `limft`) are scaled by `prefix`.

## 0.0.7 / 2014-02-06

### Added

- Added support for errors and error bars.

### Fixed

- Fixed how meta works in `Fit.to_json`.

## 0.0.4 / 2014-02-04

### Added

- Added basic examples.
- Allow for the case where no fitting parameters are given.
- Added option in Fit.to_json to omit metadata.

### Changed

- New default behavior for Fit.limits.

## 0.0.3 / 2014-02-04

### Added

- Added lmfit support.

## 0.0.1 / 2014-01-29

- Initial release.

[Unreleased]: https://github.com/razor-x/scipy-data_fitting/compare/v0.2.5...HEAD
