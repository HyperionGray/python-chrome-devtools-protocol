# Security Scanning Setup Guide

This document provides instructions for setting up automated security scanning for the PyCDP project.

## Overview

Automated security scanning helps identify vulnerabilities in dependencies, detect hardcoded secrets, and ensure code follows security best practices.

## Recommended Security Tools

### 1. Dependabot (GitHub Native)

Dependabot automatically checks for dependency vulnerabilities and creates pull requests to update vulnerable dependencies.

**Setup:**
1. Go to your repository's Settings → Security & analysis
2. Enable "Dependabot alerts"
3. Enable "Dependabot security updates"
4. (Optional) Enable "Dependabot version updates"

**Configuration:** Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "your-team"
    labels:
      - "dependencies"
      - "security"
```

### 2. CodeQL (GitHub Native)

CodeQL performs semantic code analysis to find security vulnerabilities.

**Setup:**
Create `.github/workflows/codeql-analysis.yml`:

```yaml
name: "CodeQL"

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: python

    - name: Autobuild
      uses: github/codeql-action/autobuild@v3

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
```

### 3. Safety (Python Dependency Scanner)

Safety checks Python dependencies for known security vulnerabilities.

**Installation:**
```bash
poetry add --group dev safety
```

**Usage:**
```bash
poetry run safety check
```

**CI Integration:** Add to your workflow:

```yaml
- name: Check dependencies for vulnerabilities
  run: poetry run safety check --json
```

### 4. Bandit (Python Security Linter)

Bandit finds common security issues in Python code.

**Installation:**
```bash
poetry add --group dev bandit
```

**Usage:**
```bash
poetry run bandit -r cdp/ generator/ -ll
```

**Configuration:** Create `.bandit`:

```yaml
exclude_dirs:
  - /test/
  - /docs/
tests:
  - B201  # Flask debug mode
  - B301  # Pickle usage
  - B302  # Marshal usage
  - B303  # MD5/SHA1 usage
  - B304  # Insecure ciphers
  - B305  # Insecure cipher modes
  - B306  # mktemp usage
  - B307  # eval usage
  - B308  # mark_safe usage
  - B309  # HTTPSConnection
  - B310  # URL open
  - B311  # Random usage
  - B312  # Telnet usage
  - B313  # XML parsing vulnerabilities
  - B314  - B320  # XML vulnerabilities
  - B321  # FTP usage
  - B323  # Unverified SSL context
  - B324  # Insecure hash functions
  - B325  # Tempfile usage
  - B401  - B413  # Import vulnerabilities
  - B501  - B509  # Crypto issues
  - B601  - B612  # Shell/subprocess issues
  - B701  # Jinja2 autoescape
  - B702  - B703  # Mako templates
```

### 5. pip-audit (Python Package Auditing)

pip-audit scans Python packages for known vulnerabilities.

**Installation:**
```bash
pip install pip-audit
```

**Usage:**
```bash
pip-audit
```

### 6. Secret Scanning (GitHub Native)

GitHub automatically scans repositories for known types of secrets.

**Setup:**
1. Go to repository Settings → Security & analysis
2. Enable "Secret scanning"
3. Enable "Push protection" to prevent accidental secret commits

### 7. Trivy (Container & Dependency Scanner)

Trivy scans for vulnerabilities in dependencies and containers.

**Usage:**
```bash
trivy fs --severity HIGH,CRITICAL .
```

## Recommended CI/CD Security Workflow

Create `.github/workflows/security.yml`:

```yaml
name: Security Scanning

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]
  schedule:
    - cron: '0 0 * * 1'  # Weekly

jobs:
  security:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install Poetry
      uses: snok/install-poetry@v1
    
    - name: Install dependencies
      run: poetry install
    
    - name: Run Safety
      run: poetry run safety check --json
      continue-on-error: true
    
    - name: Run Bandit
      run: poetry run bandit -r cdp/ generator/ -ll
      continue-on-error: true
    
    - name: Run pip-audit
      run: |
        pip install pip-audit
        pip-audit
      continue-on-error: true
```

## Best Practices

### 1. Keep Dependencies Updated
- Regularly update dependencies with `poetry update`
- Review and merge Dependabot PRs promptly
- Test updates in a staging environment first

### 2. Validate User Input
- Always validate and sanitize external inputs
- Use parameterized queries for database operations
- Validate WebSocket messages received from browsers

### 3. Secure Credential Management
- Never commit secrets to version control
- Use environment variables for sensitive data
- Use secrets management services (AWS Secrets Manager, HashiCorp Vault, etc.)

### 4. Code Review
- Require code reviews for all changes
- Use automated security checks in CI/CD
- Review security alerts promptly

### 5. Regular Audits
- Run security scans regularly (weekly/monthly)
- Review security advisories for dependencies
- Perform periodic manual security reviews

## Amazon Q Developer Integration

To enable Amazon Q for enhanced security scanning:

### Prerequisites
- AWS account with Amazon Q Developer access
- AWS credentials configured

### Setup Steps

1. **Install Amazon Q CLI** (when available):
   ```bash
   # Follow AWS documentation for installation
   aws configure  # Configure AWS credentials
   ```

2. **Configure Repository Access:**
   - Add AWS credentials to repository secrets:
     - `AWS_ACCESS_KEY_ID`
     - `AWS_SECRET_ACCESS_KEY`
     - `AWS_REGION`

3. **Enable Amazon CodeWhisperer:**
   - Install CodeWhisperer IDE extension
   - Configure for security scanning
   - Review security findings regularly

4. **Custom Review Rules:**
   - Define project-specific security rules
   - Configure scanning frequency
   - Set up notification channels

### Amazon Q Workflow Integration

Create `.github/workflows/amazonq-security.yml`:

```yaml
name: Amazon Q Security Review

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  amazonq-review:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Configure AWS Credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Run Amazon Q Security Scan
      run: |
        # Amazon Q CLI commands (when available)
        echo "Amazon Q integration pending CLI availability"
    
    - name: Upload Security Report
      uses: actions/upload-artifact@v4
      with:
        name: amazonq-security-report
        path: security-report.json
```

## Monitoring and Response

### Security Alert Handling

1. **Critical/High Severity:**
   - Review immediately
   - Patch within 24-48 hours
   - Deploy hotfix if necessary

2. **Medium Severity:**
   - Review within 1 week
   - Plan patch for next release
   - Document mitigation steps

3. **Low Severity:**
   - Review during regular maintenance
   - Update in next minor release
   - Add to backlog if not urgent

### Incident Response

If a security vulnerability is discovered:

1. Assess severity and impact
2. Create a private security advisory
3. Develop and test a fix
4. Coordinate disclosure with affected parties
5. Release patch and security advisory
6. Update SECURITY.md with details

## Resources

- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [AWS Security Best Practices](https://aws.amazon.com/security/best-practices/)
- [Chrome DevTools Protocol Security](https://chromedevtools.github.io/devtools-protocol/)

## Contact

For security concerns, please see [SECURITY.md](SECURITY.md) for reporting procedures.
