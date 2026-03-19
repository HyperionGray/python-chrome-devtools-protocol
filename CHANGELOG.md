# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CONTRIBUTING.md with contribution guidelines
- CHANGELOG.md for tracking version history
- CODE_OF_CONDUCT.md for community standards
- SECURITY.md with security policy and vulnerability reporting

## [0.5.0]

### Added
- I/O Mode with built-in WebSocket connection support via `cdp.connection` module
- WebSocket management with async context managers
- JSON-RPC message framing and multiplexing
- Event handling via async iterators
- Comprehensive error handling with typed exceptions
- Optional websockets dependency via `[io]` extra

### Changed
- Enhanced README with I/O mode documentation
- Improved examples demonstrating both Sans-I/O and I/O modes

## [0.4.0]

### Changed
- Updated to latest Chrome DevTools Protocol specification
- Improved type hints and mypy compliance
- Enhanced documentation

## [0.3.0]

### Added
- Initial Sans-I/O implementation
- Automatic code generation from CDP specification
- Type wrappers for all CDP types, commands, and events
- Comprehensive test suite

### Changed
- Improved project structure
- Enhanced type safety

## [0.2.0]

### Added
- Enhanced type definitions
- Additional protocol domains

### Fixed
- Various type annotation improvements
- Bug fixes in code generation

## [0.1.0]

### Added
- Initial release
- Basic type wrappers for Chrome DevTools Protocol
- Code generator from CDP specification
- MIT License

[Unreleased]: https://github.com/HyperionGray/python-chrome-devtools-protocol/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/HyperionGray/python-chrome-devtools-protocol/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/HyperionGray/python-chrome-devtools-protocol/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/HyperionGray/python-chrome-devtools-protocol/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/HyperionGray/python-chrome-devtools-protocol/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/HyperionGray/python-chrome-devtools-protocol/releases/tag/v0.1.0
