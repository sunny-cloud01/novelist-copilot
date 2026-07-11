# 7. Incident Response

Incident lifecycle:

```text
Detected
↓
Triaged
↓
Contained
↓
Mitigated
↓
Resolved
↓
Postmortem
```

Incident record must include incident_id、severity、detected_at、affected_modules、user_impact、root_cause、mitigation、follow_up_actions。

Severity levels:

- SEV1: production unavailable or data integrity at risk
- SEV2: core pipeline blocked
- SEV3: degraded function with workaround
- SEV4: minor issue or documentation correction
