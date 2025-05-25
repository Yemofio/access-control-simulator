# Security Controls

## Authentication

- JWT with RS256 asymmetric signing
- Short-lived tokens (1 hour)
- Scope-based access control

## Authorization

- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- Mandatory Access Control (MAC)

## Data Protection

- Encryption at rest (AES-256)
- TLS 1.3 for all communications
- Secrets management with HashiCorp Vault

## Threat Mitigation

- Brute force detection
- Anomalous time access alerts
- Suspicious pattern recognition
- Automated IP blocking

## Compliance

- Designed to meet NIST 800-53 controls
- Audit logging for all access decisions
- Principle of least privilege enforcement