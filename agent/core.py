"""Core agent loop and ReAct-style tool-use logic.

This version keeps a conversation history and, when the model asks to use a tool,
executes the tool and continues the conversation until the model returns a final
answer. The loop is intentionally explicit so it is easy to follow and extend.
"""
from typing import Any, Dict, List

from anthropic import Anthropic

from . import config
from tools import execute_tool, get_tool_schemas


class Agent:
    """Minimal ReAct-style agent with a tool-using loop."""

    def __init__(self):
        self.client = Anthropic(api_key=config.get_anthropic_api_key())
        self.model = config.get_model_name()
        self.messages: List[Dict[str, Any]] = []

    def _to_anthropic_messages(self) -> List[Dict[str, Any]]:
        """Convert our internal message history to Anthropic's message format."""
        anthropic_messages: List[Dict[str, Any]] = []
        for message in self.messages:
            role = message["role"]
            content = message.get("content")

            if isinstance(content, list):
                anthropic_messages.append({"role": role, "content": content})
            elif isinstance(content, str):
                anthropic_messages.append({"role": role, "content": [{"type": "text", "text": content}]})
            else:
                anthropic_messages.append({"role": role, "content": [{"type": "text", "text": str(content)}]})

        return anthropic_messages

    def _extract_text(self, response) -> str:
        """Extract the final text answer from a response object or dict."""
        if isinstance(response, dict):
            if "content" in response:
                content = response["content"]
            else:
                return response.get("text", "")
        else:
            content = getattr(response, "content", [])

        text_parts: List[str] = []
        for block in content or []:
            if isinstance(block, dict) and block.get("type") == "text":
                text_parts.append(block.get("text", ""))

        return "\n".join(text_parts).strip()

    def chat(self, user_message: str) -> str:
        """Send a user message and continue until the model produces a final answer."""
        self.messages.append({"role": "user", "content": user_message})

        for _ in range(5):
            anthropic_messages = self._to_anthropic_messages()
            response = self.client.messages.create(
                model=self.model,
                messages=anthropic_messages,
                max_tokens=1024,
                tools=get_tool_schemas(),
            )

            stop_reason = getattr(response, "stop_reason", None)

            if stop_reason == "tool_use":
                tool_calls = [
                    block for block in getattr(response, "content", []) if isinstance(block, dict) and block.get("type") == "tool_use"
                ]

                if not tool_calls:
                    break

                # Keep the tool call visible in the CLI so the reasoning loop stays inspectable.
                for tool_call in tool_calls:
                    print(f"Tool call: {tool_call['name']} | input={tool_call.get('input', {})}")

                # Store the assistant's tool call before we send back the tool result.
                self.messages.append({"role": "assistant", "content": tool_calls})

                tool_results = []
                for tool_call in tool_calls:
                    tool_name = tool_call.get("name")
                    tool_input = tool_call.get("input", {})
                    tool_result = execute_tool(tool_name, tool_input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_call.get("id"),
                            "content": tool_result,
                        }
                    )

                # Anthropic expects tool results to come back as a user message.
                self.messages.append({"role": "user", "content": tool_results})
                continue

            assistant_text = self._extract_text(response)
            if assistant_text:
                self.messages.append({"role": "assistant", "content": assistant_text})
                return assistant_text

            return "No response received."

        return "The agent loop stopped before producing a final response."
