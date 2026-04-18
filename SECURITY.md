# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.5.x   | :white_check_mark: |
| < 0.5   | :x:                |

## Reporting a Vulnerability

The PyCDP team takes security bugs seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

To report a security vulnerability, please **do not** open a public GitHub issue. Instead:

1. **Email**: Send details to the project maintainers via GitHub by opening a private security advisory at:
   https://github.com/HyperionGray/python-chrome-devtools-protocol/security/advisories/new

2. **Include the following information**:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact
   - Suggested fix (if you have one)
   - Your contact information

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
- **Communication**: We will keep you informed about the progress of fixing the vulnerability
- **Timeline**: We aim to release a fix within 30 days of receiving the report
- **Credit**: We will credit you for the discovery in the release notes (unless you prefer to remain anonymous)

## Security Best Practices for Users

When using PyCDP in your projects:

1. **Keep Updated**: Always use the latest version to benefit from security patches
2. **Validate Input**: Sanitize and validate any data sent to the Chrome DevTools Protocol
3. **Network Security**: When connecting to Chrome instances, use secure connections where possible
4. **Least Privilege**: Run Chrome with minimal privileges necessary
5. **Review Dependencies**: Keep all dependencies up to date

## Known Security Considerations

### WebSocket Connections

PyCDP's I/O mode uses WebSocket connections to communicate with Chrome instances. Be aware:

- **Authentication**: Chrome DevTools Protocol endpoints typically don't have authentication. Ensure your Chrome instance is not exposed to untrusted networks.
- **Data Exposure**: CDP can execute arbitrary JavaScript and access all page data. Only connect to trusted Chrome instances.
- **Network Security**: Use `ws://localhost` for local development. In production, consider additional network security measures.

### Code Execution

The Chrome DevTools Protocol allows arbitrary JavaScript execution in the browser. When using PyCDP:

- Never execute untrusted code through CDP commands
- Validate and sanitize any dynamic content before execution
- Be cautious when using CDP in multi-tenant environments

## Disclosure Policy

When we receive a security bug report, we will:

1. Confirm the problem and determine affected versions
2. Audit code to find similar problems
3. Prepare fixes for all supported versions
4. Release patches as soon as possible
5. Credit the reporter in the release notes

## Comments on This Policy

If you have suggestions on how this process could be improved, please open an issue or pull request.
