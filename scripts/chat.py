"""Simple CLI to talk with the Agent."""
import sys

from memory.db import list_sessions
from agent.core import Agent


def prompt_for_session():
    sessions = list_sessions()
    if not sessions:
        print("No saved sessions found. Starting a new one.")
        return None

    print("Saved sessions:")
    for index, session in enumerate(sessions, start=1):
        print(f"  {index}. {session['title']} | {session['id']}")

    choice = input("Choose a session number, type a session id, or press Enter for a new session: ").strip()
    if not choice:
        return None
    if choice.lower() in {"new", "n"}:
        return None

    for index, session in enumerate(sessions, start=1):
        if str(index) == choice or session["id"] == choice:
            return session["id"]

    print("Session not found. Starting a new one.")
    return None


def main():
    session_id = prompt_for_session()
    try:
        agent = Agent(session_id=session_id)
    except Exception as e:
        print(f"Failed to initialize Agent: {e}")
        sys.exit(1)

    print(f"Session ID: {agent.session_id}")
    print("Agent ready. Type your message and press Enter. Type 'exit' to quit.")
    while True:
        try:
            user = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\nGoodbye. Resume with session ID: {agent.session_id}")
            break

        if not user:
            continue
        if user.lower() in {"exit", "quit"}:
            print(f"Goodbye. Resume with session ID: {agent.session_id}")
            break

        try:
            reply = agent.chat(user)
        except Exception as e:
            print(f"Agent error: {e}")
            continue

        print(f"Agent: {reply}\n")


if __name__ == "__main__":
    main()
