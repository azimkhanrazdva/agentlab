from dataclasses import dataclass
from fnmatch import fnmatch
from typing import Literal

PolicyDecision = Literal["allow", "ask", "deny"]
RiskLevel = Literal["low", "medium", "high", "critical"]


@dataclass(frozen=True)
class ToolAction:
    tool: str
    operation: str
    resource: str = ""
    arguments: dict[str, object] | None = None
    side_effect: bool = False
    network_target: str | None = None
    filesystem_target: str | None = None
    risk: int = 0


DEFAULT_POLICIES: dict[str, PolicyDecision] = {
    "demo.read_file": "allow",
    "demo.write_file": "ask",
    "demo.http_request": "allow",
    "demo.shell": "ask",
    "secrets.read": "deny",
}


def risk_level(score: int) -> RiskLevel:
    if score <= 20:
        return "low"
    if score <= 50:
        return "medium"
    if score <= 80:
        return "high"
    return "critical"


def score_action(action: ToolAction) -> int:
    score = action.risk
    if action.side_effect:
        score += 25
    if action.network_target and not action.network_target.startswith(("localhost", "127.0.0.1")):
        score += 25
    if action.filesystem_target and any(part in action.filesystem_target for part in ("..", "~/.ssh", ".env")):
        score += 40
    command = str((action.arguments or {}).get("command", ""))
    dangerous = ["rm -rf", "curl * | sh", "sudo ", "chmod 777", "git push"]
    if any(fnmatch(command, pattern) or pattern.replace("*", "") in command for pattern in dangerous):
        score += 45
    return min(score, 100)


def decide(action: ToolAction, policies: dict[str, PolicyDecision] | None = None) -> PolicyDecision:
    rules = policies or DEFAULT_POLICIES
    key = f"{action.tool}.{action.operation}"
    if action.risk >= 80:
        return "deny"
    if action.risk >= 40:
        return "ask"
    if key in rules:
        return rules[key]
    if action.risk >= 30 or action.side_effect:
        return "ask"
    return "allow"
