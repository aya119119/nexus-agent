from abc import ABC, abstractmethod


class Tool(ABC):
    """Base interface every tool must implement.

    Future tools (file I/O, code execution, calendar access, etc.) should all
    subclass this and expose a consistent schema so the agent loop can call them
    generically.
    """

    name: str = ""
    description: str = ""
    input_schema: dict = {}

    @abstractmethod
    def run(self, **kwargs) -> str:
        """Execute the tool and return a readable string result."""
        raise NotImplementedError
