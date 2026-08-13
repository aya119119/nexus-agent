"""Configuration helpers for the agent.

Loads environment variables (via python-dotenv) and exposes key constants.
"""
from dotenv import load_dotenv
import os

# Load .env from project root if present
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    raise RuntimeError(
        "Missing ANTHROPIC_API_KEY. Copy .env.example to .env and set your Anthropic key."
    )

# Default model name; can be overridden by setting ANTHROPIC_MODEL in env
MODEL_NAME = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
