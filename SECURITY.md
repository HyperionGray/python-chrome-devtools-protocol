# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in PyCDP, please report it by:

1. **Do NOT** open a public issue
2. Email the maintainers directly (see repository for contact information)
3. Include detailed information about the vulnerability:
   - Description of the issue
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

We will respond to security reports within 48 hours and work with you to address the issue promptly.

## Security Scanning Setup

For information on setting up automated security scanning for this project, see [SECURITY_SETUP.md](SECURITY_SETUP.md).

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.5.x   | :white_check_mark: |
| < 0.5   | :x:                |

---

# Security-Relevant API Updates

This document highlights the security-relevant additions to the Chrome DevTools Protocol implementation in this update.

## Summary

This update brings the python-chrome-devtools-protocol library to the latest CDP specification, adding **8 new domains** and significantly expanding security-relevant APIs, particularly in the Privacy Sandbox area.

## New Security-Focused Domains

### 1. Extensions Domain
**Purpose**: Browser extension management for security testing
- Load and uninstall extensions programmatically
- Manage extension storage (local/sync/managed)
- **Use Case**: Test extension security boundaries, data isolation, and permission handling

### 2. FedCm Domain (Federated Credential Management)
**Purpose**: Test federated authentication flows
- Track and interact with FedCm dialogs
- Programmatically select accounts or dismiss dialogs
- **Use Case**: Verify federated login security, test account selection flows

### 3. DeviceAccess Domain
**Purpose**: Handle device permission prompts
- Track camera, microphone, and other device access requests
- Programmatically grant or deny permissions
- **Use Case**: Test device permission security, verify proper permission prompts

### 4. FileSystem Domain
**Purpose**: File system directory access
- Get directory access for testing File System Access API
- **Use Case**: Test file system permission boundaries

### 5. Autofill, BluetoothEmulation, PWA, Preload Domains
Additional domains for comprehensive browser testing

## Major Security Updates to Existing Domains

### Storage Domain - Privacy Sandbox APIs
The Storage domain received the most significant security-relevant updates:

#### Attribution Reporting API (Privacy-Preserving Ad Measurement)
```python
# Enable tracking and local testing
await conn.execute(storage.set_attribution_reporting_tracking(enable=True))
await conn.execute(storage.set_attribution_reporting_local_testing_mode(enabled=True))

# Send test reports
await conn.execute(storage.send_pending_attribution_reports())

# Listen for events
async for event in conn.listen():
    if isinstance(event, storage.AttributionReportingSourceRegistered):
        print(f"Source registered: {event.registration}")
```

#### Shared Storage API (Cross-Site Storage with Privacy)
```python
# Track shared storage access
await conn.execute(storage.set_shared_storage_tracking(enable=True))

# Get and set entries for testing
metadata = await conn.execute(storage.get_shared_storage_metadata(
    owner_origin="https://example.com"
))

await conn.execute(storage.set_shared_storage_entry(
    owner_origin="https://example.com",
    key="test-key",
    value="test-value"
))
```

#### Interest Groups / FLEDGE / Protected Audience API
```python
# Track interest group auctions
await conn.execute(storage.set_interest_group_tracking(enable=True))
await conn.execute(storage.set_interest_group_auction_tracking(enable=True))

# Get details for security verification
details = await conn.execute(storage.get_interest_group_details(
    owner_origin="https://example.com",
    name="interest-group-name"
))

# Configure k-anonymity for testing
await conn.execute(storage.set_protected_audience_k_anonymity(threshold=50))
```

#### Bounce Tracking Mitigation
```python
# Test bounce tracking mitigation
deleted_sites = await conn.execute(storage.run_bounce_tracking_mitigations())
print(f"Mitigated tracking for {len(deleted_sites)} sites")
```

### Network Domain - Cookie and IP Protection
```python
# Control cookie behavior for third-party cookie testing
await conn.execute(network.set_cookie_controls(mode='block-third-party'))

# Test IP protection features
status = await conn.execute(network.get_ip_protection_proxy_status())
await conn.execute(network.set_ip_protection_proxy_bypass_enabled(enabled=True))

# Get related website sets (First-Party Sets)
sets = await conn.execute(storage.get_related_website_sets())
```

### Audits Domain - Form Security
```python
# Automated form security/privacy issue detection
issues = await conn.execute(audits.check_forms_issues())
for issue in issues:
    print(f"Form issue detected: {issue}")
```

### Browser Domain - Privacy Sandbox Configuration
```python
# Override Privacy Sandbox enrollment for testing
await conn.execute(browser.add_privacy_sandbox_enrollment_override(
    url="https://example.com"
))

# Configure coordinator keys
await conn.execute(browser.add_privacy_sandbox_coordinator_key_config(
    coordinator_origin="https://coordinator.example.com",
    coordinator_key="test-key"
))
```

## Security Testing Use Cases

### 1. Privacy Sandbox Testing
Test the complete Privacy Sandbox suite:
- Attribution Reporting (privacy-preserving conversion measurement)
- Shared Storage (cross-site storage with privacy guarantees)
- Interest Groups/FLEDGE (privacy-preserving ad auctions)
- Topics API (via interest groups)
- k-anonymity thresholds

### 2. Third-Party Cookie Migration
Test alternatives to third-party cookies:
- First-Party Sets (Related Website Sets)
- Partitioned cookies (CHIPS)
- Storage Access API
- Cookie controls and policies

### 3. Authentication Security
- Test FedCm federated login flows
- Verify account selection security
- Test dialog dismissal handling

### 4. Permission Testing
- Verify device permission prompts (camera, mic, etc.)
- Test permission grant/deny flows
- Validate permission persistence

### 5. Extension Security
- Test extension isolation boundaries
- Verify extension data access controls
- Test extension installation/uninstallation

### 6. Anti-Tracking Features
- Test bounce tracking mitigation
- Verify IP protection
- Test tracking prevention measures

### 7. Form Security Auditing
- Automated detection of insecure forms
- Privacy leak detection
- Input validation issues

## Breaking Changes

**Database Domain Removed**: The deprecated Database domain has been removed from the CDP specification. If your code imports `cdp.database`, you must migrate to:
- IndexedDB APIs (`cdp.indexed_db`)
- Storage APIs (`cdp.storage`)
- Cache Storage APIs (`cdp.cache_storage`)

## Implementation Notes

### Generator Improvements
- Fixed same-domain type reference bug (e.g., `Network.TimeSinceEpoch` now correctly resolves to `TimeSinceEpoch` within the network module)
- Added domain context to all type, command, and event generation
- Protected manually-written files (connection.py, util.py) from deletion

### Testing
- All 19 tests passing
- mypy type checking successful (56 modules)
- Generator tests updated and passing (20 tests)

## Migration Guide

### For Users of cdp.database
```python
# Old (no longer works)
from cdp import database
await conn.execute(database.some_command())

# New - Use IndexedDB instead
from cdp import indexed_db
await conn.execute(indexed_db.request_database_names(security_origin="https://example.com"))
```

### For page.navigate() Users
```python
# Old return signature (3 values)
frame_id, loader_id, error_text = await conn.execute(page.navigate(url="..."))

# New return signature (4 values - added isDownload)
frame_id, loader_id, error_text, is_download = await conn.execute(page.navigate(url="..."))
```

## References

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Privacy Sandbox APIs](https://privacysandbox.com/)
- [Attribution Reporting API](https://github.com/WICG/attribution-reporting-api)
- [Shared Storage API](https://github.com/WICG/shared-storage)
- [FLEDGE/Protected Audience](https://github.com/WICG/turtledove)
- [FedCM](https://fedidcg.github.io/FedCM/)

## Examples

See `/tmp/security_examples.py` for comprehensive code examples demonstrating all new security APIs.

## Version Information

- Protocol Version: 1.3 (latest)
- Total Domains: 56 (up from 48)
- New Domains: 8
- Removed Domains: 1 (Database)
- Security-Relevant Updates: 5 domains (Storage, Network, Audits, Browser, Target)
