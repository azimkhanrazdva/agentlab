from pathlib import Path

from agentlab_attacks.scenario import load_scenario, run_scenario


def test_indirect_prompt_injection_is_prevented() -> None:
    scenario = load_scenario(Path("examples/vulnerable-agent/scenario.yml"))
    result = run_scenario(scenario)
    assert result.agent_vulnerable
    assert result.compromise_prevented
    assert result.passed
    assert {attempt.resource for attempt in result.attempts} == {"~/.ssh/id_rsa", "attacker.example"}

