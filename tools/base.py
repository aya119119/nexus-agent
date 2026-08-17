"""Base tool contract and plugin pattern.

How to add a new tool:
1. Create a new subclass of Tool in tools/.
2. Give it a unique name, description, and JSON schema.
3. Implement run(**kwargs) and keep all I/O and validation inside the tool.
4. Register the instance in tools/__init__.py; the rest of the app calls the registry generically.
"""
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
