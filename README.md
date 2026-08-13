# AI Agent

A tool-using AI agent with persistent memory, built from scratch.

## Status

- Agent loop: ✅
- Tools: 🔜
- Memory: 🔜
- UI: 🔜
- Deployment: 🔜

## Setup

1. Clone the repository.
2. Create and activate a virtual environment (Python 3.11+ recommended):

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and add your Anthropic API key.

```bash
cp .env.example .env
```

5. Run the chat CLI:

```bash
python scripts/chat.py
```

## Why this project

This repository is a minimal, educational implementation of an agent loop that will gain tool use and persistent memory over time. The goal is to understand the building blocks of agents — message handling, tool integrations, and memory — from first principles rather than relying on an opinionated framework.
