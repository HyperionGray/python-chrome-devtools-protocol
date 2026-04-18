# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- CONTRIBUTING.md with contribution guidelines
- CODE_OF_CONDUCT.md following Contributor Covenant
- SECURITY.md with security policy
- This CHANGELOG.md file

## [0.5.0] - 2023

### Added
- I/O Mode: New `cdp.connection` module with WebSocket I/O support
- WebSocket management with async context managers
- JSON-RPC message framing
- Command multiplexing
- Event handling with async iterators
- Comprehensive error handling with typed exceptions

### Changed
- Enhanced documentation with I/O mode examples
- Updated README with usage for both Sans-I/O and I/O modes

## [0.4.x and earlier]

### Features
- Sans-I/O mode with type wrappers for Chrome DevTools Protocol
- Auto-generated Python bindings from CDP specification
- Type hints for all CDP commands, events, and types
- Support for all CDP domains
- Documentation on ReadTheDocs
- Example scripts demonstrating CDP usage

---

For a complete list of changes, see the [commit history](https://github.com/HyperionGray/python-chrome-devtools-protocol/commits/master).

[Unreleased]: https://github.com/HyperionGray/python-chrome-devtools-protocol/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/HyperionGray/python-chrome-devtools-protocol/releases/tag/v0.5.0
