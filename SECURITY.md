# Security Policy

## Supported Versions

We take security seriously and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.5.x   | :white_check_mark: |
| 0.4.x   | :white_check_mark: |
| < 0.4   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in PyCDP, please help us by responsibly disclosing it to us.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by:

1. **Creating a private security advisory** on GitHub:
   - Go to the [Security tab](https://github.com/HyperionGray/python-chrome-devtools-protocol/security)
   - Click "Report a vulnerability"
   - Provide detailed information about the vulnerability

2. **Or by emailing** the maintainers directly:
   - Include "SECURITY" in the subject line
   - Provide a detailed description of the vulnerability
   - Include steps to reproduce the issue
   - Suggest a fix if possible

### What to Include

When reporting a vulnerability, please include:

- Type of vulnerability (e.g., injection, XSS, authentication bypass)
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability and potential attack scenarios

### What to Expect

- **Initial Response**: We aim to acknowledge receipt within 48 hours
- **Status Updates**: We'll keep you informed about our progress
- **Disclosure Timeline**: We'll work with you to understand the issue and develop a fix
- **Credit**: We'll acknowledge your contribution in release notes (unless you prefer to remain anonymous)

## Security Best Practices

When using PyCDP:

### WebSocket Connections

- **Always use TLS/SSL** for WebSocket connections in production (`wss://` not `ws://`)
- **Validate endpoint URLs** before connecting
- **Authenticate connections** properly to Chrome DevTools endpoints
- **Limit exposure** of CDP endpoints (use `--remote-debugging-port` carefully)

### Input Validation

- **Sanitize inputs** when sending commands to Chrome DevTools
- **Validate responses** from the browser
- **Handle errors gracefully** to prevent information disclosure

### Dependency Management

- **Keep dependencies up to date** using `poetry update`
- **Review security advisories** for dependencies
- **Use the optional `[io]` extra** only when needed to minimize dependency surface

### Access Control

- **Restrict access** to CDP endpoints to trusted clients only
- **Use proper authentication** when exposing CDP over a network
- **Monitor connections** for suspicious activity

## Security Considerations

### Chrome DevTools Protocol

The Chrome DevTools Protocol provides powerful control over browser instances:

- **Full DOM access**: Can read and modify page content
- **JavaScript execution**: Can execute arbitrary JavaScript in pages
- **Network interception**: Can intercept and modify network requests
- **Cookie access**: Can read and modify cookies
- **Storage access**: Can read and modify localStorage, sessionStorage, etc.

### Important Warnings

⚠️ **Never expose CDP endpoints to untrusted networks without authentication**

⚠️ **Be cautious when connecting to untrusted CDP endpoints**

⚠️ **Validate all data received from CDP to prevent injection attacks**

⚠️ **Do not store sensitive credentials in CDP commands or scripts**

## Known Security Considerations

### WebSocket Security

- WebSocket connections do not follow same-origin policy
- Ensure proper origin validation for CDP endpoints
- Use secure WebSocket connections (WSS) in production

### Code Execution

- CDP allows arbitrary JavaScript execution
- Validate and sanitize any user input before executing
- Be aware of potential for remote code execution vulnerabilities

## Updates and Patches

Security updates will be released as:

- **Patch versions** for critical security fixes
- **GitHub Security Advisories** for documented vulnerabilities
- **CHANGELOG.md** entries for all security-related changes

Subscribe to repository notifications to stay informed about security updates.

## Additional Resources

- [Chrome DevTools Protocol Documentation](https://chromedevtools.github.io/devtools-protocol/)
- [OWASP WebSocket Security](https://owasp.org/www-community/vulnerabilities/WebSocket_Security)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## Contact

For non-security issues, please use GitHub issues.

For security concerns, please use the private reporting methods described above.

Thank you for helping keep PyCDP and its users safe!
