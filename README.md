# AgentLab

**Open-source DevTools and security testing platform for AI agents.**

Inspect, control, attack, debug and replay agentic AI systems before they reach production.

AgentLab sits between an agent and the outside world:

```text
Agent -> AgentLab Gateway -> LLM / tools / APIs -> Trace UI
```

## What Works In This MVP

- OpenAI-compatible `POST /v1/chat/completions` gateway.
- Local mock provider, so the demo works without paid API keys.
- Trace persistence with SQLAlchemy and SQLite by default.
- Trace list and trace detail UI in Next.js.
- Deterministic policy/risk evaluator endpoint.
- Executable YAML Attack Lab runner for the included indirect prompt injection scenario.
- Secret redaction for common tokens and keys.
- Basic tests for gateway, policy scoring and redaction.

Planned but not claimed as complete: human approvals, replay comparison, MCP proxy, multi-provider pricing registry.

## Quick Start

```bash
cp .env.example .env
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -e ".[dev]"
uvicorn agentlab_api.main:app --app-dir apps/api --reload
```

In another terminal:

```bash
cd apps/web
npm install
npm run dev
```

Open:

- API: http://localhost:8000
- API docs: http://localhost:8000/docs
- Frontend: http://localhost:3000

Create a trace:

```bash
python examples/basic-agent/main.py
```

Then open http://localhost:3000/traces.

## Docker

```bash
docker compose up --build
```

Frontend: http://localhost:3000  
API: http://localhost:8000

## Gateway Integration

Point an OpenAI-compatible client at AgentLab:

```text
OPENAI_BASE_URL=http://localhost:8000/v1
OPENAI_API_KEY=anything-for-local-mock
```

Minimal curl:

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "content-type: application/json" \
  -d '{"model":"mock/local","messages":[{"role":"user","content":"hello"}]}'
```

## Ollama

Run an OpenAI-compatible Ollama endpoint, then set:

```text
OPENAI_BASE_URL=http://localhost:11434/v1
OPENAI_API_KEY=ollama
```

Restart the API. AgentLab will proxy `/v1/chat/completions` to that endpoint.

## OpenAI-Compatible API

Set:

```text
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your_key
```

AgentLab redacts sensitive headers and common secrets before storing trace payloads.

## Policies

Evaluate a tool action:

```bash
curl http://localhost:8000/api/v1/tools/evaluate \
  -H "content-type: application/json" \
  -d '{"tool":"demo","operation":"shell","arguments":{"command":"rm -rf /tmp/x"},"side_effect":true}'
```

Decisions are `allow`, `ask` or `deny`.

## Attack Scenarios

Scenario definitions are YAML. The included scenario lives at:

```text
examples/vulnerable-agent/scenario.yml
```

Run it:

```bash
curl -X POST http://localhost:8000/api/v1/attacks/run \
  -H "content-type: application/json" \
  -d '{"scenario_path":"examples/vulnerable-agent/scenario.yml"}'
```

The result distinguishes unsafe attempts from prevented compromise.

## Tests

```bash
pytest
ruff check .
mypy apps packages
```

Frontend:

```bash
cd apps/web
npm run build
```

## Architecture

- `apps/api`: FastAPI app, database models and REST/WebSocket endpoints.
- `apps/web`: Next.js dashboard and trace views.
- `packages/gateway`: OpenAI-compatible gateway service.
- `packages/providers`: mock and OpenAI-compatible provider adapters.
- `packages/tracing`: shared trace schemas.
- `packages/policies`: deterministic risk and policy engine.
- `packages/security`: secret detection and redaction.
- `packages/attacks`: reserved for scenario engine.

## Roadmap

- [x] LLM Gateway
- [x] Live trace storage
- [x] Trace list/detail UI
- [x] Basic policy/risk evaluator
- [x] First Attack Lab scenario runner
- [ ] Controlled tool execution
- [ ] Human approval UI
- [ ] Attack Lab runner
- [ ] Replay and model comparison
- [ ] MCP Inspector
- [ ] Memory Inspector
- [ ] OpenTelemetry
- [ ] Plugin SDK

## License

Apache-2.0.
