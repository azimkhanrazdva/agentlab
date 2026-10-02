from agentlab_policies.engine import ToolAction, decide, score_action
from agentlab_security.secrets import has_secret, redact_secrets


def test_redacts_common_secret() -> None:
    payload = {"Authorization": "Bearer abcdefghijklmnopqrstuvwxyz123456"}
    assert has_secret(payload)
    assert redact_secrets(payload)["Authorization"] == "[REDACTED]"


def test_scores_dangerous_filesystem_action() -> None:
    action = ToolAction(tool="demo", operation="read_file", filesystem_target="~/.ssh/id_rsa")
    assert score_action(action) >= 40


def test_denies_known_secret_read() -> None:
    action = ToolAction(tool="secrets", operation="read", risk=100)
    assert decide(action) == "deny"

