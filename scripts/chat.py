"""Simple CLI to talk with the Agent."""
import sys

from agent.core import Agent


def main():
    try:
        agent = Agent()
    except Exception as e:
        print(f"Failed to initialize Agent: {e}")
        sys.exit(1)

    print("Agent ready. Type your message and press Enter. Type 'exit' to quit.")
    while True:
        try:
            user = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye")
            break

        if not user:
            continue
        if user.lower() in {"exit", "quit"}:
            print("Goodbye")
            break

        try:
            reply = agent.chat(user)
        except Exception as e:
            print(f"Agent error: {e}")
            continue

        print(f"Agent: {reply}\n")


if __name__ == "__main__":
    main()
