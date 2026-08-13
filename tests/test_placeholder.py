import os
from agent.core import Agent


def test_agent_initializes(monkeypatch):
    # Ensure an API key is present for initialization
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    a = Agent()
    assert a is not None
    assert hasattr(a, "chat")
