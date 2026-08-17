"""Tool registry and execution helpers.

The design stays generic: each new tool is a Tool subclass and a single registry
entry. The agent core only calls get_tool_schemas() and execute_tool().
"""
from typing import Dict

from tools.base import Tool
from tools.calculator import CalculatorTool
from tools.file_io import FileReadTool, FileWriteTool
from tools.web_search import WebSearchTool

# Register tools in one place only; adding a new tool is one line here.
registry: Dict[str, Tool] = {
    WebSearchTool.name: WebSearchTool(),
    FileReadTool.name: FileReadTool(),
    FileWriteTool.name: FileWriteTool(),
    CalculatorTool.name: CalculatorTool(),
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
