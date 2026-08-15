"""Tool registry and execution helpers.

This is intentionally simple: future tools can be added by creating a new Tool
subclass and registering it in the registry below.
"""
from typing import Dict

from tools.base import Tool
from tools.web_search import WebSearchTool

registry: Dict[str, Tool] = {
    WebSearchTool.name: WebSearchTool(),
}


def get_tool_schemas():
    """Return Anthropic-formatted tool definitions for the registry."""
    return [
        {
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.input_schema,
        }
        for tool in registry.values()
    ]


def execute_tool(name: str, tool_input: dict) -> str:
    """Lookup a tool by name and execute it."""
    tool = registry.get(name)
    if tool is None:
        return f"Tool '{name}' is not registered."

    try:
        return tool.run(**tool_input)
    except Exception as exc:  # pragma: no cover - defensive guard
        return f"Tool '{name}' failed: {exc}"
