# Threat Model

## Assets

- API keys and provider credentials.
- Agent prompts and tool outputs.
- Trace database.
- Local filesystem and network reachable from tools.

## Trust Boundaries

- Agent to AgentLab Gateway.
- AgentLab to external LLM provider.
- AgentLab to future tool execution sandbox.
- Browser UI to backend API.

## MVP Mitigations

- Secret redaction before trace persistence.
- Centralized provider abstraction.
- Deterministic policy/risk logic.
- No host shell execution in the current MVP.

