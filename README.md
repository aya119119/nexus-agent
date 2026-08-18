# AI Agent

A tool-using AI agent with persistent memory, built from scratch.

## Status

- Agent loop: ✅
- Web search tool: ✅
- File I/O tool: ✅
- Calculator tool: ✅
- Conversation persistence: ✅
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

## Resuming a session

When the CLI starts, it shows any saved sessions and lets you resume one by number or session ID. Press Enter or type `new` to start a new conversation. The active session ID is printed at startup, and you can use that value later to continue the same chat history without losing earlier context.

## How the tool loop works

The agent begins with a normal user message and sends it to Anthropic with the available tool schemas. If the model decides it needs a tool, the loop captures the tool call, executes it locally, and sends the tool result back to the model as a fresh user message. This pattern — observe, act, reflect — is the essence of a ReAct loop. It keeps the reasoning process grounded in real, executable actions instead of relying on the model to invent answers from memory alone.

## Adding a new tool

1. Create a new Tool subclass in the tools package.
2. Give it a unique name, description, and JSON schema that matches the Anthropic tool format.
3. Implement run(**kwargs) with any validation and safety checks inside the tool itself.
4. Add one registry entry in tools/__init__.py and the agent can use it immediately without any other code changes.

## Why this project

This repository is a minimal, educational implementation of an agent loop that will gain tool use and persistent memory over time. The goal is to understand the building blocks of agents — message handling, tool integrations, and memory — from first principles rather than relying on a framework like LangChain.
