---
| name | description | category | revision | tags |
| :--- | :--- | :--- | :--- | :--- |
| security-governance | Zero-trust authentication standards and PII scrubbing rules for the fleet. | security | 1 | security,governance,pii |

---

# 🛡️ Security Governance Pattern

All agents operating in the Cockpit must adhere to the following security protocols.

## 1. Authentication
All internal API calls MUST use the **Cockpit Identity (JWT)** issued during `agent-ops certify`.
- **Validation**: `agent-ops audit security` verifies that `Authorization` headers are present and valid.

## 2. PII Scrubbing
Before data leaves the local VPC, it MUST pass through the **Cockpit Proxy**.
- **Rule**: No raw emails, SSNs, or API keys in completion payloads.
- **Verification**: The `SecurityAuditor` logic automatically scans egress telemetry for pattern matches.

## 3. Auditing Check
Failure to comply with these rules will trigger a **Blocker Gate** during the `zero2hero` release cycle.
