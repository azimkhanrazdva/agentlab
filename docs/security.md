# Security

Current controls:

- API keys are never required for local demo mode.
- Common bearer tokens, GitHub tokens, AWS access keys, JWTs, private keys and password-like values are redacted before trace storage.
- Tool actions can be evaluated with deterministic risk scoring.
- Unknown high-risk actions default to ask or deny.

Current limitations:

- Human approval is not implemented yet.
- Demo tools are not executable yet.
- Attack scenarios are declarative seeds only.
- Do not run untrusted commands through future tool adapters without sandboxing.

