from types import SimpleNamespace

import pytest

from agent.core import Agent
from tools import execute_tool
from tools.web_search import WebSearchTool


def test_web_search_tool_returns_non_empty_string():
    result = WebSearchTool().run(query="python")
    assert isinstance(result, str)
    assert len(result.strip()) > 0


def test_execute_tool_dispatches_by_name(monkeypatch):
    class DummyTool:
        name = "dummy_tool"
        description = "dummy tool"
        input_schema = {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}

        def run(self, **kwargs):
            return "done: " + kwargs["query"]

    monkeypatch.setattr("tools.registry", {"dummy_tool": DummyTool()})
    assert execute_tool("dummy_tool", {"query": "hello"}) == "done: hello"


def test_agent_react_loop_calls_tool_and_follows_up(monkeypatch):
    calls = []

    class FakeTool:
        name = "web_search"
        description = "Search the web"
        input_schema = {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}

        def run(self, **kwargs):
            calls.append(("run", kwargs))
            return "Search result for: " + kwargs["query"]

    # The first response asks for tool use, the second ends normally.
    first_response = SimpleNamespace(
        stop_reason="tool_use",
        content=[
            {
                "type": "tool_use",
                "id": "toolu_1",
                "name": "web_search",
                "input": {"query": "python"},
            }
        ],
    )
    second_response = SimpleNamespace(
        stop_reason="end_turn",
        content=[{"type": "text", "text": "final answer"}],
    )

    fake_client = SimpleNamespace()
    fake_client.messages = SimpleNamespace(create=lambda **kwargs: first_response if len(calls) == 0 else second_response)

    monkeypatch.setattr("tools.registry", {"web_search": FakeTool()})
    monkeypatch.setattr("agent.core.Anthropic", lambda api_key=None: fake_client)

    agent = Agent()
    answer = agent.chat("Find info about Python")

    assert answer == "final answer"
    assert calls == [("run", {"query": "python"})]
