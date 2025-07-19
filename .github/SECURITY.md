# Security Policy

## Supported Versions

We provide security updates for the following versions of the project:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

### Reporting Process

If you discover a security vulnerability in this project, please report it by emailing [SECURITY_EMAIL].

In your report, please include:

- A description of the vulnerability
- Steps to reproduce the issue
- Any potential impact of the vulnerability
- Any suggested mitigations or fixes

We will acknowledge receipt of your report within 48 hours and will send a more detailed response within 72 hours indicating the next steps in handling your report.

### Disclosure Policy

- Once the security team has verified the vulnerability, we will work on a fix as soon as possible.
- We will notify you when the vulnerability has been fixed.
- After the fix is released, we will publish a security advisory on our GitHub repository.
- We aim to fix critical security issues within 30 days of verification.

### Security Updates

Security updates will be released as patch versions (e.g., 1.0.1, 1.0.2) for the latest minor version.

### Scope

This security policy applies to all code in the main repository and any first-party packages.

## Secure Development

### Dependencies

We regularly update our dependencies to ensure known vulnerabilities are patched. You can check for any known vulnerabilities in our dependencies by running:

```bash
# Example command to check for vulnerabilities
pip install safety
safety check
```

### Reporting Security Issues in Dependencies

If you find a security issue in one of our dependencies, please report it to the appropriate package maintainers first, then notify us so we can update to a secure version.

## Credits

We would like to thank the security researchers and users who report security vulnerabilities to us.
