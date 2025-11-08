# Threat Model - Prompt Firewall

## Overview

This document provides a concise threat model for the Prompt Firewall system, identifying assets, threats, and mitigations.

## Assets

### Data Assets
- **User Prompts**: Input text from users that may contain sensitive information
- **Model Responses**: LLM-generated responses that may leak sensitive data
- **Policy Rules**: Security configuration rules
- **Audit Logs**: Security event logs containing potentially sensitive information
- **Admin Credentials**: Authentication tokens and passwords

### System Assets
- **Backend API**: FastAPI application processing requests
- **Database**: PostgreSQL instance storing logs and policies
- **Frontend Application**: Next.js web application
- **SDK**: Python client library

## Threat Landscape

### 1. Data Exposure (PII/PHI Leakage)
**Threat**: Sensitive information in prompts/responses is exposed to unauthorized parties.

**Risk Level**: HIGH

**Mitigations**:
- PII/PHI detection engine with regex patterns
- Automatic redaction of sensitive data
- Blocking of high-risk requests
- Secure logging with data sanitization
- HTTPS/TLS encryption in transit
- Database encryption at rest

### 2. Prompt Injection Attacks
**Threat**: Malicious users attempt to inject instructions to bypass security controls or extract system information.

**Risk Level**: HIGH

**Mitigations**:
- Pattern-based injection detection
- Heuristic analysis for jailbreak attempts
- Role-playing detection
- Obfuscation detection
- Policy-based blocking/redaction
- Request logging for analysis

### 3. Unauthorized Access
**Threat**: Attackers gain unauthorized access to admin console or API endpoints.

**Risk Level**: MEDIUM

**Mitigations**:
- JWT-based authentication
- Password hashing (bcrypt)
- Admin endpoint protection
- CORS configuration
- Rate limiting (to be implemented)
- Session management
- Secret storage in Secret Manager

### 4. API Abuse / DoS
**Threat**: Attackers overwhelm the API with requests causing denial of service.

**Risk Level**: MEDIUM

**Mitigations**:
- Cloud Run auto-scaling with limits
- Request validation
- Input sanitization
- Timeout configurations
- Cloud Armor (recommended for production)

### 5. Database Compromise
**Threat**: Unauthorized access to database containing logs and sensitive data.

**Risk Level**: MEDIUM

**Mitigations**:
- Private IP configuration for Cloud SQL
- Strong authentication
- Encrypted connections
- Least privilege access
- Regular backups
- Audit logging

### 6. Secret Leakage
**Threat**: API keys, database credentials, or JWT secrets are exposed.

**Risk Level**: HIGH

**Mitigations**:
- Secret Manager for sensitive data
- No secrets in code or environment files
- Regular secret rotation
- Secure secret transmission
- IAM-based access control

### 7. Log Injection / Log Poisoning
**Threat**: Malicious data in logs causes issues in log analysis or storage.

**Risk Level**: LOW

**Mitigations**:
- Input sanitization before logging
- Structured logging
- Log validation
- Separate log storage

### 8. Policy Manipulation
**Threat**: Unauthorized modification of security policies.

**Risk Level**: MEDIUM

**Mitigations**:
- Admin authentication required
- Audit trail for policy changes
- Policy validation
- Version control (future enhancement)

## Security Boundaries

### Trust Boundaries
1. **Public Internet → Frontend**: Users accessing demo UI
2. **Frontend → Backend API**: API calls from frontend
3. **Backend → Database**: Internal database connections
4. **Admin → Admin Console**: Authenticated admin access
5. **SDK → Backend API**: Third-party integrations

### Security Controls at Boundaries
- **Frontend**: CORS, input validation, HTTPS
- **Backend API**: Authentication, authorization, input validation, rate limiting
- **Database**: Private network, encrypted connections, access control
- **Admin Console**: JWT authentication, session management

## Risk Summary

| Threat | Likelihood | Impact | Risk Level | Mitigation Status |
|--------|-----------|--------|-----------|-------------------|
| PII/PHI Leakage | High | High | HIGH | ✅ Implemented |
| Prompt Injection | High | High | HIGH | ✅ Implemented |
| Unauthorized Access | Medium | High | MEDIUM | ✅ Implemented |
| API Abuse/DoS | Medium | Medium | MEDIUM | ⚠️ Partial |
| Database Compromise | Low | High | MEDIUM | ✅ Implemented |
| Secret Leakage | Low | High | HIGH | ✅ Implemented |
| Log Injection | Low | Low | LOW | ✅ Implemented |
| Policy Manipulation | Low | Medium | MEDIUM | ✅ Implemented |

## Recommendations for Production

1. **Enable Rate Limiting**: Implement rate limiting on all endpoints
2. **Cloud Armor**: Enable DDoS protection
3. **WAF**: Consider Web Application Firewall
4. **Monitoring**: Set up alerting for suspicious activity
5. **Penetration Testing**: Regular security audits
6. **Incident Response Plan**: Document procedures for security incidents
7. **Regular Updates**: Keep dependencies updated
8. **Security Headers**: Implement security headers (CSP, HSTS, etc.)
9. **Backup Strategy**: Regular automated backups
10. **Access Reviews**: Regular review of admin access

## Compliance Considerations

- **GDPR**: Data redaction, audit logging, right to deletion
- **HIPAA**: PHI detection and protection
- **SOC 2**: Audit logging, access controls
- **PCI DSS**: If handling payment data (not currently in scope)

---

**Last Updated**: 2024
**Version**: 1.0

