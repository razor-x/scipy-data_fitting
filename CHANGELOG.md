# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).
This change log follows the conventions of
[keep a CHANGELOG](http://keepachangelog.com/).

## [Unreleased][Unreleased]

### Changed

- Updated package structure based on [makenew/python-package].
- Add semver constraints to package dependencies.
- Updated development tooling to handle new features.
- Switched from Coveralls to Codecov.
- Switched from Travis CI to CircleCI.

[makenew/python-package]: https://github.com/makenew/python-package

## [0.2.5] / 2016-03-12

### Added

- Add twine and wheel as development dependencies.

## Changed

- Constrain lmfit version less than 0.9.0.

## [0.2.4] / 2014-04-06

### Added

- New README badges.
- Code coverage reports.

### Changed

- README improvements.
- Test improvements.

## [0.2.3] / 2014-04-03

### Added

- Add scipy_data_fitting/figure to packages in setup.py.

### Changed

- Use relative import for core.
- Added reference to GitHub’s .gitignore templates.

## [0.2.2] / 2014-03-29

### Added

- Added lmfit to install_requires.

## [0.2.1] / 2014-03-25

### Fixed

- Fixed error with docstring.

## [0.2.0] / 2014-03-25

### Added

- Added figure subpackage (still in development).

## [0.1.0] / 2014-03-11

- First stable release. No planned API breaking changes.

## [0.0.9] / 2014-02-25

### Changed

- Plot fit line over data points.

## [0.0.8] / 2014-02-23

### Changed

- The values of `min` and `max` (for `limft`) are scaled by `prefix`.

## [0.0.7] / 2014-02-06

### Added

- Added support for errors and error bars.

### Fixed

- Fixed how meta works in `Fit.to_json`.

## [0.0.6] / 2014-02-05

### Fixed

- Remove images from long_description.

## [0.0.5] / 2014-02-05

### Added

- Added `Fit._function` for performance.

## [0.0.4] / 2014-02-04

### Added

- Added basic examples.
- Allow for the case where no fitting parameters are given.
- Added option in Fit.to_json to omit metadata.

### Changed

- New default behavior for Fit.limits.

## [0.0.3] / 2014-02-04

### Added

- Added lmfit support.

## [0.0.2] / 2014-01-30

### Changed

- Clean up tests.

### Fixed

- Added check for README.md in setup.py.

## 0.0.1 / 2014-01-29

- Initial release.

[Unreleased]: https://github.com/razor-x/scipy-data_fitting/compare/v0.2.5...HEAD
[0.2.5]: https://github.com/razor-x/scipy-data_fitting/compare/v0.2.4...v0.2.5
[0.2.4]: https://github.com/razor-x/scipy-data_fitting/compare/v0.2.3...v0.2.4
[0.2.3]: https://github.com/razor-x/scipy-data_fitting/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/razor-x/scipy-data_fitting/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/razor-x/scipy-data_fitting/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/razor-x/scipy-data_fitting/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/razor-x/scipy-data_fitting/compare/v0.0.9...v0.1.0
[0.0.9]: https://github.com/razor-x/scipy-data_fitting/compare/v0.0.8...v0.0.9
[0.0.8]: https://github.com/razor-x/scipy-data_fitting/compare/v0.0.7...v0.0.8
[0.0.7]: https://github.com/razor-x/scipy-data_fitting/compare/v0.0.6...v0.0.7
[0.0.6]: https://github.com/razor-x/scipy-data_fitting/compare/v0.0.5...v0.0.6
[0.0.5]: https://github.com/razor-x/scipy-data_fitting/compare/v0.0.4...v0.0.5
[0.0.4]: https://github.com/razor-x/scipy-data_fitting/compare/v0.0.3...v0.0.4
[0.0.3]: https://github.com/razor-x/scipy-data_fitting/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/razor-x/scipy-data_fitting/compare/v0.0.1...v0.0.2
