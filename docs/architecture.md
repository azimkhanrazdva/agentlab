# Architecture

AgentLab is split into a small backend core and a read-only frontend.

```text
Agent / app
  -> OpenAI-compatible AgentLab Gateway
  -> provider adapter
  -> trace persistence
  -> REST API
  -> Web UI
```

The MVP stores traces, spans and events. Security logic is deterministic and separate from gateway code, so controlled tool execution can use the same policy engine later.

## Boundaries

- Gateway: accepts OpenAI-compatible calls and records trace spans.
- Providers: translate calls to mock or OpenAI-compatible upstreams.
- Tracing: schemas and persisted trace model.
- Policies: risk scoring and allow/ask/deny decisions.
- Security: secret detection and redaction.
- Attack Lab: scenario definitions first; executable runner next.

