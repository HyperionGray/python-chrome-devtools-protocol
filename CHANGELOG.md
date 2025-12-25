# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2024-12-XX

### Added
- **I/O Mode**: New `cdp.connection` module providing WebSocket I/O, JSON-RPC framing, and command multiplexing
- **8 New Domains**: Extensions, FedCm, DeviceAccess, FileSystem, Autofill, BluetoothEmulation, PWA, Preload
- **Privacy Sandbox APIs**: Comprehensive support for Attribution Reporting, Shared Storage, Interest Groups/FLEDGE
- Security-focused APIs for testing federated authentication, device permissions, and extension boundaries
- Bounce tracking mitigation testing capabilities
- IP protection proxy status and control
- Related Website Sets (First-Party Sets) support
- Form security issue detection via Audits domain
- Privacy Sandbox enrollment override for testing
- Enhanced cookie controls for third-party cookie testing

### Changed
- Updated to Chrome DevTools Protocol version 1.3 (latest)
- Fixed same-domain type reference bug in code generator (e.g., `Network.TimeSinceEpoch` now correctly resolves)
- Improved code generator to protect manually-written files (connection.py, util.py)
- `page.navigate()` now returns 4 values instead of 3 (added `is_download` parameter)

### Removed
- **Breaking Change**: Removed deprecated Database domain (use IndexedDB, Storage, or Cache Storage APIs instead)

### Security
- Added comprehensive security testing capabilities for Privacy Sandbox
- Enhanced storage domain with privacy-preserving measurement APIs
- Added attribution reporting and shared storage tracking
- Improved form security auditing

## [0.4.0] - Previous Release

### Added
- Initial sans-I/O implementation
- Type wrappers for Chrome DevTools Protocol
- Automatic code generation from CDP specification
- Support for Python 3.7+

## Migration Guide

### From 0.4.x to 0.5.0

#### Database Domain Removed
```python
# Old (no longer works)
from cdp import database
await conn.execute(database.some_command())

# New - Use IndexedDB instead
from cdp import indexed_db
await conn.execute(indexed_db.request_database_names(security_origin="https://example.com"))
```

#### page.navigate() Return Signature Changed
```python
# Old (3 values)
frame_id, loader_id, error_text = await conn.execute(page.navigate(url="..."))

# New (4 values - added is_download)
frame_id, loader_id, error_text, is_download = await conn.execute(page.navigate(url="..."))
```

## Links

- [Repository](https://github.com/HyperionGray/python-chrome-devtools-protocol)
- [Documentation](https://py-cdp.readthedocs.io)
- [PyPI](https://pypi.org/project/chrome-devtools-protocol/)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)

---

For detailed security-relevant updates, see [SECURITY.md](SECURITY.md).
For implementation details, see [IMPLEMENTATION.md](IMPLEMENTATION.md).
