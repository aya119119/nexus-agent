"""Configuration helpers for the agent.

Loads environment variables (via python-dotenv) and exposes key constants.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the project root if present.
load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")
SANDBOX_DIR = Path(__file__).resolve().parent.parent / "agent_workspace"
SANDBOX_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = SANDBOX_DIR / "conversations.db"


def get_anthropic_api_key() -> str:
    """Return the Anthropic API key or raise a clear error if it is missing."""
    api_key = os.getenv("ANTHROPIC_API_KEY") or ANTHROPIC_API_KEY
    if not api_key:
        raise RuntimeError(
            "Missing ANTHROPIC_API_KEY. Copy .env.example to .env and set your Anthropic key."
        )
    return api_key


def get_model_name() -> str:
    """Return the configured model name."""
    return os.getenv("ANTHROPIC_MODEL", MODEL_NAME)
