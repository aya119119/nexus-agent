"""Core agent loop and simple chat interface.

Keeps a local message history and forwards messages to Anthropic.
"""
from typing import List, Dict
from anthropic import Anthropic
from . import config


class Agent:
    """A minimal agent that holds conversation history and queries Anthropic.

    This is intentionally minimal: no tools, no streaming, no memory systems.
    """

    def __init__(self):
        self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        self.model = config.MODEL_NAME
        self.messages: List[Dict[str, str]] = []

    def chat(self, user_message: str) -> str:
        """Send a user message and return the assistant's reply.

        Appends messages to self.messages with roles 'user' and 'assistant'.
        """
        # Append user message
        self.messages.append({"role": "user", "content": user_message})

        # Convert our simple messages into Anthropic's expected structure
        anthropic_messages = []
        for m in self.messages:
            if m["role"] == "user":
                anthropic_messages.append({"type": "user", "text": m["content"]})
            else:
                anthropic_messages.append({"type": "assistant", "text": m["content"]})

        # Call Anthropic
        resp = self.client.messages.create(
            model=self.model,
            messages=anthropic_messages,
            max_tokens=1024,
        )

        # The SDK returns a structure; extract text
        assistant_text = resp.get("completion") or resp.get("message", {}).get("content", "")
        if not assistant_text and isinstance(resp, dict):
            # fallback common key
            assistant_text = resp.get("text", "")

        # Append assistant reply to history
        self.messages.append({"role": "assistant", "content": assistant_text})

        return assistant_text
