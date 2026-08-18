"""Simple sanity-check script for the tool registry.

This is a lightweight validation tool for local debugging.
"""
from tools import registry


def main():
    for name, tool in registry.items():
        try:
            if name == "web_search":
                result = tool.run(query="python")
            elif name == "file_read":
                result = tool.run(filename="hello.txt")
            elif name == "file_write":
                result = tool.run(filename="hello.txt", content="hello")
            elif name == "calculator":
                result = tool.run(expression="2 + 2")
            else:
                result = "unknown tool"

            print(f"PASS {name}: {result[:80]}")
        except Exception as exc:  # pragma: no cover - quick sanity check only
            print(f"FAIL {name}: {exc}")


if __name__ == "__main__":
    main()
